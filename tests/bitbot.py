#!/usr/bin/env python

from wumpus import Robot

class BitBot(Robot):

    def forward(self):
        if self.dx == 1 and self.dy == 0:
            print("e")
        elif self.dx == -1 and self.dy == 0:
            print("w")
        elif self.dx == 0 and self.dy == 1:
            print("n")
        elif self.dx == 0 and self.dy == -1:
            print("s")
    
    def receive_scent(self):
        if self.x == 0 and self.y == 0:
            return 0
        print("input:")
        return int(input())

    def shoot(self):
        if self.dx == 1 and self.dy == 0:
            print("kill e")
        elif self.dx == -1 and self.dy == 0:
            print("kill w")
        elif self.dx == 0 and self.dy == 1:
            print("kill n")
        elif self.dx == 0 and self.dy == -1:
            print("kill s")

    def rot_cw(self):
        pass

    def rot_ccw(self):
        pass


if __name__ == "__main__":
    bot = BitBot(log_actions=True)
    bot.start()