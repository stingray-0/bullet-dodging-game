# from dataclasses import dataclass
# from enum import Enum


# class BulletDirection(Enum):
#     DOWN = "down"
#     UP = "up"
#     LEFT = "left"
#     RIGHT = "right"
#     UP_DOWN = "up_down"
#     LEFT_RIGHT = "left_right"
#     ALL = "udlr"

# class BulletSpread(Enum):
#     SCATTERED = 1
#     SPACED = 2
#     LEFT_HALF = 3
#     RIGHT_HALF = 4

# @dataclass
# class BulletPattern:
#     amount: int 
#     spreadness : BulletSpread
#     direction: BulletDirection
#     speed: float = 1.0
#     delay: int = 0

patterns = [[1,"down"], [1,"up"], [3,"left"],[1,"right"],[2,"left"],[3,"down"],[2,"down"],
            [1,"right"], [3,"up"], [1,"left"],[2,"right"],[4,"left"],[4,"up"],[1,"right"],
            [5,"up_down"],[5,"down_up"],[4,"right"],[5,"right_left"],[3,"down"],
            [1,"up_down"],[1,"up_down"],[5,"left_right"],[1,"down_up"],[1,"right_left"],
            [5,"udlr"],[5,"lrud"],[1,"lrud"],[5,"left_right"],[3,"up"],[4,"right"],[5,"up_down"],
            [1,"udlr"],[1,"lrud"],[1,"udlr"],[5,"lrud"],[5,"right_left"],[1,"left"],[1,"udlr"],
            [1,"right_left"],[1,"up_down"],[1,"udlr"],[1,"lrud"],[1,"lrud"],[1,"udlr"],[1,"udlr"],]
