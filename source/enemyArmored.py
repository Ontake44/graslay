

import pyxel
import math
import random
import gcommon
import enemy
from enemy import EnemyBase
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

