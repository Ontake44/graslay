import pyxel
import math
import random
import gcommon
import enemy
import boss

class Boss3Body:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.left = 3
		self.top = 8
		self.right = 42
		self.bottom = 39

class Boss3Anchor:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.left = 1
		self.top = 4
		self.right = 23
		self.bottom = 11

#  出現
#  2 上端・下端に移動
#  3 下端からショットを打ちながら上端まで移動
#  4 車両側からEnemyShot、本体部が自機に追従
#  5 アンカー射出
#  6 上端に移動
#  7 上端からショットを打ちながら下端まで移動
#  8 本来部が中心まで移動
#  9 体当たり・戻る
#  10 最初に戻る
class Boss3(enemy.EnemyBase):
	shotCycles = (32, 24, 15)
	def __init__(self, t):
		super(Boss3, self).__init__()
		self.x = 256
		self.y = 16
		self.left = 16
		self.top = 9
		self.right = 63
		self.bottom = 38
		self.hp = boss.BOSS_3_HP
		self.layer = gcommon.C_LAYER_SKY
		self.score = 10000
		self.subcnt = 0
		self.hitcolor1 = 13
		self.hitcolor2 = 7
		self.body = Boss3Body()
		self.body.y = 72
		self.anchor = Boss3Anchor()
		self.upperARect = gcommon.Rect.create(8, 0, 72, 15)
		self.upperBRect = gcommon.Rect.create(24, 16, 71, 29)
		self.shaftRect = gcommon.Rect.create(40, 30, 62, 129)
		self.lowerBRect = gcommon.Rect.create(24, 130, 71, 143)
		self.lowerARect = gcommon.Rect.create(8, 144, 72, 159)
		self.mode = 0
		self.modeCnt = 0
		self.body_min_y = 16
		self.body_max_y = 128
		self.cycleCount = 0
		self.shotCycle = __class__.shotCycles[gcommon.GameSession.difficulty]

	def nextState(self):
		self.state += 1
		self.cnt = 0
		self.mode = 0
		self.modeCnt = 0

	def setState(self, state):
		self.state = state
		self.cnt = 0
		self.mode = 0
		self.modeCnt = 0

	def nextMode(self):
		self.mode += 1
		self.modeCnt = 0
	
	def setMode(self, mode):
		self.mode = mode
		self.modeCnt = 0

	def setBodyAnchorPos(self):
		self.body.x = self.x +20
		self.anchor.x = self.body.x -8
		self.anchor.y = self.body.y +16

	def update(self):
		if self.state == 0:
			self.x -= 1
			if self.x <= 256 -88:
				self.nextState()
			self.body.x = self.x +20
			self.anchor.x = self.body.x -8
			self.anchor.y = self.body.y +16
		elif self.state == 1:
			if self.cnt > 30:
				self.nextState()
		elif self.state == 2:
			if self.mode == 0:
				# 上に移動
				self.body.y -= 2
				if self.body.y < self.body_min_y:
					self.body.y = self.body_min_y
					self.setMode(1)
			elif self.mode == 1:
				# 下に移動
				self.body.y += 2
				if self.body.y > self.body_max_y:
					self.body.y = self.body_max_y
					self.nextState()
			self.setBodyAnchorPos()
		elif self.state == 3:
			# 下端からショットを打ちながら上端まで移動
			self.body.y -= 1
			if self.body.y < self.body_min_y:
				self.body.y = self.body_min_y
				self.nextState()
			elif self.cnt % self.shotCycle == 0:
				gcommon.ObjMgr.addObj(Boss3Shot(self.x, self.body.y+12, 4))
				gcommon.ObjMgr.addObj(Boss3Shot(self.x, self.body.y+37, 4))
				gcommon.sound(gcommon.SOUND_SHOT3)
				if self.cnt % int(self.shotCycle*2.5) == 0 and self.cycleCount & 1 == 1:
					enemy.enemy_shot_offset(self.x, self.body.y+23, 2, 0, -4)
					enemy.enemy_shot_offset(self.x, self.body.y+23, 2, 0, 4)
			self.setBodyAnchorPos()
		elif self.state == 4:
			cy = gcommon.getCenterY(gcommon.ObjMgr.myShip)
			if cy > self.body.y+25:
				self.body.y += 1
				if self.body.y > self.body_max_y:
					self.body.y = self.body_max_y
			elif cy < self.body.y+23:
				self.body.y -= 1
				if self.body.y < self.body_min_y:
					self.body.y = self.body_min_y

			self.setBodyAnchorPos()
			if self.cnt % self.shotCycle == 0:
				enemy.enemy_shot(self.x+20, self.y+27, 4, 0)
				enemy.enemy_shot(self.x+20, self.y+160-27, 4, 0)
				gcommon.sound(gcommon.SOUND_SHOT2)
			if self.cnt > 180:
				self.nextState()
		elif self.state == 5:
			if self.mode == 0:
				# アンカーが伸びる
				if self.modeCnt == 0:
					gcommon.sound(gcommon.SOUND_BOSS3_ANCHOR)
				self.anchor.x -= 8
				if self.anchor.x <= 0:
					self.anchor.x = 0
					self.nextMode()
			elif self.mode == 1:
				# アンカーが伸びきった
				if self.modeCnt > 30:
					self.nextMode()
				else:
					self.modeCnt += 1
			elif self.mode == 2:
				# アンカーが縮む
				self.anchor.x += 4
				if self.anchor.x >= self.body.x -8:
					self.anchor.x = self.body.x -8
					self.nextMode()
			elif self.mode == 3:
				if self.modeCnt > 30:
					self.nextState()
				else:
					self.modeCnt += 1
		elif self.state == 6:
			# 上に移動
			self.body.y -= 2
			if self.body.y < self.body_min_y:
				self.body.y = self.body_min_y
				self.nextState()
			self.setBodyAnchorPos()
		elif self.state == 7:
			# 上端からショットを打ちながら下端まで移動
			self.body.y += 1
			if self.body.y > self.body_max_y:
				self.body.y = self.body_max_y
				self.nextState()
			elif self.cnt % self.shotCycle == 0:
				gcommon.ObjMgr.addObj(Boss3Shot(self.x, self.body.y+12, 4))
				gcommon.ObjMgr.addObj(Boss3Shot(self.x, self.body.y+37, 4))
				gcommon.sound(gcommon.SOUND_SHOT2)
				if self.cnt % (self.shotCycle*2) == 0 and self.cycleCount & 1 == 1:
					enemy.enemy_shot_offset(self.x, self.body.y+23, 2, 0, -4)
					enemy.enemy_shot_offset(self.x, self.body.y+23, 2, 0, 4)
			self.setBodyAnchorPos()
		elif self.state == 8:
			# 中心に移動
			self.body.y -= 1
			if self.body.y < 72:
				self.body.y = 72
				self.nextState()
			self.setBodyAnchorPos()
		elif self.state == 9:
			# 体当たり・戻る
			if self.mode == 0:
				# 体当たり
				self.x -= 4
				if self.x <= -8:
					self.x = -8
					self.nextMode()
			elif self.mode == 1:
				# 左端まで移動した後の停止状態
				if self.modeCnt > 30:
					self.nextMode()
				else:
					self.modeCnt += 1
			elif self.mode == 2:
				# 戻る
				self.x += 2
				if self.x >= 256 -88:
					self.x = 256 -88
					self.setState(2)
					self.cycleCount += 1
			self.setBodyAnchorPos()

		# マップループ
		if gcommon.map_x >= 6800 + 256:
			gcommon.map_x -= 8*4

	def draw(self):
		xoffset = 0
		if self.cnt & 2 == 0:
			xoffset = -80
		# 上半分
		pyxel.blt(self.x, self.y, 1, 176 +xoffset, 224, 80, -32, gcommon.TP_COLOR)
		pyxel.blt(self.x+32, self.y+32, 1, 208, 176, 32, -48, gcommon.TP_COLOR)
		# 下半分
		pyxel.blt(self.x+32, self.y+80, 1, 208, 176, 32, 48, gcommon.TP_COLOR)
		pyxel.blt(self.x, self.y+128, 1, 176 +xoffset, 224, 80, 32, gcommon.TP_COLOR)
		# アンカー
		pyxel.blt(self.anchor.x, self.anchor.y, 1, 192, 112, 24, 16, gcommon.TP_COLOR)
		x = self.anchor.x +24
		while(x < self.body.x +8):
			pyxel.blt(x, self.anchor.y, 1, 216, 112, 16, 16, gcommon.TP_COLOR)
			x += 16

		# 本体
		pyxel.blt(self.body.x, self.body.y, 1, 208, 128, 48, 48, gcommon.TP_COLOR)

	# 自機弾と敵との当たり判定と破壊処理
	def checkShotCollision(self, shot):
		if shot.removeFlag:
			return False
		return gcommon.check_collision(self.body, shot)
	
	# def doShotCollision(self, shot):
	# 	rad = math.atan2(shot.dy, shot.dx)
	# 	enemy.Particle1.appendCenter(shot, rad)
	# 	self.hp -= shot.shotPower
	# 	if self.hp <= 0:
	# 		self.broken()
	# 		return True
	# 	else:
	# 		self.hit = True
	# 		return False
	
		# 自機と敵との当たり判定
	def checkMyShipCollision(self):
		if gcommon.check_collision(self.body, gcommon.ObjMgr.myShip):
			return True
		if gcommon.check_collision(self.anchor, gcommon.ObjMgr.myShip):
			return True
		if gcommon.check_collision2(self.x, self.y, self.upperARect, gcommon.ObjMgr.myShip):
			return True
		if gcommon.check_collision2(self.x, self.y, self.upperBRect, gcommon.ObjMgr.myShip):
			return True
		if gcommon.check_collision2(self.x, self.y, self.shaftRect, gcommon.ObjMgr.myShip):
			return True
		if gcommon.check_collision2(self.x, self.y, self.lowerBRect, gcommon.ObjMgr.myShip):
			return True
		if gcommon.check_collision2(self.x, self.y, self.lowerARect, gcommon.ObjMgr.myShip):
			return True
		return False

	def broken(self):
		self.remove()
		enemy.removeEnemyShot()
		gcommon.ObjMgr.objs.append(boss.BossExplosion(gcommon.getCenterX(self.body), gcommon.getCenterY(self.body), gcommon.C_LAYER_EXP_SKY))
		gcommon.GameSession.addScore(self.score)
		gcommon.sound(gcommon.SOUND_LARGE_EXP)
		gcommon.ObjMgr.objs.append(enemy.Delay(enemy.StageClear, [0,0,"3A"], 240))

class Boss3Shot(enemy.EnemyBase):
	# x,y 弾の中心を指定
	# dr  0 -63
	def __init__(self, x, y, speed):
		super(Boss3Shot, self).__init__()
		self.shotHitCheck = False
		self.x = x
		self.y = y -3
		self.speed = speed
		self.layer = gcommon.C_LAYER_E_SHOT
		self.left = 2
		self.top = 2
		self.right = 24 -2-1
		self.bottom = 4

	def update(self):
		self.x -= self.speed
		if self.x <=-24 or self.x >= gcommon.SCREEN_MAX_X or self.y<-16 or self.y >=gcommon.SCREEN_MAX_Y:
			self.removeFlag = True

		if gcommon.isMapFreePos(gcommon.getCenterX(self), gcommon.getCenterY(self)) == False:
			self.removeFlag = True

	def draw(self):
		# pyxel.rect(self.x+ self.left, self.y+self.top, self.right-self.left+1, self.bottom-self.top+1, 8)
		pyxel.blt(self.x, self.y, 1, 192, 96, 24, 8, gcommon.TP_COLOR)

