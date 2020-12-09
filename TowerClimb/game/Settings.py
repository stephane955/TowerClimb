import pygame
vec = pygame.math.Vector2

#Colors

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

Platforms = [[vec(300, 343), "p1", True], [vec(42, 334), "p2", True], [vec(432, 23), "p3", True],
             [vec(432, 223), "p4", True], [vec(142, 23), "p5", True], [vec(142, 23), "p6", True],
             [vec(142, -123), "p7", True],  [vec(12, -323), "p8", True], [vec(652, -523), "p9", True],
             [vec(233, -421), "p10", True], [vec(142, -883), "p11", True], [vec(343, -1323), "p12", True],
             [vec(452, -223), "p13", True], [vec(42, -823), "p14", True], [vec(42, -1600), "p&5", True]]