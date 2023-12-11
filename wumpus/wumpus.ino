#include <ArduinoBLE.h>
#include "SAMD_PWM.h"
#include "robot.h"

int motor1pin1 = 9;
int motor1pin2 = 10;
int motor2pin1 = 6;
int motor2pin2 = 5;

SAMD_PWM* motor1pin1pwm;
SAMD_PWM* motor1pin2pwm;
SAMD_PWM* motor2pin1pwm;
SAMD_PWM* motor2pin2pwm;

float stdFreq = 1000.0f; // operating frequency (unvarying)
float zeroDuty = 0.0f; // off
float slow = 18.0f; // slow speed
float turn = 20.0f; // turn speed

// scale motor 2's duty cycle by a constant to adjust for differences
// in hardware between the two motors
float m2_scale = 1.0232;

// delay needed for the bot to travel 1 block
// when motors are all forward or all backward
int block_delay = 3600;

// delay needed for the bot to rotate 90 degrees
int rot_delay = 400;


BLEService nanoBotService("180A"); // BLE Service
// BLE Characteristic for transmitting scent - custom 128-bit UUID, read and writable by central
BLEByteCharacteristic scentCharacteristic("2A57", BLERead | BLEWrite);

BLEDevice central;

void m1Forward(float dutyCycle) {
  motor1pin1pwm->setPWM(motor1pin1, stdFreq, dutyCycle);
  motor1pin2pwm->setPWM(motor1pin2, stdFreq, 0.0f);
}

void m1Backward(float dutyCycle) {
  motor1pin1pwm->setPWM(motor2pin1, stdFreq, 0.0f);
  motor1pin2pwm->setPWM(motor2pin2, stdFreq, dutyCycle);
}

void m2Forward(float dutyCycle) {
  motor2pin1pwm->setPWM(motor2pin1, stdFreq, dutyCycle * m2_scale);
  motor2pin2pwm->setPWM(motor2pin2, stdFreq, 0.0f);
}

void m2Backward(float dutyCycle) {
  motor2pin1pwm->setPWM(motor2pin1, stdFreq, 0.0f);
  motor2pin2pwm->setPWM(motor2pin2, stdFreq, dutyCycle * m2_scale);
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
  m1Forward(turn);
  m2Backward(turn);
  delay(rot_delay);
  allStop();
}

void cw() {
  m1Backward(turn);
  m2Forward(turn);
  delay(rot_delay);
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

        Serial.println("moving forward");
        Serial.println(pos.x);
        Serial.println(pos.y);
        // move NanoBot forward 1 block
        allForward(slow);
        delay(block_delay);
        allStop();

        // update internal state
        super::move_forward();
    }
    int receive_scent() const {
        /*
        Writes 0b111111 = 0x3F = '?' (query) to indicate waiting for a scent
        then returns the next value after that changes
        */
        Serial.println("receive scent called!");
        while (true) {
            if (central) {
                while(central.connected()) {
                    Serial.print("writing ");
                    Serial.println(scentCharacteristic.value());
                    
                    scentCharacteristic.writeValue('?');
                    delay(1000);
                    Serial.print("reading ");
                    Serial.println(scentCharacteristic.value());
                    
                    while (scentCharacteristic.value() == '?') {
                      Serial.println("?");
                    }
                    Serial.println("returning");
                    return scentCharacteristic.value();
                }
            }
        }
    }
    void shoot() {
        // send 0b1000000 = 0x40 = '@' (target) to indicate shooting
        // wait for aknowledgement (any other value) before continuing
        
        while (true) {
            if (central) {
            while(central.connected()) {
                scentCharacteristic.writeValue('@');
                while (scentCharacteristic.value() == '@');
                return;
            }
        }
      }
    }

    private:
    typedef Robot super;
};

NanoBot robot;

void setup() {

    // temporary for debug
    Serial.begin(9600);
    while (!Serial);

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
      Serial.println("waiting for bluetooth");
      while (central && central.connected()) {
        Serial.println("connected!");
        if (scentCharacteristic.written()) {
          Serial.println("breaking");
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
