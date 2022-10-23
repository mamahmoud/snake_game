import math
from operator import truediv
import random
import sys
import pygame
import tkinter

HEIGHT = 600
WIDTH = 600
UNIT_MOVEMENT = 20
XY_INC = set(range(UNIT_MOVEMENT, WIDTH - UNIT_MOVEMENT + 1, UNIT_MOVEMENT))
BASE_FPS = 5


class Cube:
    """
    class cube represents the food for the snake and the snake parts.
    """

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
        """
        Init func for the class
        """
        self.x_axis = x_axis
        self.y_axis = y_axis
        self.screen = screen
        self.y_dir = y_dir
        self.x_dir = x_dir
        self.color = color
        self.is_head = is_head

    def draw(self):
        """
        Draws the cube, and special drawing for snake head
        """
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
        """
        move and turns the cube based on the dictionary of turns from snake
        """
        for pos, dirs in turns.items():
            if dirs[2] != 0 and self.x_axis == pos[0] and self.y_axis == pos[1]:
                self.x_dir = dirs[0]
                self.y_dir = dirs[1]
                dirs[2] -= 1
                break

        self.x_axis += self.x_dir * UNIT_MOVEMENT
        self.y_axis += self.y_dir * UNIT_MOVEMENT


class Snake:

    """
    class snake consists of cube lists, and turns.
    """

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
        """
        Init func for the class
        """
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
        """
        Draws the snake, by calling the cube method for each body part, and special drawing for snake head
        """
        for part in self.body:
            part.draw()

    def move(self, x_dir: int, y_dir: int):
        """
        move the snake by calling the move from cube, also adds the new turns to the dictionary
        """
        if not (self.body[0].x_dir == x_dir) and not (self.body[0].y_dir == y_dir):
            self.turns[(self.body[0].x_axis, self.body[0].y_axis)] = [
                x_dir,
                y_dir,
                len(self.body),
            ]
        for part in self.body:
            part.move(self.turns)

    def has_eaten(self, c1: Cube):
        """
        Check if the snake has eaten the food
        """
        if self.body[0].x_axis == c1.x_axis and self.body[0].y_axis == c1.y_axis:
            new_c = Cube(
                self.screen,
                self.body[-1].x_axis + (-1 * UNIT_MOVEMENT * self.body[-1].x_dir),
                self.body[-1].y_axis + (-1 * UNIT_MOVEMENT * self.body[-1].y_dir),
                self.body[-1].x_dir,
                self.body[-1].y_dir,
                (255, 255, 255),
            )
            for pos, dirs in self.turns.items():
                if dirs[2] > 0:
                    dirs[2] += 1
            self.body.append(new_c)
            all_x_axis = set(part.x_axis for part in self.body)
            all_y_axis = set(part.y_axis for part in self.body)
            diff_x_axis = all_x_axis.symmetric_difference(XY_INC)
            diff_y_axis = all_y_axis.symmetric_difference(XY_INC)
            c1.y_axis = random.choice(diff_y_axis)
            c1.x_axis = random.choice(diff_x_axis)

    def is_dead(self):
        """
        Checks if snake is dead by hitting a wall or itself
        """
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


def main():
    """
    main function
    """
    pygame.init()
    game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake game")
    game_clock = pygame.time.Clock()
    snake_1 = Snake(game_screen, WIDTH // 2, WIDTH // 2)
    cube_1 = Cube(game_screen, random.choice(XY_INC), random.choice(XY_INC), 0, 0)
    y_dir = 0
    x_dir = 1
    while True:
        if snake_1.is_dead():
            return
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
        snake_1.has_eaten(cube_1)
        game_screen.fill((0, 0, 0))
        snake_1.draw()
        cube_1.draw()
        pygame.display.update()
        game_clock.tick(len(Snake.body) // 10 + BASE_FPS)


if __name__ == "__main__":
    main()
