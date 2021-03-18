import pyxel
import math
import random
import gcommon
import enemy
import boss

class Boss1Base(enemy.EnemyBase):
	def __init__(self, t):
		super(Boss1Base, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.left = 16
		self.top = 16
		self.right = 79
		self.bottom = 45
		self.hp = 999999
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.ground = True
		self.shotHitCheck = False	# 自機弾との当たり判定
		self.hitCheck = False	# 自機と敵との当たり判定
		self.enemyShotCollision = False	# 敵弾との当たり判定を行う
		self.posY = 0

	def update(self):
		if self.x <= -96:
			self.remove()
			return
		if self.cnt > 210:
			if self.posY < 64:
				 self.posY += 1

	def draw(self):
		# 上
		pyxel.blt(self.x, self.y -self.posY -40, 1, 160, 128, 96, -64, gcommon.TP_COLOR)
		# 下
		pyxel.blt(self.x, self.y +31 +self.posY, 1, 160, 128, 96, 64, gcommon.TP_COLOR)
 

class Boss1(enemy.EnemyBase):
	beamTimes = (45, 60, 90)
	def __init__(self, t):
		super(Boss1, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.left = 16
		self.top = 16
		self.right = 93
		self.bottom = 45
		self.hp = 999999
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.score = 5000
		self.subcnt = 0
		self.hitcolor1 = 9
		self.hitcolor2 = 10
		self.brake = False
		self.beam = 0
		self.subState = 0
		self.isLeft = True
		self.beamTime = __class__.beamTimes[gcommon.GameSession.difficulty]
		gcommon.debugPrint("beam Time = " + str(self.beamTime))
		self.tbl = []
		self.beamObj = Boss1Beam(self)
		gcommon.ObjMgr.addObj(self.beamObj)

	def update(self):
		# 向き
		self.isLeft = (self.x + 52) > gcommon.ObjMgr.myShip.x
		self.beam = 0
		if self.state == 0:
			self.x -= gcommon.cur_scroll_x
			if self.cnt % 60 == 0:
				self.shotFix4()
			if self.cnt > 260:
				self.nextState()
		elif self.state == 1:
			self.x -= gcommon.cur_scroll_x
			self.x += 0.625
			self.y -= 0.20		#0.125
			if self.cnt % 60 == 0:
				self.shotFix4()
			if self.cnt > 270:
				self.nextState()
		elif self.state == 2:
			self.y += 0.25
			if self.cnt % 60 == 0:
				self.shotFix4()
			if self.cnt > 120:
				self.nextState()
				self.hp = boss.BOSS_1_HP
		elif self.state == 3:
			# ４、８方向ショット
			if self.subState == 0:
				self.y -= 0.250
				if self.y < 0:
					self.y = 0
			else:
				self.y += 0.250
				if self.y > 150:
					self.y = 150
			if self.cnt & 15 == 15:
				if gcommon.GameSession.isNormalOrLess():
					self.shotFix4()
				else:
					self.shotFix8()
				#if self.cnt & 31 == 31:
				#	self.shotFix4()
				#else:
			if self.cnt > 120:
				self.nextState()
				gcommon.sound(gcommon.SOUND_BOSS1PREBEAM)
				if self.subState == 0:
					self.subState = 1
				else:
					self.subState = 0
		elif self.state == 4:
			# ビーム発射前
			if self.cnt & 1 == 1:
				x = 50 + random.random() * 30
				y = random.random() * 6
				a = 200 + random.random() * 500
				if self.cnt & 3 == 3:
					a *= -1
				self.tbl.append(Boss1Star(x, y, a))

			newTbl = []
			for s in self.tbl:
				s.x -= 2
				if s.x>=0:
					newTbl.append(s)
			self.tbl = newTbl

			if self.cnt > self.beamTime:
				self.nextState()
				gcommon.sound(gcommon.SOUND_BOSS1BEAM)
		elif self.state == 5:
			# ビーム発射開始（移動なし）
			self.beam = int(self.cnt/3) +1
			if self.beam > 5:
				self.nextState()
		elif self.state == 6:
			# ビーム発射中（移動なし）
			self.beam = 6
			self.beamObj.hitCheck = True
			if self.cnt > 60:
				self.nextState()
		elif self.state == 7:
			# ビーム発射中（移動あり）
			self.beam = 6
			zy = abs(self.y +30 - gcommon.ObjMgr.myShip.y)
			if zy > 80:
				dy = 3
			elif zy > 50:
				dy = 2
			elif zy > 20:
				dy = 1
			else:
				dy = 0.25
			if self.y +30 > gcommon.ObjMgr.myShip.y:
				dy = -dy
			self.y += dy
			if self.cnt > self.beamTime:
				self.nextState()
		elif self.state == 8:
			# ビーム発射終了（移動なし）
			self.beam = 5- int(self.cnt/3)
			self.beamObj.hitCheck = False
			if self.beam < 0:
				self.state = 3
				self.cnt = 0
	def draw(self):
		if self.state == 4:
			for s in self.tbl:
				y = s.x* s.x/s.a
				pyxel.pset(self.x -s.x, self.y +28 -y + s.y, 7)
		# 本体
		pyxel.blt(self.x, self.y+8, 1, 160, 208, 40, 48, gcommon.TP_COLOR)
		if self.isLeft:
			pyxel.blt(self.x +40, self.y+8 , 1, 200, 208, 32, 48, gcommon.TP_COLOR)
		else:
			pyxel.blt(self.x +40, self.y+8, 1, 128, 136, 32, 48, gcommon.TP_COLOR)
		pyxel.blt(self.x +72, self.y , 1, 232, 200, 24, 56, gcommon.TP_COLOR)
		if self.beam >= 1 and self.beam <=5:
			bx = self.x -12
			while(bx > -8):
				pyxel.blt(bx, self.y +10, 1, (self.beam-1) * 8, 208, 8, 40, gcommon.TP_COLOR)
				bx -=8
			
		if self.beam == 6:
			# ビーーーーーーーーーーーーーーーム！！！
			pyxel.blt(self.x -16, self.y +10, 1, 144, 208, 16, 40, gcommon.TP_COLOR)
			bx = self.x -32
			sx = 128 - ((self.cnt>>1) & 3) * 16
			while(bx > -32):
				pyxel.blt(bx, self.y +10, 1, sx, 208, 16, 40, gcommon.TP_COLOR)
				bx -=16

	def getDirection(self, dr64):
		if self.isLeft:
			return dr64
		else:
			return gcommon.getMirrorDr64(dr64)

	def shotFix4(self):
		ox = 0 if self.isLeft else 8
		enemy.enemy_shot_dr(self.x +48 +ox*2, self.y +22, 4, 1, self.getDirection(33))
		enemy.enemy_shot_dr(self.x +52 +ox, self.y +16, 4, 1, self.getDirection(37))
		enemy.enemy_shot_dr(self.x +48 +ox*2, self.y +42, 4, 1, self.getDirection(31))
		enemy.enemy_shot_dr(self.x +52 +ox, self.y +48, 4, 1, self.getDirection(27))
		gcommon.sound(gcommon.SOUND_SHOT2)

	def shotFix8(self):
		ox = 0 if self.isLeft else 8
		enemy.enemy_shot_dr(self.x +48 +ox*2, self.y +22, 2, 0, self.getDirection(31))
		enemy.enemy_shot_dr(self.x +48 +ox*2, self.y +22, 2, 0, self.getDirection(33))
		
		enemy.enemy_shot_dr(self.x +52 +ox, self.y +16, 2, 0, self.getDirection(35))
		enemy.enemy_shot_dr(self.x +52 +ox, self.y +16, 2, 0, self.getDirection(37))
		
		enemy.enemy_shot_dr(self.x +48 +ox*2, self.y +42, 2, 0, self.getDirection(31))
		enemy.enemy_shot_dr(self.x +48 +ox*2, self.y +42, 2, 0, self.getDirection(33))
		
		enemy.enemy_shot_dr(self.x +52 +ox, self.y +48, 2, 0, self.getDirection(27))
		enemy.enemy_shot_dr(self.x +52 +ox, self.y +48, 2, 0, self.getDirection(29))
		gcommon.sound(gcommon.SOUND_SHOT2)

	def broken(self):
		self.setState(100)
		self.shotHitCheck = False
		self.beamObj.remove()
		enemy.removeEnemyShot()
		gcommon.ObjMgr.objs.append(boss.BossExplosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
		gcommon.GameSession.addScore(self.score)
		self.remove()
		gcommon.sound(gcommon.SOUND_LARGE_EXP)
		enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
		gcommon.ObjMgr.objs.append(enemy.Delay(enemy.StageClear, [0,0,1], 240))


# 波動砲発射前の、あの吸い込むようなやつ
class Boss1Star:
	def __init__(self, x, y, a):
		self.x = x
		self.y = y
		self.a = a
		self.removeFlag = False


class Boss1Beam(enemy.EnemyBase):
	def __init__(self, bossObj):
		super(Boss1Beam, self).__init__()
		self.bossObj = bossObj
		self.hitCheck = False
		self.shotHitCheck = False
	
	def update(self):
		self.x = 0
		self.y = self.bossObj.y + 10
		self.right = self.bossObj.x
		self.bottom = 39

	def draw(self):
		pass

