#include "SAMD_PWM.h"

int motor1pin1 = 9;
int motor1pin2 = 10;
int motor2pin1 = 6;
int motor2pin2 = 5;
int ledpin = 13;

SAMD_PWM* motor1pin1pwm;
SAMD_PWM* motor1pin2pwm;
SAMD_PWM* motor2pin1pwm;
SAMD_PWM* motor2pin2pwm;

float stdFreq = 1000.0f;
float zeroDuty = 0.0f;
float slow = 40.0f;
float turn = 40.0f;

void setup() {
  // init and set all motor pins to 0
  motor1pin1pwm = new SAMD_PWM(motor1pin1, stdFreq, 0.0f);
  motor1pin2pwm = new SAMD_PWM(motor1pin2, stdFreq, 0.0f);
  motor2pin1pwm = new SAMD_PWM(motor2pin1, stdFreq, 0.0f);
  motor2pin2pwm = new SAMD_PWM(motor2pin2, stdFreq, 0.0f);
}

void m1Forward(float dutyCycle) {
  // set all to forward
  motor1pin1pwm->setPWM(motor1pin1, stdFreq, dutyCycle);
  motor1pin2pwm->setPWM(motor1pin2, stdFreq, 0.0f);
}

void m1Backward(float dutyCycle) {
  motor1pin1pwm->setPWM(motor2pin1, stdFreq, 0.0f);
  motor1pin2pwm->setPWM(motor2pin2, stdFreq, dutyCycle);
}

void m2Forward(float dutyCycle) {
  motor2pin1pwm->setPWM(motor2pin1, stdFreq, dutyCycle);
  motor2pin2pwm->setPWM(motor2pin2, stdFreq, 0.0f);
}

void m2Backward(float dutyCycle) {
  motor2pin1pwm->setPWM(motor2pin1, stdFreq, 0.0f);
  motor2pin2pwm->setPWM(motor2pin2, stdFreq, dutyCycle);
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
  motor1pin1pwm->setPWM(motor1pin1, stdFreq, 0.0f);
  motor1pin2pwm->setPWM(motor1pin2, stdFreq, 0.0f);
  motor2pin1pwm->setPWM(motor2pin1, stdFreq, 0.0f);
  motor2pin2pwm->setPWM(motor2pin2, stdFreq, 0.0f);
}

void ccw() {
  m1Forward(turn);
  m2Backward(turn);
  delay(1000);
  allStop();
}

void cw() {
  m1Backward(turn);
  m2Forward(turn);
  delay(1000);
  allStop();
}

void loop() {
  delay(5000);
  allForward(slow);
  delay(1000);
  allStop();
  delay(1000);
  allBackward(slow);
  delay(1000);
  allStop();
  delay(1000);
  cw();
  delay(1000);
  ccw();
  delay(1000);
  allStop();
}

