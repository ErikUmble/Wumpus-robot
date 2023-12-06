#ifndef _BOARD_
#define _BOARD_

#include <vector>
#include <unordered_map>
#include <string>


const int WIDTH = 4, HEIGHT = 4;

class Coordinate {
    public:
    Coordinate(int x, int y) : x(x), y(y) {};
    Coordinate(): x(INT16_MIN), y(INT16_MIN) {};
    bool is_null() const {return x == INT16_MIN && y == INT16_MIN;}
    bool operator==(const Coordinate & other) const { return this->x == other.x && this->y == other.y; }
    Coordinate operator+(const Coordinate & other) const { return Coordinate(this->x + other.x, this->y + other.y); }
    bool in_bounds() const { return (0 <= x) && (x < WIDTH) && (0 <= y) && (y < HEIGHT); }
    int x, y;
};


std::unordered_map<std::string, int> Tile = {{"UNKNOWN", 0b111}, {"EMPTY", 0b000}, {"PIT", 0b001}, {"WUMPUS", 0b010}, {"GOLD", 0b100}};
std::vector<Coordinate> DIRECTIONS;

std::vector<Coordinate> adjacent_positions(const Coordinate & pos);

class Board {
    public:
    friend class Robot;
    Board() {
        board = std::vector<std::vector<int> >(WIDTH, std::vector<int>(HEIGHT, Tile["UNKNOWN"]));

    }
    std::vector<int> & operator[](const int i) {
        return board[i];
    }
    int operator[](const Coordinate & c) const {
        return board[c.x][c.y];
    }
    void reduce(int scent, const Coordinate & pos);
    void eliminate(const int ** scents);
    
    private:
    Coordinate get_unique_pos(int tile);

    std::vector<std::vector<int> > board;
    Coordinate gold_pos, wumpus_pos;
};

std::vector<Coordinate> shortest_path(Coordinate start, Coordinate end, Board board);


#endif