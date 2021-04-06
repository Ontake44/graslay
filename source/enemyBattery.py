

import pyxel
import math
import random
import gcommon
import enemy
from enemy import EnemyBase
from enemy import CountMover

# x, yは中心座標 t[2], t[3]はマップ座標
class MovableBattery1(EnemyBase):
	def __init__(self, t):
		super(MovableBattery1, self).__init__()
		pos = gcommon.mapPosToScreenPos(t[2], t[3])
		self.x = pos[0] + 3.5
		self.y = pos[1] + 3.5
		self.firstShot = t[4]
		self.moveTable = t[5]
		self.left = -11
		self.top = -11
		self.right = 11
		self.bottom = 11
		self.layer = gcommon.C_LAYER_GRD
		self.hp = 100
		self.shotInterval = int(120 / gcommon.GameSession.enemy_shot_rate)
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.mover = CountMover(self, self.moveTable, False)
		self.ground = True
		self.score = 500

	def update(self):
		self.mover.update()
		if self.x <= -24 or self.x >= gcommon.SCREEN_MAX_X+24 or self.y <= -24 or self.y >= gcommon.SCREEN_MAX_Y+24:
			self.remove()
			gcommon.debugPrint("remove Battery")
			return
		if self.firstShot == self.cnt or (self.cnt > self.firstShot and (self.cnt - self.firstShot) % self.shotInterval == 0):
			if gcommon.isShotMapPos(self.x, self.y):
				enemy.enemy_shot(self.x, self.y, 3, 0)

	def draw(self):
		pyxel.blt(self.x -11.5, self.y -11.5, 1, 128, 72, 24, 24, 3)

# x, yは中心座標 t[2], t[3]はマップ座標
class Ducker1(EnemyBase):
	def __init__(self, t):
		super(Ducker1, self).__init__()
		pos = gcommon.mapPosToScreenPos(t[2], t[3])
		self.x = pos[0] + 3.5
		self.y = pos[1] + 3.5
		self.firstShot = t[4]
		self.moveTable = t[5]
		self.left = -11
		self.top = -11
		self.right = 11
		self.bottom = 11
		self.layer = gcommon.C_LAYER_GRD
		self.hp = 100
		self.shotInterval = int(120 / gcommon.GameSession.enemy_shot_rate)
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.mover = CountMover(self, self.moveTable, False)
		self.ground = True
		self.score = 500

	def update(self):
		self.mover.update()
		if self.x <= -24 or self.x >= gcommon.SCREEN_MAX_X+24 or self.y <= -24 or self.y >= gcommon.SCREEN_MAX_Y+24:
			self.remove()
			gcommon.debugPrint("remove Battery")
			return
		if self.firstShot == self.cnt or (self.cnt > self.firstShot and (self.cnt - self.firstShot) % self.shotInterval == 0):
			if gcommon.isShotMapPos(self.x, self.y):
				enemy.enemy_shot(self.x, self.y, 3, 0)

	def draw(self):
		pyxel.blt(self.x -11.5, self.y -11.5, 1, 128, 72, 24, 24, 3)
