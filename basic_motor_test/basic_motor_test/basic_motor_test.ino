int motor1pin1 = 9;
int motor1pin2 = 10;
// Encoder m1encoder(2, 3);

int motor2pin1 = 6;
int motor2pin2 = 5;
// Encoder m2encoder(11, 15);

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(motor1pin1, OUTPUT);
  pinMode(motor1pin2, OUTPUT);
  pinMode(motor2pin1, OUTPUT);
  pinMode(motor2pin2, OUTPUT);
}

void m1Forward() {
  digitalWrite(motor1pin1, HIGH);
  digitalWrite(motor1pin2, LOW);
}

void m1Backward() {
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, HIGH);
}

void m2Forward() {
  digitalWrite(motor2pin1, HIGH);
  digitalWrite(motor2pin2, LOW);
}

void m2Backward() {
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, HIGH);
}
void allStop() {
  digitalWrite(motor1pin1, LOW);
  digitalWrite(motor1pin2, LOW);
  digitalWrite(motor2pin1, LOW);
  digitalWrite(motor2pin2, LOW);
}

void loop() {
  // Serial.println(m1encoder.read());
  // Serial.println(m2encoder.read());
  delay(3000);
  digitalWrite(LED_BUILTIN, HIGH);
  m1Forward();
  m2Forward();
  delay(1000);
  allStop();
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
  digitalWrite(LED_BUILTIN, HIGH);
  m1Backward();
  m2Backward();
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  allStop();
}