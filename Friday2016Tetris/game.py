import random

import pyglet


class TetrominoType(object):
    def __init__(self, block_image, local_block_coords_by_orientation):
        self.blockImage = block_image
        self.localBlockCoordsByOrientation = local_block_coords_by_orientation

    @staticmethod
    def class_init(block_image, block_size):
        cyan = block_image.get_region(block_size, y=0, width=block_size,
                                      height=block_size)
        yellow = block_image.get_region(x=block_size *2, y=0, width=block_size,
                                        height=block_size)
        green = block_image.get_region(x=block_size * 3, y=0, width=block_size,
                                       height=block_size)
        red = block_image.get_region(x=block_size * 4, y=0, width=block_size,
                                     height=block_size)
        blue = block_image.get_region(x=block_size * 5, y=0, width=block_size,
                                      height=block_size)
        orange = block_image.get_region(x=block_size * 6, y=0,
                                        width=block_size, height=block_size)
        purple = block_image.get_region(x=block_size * 7, y=0,
                                        width=block_size, height=block_size)

        TetrominoType.TYPES = [
            # type I
            TetrominoType(cyan,
                          {
                              Tetromino.RIGHT: [(0, 1), (1, 1), (2, 1),(3, 1)],
                              Tetromino.DOWN: [(1, 0), (1, 1), (1, 2), (1, 3)],
                              Tetromino.LEFT: [(0, 2), (1, 2), (2, 2), (3, 2)],
                              Tetromino.UP: [(2, 0), (2, 1), (2, 2), (2, 3)],
                          }
                          ),
            # type O
            TetrominoType(yellow,
                          {
                              Tetromino.RIGHT: [(0, 0), (0, 1), (1, 0),(1, 1)],
                              Tetromino.DOWN: [(0, 0), (0, 1), (1, 0), (1, 1)],
                              Tetromino.LEFT: [(0, 0), (0, 1), (1, 0), (1, 1)],
                              Tetromino.UP: [(0, 0), (0, 1), (1, 0), (1, 1)],
                          }
                          ),
            # type S
            TetrominoType(green,
                          {
                              Tetromino.RIGHT: [(0, 0), (1, 0), (1, 1),(2, 1)],
                              Tetromino.DOWN: [(0, 2), (0, 1), (1, 1), (1, 0)],
                              Tetromino.LEFT: [(0, 0), (1, 0), (1, 1), (2, 1)],
                              Tetromino.UP: [(0, 2), (0, 1), (1, 1), (1, 0)],
                          }
                          ),
            # type Z
            TetrominoType(red,
                          {
                              Tetromino.RIGHT: [(0, 1), (1, 1), (1, 0),(2, 0)],
                              Tetromino.DOWN: [(0, 0), (0, 1), (1, 1), (1, 2)],
                              Tetromino.LEFT: [(0, 1), (1, 1), (1, 0), (2, 0)],
                              Tetromino.UP: [(0, 0), (0, 1), (1, 1), (1, 2)],
                          }
                          ),
            # type J
            TetrominoType(blue,
                          {
                              Tetromino.RIGHT: [(0, 1), (0, 0), (1, 0),(2, 0)],
                              Tetromino.DOWN: [(0, 2), (0, 1), (0, 0), (1, 2)],
                              Tetromino.LEFT: [(0, 2), (1, 2), (2, 2), (2, 1)],
                              Tetromino.UP: [(2, 2), (2, 1), (2, 0), (1, 0)],
                          }
                          ),
            # type L
            TetrominoType(orange,
                          {
                              Tetromino.RIGHT: [(0, 0), (1, 0), (2, 0),(2, 1)],
                              Tetromino.DOWN: [(0, 2), (0, 1), (0, 0), (1, 0)],
                              Tetromino.LEFT: [(0, 1), (0, 2), (1, 2), (2, 2)],
                              Tetromino.UP: [(1, 2), (2, 2), (2, 1), (2, 0)],
                          }
                          ),
            # type T
            TetrominoType(purple,
                          {
                              Tetromino.RIGHT: [(2, 1), (1, 1), (0, 1),(1, 2)],
                              Tetromino.DOWN: [(0, 2), (0, 1), (0, 0), (1, 1)],
                              Tetromino.LEFT: [(0, 2), (1, 2), (1, 1), (2, 2)],
                              Tetromino.UP: [(1, 1), (2, 2), (2, 1), (2, 0)],
                          }
                          ),
        ]

    @staticmethod
    def random_type():
        return random.choice(TetrominoType.TYPES)


class Tetromino(object):
    RIGHT, DOWN, LEFT, UP = range(4)
    CLOCKWISE_ROTATIONS = {RIGHT: DOWN, DOWN: LEFT, LEFT: UP, UP: RIGHT}

    def __init__(self):
        self.x = 0
        self.y = 0
        self.tetrominoType = TetrominoType.random_type()
        self.orientation = Tetromino.RIGHT
        self.blockBoardCoords = self.calc_block_board_coords()

    def calc_block_board_coords(self):
        local_block_coords = self.tetrominoType.localBlockCoordsByOrientation[
            self.orientation]
        grid_coords = []
        for coord in local_block_coords:
            grid_coord = (coord[0] + self.x, coord[1] + self.y)
            grid_coords.append(grid_coord)
        return grid_coords

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.blockBoardCoords = self.calc_block_board_coords()

    def move_down(self):
        self.y -= 1
        self.blockBoardCoords = self.calc_block_board_coords()

    def move_up(self):
        self.y += 1
        self.blockBoardCoords = self.calc_block_board_coords()

    def move_left(self):
        self.x -= 1
        self.blockBoardCoords = self.calc_block_board_coords()

    def move_right(self):
        self.x += 1
        self.blockBoardCoords = self.calc_block_board_coords()

    # def hold(self):


    def rotate_clockwise(self):
        self.orientation = Tetromino.CLOCKWISE_ROTATIONS[self.orientation]
        self.blockBoardCoords = self.calc_block_board_coords()

    def rotate_counterclockwise(self):
        self.orientation = Tetromino.CLOCKWISE_ROTATIONS[self.orientation]
        self.orientation = Tetromino.CLOCKWISE_ROTATIONS[self.orientation]
        self.orientation = Tetromino.CLOCKWISE_ROTATIONS[self.orientation]
        self.blockBoardCoords = self.calc_block_board_coords()

    def command(self, command):
        if command == Input.MOVE_DOWN:
            self.move_down()
        elif command == Input.MOVE_RIGHT:
            self.move_right()
        elif command == Input.MOVE_LEFT:
            self.move_left()
        elif command == Input.ROTATE_CLOCKWISE:
            self.rotate_clockwise()
        elif command == Input.HOLD:
            self.hold()

    def undo_command(self, command):
        if command == Input.MOVE_DOWN:
            self.move_up()
        elif command == Input.MOVE_RIGHT:
            self.move_left()
        elif command == Input.MOVE_LEFT:
            self.move_right()
        elif command == Input.ROTATE_CLOCKWISE:
            self.rotate_counterclockwise()

    def clear_row_and_adjust_down(self, board_grid_row):
        new_block_board_coords = []
        for coord in self.blockBoardCoords:
            if coord[1] > board_grid_row:
                adjusted_coord = (coord[0], coord[1] - 1)
                new_block_board_coords.append(adjusted_coord)
            if coord[1] < board_grid_row:
                new_block_board_coords.append(coord)
        self.blockBoardCoords = new_block_board_coords
        return len(self.blockBoardCoords) > 0

    def draw(self, screen_coords):
        image = self.tetrominoType.blockImage
        for coords in screen_coords:
            image.blit(coords[0], coords[1])


class Board(object):
    STARTING_ZONE_HEIGHT = 4
    NEXT_X = -5
    NEXT_Y = 20
    SET_SCORE = 0
    def __init__(self, x, y, grid_width, grid_height, block_size):
        self.x = x
        self.y = y
        self.gridWidth = grid_width
        self.gridHeight = grid_height
        self.blockSize = block_size
        self.spawnX = int(grid_width * 1 / 3)
        self.spawnY = grid_height
        self.nextTetromino = Tetromino()
        self.fallingTetromino = None
        self.spawn_tetromino()
        self.tetrominos = []

    def spawn_tetromino(self):
        self.fallingTetromino = self.nextTetromino
        self.nextTetromino = Tetromino()
        self.fallingTetromino.set_position(self.spawnX, self.spawnY)
        self.nextTetromino.set_position(Board.NEXT_X, Board.NEXT_Y)

    def command_falling_tetromino(self, command):
        self.fallingTetromino.command(command)
        if not self.is_valid_position():
            self.fallingTetromino.undo_command(command)

    def is_valid_position(self):
        non_falling_block_coords = []
        for tetromino in self.tetrominos:
            non_falling_block_coords.extend(tetromino.blockBoardCoords)
        for coord in self.fallingTetromino.blockBoardCoords:
            out_of_bounds = coord[0] < 0 or coord[0] >= self.gridWidth or \
                            coord[1] < 0
            overlapping = coord in non_falling_block_coords
            if out_of_bounds or overlapping:
                return False
        return True

    def find_full_rows(self):
        non_falling_block_coords = []
        for tetromino in self.tetrominos:
            non_falling_block_coords.extend(tetromino.blockBoardCoords)

        row_counts = {}
        for i in range(self.gridHeight + Board.STARTING_ZONE_HEIGHT):
            row_counts[i] = 0
        for coord in non_falling_block_coords:
            row_counts[coord[1]] += 1

        full_rows = []
        for row in row_counts:
            if row_counts[row] == self.gridWidth:
                full_rows.append(row)
        return full_rows

    def clear_row(self, grid_row):
        tetrominos = []
        for tetromino in self.tetrominos:
            if tetromino.clear_row_and_adjust_down(grid_row):
                tetrominos.append(tetromino)
        self.tetrominos = tetrominos

    def clear_rows(self, grid_rows):
        grid_rows.sort(reverse=True)
        for row in grid_rows:
            self.clear_row(row)

    def update_tick(self):
        num_cleared_rows = 0
        game_lost = False
        self.fallingTetromino.command(Input.MOVE_DOWN)
        if not self.is_valid_position():
            self.fallingTetromino.undo_command(Input.MOVE_DOWN)
            self.tetrominos.append(self.fallingTetromino)
            full_rows = self.find_full_rows()
            self.clear_rows(full_rows)
            game_lost = self.is_in_start_zone(self.fallingTetromino)
            if not game_lost:
                self.spawn_tetromino()
            num_cleared_rows = len(full_rows)
        return num_cleared_rows, game_lost

    def is_in_start_zone(self, tetromino):
        for coords in tetromino.blockBoardCoords:
            if coords[1] >= self.gridHeight:
                return True
        return False

    def grid_coords_to_screen_coords(self, coords):
        screen_coords = []
        for coord in coords:
            coord = (self.x + coord[0] * self.blockSize,
                     self.y + coord[1] * self.blockSize)
            screen_coords.append(coord)
        return screen_coords

    def draw(self):
        for tetromino in self.tetrominos:
            screen_coords = self.grid_coords_to_screen_coords(
                tetromino.blockBoardCoords)
            tetromino.draw(screen_coords)

        screen_coords = self.grid_coords_to_screen_coords(
            self.fallingTetromino.blockBoardCoords)
        self.fallingTetromino.draw(screen_coords)

        screen_coords = self.grid_coords_to_screen_coords(
            self.nextTetromino.blockBoardCoords)
        self.nextTetromino.draw(screen_coords)


class InfoDisplay(object):
    ROWS_CLEARED_X = 70
    ROWS_CLEARED_Y = 550

    def __init__(self, window):
        self.scoreLabel = pyglet.text.Label("Your Score: 0",
                                            font_size=14,
                                            x=InfoDisplay.ROWS_CLEARED_X ,
                                            y=InfoDisplay.ROWS_CLEARED_Y - 30)

        self.rowsClearedLabel = pyglet.text.Label('Rows cleared: 0',
                                                  font_size=14,
                                                  x=InfoDisplay.ROWS_CLEARED_X,
                                                  y=InfoDisplay.ROWS_CLEARED_Y
                                                  )
        self.pausedLabel = pyglet.text.Label('PAUSED',
                                             font_size=32,
                                             x=window.width // 2,
                                             y=window.height // 2,
                                             anchor_x='center',
                                             anchor_y='center'
                                             )
        self.gameoverLabel = pyglet.text.Label('GAME OVER',
                                               font_size=32,
                                               x=window.width // 2,
                                               y=window.height // 2,
                                               anchor_x='center',
                                               anchor_y='center'
                                               )
        self.showPausedLabel = False
        self.showGameoverLabel = False

    def set_rows_cleared(self, num_rows_cleared):
        self.rowsClearedLabel.text = 'Rows cleared: ' + str(num_rows_cleared)

    # def set_score(self,)
    #     self.scoreLabel.text = 'Your Score:' + str()

    def draw(self):
        self.scoreLabel.draw()
        self.rowsClearedLabel.draw()
        if self.showPausedLabel:
            self.pausedLabel.draw()
        if self.showGameoverLabel:
            self.gameoverLabel.draw()


class Input(object):
    TOGGLE_PAUSE, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, ROTATE_CLOCKWISE, HOLD = range(6)

    def __init__(self):
        self.action = None

    def process_keypress(self, symbol, modifiers):
        if symbol == pyglet.window.key.SPACE:
            self.action = Input.TOGGLE_PAUSE
        elif symbol == pyglet.window.key.Z:
            self.action = Input.ROTATE_CLOCKWISE
        elif symbol == pyglet.window.key.LSHIFT:
            self.action = Input.HOLD

    def process_text_motion(self, motion):
        if motion == pyglet.window.key.MOTION_LEFT:
            self.action = Input.MOVE_LEFT
        elif motion == pyglet.window.key.MOTION_RIGHT:
            self.action = Input.MOVE_RIGHT

        elif motion == pyglet.window.key.MOTION_DOWN:
            self.action = Input.MOVE_DOWN

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
    def __init__(self, board, info_display, key_input, background_image, border_Image):
        self.board = board
        self.infoDisplay = info_display
        self.input = key_input
        self.backgroundImage = background_image
        self.borderImage = border_Image
        self.paused = False
        self.lost = False
        self.numRowsCleared = 0
        #  self.Score = 0
        self.tickSpeed = 0.6
        self.ticker = GameTick()

    def add_rows_cleared(self, rows_cleared):
        self.numRowsCleared += rows_cleared
        self.infoDisplay.set_rows_cleared(self.numRowsCleared)

    # def add_score_set(self,score_set):
    #     self.Score += score_set
    #     self.infoDisplay.

    def toggle_pause(self):
        self.paused = not self.paused
        self.infoDisplay.showPausedLabel = self.paused

    def update(self):
        if self.lost:
            self.infoDisplay.showGameoverLabel = True
        else:
            command = self.input.consume()
            if command == Input.TOGGLE_PAUSE:
                self.toggle_pause()
            if not self.paused:
                if command and command != Input.TOGGLE_PAUSE:
                    self.board.command_falling_tetromino(command)
                if self.ticker.is_tick(self.tickSpeed):
                    rows_cleared, self.lost = self.board.update_tick()
                    self.add_rows_cleared(rows_cleared)

    def draw(self):
        self.backgroundImage.blit(0, 0)
        self.borderImage.blit(445,13)
        self.board.draw()
        self.infoDisplay.draw()