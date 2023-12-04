/*
Connect the IR sensor to power and ground, and its output to pin 2.

Run this program and mount the IR sensor to about 1-2 inches from a 
black surface. Turn the potentiometer fully CW.
Turn the potentiometer CCW slowly until the LED turns off.
Keep the distance constant during the calibration. 
The LED will then turn on when the sensor detects a white surface.

source: http://www.robotsforfun.com/webpages/irsensor.html

*/

void setup() {
  pinMode(13, OUTPUT);  // internal LED
  pinMode(2, INPUT);    // IR input
}

void loop() {
  int v = digitalRead(2);
  digitalWrite(13, !v);	// the ! symbol inverts the value
  delay(50);
}