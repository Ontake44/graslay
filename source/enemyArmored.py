

from objMgr import ObjMgr
import pyxel
import math
import random
import gcommon
import enemy
import myShip
from enemy import EnemyBase, enemy_shot
from enemy import CountMover

class Armored1(EnemyBase):
	srcXTable = (0, 40, 80, 120)
	def __init__(self, t):
		super(Armored1, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.mover = enemy.CountMover(self, t[4], False)
		self.left = 12
		self.top = 3
		self.right = 27
		self.bottom = 32
		self.layer = gcommon.C_LAYER_SKY
		self.exptype = gcommon.C_EXPTYPE_SKY_M
		self.hp = 50
		self.hitcolor1 = 5
		self.hitcolor2 = 12
		self.dx = -1.5
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.score = 500

	def update(self):
		#	if self.cnt % 15 == 1:
		#		enemy.enemy_shot_dr(self.x, self.y +12, 4, 0, 32)
		self.mover.update()
		if abs(self.mover.dy) > 0.01:
			if self.cnt % 12 == 1:
				enemy.enemy_shot_dr(self.x, self.y +12, 4, 0, 32)


	def draw(self):
		n = self.cnt % 3
		if n != 2:
			pyxel.blt(self.x +28, self.y, 2, n * 16, 224, 16, 24, 2)

		spNo = 0
		if abs(self.mover.dy) > 0.01:
			spNo = 2
		elif abs(self.mover.dx) < 1.0:
			spNo = 1
		pyxel.blt(self.x, self.y, 2, __class__.srcXTable[spNo], 184, 40, 40, 2)


class Walker2(EnemyBase):
	# position : 1:下  -1：上
	def __init__(self, parent, x, y, moveTable, position):
		super(__class__, self).__init__()
		self.parent = parent
		self.x = x
		self.y = y
		self.mover = enemy.CountMover(self, moveTable, loopFlag=False, selfMove=False)
		self.position = position
		self.left = 4
		self.right = 12
		if self.position == 1:
			self.top = 3
			self.bottom = 15
		else:
			self.top = 0
			self.bottom = 12
		self.layer = gcommon.C_LAYER_SKY
		self.exptype = gcommon.C_EXPTYPE_SKY_S
		self.hp = 50
		self.hitcolor1 = 5
		self.hitcolor2 = 12
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.score = 200
		self.fdx = 1

	def update(self):
		self.mover.update()
		if self.mover.isEnd:
			self.remove()
			return
		if self.mover.mode == CountMover.STOP:
			if self.mover.cnt == 20:
				enemy_shot(self.x + (self.right -self.left)/2, self.y + (self.bottom -self.top)/2, 2, 0)
		if self.mover.dx < 0.0:
			self.fdx = 1
		elif self.mover.dx > 0.0:
			self.fdx = -1
		self.x = self.parent.x + self.mover.x
		self.y = self.parent.y + self.mover.y
		#gcommon.debugPrint(str(self.x) + " " + str(self.y))

	def draw(self):
		n = 0
		if abs(self.mover.dx) > 0.1:
			n = 1 + (self.cnt>>2) & 3
		pyxel.blt(self.x, self.y, 1, 56 + n * 16, 208, 16 * self.fdx, 16 * self.position, 0)



class Ducker1(EnemyBase):
	def __init__(self, t):
		super(__class__, self).__init__()
		self.x = -16
		self.position = t[2]		# 1:下 -1:上
		self.y = self.getInitialY(self.position) -8
		self.left = -6
		self.right = 6
		self.top = -6
		self.bottom = 6
		self.layer = gcommon.C_LAYER_GRD
		self.exptype = gcommon.C_EXPTYPE_GRD_S
		self.hp = 50
		self.hitcolor1 = 5
		self.hitcolor2 = 12
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.ground = True
		self.score = 200
		self.direction = 1
		self.cycleCount = 0
		self.upDownFlag = False

	def getInitialY(self, pos):
		y = 96
		if pos == 1:
			while(True):
				n = gcommon.getMapData(-16, y)
				if n == 0:
					y += 8
				else:
					break
			return y -8 - (int(gcommon.map_y) & 7)
		else:
			while(True):
				n = gcommon.getMapData(-16, y)
				if n == 0:
					y -= 8
				else:
					break
			return y +8 - (int(gcommon.map_y) & 7)

	def move(self):
		self.dx = 0
		# 移動
		if self.position == 1:
			# 下位置
			n = gcommon.getMapData(self.x +8*self.direction, self.y+7)
			if n != 0:
				self.upDownFlag = True
				self.y -= 4
			else:
				n = gcommon.getMapData(self.x +16*self.direction, self.y+7)
				if n != 0:
					self.upDownFlag = True
					self.dx = 2 *self.direction
					self.y -= 4
				else:
					n = gcommon.getMapData(self.x, self.y +8)
					if n == 0:
						# 下が空間
						self.upDownFlag = True
						self.dx = 2 *self.direction
						self.y += 2
					else:
						self.dx = 2 *self.direction
		else:
			# 上位置
			n = gcommon.getMapData(self.x +8*self.direction, self.y-8)
			if n != 0:
				self.upDownFlag = True
				self.y += 4
			else:
				n = gcommon.getMapData(self.x +16*self.direction, self.y-8)
				if n != 0:
					self.upDownFlag = True
					self.dx = 2 *self.direction
					self.y += 4
				else:
					n = gcommon.getMapData(self.x, self.y -9)
					if n == 0:
						# 上が空間
						self.upDownFlag = True
						self.dx = 2 *self.direction
						self.y -= 2
					else:
						self.dx = 2 *self.direction
		self.x += self.dx

	def update(self):
		if self.state == 0:
			self.upDownFlag = False
			self.move()
			if self.upDownFlag == False:
				if ObjMgr.myShip.x + myShip.MyShipBase.CENTER_X >= 128:
					# 画面右側
					l = abs(ObjMgr.myShip.y + myShip.MyShipBase.CENTER_Y - self.y)
					if self.x > ObjMgr.myShip.x + myShip.MyShipBase.CENTER_X - l:
						self.nextState()
				else:
					# 画面左側
					l = abs(ObjMgr.myShip.y + myShip.MyShipBase.CENTER_Y - self.y)
					if self.x > ObjMgr.myShip.x + myShip.MyShipBase.CENTER_X + l +40:
						self.nextState()
		elif self.state == 1:
			self.dx = 0
			if self.cnt == 20:
				enemy.enemy_shot(self.x, self.y, 2, 0)
			elif self.cnt >= 60:
				self.cycleCount += 1
				if self.cycleCount > 3:
					# 撤退
					self.direction = -1
					self.nextState()
				else:
					#self.direction = -1 * self.direction
					self.setState(0)
		elif self.state == 2:
			# 撤退
			self.move()
		if self.x > 256 or self.x < -32:
			self.remove()
			return

	def draw(self):
		if self.dx == 0:
			fx = 1 if ObjMgr.myShip.x + myShip.MyShipBase.CENTER_X > self.x else -1
			pyxel.blt(self.x -8, self.y-8, 1, 64, 112, 16 * fx, 16 * self.position, 3)
		else:
			pyxel.blt(self.x -8, self.y-8, 1, ((self.cnt>>2) & 3) *16, 112, 16 *self.direction, 16 * self.position, 3)

