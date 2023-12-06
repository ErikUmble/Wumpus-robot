#include <ArduinoBLE.h>

#include "robot.h"

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

    }

    private:
    typedef Robot super;
}

void setup() {
    NanoBot robot;
}

void loop() {
    robot.start();
    while (1);
}
