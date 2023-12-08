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

// Note: USED_ARROW comes before GOLD_KNOWN, because we only shoot if we have not found gold yet
enum State {INITIAL, USED_ARROW, GOLD_KNOWN, HAS_GOLD, FINISHED};

class Robot {
    public:
    Robot(int x, int y, int dx, int dy, Board board=Board(), State state=INITIAL);
    Robot(): Robot(0, 0, 1, 0) {};
    
    // core actions
    void start();
    Coordinate get_explore_pos() const;
    bool move_to(const Coordinate & c);
    void sniff();
    void shoot_at(const Coordinate & target_pos);

    // methods to be overriden by subclasses
    virtual void rot_cw();
    virtual void rot_ccw();
    virtual void move_forward();
    // receive_scent must return the scent at the current position pos (such as by listening to cin or bluetooth).
    virtual int receive_scent() const {throw std::runtime_error("receive_scent must be implemented by subclass");}
    // shoot must shoot at the target position (such as by printing a message or physically releasing an arrow).
    virtual void shoot() {throw std::runtime_error("shoot must be implemented by subclass");}

    protected:
    // utilities
    void rotate(const Coordinate & new_dir);
    void follow_path(const std::vector<Coordinate> & path);
    Coordinate yolo();

    Coordinate pos, dir;
    const Coordinate start_pos;
    State state;
    Board board;
    std::vector<std::vector<int> > scents;
};


#endif