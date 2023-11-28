import pytest
from wumpus import *

# Note: because we access the board with board[x][y], each list inside board is a column
# which is visually counterintuitive

@pytest.fixture
def board_sample1():
    """
    this board in coordinate plane format:
    0 0 1 1
    0 1 8 0
    1 1 0 2
    0 0 0 0 
    """
    return Board([
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 8, 1],
        [0, 2, 0, 1]
    ])

def test_shortest_path(board_sample1):
    # path from start (0, 0) at top left
    assert shortest_path(0, 0, 2, 2, board_sample1) == [(1, 0), (1, 0), (0, 1), (0, 1)]

    # path starting from a pit
    assert shortest_path(0, 1, 2, 2, board_sample1) is None

    # path from tile next to gold
    assert shortest_path(3, 2, 2, 2, board_sample1) == [(-1, 0),]

    # path entirely blocked by pits
    assert shortest_path(0, 3, 2, 2, board_sample1) is None


def test_board_deductions():
    # check that reduce behaves as expected
    board = Board()
    board.reduce(Tile.GOLD.value, 1, 1)
    board.reduce(Tile.GOLD.value, 2, 2)
    board.reduce(Tile.GOLD.value, 1, 3)
    assert board == Board([[3, 0, 3, 0], 
                           [0, 3, 4, 3], 
                           [3, 0, 3, 0], 
                           [3, 3, 0, 3]])

    # check that eliminate correctly determines the location of gold
    board.eliminate(None)
    assert board.gold_pos == (1, 2)