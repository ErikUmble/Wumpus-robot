"""
0b0000 empty
0b0001 breeze (could contain a pit)
0b0010 stench (could contain a wumpus)
0b0100 glitter (could contain gold)
0b1000 gold 

"""

from enum import Enum
from queue import Queue

WIDTH = 4
HEIGHT = 4

# Valid movement directions are one tile horizontally or vertically
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

class Tile(Enum):
    UNKNOWN = 0b111
    EMPTY = 0b000
    PIT = 0b001
    WUMPUS = 0b010
    GOLD = 0b100


class States(Enum):
    # State values increase in order of progression into the solution
    INITIAL = 0
    GOLD_KNOWN = 1
    HAS_GOLD = 2
    FINISHED = 3

    
def adjacent_positions(x, y):
    """
    returns a list of (adjacent_x, adjacent_y) pairs that are valid and adjacent to (x, y)
    """
    positions = []
    for dx, dy in DIRECTIONS:
        if (0 <= x + dx < WIDTH) and (0 <= y + dy < HEIGHT):
            positions.append((x + dx, y + dy))
    return positions

def shortest_path(start_x, start_y, end_x, end_y, board : list):
    """
    given a board[WIDTH][HEIGHT] of Tile enum values,
    this returns a list of the form [(dx1, dy1), (dx2, dy2), ...] if there is a path
    from (start_x, start_y) to (end_x, end_y) on the board, which only passes through
    empty tiles and only moves verticall or horizontally in each step (ie. one of dx or dy will
    always be 0 in each pair).

    returns None if no path can be determined.

    Uses Dijikstra's shortest path algorithm

    """
    if start_x >= WIDTH or end_x >= WIDTH or start_y >= HEIGHT or end_y >= HEIGHT:
        return None
    
    costs = []
    MAX_VALUE = WIDTH * HEIGHT + 1  # no valid path can take this many moves
    for x in range(WIDTH):
        col = []
        for j in range(HEIGHT):
            col.append(MAX_VALUE)
        costs.append(col)

    # the end location has a cost of 0 to get to
    costs[end_x][end_y] = 0

    # initialize queue with tiles adjacent to end position
    # invariant: only add valid coordinates to the queue
    q = Queue()
    for x, y in adjacent_positions(end_x, end_y):
        q.put((x, y))
        costs[x][y] = 1

    while not q.empty():
        x, y = q.get()

        # do not consider path through unknown tile (Note empty = 0 and gold = 8)
        if board[x][y] & 0b111:
            # set this cost to 1 more than max value so we don't try to consider it again
            costs[x][y] = MAX_VALUE + 1
            continue

        # end early if we have already reached the start location
        if x == start_x and y == start_y:
            break

        for dx, dy in DIRECTIONS:
            if not (0 <= x + dx < WIDTH) or not (0 <= y + dy < HEIGHT):
                continue
            if (costs[x + dx][y + dy] == MAX_VALUE):
                # we have not considered that tile yet so it is one step more than this
                q.put((x + dx, y + dy))
                
                costs[x + dx][y + dy] = costs[x][y] + 1
            

    print(costs)
    # no path if start location has path cost at least as high as max value
    if costs[start_x][start_y] >= MAX_VALUE:
        return None
    
    # path exists, so compute the cordinates it follows
    x, y = start_x, start_y
    path = []
    while costs[x][y] > 0:
        for dx, dy in DIRECTIONS:
            if not (0 <= x + dx < WIDTH) or not (0 <= y + dy < HEIGHT):
                continue
            if costs[x + dx][y + dy] == costs[x][y] - 1:
                path.append((dx, dy))
                x += dx
                y += dy
                break
                
    return path

class Board(list):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.gold_pos = None
        self.wumpus_pos = None

        # initialize board if not done already
        if len(self) > 0:
            return
        
        for x in range(WIDTH):
            col = []
            for y in range(HEIGHT):
                col.append(Tile.UNKNOWN.value)
            self.append(col)

        

    def reduce(self, scent, x, y):
        """
        Given scent (one of Tile values) at a particualar position (x, y)
        this reduces the possibilities of surrounding tiles based on that information.
        """
        for dx, dy in DIRECTIONS:
            if x + dx < WIDTH and y + dy < HEIGHT:
                self[x + dx][y + dy] &= scent
        
        # since there is just 1 gold and 1 wumpus, we can further reduce from these scents
        if scent & Tile.GOLD.value or scent & Tile.WUMPUS.value:
            # create a mask that is zero only in gold and/or wumpus location respectively if they are in the scent
            mask = ~(scent & (Tile.GOLD.value | Tile.WUMPUS.value))
            
            # apply mask to every location except for the 4 adjacent to where the scent is
            for _x in range(WIDTH):
                for _y in range(HEIGHT):
                    if abs(x - _x) + abs(y - _y) != 1:
                        self[_x][_y] &= mask
            

    def eliminate(self, scents):
        """
        For each board location, this checks to see if current information about the board
        state, combined with past scent information, can be used to deduce what the tile contains 
        through elimination
        """
        def get_unique_pos(tile):
            possible_pos = []
            for x in range(WIDTH):
                if len(possible_pos) > 1:
                        break
                for y in range(HEIGHT):
                    if self[x][y] & tile:
                        possible_pos.append((x, y))
            if len(possible_pos) == 1:
                return possible_pos[0]
            return None

        # use scents to eliminate if adjacent tiles to a scent have been determined
        # intuition: if a tile had the scent of a pit but three adjacent tiles are known to not be pits, then make
        # the one possible title a guaranteed pit (same for wumpus and gold)
        # do this for every tile with a nonzero scent
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if scents[x][y] == 0:
                    continue
                for tile in [Tile.PIT, Tile.GOLD, Tile.WUMPUS]:
                    if (scents[x][y] & tile.value) == 0:
                        continue
                    possible_pos = []
                    for _x, _y in adjacent_positions(x, y):
                        if self[_x][_y] & tile.value:
                            possible_pos.append((_x, _y))
                    if len(possible_pos) == 1:
                        _x, _y = possible_pos[0]
                        self[_x][_y] = tile.value

        # if we do not know where the wumpus or gold is, see if there is only option for where it can be
        self.gold_pos = self.gold_pos or get_unique_pos(Tile.GOLD.value)
        self.wumpus_pos = self.gold_pos or get_unique_pos(Tile.WUMPUS.value)


class Robot:
    """
    Note: scents keeps track of the scent values recieved at each location on the board. 
    A 0 in scents means no scent has been recieved at that location yet. (we do not need to record
    the abscence of scent since this immediately gives us all the information it ever could about 
    surrounding tiles)
    """

    def __init__(self, board=None, x=0, y=0, dx=0, dy=1, state=States.INITIAL):
        """
        board[WIDTH][HEIGHT] of int may be specified if the robot has initial knowledge of the terrain - 
            default: each tile except (0,0) has every possibility
        x, y initial coordinates
        dx, dy initial direction
        state can be specified to initialize the robot at different situations

        """
        self.board = board or Board()
        # robot must start at a safe location, so mark it as such
        # Note: it could start at the gold
        self.board[x][y] &= 0b1100    
        
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.state = state

        self.start_pos = (x, y)

        # initialize scents with 0
        self.scents = []
        for j in range(WIDTH):
            col = []
            for i in range(HEIGHT):
                col.append(0)

    def start(self):
        # TODO: determine whether or not to shoot the wumpus
        while self.state.value < States.GOLD_KNOWN:
            x, y = self.get_explore_position()
            self.move_to(x, y)
            self.sniff()
            self.board.eliminate()

            if self.board.gold_pos:
                self.state = States.GOLD_KNOWN
                break
        
        assert(self.board.gold_pos is not None)
        gx, gy = self.board.gold_pos
        self.move_to(gx, gy)
        self.state = States.HAS_GOLD
        
        # now we have the gold, so return to origin
        sx, sy = self.start_pos
        self.move_to(sx, sy)
        self.state = States.FINISHED
        
    def get_explore_position(self):
        """
        returns the (x, y) pair for the best position to visit next
        (x, y) is guaranteed to be an empty tile (and in pracice this means there is a safe route to it)
        unvisited, safe positions are ranked by the sum of tile options adjacent to them since higher possibility sums
        means more expected information from a scent at that location. Ties are broken by the nearest tile to the robot winning.
        """
        def distance(x, y):
            # distance herisitic
            # return absolute difference between x values and y values instead of computing path length
            return abs(x - self.x) + abs(y - self.y)
        
        max_sum = 0
        best_x, best_y = self.x, self.y
        for x in range(WIDTH):
            for y in range(HEIGHT):
                sum = 0
                for _x, _y in adjacent_positions(x, y):
                    sum += self.board[_x][_y]
                if sum > max_sum or (sum == max_sum and (distance(x, y) < distance(best_x, best_y))):
                    max_sum = sum
                    best_x, best_y = x, y
        return best_x, best_y

    def move_to(self, x, y):
        """
        Uses the shortest valid path (if it exists) to move to board[x][y]
        returns False if unable to make the movement
        """
        if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
            return False
        
        path = shortest_path(self.x, self.y, x, y, self.board)
        if path is None:
            return False
        
        for dx, dy in path:
            # naieve just uses cw rotation for now
            while dx != self.dx or dy != self.dy:
                self.rot_cw()
            self.forward()
        return True

    def rot_cw(self):
        """
        rotates 90 degrees clockwise
        """
        # update direction state (eg. (dx, dy) = (1, 0) becomes (0, -1))
        tmp_dx = self.dx
        self.dx = self.dy
        self.dy = -tmp_dx

        # TODO: use motors to rotate physical bot
        raise NotImplementedError
    
    def rot_ccw(self):
        """
        rotates 90 degrees clockwise
        """
        # update direction state (eg. (dx, dy) = (1, 0) becomes (0, 1))
        tmp_dx = self.dx
        self.dx = -self.dy
        self.dy = tmp_dx

        # TODO: use motors to rotate physical bot
        raise NotImplementedError
    
    def forward(self):
        """
        moves one block forward
        """
        # update state
        self.x += self.dx
        self.y += self.dy

        # TODO: use motors to move physical bot
        raise NotImplementedError
    
    def sniff(self):
        # TODO: get scent wirelessly
        raise NotImplementedError
        scent = 7  # temporary

        # update knowledge of surrounding board tiles
        self.scents[self.x][self.y] = scent
        self.board.reduce(scent, self.x, self.y)


if __name__ == "__main__":
    robot = Robot()
    robot.start()

    
