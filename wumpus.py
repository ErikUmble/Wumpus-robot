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



def shortest_path(start_x, start_y, end_x, end_y, board): 
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
    if end_x > 0:
        q.put((end_x - 1, end_y))
        costs[end_x - 1][end_y] = 1
    if end_x < WIDTH - 1:
        q.put((end_x + 1, end_y))
        costs[end_x + 1][end_y] = 1
    if end_y > 0:
        q.put((end_x, end_y -1))
        costs[end_x][end_y - 1] = 1
    if end_y < HEIGHT - 1:
        q.put((end_x, end_y + 1))
        costs[end_x][end_y + 1] = 1

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



class Robot:
    """
    Note: scents keeps track of the scent values recieved at each location on the board. 
    A 0 in scents means no scent has been recieved at that location yet. (we do not need to record
    the abscence of scent since this immediately gives us all the information it ever could about 
    surrounding tiles)
    """

    def __init__(self, board, x=0, y=0, dx=0, dy=1, has_gold=False):
        self.board = board
        
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.has_gold = has_gold

        # initialize scents with 0
        self.scents = []
        for j in range(WIDTH):
            col = []
            for i in range(HEIGHT):
                col.append(0)

    def start(self):
        while not self.has_gold:
            # TODO: choose a square to move to, go there, sniff, repeat
            raise NotImplementedError
        
        # now we have the gold, so return to origin
        self.move_to(0, 0)
        

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
        self.dx = -self.dy
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
        scent = 7  # temporary

        # update knowledge of surrounding board tiles
        self.scents[self.x][self.y] = scent
        for dx, dy in DIRECTIONS:
            if self.x + dx < WIDTH and self.y + dy < HEIGHT:
                self.board[self.x + dx][self.y + dy] &= scent

        self.eliminate()

    def eliminate(self):
        """
        For each board location, this checks to see if current information about the board
        state, combined with past scent information, can be used to deduce what the tile contains 
        through elimination
        """
        raise NotImplementedError


if __name__ == "__main__":
    # initialize board
    board = []
    for x in range(WIDTH):
        col = []
        for y in range(HEIGHT):
            col.append(Tile.UNKNOWN.value)
        board.append(col)
    
    # robot starts in location (0,0) which is safe
    board[0][0] = Tile.EMPTY.value
    robot = Robot(board)
    robot.start()

    