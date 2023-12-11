#include <cassert>
#include <iostream>
#include <vector>

#include "board.h"
#include "robot.h"

Robot::Robot(int x, int y, int dx, int dy, Board board, State state) : pos(x, y), dir(dx, dy), start_pos(x, y), state(state), board(board), log_actions(false), has_arrow(true), log_out(std::cout.rdbuf()) {
    // Note that although cout is set as the log stream, it will not be written to until enable_logs is called

    // robot must start at a valid location, so mark it as such
    // Note: it could start at gold
    this->board.set(start_pos, board.get(start_pos) & 0b1100);

    // initialize scents to 0b10000 (not sniffed yet)
    scents = std::vector<std::vector<int> >(WIDTH, std::vector<int>(HEIGHT, 0b10000));

}

void Robot::enable_logs(std::ostream & out) {
    /*
    call this with an output stream to begin logging actions to that stream
    */
    std::ostream log_out(out.rdbuf());
    log_actions = true;
}

void Robot::start() {
    while (state < GOLD_KNOWN) {
        Coordinate explore_pos = get_explore_pos();
        // if there are no safe places to explore, shoot the wumpus and explore from that location
        if (explore_pos.is_null()) {
            if (!board.wumpus_pos.is_null() && has_arrow) {
                // we know where the wumpus is, and still have an arrow to use
                explore_pos = board.wumpus_pos;
                shoot_at(board.wumpus_pos);
            }
            else {
                // we are in a situation where we must enter a potentially dangerous tile
                // so we will just yolo it and hope for the best
                // Note: this can only arise in boards where the robot must be able to know that it is solvable for it to be solvable
                explore_pos = yolo();
            }            
        }
        move_to(explore_pos);
        sniff();
        board.eliminate(scents);
        if (!board.gold_pos.is_null()) {
            state = GOLD_KNOWN;
            break;
        }
    }
    assert(!board.gold_pos.is_null());
    if (log_actions) log("FOUND GOLD");
    Coordinate gold_pos = board.gold_pos;
    while(!move_to(gold_pos)) {
        // shoot wumpus or continue yoloing as neccessary until the path to gold is clear
        if (!board.wumpus_pos.is_null() && has_arrow) shoot_at(board.wumpus_pos);
        else move_to(yolo());
    }
    state = HAS_GOLD;
    if (log_actions) log("RETRIEVED GOLD");

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
    if (log_actions) log_out << "current board knowledge:\n" << board << std::endl;
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

void Robot::rotate(const Coordinate & new_dir) {
    /*
    rotates until the robot is facing the given direction
    */
    // check if a single ccw rotation would take us to the desired direction
    if (new_dir.x == -this->dir.y && new_dir.y == this->dir.x) {
        rot_ccw();
    }
    // otherwise, rotate cw until we are facing the desired direction
    while (!(this->dir == new_dir)) rot_cw();
}

void Robot::follow_path(const std::vector<Coordinate> & path) {
    /*
    given a path of directions, this causes the robot to rotate and move forward
    into each direction in order
    */
    if (path.size() == 0) return;
    for (const Coordinate & dir: path) {
        // rotate to face the direction given by the next step in the path
        rotate(dir);
        move_forward();
    }
    return;
}

bool Robot::move_to(const Coordinate & c) {
    /*
    Uses the shortest valid path (if it exists) to move to board[x][y]
    returns False if unable to make the movement
    */
    if (log_actions) log("moving to " + std::to_string(c.x) + ", " + std::to_string(c.y));
    if (!((0 <= c.x) && (c.x < WIDTH) && (0 <= c.y) && (c.y < HEIGHT))) {
        // invalid location
        return false;
    }
    if (c == pos) {
        // already at the desired location
        return true;
    }
    std::vector<Coordinate> path = shortest_path(pos, c, board);
    
    follow_path(path);
    // return true if we actually had to move
    return path.size() > 0;
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

    assert(pos.in_bounds());
}
void Robot::sniff() {
    /*
    calls receive_scent, stores that scent, and uses it for deduction
    Override receive_scent, not sniff for different system subclasses
    */
    int scent = receive_scent();
    if (log_actions) log("received scent " + std::to_string(scent) + " at " + std::to_string(pos.x) + ", " + std::to_string(pos.y));
    scents[pos.x][pos.y] = scent;
    board.reduce(scent, pos);
}

void Robot::shoot_at(const Coordinate & target_pos) {
    /*
    Calculates the best place to shoot the target from, aims, shoots, and updates the board 
    This also updates the board now that the position is safe and calls eliminate (so wumpus_pos will be null after this)
    throws an excpetion if it is not possible to get to an adjacent position to shoot from
    */

   // find the path to the target
    std::vector<Coordinate> path = shortest_path(pos, target_pos, board);

    // empty path means either that there is not a safe route, or we already are at the location
    assert(path.size() > 0);

    // remove the last step so that we move into the adjacent position
    Coordinate aim_dir = path.back();
    path.pop_back();

    follow_path(path);
    rotate(aim_dir);

    if (log_actions) log("shooting at " + std::to_string(target_pos.x) + ", " + std::to_string(target_pos.y));

    if (has_arrow) shoot();
    else return;
    has_arrow = false;
    
    // zero out the wumpus bit from the target position by setting the bit to 1 then flipping it
    board.set(target_pos, (board[target_pos] | Tile["WUMPUS"]) ^ Tile["WUMPUS"]);
}

Coordinate Robot::yolo() {
    /*
    call this if there are no known safe places to explore
    this uses the fact that the board is supposed to be solveable to make a logical deduction
    as to where it must move next if it is going to reach the gold
    this will take risks such as shooting at a guess of where the wumpus is, or moving into
    a tile that might contain a pit, but does so in a way that is guaranteed to be safe if the board is solvable
    this returns the coordinate to move into next (which is marked as safe, even though it could be a risk)
    the returned tile definitely does not have the wumpus in it (we shoot at it before returning if there is a chance)

    Note: this should only be called if the robot knows the board is solvable
    Note: calling yolo multiple times in a row is acceptable
    */
    if (log_actions) log("resorting to yolo - this board had better be solvable");
    // first, find out all the positions we know absolutely are bad to move into
    std::vector<std::vector<bool> > forbidden(WIDTH, std::vector<bool>(HEIGHT, false));
    for (unsigned int x = 0; x < WIDTH; x++) {
        for (unsigned int y = 0; y < HEIGHT; y++) {
            int tile = board.deduce(Coordinate(x, y), scents);
            // only forbid tiles that we are sure are pits
            if (tile == 0b001) forbidden[x][y] = true;
        }
    }

    // then, consider the collection of positions that we have not sniffed at, but might be safe, and are reachable
    // by moving through only known safe tiles
    std::vector<Coordinate> potential_safe;  // a list would be slightly better, but that would be one more library to use
    for (unsigned int x = 0; x < WIDTH; x++) {
        for (unsigned int y = 0; y < HEIGHT; y++) {
            if ((scents[x][y] & 0b10000) && !forbidden[x][y] && (shortest_path(pos, Coordinate(x, y), board).size() > 0)) potential_safe.push_back(Coordinate(x, y));
        }
    }

    Coordinate risk_pos;
    // if there are multiple positions, we need to figure out which one could possibly be blocking
    // the gold - and that must be correct to move into since we assume the board is solvable
    if (potential_safe.size() > 1) {
        // remove any positions that are neither adjacent to positions which can contain gold, 
        // nor could contain gold themselves
        bool filtered = false;
        while (!filtered) {
            filtered = true;
            for (std::vector<Coordinate>::iterator it = potential_safe.begin(); it != potential_safe.end(); it++) {
                bool possible_path_to_gold = board[*it] & Tile["GOLD"];
                for (const Coordinate & adj:adjacent_positions(*it)) {
                    if (board[adj] & Tile["GOLD"]) possible_path_to_gold = true;
                }
                if (!possible_path_to_gold) {
                    potential_safe.erase(it);
                    filtered = false;
                    break;
                }
            }
        }
    }
    if (potential_safe.size() == 0) {
        // this board is guaranteed not solvable
        // don't let the wumpus have the last laugh :)
        if (log_actions) log("this board is not solvable :(");
        while (true) rot_cw();
    }
    else {
        // there is either just one position, or multiple equally good guesses
        risk_pos = potential_safe[0];
    }
    
    if (board[risk_pos] & Tile["WUMPUS"]) {
        shoot_at(risk_pos);
    }
    // mark the tile as safe since that's what we will assume from now on
    board.set(risk_pos, board[risk_pos] & 0b0100);
    return risk_pos;
}
