#ifndef _ROBOT_
#define _ROBOT_
#include "board.h"

enum State {INITIAL, GOLD_KNOWN, HAS_GOLD, FINISHED};

class Robot {
    public:
    Robot(int x, int y, int dx, int dy, Board board=Board(), State state=INITIAL) : pos(x, y), dir(dx, dy), start_pos(x, y), board(board), state(state) {};
    void start();
    Coordinate get_explore_pos() const;
    bool move_to(const Coordinate & c);
    void rot_cw();
    void rot_ccw();
    void move_forward();
    void sniff();
    virtual int receive_scent() const;

    private:
    Coordinate pos, dir;
    const Coordinate start_pos;
    State state;
    Board board;
    int* scents[WIDTH];
};


#endif