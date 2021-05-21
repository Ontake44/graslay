from typing import get_origin
import pyxel
import gcommon
from mouseManager import MouseManager
from audio import BGM
from settings import Settings 
from drawing import Drawing

MENU_PLAYER_STOCK = 0
MENU_WEAPON_TYPE = 1
MENU_WEAPON_OPTION = 2
MENU_START_STAGE = 3
MENU_GAME_START = 4
MENU_EXIT = 5

MENU_VALUE_X = 172
START_X = 80

class CustomStartMenuScene:
	# とりあえずのステージ選択
	def __init__(self):
		self.star_pos = 0
		oy = 16
		self.menuYList = (50 +oy, 70 +oy, 90 +oy, 110+oy, 130+oy, 158 +oy)
		self.menuPos = 0
		self.state = 0
		self.cnt = 0
		self.mouseManager = MouseManager()
		self.difficulty = Settings.difficulty
		self.stageIndex = 0
		for index, stg in enumerate(gcommon.stageList):
			if stg == Settings.startStage:
				self.stageIndex = index
				break

		self.menuRects = []
		for y in self.menuYList:
			self.menuRects.append(gcommon.Rect.create(
				16, y, 16 +224 -1, y +12-1))
		self.playerStockRects = [
			gcommon.Rect.createWH(MENU_VALUE_X -10, self.menuYList[MENU_PLAYER_STOCK], 8, 8),
			gcommon.Rect.createWH(MENU_VALUE_X -10+26, self.menuYList[MENU_PLAYER_STOCK], 8, 8)
		]
		self.weaponTypeRects = [
			gcommon.Rect.createWH(MENU_VALUE_X -10, self.menuYList[MENU_WEAPON_TYPE], 8, 8),
			gcommon.Rect.createWH(MENU_VALUE_X + 6 * 8 +2, self.menuYList[MENU_WEAPON_TYPE], 8, 8)
		]
		self.multipleRects = [
			gcommon.Rect.createWH(MENU_VALUE_X -10, self.menuYList[MENU_WEAPON_OPTION], 8, 8),
			gcommon.Rect.createWH(MENU_VALUE_X -10+26, self.menuYList[MENU_WEAPON_OPTION], 8, 8)
		]
		self.startStageRects = [
			gcommon.Rect.createWH(MENU_VALUE_X -10, self.menuYList[MENU_START_STAGE], 8, 8),
			gcommon.Rect.createWH(MENU_VALUE_X -10+26, self.menuYList[MENU_START_STAGE], 8, 8)
		]
		self.difficultyRects = [
			gcommon.Rect.createWH(START_X -12, self.menuYList[MENU_GAME_START], 8, 8),
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
				BGM.sound(gcommon.SOUND_MENUMOVE)
				self.menuPos -= 1
				if self.menuPos == MENU_WEAPON_OPTION and Settings.weaponType == gcommon.WeaponType.TYPE_A:
					self.menuPos = MENU_WEAPON_TYPE
				if self.menuPos < 0:
					self.menuPos = 5
			if gcommon.checkDownP():
				BGM.sound(gcommon.SOUND_MENUMOVE)
				self.menuPos += 1
				if self.menuPos == MENU_WEAPON_OPTION and Settings.weaponType == gcommon.WeaponType.TYPE_A:
					self.menuPos = MENU_START_STAGE
				if self.menuPos > 5:
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
					BGM.sound(gcommon.SOUND_MENUMOVE)
					Settings.playerStock += 1
					if Settings.playerStock > 99:
						Settings.playerStock = 99
				elif gcommon.checkLeftP() or (gcommon.checkShotKeyP() and n == 0):
					BGM.sound(gcommon.SOUND_MENUMOVE)
					Settings.playerStock -= 1
					if Settings.playerStock < 1:
						Settings.playerStock = 1

			elif self.menuPos == MENU_START_STAGE:
				n = -1
				if self.mouseManager.visible:
					n = gcommon.checkMouseMenuPos(self.startStageRects)
				if gcommon.checkRightP() or (gcommon.checkShotKeyP() and n == 1):
					BGM.sound(gcommon.SOUND_MENUMOVE)
					self.stageIndex += 1
					if self.stageIndex >= len(gcommon.stageList):
						self.stageIndex = len(gcommon.stageList) -1
				elif gcommon.checkLeftP() or (gcommon.checkShotKeyP() and n == 0):
					BGM.sound(gcommon.SOUND_MENUMOVE)
					self.stageIndex -= 1
					if self.stageIndex < 0:
						self.stageIndex = 0

			elif self.menuPos == MENU_WEAPON_TYPE:
				n = -1
				if self.mouseManager.visible:
					n = gcommon.checkMouseMenuPos(self.weaponTypeRects)
				if gcommon.checkRightP() or (gcommon.checkShotKeyP() and n == 1):
					BGM.sound(gcommon.SOUND_MENUMOVE)
					Settings.weaponType = gcommon.WeaponType.TYPE_B
				elif gcommon.checkLeftP() or (gcommon.checkShotKeyP() and n == 0):
					BGM.sound(gcommon.SOUND_MENUMOVE)
					Settings.weaponType = gcommon.WeaponType.TYPE_A

			elif self.menuPos == MENU_WEAPON_OPTION:
				n = -1
				if self.mouseManager.visible:
					n = gcommon.checkMouseMenuPos(self.multipleRects)
				if gcommon.checkRightP() or (gcommon.checkShotKeyP() and n == 1):
					BGM.sound(gcommon.SOUND_MENUMOVE)
					Settings.multipleCount += 1
					if Settings.multipleCount > 20:
						Settings.multipleCount = 20
				elif gcommon.checkLeftP() or (gcommon.checkShotKeyP() and n == 0):
					BGM.sound(gcommon.SOUND_MENUMOVE)
					Settings.multipleCount -= 1
					if Settings.multipleCount < 0:
						Settings.multipleCount = 0

			elif self.menuPos == MENU_GAME_START:
				n = -1
				if self.mouseManager.visible:
					n = gcommon.checkMouseMenuPos(self.difficultyRects)
				if gcommon.checkRightP() or (gcommon.checkShotKeyP() and n == 1):
					if self.difficulty < 2:
						BGM.sound(gcommon.SOUND_MENUMOVE)
						self.difficulty += 1
				elif gcommon.checkLeftP() or (gcommon.checkShotKeyP() and n == 0):
					if self.difficulty > 0:
						BGM.sound(gcommon.SOUND_MENUMOVE)
						self.difficulty -= 1
				elif gcommon.checkShotKeyP():
					Settings.difficulty = self.difficulty
					Settings.startStage = gcommon.stageList[self.stageIndex]
					Settings.saveSettings()
					BGM.sound(gcommon.SOUND_GAMESTART)
					self.state = 1
					self.cnt = 0
			
			elif self.menuPos == MENU_EXIT:
				if gcommon.checkShotKeyRectP(self.menuRects[MENU_EXIT]):
					Settings.saveSettings()
					BGM.sound(gcommon.SOUND_MENUMOVE)
					gcommon.app.startTitle()
		else:
			# GAME START
			if self.cnt > 40:
				gcommon.app.startCustomGame()
		self.cnt += 1

	def draw(self):
		pyxel.cls(0)
		self.drawStar()
		Drawing.showTextHCenter(32, "CUSTOM START")
		
		x1 = 48
		x2 = MENU_VALUE_X
		x3 = START_X

		idx = 0
		self.setOptionColor(MENU_PLAYER_STOCK)
		Drawing.showText(x1, self.menuYList[MENU_PLAYER_STOCK], "PLAYER STOCK")
		Drawing.showText(x2, self.menuYList[MENU_PLAYER_STOCK], str(Settings.playerStock).rjust(2))
		if MENU_PLAYER_STOCK == self.menuPos:
			Drawing.drawUpDownMarker2(x2 -10, self.menuYList[idx], 1, 99, Settings.playerStock)

		idx += 1
		self.setOptionColor(MENU_WEAPON_TYPE)
		Drawing.showText(x1, self.menuYList[MENU_WEAPON_TYPE], "WEAPON")
		if Settings.weaponType == gcommon.WeaponType.TYPE_A:
			Drawing.showText(x2, self.menuYList[MENU_WEAPON_TYPE], "TYPE A")
		else:
			Drawing.showText(x2, self.menuYList[MENU_WEAPON_TYPE], "TYPE B")
		if MENU_WEAPON_TYPE == self.menuPos:
			typeA = (Settings.weaponType == gcommon.WeaponType.TYPE_A)
			Drawing.drawLeftMarker(x2 -10, self.menuYList[MENU_WEAPON_TYPE], not typeA)
			Drawing.drawRightMarker(x2 +6*8 +2, self.menuYList[MENU_WEAPON_TYPE], typeA)

		if Settings.weaponType == gcommon.WeaponType.TYPE_B:
			self.setOptionColor(MENU_WEAPON_OPTION)
			Drawing.showText(x1, self.menuYList[MENU_WEAPON_OPTION], " MULTIPLE")
			Drawing.showText(x2, self.menuYList[MENU_WEAPON_OPTION], str(Settings.multipleCount).rjust(2))
			if MENU_WEAPON_OPTION == self.menuPos:
				Drawing.drawUpDownMarker2(x2 -10, self.menuYList[MENU_WEAPON_OPTION], 0, 99, Settings.multipleCount)

		idx += 1
		self.setOptionColor(MENU_START_STAGE)
		Drawing.showText(x1, self.menuYList[MENU_START_STAGE], "START STAGE")
		Drawing.showText(x2, self.menuYList[MENU_START_STAGE], gcommon.stageList[self.stageIndex])
		if MENU_START_STAGE == self.menuPos:
			Drawing.drawUpDownMarker2(x2 -10, self.menuYList[MENU_START_STAGE], 0, len(gcommon.stageList)-1, self.stageIndex)
		idx += 1

		text = gcommon.difficultyText[self.difficulty] + " START"
		if self.state == 0:
			if self.state == 0 and self.menuPos == MENU_GAME_START and self.cnt & 16 == 0:
				pyxel.pal(7, 8)
				pyxel.pal(5, 4)
			else:
				self.setOptionColor(MENU_GAME_START)
			Drawing.showText(x3, self.menuYList[MENU_GAME_START], text)
			if MENU_GAME_START == self.menuPos:
				Drawing.drawLeftMarker(x3 -12, self.menuYList[MENU_GAME_START], self.difficulty > 0)
				Drawing.drawRightMarker(x3 +(6+6)*8 + 4, self.menuYList[MENU_GAME_START], self.difficulty < 2)
		else:
			if self.cnt & 2 == 0:
				pyxel.pal(7, 8)
				pyxel.pal(5, 4)
			Drawing.showText(x3, self.menuYList[MENU_GAME_START], text)
		pyxel.pal()
		idx += 1

		# if self.state == 0:
		# 	self.setOptionColor(MENU_GAME_START)
		# 	Drawing.showTextHCenter(self.menuYList[3], "GAME START")
		# else:
		# 	if self.cnt & 2 == 0:
		# 		pyxel.pal(7, 8)
		# 	Drawing.showTextHCenter(self.menuYList[3], "GAME START")
		# 	if self.cnt & 2 == 0:
		# 		pyxel.pal()
		
		self.setOptionColor(MENU_EXIT)
		Drawing.showTextHCenter(self.menuYList[MENU_EXIT], "EXIT")
		
		Drawing.setBrightness1()
		y = self.menuYList[self.menuPos] -2
		pyxel.blt(16, y, 4, 16, y, 224, 12)
		pyxel.pal()
		if self.mouseManager.visible:
			self.mouseManager.drawMenuCursor()

	def setOptionColor(self, index):
		if index == self.menuPos:
			pyxel.pal()
		else:
			pyxel.pal(7, 12)

	def drawStar(self):
		for i in range(0,96):
			pyxel.pset(gcommon.star_ary[i][0], int(i*2 +self.star_pos) % 200, gcommon.star_ary[i][1])

