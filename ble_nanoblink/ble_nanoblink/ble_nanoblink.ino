#include <ArduinoBLE.h>

long previousMillis = 0;
int interval = 0;
int blePreviousValue = 0;
int ledState = LOW;

BLEService ledService("180A"); // BLE LED Service

// BLE LED Switch Characteristic - custom 128-bit UUID, read and writable by central
BLEByteCharacteristic ledCharacteristic("2A57", BLERead | BLEWrite | BLEWriteWithoutResponse);

void setup() {

  // set built in LED pin to output mode
  pinMode(LED_BUILTIN, OUTPUT);

  // begin initialization
  if (!BLE.begin()) {

    while (1);
  }

  // set advertised local name and service UUID:
  BLE.setLocalName("Nano 33 IoT");
  BLE.setAdvertisedService(ledService);

  // add the characteristic to the service
  ledService.addCharacteristic(ledCharacteristic);

  // add service
  BLE.addService(ledService);

  // set the initial value for the characteristic:
  ledCharacteristic.writeValue(blePreviousValue);

  // start advertising
  BLE.advertise();

}

void loop() {
  // listen for BLE peripherals to connect:
  BLEDevice central = BLE.central();

  // if a central is connected to peripheral:
  if (central) {

    // while the central is still connected to peripheral:
    while (central.connected()) {
      // if the remote device wrote to the characteristic,
      // use the value to control the LED:
      if (ledCharacteristic.written() && ledCharacteristic.value() != blePreviousValue) {
        // turn the LED on if ledCharacteristic is odd
        if (ledCharacteristic.value() % 2 == 1) {
          digitalWrite(LED_BUILTIN, HIGH);
          
        }
        else {
          digitalWrite(LED_BUILTIN, LOW);
        }
        ledCharacteristic.writeValue(ledCharacteristic.value()+1);
        blePreviousValue = ledCharacteristic.value()+1;
        
        
      }
    }

    // when the central disconnects, print it out:
    digitalWrite(LED_BUILTIN, LOW);         // will turn the LED off
  }
}
