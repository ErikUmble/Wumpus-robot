#include <iostream>
#include <string>
#include "wumpus/robot.h"

class BitBot: public Robot {
    public:
    BitBot(int x, int y, int dx, int dy, Board board=Board(), State state=INITIAL) : super(x, y, dx, dy, board, state) {};
    BitBot() : super(0, 0, 1, 0) {};
    void move_forward() {
        if (dir == Coordinate(1, 0)) std::cout << "e" << std::endl;
        else if (dir == Coordinate(-1, 0)) std::cout << "w" << std::endl;
        else if (dir == Coordinate(0, 1)) std::cout << "n" << std::endl;
        else if (dir == Coordinate(0, -1)) std::cout << "s" << std::endl;
        super::move_forward();
    }
    int receive_scent() const {
        // moderator does not provide scent at first position
        if (pos == Coordinate(0, 0)) return 0;
        std::cout << "input:" << std::endl;
        int scent;
        std::cin >> scent;
        return scent;
    }
    void shoot() {
        if (dir == Coordinate(1, 0)) std::cout << "kill e" << std::endl;
        else if (dir == Coordinate(-1, 0)) std::cout << "kill w" << std::endl;
        else if (dir == Coordinate(0, 1)) std::cout << "kill n" << std::endl;
        else if (dir == Coordinate(0, -1)) std::cout << "kill s" << std::endl;
    }

    private:
    typedef Robot super;
};

int main() {
    BitBot robot;
    //robot.enable_logs(std::cout); // commet out for running with wumpus_tester.py
    robot.start();
}