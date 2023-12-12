#include "Motor_PID.h"

int motor1pin1 = 9;
int motor1pin2 = 10;
int motor1enc1 = 2;
int motor1enc2 = 3;

int motor2pin1 = 6;
int motor2pin2 = 5;
int motor2enc1 = 11;
int motor2enc2 = 21;

// PID constants
float kp = 8;
float kd = 0.1;
float ki = 0.1;

int pwm_lower_limit = 0;//full range
int pwm_upper_limit = 255;//full range

motor motor1(motor1enc1, motor1enc2, motor1pin2, motor1pin1, motor1pin2, pwm_lower_limit, pwm_upper_limit);
void setup()
{
  Serial.begin(9600);
   motor1.init(kp, kd, ki);
    motor1.set_target(10);
    motor1.start();
}
void loop()
{
  Serial.println(motor1.get_position());
}