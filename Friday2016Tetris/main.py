import pyglet

import game


WIDTH = 800
HEIGHT = 600
BOARD_X = 445
BOARD_Y = 13
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 25

window = pyglet.window.Window(WIDTH, HEIGHT)
window.set_vsync(False)

###### load resources ######
backgroundImage = pyglet.resource.image('res/background.jpg')
blocksImage = pyglet.resource.image('res/blocks.png')
boarderImage = pyglet.resource.image('res/border.png')
game.TetrominoType.class_init(blocksImage, BLOCK_SIZE)

###### init game state ######
board = game.Board(BOARD_X, BOARD_Y, GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE)
infoDisplay = game.InfoDisplay(window)
input = game.Input()
game = game.Game(board, infoDisplay, input, backgroundImage, boarderImage)


@window.event
def on_key_press(symbol, modifiers):
    input.process_keypress(symbol, modifiers)
    #window.push_handlers(pyglet.window.event.WindowEventLogger())


@window.event
def on_text_motion(motion):
    input.process_text_motion(motion)


@window.event
def on_draw():
    game.draw()


def update(dt):
    game.update()


pyglet.clock.schedule_interval(update, 1 / 60.0)
pyglet.app.run()