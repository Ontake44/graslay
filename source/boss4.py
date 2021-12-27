import pyxel
import math
import random
import gcommon
import enemy
import boss
from objMgr import ObjMgr
from gameSession import GameSession
from audio import BGM

missileTable = [
	[0, 0, 0],
	[0, 1, 0],
	[1, 1, 0],
	[0, 0, 0],
	[0, 1, 0],
	[0, 0, 0]
]

class Boss4(enemy.EnemyBase):
	def __init__(self, t):
		super(Boss4, self).__init__()
		self.x = 256
		self.y = 80
		self.layer = gcommon.C_LAYER_SKY
		self.left = 27
		self.top = 8
		self.right = 87
		self.bottom = 45
		self.hp = boss.BOSS_4_HP
		self.subState = 0
		self.subCnt = 0
		self.hitcolor1 = 9
		self.hitcolor2 = 10
		self.missileState = 0
		self.missileObj = [None, None, None]
		self.missileIndex = 0
		self.homingMissileInterval = 60
		self.homingMissileCnt = 0
		self.homingMissileFlag = False
		self.score = 12000
		gcommon.debugPrint("Boss4")

	def update(self):
		if self.state == 0:
			self.x -= gcommon.cur_scroll_x
			if self.x <= 152:
				self.nextState()
		elif self.state == 1:
			if self.subState == 0:
				# 上に移動
				self.y -= 1
				if self.y < 8:
					self.nextSubState()
			elif self.subState == 1:
				# 下に移動
				self.y += 1
				if self.y > 140:
					self.nextSubState()
			elif self.subState == 2:
				# 上に移動
				self.y -= 1
				if self.y < 80:
					self.subState = 0
					self.subCnt = 0
					self.nextState()
			if self.cnt & 15 == 15:
				self.shotDanmaku()
			self.homingMissileFlag = False
			#if self.cnt % self.homingMissileInterval == 0:
			#	self.shotHomingMissile()
		elif self.state in (2, 3, 4):
			self.shotMissle()
			self.homingMissileFlag = True
		elif self.state == 5:
			if self.subState == 0:
				self.y += 1
				if self.y > 140:
					self.nextSubState()
			elif self.subState == 1:
				self.y -= 1
				if self.y < 8:
					self.nextSubState()
			elif self.subState == 2:
				self.y += 1
				if self.y > 80:
					self.subState = 0
					self.subCnt = 0
					self.nextState()
			if self.cnt & 15 == 15:
				self.shotDanmaku()
			self.homingMissileFlag = False
			#if self.cnt % self.homingMissileInterval == 0:
			#	self.shotHomingMissile()
		elif self.state in  [6, 7, 8, 9, 10]:
			self.shotMissle()
			self.homingMissileFlag = True
		elif self.state == 11:
			self.setState(1)
		self.shotHomingMissile()

	def shotHomingMissile(self):
		if self.homingMissileFlag:
			if self.homingMissileCnt == 20:
				obj = enemy.HomingMissile1(self.x +68, self.y +8, 48)
				obj.imageSourceIndex = 1
				obj.imageSourceX = 128
				obj.imageSourceY = 80
				ObjMgr.addObj(obj)

				obj = enemy.HomingMissile1(self.x +68, self.y+48, 16)
				obj.imageSourceIndex = 1
				obj.imageSourceX = 128
				obj.imageSourceY = 80
				ObjMgr.addObj(obj)
		self.homingMissileCnt += 1
		if self.homingMissileCnt >= self.homingMissileInterval:
			self.homingMissileCnt = 0

	def shotMissle(self):
		if self.subState == 0:
			cy = gcommon.getCenterY(ObjMgr.myShip)
			if cy > self.y+30:
				self.y += 1
				if self.y > 140:
					self.y = 140
			elif cy < self.y+28:
				self.y -= 1
				if self.y < 8:
					self.y = 8			
		if self.subState == 0:
			# ミサイル発射準備
			if self.subCnt == 0:
				# ここでミサイルを決定する
				for i in range(3):
					mt = missileTable[self.missileIndex][i]
					if mt == 0:
						self.missileObj[i] = enemy.Missile1(self.x, self.y +16, 0)
					else:
						self.missileObj[i] = enemy.Missile2(self.x, self.y +16, 0)
					# else:
					# 	self.missileObj[i] = enemy.Missile1(self.x, self.y +16, 0)
				self.missileIndex += 1
				if self.missileIndex >= len(missileTable):
					self.missileIndex = 0
				self.subCnt += 1
			elif self.subCnt == 20:
				# ミサイル発射中へ
				self.nextSubState()
				self.missileState = 0
			else:
				self.subCnt += 1
		elif self.subState == 1:
			# ミサイル発射中
			if self.subCnt == 0:
				# ミサイル発射
				m = self.missileObj[self.missileState]
				m.x = self.x
				m.y = self.y +16 +self.missileState*8
				m.layer = gcommon.C_LAYER_GRD
				ObjMgr.addObj(m)
				# インクリメント
				self.missileState += 1
				if self.missileState == 3:
					self.missileObj[0] = None
					self.missileObj[1] = None
					self.missileObj[2] = None
					self.nextSubState()
					return
			self.subCnt += 1
			if self.subCnt == 10:
				self.subCnt = 0
		elif self.subState == 2:
			# 待ち
			if self.subCnt == 30:
				self.setSubState(0)
				self.nextState()
				return
			self.subCnt += 1

	def shotDanmaku(self):
		if self.cnt & 31 == 31:
			speed = 2.5
			enemy.enemy_shot_dr(self.x +52, self.y +16, speed, 0, 35)
			enemy.enemy_shot_dr(self.x +48, self.y +22, speed, 0, 31)
			enemy.enemy_shot_dr(self.x +48, self.y +42, speed, 0, 33)
			enemy.enemy_shot_dr(self.x +52, self.y +48, speed, 0, 27)
			
			if GameSession.isHard():
				enemy.enemy_shot_dr(self.x +52, self.y +16, speed, 0, 37)
				enemy.enemy_shot_dr(self.x +52, self.y +48, speed, 0, 29)
		else:
			speed = 1.5
			enemy.enemy_shot_dr(self.x +52, self.y +16, speed, 1, 36)
			enemy.enemy_shot_dr(self.x +52, self.y +48, speed, 1, 28)
			if GameSession.isHard():
				enemy.enemy_shot_dr(self.x +48, self.y +22, speed, 1, 34)
				enemy.enemy_shot_dr(self.x +48, self.y +42, speed, 1, 30)
		BGM.sound(gcommon.SOUND_SHOT2)


	def nextSubState(self):
		self.subState += 1
		self.subCnt = 0

	def setSubState(self, subState):
		self.subState = subState
		self.subCnt = 0

	def draw(self):
		if self.state in [2, 4, 5 ,6 ,7, 8]:
			if self.subState == 0:
				# ミサイル発射準備
				if self.subCnt < 32:
					x = self.x + 31- self.subCnt
				else:
					x = self.x
				for i in range(3):
					#pyxel.blt(x, self.y + 16 + i*8, 1, 48, 64, 32, 8, gcommon.TP_COLOR)
					if self.missileObj[i] != None:
						self.missileObj[i].x = x
						self.missileObj[i].y = self.y + 16 + i*8
						self.missileObj[i].drawMissile()
			elif self.subState == 1:
				# ミサイル発射中
				if self.missileState == 1:
					#pyxel.blt(self.x, self.y + 16 + 1*8, 1, 48, 64, 32, 8, gcommon.TP_COLOR)
					self.missileObj[1].x = self.x
					self.missileObj[1].y = self.y + 16 + 1*8
					self.missileObj[1].drawMissile()
				if self.missileState in [1, 2]:
					#pyxel.blt(self.x, self.y + 16 + 2*8, 1, 48, 64, 32, 8, gcommon.TP_COLOR)
					self.missileObj[2].x = self.x
					self.missileObj[2].y = self.y + 16 + 2*8
					self.missileObj[2].drawMissile()

		pyxel.blt(self.x, self.y, 1, 160, 200, 96, 56, gcommon.TP_COLOR)
		if self.homingMissileFlag:
			if (self.homingMissileCnt >=0 and self.homingMissileCnt < 10) \
				or (self.homingMissileCnt >= 30 and self.homingMissileCnt < 40):
				pyxel.blt(self.x +64, self.y +0, 1, 224, 168, 16, 16, gcommon.TP_COLOR)
				pyxel.blt(self.x +64, self.y +32, 1, 224, 184, 16, 16, gcommon.TP_COLOR)
			elif (self.homingMissileCnt >=10 and self.homingMissileCnt < 30):
				pyxel.blt(self.x +64, self.y +0, 1, 240, 168, 16, 16, gcommon.TP_COLOR)
				pyxel.blt(self.x +64, self.y +32, 1, 240, 184, 16, 16, gcommon.TP_COLOR)
			

	def broken(self):
		self.remove()
		enemy.removeEnemyShot()
		ObjMgr.objs.append(boss.BossExplosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
		GameSession.addScore(self.score)
		BGM.sound(gcommon.SOUND_LARGE_EXP)
		enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
		ObjMgr.objs.append(enemy.Delay(enemy.StageClear, None, 240))

