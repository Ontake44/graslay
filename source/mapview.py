import pyxel


MAP_PATTERN_FILE= "assets/graslay.pyxres"
MAP_IMAGE_FILE = "assets\graslay1.png"

class App:
	def __init__(self):
		pyxel.init(256, 200, caption="GRASLAY",fps=60)

		self.map_x = 0
		self.map_y = 0

		pyxel.load(MAP_PATTERN_FILE)
		pyxel.image(1).load(0,0, MAP_IMAGE_FILE)
		pyxel.tilemap(0).refimg = 1
		

		
		pyxel.run(self.update, self.draw)


	def update(self):
		if pyxel.btnp(pyxel.KEY_Q):
			pyxel.quit()

		if pyxel.btnp(pyxel.KEY_R):
			pyxel.load(MAP_PATTERN_FILE)
			pyxel.image(1).load(0,0, MAP_IMAGE_FILE)

		if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
			self.map_x += 1
		elif pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
			self.map_x -= 1
		
		if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):
			self.map_y -= 1
		elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
			self.map_y += 1


	def draw(self):
		pyxel.cls(0)
		pyxel.bltm(0, 0, 0, self.map_x, self.map_y, 32, 24, 2)
		#pyxel.text(4,2, str(self.map_y), 7)

App()
