from wumpus import Robot

import bluetooth
import time
from micropython import const
from ble_advertising import advertising_payload
import rp2
import machine
from machine import Pin, PWM, ADC

# Define BLE constants (these are not packaged in bluetooth for space efficiency)
_IO_CAPABILITY_DISPLAY_ONLY = const(0)
_FLAG_READ = const(0x0002)
_FLAG_WRITE = const(0x0008)

class NanoBotBLE:
    """
    A helpful wraper around the BLE service functions needed for the Wumpus World project
    """
    def __init__(self, ble, name="NANO RP2040"):
        # Setup bluetooth low energy communication service
        _SERVICE_UUID = bluetooth.UUID(0x1523) # unique service id for the communication
        _NanoBot_CHAR_UUID = (bluetooth.UUID(0x1525), _FLAG_WRITE | _FLAG_READ) # characteristic
        _NanoBot_SERVICE = (_SERVICE_UUID, (_NanoBot_CHAR_UUID,),) # service to provide the characteristic

        self._ble = ble
        self._ble.active(True)
        self._ble.config(
            bond=True,
            mitm=True,
            le_secure=True,
            io=_IO_CAPABILITY_DISPLAY_ONLY
        )
        ((self._handle,),) = self._ble.gatts_register_services((_NanoBot_SERVICE,))
        self._connections = set()
        self._payload = advertising_payload(name=name, services=[_SERVICE_UUID])
        self._advertise()

    def _advertise(self, interval_us=500000):
        self._ble.gap_advertise(interval_us, adv_data=self._payload)

    def send(self, value):
        # Writes value (as byte) to characteristic
        if not isinstance(value, bytes):
            if isinstance(value, int):
                value = value.to_bytes(1, "big")
            elif isinstance(value, str):
                value = value.encode('utf-8')
            else:
                raise ValueError("send value should be type bytes, int, or string")
        self._ble.gatts_write(self._handle, value)

    def read(self, as_type="bytes"):
        # reads value from characteristic and returns it as specified type
        value = self._ble.gatts_read(self._handle)
        if as_type == "bytes":
            return value
        elif as_type == "str":
            return value.decode("utf-8")
        elif as_type == "int":
            return int.from_bytes(value, "big")

        raise ValueError("as_type must be one of 'bytes', 'str', or 'int'")



class NanoBot(Robot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # initialize bluetooth
        self.bluetooth = NanoBotBLE(bluetooth.BLE())
        self.encpins = (15, 25, 7, 27)

        # initialize motors
        m1pin1 = Pin(21)
        m1pin2 = Pin(4)
        m2pin1 = Pin(18)
        m2pin2 = Pin(17)

        self.m1pwm1 = PWM(m1pin1)
        self.m1pwm2 = PWM(m1pin2)
        self.m2pwm1 = PWM(m2pin1)
        self.m2pwm2 = PWM(m2pin2)

        # initialize motor constants
        self.max_duty = 65535 # constant
        self.saturated_duty = 20000 # choice for max speed
        self.turn90ticks = 120
        self.turn_error = 10

        # PID controller constants
        self.kp = 0.8
        self.ki = 0.08
        self.kd = 0.04

        # initialize encoder variables
        self.enc1p1 = Pin(self.encpins[0], Pin.IN)
        self.enc1p2 = Pin(self.encpins[1], Pin.IN)
        self.enc2p1 = Pin(self.encpins[2], Pin.IN)
        self.enc2p2 = Pin(self.encpins[3], Pin.IN)

        self.enc1 = 0
        self.enc2 = 0
        self.enc1dir = 1
        self.enc2dir = 1

        # add interrupt callbacks to track encoder ticks
        enc1p1.irq(lambda pin: self.enc_pin_high(encpins[0]), Pin.IRQ_RISING)
        enc1p2.irq(lambda pin: self.enc_pin_high(encpins[1]), Pin.IRQ_RISING)
        enc2p1.irq(lambda pin: self.enc_pin_high(encpins[2]), Pin.IRQ_RISING)
        enc2p2.irq(lambda pin: self.enc_pin_high(encpins[3]), Pin.IRQ_RISING)

        # initialize ir sensors
        ir_left_sensor = ADC(29)
        ir_right_sensor = ADC(28)

    def enc_pin_high(self, pin):
        if pin == self.encpins[0] or pin == self.encpins[1]:
            if self.enc1p1.value() == 1 and self.enc1p2.value() == 1:
                self.enc1 += 1 * self.enc1dir
            elif self.enc1p1.value() == 1:
                self.enc1dir = 1
            else:
                self.enc1dir = -1
        if pin == self.encpins[2] or pin == self.encpins[3]:
            if self.enc2p1.value() == 1 and self.enc2p2.value() == 1:
                self.enc2 += 1 * self.enc2dir
            elif self.enc2p1.value() == 1:
                self.enc2dir = 1
            else:
                self.enc2dir = -1

    def calc_duty(self, duty_100):
        return int(duty_100 * max_duty / 100)

    def m1Forward(self, dutyCycle):
        self.m1pwm1.duty_u16(min(self.calc_duty(dutyCycle), self.saturated_duty))
        self.m1pwm2.duty_u16(0)

    def m1Backward(self, dutyCycle):
        self.m1pwm1.duty_u16(0)
        self.m1pwm2.duty_u16(min(self.calc_duty(dutyCycle), self.saturated_duty))

    def m1Signed(self, dutyCycle):
        if dutyCycle >= 0:
            self.m1Forward(dutyCycle)
        else:
            self.m1Backward(-dutyCycle)

    def m2Forward(self, dutyCycle):
        self.m2pwm1.duty_u16(min(self.calc_duty(dutyCycle), self.saturated_duty))
        self.m2pwm2.duty_u16(0)

    def m2Backward(self, dutyCycle):
        self.m2pwm1.duty_u16(0)
        self.m2pwm2.duty_u16(min(self.calc_duty(dutyCycle), self.saturated_duty))

    def m2Signed(self, dutyCycle):
        if dutyCycle >= 0:
            self.m2Forward(dutyCycle)
        else:
            self.m2Backward(-dutyCycle)

    def allStop():
        # set all duty cycles to 0
        self.m1pwm1.duty_u16(0)
        self.m1pwm2.duty_u16(0)
        self.m2pwm1.duty_u16(0)
        self.m2pwm2.duty_u16(0)

    def setup():
        # initialize frequencies
        self.m1pwm1.freq(1000)
        self.m1pwm2.freq(1000)
        self.m2pwm1.freq(1000)
        self.m2pwm2.freq(1000)

    def rot(self, ccw_dir=1):
        self.enc1 = 0
        self.enc2 = 0
        m1_integral = 0
        m2_integral = 0
        period = 1/10
        m1_last_error = None
        m2_last_error = None
        while abs(self.enc1 - self.turn90ticks * ccw_dir) > self.turn_error or abs(self.enc2 + self.turn90ticks * ccw_dir) > self.turn_error:
            m1_current_error = self.turn90ticks * ccw_dir - self.enc1
            m2_current_error = -self.turn90ticks * ccw_dir - self.enc2
            m1_integral += m1_current_error * period
            m2_integral += m2_current_error * period
            m1_derivative = 0
            if not m1_last_error is None:
                m1_derivative = (m1_current_error - m1_last_error) / period
            m2_derivative = 0
            if not m2_last_error is None:
                m2_derivative = (m2_current_error - m2_last_error) / period
            self.m1Signed(self.kp * m1_current_error + self.ki * m1_integral + self.kd * m1_derivative)
            self.m2Signed(self.kp * m2_current_error + self.ki * m2_integral + self.kd * m2_derivative)
            m1_last_error = m1_current_error
            m2_last_error = m2_current_error
            time.sleep(period)

    def rot_cw(self):
        self.rot(1)

    def rot_ccw(self):
        self.rot(-1)

    def ir_left(self):
        return self.ir_left_sensor.read_u16() < 65535 // 2

    def ir_right(self):
        return self.ir_right_sensor.read_u16() < 65535 // 2

    def forward(self):
        self.m1Forward(15000)
        self.m2Forward(15000)
        time.sleep(5)
        allStop()

    def receive_scent(self):
        # send ? to get scent
        # wait and return integer response
        self.bluetooth.send("?")
        # loop until value was changed by bluetooth client
        while (response := self.bluetooth.read("int")) == ord("?"):
            pass
        return response

    def shoot(self):
        # send @ to shoot
        # wait for change in bluetooth as acknoledgement
        self.bluetooth.send("@")

        # loop until value was changed by bluetooth client
        while (response := self.bluetooth.read("int")) == ord("@"):
            pass
        return response

