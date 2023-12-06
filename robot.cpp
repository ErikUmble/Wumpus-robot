#include <cassert>
#include "robot.h"

Robot::Robot(int x, int y, int dx, int dy, Board board=Board(), State state=INITIAL) : pos(x, y), dir(dx, dy), start_pos(x, y), board(board), state(state) {
        // robot must start at a valid location, so mark it as such

        // initialize scents to 0
        for (int x = 0; x < WIDTH; x++) {
            int col[HEIGHT];
            scents[x] = col;
            for (int y = 0; y < HEIGHT; y++)
                scents[x][y] = 0;
        }
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
    Coordinate gold_pos = board.gold_pos;
    move_to(gold_pos);
    state = HAS_GOLD;

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
    int max_sum = 0;
    Coordinate best_pos;
    for (int x = 0; x < WIDTH; x++) {
        for (int y = 0; y < HEIGHT; y++) {
            int sum = 0;
            for (const Coordinate adj:adjacent_positions(pos)) {
                sum += board[adj];
            }
            if (sum > max_sum || (sum == max_sum && distance(pos, Coordinate(x, y)) < distance(pos, best_pos))) {
                max_sum = sum;
                best_pos = Coordinate(x, y);
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
    if (!(0 <= c.x && c.x < WIDTH && 0 <= c.y && c.y < HEIGHT)) {
        // invalid location
        return false;
    }
    if (c.x == pos.x && c.y == pos.y) {
        // already at the desired location
        return true;
    }
    std::vector<Coordinate> path = shortest_path(pos, c, board);
    if (path.size() == 0) {
        return false;
    }
    for (const Coordinate & dir: path) {
        // rotate to face the direction given by the next step in the path
        if (dir.x == pos.x + 1) {
            rot_cw();
        } else if (dir.x == pos.x - 1) {
            rot_ccw();
        } else if (dir.y == pos.y + 1) {
            rot_cw();
            rot_cw();
        }
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
}
void Robot::sniff() {
    /*
    calls receive_scent, stores that scent, and uses it for deduction
    Override receive_scent, not sniff for different system subclasses
    */
    
    int scent = receive_scent();
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