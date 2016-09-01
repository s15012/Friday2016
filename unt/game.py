import random
from collections import deque

import pyglet

from unt.main import Main


class Board(object):
    """
    テトリスのボード部分の実装
    ボードは縦20横10マスの予定
    """

    def __init__(self, x, y, queue, grid_size, background):
        super().__init__()
        self._x = x
        self._y = y
        self._grid_size = grid_size
        self.fixed_block = [[0] * 10] * 20
        self._queue = queue  # type: NextTetrominoQueue
        self._falling_tetromino = None  # type: Tetromino
        self._background = background  # type: pyglet.image.AbstractImage

    def spawn_tetromino(self):
        self._falling_tetromino = self._queue.next()  # type: Tetromino
        self._falling_tetromino.set_position(4, 20)

    def draw(self):
        # ボードの背景
        self._background.blit(self._x - 6, self._y - 6)

        # 落下中のテトロミノ描画
        for coord in self._falling_tetromino.board_coordinates:
            if coord[0] < 10 and coord[1] < 20:
                self._falling_tetromino.get_block().blit(
                    coord[0] * self._grid_size + self._x,
                    coord[1] * self._grid_size + self._y)

    def send_action_falling_tetromino(self, action):
        if action == Main.MOVE_DOWN:
            self._falling_tetromino.move_down()
        elif action == Main.MOVE_RIGHT:
            self._falling_tetromino.move_right()
        elif action == Main.MOVE_LEFT:
            self._falling_tetromino.move_left()


class TetrominoType(object):
    """
    テトロミノの種類を定義
    """
    TYPES = tuple()

    def __init__(self, block_image, local_coordinates):
        self.block = block_image  # type: pyglet.image.AbstractImage
        self.coordinates = local_coordinates  # type: tuple

    @staticmethod
    def block_init(block_image, block_size):
        dummy = block_image.get_region(block_size * 0, 0, block_size, block_size)
        cyan = block_image.get_region(block_size * 1, 0, block_size, block_size)
        yellow = block_image.get_region(block_size * 2, 0, block_size, block_size)
        green = block_image.get_region(block_size * 3, 0, block_size, block_size)
        red = block_image.get_region(block_size * 4, 0, block_size, block_size)
        blue = block_image.get_region(block_size * 5, 0, block_size, block_size)
        orange = block_image.get_region(block_size * 6, 0, block_size, block_size)
        purple = block_image.get_region(block_size * 7, 0, block_size, block_size)

        TetrominoType.TYPES = (
            # type I
            TetrominoType(cyan,
                          (
                              (  # 初期の向き
                                  (0, 0), (1, 0), (2, 0), (3, 0)
                              ),
                              (  # 右回り1段階
                                  (1, 0), (1, 1), (1, 2), (1, 3)
                              ),
                              (  # 右回り2段階
                                  (0, 0), (1, 0), (2, 0), (3, 0)
                              ),
                              (  # 右回り3段階
                                  (1, 0), (1, 1), (1, 2), (1, 3)
                              ),
                          )),
            # type o
            TetrominoType(yellow,
                          (
                              (  # 初期の向き
                                  (0, 0), (1, 0), (0, 1), (1, 1)
                              ),
                              (  # 右回り1段階
                                  (0, 0), (1, 0), (0, 1), (1, 1)
                              ),
                              (  # 右回り2段階
                                  (0, 0), (1, 0), (0, 1), (1, 1)
                              ),
                              (  # 右回り3段階
                                  (0, 0), (1, 0), (0, 1), (1, 1)
                              ),
                          )),
            # type s
            TetrominoType(green,
                          (
                              (  # 初期の向き
                                  (0, 0), (1, 0), (1, 1), (2, 1)
                              ),
                              (  # 右回り1段階
                                  (0, 2), (0, 1), (1, 1), (1, 0)
                              ),
                              (  # 右回り2段階
                                  (0, 0), (1, 0), (1, 1), (2, 1)
                              ),
                              (  # 右回り3段階
                                  (0, 2), (0, 1), (1, 1), (1, 0)
                              ),
                          )),
            # type z
            TetrominoType(red,
                          (
                              (  # 初期の向き
                                  (0, 1), (1, 1), (1, 0), (2, 0)
                              ),
                              (  # 右回り1段階
                                  (1, 2), (1, 1), (0, 1), (0, 0)
                              ),
                              (  # 右回り2段階
                                  (0, 1), (1, 1), (1, 0), (2, 0)
                              ),
                              (  # 右回り3段階
                                  (1, 2), (1, 1), (0, 1), (0, 0)
                              ),
                          )),
            # type j
            TetrominoType(blue,
                          (
                              (  # 初期の向き
                                  (0, 1), (0, 0), (1, 0), (2, 0)
                              ),
                              (  # 右回り1段階
                                  (0, 0), (0, 1), (0, 2), (1, 2)
                              ),
                              (  # 右回り2段階
                                  (0, 1), (1, 1), (2, 1), (2, 0)
                              ),
                              (  # 右回り3段階
                                  (0, 0), (1, 0), (1, 1), (1, 2)
                              ),
                          )),
            # type L
            TetrominoType(orange,
                          (
                              (  # 初期の向き
                                  (0, 0), (1, 0), (2, 0), (2, 1)
                              ),
                              (  # 右回り1段階
                                  (0, 2), (0, 1), (0, 0), (1, 0)
                              ),
                              (  # 右回り2段階
                                  (0, 0), (0, 1), (1, 1), (2, 1)
                              ),
                              (  # 右回り3段階
                                  (0, 2), (1, 2), (1, 1), (1, 0)
                              ),
                          )),
            # type t
            TetrominoType(purple,
                          (
                              (  # 初期の向き
                                  (0, 0), (1, 0), (2, 0), (1, 1)
                              ),
                              (  # 右回り1段階
                                  (0, 2), (0, 1), (0, 0), (1, 1)
                              ),
                              (  # 右回り2段階
                                  (0, 1), (1, 1), (2, 1), (1, 0)
                              ),
                              (  # 右回り3段階
                                  (1, 0), (1, 1), (1, 2), (0, 1)
                              ),
                          )),
        )


class Tetromino(object):
    """テトロミノ自身を表現するクラス"""

    def __init__(self, tetromino_type):
        self._type = tetromino_type  # type: TetrominoType
        self._orientation = 0
        self._x = 0
        self._y = 0
        self.board_coordinates = self.calc_board_coordinates()

    def calc_board_coordinates(self):
        local_coordinates = self._type.coordinates[self._orientation]
        coordinates = []

        for coord in local_coordinates:
            coordinates.append([coord[0] + self._x, coord[1] + self._y])

        return coordinates

    def get_block(self):
        return self._type.block

    def set_position(self, x, y):
        self._x = x
        self._y = y
        self.board_coordinates = self.calc_board_coordinates()

    def move_down(self):
        self._y -= 1
        self.board_coordinates = self.calc_board_coordinates()

    def move_up(self):
        self._y += 1
        self.board_coordinates = self.calc_board_coordinates()

    def move_left(self):
        self._x -= 1
        self.board_coordinates = self.calc_board_coordinates()

    def move_right(self):
        self._x += 1
        self.board_coordinates = self.calc_board_coordinates()

    def rotate_clockwise(self):
        self._orientation = (self._orientation + 1) % 4
        self.board_coordinates = self.calc_board_coordinates()

    def rotate_counter_clockwise(self):
        self._orientation = (self._orientation + 3) % 4
        self.board_coordinates = self.calc_board_coordinates()


class NextTetrominoQueue(object):
    """
    Nextブロックを管理するキュー
    """

    def __init__(self, set_count=2):
        self._set_count = set_count
        self._queue = deque()  # type: deque
        self.generate_tetromino()

    def generate_tetromino(self):
        """
        Tetrominoをset_countセット作ってシャッフルしてキューにぶち込む
        """
        tetromino_type_set = list(TetrominoType.TYPES[:] * self._set_count)
        for a in range(3):
            random.shuffle(tetromino_type_set)

        for tetromino_type in tetromino_type_set:
            self._queue.append(Tetromino(tetromino_type))

    def get(self, index):
        return self._queue[index]  # type: Tetromino

    def next(self):
        if len(self._queue) < 5:
            self.generate_tetromino()

        return self._queue.popleft()  # type: Tetromino
