import pyxel
import math
import random
import gcommon
import enemy

#
#  タイトル表示
#
class TitleScene:
	colorTable1 = (3, 4, 8, 9, 10, 11, 13, 14, 15)
	colorTable2 = (2, 1, 5, 6, 7, 12)
	colorTable1a = (1, 5, 5, 12, 12, 6, 6, 7, 7)
	colorTable3 = (
		((2,1),(1,5),(5,12),(12,6),(6,7)),
		((2,5),(1,12),(5,6),(12,7),(6,7)),
		((2,12),(1,6),(5,7),(12,7),(6,7)),
		((2,6),(1,7),(5,7),(12,7),(6,7)),
		((2,7),(1,7),(5,7),(12,7),(6,7)),
	)
	def __init__(self):
		gcommon.map_y = 0
		self.cnt = 0
		pyxel.image(1).load(0,0,"assets/title.png")
		pyxel.tilemap(0).refimg = 1
		self.menuPos = 0
		self.timer = 0
		# 0 - タイトルデモ
		# 100 メニュー選択
		# 101 ゲーム開始
		self.state = 0
		self.star_pos = 0
		self.subState = 0
		self.subCnt = 0
		self.rnd = gcommon.ClassicRand()
		self.py = 0
		self.ey = 24
		self.cntLimit = 70
		self.objs = []

	def init(self):
		pass

	def update(self):
		self.star_pos -= 0.2
		if self.star_pos<0:
			self.star_pos += 255

		if self.state < 100:
			self.updateDemo()	
		else:
			self.update100()
		newObjs = []
		for obj in self.objs:
			if obj.removeFlag == False:
				obj.update()
				newObjs.append(obj)
		self.objs = newObjs

	def updateDemo(self):
		if self.state == 0:
			self.py += 0.125
			if self.subCnt >= self.cntLimit:
				self.subState += 1
				self.cntLimit -= 10
				self.subCnt = 0
				if self.subState == 9:
					self.state = 1
					self.subCnt = 0
					self.cnt = 0
		elif self.state == 1:
			# ちょっと待ち
			if self.cnt > 1:
				self.state = 2
				self.subState = 0
				self.subCnt = 0
				self.cnt = 0
		elif self.state == 2:
			# 明るくなる
			if self.subCnt > 3:
				self.subState += 1
				self.subCnt = 0
				if self.subState == len(TitleScene.colorTable3):
					self.subState = len(TitleScene.colorTable3)-1
					self.state = 3
		elif self.state == 3:
			# 戻る
			if self.subCnt > 3:
				self.subState -= 1
				self.subCnt = 0
				if self.subState == 0:
					self.state = 4
					self.cnt = 0
		elif self.state == 4:
			self.objs.append(enemy.Particle1(220 - self.cnt * 10, 64, 0))
			# 文字がせり出す
			if self.cnt > 20:
				self.state = 100
		self.subCnt += 1
		self.cnt = (self.cnt +1) & 1023
		if gcommon.checkShotKeyP():
			self.state = 100
			self.cnt = 0
			self.update100()
	
	def update100(self):
		if self.state == 100:
			# タイトル表示されていきなりゲーム開始したらダメなので30待つ
			if gcommon.checkShotKey() and self.cnt > 30:
				if self.menuPos == 0:
					gcommon.sound(gcommon.SOUND_GAMESTART)
					self.state = 101
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
		elif self.state == 101:
			# GAME START
			if self.cnt > 40:
				gcommon.app.startGame(gcommon.Defaults.INIT_START_STAGE, gcommon.Defaults.INIT_PLAYER_STOCK)
			
		
		self.cnt += 1
		if self.cnt >= 6*60:
			self.cnt = 0

	def draw(self):
		pyxel.cls(0)
		if self.state < 100:
			self.drawDemo()
		else:
			self.draw100()
		for obj in self.objs:
			if obj.removeFlag == False:
				obj.draw()

	def drawDemo(self):
		pyxel.cls(0)
		pyxel.pal()
		for i in range(0,96):
			pyxel.pset(((int)(gcommon.star_ary[i][0]+self.star_pos))&255, i*2, gcommon.star_ary[i][1])
		if self.state == 0:
			color = TitleScene.colorTable1a[self.subState]
			# 文字中
			n = int(self.rnd.rand() % (30 -self.subState*3))
			for c in TitleScene.colorTable2:
				if n == 0:
					pyxel.pal(c, color)
				else:
					pyxel.pal(c, 0)
			
			# 文字枠
			for c in TitleScene.colorTable1:
				pyxel.pal(c, 0)
			if self.cnt & 1 == 0:
				cc = self.rnd.rand() % len(TitleScene.colorTable1)
				for i in range(self.subState+1):
					pyxel.pal(TitleScene.colorTable1[(cc+i) % len(TitleScene.colorTable1)], color)
			pyxel.blt(0, 24 +36 -self.py, 1, 0, 40, 256, 80, 0)
		elif self.state == 1:
			self.drawNormal()
		elif self.state == 2 or self.state == 3:
			pyxel.pal()
			# 文字枠
			for c in TitleScene.colorTable1:
				pyxel.pal(c, 7)
			table = TitleScene.colorTable3[self.subState]
			for t in table:
				pyxel.pal(t[0], t[1])
			pyxel.blt(0, 24, 1, 0, 40, 256, 80, 0)
		elif self.state == 4:
			self.drawNormal()
			self.drawText(False, self.cnt/20)
		else:
			self.drawNormal()

	def drawNormal(self):
		pyxel.pal()
		# 文字枠
		for c in TitleScene.colorTable1:
			pyxel.pal(c, 7)
		pyxel.pal(2, 0)
		pyxel.blt(0, 24, 1, 0, 40, 256, 80, 0)

	def draw100(self):
		for i in range(0,96):
			pyxel.pset(((int)(gcommon.star_ary[i][0]+self.star_pos))&255, i*2, gcommon.star_ary[i][1])
		
		self.drawNormal()
		# pyxel.pal()
		# y = 120
		# if self.state == 100:
		# 	gcommon.setMenuColor(0, self.menuPos)
		# 	gcommon.showText(90, y, "NORMAL START")
		# else:
		# 	if self.cnt & 2 == 0:
		# 		pyxel.pal(7, 8)
		# 	gcommon.showText(90, y, "NORMAL START")
		# 	if self.cnt & 2 == 0:
		# 		pyxel.pal()

		# y += 15
		# gcommon.setMenuColor(1, self.menuPos)
		# gcommon.showText(90, y, "CUSTOM START")

		# y += 15
		# gcommon.setMenuColor(2, self.menuPos)
		# gcommon.showText(90, y, "OPTION")

		# y += 15
		# gcommon.setMenuColor(3, self.menuPos)
		# gcommon.showText(90, y, "EXIT")
		self.drawText(self.state == 101 and self.cnt & 2 == 0, 1.0)


		pyxel.pal()
		pyxel.blt(78, 120 + self.menuPos * 15, 0, 8, 32, 8, 8, gcommon.TP_COLOR)
		
	def drawText(self, startFlag, rate):
		pyxel.pal()
		y = 120
		if startFlag:
			pyxel.pal(7, 8)
		else:
			gcommon.setMenuColor(0, self.menuPos)
		gcommon.showTextRate(90, y, "NORMAL START", rate)
		if startFlag:
			pyxel.pal()

		y += 15
		gcommon.setMenuColor(1, self.menuPos)
		gcommon.showTextRate(90, y, "CUSTOM START", rate)

		y += 15
		gcommon.setMenuColor(2, self.menuPos)
		gcommon.showTextRate(90, y, "OPTION", rate)

		y += 15
		gcommon.setMenuColor(3, self.menuPos)
		gcommon.showTextRate(90, y, "EXIT", rate)

		pyxel.pal()

