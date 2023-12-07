#ifndef _ROBOT_
#define _ROBOT_
#include "board.h"

/*
senses the robot recieves (and stores) from moderator
0b0000 empty
0b0001 breeze (could contain a pit)
0b0010 stench (could contain a wumpus)
0b0100 glitter (could contain gold)
0b1000 gold 

0b10000 not sniffed yet
*/

enum State {INITIAL, GOLD_KNOWN, HAS_GOLD, FINISHED};

class Robot {
    public:
    Robot(int x, int y, int dx, int dy, Board board=Board(), State state=INITIAL);
    void start();
    Coordinate get_explore_pos() const;
    bool move_to(const Coordinate & c);
    virtual void rot_cw();
    virtual void rot_ccw();
    virtual void move_forward();
    void sniff();
    virtual int receive_scent() const;

    protected:
    Coordinate pos, dir;
    const Coordinate start_pos;
    State state;
    Board board;
    std::vector<std::vector<int> > scents;
};


#endif