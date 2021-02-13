import pyxel
import math
import random
import gcommon
import enemy

# 発艦シーン
class LaunchScene:
	lightPalTable = (5, 5, 5, 5, 5, 4, 8, 14, 8, 4)
	def __init__(self):
		self.state = 0
		self.x = 256	# -256 -216
		self.targetX = -16
		self.y = gcommon.MYSHIP_START_Y +12  -50
		self.y2 = self.y
		self.dx = 0	#3
		#self.dy = -2
		self.mx = 80
		self.my = self.y + 50
		self.mdx = 0
		self.afterBurner = 0
		self.cnt = 0
		self.objs = []
		gcommon.BGM.play(gcommon.BGM.LAUNCH)

	def init(self):
		pyxel.image(1).load(0,0,"assets/launch1.png")
		pyxel.image(2).load(0,0,"assets/launch2.png")

	def update(self):
		gcommon.star_pos -= 0.2
		if gcommon.star_pos<0:
			gcommon.star_pos += 255

		if self.state == 0:
			#self.x += self.dx
			self.dx = (self.targetX - self.x) * 0.075
			if self.dx < -2:
				self.dx = -2 
			elif abs(self.dx) < 0.1: 
				self.nextState()
				return
			self.x += self.dx
			gcommon.star_pos += self.dx
			#if self.x > -120:
			#	self.nextState()
			#if self.y <gcommon.MYSHIP_START_Y  -50:
			#	self.nextState()
		elif self.state == 1:
			self.wx = self.x + 116
			self.wy = self.y +50
			self.nextState()
		elif self.state == 2:
			# 自機発艦準備
			if (self.y + 50+12) > self.my:
				self.my += 0.25
				self.y2 += 0.25
			if self.cnt > 60 and self.cnt < 90:
				self.afterBurner = 1
				gcommon.sound(gcommon.SOUND_AFTER_BURNER)
			elif self.cnt >= 90:
				self.nextState()
				self.mdx = 1
		elif self.state == 3:
			# 発艦
			self.x += self.dx
			gcommon.star_pos += self.dx
			if self.dx > -3:
				self.dx -= 0.25
			self.mx += self.mdx
			if self.cnt > 90:
				self.afterBurner = 2
				self.mdx -= 0.01
			if self.cnt & 7 == 0 and self.mdx > 0 and self.mx < 150:
				self.objs.append(enemy.Particle1(self.mx, self.my+10, math.pi +math.pi/8, 8, 50))

			if self.mdx <= -1.5:
				self.nextState()
		elif self.state == 4:
			self.x += -3
			
			self.dx = (gcommon.MYSHIP_START_X - self.mx) * 0.1
			if self.dx < -3:
				self.dx = -3
			gcommon.star_pos += self.dx
			self.mdx = (gcommon.MYSHIP_START_X - self.mx) * 0.1
			if self.mdx < -1.5:
				self.mdx = -1.5
			self.mx += self.mdx
			if int(self.mx) == gcommon.MYSHIP_START_X:
				gcommon.app.startMainGame()

		newObjs = []
		for obj in self.objs:
			if obj.removeFlag == False:
				obj.update()
				newObjs.append(obj)
		self.objs = newObjs

		self.cnt += 1

	def nextState(self):
		self.state += 1
		self.cnt = 0

	def setLightPal(self):
		pyxel.pal(11, LaunchScene.lightPalTable[(self.cnt>>3) % len(LaunchScene.lightPalTable)])

	def draw(self):
		pyxel.cls(0)
		gcommon.drawStar(gcommon.star_pos)

		# 自機
		if self.state >= 2:
			pyxel.blt(self.mx, self.my, 0, 0, 0, 24, 16, gcommon.TP_COLOR)

			if self.afterBurner == 1:
				if self.cnt % 2 == 0:
					pyxel.blt(self.mx-32, self.my+4, 0, 72, 8, 32, 8, gcommon.TP_COLOR)
			elif self.afterBurner == 2:
				if self.cnt % 2 == 0:
					pyxel.blt(self.mx-32, self.my+4, 0, 120, 8, 32, 8, gcommon.TP_COLOR)

		# 上半分
		if self.x > -512:
			self.setLightPal()
			pyxel.blt(self.x, self.y, 1, 0, 0, 256, 64, gcommon.TP_COLOR)
			pyxel.blt(self.x +256, self.y, 1, 0, 96, 216, 64, gcommon.TP_COLOR)
			pyxel.blt(self.x, self.y+64, 1, 0, 64, 80, 32, gcommon.TP_COLOR)
			pyxel.pal()

		if self.x > -512:
			# 下半分
			self.setLightPal()
			pyxel.blt(self.x, self.y2, 2, 0, 0, 256, 96, gcommon.TP_COLOR)
			pyxel.blt(self.x +256, self.y2, 2, 0, 96, 216, 96, gcommon.TP_COLOR)
			pyxel.pal()

			# バーニア
			if self.cnt % 2 == 0:
				sx = 72 if self.cnt % 4 == 0 else 120
				pyxel.blt(gcommon.sint(self.x -27), self.y+36, 0, sx, 8, 32, 8, gcommon.TP_COLOR)
				pyxel.blt(gcommon.sint(self.x -22), self.y+48, 0, sx, 8, 32, 8, gcommon.TP_COLOR)
				pyxel.blt(gcommon.sint(self.x -22), self.y+59, 0, sx, 8, 32, 8, gcommon.TP_COLOR)
				pyxel.blt(gcommon.sint(self.x -27), self.y+71, 0, sx, 8, 32, 8, gcommon.TP_COLOR)

		for obj in self.objs:
			if obj.removeFlag == False:
				obj.draw()

