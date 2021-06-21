

import pyxel
import math
import random
import gcommon
import enemy
import item
from objMgr import ObjMgr
from enemy import EnemyBase
from enemy import CountMover
from gameSession import GameSession

# 倉庫内移動砲台
# x, yは中心座標 t[2], t[3]はマップ座標
# このクラスは生成用で、実際に画面上で動作するのはMovableBattery1p
class MovableBattery1(EnemyBase):
	lightTable = (0, 2, 4, 8, 8, 4, 2, 0)
	spTable = (3, 2, 1, 0, -1, 0, 1, 2)
	def __init__(self, t):
		super(MovableBattery1, self).__init__()
		self.mx = t[2]
		self.my = t[3]
		pos = gcommon.mapPosToScreenPos(t[2], t[3])
		self.x = pos[0] + 3.5
		self.y = pos[1] + 3.5
		self.firstShot = t[4]
		self.moveTable = t[5]
		if self.x <= -96 or self.x >= gcommon.SCREEN_MAX_X+96 or self.y <= -96 or self.y >= gcommon.SCREEN_MAX_Y+96:
			gcommon.debugPrint("MovableBattery1 is ng start point (" +  str(self.mx) + ","+ str(self.my) +") (" + str(self.x) + "," + str(self.y)+"")
		else:
			ObjMgr.addObj(MovableBattery1p(self.x, self.y, self.firstShot, self.moveTable))
		self.remove()

	def update(self):
		pass

# 倉庫内移動砲台
# x, yは中心座標 t[2], t[3]はマップ座標
class MovableBattery1p(EnemyBase):
	lightTable = (0, 2, 4, 8, 8, 4, 2, 0)
	spTable = (3, 2, 1, 0, -1, 0, 1, 2)
	def __init__(self, x, y, firstShot, moveTable):
		super(MovableBattery1p, self).__init__()
		self.x = x
		self.y = y
		self.firstShot = firstShot
		self.moveTable = moveTable
		self.left = -11
		self.top = -11
		self.right = 11
		self.bottom = 11
		self.layer = gcommon.C_LAYER_GRD
		self.hitcolor1 = 13
		self.hitcolor2 = 15
		self.hp = 70
		self.shotInterval = int(120 / GameSession.enemy_shot_rate)
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.mover = CountMover(self, self.moveTable, False)
		self.ground = True
		self.score = 500
		# 0 :閉じている
		# 1 :開く1
		# 2 :開く2
		# 3 :開く3
		# 4 :開く4  ショット
		# 5 :開く3
		# 6 :開く2
		# 7 :開く1
		self.shotState = 0
		self.shotCnt = 0

	def update(self):
		self.mover.update()
		if self.x <= -96 or self.x >= gcommon.SCREEN_MAX_X+96 or self.y <= -96 or self.y >= gcommon.SCREEN_MAX_Y+96:
			#gcommon.debugPrint("remove MovableBattery1p")
			self.remove()
			return
		if self.firstShot == self.cnt or (self.cnt > self.firstShot and (self.cnt - self.firstShot) % self.shotInterval == 0):
			if self.shotState == 0:
				self.shotState = 1
		if self.shotState >= 1:
			self.shotCnt += 1
			if self.shotCnt > 5:
				self.shotCnt = 0
				self.shotState += 1
				if self.shotState == 4 and gcommon.isShotMapPos(self.x, self.y):
					enemy.enemy_shot(self.x, self.y, 3, 0)
				elif self.shotState >= 8:
					self.shotState = 0

	def draw(self):
		n = (self.cnt>>2) % len(__class__.lightTable)
		pyxel.pal(8, __class__.lightTable[n])
		sp = __class__.spTable[self.shotState]
		pyxel.blt(gcommon.sint(self.x -11.5), gcommon.sint(self.y -11.5), 2, 0, 0, 24, 24, 3)
		if sp >= 0:
			pyxel.blt(gcommon.sint(self.x -11.5)+4, gcommon.sint(self.y -11.5)+4, 2, sp*16, 24, 16, 16)
		pyxel.pal()

# 武装なしのコンテナキャリアー
class ContainerCarrier1(EnemyBase):
	lightTable = (0, 2, 4, 8, 8, 4, 2, 0)
	def __init__(self, t):
		super(ContainerCarrier1, self).__init__()
		self.mx = t[2]
		self.my = t[3]
		pos = gcommon.mapPosToScreenPos(t[2], t[3])
		self.x = pos[0] + 3.5
		self.y = pos[1] + 3.5
		self.moveTable = t[4]
		self.left = -11
		self.top = -11
		self.right = 11
		self.bottom = 11
		self.layer = gcommon.C_LAYER_GRD
		self.hp = 50
		self.hitcolor1 = 13
		self.hitcolor2 = 15
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.mover = CountMover(self, self.moveTable, False)
		self.ground = True
		self.score = 100

	def update(self):
		self.mover.update()
		if self.x <= -96 or self.x >= gcommon.SCREEN_MAX_X+96 or self.y <= -96 or self.y >= gcommon.SCREEN_MAX_Y+96:
			self.remove()
			if self.cnt < 10:
				gcommon.debugPrint("ContainerCarrier1 is ng start point (" +  str(self.mx) + ","+ str(self.my) +") (" + str(self.x) + "," + str(self.y)+"")
			return

	def draw(self):
		n = (self.cnt>>2) % len(__class__.lightTable)
		pyxel.pal(8, __class__.lightTable[n])
		pyxel.blt(gcommon.sint(self.x -11.5), gcommon.sint(self.y -11.5), 2, 24, 0, 24, 24, 3)
		pyxel.pal()

# 牽引車
class Tractor1(EnemyBase):
	lightTable = (0, 2, 4, 8, 8, 4, 2, 0)
	def __init__(self, t):
		super(Tractor1, self).__init__()
		pos = gcommon.mapPosToScreenPos(t[2], t[3])
		self.x = pos[0] + 3.5
		self.y = pos[1] + 3.5
		self.moveTable = t[4]
		self.left = -11
		self.top = -11
		self.right = 11
		self.bottom = 11
		self.layer = gcommon.C_LAYER_GRD
		self.hp = 50
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.mover = CountMover(self, self.moveTable, False)
		self.ground = True
		self.score = 100
		# 貨物車を追加
		obj = Freight1(self, 0, 36, 1)
		ObjMgr.addObj(obj)
		ObjMgr.addObj(Freight1(obj, 0, 48, 2))

	def update(self):
		self.mover.update()
		if self.x <= -136 or self.x >= gcommon.SCREEN_MAX_X+136 or self.y <= -136 or self.y >= gcommon.SCREEN_MAX_Y+136:
			self.remove()
			gcommon.debugPrint("Tractor1 removed")
			return

	def draw(self):
		n = (self.cnt>>2) % len(__class__.lightTable)
		pyxel.pal(8, __class__.lightTable[n])
		pyxel.blt(self.x -11.5, self.y -11.5, 2, 48, 0, 24, 24, 3)
		pyxel.pal()


# 貨物車
class Freight1(EnemyBase):
	def __init__(self, parent, offsetX, offsetY, itemType=0):
		super(Freight1, self).__init__()
		self.x = parent.x + offsetX
		self.y = parent.y + offsetY
		self.parent = parent
		self.offsetX = offsetX
		self.offsetY = offsetY
		self.itemType = itemType
		self.left = -11
		self.top = -22
		self.right = 11
		self.bottom = 22
		self.layer = gcommon.C_LAYER_GRD
		self.hp = 300
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.ground = True
		self.score = 500

	def update(self):
		if self.parent.removeFlag == False:
			self.x = self.parent.x + self.offsetX
			self.y = self.parent.y + self.offsetY
		if self.x <= -100 or self.x >= gcommon.SCREEN_MAX_X+100 or self.y <= -100 or self.y >= gcommon.SCREEN_MAX_Y+100:
			self.remove()
			gcommon.debugPrint("Tractor1 removed")
			return

	def draw(self):
		pyxel.blt(self.x -11.5, self.y -24.5, 2, 0, 48, 24, 48, 3)

	def broken(self):
		super().broken()
		if self.itemType == 1:
			item.ScoreItem1.createByPos(self.x, self.y)
		elif self.itemType == 2:
			item.OneUpItem1.createByPos(self.x, self.y)


# ※動かない
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
		self.shotInterval = int(120 / GameSession.enemy_shot_rate)
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.mover = CountMover(self, self.moveTable, False)
		self.ground = True
		self.score = 500

	def update(self):
		pass

	def draw(self):
		pass


# 植物砲台（大）
class PlantBattery1(EnemyBase):
	def __init__(self, t):
		super(PlantBattery1, self).__init__()
		pos = gcommon.mapPosToScreenPos(t[2], t[3])
		self.x = pos[0]
		self.y = pos[1]
		self.mirror = t[4]
		self.firstShot = t[5]
		self.left = 11
		self.top = 3
		self.right = 44
		self.bottom = 16
		if self.mirror == 1:
			self.top = 23 -16
			self.bottom = 23 -3
		self.layer = gcommon.C_LAYER_GRD
		self.exptype = gcommon.C_EXPTYPE_GRD_M
		self.hp = 100
		self.shotInterval = int(120 / GameSession.enemy_shot_rate)
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.ground = True
		self.score = 500
		self.state = 0

	def update(self):
		if self.x <= -56:
			self.remove()
			return
		if self.state == 0 and self.cnt == self.firstShot:
			self.setState(1)
		if self.state == 1:
			if self.cnt == 10:
				if self.mirror:
					if self.y < 28:
						return
				else:
					if self.y > (gcommon.SCREEN_MAX_Y -28):
						return
				shotY = 48
				if self.mirror != 0:
					shotY = 16
				shotCount = 6
				if GameSession.difficulty == gcommon.DIFFICULTY_EASY:
					shotCount = 4
				elif GameSession.difficulty == gcommon.DIFFICULTY_NORMAL:
					shotCount = 6
				else:
					shotCount = 8
				enemy.enemy_shot_dr_multi(self.x +27.5, self.y + self.mirror * 24, 2, 0, shotY, shotCount, 4)
			elif self.cnt > 30:
				self.state = 2
		elif self.state == 2:
			if self.cnt == self.shotInterval:
				self.setState(1)

	def draw(self):
		ssy = 1
		if self.mirror:
			ssy = -1
		pyxel.blt(self.x, self.y, 2, 0, 40, 16, 24 * ssy, 3)
		pyxel.blt(self.x +40, self.y, 2, 40, 40, 16, 24 * ssy, 3)
		if self.state == 1:
			sx = 56
			if self.cnt > 8 and self.cnt < 22:
				sx = 80
			pyxel.blt(self.x +16, self.y, 2, sx, 40, 24, 24 * ssy, 3)
		else:
			pyxel.blt(self.x +16, self.y, 2, 16, 40, 24, 24 * ssy, 3)

# 植物砲台（小）
class PlantBattery2(EnemyBase):
	def __init__(self, t):
		super(PlantBattery2, self).__init__()
		pos = gcommon.mapPosToScreenPos(t[2], t[3])
		self.x = pos[0]
		self.y = pos[1]
		self.mirror = t[4]
		self.firstShot = t[5]
		self.left = 7
		self.top = 3
		self.right = 16
		self.bottom = 15
		if self.mirror == 1:
			self.top = 23 -15
			self.bottom = 23 -3
		self.layer = gcommon.C_LAYER_GRD
		self.hp = 20
		self.shotInterval = int(150 / GameSession.enemy_shot_rate)
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.ground = True
		self.score = 200
		self.state = 0

	def update(self):
		if self.x <= -24:
			self.remove()
			return
		if self.state == 0 and self.cnt == self.firstShot:
			self.setState(1)
		if self.state == 1:
			if self.cnt == 10:
				enemy.enemy_shot(self.x +12.5, self.y + self.mirror * 24, 2, 0)
			elif self.cnt > 30:
				self.state = 2
		elif self.state == 2:
			if self.cnt == self.shotInterval:
				self.setState(1)

	def draw(self):
		sx = 72 if self.cnt & 16 == 0 else 96
		ssy = 1
		if self.mirror:
			ssy = -1
		pyxel.blt(self.x, self.y, 2, sx, 16, 24, 24 * ssy, 3)

class FireBattery1(enemy.Battery0):
	def __init__(self, mx, my, mirror):
		pos = gcommon.mapPosToScreenPos(mx, my)
		super(__class__, self).__init__(pos[0], pos[1], mirror)
		self.imageSourceIndex = 2
		self.imageSourceX = 0
		self.imageSourceY = 80
