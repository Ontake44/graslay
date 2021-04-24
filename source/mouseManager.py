
import pyxel
from settings import Settings

class MouseManager:
    def __init__(self):
        self.prevMouseX = pyxel.mouse_x
        self.prevMouseY = pyxel.mouse_y
        self.mouseCounter = 0
        self.visible = False

    def isOutOfScreen(self):
        return pyxel.mouse_x < 0 or pyxel.mouse_y < 0 or pyxel.mouse_x >= pyxel.width or pyxel.mouse_y >= pyxel.height

    def update(self):
        if Settings.mouseEnabled == False:
            self.visible = False
            return
		
        # 5秒マウス触らなかったらカーソル消える
        if (self.prevMouseX != pyxel.mouse_x or self.prevMouseY != pyxel.mouse_y) and self.isOutOfScreen() == False:
            self.mouseCounter = 0
            self.visible = True
            self.prevMouseX = pyxel.mouse_x
            self.prevMouseY = pyxel.mouse_y
        else:
            self.prevMouseX = pyxel.mouse_x
            self.prevMouseY = pyxel.mouse_y
            self.mouseCounter += 1
            if self.mouseCounter > 180:
                self.visible = False
	
    def draw(self):
        # マウスカーソル
        if self.visible:
            self.drawMenuCursor()

    def drawMenuCursor(self):
        if pyxel.frame_count & 32 == 0:
            pyxel.pal(6, 7)
        pyxel.blt(pyxel.mouse_x -7, pyxel.mouse_y -7, 0, 40, 32, 16, 16, 2)
        pyxel.pal()

