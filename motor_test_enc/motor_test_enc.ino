#include "SAMD_PWM.h"
#include "Encoder.h"

int motor1pin1 = 9;
int motor1pin2 = 10;
Encoder m1encoder(2, 3);

int motor2pin1 = 6;
int motor2pin2 = 5;
Encoder m2encoder(11, 21);

float OK_ERROR = 50;

SAMD_PWM* motor1pin1pwm;
SAMD_PWM* motor1pin2pwm;
SAMD_PWM* motor2pin1pwm;
SAMD_PWM* motor2pin2pwm;

float stdFreq = 1000.0f; // operating frequency (unvarying)
float zeroDuty = 0.0f; // off
float slow = 22.0f; // slow speed
float turnProportion = 0.05; // turn speed
float intProportion = 0.002;

// scale motor 2's duty cycle by a constant to adjust for differences
// in hardware between the two motors
float m2_scale = 1.0232;

// number of encoder ticks in one block
long blockEncTarget = 4000;

// number of encoder ticks in each wheel
// to turn 90 degrees
long turnEncTarget = 680;

void setup() {

  // for debug
  /*
  Serial.begin(9600);
  while(!Serial);
  */

  // init and set all motor pins to 0
  motor1pin1pwm = new SAMD_PWM(motor1pin1, stdFreq, 0.0f);
  motor1pin2pwm = new SAMD_PWM(motor1pin2, stdFreq, 0.0f);
  motor2pin1pwm = new SAMD_PWM(motor2pin1, stdFreq, 0.0f);
  motor2pin2pwm = new SAMD_PWM(motor2pin2, stdFreq, 0.0f);
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

void forward1Block(float dutyCycle) {
  
  m1encoder.readAndReset();
  m2encoder.readAndReset();
  while(blockEncTarget - (m1encoder.read() + m2encoder.read()) / 2 > OK_ERROR) {

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

void loop() {
  delay(5000);
  ccw();
  ccw();
}