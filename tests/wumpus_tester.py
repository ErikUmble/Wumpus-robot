#!/usr/bin/python3

"""
source: https://github.com/tfdahlin/WumpusTester/blob/main/tester.py
author: tfdahlin
GNU GENERAL PUBLIC LICENSE

Usage
./tester.py <your_executable> <difficulty> [--enable_hardest]

How to use
When you have compiled your code, you can run this tester against your code to see whether or not it passes the sample Wumpus World puzzles I have included in this script. There are three different difficulties of puzzles (easy, medium, and hard), and three puzzles at each difficulty, for a total of 9 puzzles. Additionally, if you think your solution is particularly clever, you can test it against my diabolical example.

This script is a little finnicky about how it expects input to be formatted in order for it to work. It assumes that your robot starts in the bottom left corner, which is considered southwest, and it expects your program to print to stdout in the following format:
Movement commands: "n", "e", "s", "w" (for north, east, south, west)
Kill commands: "kill n", "kill e", "kill s", "kill w" (for killing the Wumpus)
Request input: "input:"
If text besides what is listed above is printed to stdout, it will assume you have made a mistake, and will fail the test, so be careful about spelling. Furthermore, it assumes that there will not be excess newlines, and that there will be a newline after each input.
"""

import subprocess, io, sys, argparse
import os

class Tile:
    """State representation of a single tile in the Wumpus World."""
    def __init__(self, x, y, content):
        self.x = x
        self.y = y
        self.content = content
        self.visited = False
        pass
    def __str__(self):
        return self.content
    def visit(self):
        self.visited = True
    def is_visited(self):
        return self.visited

class World:
    """State representation of the Wumpus World."""
    def __init__(self, arr):
        self.grid = []
        for i in range(4):
            tmp = []
            for j in range(4):
                curr_tile = Tile(i, j, arr[i][j])
                tmp.append(curr_tile)
            self.grid.append(tmp)
        self.grid[3][0].visit()
        self.bot_x = 0
        self.bot_y = 3
        self.arrow = True
        self.gold = False

    def __str__(self):
        result = ""
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.bot_x == j and self.bot_y == i:
                    result += "r"
                else:
                    result += str(self.grid[i][j])
            result += "\n"
        return result[:-1]
    
    def query(self):
        if self.grid[self.bot_y][self.bot_x].is_visited():
            print("Already visited.")
            return None
        else:
            self.grid[self.bot_y][self.bot_x].visit()
            info = [False, False, False, False]
            if self.bot_x == 0: # don't look left
                # look right
                info = self.pairwise_or(info, self.look_right())
                if self.bot_y == 0: # don't look up
                    # look down
                    info = self.pairwise_or(info, self.look_down())
                elif self.bot_y == 3: # don't look down
                    info = self.pairwise_or(info, self.look_up())
                else: # look all directions
                    info = self.pairwise_or(info, self.look_up())
                    info = self.pairwise_or(info, self.look_down())
            elif self.bot_x == 3: # don't look right
                # look left
                info = self.pairwise_or(info, self.look_left())
                if self.bot_y == 0: # don't look up
                    # look down
                    info = self.pairwise_or(info, self.look_down())
                elif self.bot_y == 3: # don't look down
                    info = self.pairwise_or(info, self.look_up())
                else: # look all directions
                    info = self.pairwise_or(info, self.look_up())
                    info = self.pairwise_or(info, self.look_down())
            else: # look left + right
                info = self.pairwise_or(info, self.look_left())
                info = self.pairwise_or(info, self.look_right())
                if self.bot_y == 0: # don't look up
                    # look down
                    info = self.pairwise_or(info, self.look_down())
                elif self.bot_y == 3: # don't look down
                    info = self.pairwise_or(info, self.look_up())
                else: # look all directions
                    info = self.pairwise_or(info, self.look_up())
                    info = self.pairwise_or(info, self.look_down())
            result = 0
            if(info[0]):
                result += 1
            if(info[1]):
                result += 2
            if(info[2]):
                result += 4
            if(self.grid[self.bot_y][self.bot_x].content == "g"):
                result += 8
            return result

    def pairwise_or(self, arr1, arr2):
        result = []
        for arr1_item, arr2_item in zip(arr1, arr2):
            result.append(arr1_item or arr2_item)
        return result

    def look_left(self):
        return self.assess_contents(self.grid[self.bot_y][self.bot_x-1].content)
    def look_right(self):
        return self.assess_contents(self.grid[self.bot_y][self.bot_x+1].content)
    def look_up(self):
        return self.assess_contents(self.grid[self.bot_y-1][self.bot_x].content)
    def look_down(self):
        return self.assess_contents(self.grid[self.bot_y+1][self.bot_x].content)

    def assess_contents(self, contents):
        if contents == "g":
            return [False, False, True, False]
        elif contents == "w":
            return [False, True, False, False]
        elif contents == "h":
            return [True, False, False, False]
        else:
            return [False, False, False, False]

    def move(self, direction):
        if(direction == "n"):
            if(self.bot_y == 0):
                raise Exception("Walked out of map. (Too far north)")
            else:
                self.bot_y -= 1
        if(direction == "s"):
            if(self.bot_y == 3):
                raise Exception("Walked out of map. (Too far south)")
            else:
                self.bot_y += 1
        if(direction == "e"):
            if(self.bot_x == 3):
                print("Error. Cannot move east.")
                raise Exception("Walked out of map. (Too far east)")
            else:
                self.bot_x += 1
        if(direction == "w"):
            if(self.bot_x == 0):
                raise Exception("Walked out of map. (Too far west)")
            else:
                self.bot_x -= 1
        if(self.grid[self.bot_y][self.bot_x].content in ["h", "w"]):
            cause = self.grid[self.bot_y][self.bot_x].content
            if(cause == "h"):
                raise Exception("You fell into a hole.")
            if(cause == "w"):
                raise Exception("You were killed by the Wumpus.")
        if(self.grid[self.bot_y][self.bot_x].content == "g"):
            self.gold = True
    
    def kill_wumpus(self, direction):
        if(not self.arrow):
            raise Exception("You've already used your arrow.")
        self.arrow = False
        if(direction == "n"):
            if(self.bot_y != 0):
                if(self.grid[self.bot_y-1][self.bot_x].content == "w"):
                    self.grid[self.bot_y-1][self.bot_x].content = "e"
        if(direction == "e"):
            if(self.bot_x != 3):
                if(self.grid[self.bot_y][self.bot_x+1].content == "w"):
                    self.grid[self.bot_y][self.bot_x+1].content = "e"
        if(direction == "s"):
            if(self.bot_y != 3):
                if(self.grid[self.bot_y+1][self.bot_x].content == "w"):
                    self.grid[self.bot_y+1][self.bot_x].content = "e"
        if(direction == "w"):
            if(self.bot_x != 0):
                if(self.grid[self.bot_y][self.bot_x-1].content == "w"):
                    self.grid[self.bot_y][self.bot_x-1].content = "e"
        
def main():
    # Better command line argument parsing
    parser = argparse.ArgumentParser(description='Test a user-developed application against Wumpus World puzzles.')
    parser.add_argument('application', type=str, help='The application to test. This can be an executable or a python script.')
    parser.add_argument('difficulty', type=str, help='The difficulty of the tests to run against. This can be "easy", "medium", "hard", or "all"', choices=['easy', 'medium', 'hard', 'all'])
    parser.add_argument('--enable_hardest', help='Enable the hardest difficulty puzzle.', action='store_true')
    args = parser.parse_args()

    if args.difficulty in ['easy', 'medium', 'hard']:
        runTests(args.application, args.difficulty, args.enable_hardest)
    else:
        runTests(args.application, 'easy')
        runTests(args.application, 'medium')
        runTests(args.application, 'hard', args.enable_hardest)

def test(program, world):
    try:
        my_process = subprocess.Popen(program, bufsize=1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        valid_inputs = [
            "n", "e", "s", "w",
            "kill n", "kill e", "kill s", "kill w",
            "input:"
        ]
        while(my_process.returncode is None):
            line = my_process.stdout.readline().decode('utf-8').rstrip()
            if line in [None, ""] or line.isspace():
                break
            elif line in valid_inputs:
                if "kill" in line: 
                    world.kill_wumpus(line[-1:])
                elif "input" in line:
                    value = world.query()

                    if value is None:
                        return False
                    else:
                        my_process.stdin.write(str.encode(str(value) + "\n"))
                        my_process.stdin.flush()
                else:
                    try:
                        world.move(line)
                    except Exception as e:
                        print("Test failed. ",end="")
                        print(e)
                        return False
                    
            else:
                print("Invalid input: " + line)
                return False
                
    except Exception as e:
        print(e)
        print("Quitting test.")
        return False
    if(world.bot_x == 0 and world.bot_y == 3):
        if(world.gold):
            print("Passed!")
            return True
        else:
            print("Test failed. Did not retrieve gold.")
            return False
    else:
        print("Test failed. Did not return to start.")
        
        return False


def legend():
    """Print a legend for the puzzle output."""
    print("Legend:")
    print("e - empty space")
    print("h - hole")
    print("w - wumpus")
    print("g - gold")
    print("r - robot")
    print()

def runTests(program, difficulty, enable_hardest=False):
    """Run the user-provided program against a test-suite of puzzles.

    There are 3 puzzles at each difficulty level, as well as an optional
    puzzle that is significantly harder to solve than the others.

    Arguments:
        program (str): The program to run and interact with.
        difficulty (str): The difficulty level of tests to run.
        enable_hardest (bool): Whether or not to test against the most difficult puzzle.
    """
    failures = 0
    if difficulty == "easy":
        print("Running easy tests.\n")
        legend()
        print("custom world:")
        world0 = World([
            ["g", "p", "e", "e"],
            ["w", "e", "e", "e"],
            ["e", "e", "e", "e"],
            ["e", "e", "e", "e"]
        ])
        test(program, world0)
        print("Easy world 1:")
        world1 = World([
            ["e", "e", "e", "g"],
            ["e", "e", "e", "e"],
            ["e", "e", "e", "e"],
            ["e", "e", "e", "w"]
        ])
        print(str(world1))
        if not test(program, world1):
            failures += 1
        print()
        print("Easy world 2:")
        world2 = World([
            ["e", "e", "e", "h"],
            ["e", "g", "e", "e"],
            ["e", "e", "e", "w"],
            ["e", "e", "e", "e"]
        ])
        print(str(world2))
        if not test(program, world2):
            failures += 1
        print()
        print("Easy world 3:")
        world3 = World([
            ["h", "h", "e", "e"],
            ["e", "e", "e", "w"],
            ["e", "e", "g", "e"],
            ["e", "e", "e", "e"]
        ])
        print(str(world3))
        if not test(program, world3):
            failures += 1
        print()
    elif difficulty == "medium":
        print("Running medium tests.\n")
        legend()
        world1 = World([
            ["h", "h", "g", "h"],
            ["h", "e", "e", "e"],
            ["e", "e", "e", "e"],
            ["e", "e", "e", "w"]
        ])
        print('Medium world 1:')
        print(str(world1))
        if not test(program, world1):
            failures += 1
        print()
        print("Medium world 2:")
        world2 = World([
            ["e", "e", "h", "w"],
            ["e", "e", "e", "g"],
            ["e", "e", "e", "e"],
            ["e", "e", "h", "h"]
        ])
        print(str(world2))
        if not test(program, world2):
            failures += 1
        print()
        print("Medium world 3:")
        world3 = World([
            ["w", "e", "g", "e"],
            ["e", "h", "e", "e"],
            ["e", "e", "e", "e"],
            ["e", "e", "e", "h"]
        ])
        print(str(world3))
        if not test(program, world3):
            failures += 1
    elif difficulty == "hard":
        print("Running hard tests.\n")
        legend()
        world1 = World([
            ["h", "h", "g", "e"],
            ["h", "h", "e", "e"],
            ["e", "h", "e", "e"],
            ["e", "e", "w", "e"]
        ])
        print('Hard world 1:')
        print(str(world1))
        if not test(program, world1):
            failures += 1
        print()
        print("Hard world 2:")
        world2 = World([
            ["e", "h", "e", "h"],
            ["e", "e", "g", "e"],
            ["e", "e", "e", "h"],
            ["e", "e", "e", "e"]
        ])
        print(str(world2))
        if not test(program, world2):
            failures += 1
        print()
        print("Hard world 3:")
        world3 = World([
            ["e", "e", "w", "g"],
            ["e", "e", "h", "h"],
            ["e", "e", "e", "h"],
            ["e", "e", "e", "h"]
        ])
        print(str(world3))
        if not test(program, world3):
            failures += 1
    else:
        pass
    if enable_hardest:
        print()
        print("Hardest world:")
        evil = World([
            ["e", "e", "h", "g"],
            ["e", "e", "h", "w"],
            ["e", "e", "e", "e"],
            ["e", "e", "h", "h"]
        ])
        print(str(evil))
        if(not test(program, evil)):
            failures += 1

    print(f'All tests completed with {failures} failures.')
    print("====================================")


if __name__ == "__main__":
    main()