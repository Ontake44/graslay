import pyxel
import gcommon

MENU_PLAYER_STOCK = 0
MENU_START_STAGE = 1
MENU_GAME_START = 2
MENU_EXIT = 3

MENU_VALUE_X = 180
START_X = 80

class CustomStartMenuScene:
	def __init__(self):
		self.star_pos = 0
		oy = 16
		self.menuYList = (50 +oy, 70 +oy, 90 +oy, 118 +oy)
		self.menuPos = 0
		self.state = 0
		self.cnt = 0
		self.mouseManager = gcommon.MouseManager()
		self.menuRects = []
		for y in self.menuYList:
			self.menuRects.append(gcommon.Rect.create(
				16, y, 16 +224 -1, y +12-1))
		self.playerStockRects = [
			gcommon.Rect.createWH(MENU_VALUE_X -10, self.menuYList[0], 8, 8),
			gcommon.Rect.createWH(MENU_VALUE_X -10+26, self.menuYList[0], 8, 8)
		]
		self.startStageRects = [
			gcommon.Rect.createWH(MENU_VALUE_X -10, self.menuYList[1], 8, 8),
			gcommon.Rect.createWH(MENU_VALUE_X -10+26, self.menuYList[1], 8, 8)
		]
		self.difficultyRects = [
			gcommon.Rect.createWH(START_X -12, self.menuYList[2], 8, 8),
			gcommon.Rect.createWH(START_X +(6+6)*8 + 4, self.menuYList[2], 8, 8),
		]

	def init(self):
		self.menuPos = 0

	def update(self):
		self.star_pos -= 0.25
		if self.star_pos<0:
			self.star_pos += 200
		self.mouseManager.update()
		if self.cnt >= 6*60:
			self.cnt = 0
		if self.state == 0:
			if gcommon.checkUpP():
				gcommon.sound(gcommon.SOUND_MENUMOVE)
				self.menuPos -= 1
				if self.menuPos < 0:
					self.menuPos = 3
			if gcommon.checkDownP():
				gcommon.sound(gcommon.SOUND_MENUMOVE)
				self.menuPos += 1
				if self.menuPos > 3:
					self.menuPos = 0
			
			if self.mouseManager.visible:
				n = gcommon.checkMouseMenuPos(self.menuRects)
				if n != -1:
					self.menuPos = n

			if self.menuPos == MENU_PLAYER_STOCK:
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
				n = -1
				if self.mouseManager.visible:
					n = gcommon.checkMouseMenuPos(self.difficultyRects)
				if gcommon.checkRightP() or (gcommon.checkShotKeyP() and n == 1):
					gcommon.Settings.difficulty = gcommon.DIFFICULTY_NORMAL
					gcommon.sound(gcommon.SOUND_MENUMOVE)
				elif gcommon.checkLeftP() or (gcommon.checkShotKeyP() and n == 0):
					gcommon.Settings.difficulty = gcommon.DIFFICULTY_EASY
					gcommon.sound(gcommon.SOUND_MENUMOVE)
				elif gcommon.checkShotKeyP():
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
		pyxel.cls(0)
		self.drawStar()
		gcommon.showTextHCenter(32, "CUSTOM START")
		
		x1 = 48
		x2 = MENU_VALUE_X
		x3 = START_X

		idx = 0
		self.setOptionColor(MENU_PLAYER_STOCK)
		gcommon.showText(x1, self.menuYList[idx], "PLAYER STOCK")
		gcommon.showText(x2, self.menuYList[idx], str(gcommon.Settings.playerStock).rjust(2))
		if MENU_PLAYER_STOCK == self.menuPos:
			gcommon.drawUpDownMarker2(x2 -10, self.menuYList[idx], 1, 99, gcommon.Settings.playerStock)
		
		idx += 1
		self.setOptionColor(MENU_START_STAGE)
		gcommon.showText(x1, self.menuYList[idx], "START STAGE")
		gcommon.showText(x2, self.menuYList[idx], str(gcommon.Settings.startStage).rjust(2))
		if MENU_START_STAGE == self.menuPos:
			gcommon.drawUpDownMarker2(x2 -10, self.menuYList[idx], 1, 6, gcommon.Settings.startStage)
		idx += 1

		text = gcommon.difficultyText[gcommon.Settings.difficulty] + " START"
		if self.state == 0:
			if self.state == 0 and self.menuPos == MENU_GAME_START and self.cnt & 16 == 0:
				pyxel.pal(7, 8)
				pyxel.pal(5, 4)
			else:
				self.setOptionColor(MENU_GAME_START)
			gcommon.showText(x3, self.menuYList[idx], text)
			if MENU_GAME_START == self.menuPos:
				leftMarker = (gcommon.Settings.difficulty == gcommon.DIFFICULTY_NORMAL)
				gcommon.drawLeftMarker(x3 -12, self.menuYList[idx], leftMarker)
				gcommon.drawRightMarker(x3 +(6+6)*8 + 4, self.menuYList[idx], not leftMarker)
		else:
			if self.cnt & 2 == 0:
				pyxel.pal(7, 8)
				pyxel.pal(5, 4)
			gcommon.showText(x3, self.menuYList[idx], text)
		pyxel.pal()
		idx += 1

		# if self.state == 0:
		# 	self.setOptionColor(MENU_GAME_START)
		# 	gcommon.showTextHCenter(self.menuYList[3], "GAME START")
		# else:
		# 	if self.cnt & 2 == 0:
		# 		pyxel.pal(7, 8)
		# 	gcommon.showTextHCenter(self.menuYList[3], "GAME START")
		# 	if self.cnt & 2 == 0:
		# 		pyxel.pal()
		
		self.setOptionColor(MENU_EXIT)
		gcommon.showTextHCenter(self.menuYList[idx], "EXIT")
		
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

	def drawStar(self):
		for i in range(0,96):
			pyxel.pset(gcommon.star_ary[i][0], int(i*2 +self.star_pos) % 200, gcommon.star_ary[i][1])

