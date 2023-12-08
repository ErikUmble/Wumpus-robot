#include <ArduinoBLE.h>

#include "robot.h"

BLEService nanoBotService("180A"); // BLE Service
// BLE Characteristic for transmitting scent - custom 128-bit UUID, read and writable by central
BLEByteCharacteristic scentCharacteristic("2A57", BLERead | BLEWrite);


class NanoBot: public Robot {
    public:
    NanoBot() { super(); }
    void rot_cw() {

        // update internal state
        super::rot_cw();
    }
    void rot_ccw() {

        // update internal state
        super::rot_ccw();
    }
    void move_forward() {

        // update internal state
        super::move_forward();
    }
    int receive_scent() {
        /*
        Writes 0b111111 = 0x3F = '?' (query) to indicate waiting for a scent
        then returns the next value after that changes
        */
        while (true) {
            BLEDevice central = BLE.central();
            if (central) {
                while(central.connected()) {
                    scentCharacteristic.writeValue('?');
                    while (scentCharacteristic.value() == '?');
                    return scentCharacteristic.value();
                }
            }
        }
    }
    void shoot() {
        // send 0b1000000 = 0x40 = '@' (target) to indicate shooting
        // wait for aknowledgement (any other value) before continuing
        
        while (true) {
            BLEDevice central = BLE.central();
            if (central) {
            while(central.connected()) {
                scentCharacteristic.writeValue('@');
                while (scentCharacteristic.value() == '@');
                return;
            }
        }
    }

    private:
    typedef Robot super;
};

void setup() {
    NanoBot robot;

    // initialize Bluetooth connection
    if (!BLE.begin()) {
        while (1);
    }

    // temporary: only include for using serial
    Serial.begin(9600);
    while (!Serial);

    // set advertised local name and service UUID
    BLE.setLocalName("Nano 33 IoT");
    BLE.setAdvertisedService(nanoBotService);
    nanoBotService.addCharacteristic(scentCharacteristic);
    BLE.addService(nanoBotService);

    // initialize to 0
    scentCharacteristic.writeValue(0);
    BLE.advertise();

    Serial.println("BLE LED Peripheral");
}

void loop() {
    //robot.start();
    BLEDevice central = BLE.central();
    if (central) {
      Serial.println("started");
      while(central.connected()) {
        if (scentCharacteristic.written());
          Serial.print("found ");
          Serial.println(scentCharacteristic.value());
          char scent = scentCharacteristic.value() + 1;
          scentCharacteristic.writeValue(scent);
      }
    }
}
