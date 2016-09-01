"""
Pygletを使ったテトリス。実装部分

"""
import random
import warnings
from collections import deque

import pyglet


class TetrominoType(object):
    TYPES = tuple()

    def __init__(self, block_image, dmblock , local_coords):
        self._block_image = block_image
        self._dmblock = dmblock
        self._local_coords = local_coords

    @staticmethod
    def class_init(block_image, dmblock, block_size):
        """
        block_imageからblock_sizeで8色のブロックを切り出す。
        その後、7種のテトロミノタイプを定義してstaticメンバとして生成
        :param block_image: ブロック画像
        :param block_size: ブロックのサイズ
        :return: None
        """
        dummy = block_image.get_region(block_size * 0, 0, block_size, block_size)
        cyan = block_image.get_region(block_size * 1, 0, block_size, block_size)
        yellow = block_image.get_region(block_size * 2, 0, block_size, block_size)
        green = block_image.get_region(block_size * 3, 0, block_size, block_size)
        red = block_image.get_region(block_size * 4, 0, block_size, block_size)
        blue = block_image.get_region(block_size * 5, 0, block_size, block_size)
        orange = block_image.get_region(block_size * 6, 0, block_size, block_size)
        purple = block_image.get_region(block_size * 7, 0, block_size, block_size)

        dm_dummy = dmblock.get_region(block_size * 0, 0, block_size, block_size)
        dm_cyan = dmblock.get_region(block_size * 1, 0, block_size, block_size)
        dm_yellow = dmblock.get_region(block_size * 2, 0, block_size, block_size)
        dm_green = dmblock.get_region(block_size * 3, 0, block_size, block_size)
        dm_red = dmblock.get_region(block_size * 4, 0, block_size, block_size)
        dm_blue = dmblock.get_region(block_size * 5, 0, block_size, block_size)
        dm_orange = dmblock.get_region(block_size * 6, 0, block_size, block_size)
        dm_purple = dmblock.get_region(block_size * 7, 0, block_size, block_size)

        TetrominoType.TYPES = (
            # type I
            TetrominoType(cyan,dm_cyan,
                          {
                              Tetromino.RIGHT: ((0, 1), (1, 1), (2, 1), (3, 1)),
                              Tetromino.DOWN: ((1, 0), (1, 1), (1, 2), (1, 3)),
                              Tetromino.LEFT: ((0, 1), (1, 1), (2, 1), (3, 1)),
                              Tetromino.UP: ((1, 0), (1, 1), (1, 2), (1, 3)),
                          }
                          ),
            # type O
            TetrominoType(yellow,dm_yellow,
                          {
                              Tetromino.RIGHT: ((1, 0), (1, 1), (2, 0), (2, 1)),
                              Tetromino.DOWN: ((1, 0), (1, 1), (2, 0), (2, 1)),
                              Tetromino.LEFT: ((1, 0), (1, 1), (2, 0), (2, 1)),
                              Tetromino.UP: ((1, 0), (1, 1), (2, 0), (2, 1)),
                          }
                          ),
            # type S
            TetrominoType(green,dm_green,
                          {
                              Tetromino.RIGHT: ((0, 0), (1, 0), (1, 1), (2, 1)),
                              Tetromino.DOWN: ((0, 2), (0, 1), (1, 1), (1, 0)),
                              Tetromino.LEFT: ((0, 0), (1, 0), (1, 1), (2, 1)),
                              Tetromino.UP: ((0, 2), (0, 1), (1, 1), (1, 0)),
                          }
                          ),
            # type Z
            TetrominoType(red,dm_red,
                          {
                              Tetromino.RIGHT: ((0, 1), (1, 1), (1, 0), (2, 0)),
                              Tetromino.DOWN: ((0, 0), (0, 1), (1, 1), (1, 2)),
                              Tetromino.LEFT: ((0, 1), (1, 1), (1, 0), (2, 0)),
                              Tetromino.UP: ((0, 0), (0, 1), (1, 1), (1, 2)),
                          }
                          ),
            # type J
            TetrominoType(blue,dm_blue,
                          {
                              Tetromino.RIGHT: ((0, 2), (0, 1), (1, 1), (2, 1)),
                              Tetromino.DOWN: ((1, 0), (1, 1), (1, 2), (2, 2)),
                              Tetromino.LEFT: ((0, 1), (1, 1), (2, 1), (2, 0)),
                              Tetromino.UP: ((0, 0), (1, 0), (1, 1), (1, 2)),
                          }
                          ),
            # type L
            TetrominoType(orange,dm_orange,
                          {
                              Tetromino.RIGHT: ((0, 1), (1, 1), (2, 1), (2, 2)),
                              Tetromino.DOWN: ((1, 2), (1, 1), (1, 0), (2, 0)),
                              Tetromino.LEFT: ((0, 0), (0, 1), (1, 1), (2, 1)),
                              Tetromino.UP: ((0, 2), (1, 2), (1, 1), (1, 0)),
                          }

                          ),
            # type T
            TetrominoType(purple,dm_purple,
                          {
                              Tetromino.RIGHT: ((0, 1), (1, 1), (2, 1), (1, 2)),
                              Tetromino.DOWN: ((1, 0), (1, 1), (1, 2), (2, 1)),
                              Tetromino.LEFT: ((0, 1), (1, 1), (2, 1), (1, 0)),
                              Tetromino.UP: ((1, 0), (1, 1), (1, 2), (0, 1)),
                          }
                          ),
        )



    @staticmethod
    def random_type():
        warnings.warn("キューを使う方式に変更して下さい", category=DeprecationWarning, stacklevel=2)
        return random.choice(TetrominoType.TYPES)

    def get_local_coords(self, orientation):
        return self._local_coords[orientation]

    def get_block(self):
        return self._block_image


class Tetromino(object):
    RIGHT, DOWN, LEFT, UP = range(4)
    CLOCKWISE_ROTATIONS = {RIGHT: DOWN, DOWN: LEFT, LEFT: UP, UP: RIGHT}

    def __init__(self, tetromino_type=None):
        self._x = 0
        self._y = 0
        if tetromino_type is None:
            self._tetromino_type = TetrominoType.random_type()  # type: TetrominoType
        else:
            self._tetromino_type = tetromino_type
        self._orientation = Tetromino.RIGHT
        self._block_board_coords = self.calc_block_board_coords()

    def calc_block_board_coords(self):
        local_block_coords = self._tetromino_type.get_local_coords(self._orientation)
        grid_coords = []
        for coord in local_block_coords:
            grid_coord = (coord[0] + self._x, coord[1] + self._y)
            grid_coords.append(grid_coord)
        return grid_coords

    def get_block_board_coords(self):
        return self._block_board_coords

    def get_position(self):
        return self._x, self._y

    def set_position(self, x, y):
        self._x = x
        self._y = y
        self._block_board_coords = self.calc_block_board_coords()

    def move_down(self):
        self._y -= 1
        self._block_board_coords = self.calc_block_board_coords()

    def move_up(self):
        self._y += 1
        self._block_board_coords = self.calc_block_board_coords()

    def move_left(self):
        self._x -= 1
        self._block_board_coords = self.calc_block_board_coords()

    def move_right(self):
        self._x += 1
        self._block_board_coords = self.calc_block_board_coords()

    def rotate_clockwise(self):
        self._orientation = Tetromino.CLOCKWISE_ROTATIONS[self._orientation]
        self._block_board_coords = self.calc_block_board_coords()

    def rotate_counterclockwise(self):
        self._orientation = Tetromino.CLOCKWISE_ROTATIONS[self._orientation]
        self._orientation = Tetromino.CLOCKWISE_ROTATIONS[self._orientation]
        self._orientation = Tetromino.CLOCKWISE_ROTATIONS[self._orientation]
        self._block_board_coords = self.calc_block_board_coords()

    def command(self, command):
        if command == InputProcessor.MOVE_DOWN:
            self.move_down()
        elif command == InputProcessor.MOVE_RIGHT:
            self.move_right()
        elif command == InputProcessor.MOVE_LEFT:
            self.move_left()
        elif command == InputProcessor.ROTATE_CLOCKWISE:
            self.rotate_clockwise()

    def undo_command(self, command):
        if command == InputProcessor.MOVE_DOWN:
            self.move_up()
        elif command == InputProcessor.MOVE_RIGHT:
            self.move_left()
        elif command == InputProcessor.MOVE_LEFT:
            self.move_right()
        elif command == InputProcessor.ROTATE_CLOCKWISE:
            self.rotate_counterclockwise()

    def clear_row_and_adjust_down(self, board_grid_row):
        new_block_board_coords = []
        for coord in self._block_board_coords:
            if coord[1] > board_grid_row:
                adjusted_coord = (coord[0], coord[1] - 1)
                new_block_board_coords.append(adjusted_coord)
            if coord[1] < board_grid_row:
                new_block_board_coords.append(coord)
        self._block_board_coords = new_block_board_coords
        return len(self._block_board_coords) > 0

    def draw(self, screen_coords, isDummy=False):
        image = self._tetromino_type.get_block()
        if isDummy:
            image = self._tetromino_type._dmblock
        for coords in screen_coords:
            image.blit(coords[0], coords[1])


class Board(object):
    STARTING_ZONE_HEIGHT = 4

    def __init__(self, x, y, grid_width, grid_height, block_size, queue, holder):
        self._x = x
        self._y = y
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._block_size = block_size
        self._spawn_x = int(grid_width * 1 / 3)
        self._spawn_y = grid_height
        self._queue = queue
        self._falling_tetromino = None  # type: Tetromino
        self.spawn_tetromino()
        self._tetromino_list = []
        self._is_after_move = False
        self.dummy = Tetromino()
        self._holder = holder  # type: Holder

    def spawn_tetromino(self):
        self._falling_tetromino = self._queue.next()
        self._falling_tetromino.set_position(self._spawn_x, self._spawn_y)

    def command_falling_tetromino(self, command):
        if command != InputProcessor.MOVE_DOWN:
            self._is_after_move = True
        if command != InputProcessor.MOVE_UP:
            self._is_after_move = True

        if command == InputProcessor.DROP:
            while True:
                self._falling_tetromino.command(InputProcessor.MOVE_DOWN)
                if not self.is_valid_position():
                    self._falling_tetromino.undo_command(InputProcessor.MOVE_DOWN)
                    # self._tetromino_list.append(self._falling_tetromino)
                    # full_rows = self.find_full_rows()
                    # self.clear_rows(full_rows)
                    # self.spawn_tetromino()
                    # self._holder.release()
                    self._is_after_move = False
                    break
                    # TODO aaaaaaaaaaaaaaaaaaaaaaaa



        if command == InputProcessor.HOLDING:
            tetromino, swapped = self._holder.swap(self._falling_tetromino)
            if swapped:
                if tetromino is None:
                    self.spawn_tetromino()
                else:
                    self._falling_tetromino = tetromino
                    self._falling_tetromino.set_position(self._spawn_x, self._spawn_y)

        self._falling_tetromino.command(command)
        if not self.is_valid_position():
            if command == InputProcessor.ROTATE_CLOCKWISE:
                self._super_rotation()
            else:
                self._falling_tetromino.undo_command(command)

    def _super_rotation(self):
        direction = None
        coords = self._falling_tetromino.get_block_board_coords()
        for coord in coords:
            if coord[0] < 0:
                direction = InputProcessor.MOVE_LEFT
            elif coord[0] >= 20:
                direction = InputProcessor.MOVE_RIGHT
            elif coord[1] < 0:
                direction = InputProcessor.MOVE_DOWN

        if direction is not None:
            self._falling_tetromino.undo_command(direction)
            if not self.is_valid_position():
                self._falling_tetromino.command(direction)
                self._falling_tetromino.undo_command(InputProcessor.ROTATE_CLOCKWISE)
        else:
            self._falling_tetromino.command(InputProcessor.MOVE_LEFT)
            if not self.is_valid_position():
                self._falling_tetromino.command(InputProcessor.MOVE_LEFT)
                if not self.is_valid_position():
                    self._falling_tetromino.undo_command(InputProcessor.MOVE_LEFT)
                    self._falling_tetromino.undo_command(InputProcessor.MOVE_LEFT)
                    self._falling_tetromino.command(InputProcessor.MOVE_RIGHT)
                    if not self.is_valid_position():
                        self._falling_tetromino.undo_command(InputProcessor.MOVE_RIGHT)
                        self._falling_tetromino.undo_command(InputProcessor.ROTATE_CLOCKWISE)

    def update_dummy(self):
        self.dummy._x = self._falling_tetromino._x
        self.dummy._y = self._falling_tetromino._y
        self.dummy._orientation = self._falling_tetromino._orientation
        self.dummy._block_board_coords = self._falling_tetromino._block_board_coords
        self.dummy._tetromino_type = self._falling_tetromino._tetromino_type
        print(self.dummy._x, self.dummy._y)

        while True:
            self.dummy.command(InputProcessor.MOVE_DOWN)
            if not self.is_valid_position(self.dummy):
                self.dummy.undo_command(InputProcessor.MOVE_DOWN)
                break
        print(self.dummy._x, self.dummy._y)

    def is_valid_position(self, mino=None):
        if mino is None:
            mino = self._falling_tetromino
        non_falling_block_coords = []
        for tetromino in self._tetromino_list:
            non_falling_block_coords.extend(tetromino.get_block_board_coords())
        for coord in mino.get_block_board_coords():
            out_of_bounds = coord[0] < 0 or coord[0] >= self._grid_width or \
                            coord[1] < 0
            overlapping = coord in non_falling_block_coords
            if out_of_bounds or overlapping:
                return False
        return True

    def find_full_rows(self):
        non_falling_block_coords = []
        for tetromino in self._tetromino_list:
            non_falling_block_coords.extend(tetromino.get_block_board_coords())

        row_counts = {}
        for i in range(self._grid_height + Board.STARTING_ZONE_HEIGHT):
            row_counts[i] = 0
        for coord in non_falling_block_coords:
            row_counts[coord[1]] += 1

        full_rows = []
        for row in row_counts:
            if row_counts[row] == self._grid_width:
                full_rows.append(row)
        return full_rows

    def clear_row(self, grid_row):
        tetrominos = []
        for tetromino in self._tetromino_list:
            if tetromino.clear_row_and_adjust_down(grid_row):
                tetrominos.append(tetromino)
        self._tetromino_list = tetrominos

    def clear_rows(self, grid_rows):
        grid_rows.sort(reverse=True)
        for row in grid_rows:
            self.clear_row(row)

    def update_tick(self):
        num_cleared_rows = 0
        game_lost = False
        self._falling_tetromino.command(InputProcessor.MOVE_DOWN)

        if not self.is_valid_position():
            self._falling_tetromino.undo_command(InputProcessor.MOVE_DOWN)
            if self._is_after_move:
                self._is_after_move = False
            else:
                self._tetromino_list.append(self._falling_tetromino)
                full_rows = self.find_full_rows()
                self.clear_rows(full_rows)
                game_lost = self.is_in_start_zone(self._falling_tetromino)
                if not game_lost:
                    self.spawn_tetromino()
                    self._holder.release()
                num_cleared_rows = len(full_rows)
        return num_cleared_rows, game_lost

    def is_in_start_zone(self, tetromino):
        for coords in tetromino.get_block_board_coords():
            if coords[1] >= self._grid_height:
                return True
        return False

    def grid_coords_to_screen_coords(self, coords):
        screen_coords = []
        for coord in coords:
            coord = (self._x + coord[0] * self._block_size,
                     self._y + coord[1] * self._block_size)
            screen_coords.append(coord)
        return screen_coords

    def draw(self):
        for tetromino in self._tetromino_list:
            screen_coords = self.grid_coords_to_screen_coords(
                tetromino.get_block_board_coords())
            tetromino.draw(screen_coords)

        screen_coords = self.grid_coords_to_screen_coords(
            self._falling_tetromino.get_block_board_coords())
        self._falling_tetromino.draw(screen_coords)

        screen_coords = self.grid_coords_to_screen_coords(
            self.dummy.get_block_board_coords())
        self.dummy.draw(screen_coords, isDummy=True)


class InfoDisplay(object):
    def __init__(self, window, score_x, score_y, lines_x, lines_y):
        self._score_label = pyglet.text.Label('{0:07d}'.format(0),
                                              font_size=18,
                                              x=score_x,
                                              y=score_y
                                              )
        self._rows_cleared_label = pyglet.text.Label('{0:07d}'.format(0),
                                                     font_size=18,
                                                     x=lines_x,
                                                     y=lines_y
                                                     )
        self._paused_label = pyglet.text.Label('PAUSED',
                                               font_size=32,
                                               x=window.width // 2,
                                               y=window.height // 2,
                                               anchor_x='center',
                                               anchor_y='center'
                                               )
        self._game_over_label = pyglet.text.Label('GAME OVER',
                                                  font_size=32,
                                                  x=window.width // 2,
                                                  y=window.height // 2,
                                                  anchor_x='center',
                                                  anchor_y='center'
                                                  )
        self._show_paused_label = False
        self._show_game_over_label = False

    def set_rows_cleared(self, num_rows_cleared):
        self._rows_cleared_label.text = '{0:07d}'.format(num_rows_cleared)

    def set_score(self, score):
        self._score_label.text = '{0:07d}'.format(score)

    def draw(self):
        self._rows_cleared_label.draw()
        self._score_label.draw()
        if self._show_paused_label:
            self._paused_label.draw()
        if self._show_game_over_label:
            self._game_over_label.draw()


class InputProcessor(object):
    TOGGLE_PAUSE, MOVE_UP, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, ROTATE_CLOCKWISE, HOLDING, DROP = range(8)

    def __init__(self):
        self.action = None

    def process_keypress(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.action = InputProcessor.TOGGLE_PAUSE
        elif symbol == pyglet.window.key.Z:
            self.action = InputProcessor.ROTATE_CLOCKWISE
        elif symbol == pyglet.window.key.LSHIFT:
            self.action = InputProcessor.HOLDING

    def process_text_motion(self, motion):
        if motion == pyglet.window.key.MOTION_LEFT:
            self.action = InputProcessor.MOVE_LEFT
        elif motion == pyglet.window.key.MOTION_RIGHT:
            self.action = InputProcessor.MOVE_RIGHT
        elif motion == pyglet.window.key.MOTION_DOWN:
            self.action = InputProcessor.MOVE_DOWN
        elif motion == pyglet.window.key.MOTION_UP:
            self.action = InputProcessor.DROP

    def consume(self):
        action = self.action
        self.action = None
        return action


class GameTick(object):
    def __init__(self, tick_on_first_call=False):
        self.tick = tick_on_first_call
        self.started = tick_on_first_call

    def is_tick(self, next_tick_time):
        def set_tick(dt):
            self.tick = True

        if not self.started:
            self.started = True
            pyglet.clock.schedule_once(set_tick, next_tick_time)
            return False
        elif self.tick:
            self.tick = False
            pyglet.clock.schedule_once(set_tick, next_tick_time)
            return True
        else:
            return False


class Game(object):
    def __init__(self, board, info_display, key_input, background_image, queue, holder):
        self._queue = queue
        self._board = board
        self._info_display = info_display
        self._input = key_input
        self._background_image = background_image
        self._paused = False
        self._lost = False
        self._num_rows_cleared = 0
        self._score = 0
        self._tick_speed = 0.3
        self._ticker = GameTick()
        self._holder = holder

    def add_rows_cleared(self, rows_cleared):
        self._num_rows_cleared += rows_cleared
        if rows_cleared == 1:
            self._score += 1
        elif rows_cleared == 2:
            self._score += 2
        elif rows_cleared == 3:
            self._score += 5
        elif rows_cleared == 4:
            self._score += 8

        elif self._score >= 60:
            self._tick_speed = 0.05
        elif self._score >= 40:
            self._tick_speed = 0.1
        elif self._score >= 20:
            self._tick_speed = 0.2


        self._info_display.set_rows_cleared(self._num_rows_cleared)
        self._info_display.set_score(self._score)

    def toggle_pause(self):
        self._paused = not self._paused
        self._info_display.showPausedLabel = self._paused



    def update(self):
        if self._lost:
            self._info_display._show_game_over_label = True
        else:
            command = self._input.consume()
            if command == InputProcessor.TOGGLE_PAUSE:
                self.toggle_pause()
            if not self._paused:
                if command and command != InputProcessor.TOGGLE_PAUSE:
                    self._board.command_falling_tetromino(command)
                if self._ticker.is_tick(self._tick_speed) or command == InputProcessor.MOVE_UP:
                    print(self._board._is_after_move)
                    rows_cleared, self._lost = self._board.update_tick()
                    self.add_rows_cleared(rows_cleared)
                self._board.update_dummy()


    def draw(self):
        self._background_image.blit(0, 0)
        self._board.draw()
        self._queue.draw()
        self._info_display.draw()
        self._holder.draw()


class NextTetrominoQueue(object):
    """
    Nextブロックを管理するキュー
    """
    NEXT_COUNT = 3

    def __init__(self, x, y, block_size, set_count=3):
        self._x = x
        self._y = y
        self._set_count = set_count
        self._block_size = block_size
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

    def grid_coords_to_screen_coords(self, coords):
        screen_coords = []
        for coord in coords:
            coord = (self._x + coord[0] * self._block_size,
                     self._y + coord[1] * self._block_size)
            screen_coords.append(coord)
        return screen_coords

    def draw(self):
        for i in range(self.NEXT_COUNT):
            self._queue[i].set_position(0, 4 * (self.NEXT_COUNT - i - 1))
            screen_coords = self.grid_coords_to_screen_coords(
                self._queue[i].get_block_board_coords())
            self._queue[i].draw(screen_coords)


class Holder(object):
    def __init__(self, x, y, block_size):
        self._x = x
        self._y = y
        self._block_size = block_size
        self._tetromino = None  # type: Tetromino
        self._is_swapped = False

    def grid_coords_to_screen_coords(self, coords):
        screen_coords = []
        for coord in coords:
            coord = (self._x + coord[0] * self._block_size,
                     self._y + coord[1] * self._block_size)
            screen_coords.append(coord)
        return screen_coords

    def draw(self):
        if self._tetromino is None:
            return

        screen_coords = self.grid_coords_to_screen_coords(
            self._tetromino.get_block_board_coords())
        self._tetromino.draw(screen_coords)

    def swap(self, tetromino):
        if self._is_swapped:
            return tetromino, False
        else:
            self._is_swapped = True
            self._tetromino, tetromino = tetromino, self._tetromino
            self._tetromino.set_position(0, 0)
            return tetromino, True

    def release(self):
        self._is_swapped = False
