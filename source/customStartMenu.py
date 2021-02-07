import pyxel
import gcommon

MENU_DIFFCULTY = 0
MENU_PLAYER_STOCK = 1
MENU_START_STAGE = 2
MENU_GAME_START = 3
MENU_EXIT = 4

MENU_VALUE_X = 180

class CustomStartMenuScene:
	def __init__(self):
		self.menuYList = (50, 70, 90, 118, 138)
		self.menuPos = 0
		self.state = 0
		self.cnt = 0
		self.mouseManager = gcommon.MouseManager()
		self.menuRects = []
		for y in self.menuYList:
			self.menuRects.append(gcommon.Rect.create(
				16, y, 16 +224 -1, y +12-1))
		self.difficultyRects = [
			gcommon.Rect.createWH(MENU_VALUE_X -10, self.menuYList[0], 8, 8),
			gcommon.Rect.createWH(MENU_VALUE_X +8*6 +2, self.menuYList[0], 8, 8),
		]
		self.playerStockRects = [
			gcommon.Rect.createWH(MENU_VALUE_X -10, self.menuYList[1], 8, 8),
			gcommon.Rect.createWH(MENU_VALUE_X -10+26, self.menuYList[1], 8, 8)
		]
		self.startStageRects = [
			gcommon.Rect.createWH(MENU_VALUE_X -10, self.menuYList[2], 8, 8),
			gcommon.Rect.createWH(MENU_VALUE_X -10+26, self.menuYList[2], 8, 8)
		]

	def init(self):
		self.menuPos = 0

	def update(self):
		self.mouseManager.update()
		if self.cnt >= 6*60:
			self.cnt = 0
		if self.state == 0:
			if gcommon.checkUpP():
				gcommon.sound(gcommon.SOUND_MENUMOVE)
				self.menuPos -= 1
				if self.menuPos < 0:
					self.menuPos = 4
			if gcommon.checkDownP():
				gcommon.sound(gcommon.SOUND_MENUMOVE)
				self.menuPos += 1
				if self.menuPos > 4:
					self.menuPos = 0
			
			if self.mouseManager.visible:
				n = gcommon.checkMouseMenuPos(self.menuRects)
				if n != -1:
					self.menuPos = n

			if self.menuPos == MENU_DIFFCULTY:
				n = -1
				if self.mouseManager.visible:
					n = gcommon.checkMouseMenuPos(self.difficultyRects)
				if gcommon.checkRightP() or (gcommon.checkShotKeyP() and n == 1):
					gcommon.Settings.difficulty = gcommon.DIFFICULTY_NORMAL
					gcommon.sound(gcommon.SOUND_MENUMOVE)
				elif gcommon.checkLeftP() or (gcommon.checkShotKeyP() and n == 0):
					gcommon.Settings.difficulty = gcommon.DIFFICULTY_EASY
					gcommon.sound(gcommon.SOUND_MENUMOVE)
			elif self.menuPos == MENU_PLAYER_STOCK:
				n = -1
				if self.mouseManager.visible:
					n = gcommon.checkMouseMenuPos(self.playerStockRects)
				if gcommon.checkRightP() or (gcommon.checkShotKeyP() and n == 1):
					gcommon.sound(gcommon.SOUND_MENUMOVE)
					gcommon.Settings.playerStock += 1
					if gcommon.Settings.playerStock > 99:
						gcommon.Settings.playerStock = 99
				elif gcommon.checkLeftP() or (gcommon.checkShotKeyP() and n == 0):
					gcommon.sound(gcommon.SOUND_MENUMOVE)
					gcommon.Settings.playerStock -= 1
					if gcommon.Settings.playerStock < 1:
						gcommon.Settings.playerStock = 1
			elif self.menuPos == MENU_START_STAGE:
				n = -1
				if self.mouseManager.visible:
					n = gcommon.checkMouseMenuPos(self.startStageRects)
				if gcommon.checkRightP() or (gcommon.checkShotKeyP() and n == 1):
					gcommon.sound(gcommon.SOUND_MENUMOVE)
					gcommon.Settings.startStage += 1
					if gcommon.Settings.startStage > 6:
						gcommon.Settings.startStage = 6
				elif gcommon.checkLeftP() or (gcommon.checkShotKeyP() and n == 0):
					gcommon.sound(gcommon.SOUND_MENUMOVE)
					gcommon.Settings.startStage -= 1
					if gcommon.Settings.startStage < 1:
						gcommon.Settings.startStage = 1

			elif self.menuPos == MENU_GAME_START:
				if gcommon.checkShotKeyRectP(self.menuRects[MENU_GAME_START]):
					gcommon.saveSettings()
					gcommon.sound(gcommon.SOUND_GAMESTART)
					self.state = 1
					self.cnt = 0
			
			elif self.menuPos == MENU_EXIT:
				if gcommon.checkShotKeyRectP(self.menuRects[MENU_EXIT]):
					gcommon.sound(gcommon.SOUND_MENUMOVE)
					gcommon.app.startTitle()

			# if gcommon.checkShotKey():
			# 	gcommon.saveSettings()
			# 	if self.menuPos == MENU_GAME_START:
			# 		gcommon.sound(gcommon.SOUND_GAMESTART)
			# 		self.state = 1
			# 		self.cnt = 0
			# 	elif self.menuPos == MENU_EXIT:
			# 		gcommon.app.startTitle()
		else:
			# GAME START
			if self.cnt > 40:
				gcommon.app.startCustomGame(gcommon.Settings.difficulty, gcommon.Settings.startStage, gcommon.Settings.playerStock)
		self.cnt += 1

	def draw(self):
		pyxel.cls(1)
		gcommon.showTextHCenter(8, "CUSTOM START")
		
		x1 = 48
		x2 = MENU_VALUE_X
		self.setOptionColor(MENU_DIFFCULTY)
		gcommon.showText(x1, self.menuYList[0], "DIFFICULTY")
		text = gcommon.difficultyText[gcommon.Settings.difficulty]
		gcommon.showText(x2, self.menuYList[0], text)
		if MENU_DIFFCULTY == self.menuPos:
			leftMarker = (gcommon.Settings.difficulty == gcommon.DIFFICULTY_NORMAL)
			gcommon.drawLeftMarker(x2 -10, self.menuYList[0], leftMarker)
			gcommon.drawRightMarker(x2 +6*8 + 2, self.menuYList[0], not leftMarker)

		self.setOptionColor(MENU_PLAYER_STOCK)
		gcommon.showText(x1, self.menuYList[1], "PLAYER STOCK")
		gcommon.showText(x2, self.menuYList[1], str(gcommon.Settings.playerStock).rjust(2))
		if MENU_PLAYER_STOCK == self.menuPos:
			gcommon.drawUpDownMarker2(x2 -10, self.menuYList[1], 1, 99, gcommon.Settings.playerStock)

		self.setOptionColor(MENU_START_STAGE)
		gcommon.showText(x1, self.menuYList[2], "START STAGE")
		gcommon.showText(x2, self.menuYList[2], str(gcommon.Settings.startStage).rjust(2))
		if MENU_START_STAGE == self.menuPos:
			gcommon.drawUpDownMarker2(x2 -10, self.menuYList[2], 1, 6, gcommon.Settings.startStage)

		if self.state == 0:
			self.setOptionColor(MENU_GAME_START)
			gcommon.showTextHCenter(self.menuYList[3], "GAME START")
		else:
			if self.cnt & 2 == 0:
				pyxel.pal(7, 8)
			gcommon.showTextHCenter(self.menuYList[3], "GAME START")
			if self.cnt & 2 == 0:
				pyxel.pal()
		
		self.setOptionColor(MENU_EXIT)
		gcommon.showTextHCenter(self.menuYList[4], "EXIT")
		
		gcommon.setBrightness1()
		y = self.menuYList[self.menuPos] -2
		pyxel.blt(16, y, 4, 16, y, 224, 12)
		pyxel.pal()
		if self.mouseManager.visible:
			gcommon.drawMenuCursor()

	def setOptionColor(self, index):
		if index == self.menuPos:
			pyxel.pal()
		else:
			pyxel.pal(7, 12)

#
