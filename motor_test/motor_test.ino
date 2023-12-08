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

float stdFreq = 1000.0f; // operating frequency (unvarying)
float zeroDuty = 0.0f; // off
float slow = 15.0f; // slow speed
float turn = 20.0f; // turn speed


// scale motor 2's duty cycle by a constant to adjust for differences
// in hardware between the two motors
float m2_scale = 1.0232;

// delay needed for the bot to travel 1 block
// when motors are all forward or all backward
int block_delay = 4000;

// delay needed for the bot to rotate 90 degrees
int rot_delay = 950;

void setup() {
  // init and set all motor pins to 0
  motor1pin1pwm = new SAMD_PWM(motor1pin1, stdFreq, 0.0f);
  motor1pin2pwm = new SAMD_PWM(motor1pin2, stdFreq, 0.0f);
  motor2pin1pwm = new SAMD_PWM(motor2pin1, stdFreq, 0.0f);
  motor2pin2pwm = new SAMD_PWM(motor2pin2, stdFreq, 0.0f);
}

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
  delay(rot_delay);
  allStop();
}

void cw() {
  m1Backward(turn);
  m2Forward(turn);
  delay(rot_delay);
  allStop();
}

void loop() {
  // go forward for 4.5 s and then we can measure error
  delay(5000);
  cw();
  delay(5000);
  ccw();
  delay(5000);
  allForward(slow);
  delay(block_delay);
  allStop();
  delay(5000);
}