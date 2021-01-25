import pyxel
import gcommon

MENU_PLAYER_STOCK = 0
MENU_START_STAGE = 1
MENU_GAME_START = 2
MENU_EXIT = 3

class CustomStartMenuScene:
	def __init__(self):
		self.menuYList = (50, 70, 90, 110)
		self.menuPos = 0
		self.state = 0
		self.cnt = 0
	
	def init(self):
		self.menuPos = 0

	def update(self):
		if self.cnt >= 6*60:
			self.cnt = 0
		if self.state == 0:
			if gcommon.checkUpP():
				self.menuPos -= 1
				if self.menuPos < 0:
					self.menuPos = 3
			if gcommon.checkDownP():
				self.menuPos += 1
				if self.menuPos > 3:
					self.menuPos = 0
			
			if gcommon.checkRightP():
				if self.menuPos == MENU_PLAYER_STOCK:
					gcommon.Settings.playerStock += 1
					if gcommon.Settings.playerStock > 99:
						gcommon.Settings.playerStock = 99
				elif self.menuPos == MENU_START_STAGE:
					gcommon.Settings.startStage += 1
					if gcommon.Settings.startStage > 6:
						gcommon.Settings.startStage = 6
			elif gcommon.checkLeftP():
				if self.menuPos == MENU_PLAYER_STOCK:
					gcommon.Settings.playerStock -= 1
					if gcommon.Settings.playerStock < 1:
						gcommon.Settings.playerStock = 1
				elif self.menuPos == MENU_START_STAGE:
					gcommon.Settings.startStage -= 1
					if gcommon.Settings.startStage < 1:
						gcommon.Settings.startStage = 1
			
			if gcommon.checkShotKey():
				gcommon.saveSettings()
				if self.menuPos == MENU_GAME_START:
					gcommon.sound(gcommon.SOUND_GAMESTART)
					self.state = 1
					self.cnt = 0
				elif self.menuPos == MENU_EXIT:
					gcommon.app.startTitle()
		else:
			# GAME START
			if self.cnt > 40:
				gcommon.app.startGame(gcommon.DIFFICULTY_EASY, gcommon.Settings.startStage, gcommon.Settings.playerStock)
		self.cnt += 1

	def draw(self):
		pyxel.cls(1)
		gcommon.showTextHCenter(8, "CUSTOM START")
		
		x1 = 64
		x2 = 180
		self.setOptionColor(MENU_PLAYER_STOCK)
		gcommon.showText(x1, self.menuYList[0], "PLAYER STOCK")
		gcommon.showText(x2, self.menuYList[0], str(gcommon.Settings.playerStock).rjust(2))
		if MENU_PLAYER_STOCK == self.menuPos:
			gcommon.drawUpDownMarker(x2 -10, self.menuYList[0])

		self.setOptionColor(MENU_START_STAGE)
		gcommon.showText(x1, self.menuYList[1], "START STAGE")
		gcommon.showText(x2, self.menuYList[1], str(gcommon.Settings.startStage).rjust(2))
		if MENU_START_STAGE == self.menuPos:
			gcommon.drawUpDownMarker(x2 -10, self.menuYList[1])

		if self.state == 0:
			self.setOptionColor(MENU_GAME_START)
			gcommon.showText(x1, self.menuYList[2], "GAME START")
		else:
			if self.cnt & 2 == 0:
				pyxel.pal(7, 8)
			gcommon.showText(x1, self.menuYList[2], "GAME START")
			if self.cnt & 2 == 0:
				pyxel.pal()
		
		self.setOptionColor(MENU_EXIT)
		gcommon.showText(x1, self.menuYList[3], "EXIT")
		pyxel.pal()

		pyxel.blt(x1 -12, self.menuYList[self.menuPos], 0, 8, 32, 8, 8, gcommon.TP_COLOR)

	def setOptionColor(self, index):
		if index == self.menuPos:
			pyxel.pal()
		else:
			pyxel.pal(7, 12)

#
