from wumpus import Robot

import bluetooth
import time
from micropython import const
from ble_advertising import advertising_payload

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

    def rot_cw(self):
        pass

    def rot_ccw(self):
        pass

    def forward(self):
        pass

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


