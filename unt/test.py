import pyglet

window = pyglet.window.Window(width=800, height=600)
pyglet.resource.path = ['res']
pyglet.resource.reindex()

block_image = pyglet.resource.image('blocks.png')  # type: pyglet.image.AbstractImage
blocks = []

for i in range(8):
    blocks.append(block_image.get_region(i * 25, 0, 25, 25))


@window.event
def on_draw():
    window.clear()
    blocks[0].blit(0, 0)
    blocks[1].blit(50, 50)
    blocks[2].blit(100, 100)
    blocks[3].blit(150, 150)
    blocks[4].blit(200, 200)
    blocks[5].blit(250, 250)
    blocks[6].blit(300, 300)
    blocks[7].blit(350, 350)


pyglet.app.run()
