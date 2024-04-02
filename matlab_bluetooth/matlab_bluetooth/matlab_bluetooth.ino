/*

*/
#include <ArduinoBLE.h>


BLEService nanoBotService("180A"); // BLE Service
// BLE Characteristic for transmitting scent - custom 128-bit UUID, read and writable by central
BLEByteCharacteristic testCharacteristic("2A57", BLERead | BLEWrite | BLEWriteWithoutResponse);
BLEByteCharacteristic anotherCharacteristic("2A58", BLERead | BLEWrite | BLEWriteWithoutResponse);

BLEDevice central;

void setup() {

  // initialize Bluetooth connection
    if (!BLE.begin()) {
        while (1);
    }
   // set advertised local name and service UUID
    BLE.setLocalName("Nano 33 IoT");
    BLE.setAdvertisedService(nanoBotService);
    nanoBotService.addCharacteristic(testCharacteristic);
    nanoBotService.addCharacteristic(anotherCharacteristic);
    BLE.addService(nanoBotService);

    // initialize to 0
    testCharacteristic.writeValue(0);
    anotherCharacteristic.writeValue(5);
    BLE.advertise();

      // initialize serial communication
  Serial.begin(9600);
  while (!Serial);
    
  Serial.println("Serial live!");

  // wait for connection and write
  while(true) {
    central = BLE.central();
    Serial.println("Waiting for connection!");
    while (central && central.connected()) {
      Serial.println("Waiting for write!");
      if (testCharacteristic.written()) {
        break;
      }
    }
    if (central && central.connected()) {
      break;
    }
  }

}

void loop() {

  central = BLE.central();

  while (central.connected()) {
      // if the remote device wrote to the characteristic,
      // use the value to control the LED:
      if (testCharacteristic.written()) {
        Serial.println(testCharacteristic.value());
          }
  }
  Serial.println("Disconnected");
}