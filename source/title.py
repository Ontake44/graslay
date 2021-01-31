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
	# 文字内側が光る
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
		# 200 ゲーム開始
		self.state = 0
		self.star_pos = 0
		self.subState = 0
		self.subCnt = 0
		self.rnd = gcommon.ClassicRand()
		self.py = 0
		self.ey = 24
		self.cntLimit = 70
		self.objs = []
		self.difficulty = gcommon.Settings.difficulty
		self.credits = gcommon.Settings.credits

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
			self.objs.append(enemy.Particle1(220 - self.cnt * 10, 64, 0, 8, 50))
			# 文字がせり出す
			if self.cnt > 20:
				self.state = 100
		self.subCnt += 1
		self.cnt = (self.cnt +1) & 1023
		if gcommon.checkShotKeyP():
			self.state = 100
			self.cnt = 0
	
	# メニュー処理があるupdate
	def update100(self):
		if self.state >= 100 and self.state < 200:
			if gcommon.checkShotKeyP():		# and self.cnt > 30:
				if self.menuPos == 0:
					gcommon.sound(gcommon.SOUND_GAMESTART)
					# ここですぐにはゲームスタートしない
					self.state = 200
					self.cnt = 0
				elif self.menuPos == 1:
					gcommon.app.startCustomStartMenu()
				elif self.menuPos == 2:
					gcommon.app.startOption()
				elif self.menuPos == 3:
					pyxel.quit()
				#app.startStageClear()
			
			if self.menuPos == 0:
				if gcommon.checkLeftP():
					gcommon.sound(gcommon.SOUND_MENUMOVE)
					self.difficulty = gcommon.DIFFICULTY_EASY
				elif gcommon.checkRightP():
					gcommon.sound(gcommon.SOUND_MENUMOVE)
					self.difficulty = gcommon.DIFFICULTY_NORMAL
			if gcommon.checkUpP():
				gcommon.sound(gcommon.SOUND_MENUMOVE)
				self.menuPos = (self.menuPos -1) % 4
			elif gcommon.checkDownP():
				gcommon.sound(gcommon.SOUND_MENUMOVE)
				self.menuPos = (self.menuPos +1) % 4
		if self.state == 102:
			# 明るくなる
			if self.subCnt > 3:
				self.subState += 1
				self.subCnt = 0
				if self.subState == len(TitleScene.colorTable3):
					self.subState = len(TitleScene.colorTable3)-1
					self.state = 103
			self.subCnt += 1
		elif self.state == 103:
			# 戻る
			if self.subCnt > 3:
				self.subState -= 1
				self.subCnt = 0
				if self.subState == 0:
					self.state = 100
					self.cnt = 0
			self.subCnt += 1
		elif self.state == 200:
			# GAME START
			if self.cnt > 40:
				gcommon.app.startNormalGame(self.difficulty)
			
		self.cnt += 1
		if self.cnt >= 10*60:
			self.cnt = 0
			if self.state == 100:
				self.state = 102
				self.subState = 0
				self.subCnt = 0

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
			self.drawTitleNormal()
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
			self.drawTitleNormal()
			self.drawMenu(False, self.cnt/20)
		else:
			self.drawTitleNormal()

	# タイトル通常描画
	def drawTitleNormal(self):
		pyxel.pal()
		# 文字枠
		for c in TitleScene.colorTable1:
			pyxel.pal(c, 7)
		pyxel.pal(2, 0)
		pyxel.blt(0, 24, 1, 0, 40, 256, 80, 0)

	def draw100(self):
		for i in range(0,96):
			pyxel.pset(((int)(gcommon.star_ary[i][0]+self.star_pos))&255, i*2, gcommon.star_ary[i][1])
		
		if self.state in (100,200):
			self.drawTitleNormal()
		elif self.state == 102 or self.state == 103:
			pyxel.pal()
			# 文字枠
			for c in TitleScene.colorTable1:
				pyxel.pal(c, 7)
			table = TitleScene.colorTable3[self.subState]
			for t in table:
				pyxel.pal(t[0], t[1])
			pyxel.blt(0, 24, 1, 0, 40, 256, 80, 0)		# pyxel.pal()
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
		self.drawMenu(self.state == 200 and self.cnt & 2 == 0, 1.0)

		pyxel.text(200, 188, "CREDIT(S) "  +str(self.credits), 7)

		pyxel.pal()
		#pyxel.blt(78, 120 + self.menuPos * 15, 0, 8, 32, 8, 8, gcommon.TP_COLOR)
		
	def drawMenu(self, startFlag, rate):
		pyxel.pal()
		y = 120
		if startFlag:
			pyxel.pal(7, 8)
		else:
			gcommon.setMenuColor(0, self.menuPos)
		text = gcommon.difficultyText[self.difficulty] + " START"
		gcommon.showTextRateHCenter(y, text, rate)
		if self.menuPos == 0:
			leftMarker = (self.difficulty == gcommon.DIFFICULTY_NORMAL)
			gcommon.drawLeftMarker(120 -len(text)*4 -4, y, leftMarker)
			gcommon.drawRightMarker(128 +len(text)*4 + 4, y, not leftMarker)
		if startFlag:
			pyxel.pal()

		y += 15
		gcommon.setMenuColor(1, self.menuPos)
		gcommon.showTextRateHCenter(y, "CUSTOM START", rate)

		y += 15
		gcommon.setMenuColor(2, self.menuPos)
		gcommon.showTextRateHCenter(y, "OPTION", rate)

		y += 15
		gcommon.setMenuColor(3, self.menuPos)
		gcommon.showTextRateHCenter(y, "EXIT", rate)

		gcommon.setBrightness1()
		pyxel.blt(48, 118 + self.menuPos * 15, 4, 48, 118 + self.menuPos * 15, 160, 12)
		pyxel.pal()

