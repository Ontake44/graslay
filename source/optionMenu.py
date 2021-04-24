import pyxel
import gcommon
from mouseManager import MouseManager
from audio import BGM
from settings import Settings 

OPTIONMENU_BGM_VOL = 0
OPTIONMENU_SOUND_VOL = 1
OPTIONMENU_MOUSE_ENABLED = 2
OPTIONMENU_SCORE_RANKIG = 3
OPTIONMENU_EXIT = 4

MENU_VALUE_X = 180

class OptionMenuScene:
	def __init__(self):
		self.star_pos = 0
		self.menuPos = 0
		self.mouseManager = MouseManager()
		self.menuRects = []
		for i in range(5):
			self.menuRects.append(gcommon.Rect.createWH(
				32, 48 + i * 20, 192, 12))
		# BGM Marker
		self.bgmUpDownRects = [
			gcommon.Rect.createWH(MENU_VALUE_X -10, 50, 8, 8),
			gcommon.Rect.createWH(26 +MENU_VALUE_X -10, 50, 8, 8)
		]
		# SE Marker
		self.seUpDownRects = [
			gcommon.Rect.createWH(MENU_VALUE_X -10, 70, 8, 8),
			gcommon.Rect.createWH(MENU_VALUE_X +8*3+2, 70, 8, 8)
		]
		# Mouse ON/OFF Marker
		self.mouseOnOffRects = [
			gcommon.Rect.createWH(MENU_VALUE_X -10, 90, 8, 8),
			gcommon.Rect.createWH(MENU_VALUE_X +8*3+2, 90, 8, 8)
		]

	def init(self):
		self.menuPos = 0

	def update(self):
		self.star_pos -= 0.25
		if self.star_pos<0:
			self.star_pos += 200
		self.mouseManager.update()
		if gcommon.checkUpP():
			BGM.sound(gcommon.SOUND_MENUMOVE)
			self.menuPos -= 1
			if self.menuPos < 0:
				self.menuPos = 4
		if gcommon.checkDownP():
			BGM.sound(gcommon.SOUND_MENUMOVE)
			self.menuPos += 1
			if self.menuPos > 4:
				self.menuPos = 0

		if self.mouseManager.visible:
			n = gcommon.checkMouseMenuPos(self.menuRects)
			if n != -1:
				self.menuPos = n
		
		if self.menuPos == OPTIONMENU_BGM_VOL:
			n = -1
			if self.mouseManager.visible:
				n = gcommon.checkMouseMenuPos(self.bgmUpDownRects)
			if gcommon.checkRightP() or (gcommon.checkShotKeyP() and n == 1):
				BGM.sound(gcommon.SOUND_MENUMOVE)
				Settings.bgmVolume += 1
				if Settings.bgmVolume > 10:
					Settings.bgmVolume = 10
			elif gcommon.checkLeftP() or (gcommon.checkShotKeyP() and n == 0):
				BGM.sound(gcommon.SOUND_MENUMOVE)
				Settings.bgmVolume -= 1
				if Settings.bgmVolume < 0:
					Settings.bgmVolume = 0
		elif self.menuPos == OPTIONMENU_SOUND_VOL:
			n = -1
			if self.mouseManager.visible:
				n = gcommon.checkMouseMenuPos(self.seUpDownRects)
			if gcommon.checkRightP() or (gcommon.checkShotKeyP() and n == 1):
				Settings.soundVolume = 10
				BGM.sound(gcommon.SOUND_MENUMOVE)
			elif gcommon.checkLeftP() or (gcommon.checkShotKeyP() and n == 0):
				Settings.soundVolume = 0
				BGM.sound(gcommon.SOUND_MENUMOVE)

		elif self.menuPos == OPTIONMENU_MOUSE_ENABLED:
			n = -1
			if self.mouseManager.visible:
				n = gcommon.checkMouseMenuPos(self.mouseOnOffRects)
			if gcommon.checkRightP() or (gcommon.checkShotKeyP() and n == 1):
				Settings.mouseEnabled = True
				BGM.sound(gcommon.SOUND_MENUMOVE)
			elif gcommon.checkLeftP() or (gcommon.checkShotKeyP() and n == 0):
				Settings.mouseEnabled = False
				BGM.sound(gcommon.SOUND_MENUMOVE)

		elif self.menuPos == OPTIONMENU_SCORE_RANKIG and gcommon.checkShotKeyRectP(self.menuRects[OPTIONMENU_SCORE_RANKIG]):
			BGM.sound(gcommon.SOUND_MENUMOVE)
			Settings.saveSettings()
			gcommon.app.startScoreRanking(1)
			#gcommon.app.startEnterPlayerNameScene()

		elif self.menuPos == OPTIONMENU_EXIT and gcommon.checkShotKeyRectP(self.menuRects[OPTIONMENU_EXIT]):
			BGM.sound(gcommon.SOUND_MENUMOVE)
			Settings.saveSettings()
			gcommon.app.startTitle()

	def draw(self):
		pyxel.cls(0)
		self.drawStar()

		pyxel.pal()
		x1 = 72
		x2 = MENU_VALUE_X
		gcommon.showTextHCenter(8, "OPTION")
		y = 50
		gcommon.setMenuColor(OPTIONMENU_BGM_VOL, self.menuPos)
		gcommon.showText(x1, y, "BGM VOLUME")
		gcommon.showText(x2, y, str(Settings.bgmVolume).rjust(2))
		if OPTIONMENU_BGM_VOL == self.menuPos:
			#gcommon.drawUpDownMarker(x2 -10, y)
			gcommon.drawUpDownMarker2(x2 -10, y, 0, 10, Settings.bgmVolume)
		y += 20

		gcommon.setMenuColor(OPTIONMENU_SOUND_VOL, self.menuPos)
		gcommon.showText(x1, y, "SE VOLUME")
		se = "ON " if Settings.soundVolume > 0 else "OFF"
		gcommon.showText(x2, y, se)
		if OPTIONMENU_SOUND_VOL == self.menuPos:
			leftMarker = (Settings.soundVolume > 0)
			gcommon.drawLeftMarker(x2 -10, y, leftMarker)
			gcommon.drawRightMarker(x2 +len(se)*8 + 2, y, not leftMarker)
		y += 20

		gcommon.setMenuColor(OPTIONMENU_MOUSE_ENABLED, self.menuPos)
		gcommon.showText(x1, y, "MOUSE")
		mouseOnOff = "ON " if Settings.mouseEnabled else "OFF"
		gcommon.showText(x2, y, mouseOnOff)
		if OPTIONMENU_MOUSE_ENABLED == self.menuPos:
			leftMarker = (Settings.mouseEnabled == True)
			gcommon.drawLeftMarker(x2 -10, y, leftMarker)
			gcommon.drawRightMarker(x2 +len(se)*8 + 2, y, not leftMarker)
		y += 20

		gcommon.setMenuColor(OPTIONMENU_SCORE_RANKIG, self.menuPos)
		gcommon.showTextHCenter(y, "SCORE RANKING")
		y += 20

		gcommon.setMenuColor(OPTIONMENU_EXIT, self.menuPos)
		gcommon.showTextHCenter(y, "EXIT")
		
		gcommon.setBrightness1()
		pyxel.blt(32, 48 + self.menuPos * 20, 4, 32, 48 + self.menuPos * 20, 192, 12)
		pyxel.pal()

		if self.mouseManager.visible:
			self.mouseManager.drawMenuCursor()

	def drawStar(self):
		for i in range(0,96):
			pyxel.pset(gcommon.star_ary[i][0], int(i*2 +self.star_pos) % 200, gcommon.star_ary[i][1])
