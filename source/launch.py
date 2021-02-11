import pyxel
import math
import random
import gcommon
import enemy

# 発艦シーン
class LaunchScene:
	def __init__(self):
		self.state = 0
		self.x = -256 -216
		self.y = gcommon.MYSHIP_START_Y +12  -50
		self.dx = 3
		self.mx = 80
		self.my = self.y + 50
		self.mdx = 0
		self.cnt = 0
		self.objs = []
		gcommon.BGM.play(gcommon.BGM.LAUNCH)

	def init(self):
		pyxel.image(1).load(0,0,"assets/launch.png")

	def update(self):
		gcommon.star_pos -= 0.2
		if gcommon.star_pos<0:
			gcommon.star_pos += 255

		if self.state == 0:
			self.x += self.dx
			if self.x > -120:
				self.nextState()
		elif self.state == 1:
			# 空母減速
			self.x += self.dx
			self.dx -= 0.05
			if self.dx <= 0:
				self.nextState()
		elif self.state == 2:
			# 自機発艦準備
			if (self.y + 50-12) < self.my:
				self.my -= 1
			if self.cnt > 60:
				self.nextState()
				self.mdx = 1.5
				gcommon.sound(gcommon.SOUND_AFTER_BURNER)
		elif self.state == 3:
			# 発艦
			self.x += self.dx
			if self.dx > -3:
				self.dx -= 0.25
			self.mx += self.mdx
			self.mdx -= 0.01
			if self.cnt & 7 == 0 and self.mdx > 0 and self.mx < 150:
				self.objs.append(enemy.Particle1(self.mx, self.my+10, math.pi +math.pi/8, 8, 50))

			if self.mdx <= -1.5:
				self.nextState()
		elif self.state == 4:
			self.x += -3
			self.mx -= 1
			if int(self.mx) == gcommon.MYSHIP_START_X:
				#print("my = " + str(self.my))
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

	def draw(self):
		pyxel.cls(0)
		gcommon.drawStar(gcommon.star_pos)

		# 上半分
		pyxel.blt(self.x, self.y, 1, 0, 0, 256, 50, gcommon.TP_COLOR)
		pyxel.blt(self.x +256, self.y, 1, 0, 96, 216, 50, gcommon.TP_COLOR)

		if self.state >= 2:
			pyxel.blt(self.mx, self.my, 0, 0, 0, 24, 16, gcommon.TP_COLOR)

			if self.state in (3,4):
				if self.mdx > 0.0:
					if self.cnt % 2 == 0:
						pyxel.blt(self.mx-32, self.my+4, 0, 72, 8, 32, 8, gcommon.TP_COLOR)
				else:
					if self.cnt % 2 == 0:
						pyxel.blt(self.mx-24, self.my+4, 0, 120, 8, 24, 8, gcommon.TP_COLOR)

		# 下半分
		pyxel.blt(self.x, self.y+50, 1, 0, 50, 256, 96-50, gcommon.TP_COLOR)
		pyxel.blt(self.x +256, self.y+50, 1, 0, 96+50, 216, 96-50, gcommon.TP_COLOR)

		for obj in self.objs:
			if obj.removeFlag == False:
				obj.draw()

