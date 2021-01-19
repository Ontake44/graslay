import pyxel
import gcommon

#
#  タイトル表示
#
class TitleScene:
	def __init__(self):
		gcommon.map_y = 0
		self.cnt = 0
		pyxel.image(1).load(0,0,"assets/title.png")
		pyxel.tilemap(0).refimg = 1
		self.menuPos = 0
		self.timer = 0
		self.state = 0
		self.star_pos = 0
	
	def init(self):
		pass

	def update(self):
		if self.cnt >= 6*60:
			self.cnt = 0
		
		if self.state == 0:
			# タイトル表示されていきなりゲーム開始したらダメなので30待つ
			if gcommon.checkShotKey() and self.cnt > 30:
				if self.menuPos == 0:
					gcommon.sound(gcommon.SOUND_GAMESTART)
					self.state = 1
					self.cnt = 0
				elif self.menuPos == 1:
					gcommon.app.startCustomStartMenu()
				elif self.menuPos == 2:
					gcommon.app.startOption()
				elif self.menuPos == 3:
					pyxel.quit()
				#app.startStageClear()
			
			if gcommon.checkUpP():
				self.menuPos = (self.menuPos -1) % 4
			elif gcommon.checkDownP():
				self.menuPos = (self.menuPos +1) % 4
		else:
			# GAME START
			if self.cnt > 40:
				gcommon.app.startGame(gcommon.Defaults.INIT_START_STAGE, gcommon.Defaults.INIT_PLAYER_STOCK)
			
		
		self.cnt+=1

	def draw(self):
		pyxel.cls(0)

		for i in range(0,96):
			pyxel.pset(((int)(gcommon.star_ary[i][0]+self.star_pos))&255, i*2, gcommon.star_ary[i][1])
		
		self.star_pos -= 0.2
		if self.star_pos<0:
			self.star_pos += 255

		pyxel.blt(0, 24, 1, 0, 40, 256, 72, gcommon.TP_COLOR)
		pyxel.pal()
		y = 120
		if self.state == 0:
			gcommon.setMenuColor(0, self.menuPos)
			gcommon.showText(90, y, "NORMAL START")
		else:
			if self.cnt & 2 == 0:
				pyxel.pal(7, 8)
			gcommon.showText(90, y, "NORMAL START")
			if self.cnt & 2 == 0:
				pyxel.pal()

		y += 15
		gcommon.setMenuColor(1, self.menuPos)
		gcommon.showText(90, y, "CUSTOM START")

		y += 15
		gcommon.setMenuColor(2, self.menuPos)
		gcommon.showText(90, y, "OPTION")

		y += 15
		gcommon.setMenuColor(3, self.menuPos)
		gcommon.showText(90, y, "EXIT")

		pyxel.pal()
		pyxel.blt(78, 120 + self.menuPos * 15, 0, 8, 32, 8, 8, gcommon.TP_COLOR)
		
