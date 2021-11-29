import pyxel
import math
import random
import gcommon
import enemy
from objMgr import ObjMgr
from audio import BGM
from drawing import Drawing

# ボス処理

BOSS_1_HP = 1200
BOSS_2_HP = 2800
BOSS_3_HP = 4000
BOSS_4_HP = 3500
BOSS_FACTORY_HP = 5500
BOSS_LAST_1 = 2000
BOSS_LAST_2 = 4000
BOSS_LAST_3 = 7000
BOSS_LAST_CORE_HP = 1200
BOSS_WAREHOUSE_HP = 9000
BOSS_CAVE_HP = 7000
BOSS_FIRE_HP = 4000
BOSS_BATTLESHIP_HP = 4000
BOSS_LABYRINTH_1 = 5000
BOSS_LABYRINTH_2 = 6000
BOSS_ENEMYBASE_1 = 3500
BOSS_ENEMYBASE_2 = 200
BOSS_ENEMYBASE_3 = 5000

# def remove_all_battery():
# 	for obj in ObjMgr.objs:
# 		if obj.t == gcommon.T_BATTERY1:
# 			obj.removeFlag = True

# def shot_cross(cx,cy,dr):
# 	for i in range(0,64,16):
# 		enemy.enemy_shot_dr(
# 			cx + math.cos(gcommon.atan_table[(i+dr) & 63])*8,
# 			cy + math.sin(gcommon.atan_table[(i+dr) & 63])*8,
# 			2*2, 1, (i+dr) & 63)


# def nextstate(self, cnt, nextstate):
# 	if self.cnt>cnt:
# 		self.state = nextstate
# 		self.cnt = 0


# def shot_radial(self, dr):
# 	#for i=1,64,4 do
# 	for i in range(0, 64, 4):
# 		enemy.enemy_shot_dr(
# 			self.x+32,
# 			self.y+18,
# 			2, 1, (i+dr) & 63)


class BossExplosion(enemy.EnemyBase):
	def __init__(self, cx, cy, layer):
		super(BossExplosion, self).__init__()
		self.t = gcommon.T_BOSSEXPLOSION
		self.x = cx
		self.y = cy
		self.layer = layer
		self.hitCheck = False
		self.shotHitCheck = False

	def update(self):
		if self.state == 0:
			if self.cnt == 0:
				BGM.sound(gcommon.SOUND_BOSS_EXP)
			elif self.cnt>120:
				#self.nextState()
				self.remove()
		elif self.state == 1:
			if self.cnt>40:
				self.remove()
		

	def draw(self):
		if self.state==0:
			pyxel.circb(self.x,
				self.y, self.cnt**1.2 * 2,7)
			#--circfill(self.x+(self.r-self.l)/2,
			#-- self.y+(self.b-self.u)/2, self.cnt,7)
			gcommon.circfill_obj_center(self, self.cnt**1.2, 7)
			gcommon.draw_splash(self)

		elif self.state==1:
			if self.cnt & 3 == 3:
				pyxel.rect(0, 0, 256, 256, 7)


class BossLaserBeam1(enemy.EnemyBase):
	beamPoints = [[0,2],[7,0],[14,2],[7,4]]
	#beamPoints = [[0,1],[7,0],[14,1],[7,2]]
	#beamPoints = [[0.0,1.5],[7.0,0.0],[14.0,1.5],[7.0,3.0]]
	def __init__(self, x, y, rad):
		super(BossLaserBeam1, self).__init__()
		self.x = x
		self.y = y
		self.rad = rad
		self.left = -2
		self.top = -2
		self.right = 2
		self.bottom = 2
		self.hp = 0
		self.layer = gcommon.C_LAYER_E_SHOT
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False
		self.dx = math.cos(self.rad) * 3
		self.dy = math.sin(self.rad) * 3
		self.polygonList = gcommon.getAnglePoints([0,0], __class__.beamPoints, [7,1], self.rad)
		#self.xpolygons = None

	def update(self):
		self.x += self.dx
		self.y += self.dy
		if self.x < -20 or self.x > 276:
			self.remove()
			return
		elif self.y < -20 or self.y > gcommon.SCREEN_MAX_Y + 20:
			self.remove()
			return
		#self.xpolygons = gcommon.getAnglePolygons([self.x, self.y], self.polygonList, [7,2], self.rad)

	def draw(self):
		if self.cnt & 2 == 0:
			Drawing.drawPolygonPos(self.x, self.y, self.polygonList, 7)
		else:
			Drawing.drawPolygonPos(self.x, self.y, self.polygonList, 10)

class MiddleBoss1(enemy.EnemyBase):
	def __init__(self, t):
		super(MiddleBoss1, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.left = 40
		self.top = 24
		self.right = 105
		self.bottom = 71
		self.hp = 700
		self.layer = gcommon.C_LAYER_SKY
		self.ground = False
		self.score = 1000
		self.exptype = gcommon.C_EXPTYPE_GRD_M
		self.dx = 0
		self.dy = 0
		self.moveState = 0
		self.moveCnt = 0
		self.moveCycle = 0

	def update(self):
		if self.state == 0:
			self.x -= 2
			if self.x <= 160:
				self.nextState()
		elif self.state == 1:
			if self.moveCycle & 2 == 0:
				if self.cnt % 40 == 0:
					if self.cnt % 80 == 0:
						for i in range(5):
							enemy.enemy_shot_offset(self.x +43, self.y +47, 3, 0, -4 + i * 2)
					else:
						for i in range(6):
							enemy.enemy_shot_offset(self.x +43, self.y +47, 3, 0, -6 + i * 2)
			else:
				if self.cnt % 30 == 0:
					if self.cnt % 70 == 0:
						for i in range(5):
							enemy.enemy_shot_offset(self.x +43, self.y +47, 3, 0, -4 + i * 2)
					else:
						for i in range(6):
							enemy.enemy_shot_offset(self.x +43, self.y +47, 3, 0, -6 + i * 2)
			if self.moveState == 0:
				# 上に移動
				self.y += self.dy
				if self.y < 40:
					self.dy += 0.05
					if self.dy >= 0.0:
						self.shotAll()
						self.dy = 0.05
						self.moveState = 1
						self.moveCnt = 0
				elif self.dy > -2.0:
					self.dy -= 0.05
			elif self.moveState == 1:
				# 待ち
				self.moveCnt += 1
				if self.moveCnt >= 20:
					self.moveState = 2
			elif self.moveState == 2:
				# 下に移動
				self.y += self.dy
				if self.y > 60:
					self.dy -= 0.05
					if self.dy <= 0.0:
						self.shotAll()
						self.dy = -0.05
						self.moveState = 3
						self.moveCnt = 0
				elif self.dy < 2.0:
					self.dy += 0.05			
			elif self.moveState == 3:
				# 待ち
				self.moveCnt += 1
				if self.moveCnt >= 20:
					self.moveState = 0
					self.moveCycle += 1
					if self.moveCycle >= 5:
						self.moveState = 4
			elif self.moveState == 4:
				# 上に移動
				self.y += self.dy
				if self.y < 70:
					self.dy += 0.05
					if self.dy >= 0.0:
						self.shotAll()
						self.dy = 0.05
						self.state = 2
				elif self.dy > -2.0:
					self.dy -= 0.05
		elif self.state == 2:
			self.x += self.dx
			if self.x <= -88:
				self.remove()
			elif self.dx >= -3:
				self.dx -= 0.05

	def shotAll(self):
		ObjMgr.addObj(MiddleBoss1Laser(self.x +39, self.y +7))
		ObjMgr.addObj(MiddleBoss1Laser(self.x +24, self.y +20))
		ObjMgr.addObj(MiddleBoss1Laser(self.x, self.y +33))
		ObjMgr.addObj(MiddleBoss1Laser(self.x, self.y +62))
		ObjMgr.addObj(MiddleBoss1Laser(self.x +24, self.y +75))
		ObjMgr.addObj(MiddleBoss1Laser(self.x +39, self.y +88))

	def draw(self):
		pyxel.blt(self.x,self.y, 2, 0, 80, 88, 96, 3)

	def broken(self):
		super(MiddleBoss1, self).broken()
		if gcommon.game_timer < 1940:
			gcommon.game_timer = 1940

class MiddleBoss1Laser(enemy.EnemyBase):
	def __init__(self, x, y):
		super(MiddleBoss1Laser, self).__init__()
		self.x = x
		self.y = y
		self.speed = 4
		self.left = 2
		self.top = 0
		self.right = 13
		self.bottom = 3
		self.layer = gcommon.C_LAYER_SKY
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False

	def update(self):
		self.x -= self.speed
		if self.x <= -16:
			self.remove()
	
	def draw(self):
		pyxel.blt(self.x, self.y, 2, 184, 0, 16, 4, gcommon.TP_COLOR)

class ChangeDirectionLaser1(enemy.EnemyBase):
	def __init__(self, x, y, rad, omega):
		super(__class__, self).__init__()
		self.x = x
		self.y = y
		self.rad = rad
		self.omega = omega
		self.speed = 1.0
		self.left = 0
		self.top = 0
		self.right = 0
		self.bottom = 0
		self.layer = gcommon.C_LAYER_E_SHOT
		self.ground = True
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False
		self.phase1Time = 20
		self.phase2Time = 20
		self.laserLength = 20
		# 終点へのオフセット
		self.edx = 0.0
		self.edy = 0.0
		self.cycleCount = 0

	def update(self):
		if self.state == 0:
			#gcommon.debugPrint("0:" + str(self.x) + " " + str(self.y))
			# 視点から伸びる
			self.left = -3
			self.top = -3
			self.right = 3
			self.bottom = 3
			self.edx = self.laserLength * math.cos(self.rad) * self.cnt / self.phase1Time
			self.edy = self.laserLength * math.sin(self.rad) * self.cnt / self.phase1Time
			if self.cnt >= self.phase1Time:
				self.nextState()

		elif self.state == 1:
			#gcommon.debugPrint("1:" + str(self.x) + " " + str(self.y))
			# 移動
			dx = math.cos(self.rad) * self.speed
			dy = math.sin(self.rad) * self.speed
			self.x += dx
			self.y += dy
			self.left = self.edx -3
			self.top = self.edy -3
			self.right = self.left +6
			self.bottom = self.top +6
			if self.cnt >= self.phase2Time:
				self.nextState()
		
		elif self.state == 2:
			#gcommon.debugPrint("2:" + str(self.x) + " " + str(self.y))
			# 終点に着き、縮む
			#   始点と終点が入れ替える
			if self.cnt == 0:
				self.x = self.x + self.edx
				self.y = self.y + self.edy
			self.edx = -self.laserLength * math.cos(self.rad) * (self.phase1Time -self.cnt) / self.phase1Time
			self.edy = -self.laserLength * math.sin(self.rad) * (self.phase1Time -self.cnt) / self.phase1Time
			self.left = -3
			self.top = -3
			self.right = self.left +6
			self.bottom = self.top +6
			if self.cnt >= self.phase1Time:
				self.cycleCount += 1
				if self.cycleCount >= 10:
					self.remove()
				else:
					self.rad += self.omega
					self.setState(0)


	def draw(self):
		x1 = self.x
		x2 = self.x + self.edx
		y1 = self.y
		y2 = self.y + self.edy
		pyxel.line(x1, y1 -1, x2, y2-1, 9)
		pyxel.line(x1, y1 +1, x2, y2+1, 9)
		pyxel.line(x1-1, y1, x2-1, y2, 9)
		pyxel.line(x1+1, y1, x2+1, y2, 9)
		pyxel.line(x1, y1, x2, y2, 10)
		sx = 48 if self.cnt & 4 == 0 else 56
		if self.state in (0,2):
			pyxel.blt(x1 -3, y1 -3, 2, sx, 120, 7, 7, 3)
		if self.state == 1:
			pyxel.blt(x2 -3, y2 -3, 2, sx, 120, 7, 7, 3)


class DelayedShotLaser1(enemy.EnemyBase):
	def __init__(self, x, y, rad):
		super(__class__, self).__init__()
		self.x = x
		self.y = y
		self.rad = rad
		self.speed = 2.0
		self.left = -3
		self.top = -3
		self.right = 3
		self.bottom = 3
		self.layer = gcommon.C_LAYER_E_SHOT
		self.ground = True
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False
		self.phase1Time = 20
		self.phase2Time = 20
		self.laserLength = 20
		self.dx = 0.0
		self.dy = 0.0
		self.cycleCount = 0
		self.ex = 0.0
		self.ey = 0.0

	def update(self):
		if self.state == 0:
			# 射出前
			if self.cnt >= self.phase1Time:
				self.dx = math.cos(self.rad) * self.speed
				self.dy = math.sin(self.rad) * self.speed
				self.ex = math.cos(self.rad) * 8
				self.ey = math.sin(self.rad) * 8
				self.x += self.ex
				self.y += self.ey
				self.nextState()

		elif self.state == 1:
			# 移動
			self.x += self.dx
			self.y += self.dy
			if self.x < -12 or self.x > gcommon.SCREEN_MAX_X +12 or self.y < -12 or self.y > gcommon.SCREEN_MAX_Y +12:
				self.remove()

		
	def draw(self):
		if self.state == 0:
			sx = 48 if self.cnt & 4 == 0 else 56
			pyxel.blt(self.x -3, self.y -3, 2, sx, 120, 7, 7, 3)
		else:
			x1 = self.x + self.ex
			x2 = self.x - self.ex
			y1 = self.y + self.ey
			y2 = self.y - self.ey
			pyxel.line(x1, y1 -1, x2, y2-1, 9)
			pyxel.line(x1, y1 +1, x2, y2+1, 9)
			pyxel.line(x1-1, y1, x2-1, y2, 9)
			pyxel.line(x1+1, y1, x2+1, y2, 9)
			pyxel.line(x1, y1, x2, y2, 10)

# 波動砲発射前の、あの吸い込むようなやつ
class BeamEffectStar:
	def __init__(self, x, y, a):
		self.x = x
		self.y = y
		self.a = a
		self.removeFlag = False

# 艦首ビーム発射前の吸い込むようなやつ
class BeamPrepareEffect1(enemy.EnemyBase):
	def __init__(self, parent, ox, oy):
		super(__class__, self).__init__()
		self.parent = parent
		self.offsetX = ox
		self.offsetY = oy
		self.layer = gcommon.C_LAYER_E_SHOT
		self.hitCheck = False
		self.shotHitCheck = False
		self.enemyShotCollision = False
		self.tbl = []
		self.imageSourceX = 160
		self.imageSourceY = 64
		self.starMax = 1

	def update(self):
		self.x = self.parent.x + self.offsetX
		self.y = self.parent.y + self.offsetY
		for i in range(self.starMax):
			x = 50 + random.random() * 30
			y = random.random() * 6
			a = random.random() * 0.007
			if self.cnt & 1 == 1:
				a *= -1
			self.tbl.append(BeamEffectStar(x, y, a))

		newTbl = []
		for s in self.tbl:
			s.x -= 2
			if s.x>=0:
				newTbl.append(s)
		self.tbl = newTbl
		self.starMax = 1 + int(self.cnt/20)
		if self.starMax > 6:
			self.starMax = 6
			

	def draw(self):
		if self.cnt & 3 == 0:
			pyxel.blt(self.x -22, self.y-7.5, 2, self.imageSourceX, self.imageSourceY, 24, 16, 0)
		elif self.cnt & 3 == 1:
			pyxel.blt(self.x -22, self.y-7.5, 2, self.imageSourceX, self.imageSourceY+16, 24, 16, 0)
		for s in self.tbl:
			y = s.x* s.x * s.a
			pyxel.pset(self.x -s.x, self.y -y, 7)
