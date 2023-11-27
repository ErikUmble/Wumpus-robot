"""
0b0000 empty
0b0001 breeze (could contain a pit)
0b0010 stench (could contain a wumpus)
0b0100 glitter (could contain gold)
0b1000 gold 

"""

from enum import Enum

WIDTH = 4
HEIGHT = 4

class Tile(Enum):
    UNKNOWN = 0b111
    EMPTY = 0b000
    PIT = 0b001
    WUMPUS = 0b010
    GOLD = 0b100

class Robot:
    """
    Note: scents keeps track of the scent values recieved at each location on the board. 
    A 0 in scents means no scent has been recieved at that location yet. (we do not need to record
    the abscence of scent since this immediately gives us all the information it ever could about 
    surrounding tiles)
    """

    def __init__(self, board, x=0, y=0, dx=0, dy=1):
        self.board = board
        
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

        # initialize scents with -1
        self.scents = []
        for j in range(WIDTH):
            col = []
            for i in range(HEIGHT):
                col.append(0)

    def start(self):
        raise NotImplementedError
    
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
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            if self.x + dx < WIDTH and self.y + dy < HEIGHT:
                self.board[self.x + dx][self.y + dy] &= scent

        # we can possibly deduce more at this point based on previous scents
        # TODO: decide whether to make deduction here or wait until no known empty squares left



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

    