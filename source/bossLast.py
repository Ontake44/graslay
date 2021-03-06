import pyxel
import math
import random
import gcommon
import enemy
import boss

# レーザー移動砲台発射口
class BossLast1Launcher(enemy.EnemyBase):
	def __init__(self, x, y, flag):
		super(BossLast1Launcher, self).__init__()
		self.x = x
		self.y = y
		self.flag = flag
		self.layer = gcommon.C_LAYER_SKY
		self.ground = True
		self.hitCheck = False
		self.shotHitCheck = False
		self.enemyShotCollision = False

	def update(self):
		pass

	def draw(self):
		pyxel.blt(self.x, self.y, 2, 128, 64,  40, 16 * self.flag, 3)


class BossLast1(enemy.EnemyBase):
	coreTable = [[0,224],[64,224],[128,224],[192,224],[128,192],[64,192]]
	beamTable = [
		[[0,156],[0,43],[100,199],[83,0]],
		[[85,199],[0,38],[0,77],[0,117]],
		[[0,130],[9,0],[9,199],[0,68]],
	]
	launcherTable = [[38,24],[66,128+15],[66,49],[38,128+40]]
	table8 = [5,3,6,2,1,7,4,0]
	arrowDrTable = [1.0, 0.8, 1.2, 0.95, 1.1, 0.7, 1.05, 0.9, 1.3, 0.85, 1.15]
	initHp = boss.BOSS_LAST_1 + boss.BOSS_LAST_2 + boss.BOSS_LAST_3	# 5000		# 2000
	hp2 = boss.BOSS_LAST_2 + boss.BOSS_LAST_3 # 3500			# 1900
	hp3 = boss.BOSS_LAST_3	# 1500			# 1700
	def __init__(self, t):
		super(BossLast1, self).__init__()
		self.x = 256
		self.y = 0
		self.left = 52
		self.top = 80
		self.right = 111
		self.bottom = 111
		self.hp = BossLast1.initHp
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.ground = True
		self.score = 20000
		self.exptype = gcommon.C_EXPTYPE_GRD_BOSS
		# 破壊状態
		self.brokenState = 0
		self.coreBrightState = 0
		self.coreBrightness = 0
		self.shotType = 3
		self.beamIndex = 0
		self.cycleCount = 0
		# 本体ビームカウント
		self.cycleCount2 = 0
		self.beam1List = [None] * 4
		self.beam2 = None
		self.roundBeam = None
		# ボスの攻撃形態
		self.mode = 0
		self.coreX = self.x +32+16+32
		self.coreY = self.y +64+16+16
		# コアの回転角度
		self.rad = 0.0
		self.subState = 0
		self.subCnt = 0
		self.arrowRad = math.pi
		self.omega = 0.0
		self.random = gcommon.ClassicRand()
		pyxel.image(2).load(0,0,"assets/graslay_last-3.png")
		# 移動ビーム砲台発射口
		gcommon.ObjMgr.addObj(BossLast1Launcher(self.x, self.y, -1))
		gcommon.ObjMgr.addObj(BossLast1Launcher(self.x, self.y +176, 1))

	def nextState(self):
		self.state += 1
		self.cnt = 0
		self.subState = 0
		self.subCnt = 0

	def setState(self, state):
		self.state = state
		self.cnt = 0
		self.subState = 0
		self.subCnt = 0

	def nextSubState(self):
		self.subState += 1
		self.subCnt = 0

	def setSubState(self, subState):
		self.subState = subState
		self.subCnt = 0

	def update(self):
		if self.mode == 0:
			self.updateMode0()
		elif self.mode == 1:
			self.updateMode1()
		else:
			self.updateMode2()

	def updateMode0(self):
		self.coreX = self.x +32+16+32
		self.coreY = self.y +64+16+16
		if self.state == 0:
			if self.x <= 256-112:
				# スクロール停止
				gcommon.scroll_flag = False
				self.nextState()
		elif self.state == 1:
			if self.cnt > 40:
				self.nextState()
		elif self.state == 2:
			if self.cnt % 25 == 1:
				count = 5
				n = self.cnt & 3
				if n == 0:
					enemy.ContinuousShot.create(self.x + 38, self.y +24, self.shotType, count, 5, 4)
				elif n == 1:
					enemy.ContinuousShot.create(self.x + 66, self.y +128+15, self.shotType, count, 5, 4)
				elif n == 2:
					enemy.ContinuousShot.create(self.x + 66, self.y +49, self.shotType, count, 5, 4)
				elif n == 3:
					enemy.ContinuousShot.create(self.x + 38, self.y +128+40, self.shotType, count, 5, 4)
				if gcommon.GameSession.isHard():
					self.shotType = 1 + (self.shotType + 1) % 3
			if self.cnt> 100:
				self.nextState()
		
		elif self.state == 3:
			# ４箇所からのビーム
			if self.cnt == 1:
				for i in range(4):
					start = BossLast1.launcherTable[i]
					pos = BossLast1.beamTable[self.beamIndex][i]
					self.beam1List[i] = BossLastBeam1(self.x + start[0], self.y +start[1], pos[0], pos[1])
					gcommon.ObjMgr.addObj(self.beam1List[i])
				self.beamIndex += 1
				if self.beamIndex >=len(BossLast1.beamTable):
					self.beamIndex = 0
			else:
				if self.beam1List[0].removeFlag:
					self.nextState()
		
		elif self.state == 4:
			if self.cycleCount % 3 == 2:
				self.nextState()
			else:
				self.setState(2)	
			self.cycleCount += 1

		elif self.state == 5:
			# 本体ビーム
			if self.cnt == 1:
				self.beam2 = BossLastBeam2(180, 96, (self.cycleCount2 & 1 != 0))
				gcommon.ObjMgr.addObj(self.beam2)
				self.cycleCount2 += 1
			else:
				if self.beam2.removeFlag:
					if self.cycleCount2 & 2 != 0:
						self.nextState()
					else:
						self.setState(2)	

		elif self.state == 6:
			# レーザー砲台射出
			if gcommon.GameSession.difficulty == gcommon.DIFFICULTY_EASY:
				rate = 80
			elif gcommon.GameSession.difficulty == gcommon.DIFFICULTY_NORMAL:
				rate = 60
			else:
				rate = 40
			if self.cnt % rate == 1:
				gcommon.ObjMgr.objs.append(BossLastBattery1(156, 192, -1))
			elif self.cnt % rate == int(rate/2)+1:
				gcommon.ObjMgr.objs.append(BossLastBattery1(156, -16, 1))
			if self.cnt > 200:				
				self.setState(2)	
		self.rad = (self.rad + math.pi/60) % (math.pi * 2)
		
	def updateMode1(self):
		self.coreX = self.x +32+16+32
		self.coreY = self.y +64+16+16
		if self.state == 0:
			if self.x <= 256-112:
				# スクロール停止
				gcommon.scroll_flag = False
				self.nextState()
		elif self.state == 1:
			if self.cnt > 60:
				self.nextState()
		elif self.state == 2:
			# ダイアモンドショットホーミング射出
			if gcommon.GameSession.difficulty == gcommon.DIFFICULTY_EASY:
				count = 20
			elif gcommon.GameSession.difficulty == gcommon.DIFFICULTY_NORMAL:
				count = 15
			else:
				count = 8
			if self.cnt % count == 0:
				n = BossLast1.table8[int(self.cnt /8) & 7]
				gcommon.ObjMgr.addObj(BossLastDiamondShot(self.x +32+16+32, self.y +64+16+16+8, 24 -n*2))
				gcommon.ObjMgr.addObj(BossLastDiamondShot(self.x +32+16+32, self.y +64+16+16-8, 40 +n*2))
			if self.cnt > 300:
				self.nextState()
		elif self.state == 3:
			if self.cnt > 30:
				self.nextState()
		elif self.state == 4:
			# # 矢型の弾
			# if self.cnt & 3 == 0:
			# 	self.arrowRad = math.pi + math.pi * (self.random.rand() % 100 -50)/120
			# 	gcommon.ObjMgr.addObj(BossLastArrowShot(self.x +32+16+32, self.y +64+16+16, self.arrowRad))
			# ひし形弾
			if gcommon.GameSession.difficulty == gcommon.DIFFICULTY_EASY:
				count = 12
			elif gcommon.GameSession.difficulty == gcommon.DIFFICULTY_NORMAL:
				count = 8
			else:
				count = 5
			if self.cnt % count == 0:
				gcommon.ObjMgr.addObj(BossLastFallShotGroup(self.x +32+16+32, self.y +64+16+16,
					math.pi + math.pi * (self.random.rand() % 100 -50)/120, 
					(self.random.rand() % 120 -60)/800, 5))
			if self.cnt > 240:
				self.nextState()
		elif self.state == 5:
			if self.cnt == 1:
				self.roundBeam = BossLastRoundBeam(self.x +32+16+32, self.y +64+16+16)
				gcommon.ObjMgr.addObj(self.roundBeam)
			if self.roundBeam != None and self.roundBeam.removeFlag:
				self.setState(2)

		self.rad = (self.rad + math.pi/60) % (math.pi * 2)

	def updateMode2(self):
		if self.state == 0:
			if self.cnt > 120:
				self.nextState()
		elif self.state == 1:
			# 右の画面外に移動
			if self.cnt == 1:
				enemy.Splash.appendDr(self.coreX, self.coreY -8, gcommon.C_LAYER_SKY, math.pi, math.pi/6, 20)
				enemy.Splash.appendDr(self.coreX -16, self.coreY, gcommon.C_LAYER_SKY, math.pi, math.pi/6, 20)
				enemy.Splash.appendDr(self.coreX, self.coreY +8, gcommon.C_LAYER_SKY, math.pi, math.pi/6, 20)
			if self.coreX < 300:
				self.coreX += 4
			if self.cnt == 120:
				gcommon.scroll_flag = True
				# ボスコアを生成
				gcommon.ObjMgr.addObj(BossLast1Core(self.coreX, self.coreY))
				gcommon.ObjMgr.addObj(enemy.Delay(BossLastBaseExplosion, [], 240))
				gcommon.BGM.play(gcommon.BGM.BOSS_LAST)
		if self.x <= -160:
			self.remove()

		self.rad = (self.rad + math.pi/30) % (math.pi * 2)


	def draw(self):
		# 上
		pyxel.blt(self.x, self.y, 2, 96, 0,  160, -64, 3)
		# 中

		# コア部分
		if self.brokenState in (1, 2):
			gcommon.setBrightnessWithoutBlack(self.coreBrightness)
			BossLast1Core.drawCore(self.coreX, self.coreY, self.rad)
			pyxel.pal()
			if self.cnt & 3 == 0:
				if self.coreBrightState == 0:
					self.coreBrightness += 1
					if self.coreBrightness >= 4:
						self.coreBrightState = 1
				else:
					self.coreBrightness -= 1
					if self.coreBrightness <= -3:
						self.coreBrightState = 0
		pyxel.blt(self.x +32, self.y +64, 2, 0, 128, 96, 64, 3)
		if self.brokenState in (0,1):
			if self.hit:
				gcommon.setBrightnessWithoutBlack(1)
			pyxel.blt(self.x +32, self.y +64, 2, 0, self.brokenState* 64, 96, 64, 3)
			pyxel.pal()
		# 下
		pyxel.blt(self.x, self.y +128, 2, 96, 0, 160, 64, 3)

	def checkShotCollision(self, shot):
		ret = super(BossLast1, self).checkShotCollision(shot)
		#if ret:
		#	rad = math.atan2(shot.dy, shot.dx)
		#	enemy.Particle1.appendCenter(shot, rad)
		if self.mode == 0:
			if self.brokenState == 0 and self.hp < BossLast1.hp2:
				# 初期状態⇒先端が欠けた状態
				self.brokenState = 1
				enemy.create_explosion(self.x +32+32, self.y +64+16+16, gcommon.C_LAYER_GRD, gcommon.C_EXPTYPE_GRD_M)
				gcommon.GameSession.addScore(1000)
			elif self.brokenState == 1 and self.hp < BossLast1.hp3:
				# 先端が欠けた状態⇒コアむき出し状態
				self.brokenState = 2
				self.mode = 1
				self.setState(0)
				self.removeAllShot()
				enemy.create_explosion(self.x +32+32, self.y +64+16+16, gcommon.C_LAYER_GRD, gcommon.C_EXPTYPE_GRD_M)
				enemy.Splash.append(self.x +32+32+24, self.y +64+16+16, gcommon.C_LAYER_EXP_SKY)
				gcommon.GameSession.addScore(3000)
		return ret

	def broken(self):
		self.mode = 2
		self.setState(0)
		self.hitCheck = False
		self.shotHitCheck = False
		self.removeAllShot()
		enemy.removeEnemyShot()
		gcommon.sound(gcommon.SOUND_LARGE_EXP)
		enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
		gcommon.GameSession.addScore(self.score)

	def removeAllShot(self):
		enemy.removeEnemyShot()
		for i in range(len(self.beam1List)):
			obj = self.beam1List[i]
			if obj != None and obj.removeFlag == False:
				self.beam1List[i].remove()
				self.beam1List[i] = None
		if self.beam2 != None and self.beam2.removeFlag == False:
			self.beam2.remove()
			self.beam2 = None
		if self.roundBeam != None and self.roundBeam.removeFlag == False:
			self.roundBeam.remove()
			self.roundBeam = None

class BossLastBeam1(enemy.EnemyBase):
	beamPoints = [[0,0],[6,-6],[300,-6],[300,6],[6,6]]
	def __init__(self, sx, sy, ex, ey):
		super(BossLastBeam1, self).__init__()
		self.sx = sx
		self.sy = sy
		self.ex = ex
		self.ey = ey
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.ground = False
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False
		self.polygonList1 = []
		self.polygonList1.append(gcommon.Polygon(BossLastBeam1.beamPoints, 10))
		self.rad = math.atan2(ey -sy, ex -sx)
		self.xpolygonList1 = None
		self.xpolygonList2 = None
		self.xpolygonList3 = None
		self.size = 0

	def update(self):
		if self.state == 0:
			if self.cnt > 30:
				self.nextState()
		else:
			# 1からはポリゴンで描く
			if self.state == 1:
				self.size += 0.05
				if self.size >= 1.0:
					self.size = 1.0
				if self.cnt > 45:
					self.nextState()
			else:
				self.size -= 0.05
				if self.size <= 0:
					self.remove()
					return
			self.xpolygonList1 = gcommon.getAnglePolygons2([self.sx, self.sy], self.polygonList1, [0,0], self.rad, 1, self.size)
			self.xpolygonList2 = gcommon.getAnglePolygons2([self.sx, self.sy], self.polygonList1, [0,0], self.rad, 1, self.size*0.8)
			self.xpolygonList3 = gcommon.getAnglePolygons2([self.sx, self.sy], self.polygonList1, [0,0], self.rad, 1, self.size/2)

	# 自機と敵との当たり判定
	def checkMyShipCollision(self):
		if self.xpolygonList1 == None:
			return False
		pos = gcommon.getCenterPos(gcommon.ObjMgr.myShip)
		if gcommon.checkCollisionPointAndPolygon(pos, self.xpolygonList1.polygons[0].points):
			return True
		return False

	def draw(self):
		if self.state == 0:
			pyxel.line(self.sx, self.sy, self.ex, self.ey, pyxel.frame_count & 15)
		else:
			if self.xpolygonList1 == None:
				return
			if self.cnt & 2 == 0:
				self.xpolygonList1.polygons[0].clr = 9
				self.xpolygonList2.polygons[0].clr = 10
				self.xpolygonList3.polygons[0].clr = 7
			else:
				self.xpolygonList1.polygons[0].clr = 8
				self.xpolygonList2.polygons[0].clr = 9
				self.xpolygonList3.polygons[0].clr = 10
			gcommon.drawPolygons(self.xpolygonList1)
			gcommon.drawPolygons(self.xpolygonList2)
			gcommon.drawPolygons(self.xpolygonList3)

#
# 本体からの極太ビーム
class BossLastBeam2(enemy.EnemyBase):
	beamPoints = [[0,0],[6,-6],[300,-6],[300,6],[6,6]]
	def __init__(self, x, y, flag):
		super(BossLastBeam2, self).__init__()
		self.x = x
		self.y = y
		self.flag = flag		# 最初にどっちに向くか
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.ground = False
		self.hitCheck = False
		self.shotHitCheck = False
		self.enemyShotCollision = False
		self.polygonList1 = []
		self.polygonList1.append(gcommon.Polygon(BossLastBeam2.beamPoints, 10))
		self.rad = math.pi
		self.xpolygonList1 = None
		self.xpolygonList2 = None
		self.xpolygonList3 = None
		self.size = 0
		self.omega = math.pi/120
		self.angle = math.pi * 0.25
	
	def update(self):
		if self.flag:
			if self.state == 0:
				self.size += 0.05
				if self.size >= 0.125:
					self.size = 0.125
				if self.cnt > 45:
					self.hitCheck = True
					self.nextState()
			elif self.state == 1:
				self.size += 0.05
				if self.size >= 2.0:
					self.size = 2.0
				if self.cnt > 45:
					self.nextState()
			elif self.state == 2:
				if self.cnt > 30:
					self.nextState()
			elif self.state == 3:
				self.rad -= self.omega
				if self.rad < (math.pi -self.angle):
					self.nextState()
			elif self.state == 4:
				self.rad += self.omega
				if self.rad > (math.pi +self.angle):
					self.nextState()
			elif self.state == 5:
				self.rad -= self.omega
				if self.rad <= math.pi:
					self.rad = math.pi
					self.nextState()
			else:
				self.size -= 0.05
				if self.size <= 0:
					self.remove()
		else:
			if self.state == 0:
				self.size += 0.05
				if self.size >= 0.125:
					self.size = 0.125
				if self.cnt > 45:
					self.hitCheck = True
					self.nextState()
			elif self.state == 1:
				self.size += 0.05
				if self.size >= 2.0:
					self.size = 2.0
				if self.cnt > 45:
					self.nextState()
			elif self.state == 2:
				if self.cnt > 30:
					self.nextState()
			elif self.state == 3:
				self.rad += self.omega
				if self.rad > (math.pi +self.angle):
					self.nextState()
			elif self.state == 4:
				self.rad -= self.omega
				if self.rad < (math.pi -self.angle):
					self.nextState()
			elif self.state == 5:
				self.rad += self.omega
				if self.rad >= math.pi:
					self.rad = math.pi
					self.nextState()
			else:
				self.size -= 0.05
				if self.size <= 0:
					self.remove()
		if self.removeFlag == False:
			self.xpolygonList1 = gcommon.getAnglePolygons2([self.x, self.y], self.polygonList1, [0,0], self.rad, 1, self.size)
			self.xpolygonList2 = gcommon.getAnglePolygons2([self.x, self.y], self.polygonList1, [0,0], self.rad, 1, self.size*0.8)
			self.xpolygonList3 = gcommon.getAnglePolygons2([self.x, self.y], self.polygonList1, [0,0], self.rad, 1, self.size/2)
			if self.cnt & 1 == 0:
				if self.rad > math.pi * 1.05:
					x = self.x - ((self.y -8)/ math.tan(self.rad))
					if x > 0:
						enemy.create_explosion(x, 4 + random.randrange(8), gcommon.C_LAYER_EXP_SKY, gcommon.C_EXPTYPE_GRD_M)
				elif self.rad < math.pi * 0.95:
					x = self.x + ((184 -self.y)/ math.tan(self.rad))
					if x > 0:
						enemy.create_explosion(x, 184 + random.randrange(8), gcommon.C_LAYER_EXP_SKY, gcommon.C_EXPTYPE_GRD_M)

	# 自機と敵との当たり判定
	def checkMyShipCollision(self):
		if self.xpolygonList1 == None:
			return False
		pos = gcommon.getCenterPos(gcommon.ObjMgr.myShip)
		if gcommon.checkCollisionPointAndPolygon(pos, self.xpolygonList1.polygons[0].points):
			return True
		return False

	def draw(self):
		if self.cnt & 2 == 0:
			self.xpolygonList1.polygons[0].clr = 9
			self.xpolygonList2.polygons[0].clr = 10
			self.xpolygonList3.polygons[0].clr = 7
		else:
			if self.state > 0:
				self.xpolygonList1.polygons[0].clr = 8
				self.xpolygonList2.polygons[0].clr = 9
				self.xpolygonList3.polygons[0].clr = 10
		gcommon.drawPolygons(self.xpolygonList1)
		gcommon.drawPolygons(self.xpolygonList2)
		gcommon.drawPolygons(self.xpolygonList3)

# ラスボス 移動レーザー砲台
class BossLastBattery1(enemy.EnemyBase):
	def __init__(self, x, y, flag):
		super(BossLastBattery1, self).__init__()
		self.x = x
		self.y = y
		self.flag = flag		# -1:上向き  1:下向き
		self.left = 2
		self.top = 2
		self.right = 13
		self.bottom = 13
		self.hp = 500
		self.score = 200
		self.layer = gcommon.C_LAYER_GRD
		self.ground = False
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False

	def update(self):
		if self.state == 0:
			self.y += self.flag
			if self.cnt > 20:
				self.nextState()
		else:
			self.x -= 2
			if self.x <= -16:
				self.remove()
				return
			if self.cnt % 30 == (15 + self.flag * 5):
				gcommon.ObjMgr.addObj(BossLastBattery1Beam(self.x, self.y, 4 * self.flag))

	def draw(self):
		pyxel.blt(self.x, self.y, 2, 96, 64, 16, -16 *self.flag, 3)

class BossLastBattery1Beam(enemy.EnemyBase):
	def __init__(self, x, y, dy):
		super(BossLastBattery1Beam, self).__init__()
		self.x = x
		self.y = y
		self.dy = dy		# 
		self.left = 7
		self.top = 1
		self.right = 8
		self.bottom = 14
		self.layer = gcommon.C_LAYER_SKY
		self.ground = False
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False

	def update(self):
		self.y += self.dy
		if self.y <= -16:
			self.remove()

	def draw(self):
		pyxel.blt(self.x, self.y, 2, 112, 64, 16, 16, 3)

# ひし形ボス弾（ビームという呼称は間違っている）
class BossLastDiamondBeam(enemy.EnemyBase):
	points1 = [[0, 3],[11,0],[11,6]]
	points2 = [[11,0],[11,6],[22,3]]
	def __init__(self, x, y, dr):
		super(BossLastDiamondBeam, self).__init__()
		self.x = x
		self.y = y
		self.dr = dr
		self.left = -2
		self.top = -2
		self.right = 2
		self.bottom = 2
		self.layer = gcommon.C_LAYER_SKY
		self.ground = False
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.speed = 3.0
		self.polygons = [gcommon.Polygon(BossLastDiamondBeam.points1, 12), gcommon.Polygon(BossLastDiamondBeam.points2, 6)]

	def update(self):
		if self.cnt & 2 == 0 and self.cnt <= 63:
			tempDr = gcommon.get_atan_no_to_ship(self.x +11, self.y +11)
			if self.dr == -1:
				self.dr = tempDr
			else:
				rr = tempDr - self.dr
				if rr == 0:
					pass
				elif  (tempDr - self.dr) > 0:
					self.dr = (self.dr + 1) & 63
				else:
					self.dr = (self.dr - 1) & 63
		if self.cnt < 30:
			self.speed *= 0.97
		elif self.cnt < 60 and self.speed < 5:
			self.speed *= 1.1

		self.x += gcommon.cos_table[self.dr] * self.speed
		self.y += gcommon.sin_table[self.dr] * self.speed
		#if self.speed < 6:
		#	self.speed += 0.05
		if self.x <= -24 or self.x > gcommon.SCREEN_MAX_X:
			self.remove()
		elif self.y <= -24 or self.y > gcommon.SCREEN_MAX_Y:
			self.remove()

	def draw(self):
		gcommon.drawPolygons(gcommon.getAnglePolygons([self.x, self.y], self.polygons, [11, 3], gcommon.atan_table[self.dr]))

# ダイアモンド型のホーミングミサイル
class BossLastDiamondShot(enemy.EnemyBase):
	# 8方向のスプライトインデックスとX,Y方向+-
	# 全体は16方向だが、残り8方向は全く同じなのでこれを使う
	patternList = [[0,1,1],[1,1,1],[2,1,1],[3,1,1],[4,1,1],[3,-1,1],[2,-1,1],[1,-1,1]]
	def __init__(self, x, y, dr64):
		super(BossLastDiamondShot, self).__init__()
		self.x = x
		self.y = y
		self.dr = dr64		# 64方向インデックス
		self.left = -2
		self.top = -2
		self.right = 2
		self.bottom = 2
		self.layer = gcommon.C_LAYER_SKY
		self.ground = False
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.hp = 1
		self.score = 20
		self.speed = 3.0
		self.particleTable = []


	def update(self):
		if self.cnt & 2 == 0 and self.cnt <= 63:
			tempDr = gcommon.get_atan_no_to_ship(self.x +11, self.y +11)
			if self.dr == -1:
				self.dr = tempDr
			else:
				rr = tempDr - self.dr
				if rr == 0:
					pass
				elif  (tempDr - self.dr) > 0:
					self.dr = (self.dr + 1) & 63
				else:
					self.dr = (self.dr - 1) & 63
		if self.cnt < 30:
			self.speed *= 0.97
		elif self.cnt < 60 and self.speed < 5:
			self.speed *= 1.1

		#if self.cnt & 15 == 15:
		#	enemy.Particle1.append(self.x, self.y, gcommon.atan_table[self.dr] + math.pi)

		self.x += gcommon.cos_table[self.dr] * self.speed
		self.y += gcommon.sin_table[self.dr] * self.speed
		#if self.speed < 6:
		#	self.speed += 0.05
		if self.x <= -24 or self.x > gcommon.SCREEN_MAX_X:
			self.remove()
			return
		elif self.y <= -24 or self.y > gcommon.SCREEN_MAX_Y:
			self.remove()
			return
		self.updateParticle()

	def updateParticle(self):
		if self.cnt & 3 == 0:
			r = gcommon.atan_table[self.dr] + random.random() * math.pi/4 - math.pi/8 + math.pi
			speed = random.random() * 6
			s = enemy.SplashItem(self.x, self.y, speed * math.cos(r), speed * math.sin(r), random.randrange(10, 50))
			self.particleTable.append(s)
		newTbl = []
		for s in self.particleTable:
			s.cnt -= 1
			if s.cnt > 0:
				newTbl.append(s)
				s.x += s.dx
				s.y += s.dy
				s.dx *= 0.97
				s.dy *= 0.97
		self.particleTable = newTbl

	def drawParticle(self):
		for s in self.particleTable:
			n = (s.life - s.cnt)/ s.life
			if n > 0.5:
				if s.cnt & 1 == 0:
					continue
			elif n > 0.6:
				if s.cnt & 3 != 0:
					continue
			elif n > 0.8:
				if s.cnt & 7 != 0:
					continue
			pyxel.pset(s.x, s.y, 7)

	def draw(self):
		#gcommon.drawPolygons(gcommon.getAnglePolygons([self.x, self.y], self.polygons, [11, 3], gcommon.atan_table[self.dr]))
		p  = BossLastDiamondShot.patternList[((self.dr+2)>>2) & 7]
		#p  = BossLastDiamondShot.patternList[(self.cnt>>2) & 7]
		pyxel.blt(self.x -11, self.y -11, 2, p[0] * 24, 216, 24 * p[1], -24 * p[2], 3)
		self.drawParticle()

class BossLastArrowShot(enemy.EnemyBase):
	points1 = [[23,7],[0,14],[14,7]]
	points2 = [[23,7],[14,7],[0,0]]
	def __init__(self, x, y, dr):
		super(BossLastArrowShot, self).__init__()
		self.x = x
		self.y = y
		self.dr = dr		# ラジアン
		self.left = -2
		self.top = -2
		self.right = 2
		self.bottom = 2
		self.layer = gcommon.C_LAYER_SKY
		self.ground = False
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False
		self.speed = 4.0
		self.polygons = [gcommon.Polygon(BossLastArrowShot.points1, 10), gcommon.Polygon(BossLastArrowShot.points2, 7)]
	def update(self):
		self.x += math.cos(self.dr) * self.speed
		self.y += -math.sin(self.dr) * self.speed
		if self.x <= -24:
			self.remove()
			return
		elif self.y <= -24 or self.y > gcommon.SCREEN_MAX_Y + 24:
			self.remove()
			return

	def draw(self):
		gcommon.drawPolygons(gcommon.getAnglePolygons([self.x, self.y], self.polygons, [0, 7], -self.dr))

# ひし形の弾。回るように動く
class BossLastFallShot(enemy.EnemyBase):
	points = [[11,0],[0,7],[11,14],[22,7]]
	def __init__(self, x, y, rad, omega):
		super(BossLastFallShot, self).__init__()
		self.x = x
		self.y = y
		self.omega = omega		# 角速度（ラジアン）
		self.left = -2
		self.top = -2
		self.right = 2
		self.bottom = 2
		self.layer = gcommon.C_LAYER_SKY
		self.ground = False
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False
		self.hp = 1
		self.score = 20
		self.speed = 4.0
		self.rad = rad		#math.pi
		self.clr = 8
	def update(self):
		self.x += math.cos(self.rad) * self.speed
		self.y += -math.sin(self.rad) * self.speed
		self.rad += self.omega
		if self.cnt > 20:
			self.shotHitCheck = True
			self.clr = 7
		if self.x <= -8 or self.x > gcommon.SCREEN_MAX_X + 8:
			self.remove()
			return
		elif self.y <= -8 or self.y > gcommon.SCREEN_MAX_Y + 8:
			self.remove()
			return
		if self.cnt > 120:
			self.remove()

	def draw(self):
		#pyxel.circb(self.x, self.y, 8, 7)
		xpoints = gcommon.getAnglePoints([self.x, self.y], BossLastFallShot.points, [11,7], -self.rad)
		gcommon.drawQuadrangleB(xpoints, self.clr)

class BossLastStraightBeam(enemy.EnemyBase):
	def __init__(self, x, y):
		super(BossLastStraightBeam, self).__init__()
		self.x = x -7.5
		self.y = y -1
		self.left = 2
		self.top = 1
		self.right = 13
		self.bottom = 1
		self.layer = gcommon.C_LAYER_SKY
		self.ground = False
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False
		self.speed = 4.0
	def update(self):
		self.x -= self.speed
		if self.x <= -16:
			self.remove()
			return
	def draw(self):
		pyxel.blt(self.x, self.y, 2, 72, 192, 16, 3, 3)

class BossLastFallShotGroup(enemy.EnemyBase):
	def __init__(self, x, y, rad, omega, count):
		super(BossLastFallShotGroup, self).__init__()
		self.x = x
		self.y = y
		self.rad = rad
		self.omega = omega		# 角速度（ラジアン）
		self.count = count
		self.left = -2
		self.top = -2
		self.right = 2
		self.bottom = 2
		self.layer = gcommon.C_LAYER_SKY
		self.ground = False
		self.hitCheck = False
		self.shotHitCheck = False
		self.enemyShotCollision = False
	def update(self):
		if self.cnt & 3 == 0:
			gcommon.ObjMgr.addObj(BossLastFallShot(self.x, self.y, self.rad, self.omega))
			self.count -= 1
			if self.count <= 0:
				self.remove()
	def draw(self):
		pass

# ラスボスのコア
class BossLast1Core(enemy.EnemyBase):
	def __init__(self, x, y):
		super(BossLast1Core, self).__init__()
		self.x = x
		self.y = y
		self.left = -8
		self.top = -8
		self.right = 8
		self.bottom = 8
		self.layer = gcommon.C_LAYER_SKY
		self.ground = False
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.hp = boss.BOSS_LAST_CORE_HP
		self.score = 50000
		self.rad = 0.0
		#self.dx = 0.0
		#self.dy = 0.0
		self.radY = 0.0
		self.angle = 0.0
		self.random = None
		self.roundRad = 0.0
		self.roundCount = 0
		self.cycleCount = 0
		self.coreBrightState = 0
		self.coreBrightness = 0

	@classmethod
	def drawLine(cls, cx, cy, r):
		radius = 14
		y = cy - radius * math.sin(r)
		y2 = cy - radius * math.sin(r - math.pi/2.0)
		if r <= math.pi*0.25:
			clr = 5
		elif r <= math.pi*0.5:
			clr = 12
		elif r <= math.pi*0.75:
			clr = 6
		else:
			clr = 5
		pyxel.line(cx -32, cy, cx -8, y, clr)
		pyxel.line(cx -8, y, cx +8, y, clr)
		pyxel.line(cx +8, y, cx +32, cy, clr)
		if r >math.pi*0.75 and r <= math.pi * 1.75:
			pass
		else:
			#if r <= math.pi*0.25:
			#	clr = 5
			#elif r <= math.pi*0.5:
			#	clr = 12
			#elif r <= math.pi*0.75:
			#	clr = 6
			#else:
			#	clr = 5
			pyxel.line(cx -8, y, cx -8, y2, clr)
			pyxel.line(cx +8, y, cx +8, y2, clr)

	@classmethod
	def drawLineAngle(cls, cx, cy, r, angle):
		points = []
		radius = 14
		y = -radius * math.sin(r)
		y2 = -radius * math.sin(r - math.pi/2.0)
		if r <= math.pi*0.25:
			clr = 5
		elif r <= math.pi*0.5:
			clr = 12
		elif r <= math.pi*0.75:
			clr = 6
		else:
			clr = 5
		#pyxel.line(cx -32, cy, cx -8, y, clr)
		#pyxel.line(cx -8, y, cx +8, y, clr)
		#pyxel.line(cx +8, y, cx +32, cy, clr)
		points.append([-32, +0])
		points.append([-8, +y])
		points.append([+8, +y])
		points.append([+32, +0])
		xpoints = gcommon.getAnglePoints([cx, cy], points, [0,0], angle)
		gcommon.drawConnectedLines(xpoints, clr)
		if r >math.pi*0.75 and r <= math.pi * 1.75:
			pass
		else:
			#pyxel.line(cx -8, y, cx -8, y2, clr)
			#pyxel.line(cx +8, y, cx +8, y2, clr)
			points = [[-8, y], [-8, y2], [+8, y], [+8, y2]]
			xpoints = gcommon.getAnglePoints([cx, cy], points, [0,0], angle)
			gcommon.drawLines(xpoints, clr)

	@classmethod
	def drawCore(cls, x, y, rad):
		BossLast1Core.drawCoreAngle(x, y, rad, 0.0)

	@classmethod
	def drawCoreAngle(cls, x, y, rad, angle):
		# 玉の後ろ
		for i in range(4):
			r = rad + i * math.pi/2.0
			if r >= math.pi * 2:
				r -= math.pi * 2
			if r >= math.pi*0.5 and r < math.pi*1.5:
				#BossLast1Core.drawLine(x, y, r)
				BossLast1Core.drawLineAngle(x, y, r, angle)
		pyxel.blt(x -9, y -9, 2, 0, 192, 18, 18, 3)
		# 玉の前
		for i in range(4):
			r = rad + i * math.pi/2.0
			if r >= math.pi * 2:
				r -= math.pi * 2
			if r < math.pi*0.5 or r >= math.pi*1.5:
				#BossLast1Core.drawLine(x, y, r)
				BossLast1Core.drawLineAngle(x, y, r, angle)

	def update(self):
		if self.state == 0:
			if self.cnt & 7 == 0:
				gcommon.cur_scroll_x += 0.25
				if gcommon.cur_scroll_x > 6.0:
					gcommon.cur_scroll_x = 6.0
					self.nextState()
		elif self.state == 1:
			self.x -= 1
			if self.x < 220:
				self.x = 220
				self.nextState()
		elif self.state == 2:
			if self.cnt == 0:
				self.radY = math.pi/2.0
				self.random = gcommon.ClassicRand()
			self.y += 4.2 * math.sin(self.radY)
			self.radY += math.pi/60
			if gcommon.GameSession.difficulty == gcommon.DIFFICULTY_EASY:
				count = 18
			elif gcommon.GameSession.difficulty == gcommon.DIFFICULTY_NORMAL:
				count = 15
			else:
				count = 7
			if self.cnt % (self.random.rand() % count +3) == 0:
				gcommon.ObjMgr.addObj(BossLastStraightBeam(self.x -16, self.y))
			if self.cnt > 240:
				self.nextState()
		elif self.state == 3:
			# 位置補正
			if self.cnt == 0:
				self.angle = 0.0
			if (96 -self.y) > 2:
				self.y += 2
			elif (96 -self.y) < -2:
				self.y -= 2
			else:
				self.nextState()
		elif self.state == 4:
			# ぐるぐる自機の周りを回りながら攻撃
			if self.cnt == 0:
				self.roundRad = 0.0
				self.roundCount = 0
			self.x = 128 + 92 * math.cos(self.roundRad)
			self.angle = (self.angle + math.pi/20) % (math.pi*2)
			if self.cycleCount & 1 == 0:
				self.y = 96 + 80 * math.sin(self.roundRad)
				workAngle = self.angle
			else:
				self.y = 96 - 80 * math.sin(self.roundRad)
				workAngle = -self.angle
			self.roundRad +=  math.pi/180
			if self.roundRad >= math.pi*2:
				self.roundRad -= math.pi*2
				self.roundCount += 1
				if self.roundCount >= 2:
					self.setState(2)
					self.angle = 0.0
					self.cycleCount += 1
			if gcommon.GameSession.difficulty == gcommon.DIFFICULTY_EASY:
				count = 15
			elif gcommon.GameSession.difficulty == gcommon.DIFFICULTY_NORMAL:
				count = 10
			else:
				count = 5
			if self.cnt % count == 0:
				gcommon.ObjMgr.addObj(boss.BossLaserBeam1(self.x +math.cos(workAngle)* 24, self.y +math.sin(workAngle) * 24, workAngle))
				gcommon.ObjMgr.addObj(boss.BossLaserBeam1(self.x -math.cos(workAngle)* 24, self.y -math.sin(workAngle) * 24, workAngle + math.pi))
		self.rad = (self.rad + math.pi/30) % (math.pi * 2)

	def draw(self):
		gcommon.setBrightnessWithoutBlack(self.coreBrightness)
		if self.cycleCount & 1 == 0:
			BossLast1Core.drawCoreAngle(self.x, self.y, self.rad, self.angle)
		else:
			BossLast1Core.drawCoreAngle(self.x, self.y, self.rad, -self.angle)
		pyxel.pal()
		if self.cnt & 3 == 0:
			if self.coreBrightState == 0:
				self.coreBrightness += 1
				if self.coreBrightness >= 4:
					self.coreBrightState = 1
			else:
				self.coreBrightness -= 1
				if self.coreBrightness <= -3:
					self.coreBrightState = 0		

	# def checkShotCollision(self, shot):
	# 	ret = super(BossLast1Core, self).checkShotCollision(shot)
	# 	if ret:
	# 		rad = math.atan2(shot.dy, shot.dx)
	# 		enemy.Particle1.appendCenter(shot, rad)

	def broken(self):
		self.setState(100)
		self.shotHitCheck = False
		enemy.removeEnemyShot()
		gcommon.ObjMgr.objs.append(boss.BossExplosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
		gcommon.GameSession.addScore(self.score)
		self.remove()
		gcommon.sound(gcommon.SOUND_LARGE_EXP)
		enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
		gcommon.ObjMgr.addObj(enemy.Delay(enemy.StageClear, [0,0,6], 240))

# ぐるぐる螺旋ビーム
class BossLastRoundBeam(enemy.EnemyBase):
	def __init__(self, x, y):
		super(BossLastRoundBeam, self).__init__()
		self.x = x
		self.y = y
		self.left = -2
		self.top = -2
		self.right = 2
		self.bottom = 2
		self.layer = gcommon.C_LAYER_GRD | gcommon.C_LAYER_UPPER_SKY
		self.ground = False
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False
		self.radOffset = 0.0
		self.limit = 240
		self.beamRadStart = 0.0
		self.beamRadDelta = 0.0
		self.listArray = [None] * 12
		self.stateCycle = 0
	def update(self):
		#self.radOffset -= math.pi * 0.05
		#if self.radOffset < 0:
		#	self.radOffset += 2 * math.pi
		self.radOffset += math.pi * 0.02
		if self.radOffset > 2 * math.pi:
			self.radOffset -= 2 * math.pi
		if self.state == 0:
			if self.limit >= -10:
				self.limit -= 2
			else:
				self.nextState()
		elif self.state == 1:
			if self.cnt > 40:
				self.nextState()
				self.beamRadStart = 0.0
		elif self.state == 2:
			if self.beamRadDelta > -math.pi/120:
				self.beamRadDelta -= (math.pi/120/30)
			if self.beamRadStart < math.pi*0.35:
				 self.beamRadStart += math.pi/200
			if self.cnt > 150:
				self.nextState()
		elif self.state == 3:
			if self.beamRadDelta < math.pi/120:
				self.beamRadDelta += (math.pi/120/30)
			if self.beamRadStart > -math.pi*0.35:
				 self.beamRadStart -= math.pi/200
			if self.cnt > 150:
				self.stateCycle += 1
				if self.stateCycle == 3:
					self.setState(10)
				else:
					self.setState(2)
		elif self.state == 10:
			if self.beamRadDelta > 0:
				self.beamRadDelta -= (math.pi/120/30)
			self.beamRadStart += math.pi/200
			if self.beamRadStart >= 0:
				self.nextState()
		elif self.state == 11:
			if self.limit < 240:
				self.limit += 2
			else:
				self.remove()

		# 描画準備
		rad = self.radOffset
		x2 = self.x
		r = 0
		beamRad = self.beamRadStart
		px = self.x
		py = self.y
		count = 0
		for i in range(len(self.listArray)):
			self.listArray[i] = []
		while(x2 > self.limit and count < 50):
			#y2 = py - math.sin(rad) * r
			
			pos = gcommon.getAngle(0, - math.sin(rad) * r, beamRad)
			x2 = px + pos[0]
			y2 = py + pos[1]
			
			n = int(rad / (math.pi/6)) % 12
			#print(str(n))
			if gcommon.isMapFreePos(x2, y2) == False and self.cnt & 3 == 0:
				enemy.create_explosion(x2, y2, gcommon.C_LAYER_GRD, gcommon.C_EXPTYPE_GRD_S)
			self.listArray[n].append([x2, y2])
			# 奥から描画するために反転する
			if n in (8,9):
				self.listArray[n].reverse()
			
			rad += math.pi/4
			if rad > math.pi*2:
				rad -= math.pi*2
			if r < 40:
				r += 2
			px += (math.cos(beamRad)* -8)
			py += (math.sin(beamRad)* -8)
			beamRad += self.beamRadDelta
			count += 1
		
	def drawLayer(self, layer):
		if (layer & gcommon.C_LAYER_GRD) != 0:
			for i in range(0,2):
				self.drawBeam(self.listArray[i], 0)
			for i in range(10,12):
				self.drawBeam(self.listArray[i], 0)
			for i in range(2,4):
				self.drawBeam(self.listArray[i], 1)
			for i in range(9,8,-1):
				self.drawBeam(self.listArray[i], 1)
		elif (layer & gcommon.C_LAYER_UPPER_SKY) != 0:
			for i in range(4,8):
				self.drawBeam(self.listArray[i], 2)

	def drawBeam(self, list, clr):
		for pos in list:
			#pyxel.circ(pos[0], pos[1], 8, clr)
			pyxel.blt(pos[0] -7, pos[1] -7, 2, 24 +clr * 16, 192, 16, 16, 3)



	# 自機と敵との当たり判定
	def checkMyShipCollision(self):
		myPos : [float] = gcommon.getCenterPos(gcommon.ObjMgr.myShip)
		for i in [2,3, 8, 9]:
			for pos in self.listArray[i]:
				d = gcommon.get_distance_pos2(myPos, pos)
				if d < 6:
					return True
		return False

# 最終ステージ脱出時の基地爆発
class BossLastBaseExplosion(enemy.EnemyBase):
	def __init__(self, t):
		super(BossLastBaseExplosion, self).__init__()
		self.layer = gcommon.C_LAYER_SKY
		self.ground = False
		self.hitCheck = False
		self.shotHitCheck = True
		self.enemyShotCollision = False

	def update(self):
		if self.cnt % 3 == 0:
			obj = gcommon.ObjMgr.addObj(enemy.Explosion(32 +random.randrange(64), random.randrange(gcommon.SCREEN_MAX_Y), gcommon.C_LAYER_GRD, gcommon.C_EXPTYPE_SKY_M))
			obj.particle = False
			if self.cnt < 120:
				# 120超えるとサウンドなし
				gcommon.sound(gcommon.SOUND_MID_EXP)
