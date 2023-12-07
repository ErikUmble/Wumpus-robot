#include <ArduinoBLE.h>

#include "robot.h"

BLEService nanoBotService("180A"); // BLE Service
// BLE Characteristic for transmitting scent - custom 128-bit UUID, read and writable by central
BLEByteCharacteristic scentCharacteristic("2A57", BLERead | BLEWrite);


class NanoBot: public Robot {
    public:
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
    void receive_scent() {
        BLEDevice central = BLE.central();
        // todo: consider writing a value to indicate request for scent
        // wait until a scent is written to the Bluetooth service characteristic
        while (!scentCharacteristic.written());
        int scent = scentCharacteristic.value();
        return scent;
    }
    void shoot() {
        // send 111 over bluetooth to indicate shooting 
        scentCharacteristic.writeValue(111);
        delay(2000);
    }

    private:
    typedef Robot super;
};

void setup() {
    NanoBot robot;
    Serial.begin(9600);
    while (!Serial);

    // initialize Bluetooth connection
    if (!BLE.begin()) {
        Serial.println("starting Bluetooth® Low Energy failed!");
        while (1);
    }

    // set advertised local name and service UUID
    BLE.setLocalName("Nano 33 IoT");
    BLE.setAdvertisedService(nanoBotService);
    BLE.addServie(nanoBotService);
    // initialize to 0
    scentCharacteristic.writeValue(0);
}

void loop() {
    //robot.start();
    for (unsigned int i=0; i < 3; i++) {
        while (!scentCharacteristic.written());
        int scent = scentCharacteristic.value();
        scnetCharacteristic.writeValue(scent);
    }
    while (1);
}
