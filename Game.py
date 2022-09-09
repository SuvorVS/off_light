import copy
from enum import Enum


class GameState(Enum):
    PLAYING = 0  # игра не закончена
    WIN = 1      # игра закончена победой



class Cell:
    def __init__(self, light: bool = True):
        self._light = light      # есть ли свет

    @property
    def light(self) -> bool:
        return self.light


class Game:
    def __init__(self, row_count: int, col_count: int):
        self._row_count = row_count
        self._col_count = col_count
        self.new_game()

    def set_size(self, r, c):
        self._row_count = r
        self._col_count = c

    def new_game(self) -> None:
        self._field = [
            copy.deepcopy([Cell() for c in range(self.col_count)])
            for r in range(self.row_count)
        ]


        for r in range(self.row_count):
            for c in range(self.col_count):
                self._field[r][c] = True



        self._state = GameState.PLAYING


    def sets(self, state):
        self._state=state


    @property
    def row_count(self) -> int:
        return self._row_count

    @property
    def col_count(self) -> int:
        return self._col_count


    @property
    def state(self) -> GameState:
        return self._state

    def __getitem__(self, indices: tuple) -> Cell:
        return self._field[indices[0]][indices[1]]

    def _cells(self):
        for r in range(self.row_count):
            for c in range(self.col_count):
                yield self[r, c]

    def _update_playing_state(self):
        if not any(any(row) for row in self._field):
            self._state = GameState.WIN
        else:
            self._state = GameState.PLAYING

    def neigthbour_indexes(self, r, c):
        res = [(r, c)]
        if r >= 1:
            res.append((r - 1, c))
        if r < len(self._field) - 1:
            res.append((r + 1, c))
        if c >= 1:
            res.append((r, c - 1))
        if c < len(self._field[r]) - 1:
            res.append((r, c + 1))
        return res

    def left_mouse_click(self, row: int, col: int) -> None:
        if self.state != GameState.PLAYING:
            return
        for i, j in self.neigthbour_indexes(row, col):
            self._field[i][j] = not self._field[i][j]
        self._update_playing_state()




