import pyglet
#
# window = pyglet.window.Window(width=800, height=600)
# pyglet.resource.path = ['res']
# pyglet.resource.reindex()
# background = pyglet.resource.image('.jpg')
#
#`
# @window.event
# def on_draw():
#     window.clear()
#     background.blit(0,0)

class Main(pyglet.window.Window):
    def __init__(self, width, height):
        super().__init__(width=width, height=height)
        self.width = width
        self.height = height
        # リソースパス設定
        pyglet.resource.path = ['res']
        pyglet.resource.reindex()

        block_image = pyglet.resource.image('blocks.png') #type: pyglet.image.Abstract
        blocks = []

        for i in range(8):
            blocks.append(block_image.get_region(i * 25, 0, 25, 25))

        # 背景画像取得
        self.background = pyglet.resource.image('background.jpg')
        self.image_center(self.background)



    def on_draw(self):
        self.clear()
        self.background.blit(self.width / 2, self.height / 2)

        self.blocks[0].blit(0, 0)
        self.blocks[1].blit(50, 50)
        self.blocks[2].blit(100, 100)
        self.blocks[3].blit(150, 150)
        self.blocks[4].blit(200, 200)
        self.blocks[5].blit(250, 250)
        self.blocks[6].blit(300, 300)
        self.blocks[7].blit(350, 350)




    @staticmethod
    def image_center(image: pyglet.image.AbstractImage):
        image.anchor_y = image.height / 2
        image.anchor_x = image.width / 2



if __name__ == '__main__':
    main = Main(width=800, height=600)
    pyglet.app.run()