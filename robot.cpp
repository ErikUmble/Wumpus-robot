#include <cassert>
#include <iostream>
#include <vector>
#include "robot.h"

Robot::Robot(int x, int y, int dx, int dy, Board board, State state) : pos(x, y), dir(dx, dy), start_pos(x, y), state(state), board(board) {
        // robot must start at a valid location, so mark it as such
        // Note: it could start at gold
        this->board.set(start_pos, board.get(start_pos) & 0b1100);

        // initialize scents to 0b10000 (not sniffed yet)
        scents = std::vector<std::vector<int> >(WIDTH, std::vector<int>(HEIGHT, 0b10000));
    }

void Robot::start() {
    // TODO: determine whether or not to shoot the wumpus
    while (state < GOLD_KNOWN) {
        Coordinate explore_pos = get_explore_pos();
        move_to(explore_pos);
        sniff();
        board.eliminate(scents);
        if (!board.gold_pos.is_null()) {
            state = GOLD_KNOWN;
            break;
        }
        
    }
    assert(!board.gold_pos.is_null());
    out << "FOUND GOLD\n";
    Coordinate gold_pos = board.gold_pos;
    move_to(gold_pos);
    state = HAS_GOLD;
    out << "GOT THE GOLD\n";


    // now we have the gold, so return to origin
    move_to(start_pos);
    state = FINISHED;

}
int distance(const Coordinate & a, const Coordinate & b) {
    /*
    distance herisitic
    return absolute difference between x values and y values instead of computing path length
    */
    return abs(a.x - b.x) + abs(a.y - b.y);
}

Coordinate Robot::get_explore_pos() const {
    /*
    returns the (x, y) pair for the best position to visit next
    (x, y) is guaranteed to be an empty tile (and in pracice this means there is a safe route to it)
    unvisited, safe positions are ranked by the sum of tile options adjacent to them since higher possibility sums
    means more expected information from a scent at that location. Ties are broken by the nearest tile to the robot winning.
    */
    out << "current board knowledge:\n" << board;
    int max_sum = 0;
    Coordinate best_pos;
    for (int x = 0; x < WIDTH; x++) {
        for (int y = 0; y < HEIGHT; y++) {
            Coordinate potential(x, y);
            // skip tiles that are not known to be safe
            if (board.get(potential) & 0b011) continue;

            // skip tiles that we already sniffed at 
            if (!(scents[x][y] & 0b10000)) continue;
            

            int sum = 0;
            for (const Coordinate adj:adjacent_positions(potential)) {
                sum += board[adj];
            }
            if (sum > max_sum || (sum == max_sum && distance(pos, potential) < distance(pos, best_pos))) {
                max_sum = sum;
                best_pos = potential;
            }
        }
    }
    return best_pos;
}
bool Robot::move_to(const Coordinate & c) {
    /*
    Uses the shortest valid path (if it exists) to move to board[x][y]
    returns False if unable to make the movement
    */
   out << "moving to " << c.x << ", " << c.y << std::endl;
    if (!((0 <= c.x) && (c.x < WIDTH) && (0 <= c.y) && (c.y < HEIGHT))) {
        // invalid location
        return false;
    }
    if (c == pos) {
        // already at the desired location
        return true;
    }
    std::vector<Coordinate> path = shortest_path(pos, c, board);
    if (path.size() == 0) {
        return false;
    }
    out << "path " << path;
    for (const Coordinate & dir: path) {
        // rotate to face the direction given by the next step in the path

        // check if a single ccw rotation would take us to the desired direction
        if (dir.x == -this->dir.y && dir.y == this->dir.x) {
            rot_ccw();
        }
        // otherwise, rotate cw until we are facing the desired direction
        while (!(this->dir == dir)) rot_cw();
        
        move_forward();
    }
    return true;

}
void Robot::rot_cw() {
    /*
    rotates 90 degrees clockwise
    if this function is overriden by a descendent, it should be called
    within that function to keep the internal state correct.
    */

    //update direction state (eg. (dx, dy) = (1, 0) becomes (0, -1))
    int tmp_dx = dir.x;
    dir.x = dir.y;
    dir.y = -tmp_dx;

}
void Robot::rot_ccw() {
    /*
    rotates 90 degrees clockwise
    if this function is overriden by a descendent, it should be called
    within that function to keep the internal state correct.
    */
    //update direction state (eg. (dx, dy) = (1, 0) becomes (0, 1))
    int tmp_dx = dir.x;
    dir.x = -dir.y;
    dir.y = tmp_dx;

}
void Robot::move_forward() {
    /*
    moves forward by 1 unit in the current direction
    
    if this function is overriden by a descendent, it should be called
    within that function to keep the internal state correct.
    */
    pos.x += dir.x;
    pos.y += dir.y;
    out << "moved to " << pos.x << ", " << pos.y << std::endl;

    assert(pos.in_bounds());
}
void Robot::sniff() {
    /*
    calls receive_scent, stores that scent, and uses it for deduction
    Override receive_scent, not sniff for different system subclasses
    */
    out << "sniffing at " << pos.x << ", " << pos.y << std::endl;
    int scent = receive_scent();
    out << "received scent " << scent << std::endl;
    scents[pos.x][pos.y] = scent;
    board.reduce(scent, pos);
}

int Robot::receive_scent() const {
    /*
    listens for the scent at the current position
    and returns that scent.
    */
    return 7; // TODO: implement
}