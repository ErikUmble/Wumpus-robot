
#include <vector>
#include <iostream>
#include <queue>
#include <cassert>

#include "board.h"


std::ofstream out("output.txt");

// Note: when 0b1000 is sensed, this means the current tile contains gold and says nothing about surrounding tiles
// we still regard 0b100 to be tile gold value
std::unordered_map<std::string, int> Tile = {{"UNKNOWN", 0b111}, {"EMPTY", 0b000}, {"PIT", 0b001}, {"WUMPUS", 0b010}, {"GOLD", 0b100}};
const std::vector<Coordinate> DIRECTIONS = {Coordinate(0, 1), Coordinate(1, 0), Coordinate(0, -1), Coordinate(-1, 0)};


std::vector<Coordinate> adjacent_positions(const Coordinate & pos) {
    std::vector<Coordinate> adjacent;
    for (const Coordinate & dir: DIRECTIONS) {
        int x = pos.x + dir.x, y = pos.y + dir.y;
        if (x >= 0 && x < WIDTH && y >= 0 && y < HEIGHT)
            adjacent.push_back(Coordinate(x, y));
    }
    return adjacent;
}

std::vector<Coordinate> shortest_path(const Coordinate & start, const Coordinate  &end, const Board & board) {
    /*
    given a board[WIDTH][HEIGHT] of Tile enum values,
    this returns a list of the form [(dx1, dy1), (dx2, dy2), ...] if there is a path
    from (start_x, start_y) to (end_x, end_y) on the board, which only passes through
    empty tiles and only moves verticall or horizontally in each step (ie. one of dx or dy will
    always be 0 in each pair).

    returns empty vector if no path can be determined (or if start equals end).

    Uses Dijikstra's shortest path algorithm
    */

   std::vector<Coordinate> path;
   // end early if start == end, or 
   if ((start.x >= WIDTH) || (end.x >= WIDTH) || (start.y >= HEIGHT) || (end.y >= HEIGHT)
    || (start == end)) return path;

    // initialize cost to each location to MAX_VALUE
    int MAX_VALUE = WIDTH * HEIGHT; // no valid path can take this many moves
    std::vector<std::vector<int> > costs(WIDTH, std::vector<int>(HEIGHT, MAX_VALUE));

    // end location has cost of 0 to get to (because zero moves needed if we start there)
    costs[end.x][end.y] = 0;

    // initialize queue with tiles adjacent to end position
    // invariant: only add valid coordinates to the queue
    std::queue<Coordinate> q;
    for (Coordinate c: adjacent_positions(end)) {
        q.push(c);
        costs[c.x][c.y] = 1;
    }

    while (!q.empty()) {
        Coordinate c = q.front();
        q.pop();

        // do not consider path through unsafe tile (Note empty = 0 and gold = 8)
        if (board[c] & 0b011) {
            // set cost to 1 more than max value so e don't consider it again
            costs[c.x][c.y] = MAX_VALUE + 1;
            continue;
        }

        // end early if we have already reached the start location
        if (c == start) break;

        // look for the locations we can get to by taking one step from here
        for (Coordinate adj: adjacent_positions(c)) {
            if (costs[adj.x][adj.y] == MAX_VALUE) {
                // we have not considered this tile yet so it is one step more than this
                q.push(adj);
                costs[adj.x][adj.y] = costs[c.x][c.y] + 1;
            }
        }
    }
    // no path if start location has path cost at least as high as max value
    if (costs[start.x][start.y] >= MAX_VALUE) return path;
    // path exists, so compute the directions it follows
    Coordinate c = start;
    while (costs[c.x][c.y] > 0) {
        for (const Coordinate & dir: DIRECTIONS) {
            if (!(c + dir).in_bounds()) continue;

            // the next location along the path always has 1 less move to go until the end
            if (costs[c.x + dir.x][c.y + dir.y] == costs[c.x][c.y] - 1) {
                path.push_back(dir);
                c = c + dir;
                break;
            }
        }
    }

    return path;
}

void Board::reduce(int scent, const Coordinate & pos) {
    /*
    Given scent (one of Tile values) at a particualar position (x, y)
    this reduces the possibilities of surrounding tiles based on that information. 
    */
   // Note: when 0b1000 is sensed, this means the current tile contains gold and says nothing about surrounding tiles
    if (scent == 0b1000) {
        board[pos.x][pos.y] = Tile["GOLD"];
        gold_pos = pos;
        return;
    }
   
   for (const Coordinate c: adjacent_positions(pos)) {
       board[c.x][c.y] &= scent;
   }

   // since there is just 1 gold and 1 wumpus, we can further reduce from these scents
   if ((scent & Tile["GOLD"]) || (scent & Tile["WUMPUS"])) {
        // create a mask that is 0 everywhere except where there is a gold or wumpus
        int mask = ~(scent & (Tile["GOLD"] | Tile["WUMPUS"]));

        // apply the mask to every location expect for the 4 adjacent to where the scent is
        for (int x = 0; x < WIDTH; x++) {
            for (int y = 0; y < HEIGHT; y++)
                if (abs(x - pos.x) + abs(y - pos.y) > 1)
                    board[x][y] &= mask;
        }

   }
}

Coordinate Board::get_unique_pos(int tile) {
    std::vector<Coordinate> possible_pos;
    for (int x = 0; x < WIDTH; x++) {
        
        for (int y = 0; y < HEIGHT; y++){
            if (possible_pos.size() > 1)
            break;
            if (board[x][y] & tile)
                possible_pos.push_back(Coordinate(x, y));
        }  
    }
    if (possible_pos.size() == 1) {
        return possible_pos[0];
    }
        
    else
        return Coordinate();
}

int Board::deduce(const Coordinate & pos, const std::vector<std::vector<int> > scents) {
    /*
    the the tile at position pos can be fully determined by the scents provided, this returns
    that tile value,
    otherwise it returns -1
    */

    // use scents to eliminate if adjacent tiles to a scent have been determined
    // intuition: if a tile had the scent of a pit but three adjacent tiles are known to not be pits, then make
    // the one possible title a guaranteed pit (same for wumpus and gold)
    if ((scents[pos.x][pos.y] & 0b10000) == 0) return -1; // skip unsniffed locations 
    for (const int tile: {Tile["PIT"], Tile["WUMPUS"], Tile["GOLD"]}) {
        
        if ((scents[pos.x][pos.y] & tile) == 0) continue; // skip this tile type since we did not sense it here
        
        std::vector<Coordinate> possible_pos;

        for (const Coordinate adj: adjacent_positions(pos)) {
            if (board[adj.x][adj.y] & tile)
                possible_pos.push_back(adj);
        }
        if (possible_pos.size() == 1) {
            return tile;
        }
    }
    return - 1;
}

void Board::eliminate(const std::vector<std::vector<int> > & scents) {
    /*
    For each board location, this checks to see if current information about the board
    state, combined with past scent information, can be used to deduce what the tile contains 
    through elimination
    */

    // deduce at each location
    int tile;
    for (int x = 0; x < WIDTH; x++) {
        for (int y = 0; y < HEIGHT; y++) {
            tile = deduce(Coordinate(x, y), scents);
            if (tile > -1) board[x][y] = tile;
        }
    }

    // if we do not know where the wumpus or gold is, see if there is only option for where it can be
    if (wumpus_pos.is_null()) {
        wumpus_pos = get_unique_pos(Tile["WUMPUS"]);
        if (!wumpus_pos.is_null()) board[wumpus_pos.x][wumpus_pos.y] = Tile["WUMPUS"];
    }
    if (gold_pos.is_null()) {
        gold_pos = get_unique_pos(Tile["GOLD"]);
        if (!gold_pos.is_null()) board[gold_pos.x][gold_pos.y] = Tile["GOLD"];
    }

}


std::ostream & operator<<(std::ostream & out, const Board & board) {
    /*
    prints out the board with (0, 0) in lower left corner
    */
   out << board.board;
   return out;
}
std::ostream & operator<<(std::ostream & out, const std::vector<std::vector<int> > & v) {
    /*
    prints of the 2d vector v with the shap of board with (0, 0) in lower left corner
    */
    assert(v.size() == WIDTH && v[0].size() == HEIGHT);
    for (int y = HEIGHT - 1; y >= 0; y--) {
         for (int x = 0; x < WIDTH; x++) {
              out << v[x][y] << " ";
         }
         out << std::endl;
    }
    return out;
}

std::ostream & operator<<(std::ostream & out, std::vector<Coordinate> v) {
    for (const Coordinate & c: v) {
        out << c << " ";
    }
    out << std::endl;
    return out;
}