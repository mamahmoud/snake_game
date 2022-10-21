import math
import random
import sys
import pygame
import tkinter

HEIGHT = 600
WIDTH = 600
UNIT_MOVEMENT = 10


class Cube:
    def __init__(self, screen, x_axis, y_axis, x_dir=1, y_dir=0):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.screen = screen
        self.y_dir = y_dir
        self.x_dir = x_dir

    def draw(self):
        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            pygame.Rect(self.x_axis, self.y_axis, UNIT_MOVEMENT, UNIT_MOVEMENT),
        )

    def move(self):
        self.x_axis += self.x_dir * UNIT_MOVEMENT
        self.y_axis += self.y_dir * UNIT_MOVEMENT


class Snake:
    def __init__(self, screen, img, x_axis, y_axis):
        pass

    def draw(self):
        pass

    def move(self):
        pass


def main():
    pygame.init()
    game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake game")
    game_clock = pygame.time.Clock()
    c1 = Cube(game_screen, 0, 0)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                c1.y_dir = -1
                c1.x_dir = 0
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                c1.y_dir = 1
                c1.x_dir = 0
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                c1.y_dir = 0
                c1.x_dir = 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                c1.y_dir = 0
                c1.x_dir = -1

        game_screen.fill((0, 0, 0))
        c1.move()
        c1.draw()
        pygame.display.update()
        game_clock.tick(5)


if __name__ == "__main__":
    main()
