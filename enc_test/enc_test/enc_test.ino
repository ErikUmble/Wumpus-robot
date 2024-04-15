#include "Encoder.h"

Encoder m1encoder(2, 3);
Encoder m2encoder(11, 15);

void setup() {
  Serial.begin(9600);
  while(!Serial);
}

void loop() {
  delay(500);
  // put your main code here, to run repeatedly:
  Serial.print(m1encoder.read());
  Serial.print(" ");
  Serial.println(m2encoder.read());
}
