
import pyxel
import math
import random
import gcommon
from objMgr import ObjMgr
import enemy
import enemyOthers

# 弧を描くように回って飛ぶ
# x,y は中心座標
class BossFactoryShot2(enemy.EnemyBase):
	def __init__(self, x, y, rad):
		super(BossFactoryShot2, self).__init__()
		self.x = x
		self.y = y
		self.rad = rad
		self.left = -3.0
		self.top = -3.0
		self.right = 3.0
		self.bottom = 3.0
		self.layer = gcommon.C_LAYER_E_SHOT
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False

	def update(self):
		if self.cnt > 180:
			self.remove()
			return
		self.x += math.cos(self.rad) * 2.0
		self.y += math.sin(self.rad) * 2.0
		self.rad -= math.pi/256
		if self.rad < 0.0:
			self.rad += math.pi*2.0

	def draw(self):
		if self.cnt & 2 == 0:
			pyxel.blt(self.x -4.0, self.y -4.0, 2, 0, 144, 9, 9, 2)
		else:
			pyxel.blt(self.x -4.0, self.y -4.0, 2, 16, 144, 9, 9, 2)

class HomingBeam1(enemy.EnemyBase):
	colorTables = [(1,5,12,6,7),(2,4,9,10,7)]
	def __init__(self, x, y, dr, homingTime=45,colorTableNo=0):
		super(HomingBeam1, self).__init__()
		self.x = x
		self.y = y
		self.dr = dr
		self.homingTime = homingTime
		self.left = -2
		self.top = -2
		self.right = 2
		self.bottom = 2
		self.layer = gcommon.C_LAYER_SKY
		self.ground = False
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False
		self.speed = 3.0
		self.colorTable = __class__.colorTables[colorTableNo]
		# 角速度
		self.omega = math.pi/60
		self.posList = []

	def update(self):
		if self.cnt <= self.homingTime:
			tempDr = gcommon.get_atan_rad_to_ship(self.x, self.y)
			rr = gcommon.radNormalize(tempDr - self.dr)
			if rr == 0.0:
				pass
			elif  rr > 0.0:
				self.dr += self.omega
				if self.dr >= math.pi*2:
					self.dr -= math.pi*2
			else:
				self.dr -= self.omega
				if self.dr <= 0.0:
					self.dr += math.pi*2
		if self.cnt < 30:
			self.speed *= 0.97
		elif self.cnt < 60 and self.speed < 5:
			self.speed *= 1.1

		#if self.cnt & 15 == 15:
		#	enemy.Particle1.append(self.x, self.y, gcommon.atan_table[self.dr] + math.pi)

		self.posList.append([self.x, self.y])
		if len(self.posList) > 16:
			del self.posList[0]
		self.x += math.cos(self.dr) * self.speed
		self.y += math.sin(self.dr) * self.speed
		#if self.speed < 6:
		#	self.speed += 0.05
		if self.x <= -64 or self.x >= (gcommon.SCREEN_MAX_X+64):
			self.remove()
			return
		elif self.y <= -64 or self.y >= (gcommon.SCREEN_MAX_Y+64):
			self.remove()
			return

	def draw(self):
		for i, pos in enumerate(self.posList):
			pyxel.pal(7, self.colorTable[(i>>2) % len(self.colorTable)])
			pyxel.blt(pos[0] -3, pos[1] -3, 0, 0, 40, 7, 7, 0)
		pyxel.pal()
		pyxel.blt(self.x -3, self.y -3, 0, 0, 40, 7, 7, 0)

# 魚雷
class Torpedo1(enemy.EnemyBase):
	def __init__(self, x, y):
		super(__class__, self).__init__()
		self.x = x
		self.y = y
		self.left = 1
		self.top = 0
		self.right = 44
		self.bottom = 6
		self.layer = gcommon.C_LAYER_SKY
		self.ground = False
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.hp = 50
		self.ground = True
		self.speed = 3.0
		self.imageSourceX = 0
		self.imageSourceY = 112
		self.imageSourceIndex = 1

	def update(self):
		self.x += self.speed
		if self.x > gcommon.SCREEN_MAX_X:
			self.remove()
			return
		if self.cnt % 3 == 0:
			obj = enemyOthers.Smoke1(self.x -8, self.y +3)
			obj.ground = True
			ObjMgr.addObj(obj)
		if self.speed < 6.0:
			self.speed += 0.1

	def draw(self):
		pyxel.blt(self.x, self.y, self.imageSourceIndex, self.imageSourceX, self.imageSourceY, 48, 7, 3)


