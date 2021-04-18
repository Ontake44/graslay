import pyxel


#MAP_FILE0 = "assets/stage_warehouse0.pyxmap"
#MAP_FILE1 = "assets/stage_warehouse1.pyxmap"
#MAP_IMAGE_FILE = "assets/stage_warehouse.png"
MAP_FILE0 = "assets/stage_cave.pyxmap"
#MAP_FILE1 = "assets/stage_warehouse1.pyxmap"
MAP_IMAGE_FILE = "assets/stage_cave.png"

class App:
	def __init__(self):
		pyxel.init(256, 200, caption="Mapview",fps=60)

		self.map_x = 0
		self.map_y = 0

		self.loadData()
		pyxel.tilemap(0).refimg = 1
		#pyxel.tilemap(1).refimg = 1

		
		pyxel.run(self.update, self.draw)

	def loadData(self):
		pyxel.image(1).load(0,0, MAP_IMAGE_FILE)
		self.loadMapData(0, MAP_FILE0)
		#self.loadMapData(1, MAP_FILE1)

	def loadMapData(self, tm, fileName):
		mapFile = open(fileName, mode = "r")
		lines = mapFile.readlines()
		mapFile.close()
		pyxel.tilemap(tm).set(0, 0, lines)
	
	def update(self):
		if pyxel.btnp(pyxel.KEY_Q):
			pyxel.quit()

		if pyxel.btnp(pyxel.KEY_R):
			self.loadData()

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
		#pyxel.bltm(0, 0, 1, self.map_x, self.map_y, 32, 32, 3)
		pyxel.bltm(0, 0, 0, self.map_x, self.map_y, 32, 32, 2)
		pyxel.text(4,2, str(self.map_x) + " " + str(self.map_y), 7)

App()
