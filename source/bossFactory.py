import pyxel
import math
import random
import gcommon
import enemy
import boss

class BossFactoryShot1(enemy.EnemyBase):
	def __init__(self, x, y):
		super(BossFactoryShot1, self).__init__()
		self.x = x
		self.y = y
		self.dr = -1
		self.left = 5
		self.top = 5
		self.right = 17
		self.bottom = 17
		self.hp = 15
		self.layer = gcommon.C_LAYER_E_SHOT
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.speed = 1
		self.image = 2
		self.imageX = 0
		self.imageY = 96
		self.maxSpeed = 4 if gcommon.GameSession.isHard() else 3

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
		self.x += gcommon.cos_table[self.dr] * self.speed
		self.y += gcommon.sin_table[self.dr] * self.speed
		if self.speed < 4:
			self.speed += 0.05
		if self.x <= -24 or self.x > gcommon.SCREEN_MAX_X:
			self.remove()
		elif self.y <= -24 or self.y > gcommon.SCREEN_MAX_Y:
			self.remove()


	def draw(self):
		if self.cnt & 2 == 2:
			pyxel.blt(self.x, self.y, self.image, self.imageX, self.imageY, 24, 24, gcommon.TP_COLOR)
		else:
			pyxel.blt(self.x, self.y, self.image, self.imageX +24, self.imageY, 24, 24, gcommon.TP_COLOR)


bossFactoryFin1 = [
	[10, 0],
	[2, 23],
	[9, 26],
	[23, 26],
	[31, 23],
	[23, 0]
]

bossFactoryFin2 = [
	[2, 23],
	[1, 26],
	[7, 30],
	[26, 30],
	[32, 26],
	[31, 23]
]

# clr = 10 黄色の左横
bossFactoryFinA1 = [
	[10, 0],	[1, 25],	[15, 15]
]
# clr = 10 黄色の上
bossFactoryFinA2 = [
	[10, 0],	[16, 10],	[23, 0]
]
# clr = 4  茶色の左下
bossFactoryFinA3 = [
	[1, 26],	[7, 30],	[10, 21]
]
# clr = 4  茶色の真ん中
bossFactoryFinA4 = [
	[7, 30],	[26, 30],	[16.5, 7]
]
# clr = 4  茶色の右下
bossFactoryFinA5 = [
	[26, 30],	[21, 21],	[32, 26]
]
# clr = 4  茶色の右横
bossFactoryFinA6 = [
	[32, 26],	[15, 12],	[23, 0]
]
# clr = 9  オレンジの正面
bossFactoryFinA7 = [
	[12, 3],	[5, 23],	[8, 25],	[24, 25],	[28, 23],	[21, 3]
]

class BossFactory(enemy.EnemyBase):
	def __init__(self, t):
		super(BossFactory, self).__init__()
		self.x = 80
		self.y = -120
		self.layer = gcommon.C_LAYER_SKY
		self.left = 27
		self.top = 8
		self.right = 87
		self.bottom = 45
		self.hp = boss.BOSS_FACTORY_HP
		self.score = 15000
		self.subState = 0
		self.subCnt = 0
		self.hitcolor1 = 9
		self.hitcolor2 = 10
		self.shotHitCheck = True	# 自機弾との当たり判定
		self.hitCheck = True	# 自機と敵との当たり判定
		self.enemyShotCollision = False	# 敵弾との当たり判定を行う
		#self.xpoints1 = []
		#self.xpoints2 = []
		# 回転角度
		self.rad = 0.0
		self.omega = math.pi/64		# 角速度
		# フィンの距離
		self.distance = 22.0
		self.dx = 1
		self.dy = 2
		self.subStateCycle = 0
		# 移動状態
		self.moveState = 0		# 0:上に移動  1:下に移動
		# どちらを開くか
		self.finMode = 0
		self.polygonList = []
		self.polygonList.append(gcommon.Polygon(bossFactoryFinA1, 10))
		self.polygonList.append(gcommon.Polygon(bossFactoryFinA2, 10))
		self.polygonList.append(gcommon.Polygon(bossFactoryFinA3, 4))
		self.polygonList.append(gcommon.Polygon(bossFactoryFinA4, 4))
		self.polygonList.append(gcommon.Polygon(bossFactoryFinA5, 4))
		self.polygonList.append(gcommon.Polygon(bossFactoryFinA6, 4))
		self.polygonList.append(gcommon.Polygon(bossFactoryFinA7, 9))
		self.xpolygonsList = []
		self.firstCycle = True
		# 中心玉の半径
		self.centerRadius = 14
		# 移動方向
		self.moveDr64 = 0
		self.speed = 0
		self.stateCycle = 0
		# 回転ON/OFF
		self.rolling = True
		self.dr64 = 0

	def nextState(self):
		self.state += 1
		self.cnt = 0
		self.subState = 0
		self.subCnt = 0
		self.subStateCycle = 0

	def setState(self, state):
		self.state = state
		self.cnt = 0
		self.subState = 0
		self.subCnt = 0
		self.subStateCycle = 0

	def setSubState(self, subState):
		self.subCnt = 0
		self.subState = subState

	def update(self):
		self.subCnt += 1
		if self.rolling:
			self.rad += self.omega
		if self.rad >= math.pi/2:
			self.rad -= math.pi/2
		elif self.rad <= -math.pi/2:
			self.rad += math.pi/2

		if self.state == 0:
			if self.subState == 0:
				# 後ろから落下
				self.x += self.dx
				self.y += self.dy
				self.dy += 0.2
				if self.y > 80:
					# 跳ねる
					self.dy = -self.dy * 0.8
					for i in range(3):
						enemy.Particle1.append(self.x +39.5, self.y +88, -math.pi/4 -math.pi/4*i)
						#gcommon.ObjMgr.objs.append(
						#	enemy.Particle1(self.x +39.5, self.y +88, -math.pi/4 -math.pi/4*i))
				if self.x > 280:
					self.dx = -self.dx
					# 回転を逆にする
					self.omega = -math.pi/128
					self.setSubState(1)
			elif self.subState == 1:
				# 右端から戻ってくる
				self.x += self.dx
				self.y += self.dy
				self.dy += 0.2
				if self.y > 80:
					# 跳ねる
					self.dy = -self.dy
					for i in range(4):
						gcommon.ObjMgr.objs.append(
							enemy.Particle1(self.x +39.5, self.y +88, -math.pi/4 -math.pi/4*i, 8, 50))
				if self.x <= 152:
					self.omega = -math.pi/64
					self.setSubState(2)
			elif self.subState == 2:
				# 規定位置まで移動
				self.y -= 1
				if self.y < 50:
					self.y = 50
				if self.subCnt > 30:
					self.dx = 0
					self.dy = -2
					self.moveState = 0	# 0:上に移動
					self.nextState()
		elif self.state == 1:
			if self.subState == 0:
				if self.subCnt == 30:
					self.setSubState(1)
			elif self.subState == 1:
				# 開く
				self.distance += 0.5
				if self.distance > 38:
					self.setSubState(2)
			elif self.subState == 2:
				# 開いている（攻撃）
				if self.stateCycle & 1 == 0:
					# 最初（奇数）のサイクル
					if self.finMode == 0:
						if self.subCnt & 7 == 0:
							for i in range(4):
								enemy.enemy_shot(
									self.x +39.5 +math.cos(self.rad + math.pi/2 * i) * 32,
									self.y +39.5 +math.sin(self.rad + math.pi/2 * i) * 32,
									4, 0)
					else:
						if self.subCnt % 15 == 0:
							for i in range(4):
								# 自動追尾泡？ショット
								gcommon.ObjMgr.objs.append(
										BossFactoryShot1(
											self.x +39.5 +math.cos(self.rad + math.pi/4 + math.pi/2 * i) * 32,
											self.y +39.5 +math.sin(self.rad + math.pi/4 + math.pi/2 * i) * 32))
					if self.subCnt == 30:
						self.setSubState(3)
				else:
					# 偶数サイクル
					if self.finMode == 0:
						rr = 0
						if self.subCnt % 20 == 0:
							dr64 = gcommon.get_atan_no_to_ship(self.x +39.5, self.y +39.5)
							if self.subCnt % 40 == 0:
								for i in range(4):
									enemy.enemy_shot_dr(
										self.x +39.5 +math.cos(self.rad + rr + math.pi/2 * i) * 32,
										self.y +39.5 +math.sin(self.rad + rr +math.pi/2 * i) * 32,
										2.5, 0, dr64 -4)
									enemy.enemy_shot_dr(
										self.x +39.5 +math.cos(self.rad + rr + math.pi/2 * i) * 32,
										self.y +39.5 +math.sin(self.rad + rr +math.pi/2 * i) * 32,
										2.5, 0, dr64 +4)
							else:
								for i in range(4):
									enemy.enemy_shot_dr(
										self.x +39.5 +math.cos(self.rad + rr + math.pi/2 * i) * 32,
										self.y +39.5 +math.sin(self.rad + rr +math.pi/2 * i) * 32,
										3, 0, dr64)
					else:
						if self.subCnt % 15 == 0:
							for i in range(4):
								enemy.enemy_shot_offset(
									self.x +39.5 +math.cos(self.rad + math.pi/4 + math.pi/2 * i) * 32,
									self.y +39.5 +math.sin(self.rad + math.pi/4 + math.pi/2 * i) * 32,
									4, 0, 2)
								enemy.enemy_shot_offset(
									self.x +39.5 +math.cos(self.rad + math.pi/4 + math.pi/2 * i) * 32,
									self.y +39.5 +math.sin(self.rad + math.pi/4 + math.pi/2 * i) * 32,
									4, 0, -2)

					if self.subCnt == 64:
						self.setSubState(3)
			elif self.subState == 3:
				# 閉まる
				self.distance -= 0.5
				if self.distance < 22:
					self.distance = 22.0
					self.setSubState(0)
					self.finMode = (self.finMode + 1) & 1
					self.subStateCycle += 1
					self.firstCycle = False
					if self.subStateCycle > 4:
						self.nextState()
			# state:1での移動
			if self.subStateCycle > 1 and self.firstCycle == False:
				# 最初は移動しない
				if self.moveState == 0:
					# 上に移動
					self.y += self.dy
					if self.y < 30:
						self.dy += 0.05
						if self.dy >= 0.0:
							self.dy = 0.05
							self.moveState = 1
					elif self.dy > -2.0:
						self.dy -= 0.05
				else:
					# 下に移動
					self.y += self.dy
					if self.y > 100:
						self.dy -= 0.05
						if self.dy <= 0.0:
							self.dy = -0.05
							self.moveState = 0
					elif self.dy < 2.0:
						self.dy += 0.05
		elif self.state == 2:
			# 拡散ビーム
			if self.subState == 0:
				# 待ち
				if self.centerRadius >= 1:
					self.centerRadius -= 1
				if self.subCnt > 20:
					self.setSubState(1)
			elif self.subState == 1:
				# 拡散ビーム？
				if self.cnt & 7 == 7:
					rad = (self.stateCycle & 1) * 2 * math.pi/16
					for i in range(64):
						if i & 4 == 0:
							gcommon.ObjMgr.objs.append(
								boss.BossLaserBeam1(self.x +39.5, self.y + 39.5, rad))
						rad += 2 * math.pi/64
				if self.cnt > 60:
					self.setSubState(2)
			elif self.subState == 2:
				# 待ち
				if self.centerRadius < 14:
					self.centerRadius += 1
				if self.subCnt > 30:
					self.setState(3)
		elif self.state == 3:
			# 自機を追いかける
			if self.cnt == 1:
				self.speed = 0.0
				self.moveDr64 = -1
			if self.subState == 0:
				# 追いかける
				if self.cnt % 4 == 0 and self.cnt <= 30 * gcommon.GameSession.enemy_shot_rate:
					tempDr = gcommon.get_atan_no_to_ship(self.x +39.5, self.y +39.5)
					# 右左を決める
					if self.moveDr64 == -1:
						self.moveDr64 = tempDr
					else:
						self.moveDr64 = (self.moveDr64 + gcommon.get_leftOrRight(self.moveDr64, tempDr)) & 63
					self.speed += 0.5
					if self.speed >= 3.0:
						self.speed = 3.0
				self.x += gcommon.cos_table[self.moveDr64] * self.speed
				self.y += gcommon.sin_table[self.moveDr64] * self.speed
				#if self.x < 40 or self.y < 40 or (self.x + 40 > gcommon.SCREEN_MAX_X) or (self.y +40 > gcommon.SCREEN_MAX_Y):
				if self.subCnt > 120:
					self.setSubState(1)
			elif self.subState == 1:
				# 戻る
				if self.subCnt == 1:
					pass
					#print("self.subState == 1")
				if self.cnt & 2 == 0:
					# 右左を決める
					tempDr = gcommon.get_atan_no(self.x, self.y, 152, (gcommon.SCREEN_HEIGHT -80)/2)
					self.moveDr64 = (self.moveDr64 + gcommon.get_leftOrRight(self.moveDr64, tempDr)) & 63
				self.x += gcommon.cos_table[self.moveDr64] * self.speed
				self.y += gcommon.sin_table[self.moveDr64] * self.speed
				l = math.hypot(152 -self.x, (gcommon.SCREEN_HEIGHT -80)/2 -self.y)
				if l < 4:
					self.stateCycle += 1
					# ステート1に戻る
					self.setState(4)
				elif l < 50:
					self.speed -= 0.25
					if self.speed < 0.5:
						self.speed = 0.5
		elif self.state == 4:
			if self.subState == 0:
				# 開く
				if self.distance < 38:
					self.distance += 0.5
				#print("rad = " + str(self.rad))
				if self.distance >= 38 and abs(self.rad) <= math.pi/64 :
					self.rad = 0.0
					self.rolling = False
					self.setSubState(1)
					self.dr64 = -1
			elif self.subState == 1:
				#if self.dr64 == -1:
				#	self.dr64 = gcommon.get_atan_no_to_ship(xx, yy)
				# if self.subCnt & 7 == 0:
				# 	for i in range(4):
				# 		xx = self.x +39.5 +math.cos(self.rad + math.pi/4 + math.pi/2 * i) * 32
				# 		yy = self.y +39.5 +math.sin(self.rad + math.pi/4 + math.pi/2 * i) * 32
				# 		enemy.enemy_shot(xx, yy, 3, 0)
				if self.subCnt & 31 == 1:
					rr = 0 if self.finMode == 0 else math.pi/4
					n = 5 if gcommon.GameSession.isHard() else 4
					dr = gcommon.get_atan_no_to_ship(self.x +39.5, self.y +39.5)
					if self.subCnt & 32 == 0:
						#print("5")
						for i in range(4):
							enemy.enemy_shot_dr_multi(
								self.x +39.5 +math.cos(self.rad + rr +math.pi/2 * i) * 32,
								self.y +39.5 +math.sin(self.rad + rr +math.pi/2 * i) * 32,
								2, 0, dr, n, 6)
					else:
						#print("4")
						for i in range(4):
							enemy.enemy_shot_dr_multi(
								self.x +39.5 +math.cos(self.rad + rr +math.pi/2 * i) * 32,
								self.y +39.5 +math.sin(self.rad + rr +math.pi/2 * i) * 32,
								2, 0, dr, n -1, 4)

				if self.subCnt > 150:
					self.setSubState(2)
			elif self.subState == 2:
				# 閉まる
				self.distance -= 0.5
				if self.distance < 22:
					self.distance = 22.0
					# ステート1に戻る
					self.setState(1)
					self.rolling = True

		#self.xpoints1 = []
		#self.xpoints2 = []
		self.xpolygonsList = []
		# Finの座標計算
		for i in range(8):
			distance = 22.0
			if self.finMode == 0:
				if i & 1 == 0:
					distance = self.distance
			else:
				if i & 1 == 1:
					distance = self.distance
			#self.xpoints1.append(gcommon.getAnglePoints([self.x + 39.5, self.y +39.5],
			#	bossFactoryFin1, [15.5, -distance], self.rad + math.pi/4 *i))
			#self.xpoints2.append(gcommon.getAnglePoints([self.x + 39.5, self.y +39.5],
			#	bossFactoryFin2, [15.5, -distance], self.rad + math.pi/4 *i))
			self.xpolygonsList.append(gcommon.getAnglePolygons([self.x + 39.5, self.y +39.5],
				self.polygonList, [15.5, -distance], self.rad + math.pi/4 *i))
			#self.xpoints1.append(gcommon.getAnglePoints([self.x + 39.5, self.y +39.5],
			#	bossFactoryFin1, [15.5, -distance], self.rad + math.pi/4 *i))

	def draw(self):
		# 本体のドーナツ部
		pyxel.blt(self.x, self.y, 2, 64, 48, 80, 80, gcommon.TP_COLOR)

		# 中心の玉
		for i in range(4):
			pyxel.blt(
				self.x +39.5 +math.cos(self.rad + math.pi/2 * i) * self.centerRadius -7.5,
				self.y +39.5 +math.sin(self.rad + math.pi/2 * i) * self.centerRadius -7.5, 
				2, 0, 32, 16, 16, gcommon.TP_COLOR)

		# Finに隠れた砲台
		for i in range(8):
			if i & 1 == 0:
				pyxel.blt(
					self.x +39.5 +math.cos(self.rad + math.pi/4 * i) * 32 -7.5,
					self.y +39.5 +math.sin(self.rad + math.pi/4 * i) * 32 -7.5, 
					2, 16, 32, 16, 16, gcommon.TP_COLOR)
			else:
				pyxel.blt(
					self.x +39.5 +math.cos(self.rad + math.pi/4 * i) * 32 -7.5,
					self.y +39.5 +math.sin(self.rad + math.pi/4 * i) * 32 -7.5, 
					2, 32, 32, 16, 16, gcommon.TP_COLOR)

		# for p in self.xpoints2:
		# 	gcommon.drawPolygon(p, 4)
		# for p in self.xpoints1:
		# 	gcommon.drawPolygon2(p, 9, 4)
		for polygons in self.xpolygonsList:
			gcommon.drawPolygons(polygons)

	# 自機弾と敵との当たり判定と破壊処理
	def checkShotCollision(self, shot):
		if shot.removeFlag:
			return False
		hit = False
		pos = gcommon.getCenterPos(shot)
		if math.hypot(self.x+39.5-pos[0], self.y+39.5 -pos[1]) <40:
			hit = True
		if hit:
			rad = math.atan2(shot.dy, shot.dx)
			enemy.Particle1.appendCenter(shot, rad)
			gcommon.sound(gcommon.SOUND_HIT, gcommon.SOUND_CH2)
			self.hp -= shot.shotPower
			if self.hp <= 0:
				self.broken()
			else:
				self.hit = True
			return True
		else:
			return False

		# 自機と敵との当たり判定
	def checkMyShipCollision(self):
		pos = gcommon.getCenterPos(gcommon.ObjMgr.myShip)
		return math.hypot(self.x+39.5-pos[0], self.y+39.5 -pos[1]) <40

	def broken(self):
		self.remove()
		enemy.removeEnemyShot()
		gcommon.ObjMgr.objs.append(boss.BossExplosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
		gcommon.GameSession.addScore(self.score)
		gcommon.sound(gcommon.SOUND_LARGE_EXP)
		enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
		gcommon.ObjMgr.objs.append(enemy.Delay(enemy.StageClear, [0,0,5], 240))

