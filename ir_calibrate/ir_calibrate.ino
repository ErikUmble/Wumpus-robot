void setup() {
  Serial.begin(9600);  // Initialize serial communication

  pinMode(16, INPUT);
  pinMode(17, INPUT);
  pinMode(13, OUTPUT);
}

void loop() {

  int value = analogRead(16);
  if (value > 1023/2) {
    digitalWrite(13, HIGH);
  }
  else {
    digitalWrite(13, LOW);
  }
  delay(500);
}
