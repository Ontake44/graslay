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
	[2, 0, 0],
	[0, 1, 2],
	[2, 2, 2]
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
		self.score = 12000

	def update(self):
		if self.state == 0:
			self.x -= gcommon.cur_scroll_x
			if self.x <= 152:
				self.nextState()
		elif self.state == 1:
			if self.subState == 0:
				self.y -= 1
				if self.y < 8:
					self.nextSubState()
			elif self.subState == 1:
				self.y += 1
				if self.y > 140:
					self.nextSubState()
			elif self.subState == 2:
				self.y -= 1
				if self.y < 80:
					self.subState = 0
					self.subCnt = 0
					self.nextState()
			if self.cnt & 15 == 15:
				self.shotDanmaku()
		elif self.state == 2:
			self.shotMissle()
		elif self.state == 3:
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
		elif self.state in  [4, 5, 6, 7, 8]:
			self.shotMissle()
		elif self.state == 9:
			self.setState(1)

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
					elif mt == 1:
						self.missileObj[i] = enemy.Missile2(self.x, self.y +16, 0)
					else:
						self.missileObj[i] = enemy.Missile3(self.x, self.y +16, 0)
				self.missileIndex += 1
				if self.missileIndex >= len(missileTable):
					self.missileIndex = 0
				self.subCnt += 1
			elif self.subCnt == 40:
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
			speed = 3
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

	def broken(self):
		self.remove()
		enemy.removeEnemyShot()
		ObjMgr.objs.append(boss.BossExplosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
		GameSession.addScore(self.score)
		BGM.sound(gcommon.SOUND_LARGE_EXP)
		enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
		ObjMgr.objs.append(enemy.Delay(enemy.StageClear, None, 240))

