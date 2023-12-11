#include <ArduinoBLE.h>
#include "SAMD_PWM.h"
#include "robot.h"
#include "Encoder.h"

int motor1pin1 = 9;
int motor1pin2 = 10;
Encoder m1encoder(2, 3);

int motor2pin1 = 6;
int motor2pin2 = 5;
Encoder m2encoder(11, 21);

float OK_ERROR = 100;

SAMD_PWM* motor1pin1pwm;
SAMD_PWM* motor1pin2pwm;
SAMD_PWM* motor2pin1pwm;
SAMD_PWM* motor2pin2pwm;

float stdFreq = 1000.0f; // operating frequency (unvarying)
float zeroDuty = 0.0f; // off
float slow = 22.0f; // slow speed
float turnProportion = 0.05; // turn speed
float intProportion = 0.002;

int block_delay = 3600;

// scale motor 2's duty cycle by a constant to adjust for differences
// in hardware between the two motors
float m2_scale = 1.0232;

// number of encoder ticks in one block
long blockEncTarget = 4000;

// number of encoder ticks in each wheel
// to turn 90 degrees
long turnEncTarget = 680;

BLEService nanoBotService("180A"); // BLE Service
// BLE Characteristic for transmitting scent - custom 128-bit UUID, read and writable by central
BLEByteCharacteristic scentCharacteristic("2A57", BLERead | BLEWrite);

BLEDevice central;

bool ir_left() {
  // returns true if the left infrared sensor detects white
  return analogRead(17) > 1023 / 2;
}


bool ir_right() {
  // returns true if the right infrared sensor detects white
  return analogRead(16) > 1023 / 2;
}


void m1Forward(float dutyCycle) {
  if (dutyCycle >= 100.0) {
    motor1pin1pwm->setPWM(motor1pin1, stdFreq, 100.0f);
    motor1pin2pwm->setPWM(motor1pin2, stdFreq, 0.0f);
  }
  else {
    motor1pin1pwm->setPWM(motor1pin1, stdFreq, dutyCycle);
    motor1pin2pwm->setPWM(motor1pin2, stdFreq, 0.0f);
  }
}

void m1Backward(float dutyCycle) {
  if (dutyCycle >= 100) {
    motor1pin1pwm->setPWM(motor1pin1, stdFreq, 0.0f);
    motor1pin2pwm->setPWM(motor1pin2, stdFreq, 100.0f);
  }
  else {
    motor1pin1pwm->setPWM(motor1pin1, stdFreq, 0.0f);
    motor1pin2pwm->setPWM(motor1pin2, stdFreq, dutyCycle);
  }
}

void m2Forward(float dutyCycle) {
  if (dutyCycle * m2_scale >= 100) {
    motor2pin1pwm->setPWM(motor2pin1, stdFreq, 100.0);
    motor2pin2pwm->setPWM(motor2pin2, stdFreq, 0.0f);
  }
  else {
    motor2pin1pwm->setPWM(motor2pin1, stdFreq, dutyCycle * m2_scale);
    motor2pin2pwm->setPWM(motor2pin2, stdFreq, 0.0f);
  }
}

void m2Backward(float dutyCycle) {
  if (dutyCycle * m2_scale >= 100) {
    motor2pin1pwm->setPWM(motor2pin1, stdFreq, 0.0f);
    motor2pin2pwm->setPWM(motor2pin2, stdFreq, 100.0);
  }
  else {
    motor2pin1pwm->setPWM(motor2pin1, stdFreq, 0.0f);
    motor2pin2pwm->setPWM(motor2pin2, stdFreq, dutyCycle * m2_scale);
  }
}

void m1SignedDirection(float dutyCycle) {
  if (dutyCycle > 0) {
    m1Forward(dutyCycle);
  }
  else {
    m1Backward(-dutyCycle);
  }
}

void m2SignedDirection(float dutyCycle) {
  if (dutyCycle > 0) {
    m2Forward(dutyCycle);
  }
  else {
    m2Backward(-dutyCycle);
  }
}

void allForward(float dutyCycle) {
  m1Forward(dutyCycle);
  m2Forward(dutyCycle);
}

void allStop() {
  // set all duty cycles to 0
  motor1pin1pwm->setPWM(motor1pin1, stdFreq, 0.0f);
  motor1pin2pwm->setPWM(motor1pin2, stdFreq, 0.0f);
  motor2pin1pwm->setPWM(motor2pin1, stdFreq, 0.0f);
  motor2pin2pwm->setPWM(motor2pin2, stdFreq, 0.0f);
}

void ccw() {
  m1encoder.readAndReset();
  m2encoder.readAndReset();
  float m1integral = 0;
  float m2integral = 0;
  while (abs(m1encoder.read() - turnEncTarget) > OK_ERROR || abs(m2encoder.read() + turnEncTarget) > OK_ERROR) {
    if (abs(m1encoder.read() - turnEncTarget) > OK_ERROR) {
      m1SignedDirection(-1 * (turnProportion * (m1encoder.read() - turnEncTarget) + intProportion * m1integral));
      m1integral += m1encoder.read() - turnEncTarget;
    }
    if (abs(m2encoder.read() + turnEncTarget) > OK_ERROR) {
      m2SignedDirection(-1 * (turnProportion * (m2encoder.read() + turnEncTarget) + intProportion * m2integral));
      m2integral += m2encoder.read() + turnEncTarget;
    }
    delay(50);
  }
  allStop();
}

void cw() {
  m1encoder.readAndReset();
  m2encoder.readAndReset();
  float m1integral = 0;
  float m2integral = 0;
  while (abs(m1encoder.read() + turnEncTarget) > OK_ERROR || abs(m2encoder.read() - turnEncTarget) > OK_ERROR) {
    if (abs(m1encoder.read() + turnEncTarget) > OK_ERROR) {
      m1SignedDirection(-1 * (turnProportion * (m1encoder.read() + turnEncTarget) + intProportion * m1integral));
      m1integral += m1encoder.read() + turnEncTarget;
    }
    if (abs(m2encoder.read() - turnEncTarget) > OK_ERROR) {
      m2SignedDirection(-1 * (turnProportion * (m2encoder.read() - turnEncTarget) + intProportion * m2integral));
      m2integral += m2encoder.read() - turnEncTarget;
    }
    delay(50);
  }
  allStop();
}

class NanoBot: public Robot {
    public:
    NanoBot() { super(); }
    void rot_cw() {

        // turn NanoBot
        cw();

        // update internal state
        super::rot_cw();
    }
    void rot_ccw() {

        // turn NanoBot
        ccw();

        // update internal state
        super::rot_ccw();
    }
    void move_forward() {


        // move forward and then make corrections until both sensors detect white at the same time
        bool white_left, white_right;
        while (true) {
          unsigned long distance_ms = 0;
          allForward(slow);
          while(!ir_left() && !ir_right()) {
            distance_ms += 1; 
            delay(1); 
            white_left = ir_left(); white_right = ir_right();
            }
          allStop();
          if (white_left && white_right) break;
          if (white_left) m2Backward(slow);
          if (white_right) m1Backward(slow);
          delay(distance_ms / 20);
          allStop();
        }
        allForward(slow);
        delay(block_delay/2);
        allStop();


        // update internal state
        super::move_forward();
    }
    int receive_scent() const {
        /*
        Writes 0b111111 = 0x3F = '?' (query) to indicate waiting for a scent
        then returns the next value after that changes
        */
        // listen for BLE peripherals to connect:
        central = BLE.central();

        if (central) {
          scentCharacteristic.writeValue('?');
          while(central.connected()) {
            if (scentCharacteristic.written());
              char scent = scentCharacteristic.value();
              if (scent == '?') continue;
              return scent;
          }
        }
    }
    void shoot() {
        // send 0b1000000 = 0x40 = '@' (target) to indicate shooting
        // wait for aknowledgement (any other value) before continuing
        
        central = BLE.central();

        if (central) {
          scentCharacteristic.writeValue('@');
          while(central.connected()) {
            if (scentCharacteristic.written());
              char scent = scentCharacteristic.value();
              if (scent == '@') continue;
              return;
          }
        }
    }

    private:
    typedef Robot super;
};

NanoBot robot;

void setup() {

    // initialize Bluetooth connection
    if (!BLE.begin()) {
        while (1);
    }

    // set advertised local name and service UUID
    BLE.setLocalName("Nano 33 IoT");
    BLE.setAdvertisedService(nanoBotService);
    nanoBotService.addCharacteristic(scentCharacteristic);
    BLE.addService(nanoBotService);

    // initialize to 0
    scentCharacteristic.writeValue(0);
    BLE.advertise();

    // init and set all motor pins to 0
    motor1pin1pwm = new SAMD_PWM(motor1pin1, stdFreq, 0.0f);
    motor1pin2pwm = new SAMD_PWM(motor1pin2, stdFreq, 0.0f);
    motor2pin1pwm = new SAMD_PWM(motor2pin1, stdFreq, 0.0f);
    motor2pin2pwm = new SAMD_PWM(motor2pin2, stdFreq, 0.0f);


    // debugging
    while(true) {
      central = BLE.central();
      while (central && central.connected()) {
        if (scentCharacteristic.written()) {
          break;
        }
      }
      if (central && central.connected()) {
        break;
      }
    }
}

void loop() {
  robot.start();
}
