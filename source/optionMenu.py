import pyxel
import gcommon

OPTIONMENU_BGM_VOL = 0
OPTIONMENU_SOUND_VOL = 1
OPTIONMENU_EXIT = 2

MENU_VALUE_X = 180

class OptionMenuScene:
	def __init__(self):
		self.menuPos = 0
		self.mouseManager = gcommon.MouseManager()
		self.menuRects = []
		for i in range(3):
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

	def init(self):
		self.menuPos = 0

	def update(self):
		self.mouseManager.update()
		if gcommon.checkUpP():
			gcommon.sound(gcommon.SOUND_MENUMOVE)
			self.menuPos -= 1
			if self.menuPos < 0:
				self.menuPos = 2
		if gcommon.checkDownP():
			gcommon.sound(gcommon.SOUND_MENUMOVE)
			self.menuPos += 1
			if self.menuPos > 2:
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
				gcommon.sound(gcommon.SOUND_MENUMOVE)
				gcommon.Settings.bgmVolume += 1
				if gcommon.Settings.bgmVolume > 10:
					gcommon.Settings.bgmVolume = 10
			elif gcommon.checkLeftP() or (gcommon.checkShotKeyP() and n == 0):
				gcommon.sound(gcommon.SOUND_MENUMOVE)
				gcommon.Settings.bgmVolume -= 1
				if gcommon.Settings.bgmVolume < 0:
					gcommon.Settings.bgmVolume = 0
		elif self.menuPos == OPTIONMENU_SOUND_VOL:
			n = -1
			if self.mouseManager.visible:
				n = gcommon.checkMouseMenuPos(self.seUpDownRects)
			if gcommon.checkRightP() or (gcommon.checkShotKeyP() and n == 1):
				gcommon.Settings.soundVolume = 10
				gcommon.sound(gcommon.SOUND_MENUMOVE)
			elif gcommon.checkLeftP() or (gcommon.checkShotKeyP() and n == 0):
				gcommon.Settings.soundVolume = 0
				gcommon.sound(gcommon.SOUND_MENUMOVE)
		
		# if gcommon.checkRightP():
		# 	gcommon.sound(gcommon.SOUND_MENUMOVE)
		# 	if self.menuPos == OPTIONMENU_BGM_VOL:
		# 		gcommon.Settings.bgmVolume += 1
		# 		if gcommon.Settings.bgmVolume > 10:
		# 			gcommon.Settings.bgmVolume = 10
		# 	elif self.menuPos == OPTIONMENU_SOUND_VOL:
		# 		gcommon.Settings.soundVolume = 10
		# elif gcommon.checkLeftP():
		# 	gcommon.sound(gcommon.SOUND_MENUMOVE)
		# 	if self.menuPos == OPTIONMENU_BGM_VOL:
		# 		gcommon.Settings.bgmVolume -= 1
		# 		if gcommon.Settings.bgmVolume < 0:
		# 			gcommon.Settings.bgmVolume = 0
		# 	elif self.menuPos == OPTIONMENU_SOUND_VOL:
		# 		gcommon.Settings.soundVolume = 0
		
		if self.menuPos == OPTIONMENU_EXIT and gcommon.checkShotKeyRectP(self.menuRects[OPTIONMENU_EXIT]):
			gcommon.sound(gcommon.SOUND_MENUMOVE)
			gcommon.saveSettings()
			gcommon.app.startTitle()

	def draw(self):
		pyxel.cls(1)

		pyxel.pal()
		x1 = 72
		x2 = MENU_VALUE_X
		gcommon.showTextHCenter(8, "OPTION")
		y = 50
		gcommon.setMenuColor(OPTIONMENU_BGM_VOL, self.menuPos)
		gcommon.showText(x1, y, "BGM VOLUME")
		gcommon.showText(x2, y, str(gcommon.Settings.bgmVolume).rjust(2))
		if OPTIONMENU_BGM_VOL == self.menuPos:
			#gcommon.drawUpDownMarker(x2 -10, y)
			gcommon.drawUpDownMarker2(x2 -10, y, 0, 10, gcommon.Settings.bgmVolume)
		y += 20

		gcommon.setMenuColor(OPTIONMENU_SOUND_VOL, self.menuPos)
		gcommon.showText(x1, y, "SE VOLUME")
		se = "ON " if gcommon.Settings.soundVolume > 0 else "OFF"
		gcommon.showText(x2, y, se)
		if OPTIONMENU_SOUND_VOL == self.menuPos:
			#gcommon.drawUpDownMarker(x2 -10, y)
			leftMarker = (gcommon.Settings.soundVolume > 0)
			gcommon.drawLeftMarker(x2 -10, y, leftMarker)
			gcommon.drawRightMarker(x2 +len(se)*8 + 2, y, not leftMarker)
		y += 20
		
		gcommon.setMenuColor(OPTIONMENU_EXIT, self.menuPos)
		gcommon.showTextHCenter(y, "EXIT")
		
		gcommon.setBrightness1()
		pyxel.blt(32, 48 + self.menuPos * 20, 4, 32, 48 + self.menuPos * 20, 192, 12)
		pyxel.pal()

		if self.mouseManager.visible:
			gcommon.drawMenuCursor()
