import pygame
import Colors
from typing import Tuple

WORLD_WIDTH = 10
WORLD_HEIGHT = 10

PLAYER_COLOR = Colors.BLUE
GOAL_COLOR = Colors.YELLOW
BORDER_COLOR = Colors.WHITE


class Map:

    def __init__(self, width: int = WORLD_WIDTH, height: int = WORLD_HEIGHT):
        self.width = width
        self.height = height
        self.player = Cell(["player"])
        self.goal = Cell(["goal"])
        self.map: list[list[Cell]] = [[Cell() for _ in range(width)] for _ in range(height)]
        self.cell_size_x = 800 / self.width
        self.cell_size_y = 600 / self.height
        self.set_cell(0, 0, self.player)
        self.set_cell(width - 1, height - 1, self.goal)

    def render(self, screen) -> None:
        for i in range(self.height):
            for j in range(self.width):
                self.map[i][j].render(screen, j, i, self.cell_size_x, self.cell_size_y)

    def set_cell(self, x: int, y: int, cell: "Cell") -> bool:
        if not self.is_inside(x, y):
            return False

        self.map[y][x] = cell
        return True

    def is_inside(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def move_player(self, x, y) -> bool:
        if not self.is_inside(x, y):
            return False

        self.player.items.remove("player")
        self.player = self.map[y][x]
        self.player.items.append("player")


class Cell:

    def __init__(self, items: list[str] = None):
        self.items = items if items else []

    def render(self, screen, x, y, size_x, size_y) -> Tuple[int, int, int]:
        if len(self.items) == 0:
            pygame.draw.rect(screen, BORDER_COLOR, (x * size_x, y * size_y, size_x, size_y), 3)
        else:
            for item in self.items:
                if item == "player":
                    pygame.draw.rect(screen, PLAYER_COLOR, (x * size_x, y * size_y, size_x, size_y))
                elif item == "goal":
                    pygame.draw.rect(screen, GOAL_COLOR, (x * size_x, y * size_y, size_x, size_y))

    def get_position(self, map) -> Tuple[int, int]:
        for i in range(map.height):
            for j in range(map.width):
                cell = map.map[i][j]
                if cell == self:
                    return (j, i)
        return (-1, -1)
