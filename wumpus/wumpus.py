"""
wumpus.py
This module provides the logical backend to a Wumpus World solving robot. To
use this for your own robot (whether micropython, virtual, or simulated, etc.),
simply subclass Robot and provide implementations for the following 5 methods:

    receive_scent(self) -> int
    shoot(self)
    rot_ccw
    rot_cw
    forward

You may optionally override rot_180 if you wish to provide a more efficient or effective
implementation than the default which simply rotates cw twice.

From there, you can call robot.start() to have the robot solve the Wumpus World.

If you would like to log the robot's actions, you can set log_actions to True in the Robot constructor,
and this will produce a log.txt file with actions taken and knowledge at different stages in the solution which can 
be useful for debugging.

recieve_scent should return one of the following values:

    0b1000 only when recieving_scent at gold position exactly

    otherwise, some oring of the following values:
        0b0000 empty
        0b0001 breeze (could contain a pit)
        0b0010 stench (could contain a wumpus)
        0b0100 glitter (could contain gold)

shoot is an event handle for when the robot decides to shoot an arrow. Depending on your implementation of the robot,
this method may neeed do something like printing/logging a message, physically shooting an arrow, or reporting a message with bluetooth,
and can do so in the shoot method.

rot_ccw and rot_cw should rotate the robot 90 degrees counter-clockwise and clockwise respectively.

forward should move the robot one block forward in the direction it is facing.

"""

WIDTH = 4
HEIGHT = 4

# Valid movement directions are one tile horizontally or vertically
DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]

class Queue(list):
    # Queue as a list for micropython support
    def put(self, item):
        self.append(item)
    def get(self):
        return self.pop(0)
    def empty(self):
        return len(self) == 0

class Tile:
    UNKNOWN = 0b111
    EMPTY = 0b000
    PIT = 0b001
    WUMPUS = 0b010
    GOLD = 0b100
    UNSNIFFED = 0b10000  # only used inside the scents list


class States:
    # State values increase in order of progression into the solution
    INITIAL = 0
    GOLD_KNOWN = 1
    HAS_GOLD = 2
    FINISHED = 3

    
def adjacent_positions(x, y):
    """
    returns a list of (adjacent_x, adjacent_y) pairs that are valid and adjacent to (x, y)
    """
    adjacent = []
    for dx, dy in DIRECTIONS:
        if (0 <= x + dx < WIDTH) and (0 <= y + dy < HEIGHT):
            adjacent.append((x + dx, y + dy))
    return adjacent

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
    MAX_VALUE = WIDTH * HEIGHT  # no valid path can take this many moves
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

        # do not consider path through potentially dangerous tile (Note empty = 0 and gold = 8)
        if board[x][y] & 0b011 != 0:
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
    
    # path exists, so compute the directions it follows
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
                col.append(Tile.UNKNOWN)
            self.append(col)

        

    def reduce(self, scent, x, y):
        """
        Given scent (one of Tile values) at a particualar position (x, y)
        this reduces the possibilities of surrounding tiles based on that information.

        Note: when 0b1000 is sensed, this means the current tile contains gold and says nothing
        about surrounding tiles.
        """
        if (scent == 0b1000):
            self[x][y] = Tile.GOLD
            self.gold_pos = (x, y)
            return
        
        for x_adj, y_adj in adjacent_positions(x, y):
            self[x_adj][y_adj] &= scent
        
        # since there is just 1 gold and 1 wumpus, we can further reduce from these scents
        if scent & Tile.GOLD or scent & Tile.WUMPUS:
            # create a mask that is zero only in gold and/or wumpus location respectively if they are in the scent
            mask = ~(scent & (Tile.GOLD | Tile.WUMPUS))
            
            # apply mask to every location except for the 4 adjacent to where the scent is
            for _x in range(WIDTH):
                for _y in range(HEIGHT):
                    if abs(x - _x) + abs(y - _y) != 1:
                        self[_x][_y] &= mask
            
    def deduce(self, x, y, scents):
        """
        if the tile at position (x, y) can be fully determined by the scents provided, this returns
        that tile value,
        otherwise it returns Tile.UNKNOWN 
        """
        # intuition: consider adjacent positions, and if any of them sensed something that is definitely 
        # not at any of its other adjacent positions, then it must be at the current position
        for _x, _y in adjacent_positions(x, y):
            if scents[_x][_y] == 0:
                # definitely safe if adjacent tile had no scent
                return Tile.EMPTY
            if scents[_x][_y] & Tile.UNSNIFFED:
                continue

            for tile in [Tile.PIT, Tile.WUMPUS, Tile.GOLD]:
                if (scents[_x][_y] & tile) == 0:
                    # skip if this tile type was not scented here
                    continue
                possible_pos = []

                for __x, __y in adjacent_positions(_x, _y):
                    # add neighbors that are not the current tile
                    if self[__x][__y] & tile and (__x, __y) != (x, y):
                        possible_pos.append((__x, __y))

                if len(possible_pos) == 0:
                    # no other options for where that scent could be coming from
                    return tile
        return Tile.UNKNOWN
        
    def eliminate(self, scents):
        """
        For each board location, this checks to see if current information about the board
        state, combined with past scent information, can be used to deduce what the tile contains 
        through elimination
        """
        def get_unique_pos(tile):
            # returns the (x, y) pair if there is only (exactly) one possible location for the tile on the board
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
                if scents[x][y] == Tile.UNSNIFFED:
                    continue

                for tile in [Tile.PIT, Tile.GOLD, Tile.WUMPUS]:
                    if (scents[x][y] & tile) == 0:
                        # did not sense this tile type here
                        continue

                    possible_pos = []
                    for _x, _y in adjacent_positions(x, y):
                        if self[_x][_y] & tile:
                            possible_pos.append((_x, _y))

                    if len(possible_pos) == 1:
                        _x, _y = possible_pos[0]
                        self[_x][_y] = tile

        # if we do not know where the wumpus or gold is, see if there is only option for where it can be
        self.gold_pos = self.gold_pos or get_unique_pos(Tile.GOLD)
        self.wumpus_pos = self.gold_pos or get_unique_pos(Tile.WUMPUS)
    
    def __str__(self):
        """
        string of board with (0, 0) in lower left
        """
        s = ""
        for y in range(HEIGHT - 1, -1, -1):
            for x in range(WIDTH):
                s += str(self[x][y]) + " "
            s += "\n"
    
class Robot:
    """
    Note: scents keeps track of the scent values recieved at each location on the board. 
    A 0 in scents means no scent has been recieved at that location yet. (we do not need to record
    the abscence of scent since this immediately gives us all the information it ever could about 
    surrounding tiles)
    """

    def __init__(self, board=None, x=0, y=0, dx=1, dy=0, state=States.INITIAL, log_actions=False):
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
        self.log_actions = log_actions
        self.has_arrow = True

        self.start_pos = (x, y)

        # initialize scents with 0
        self.scents = []
        for j in range(WIDTH):
            col = []
            for i in range(HEIGHT):
                col.append(Tile.UNSNIFFED)

    def start(self):
        while self.state < States.GOLD_KNOWN:
            explore_pos = self.get_explore_position()
            # if there are no safe places to explore, shoot the wumpus and explore from that location
            if explore_pos is None:
                if self.board.wumpus_pos is not None and self.has_arrow:
                    # we know where the wumpus is, and still have an arrow to use
                    explore_pos = self.board.wumpus_pos
                    self.shoot_at(*self.board.wumpus_pos)
                else:
                    # we are in a situation where we must enter a potentially dangerous tile
                    # so we will just yolo it and hope for the best
                    # Note: this can only arise in boards where the robot must be able to know that it is solvable for it to be solvable
                    explore_pos = self.yolo()

            self.move_to(*explore_pos)
            self.sniff()
            self.board.eliminate(self.scents)
            if self.board.gold_pos is not None:
                self.state = States.GOLD_KNOWN
                break

        assert(self.board.gold_pos is not None)
        if self.log_actions:
            self.log("FOUND GOLD")

        gold_pos = self.board.gold_pos
        while not self.move_to(*gold_pos):
            # shoot wumpus or continue yoloing as neccessary until the path to gold is clear
            if self.board.wumpus_pos is not None and self.has_arrow:
                self.shoot_at(*self.board.wumpus_pos)
            else:
                self.move_to(*self.yolo())
        self.state = States.HAS_GOLD
        if self.log_actions:
            self.log("RETRIEVED GOLD")

        # now we have the gold, so return to origin
        self.move_to(*self.start_pos)
        self.state = States.FINISHED
        
    def get_explore_position(self):
        """
        returns the (x, y) pair for the best position to visit next
        (x, y) is guaranteed to be an empty tile (and in pracice this means there is a safe route to it)
        unvisited, safe positions are ranked by the sum of tile options adjacent to them since higher possibility sums
        means more expected information from a scent at that location. Ties are broken by the nearest tile to the robot winning.
        """
        if self.log_actions:
            self.log("current board knowledge:\n" + str(self.board))

        max_sum = 0
        best_pos = None
        for x in range(WIDTH):
            for y in range(HEIGHT):
                potential = (x, y)
                # skip tiles that are not known to be safe
                if self.board[x][y] & 0b011:
                    continue

                # skip tiles that we already sniffed at 
                if self.scents[x][y] & Tile.UNSNIFFED:
                    continue
                
                sum = 0
                for adj in adjacent_positions(x, y):
                    sum += self.board[adj[0]][adj[1]]
                    # a tile is highly valuable if it is adjacent to a tile that scented gold
                    if (self.scents[adj[0]][adj[1]] & Tile.GOLD) and (self.board[x][y] & Tile.GOLD):
                        sum += 100
                if sum > max_sum or (sum == max_sum and self.distance(self.start_pos, potential) < self.distance(self.start_pos, best_pos)):
                    max_sum = sum
                    best_pos = potential
        return best_pos
    
    def sniff(self):
        """
        calls receive_scent, stores that scent, and uses it for deduction
        Override receive_scent, not sniff for different system subclasses
        """
        scent = self.receive_scent()
        if self.log_actions:
            self.log(f"recieved scent {scent} at {self.x}, {self.y}")
        self.scents[self.x][self.y] = scent
        self.board.reduce(scent, self.x, self.y)

    def rotate(self, dx, dy):
        """
        rotates until robot is facing the given direction
        """
        if dx == -self.dy and dy == self.dx:
            self._rot_ccw()
        elif (dx == -self.dx and dx != 0) or (dy == -self.dy and dy != 0):
            self._rot_180()
        else:
            while not (self.dx == dx and self.dy == dy):
                self._rot_cw()

    def move_to(self, x, y):
        """
        Uses the shortest valid path (if it exists) to move to board[x][y]
        returns False if unable to make the movement
        """
        if self.log_actions:
            self.log(f"moving to {x}, {y}")

        if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
            return False
        
        path = shortest_path(self.x, self.y, x, y, self.board)
        if path is None:
            return False
        
        self.follow_path(path)
        return True


    def follow_path(self, path):
        """
        Given a path of directions [(dx1, dy1), (dx2, dy2), ...]
        this moves the robot along that path in that order
        """
        for dx, dy in path:
            self.rotate(dx, dy)
            self.forward()

    def yolo(self):
        """
        call this if there are no known safe places to explore
        this uses the fact that the board is supposed to be solveable to make a logical deduction
        as to where it must move next if it is going to reach the gold
        this will take risks such as shooting at a guess of where the wumpus is, or moving into
        a tile that might contain a pit, but does so in a way that is guaranteed to be safe if the board is solvable
        this returns the coordinate to move into next (which is marked as safe, even though it could be a risk)
        the returned tile definitely does not have the wumpus in it (we shoot at it before returning if there is a chance)

        Note: this should only be called if the robot knows the board is solvable
        Note: calling yolo multiple times in a row is acceptable
        """
        if self.log_actions:
            self.log("resorting to yolo - this board had better be solvable :)")
        # first, find out all the positions we know absolutely are bad to move into
        forbidden = []
        for x in range(WIDTH):
            col = []
            for y in range(HEIGHT):
                tile = self.board.deduce(x, y, self.scents)
                # forbid tiles known to be pits
                if tile == Tile.PIT:
                    col.append(True)
                else:
                    col.append(False)
            forbidden.append(col)

        # then, consider the collection of positions that we have not sniffed at, but might be safe, and are reachable
        # by moving through only known safe tiles
        potential_safe = []
        for x in range(WIDTH):
            for y in range(HEIGHT):
                if (self.scents[x][y] & Tile.UNSNIFFED) and not forbidden[x][y] and len(shortest_path(self.x, self.y, x, y, self.board)) > 0:
                    potential_safe.append((x, y))

        risk_pos = None
        # if there are multiple positions, we need to figure out which one could possibly be blocking
        # the gold - and that must be correct to move into since we assume the board is solvable
        if len(potential_safe) > 1:
            # remove any positions that are neither adjacent to positions which can contain gold, 
            # nor could contain gold themselves
            filtered = False
            while not filtered:
                filtered = True
                for pos in potential_safe:
                    possible_path_to_gold = self.board[pos[0]][pos[1]] & Tile.GOLD
                    for adj in adjacent_positions(*pos):
                        if self.board[adj[0]][adj[1]] & Tile.GOLD:
                            possible_path_to_gold = True
                    if not possible_path_to_gold:
                        potential_safe.remove(pos)
                        filtered = False
                        break
            if len(potential_safe) == 0:
                # this board is guaranteed not solvable
                # don't let the wumpus have the last laugh :)
                if self.log_actions:
                    self.log("this board is not solvable :(")
                while True:
                    self._rot_cw()
        else:
            # there is either just one position, or multiple equally good guesses
            risk_pos = potential_safe[0]

        if self.board[risk_pos[0]][risk_pos[1]] & Tile.WUMPUS:
            self.shoot_at(*risk_pos)
        # mark the tile as safe since that's what we will assume from now on
        self.board[risk_pos[0]][risk_pos[1]] = self.board[risk_pos[0]][risk_pos[1]] & Tile.EMPTY
        return risk_pos

    def log(self, message):
        with open("log.txt", "a") as f:
            f.write(message + "\n")

    def shoot_at(self, x, y):
        """
        shoots at the location (x, y) and updates the board
        """
        path = shortest_path(self.x, self.y, x, y, self.board)
        if path is None:
            raise Exception("Cannot shoot at that location")
        aim_x, aim_y = path.pop()
        self.follow_path(path)
        self.rotate(aim_x, aim_y)

        if self.log_actions:
            self.log(f"shooting at {x}, {y}")

        if self.has_arrow:
            self.shoot()
        else:
            return
        self.has_arrow = False

        # zero out the wumpus bit from the target position by setting the bit to 1 then flipping it
        self.board[x][y] = (self.board[x][y] | Tile.WUMPUS) ^ Tile.WUMPUS

    def _rot_cw(self):
        """
        rotates 90 degrees clockwise
        """
        # update direction state (eg. (dx, dy) = (1, 0) becomes (0, -1))
        tmp_dx = self.dx
        self.dx = self.dy
        self.dy = -tmp_dx

        self.rot_cw()
    
    def _rot_ccw(self):
        """
        rotates 90 degrees clockwise
        """
        # update direction state (eg. (dx, dy) = (1, 0) becomes (0, 1))
        tmp_dx = self.dx
        self.dx = -self.dy
        self.dy = tmp_dx

        self.rot_ccw()

  
    def _rot_180(self):
        """
        rotates 180 degrees
        """
        self.dx = -self.dx
        self.dy = -self.dy

        self.rot_180()

    def _forward(self):
        """
        moves one block forward
        """
        # update state
        self.x += self.dx
        self.y += self.dy

        self.forward()

    def rot_180(self):
        self.rot_cw()
        self.rot_cw()

    def rot_cw(self):
        raise NotImplementedError("Must implement rot_cw in subclass")

    def rot_ccw(self):
        raise NotImplementedError("Must implement rot_ccw in subclass")

    def receive_scent(self):
        raise NotImplementedError("Must implement recieve_scent in subclass")
    
    def shoot(self):
        raise NotImplementedError("Must implement shoot in subclass")
    
    def forward(self):
        raise NotImplementedError("Must implement forward in subclass")


    
