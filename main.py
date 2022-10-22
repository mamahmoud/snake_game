import math
from operator import truediv
import random
import sys
import pygame
import tkinter

HEIGHT = 600
WIDTH = 600
UNIT_MOVEMENT = 20
XY_INC = list(range(UNIT_MOVEMENT, WIDTH - UNIT_MOVEMENT + 1, UNIT_MOVEMENT))


class Cube:
    def __init__(
        self,
        screen: pygame.Surface,
        x_axis: int,
        y_axis: int,
        x_dir: int = 1,
        y_dir: int = 0,
        color: tuple = (255, 0, 0),
        is_head: bool = False,
    ):
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.screen = screen
        self.y_dir = y_dir
        self.x_dir = x_dir
        self.color = color
        self.is_head = is_head

    def draw(self):
        if not self.is_head:
            pygame.draw.rect(
                self.screen,
                self.color,
                pygame.Rect(self.x_axis, self.y_axis, UNIT_MOVEMENT, UNIT_MOVEMENT),
            )
        else:
            pygame.draw.rect(
                self.screen,
                self.color,
                pygame.Rect(self.x_axis, self.y_axis, UNIT_MOVEMENT, UNIT_MOVEMENT),
            )
            pygame.draw.circle(
                self.screen,
                (255, 0, 0),
                (self.x_axis + UNIT_MOVEMENT // 2, self.y_axis + UNIT_MOVEMENT // 4),
                UNIT_MOVEMENT // 10,
            )
            pygame.draw.circle(
                self.screen,
                (255, 0, 0),
                (
                    self.x_axis + UNIT_MOVEMENT // 2,
                    self.y_axis + (3 * UNIT_MOVEMENT) // 4,
                ),
                UNIT_MOVEMENT // 10,
            )

    def move(self, turns: dict):
        for pos, dirs in turns.items():
            if dirs[2] != 0 and self.x_axis == pos[0] and self.y_axis == pos[1]:
                self.x_dir = dirs[0]
                self.y_dir = dirs[1]
                dirs[2] -= 1
                break

        self.x_axis += self.x_dir * UNIT_MOVEMENT
        self.y_axis += self.y_dir * UNIT_MOVEMENT


class Snake:
    body = []
    turns = {}

    def __init__(
        self,
        screen: pygame.Surface,
        x_axis: int,
        y_axis: int,
        x_dir: int = 1,
        y_dir: int = 0,
    ):
        self.screen = screen
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.x_dir = x_dir
        self.y_dir = y_dir
        self.head = Cube(
            self.screen, self.x_axis, self.y_axis, x_dir, y_dir, (255, 255, 255), True
        )
        self.body.append(self.head)

    def draw(self):
        for part in self.body:
            part.draw()

    def move(self, x_dir: int, y_dir: int):
        if not (self.body[0].x_dir == x_dir) and not (self.body[0].y_dir == y_dir):
            self.turns[(self.body[0].x_axis, self.body[0].y_axis)] = [
                x_dir,
                y_dir,
                len(self.body),
            ]
        for part in self.body:
            part.move(self.turns)

    def has_eaten(self, c1: Cube):
        print(c1.x_axis, c1.y_axis)
        if self.body[0].x_axis == c1.x_axis and self.body[0].y_axis == c1.y_axis:
            c1.y_axis = random.choice(XY_INC)
            c1.x_axis = random.choice(XY_INC)

            new_c = Cube(
                self.screen,
                self.body[0].x_axis + (UNIT_MOVEMENT * self.body[0].x_dir),
                self.body[0].y_axis + (UNIT_MOVEMENT * self.body[0].y_dir),
                self.body[0].x_dir,
                self.body[0].y_dir,
                (255, 255, 255),
                True,
            )
            self.body[0].is_head = False
            self.body.insert(0, new_c)

    def is_dead(self):
        if (
            (self.body[0].x_axis < 0)
            or (self.body[0].x_axis > WIDTH - UNIT_MOVEMENT)
            or (self.body[0].y_axis < 0)
            or (self.body[0].y_axis > WIDTH - UNIT_MOVEMENT)
        ):
            return True
        for part in self.body[1:]:
            if (
                part.x_axis == self.body[0].x_axis
                and part.y_axis == self.body[0].y_axis
            ):
                return True

    def cleanup_turns(self):
        pass


def main():
    pygame.init()
    game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake game")
    game_clock = pygame.time.Clock()
    snake_1 = Snake(game_screen, WIDTH // 2, WIDTH // 2)
    cube_1 = Cube(game_screen, random.choice(XY_INC), random.choice(XY_INC), 0, 0)
    cube_2 = Cube(game_screen, 580, 600, 0, 0)
    y_dir = 0
    x_dir = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                y_dir = -1
                x_dir = 0
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                y_dir = 1
                x_dir = 0
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                y_dir = 0
                x_dir = 1
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                y_dir = 0
                x_dir = -1
        snake_1.move(x_dir, y_dir)
        if snake_1.is_dead():
            return
        snake_1.has_eaten(cube_1)
        game_screen.fill((0, 0, 0))
        snake_1.draw()
        cube_1.draw()
        pygame.display.update()
        game_clock.tick(5)


if __name__ == "__main__":
    main()
