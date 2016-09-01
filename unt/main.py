import pyglet

from unt import game

# グローバルな定数たち
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


class Main(pyglet.window.Window):
    TOGGLE_PAUSE, MOVE_DOWN, MOVE_LEFT, MOVE_RIGHT, ROTATE_CLOCKWISE = range(5)

    def __init__(self, width, height):
        super().__init__(width=width, height=height)
        self.width = width
        self.height = height
        pyglet.resource.path = ['res']
        pyglet.resource.reindex()
        self.background = pyglet.resource.image('background.jpg')  # type: pyglet.image.AbstractImage
        self.block_image = pyglet.resource.image('blocks.png')  # type: pyglet.image.AbstractImage
        self.board_background_image = pyglet.resource.image('border.png')  # type: pyglet.image.AbstractImage
        self.block_size = min(self.block_image.width, self.block_image.height)
        self.action = None

        game.TetrominoType.block_init(self.block_image, self.block_size)
        self.queue = game.NextTetrominoQueue()

        self.board = game.Board(80, 50, self.queue, self.block_size, self.board_background_image)

        pyglet.clock.schedule_interval(self.update, 1 / 60.0)

        # でばぐよう
        self.board.spawn_tetromino()

    def on_draw(self):
        self.clear()
        self.background.blit(0, 0)
        self.board.draw()

    def update(self, delta):
        action = self.action
        self.action = None
        if action in (self.MOVE_DOWN, self.MOVE_LEFT, self.MOVE_RIGHT):
            self.board.send_action_falling_tetromino(action)

    def on_key_press(self, symbol, modifiers):
        pass

    def on_text_motion(self, motion):
        if motion == pyglet.window.key.MOTION_LEFT:
            self.action = self.MOVE_LEFT
        elif motion == pyglet.window.key.MOTION_RIGHT:
            self.action = self.MOVE_RIGHT
        elif motion == pyglet.window.key.MOTION_UP:
            self.action = self.ROTATE_CLOCKWISE
        elif motion == pyglet.window.key.MOTION_DOWN:
            self.action = self.MOVE_DOWN


if __name__ == '__main__':
    main = Main(width=WINDOW_WIDTH, height=WINDOW_HEIGHT)
    pyglet.app.run()
