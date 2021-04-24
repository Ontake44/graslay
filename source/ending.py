import pyxel
import math
import random
import enemy
import gcommon
from audio import BGM

class Star:
	def __init__(self, x, y, dx, dy, cnt):
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.cnt = cnt
		self.life = cnt
		self.removeFlag = False


class EndingScene0:
	def __init__(self, parent):
		self.parent = parent
		self.sptable = [0, 1, 0, 1]
		self.star_ary = []
		self.radius = 1
		self.state = 0
		self.cnt = 0
		self.px = 127
		self.py = 100
		self.pos = 0
		self.speed = 2
		self.tbl = []
		self.objs = []

	def addStar(self, x, y, dx, dy, life):
		s = Star(x, y, dx, dy, life)
		self.tbl.append(s)

	def update(self):
		if self.state == 0:
			if self.cnt > 120:
				for i in range(0,800):
					r = random.random() * 2 * math.pi
					speed = random.random() * 6
					self.addStar(128, 100, speed * math.cos(r), speed * math.sin(r), random.randrange(50, 2000))
					#s = Star(128, 100, speed * math.cos(r), speed * math.sin(r), random.randrange(50, 2000))
					#tbl.append(s)
				self.state = 1
				self.cnt = 0

		elif self.state == 1:
			self.radius += 1
			if self.cnt > 300:
				self.state = 2
				self.cnt = 0
		elif self.state == 2:
			self.px -= 0.25
			self.py -= 0.25
			if self.cnt & 7 == 0:
				self.addStar(self.px+1, self.py, 0.0, 0.0, random.randrange(10, 80))
			if self.cnt == 150:
				self.parent.setScene(EndingScene1(self.parent))
				self.state = 0
				self.cnt = 0
				self.px = 256
				self.py = 220

		for s in self.tbl:
			s.x += s.dx
			s.y += s.dy
			s.dx *= 0.99
			s.dy *= 0.99
		
		self.cnt += 1
	def draw(self):
		pyxel.cls(0)

		# 星
		for i in range(0,96):
			pyxel.pset(EndingScene.star_ary[i][0], i*2, int(random.randrange(0,2)+5))

		if self.state == 0:
			if self.cnt & 2 == 0:
				pyxel.blt(104, 76, 2, 208, 0, 48, 48, 0)
			else:
				pyxel.blt(104, 76, 2, 208, 48, 48, 48, 0)

		elif self.state == 1:
			if self.radius < 150:
				pyxel.circb(128, 100, self.radius * self.radius/10, 7)
				pyxel.circ(128, 100, self.radius, 6)
			elif self.radius < 200:
				pyxel.rect(0,0, 256, 200, 12)
			elif self.radius < 250:
				pyxel.rect(0,0, 256, 200, 5)
			elif self.radius < 300:
				pyxel.rect(0,0, 256, 200, 1)


		if self.state == 2:
			if self.cnt % 3 == 0:
				sx = self.sptable[self.cnt % 4]
				pyxel.blt(self.px -15, self.py -15, 2, 32*sx, 0, 32, 32, 0)

		newTbl = []
		for s in self.tbl:
			s.cnt -= 1
			if s.cnt != 0:
				skip = False
				n = (s.life - s.cnt)/ s.life
				if n > 0.5:
					if s.cnt & 1 == 0:
						skip = True
				elif n > 0.6:
					if s.cnt & 3 != 0:
						skip = True
				elif n > 0.8:
					if s.cnt & 7 != 0:
						skip = True
				if skip == False:
					pyxel.pset(s.x, s.y, 7)
				newTbl.append(s)
		self.tbl = newTbl

class EndingScene1:
	def __init__(self, parent):
		self.parent = parent
		self.sptable = [0, 1, 0, 1]
		self.star_ary = []
		self.radius = 1
		self.state = 0
		self.cnt = 0
		self.px = 127
		self.py = 100
		self.scene = 0
		self.pos = 0
		self.speed = 2
		self.tbl = []
		self.objs = []

	def update(self):
		if self.state == 0:
			self.px -= self.speed
			self.py -= self.speed
			if self.px < 80:
				self.speed *= 0.9
			if self.speed < 0.1:
				self.state = 1
				self.cnt = 0
			if self.cnt % 5 == 0 and self.speed > 1.7:
				obj = enemy.Particle1(self.px + 10, self.py + 10, math.pi/4, 20, 200)
				obj.speedDown = False
				self.objs.append(obj)
		elif self.state == 1:
			self.px += self.speed
			self.py += self.speed
			self.speed *= 1.03
			if self.cnt > 60:
				self.state = 2
				self.cnt = 0
				self.speed = 1
		elif self.state == 2:
			self.px -= self.speed
			self.py -= self.speed
			self.speed *= 1.1
			if self.cnt % 3 == 0:
				obj = enemy.Particle1(self.px + 77, self.py + 75, math.pi/4, 20, 200)
				obj.speedDown = False
				self.objs.append(obj)
			if self.cnt > 200:
				self.parent.setScene(EndingScene2(self.parent))
				self.state = 0
				self.cnt = 0

		newObjs = []
		for obj in self.objs:
			if obj.removeFlag == False:
				obj.update()
				newObjs.append(obj)
		self.objs = newObjs	
		self.pos += 2
		self.cnt += 1

	def draw(self):
		pyxel.cls(0)
		for i in range(0,96):
			x = (EndingScene.star_ary[i][0] +self.pos) & 255
			y = (i*2 +self.pos) % 200
			pyxel.pset(x, y, int(random.randrange(0,2)+5))

		x = self.px 	#+ random.randrange(-1, 1)
		y = self.py #+ random.randrange(-1, 1)
		pyxel.blt(x, y, 2, 0, 48, 96, 80, 0)
		if self.cnt & 2 == 0:
			if self.state < 2:
				if self.cnt % 4 == 0:
					pyxel.blt(x +77, y +75, 2, 0, 128, 48, 48, 0)
				else:
					pyxel.blt(x +77, y +75, 2, 48, 128, 56, 56, 0)
			else:
				if self.cnt % 4 == 0:
					pyxel.blt(x +77, y +75, 2, 48, 128, 56, 56, 0)
				else:
					pyxel.blt(x +77, y +75, 2, 104, 128, 72, 72, 0)

		for obj in self.objs:
			if obj.removeFlag == False:
				obj.draw()

# 本星に帰る
class EndingScene2:
	def __init__(self, parent):
		self.parent = parent
		self.py = 190
		self.px = 150
		self.dy = -2
		self.sx = 88
		self.sy = 32
		self.size = 1.0
		self.state = 0
		self.cnt = 0
		self.message = "THE END"
		self.objs = []
		BGM.playOnce(BGM.ENDING)

	def update(self):
		if self.state == 0:
			self.py += self.dy
			self.dy *= 0.98	#	0.985
			self.size *= 0.99
			if self.cnt < 46 and self.cnt % 8 == 0:
				obj = enemy.Particle2(self.px, self.py+4, 20)
				self.objs.append(obj)
			if self.cnt > 240:
				self.cnt = 0
				self.state = 1
		elif self.state == 1:
			# 待ち
			if self.cnt > 120:
				self.cnt = 0
				self.state = 2
		elif self.state == 2:
			# キラーン！ ☆
			if self.cnt > 600:
				self.cnt = 0
				gcommon.app.startGameClear()
		newObjs = []
		for obj in self.objs:
			if obj.removeFlag == False:
				obj.update()
				newObjs.append(obj)
		self.objs = newObjs	
		self.cnt += 1

	def draw(self):
		pyxel.cls(0)
		# 星
		for i in range(0,96):
			pyxel.pset(EndingScene.star_ary[i][0], i*2, int(random.randrange(0,2)+5))
		
		pyxel.blt(128 -56/2, 40, 2, 128, 48, 56, 56, 2)
		if self.state == 0:
			gcommon.stretchBlt(self.px - self.sx * self.size/2, self.py - self.sy * self.size/2, 	\
				self.sx * self.size, self.sy * self.size,	\
				1, 0, 0, self.sx, self.sy)
		elif self.state == 2:
			px = 132
			py = 60
			if self.cnt < 18:
				self.drawShine(px, py, int(self.cnt/6))
			elif self.cnt < 60:
				if self.cnt & 2 == 0:
					self.drawShine(px, py, 2)
			elif self.cnt < 80:
				self.drawShine(px, py, int(2 -(self.cnt-62)/6))
			elif self.cnt >= 150:
				l = int((self.cnt -150)/20)
				sl = len(self.message)
				if l > sl:
					l = sl
				gcommon.showText(128 -sl*4, 120, self.message[:l])

		for obj in self.objs:
			if obj.removeFlag == False:
				obj.draw()

	def drawShine(self, x, y, n):
		pyxel.blt(x, y, 2, 160 -int(n)*32, 0, 32, 32, 0)

class EndingScene:
	star_ary = []
	def __init__(self):
		pyxel.image(2).load(0,0,"assets/Ending0.png")
		pyxel.image(1).load(0,0,"assets/Ending1.png")
		
		EndingScene.star_ary = []
		for i in range(0,96):
			o = [int(random.randrange(0,256)), int(random.randrange(0,2)+5)]
			EndingScene.star_ary.append(o)		
		self.scene = EndingScene0(self)
		
	def init(self):
		pass

	def setScene(self, scene):
		self.scene = scene
		self.update()

	def update(self):
		self.scene.update()

	def draw(self):
		self.scene.draw()

