import pyxel
import math
import random
import gcommon
import enemy
from settings import Settings
from audio import BGM
from mouseManager import MouseManager
from drawing import Drawing

TITLEMENU_START = 0
TITLEMENU_CUSTOMSTART = 1
TITLEMENU_BOSSRUSHSTART = 2
TITLEMENU_OPTION = 3
TITLEMENU_EXIT = 4

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
	polyPoints = [[0,0],[24,0],[0,72],[-24,72]]

	title_y = 16
	menu_top_y = 105

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
		self.difficulty = Settings.difficulty
		self.credits = Settings.credits
		self.mouseManager = MouseManager()
		self.menuRects = []
		for i in range(5):
			self.menuRects.append(gcommon.Rect.create(
				48, __class__.menu_top_y -2 + i * 15,  48 +160-1, __class__.menu_top_y -2 + i * 15 + 12 -1))
		self.difficultyRects = [
			gcommon.Rect.createWH(128 -8 -48 -4, 120, 8, 8),
			gcommon.Rect.createWH(128 +48 +4, 120, 8, 8),
		]


	def init(self):
		BGM.play(BGM.TITLE)

	def update(self):
		self.star_pos -= 0.25
		if self.star_pos<0:
			self.star_pos += 200

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
			if self.cnt > 180:
				self.cnt = 0
				self.state = 1
		elif self.state == 1:
			self.py += 0.15
			#self.py += 0.5
			if self.subCnt >= self.cntLimit:
				self.subState += 1
				self.cntLimit = int(self.cntLimit * 0.8)
				self.subCnt = 0
				if self.subState == 9:
					self.state = 2
					self.subCnt = 0
					self.cnt = 0
		elif self.state == 2:
			# ちょっと待ち
			if self.cnt > 1:
				self.state = 3
				self.subState = 0
				self.subCnt = 0
				self.cnt = 0
		elif self.state == 3:
			# 明るくなる
			if self.subCnt > 3:
				self.subState += 1
				self.subCnt = 0
				if self.subState == len(TitleScene.colorTable3):
					self.subState = len(TitleScene.colorTable3)-1
					self.state = 4
		elif self.state == 4:
			# 戻る
			if self.subCnt > 3:
				self.subState -= 1
				self.subCnt = 0
				if self.subState == 0:
					self.state = 5
					self.cnt = 0
		elif self.state == 5:
			if self.subCnt > 32:
				self.state = 6
				self.cnt = 0
		elif self.state == 6:
			#self.objs.append(enemy.Particle1(220 - self.cnt * 10, 60, 0, 8, 50))
			# 文字がせり出す
			if self.cnt > 20:
				self.setUpdate100()
				return
		self.subCnt += 1
		self.cnt = (self.cnt +1) & 1023
		if gcommon.checkShotKeyP():
			self.setUpdate100()
	
	# メニュー処理へ移行
	def setUpdate100(self):
		self.state = 100
		self.cnt = 0

	# メニュー処理があるupdate
	def update100(self):
		self.mouseManager.update()
		if self.state >= 100 and self.state < 200:
			
			if self.mouseManager.visible:
				n = gcommon.checkMouseMenuPos(self.menuRects)
				if n != -1:
					self.menuPos = n

			if gcommon.checkUpP():
				BGM.sound(gcommon.SOUND_MENUMOVE)
				self.menuPos = (self.menuPos -1) % 5
			elif gcommon.checkDownP():
				BGM.sound(gcommon.SOUND_MENUMOVE)
				self.menuPos = (self.menuPos +1) % 5
			elif pyxel.btnp(pyxel.KEY_T):
				gcommon.app.startStageSelect()
				return
			
			if self.menuPos == TITLEMENU_START:
				n = -1
				if self.mouseManager.visible:
					n = gcommon.checkMouseMenuPos(self.difficultyRects)
				if gcommon.checkLeftP() or (gcommon.checkShotKeyP() and n == 0):
					if self.difficulty > 0:
						BGM.sound(gcommon.SOUND_MENUMOVE)
						self.difficulty -= 1
					return
				elif gcommon.checkRightP() or (gcommon.checkShotKeyP() and n == 1):
					if self.difficulty < 2:
						BGM.sound(gcommon.SOUND_MENUMOVE)
						self.difficulty += 1
					return
				elif gcommon.checkShotKeyRectP(self.menuRects[TITLEMENU_START]):
					BGM.stop()
					BGM.sound(gcommon.SOUND_GAMESTART)
					# ここですぐにはゲームスタートしない
					self.state = 200
					self.cnt = 0
					return
			elif self.menuPos == TITLEMENU_CUSTOMSTART:
				if gcommon.checkShotKeyRectP(self.menuRects[TITLEMENU_CUSTOMSTART]):
					BGM.sound(gcommon.SOUND_MENUMOVE)
					gcommon.app.startCustomStartMenu()
					return
			elif self.menuPos == TITLEMENU_BOSSRUSHSTART:
				if gcommon.checkShotKeyRectP(self.menuRects[TITLEMENU_BOSSRUSHSTART]):
					BGM.sound(gcommon.SOUND_MENUMOVE)
					gcommon.app.startBossRushStartMenu()
					return
			elif self.menuPos == TITLEMENU_OPTION:
				if gcommon.checkShotKeyRectP(self.menuRects[TITLEMENU_OPTION]):
					BGM.sound(gcommon.SOUND_MENUMOVE)
					gcommon.app.startOption()
					return
			elif self.menuPos == TITLEMENU_EXIT:
				if gcommon.checkShotKeyRectP(self.menuRects[TITLEMENU_EXIT]):
					pyxel.quit()

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
					self.state = 104
					self.cnt = 0
					return
			self.subCnt += 1
		elif self.state == 104:
			if self.subCnt > 32:
				self.state = 100
				self.cnt = 0
				return
			self.subCnt += 1
		elif self.state == 200:
			# GAME START
			if self.cnt > 40:
				gcommon.app.startNormalGame(self.difficulty)
			
		self.cnt += 1
		if self.cnt >= 5*60:
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

	def drawStar(self):
		for i in range(0,96):
			pyxel.pset(gcommon.star_ary[i][0], int(i*2 +self.star_pos) % 200, gcommon.star_ary[i][1])

	def drawDemo(self):
		pyxel.cls(0)
		pyxel.pal()
		self.drawStar()
		if self.state == 0:
			pass
		elif self.state == 1:
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
			w = (10 -self.subState)
			for i in range(80):
				pyxel.blt(((self.rnd.rand() % w) -w/2) * 3, __class__.title_y +36 -self.py +i, 1, 0, 40 +i, 256, 1, 0)
		elif self.state == 2:
			self.drawTitleNormal()
		elif self.state == 3 or self.state == 4:
			pyxel.pal()
			# 文字枠
			for c in TitleScene.colorTable1:
				pyxel.pal(c, 7)
			table = TitleScene.colorTable3[self.subState]
			for t in table:
				pyxel.pal(t[0], t[1])
			pyxel.blt(0, __class__.title_y, 1, 0, 40, 256, 80, 0)
		elif self.state == 5:
			self.drawTitleNormal()
			self.drawFlash(self.subCnt*8, __class__.title_y)
		elif self.state == 6:
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
		pyxel.blt(0, __class__.title_y, 1, 0, 40, 256, 80, 0)

	def draw100(self):
		self.drawStar()
		
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
			pyxel.blt(0, __class__.title_y, 1, 0, 40, 256, 80, 0)		# pyxel.pal()
		elif self.state == 104:
			self.drawTitleNormal()
			self.drawFlash(self.subCnt*8, 32)
			
		self.drawMenu(self.state == 200, 1.0)

		pyxel.text(200, 188, "CREDIT(S) "  +str(self.credits), 7)
		pyxel.blt(10, 186, 0, 88, 120, 8, 8, 0)
		pyxel.text(20, 188, "2021 ONTAKE44", 7)

		Drawing.showTextHCentor2(188, "VER " + gcommon.VERSION , 7)

		pyxel.pal()
		if self.mouseManager.visible:
			self.mouseManager.drawMenuCursor()
		#pyxel.blt(78, 120 + self.menuPos * 15, 0, 8, 32, 8, 8, gcommon.TP_COLOR)
		
	def drawFlash(self, x, y):
		pyxel.pal()
		for c in range(1, 15):
			pyxel.pal(c, 7)
		#pyxel.blt(self.subCnt*8, 24, 4, self.subCnt*8, 24, 40, 80, 0)
		Drawing.drawPolygonSystemImage(gcommon.getShitPoints([x, y], TitleScene.polyPoints))
		pyxel.pal()

	def drawMenu(self, startFlag, rate):
		pyxel.pal()
		y = __class__.menu_top_y
		if rate < 1.0:
			gcommon.setMenuColor(0, -1)
		else:
			if (startFlag and self.cnt & 2 == 0) or (startFlag == False and self.menuPos == 0 and self.cnt & 16 == 0):
				pyxel.pal(7, 8)
				pyxel.pal(5, 4)
			else:
				gcommon.setMenuColor(0, self.menuPos)
		text = gcommon.difficultyText[self.difficulty] + " START"
		Drawing.showTextRateHCenter(y, text, rate)
		if rate == 1.0 and self.menuPos == 0:
			Drawing.drawLeftMarker(128 -8 -48 -4, y, self.difficulty > 0)
			Drawing.drawRightMarker(128 +48 + 4, y, self.difficulty < 2)
		pyxel.pal()

		y += 15
		gcommon.setMenuColor(1, self.menuPos)
		Drawing.showTextRateHCenter(y, "CUSTOM START", rate)

		y += 15
		gcommon.setMenuColor(2, self.menuPos)
		Drawing.showTextRateHCenter(y, "BOSS RUSH START", rate)

		y += 15
		gcommon.setMenuColor(3, self.menuPos)
		Drawing.showTextRateHCenter(y, "OPTION", rate)

		y += 15
		gcommon.setMenuColor(4, self.menuPos)
		Drawing.showTextRateHCenter(y, "EXIT", rate)

		if rate == 1.0:
			Drawing.setBrightness1()
			pyxel.blt(48, __class__.menu_top_y -2 + self.menuPos * 15, pyxel.screen, 48, __class__.menu_top_y -2 + self.menuPos * 15, 160, 12)
			pyxel.pal()

