#include <ArduinoBLE.h>
#include "robot.h"
#include "Encoder.h"

int motor1pin1 = 9;
int motor1pin2 = 10;
Encoder m1encoder(2, 3);

int motor2pin1 = 6;
int motor2pin2 = 5;
Encoder m2encoder(11, 21);

float OK_ERROR = 30;

int slow = 45; // slow speed
int med = 60;
float turnProportion = 0.05; // turn speed
int maxDuty = 70;
float intProportion = 0.0025;
int maxIntPower = 300;

int block_delay = 1200;

// scale motor 2's duty cycle by a constant to adjust for differences
// in hardware between the two motors
float m2_scale = 1.0403;

// number of encoder ticks in one block
long ticksAfterLine = 950;

// number of encoder ticks in each wheel
// to turn 90 degrees
long turn90ticks = 600;

BLEService nanoBotService("180A"); // BLE Service
// BLE Characteristic for transmitting scent - custom 128-bit UUID, read and writable by central
BLEByteCharacteristic scentCharacteristic("2A57", BLERead | BLEWrite);

BLEDevice central;

bool ir_left() {
  // returns true if the left infrared sensor detects white
  return analogRead(17) < 1023 / 2;
}


bool ir_right() {
  // returns true if the right infrared sensor detects white
  return analogRead(16) < 1023 / 2;
}


void m1Forward(int dutyCycle) {
  if (dutyCycle >= maxDuty) {
    analogWrite(motor1pin1, maxDuty);
    analogWrite(motor1pin2, 0);
  }
  else {
    analogWrite(motor1pin1, dutyCycle);
    analogWrite(motor1pin2, 0);
  }
}

void m1Backward(int dutyCycle) {
  if (dutyCycle >= maxDuty) {
    analogWrite(motor1pin1, 0);
    analogWrite(motor1pin2, maxDuty);
  }
  else {
    analogWrite(motor1pin1, 0);
    analogWrite(motor1pin2, dutyCycle);
  }
}

void m2Forward(int dutyCycle) {
  if (dutyCycle * m2_scale >= (float)maxDuty) {
    analogWrite(motor2pin1, maxDuty);
    analogWrite(motor2pin2, 0);
  }
  else {
    analogWrite(motor2pin1, dutyCycle * m2_scale);
    analogWrite(motor2pin2, 0);
  }
}

void m2Backward(int dutyCycle) {
  if (dutyCycle * m2_scale >= (float)maxDuty) {
    analogWrite(motor2pin1, 0);
    analogWrite(motor2pin2, maxDuty);
  }
  else {
    analogWrite(motor2pin1, 0);
    analogWrite(motor2pin2, dutyCycle * m2_scale);
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

void allBackward(float dutyCycle) {
  m1Backward(dutyCycle);
  m2Backward(dutyCycle);
}

void allStop() {
  // set all duty cycles to 0
  analogWrite(motor1pin1, 0);
  analogWrite(motor1pin2, 0);
  analogWrite(motor2pin1, 0);
  analogWrite(motor2pin2, 0);
}

void ccw(long ticks) {
  m1encoder.readAndReset();
  m2encoder.readAndReset();
  float m1integral = 0;
  float m2integral = 0;
  long timeSinceStart = 0;
  while (abs(m1encoder.read() - ticks) > OK_ERROR || abs(m2encoder.read() + ticks) > OK_ERROR) {
    if (abs(m1encoder.read() - ticks) > OK_ERROR) {
      float intPower = maxIntPower;
      if (intProportion * m1integral < maxIntPower) {
        intPower = intProportion * m1integral;
      }
      m1SignedDirection(-1 * (turnProportion * (m1encoder.read() - ticks) + intPower));
      m1integral += (m1encoder.read() - ticks) * (timeSinceStart / 2000);
    }
    if (abs(m2encoder.read() + ticks) > OK_ERROR) {
      float intPower = maxIntPower;
      if (intProportion * m2integral < maxIntPower) {
        intPower = intProportion * m2integral;
      }
      m2SignedDirection(-1 * (turnProportion * (m2encoder.read() + ticks) + intPower));
      m2integral += (m2encoder.read() + ticks) * (timeSinceStart / 2000);
    }
    timeSinceStart += 50;
    delay(50);
  }
  allStop();
}

void cw(long ticks) {
  m1encoder.readAndReset();
  m2encoder.readAndReset();
  float m1integral = 0;
  float m2integral = 0;
  long timeSinceStart = 0;
  while (abs(m1encoder.read() + ticks) > OK_ERROR || abs(m2encoder.read() - ticks) > OK_ERROR) {
    if (abs(m1encoder.read() + ticks) > OK_ERROR) {
      float intPower = maxIntPower;
      if (intProportion * m1integral < maxIntPower) {
        intPower = intProportion * m1integral;
      }
      m1SignedDirection(-1 * (turnProportion * (m1encoder.read() + ticks) + intPower));
      m1integral += (m1encoder.read() + ticks) * (timeSinceStart / 2000);
    }
    if (abs(m2encoder.read() - ticks) > OK_ERROR) {
      float intPower = maxIntPower;
      if (intProportion * m2integral < maxIntPower) {
        intPower = intProportion * m2integral;
      }
      m2SignedDirection(-1 * (turnProportion * (m2encoder.read() - ticks) + intPower));
      m2integral += (m2encoder.read() - ticks) * (timeSinceStart / 2000);
    }
    timeSinceStart += 50;
    delay(50);
  }
  allStop();
}

void forwardTicks(float dutyCycle, long ticks) {
  
  m1encoder.readAndReset();
  m2encoder.readAndReset();
  while(ticks - (m1encoder.read() + m2encoder.read()) / 2 > OK_ERROR) {

    float curScale = 1;
    if (m1encoder.read() > 100) {
      curScale = (float)m1encoder.read() / (float)m2encoder.read();
      curScale *= curScale;
    }
    m1Forward(dutyCycle);
    m2Forward(dutyCycle * curScale);
    /*
    Serial.print(m1encoder.read());
    Serial.print(" ");
    Serial.print(m2encoder.read());
    Serial.print(" ");
    Serial.println(curScale);
    */
    delay(50);

  }

}

class NanoBot: public Robot {
    public:
    NanoBot() { super(); }
    void rot_cw() {

        // turn NanoBot
        cw(turn90ticks);

        // update internal state
        super::rot_cw();
    }
    void rot_ccw() {

        // turn NanoBot
        ccw(turn90ticks);

        // update internal state
        super::rot_ccw();
    }
    void rot_180() {

      // turn NanoBot
      ccw(turn90ticks * 2);

      // update internal state
      super::rot_180();
    }
    void move_forward() {


        // move forward and then make corrections until both sensors detect white at the same time
        bool white_left = false, white_right = false;
        int left_time = 0, right_time = 0;
        int error_threshold_ms = 20;
        while (true) {
          int count = 0;
          allForward(slow);
          while(!white_left || !white_right) {
            count += 1; 
            delay(1); 
            if (!white_left && ir_left()) {
              white_left = true;
              left_time = count;
            }
            if (!white_right && ir_right()) {
              white_right = true;
              right_time = count;
            }
          }
          allStop();
          if (abs(left_time - right_time) < error_threshold_ms) break;
          /*if (left_time < right_time) m2Backward(med);
          else m1Backward(med);
          delay(abs(left_time - right_time) * 5);*/
          
          // backup and rotate to correct
          allBackward(med);
          delay(500);
          allStop();


          if (left_time < right_time) ccw((right_time - left_time));
          else cw((left_time - right_time) * 2);
          white_left = false;
          white_right = false;
          left_time = 0;
          right_time = 0;
        }
        forwardTicks(slow, ticksAfterLine);
        delay(block_delay*1/2);
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
    pinMode(motor1pin1, OUTPUT);
    pinMode(motor1pin2, OUTPUT);
    pinMode(motor2pin1, OUTPUT);
    pinMode(motor2pin2, OUTPUT);

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
  // celebrate
  ccw(720);
  // stop
  while(true);
}
