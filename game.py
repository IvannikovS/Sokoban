import os.path
from enum import Enum


class CellType(Enum):
    EMPTY = 0
    WALL = 1
    BOX = 2
    GROUND = 3
    TARGET = 4
    MAN = 5
    BOX_ON_TARGET = 6


class Game:

    def __init__(self):
        self.field = []
        self.x = 0
        self.y = 0
        self.boxes = []
        self.targets = set()
        self.n_steps = 0
        self.level_complete = False

    @staticmethod
    def load_level(f_name, game_inst):
        if os.path.isfile(f_name):
            f = open(f_name, 'rt')
            data = f.readlines()
            game_inst.field.clear()
            game_inst.boxes.clear()
            game_inst.targets.clear()
            game_inst.n_steps = 0
            for k in range(len(data)):
                b = []
                for k2 in range(len(data[k])):
                    cell = ord(data[k][k2]) - 48
                    if cell < 0:
                        continue
                    # print(cell, end='')
                    if cell == CellType.MAN.value:
                        game_inst.x = k2
                        game_inst.y = k
                        # print(f'man{game_inst.x} {game_inst.y}')
                    if cell == CellType.BOX.value or cell == CellType.BOX_ON_TARGET.value:
                        game_inst.boxes.append((k2, k))
                    if cell == CellType.TARGET.value or cell == CellType.BOX_ON_TARGET.value:
                        game_inst.targets.add((k2, k))
                    if cell == CellType.WALL.value or cell == CellType.EMPTY.value:
                        b.append(cell)
                    else:
                        b.append(CellType.GROUND.value)
                # print()
                game_inst.field.append(b)
        else:
            print(f'{f_name} not found')

    def command_left(self):
        if self.x > 0:
            cell_left = (self.x - 1, self.y)
            if self.field[self.y][self.x - 1] == CellType.WALL.value:
                return
            if cell_left not in self.boxes: # не стена и нет коробки
                self.x -= 1
                self.n_steps += 1
            else:
                if self.x < 2 or (self.x - 2, self.y) in self.boxes:
                    return
                if self.field[self.y][self.x - 2] == CellType.GROUND.value:
                    self.boxes.remove(cell_left)
                    self.boxes.append((self.x - 2, self.y))
                    self.x -= 1
                    self.n_steps += 1

    def command_right(self):
        if self.x < len(self.field[0]) - 1:
            cell_right = (self.x + 1, self.y)
            if self.field[self.y][self.x + 1] == CellType.WALL.value:
                return
            if cell_right not in self.boxes:  # не стена и нет коробки
                self.x += 1
                self.n_steps += 1
            else:
                if self.x > len(self.field[0]) - 2 or (self.x + 2, self.y) in self.boxes:
                    return
                if self.field[self.y][self.x + 2] == CellType.GROUND.value:
                    self.boxes.remove(cell_right)
                    self.boxes.append((self.x + 2, self.y))
                    self.x += 1
                    self.n_steps += 1

    def command_up(self):
        if self.y > 0:
            cell_up = (self.x, self.y - 1)
            if self.field[self.y - 1][self.x] == CellType.WALL.value:
                return
            if cell_up not in self.boxes:  # не стена и нет коробки
                self.y -= 1
                self.n_steps += 1
            else:
                if self.y < 2 or (self.x, self.y - 2) in self.boxes:
                    return
                if self.field[self.y - 2][self.x] == CellType.GROUND.value:
                    self.boxes.remove(cell_up)
                    self.boxes.append((self.x, self.y - 2))
                    self.y -= 1
                    self.n_steps += 1

    def command_down(self):
        if self.y < len(self.field) - 1:
            cell_down = (self.x, self.y + 1)
            if self.field[self.y + 1][self.x] == CellType.WALL.value:
                return
            if cell_down not in self.boxes:  # не стена и нет коробки
                self.y += 1
                self.n_steps += 1
            else:
                if self.y > len(self.field) - 2 or (self.x, self.y + 2) in self.boxes:
                    return
                if self.field[self.y + 2][self.x] == CellType.GROUND.value:
                    self.boxes.remove(cell_down)
                    self.boxes.append((self.x, self.y + 2))
                    self.y += 1
                    self.n_steps += 1

    def check_level_victory(self):
        for b in self.boxes:
            if b not in self.targets:
                return False
        return True
