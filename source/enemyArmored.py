

import pyxel
import math
import random
import gcommon
import enemy
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
	def __init__(self, parent, x, y, moveTable):
		super(__class__, self).__init__()
		self.parent = parent
		self.x = x
		self.y = y
		self.mover = enemy.CountMover(self, moveTable, loopFlag=False, selfMove=False)
		self.left = 5
		self.top = 3
		self.right = 12
		self.bottom = 15
		self.layer = gcommon.C_LAYER_SKY
		self.exptype = gcommon.C_EXPTYPE_SKY_S
		self.hp = 20
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
		self.fdx = 1 if self.mover.dx < 0 else -1
		self.x = self.parent.x + self.mover.x
		self.y = self.parent.y + self.mover.y
		#gcommon.debugPrint(str(self.x) + " " + str(self.y))

	def draw(self):
		n = 0
		if abs(self.mover.dx) > 0.1:
			n = 1 + (self.cnt>>2) & 3
		pyxel.blt(self.x, self.y, 1, 56 + n * 16, 208, 16 * self.fdx, 16, 0)

