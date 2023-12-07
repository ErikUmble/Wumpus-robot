#ifndef _BOARD_
#define _BOARD_

#include <vector>
#include <unordered_map>
#include <string>
#include <iostream>

#include <fstream>
extern std::ofstream out;

const int WIDTH = 4, HEIGHT = 4;

class Coordinate {
    public:
    Coordinate(int x, int y) : x(x), y(y) {};
    Coordinate(): x(INT16_MIN), y(INT16_MIN) {};
    bool is_null() const {return x == INT16_MIN && y == INT16_MIN;}
    bool operator==(const Coordinate & other) const { return this->x == other.x && this->y == other.y; }
    Coordinate operator+(const Coordinate & other) const { return Coordinate(this->x + other.x, this->y + other.y); }
    bool in_bounds() const { return (0 <= x) && (x < WIDTH) && (0 <= y) && (y < HEIGHT); }
    friend std::ostream & operator<<(std::ostream & out, const Coordinate & c) {
        out << "(" << c.x << ", " << c.y << ")";
        return out;
    }
    int x, y;
};

std::ostream & operator<<(std::ostream & out, std::vector<Coordinate> v);

extern std::unordered_map<std::string, int> Tile; // treat as const - only is not const for the sake of [] accessor
extern const std::vector<Coordinate> DIRECTIONS;

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
    void set(const Coordinate & c, int tile) {board[c.x][c.y] = tile;}
    int get(const Coordinate & c) const {return board[c.x][c.y];}

    int operator[](const Coordinate & c) const {
        return board[c.x][c.y];
    }
    void reduce(int scent, const Coordinate & pos);
    void eliminate(const std::vector<std::vector<int> > & scents);

    friend std::ostream & operator<<(std::ostream & out, const Board & board);
    
    private:
    Coordinate get_unique_pos(int tile);
    int deduce(const Coordinate & pos, const std::vector<std::vector<int> > scents);

    std::vector<std::vector<int> > board;
    Coordinate gold_pos, wumpus_pos;
};

std::vector<Coordinate> shortest_path(const Coordinate & start, const Coordinate  &end, const Board & board);
std::ostream & operator<<(std::ostream & out, const std::vector<std::vector<int> > & v);

#endif