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
    return [
        [0, 1, 0, 0],
        [0, 1, 1, 0],
        [0, 0, 8, 1],
        [0, 2, 0, 1]
    ]

def test_shortest_path(board_sample1):
    # path from start (0, 0) at top left
    assert shortest_path(0, 0, 2, 2, board_sample1) == [(1, 0), (1, 0), (0, 1), (0, 1)]

    # path starting from a pit
    assert shortest_path(0, 1, 2, 2, board_sample1) is None

    # path from tile next to gold
    assert shortest_path(3, 2, 2, 2, board_sample1) == [(-1, 0),]

    # path entirely blocked by pits
    assert shortest_path(0, 3, 2, 2, board_sample1) is None