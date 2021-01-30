import pyxel
import gcommon

OPTIONMENU_BGM_VOL = 0
OPTIONMENU_SOUND_VOL = 1
OPTIONMENU_EXIT = 2

class OptionMenuScene:
	def __init__(self):
		self.menuPos = 0
	
	def init(self):
		self.menuPos = 0

	def update(self):
		if gcommon.checkUpP():
			self.menuPos -= 1
			if self.menuPos < 0:
				self.menuPos = 2
		if gcommon.checkDownP():
			self.menuPos += 1
			if self.menuPos > 2:
				self.menuPos = 0
		
		if gcommon.checkRightP():
			if self.menuPos == OPTIONMENU_BGM_VOL:
				gcommon.Settings.bgmVolume += 1
				if gcommon.Settings.bgmVolume > 10:
					gcommon.Settings.bgmVolume = 10
			elif self.menuPos == OPTIONMENU_SOUND_VOL:
				gcommon.Settings.soundVolume = 10
		elif gcommon.checkLeftP():
			if self.menuPos == OPTIONMENU_BGM_VOL:
				gcommon.Settings.bgmVolume -= 1
				if gcommon.Settings.bgmVolume < 0:
					gcommon.Settings.bgmVolume = 0
			elif self.menuPos == OPTIONMENU_SOUND_VOL:
				gcommon.Settings.soundVolume = 0
		
		if gcommon.checkShotKey() and self.menuPos == OPTIONMENU_EXIT:
			gcommon.saveSettings()
			gcommon.app.startTitle()

	def draw(self):
		pyxel.cls(1)

		pyxel.pal()
		x1 = 72
		x2 = 180
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
		se = "ON" if gcommon.Settings.soundVolume > 0 else "OFF"
		gcommon.showText(x2, y, se)
		if OPTIONMENU_SOUND_VOL == self.menuPos:
			#gcommon.drawUpDownMarker(x2 -10, y)
			leftMarker = (gcommon.Settings.soundVolume > 0)
			gcommon.drawLeftMarker(x2 -12, y, leftMarker)
			gcommon.drawRightMarker(x2 +len(se)*8 + 4, y, not leftMarker)
		y += 20
		
		gcommon.setMenuColor(OPTIONMENU_EXIT, self.menuPos)
		gcommon.showTextHCenter(y, "EXIT")
		
		gcommon.setBrightness1()
		pyxel.blt(32, 48 + self.menuPos * 20, 4, 32, 48 + self.menuPos * 20, 192, 12)
		pyxel.pal()
