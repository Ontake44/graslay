import pyxel
import math
import random
import gcommon
import enemy
import boss
import enemyShot
import enemyBattery
import drawing
from objMgr import ObjMgr
from gameSession import GameSession
from audio import BGM

# bossWarehouseOutline = [
# 	#[18,-1],[41, -1], [52, 10], [52, 31], [41, 42], [18, 42], [7, 30], [7, 10]
# 	[18, 0],[41, 0], [51, 10], [51, 31], [41, 41], [18, 41], [8, 31], [8, 10]
# ]

# # clr = 7 左上
# bossWarehouse0 = [
# 	[18, 0], [18, 10], [8, 10]
# ]
# # clr = 6
# bossWarehouse1 = [
# 	[18, 0], [41, 0], [51, 10], [18, 10]
# ]
# # clr = 5 右の部分
# bossWarehouse2 = [
# 	[41, 10], [51, 10], [51, 31], [41, 41]
# ]
# # clr = 12 左下
# bossWarehouse3 = [
# 	[18, 31], [18, 41], [8, 31]
# ]
# # clr = 5 下の部分
# bossWarehouse4 = [
# 	[18, 31], [51, 31], [41, 41], [18, 41]
# ]
# # clr = 6 左の部分
# bossWarehouse5 = [
# 	[17, 31], [8, 31], [8, 10], [17, 10]
# ]
# bossWarehouseUpper = [
# 	[18, 8], [41, 8], [43, 10], [43, 31], [41, 33], [18, 33], [16, 31], [16, 10]
# ]

# # # clr = 0
# # bossWarehouseGun0 = [
# # 	[0, 15], [23, 15], [23, 26], [0, 26]
# # ]
# # # clr = 5
# # bossWarehouseGun1 = [
# # 	[1, 16], [22, 16], [22, 25], [1, 25]
# # ]
# # # clr = 12
# # bossWarehouseGun2 = [
# # 	[1, 18], [22, 18], [22, 23], [1, 23]
# # ]
# # bossWarehouseGun3 = [
# # 	[1, 19], [22, 19], [22, 22], [1, 22]
# # ]
# # bossWarehouseGun4 = [
# # 	[1, 20], [22, 20], [22, 21], [1, 21]
# # ]
# # clr = 1
# bossWarehouseGun0 = [
# 	[4, 13], [14, 13], [14, 28], [4, 28]
# ]
# # clr = 5
# bossWarehouseGun1 = [
# 	[4, 14], [13, 14], [13, 19], [4, 19]
# ]
# # clr = 5
# bossWarehouseGun2 = [
# 	[4, 22], [13, 22], [13, 27], [4, 27]
# ]
# # clr = 12
# bossWarehouseGun3 = [
# 	[4, 15], [13, 15], [13, 18], [4, 18]
# ]
# # clr = 12
# bossWarehouseGun4 = [
# 	[4, 23], [13, 23], [13, 26], [4, 26]
# ]
# # clr = 7
# bossWarehouseGun5 = [
# 	[4, 16], [13, 16]
# ]
# # clr = 7
# bossWarehouseGun6 = [
# 	[4, 24], [13, 24]
# ]

# # clr = 6
# bossWarehouseGunUpper0 = [
# 	[21, 11], [25, 11], [31, 17], [18, 16]
# ]
# # clr = 5
# bossWarehouseGunUpper1 = [
# 	[18, 25], [31, 24], [25, 30], [21, 30]
# ]
# # clr = 1
# bossWarehouseGunUpper2 = [
# 	[21, 11], [22, 18], [22, 23], [21, 30], [18, 25], [18, 16]
# ]

# # clr = 1
# bossWarehouse4shot0 = [
# 	[0, 0], [7, 0], [7, 7], [0, 7]
# ]
# # clr = 5
# bossWarehouse4shot1 = [
# 	[1, 1], [6, 1], [6, 6], [1, 6]
# ]
# # clr = 6
# bossWarehouse4shot2 = [
# 	[1, 4], [6, 4], [6, 6], [1, 6]
# ]

class BossWarehouse(enemy.EnemyBase):
	moveTable = [
		[0, 5, 150, 95.5, 0.5], 	# 0 前進
		[50, -1],					# 1 砲台射出
		[0, 5, 200, 95.5, 0.5], 	# 2 後ろに下がる
		[120, -1],					# 3 射撃
		[0, 5, 150, 95.5 -64, 0.5],	# 4 前方上
		[120, -1],					# 5 砲台射出
		[0, 5, 200, 95.5 -64, 0.5],	# 6 後方上
		[120, -1],					# 7 射撃
		[0, 5, 150, 95.5+64, 0.5],	# 8 前方下
		[120, -1],					# 9 砲台射出
		[0, 5, 200, 95.5+64, 0.5],	# 10 後方下
		[120, -1],					# 11 射撃
	]
	pos4rads = [math.pi/5.0, -math.pi/5.0, math.pi -math.pi/5.0, math.pi +math.pi/5.0]
	shot4poss = [[-6, -16], [10, -16], [-6, 16], [10, 16]]
	def __init__(self, t):
		super(BossWarehouse, self).__init__()
		self.x = 256 + 48
		self.y = 95.5	#95.5
		self.layer = gcommon.C_LAYER_GRD | gcommon.C_LAYER_SKY
		self.left = -36
		self.top = -44
		self.right = 64
		self.bottom = 44
		self.hp = boss.BOSS_WAREHOUSE_HP
		self.score = 15000
		self.subState = 0
		self.subCnt = 0
		self.hitcolor1 = 12
		self.hitcolor2 = 6
		self.ground = True
		self.shotHitCheck = True	# 自機弾との当たり判定
		self.hitCheck = True	# 自機と敵との当たり判定
		self.enemyShotCollision = False	# 敵弾との当たり判定を行う
		self.countMover = enemy.CountMover(self, __class__.moveTable, True)
		# self.polygonList = []
		# self.polygonList.append(gcommon.Polygon(bossWarehouse0, 7))
		# self.polygonList.append(gcommon.Polygon(bossWarehouse1, 6))
		# self.polygonList.append(gcommon.Polygon(bossWarehouse2, 5))
		# self.polygonList.append(gcommon.Polygon(bossWarehouse3, 12))
		# self.polygonList.append(gcommon.Polygon(bossWarehouse4, 5))
		# self.polygonList.append(gcommon.Polygon(bossWarehouse5, 6))
		# self.polygonList.append(gcommon.Polygon(bossWarehouseUpper, 12))
		# self.polygonList.append(gcommon.Polygon(bossWarehouseOutline, 1, fill=False))
		# self.polygonList.append(gcommon.Polygon(bossWarehouseGun0, 1))
		# self.polygonList.append(gcommon.Polygon(bossWarehouseGun1, 5))
		# self.polygonList.append(gcommon.Polygon(bossWarehouseGun2, 5))
		# self.polygonList.append(gcommon.Polygon(bossWarehouseGun3, 12))
		# self.polygonList.append(gcommon.Polygon(bossWarehouseGun4, 12))
		# self.polygonList.append(gcommon.Polygon(bossWarehouseGun5, 7, False))
		# self.polygonList.append(gcommon.Polygon(bossWarehouseGun6, 7, False))
		# self.polygonList.append(gcommon.Polygon(bossWarehouseGunUpper0, 6))
		# self.polygonList.append(gcommon.Polygon(bossWarehouseGunUpper1, 5))
		# self.polygonList.append(gcommon.Polygon(bossWarehouseGunUpper2, 1))

		# self.polygonList4shot = []
		# self.polygonList4shot.append(gcommon.Polygon(bossWarehouse4shot0, 1))
		# self.polygonList4shot.append(gcommon.Polygon(bossWarehouse4shot1, 5))
		# self.polygonList4shot.append(gcommon.Polygon(bossWarehouse4shot2, 6))
		# self.xpolygonsList = []
		# self.xpolygons4shotList = []
		self.gunRad = math.pi
		self.gun_cx = self.x + 20.0
		self.gun_cy = self.y
		self.wheelCnt = 0
		self.gunWidth = 56
		self.gunHeight = 56
		self.image = [None]* self.gunWidth
		self.work = [None]* self.gunHeight
		for y in range(self.gunWidth):
			self.image[y] = [0]*self.gunHeight
		img = pyxel.image(2)
		for y in range(self.gunWidth):
			for x in range(self.gunHeight):
				self.image[y][x] = img.get(x +176, y +104)

	def update(self):
		self.countMover.update()
		self.gun_cx = self.x + 20.0
		self.gun_cy = self.y
		self.subCnt += 1
		if abs(self.countMover.dx) > 0.025 or abs(self.countMover.dy) > 0.025:
			self.wheelCnt += 1
		if self.state == 0:
			if self.countMover.tableIndex in (2, 4, 6, 8, 10):
				self.gunRad = gcommon.getRadToShip(self.x, self.y, self.gunRad +math.pi, math.pi/60) - math.pi
			elif self.countMover.tableIndex in (1, 3, 5, 7, 9, 11):
				self.shotMainState()
			if self.countMover.tableIndex == 1:
				if self.countMover.cnt % 45 == 0:
					ObjMgr.addObj(enemyBattery.MovableBattery1p(self.x -16, self.y, 30, [[100*8, 0, -1.0, 0.0]]))
			elif self.countMover.tableIndex == 5:
				if self.countMover.cnt % 45 == 0:
					ObjMgr.addObj(enemyBattery.MovableBattery1p(self.x -16, self.y, 30, [[0, 5, 44, self.y, 1.0],[100*8, 0, 0.0, 1.0]]))
			elif self.countMover.tableIndex == 9:
				if self.countMover.cnt % 45 == 0:
					ObjMgr.addObj(enemyBattery.MovableBattery1p(self.x -16, self.y, 30, [[0, 5, 44, self.y, 1.0],[100*8, 0, 0.0, -1.0]]))
			if self.hp < boss.BOSS_WAREHOUSE_HP/3:
				self.state = 1
		elif self.state == 1:
			if self.gunRad < 0.75 * math.pi:
				self.gunRad += 0.025* math.pi
			else:
				self.nextState()
		elif self.state == 2:
			if self.cnt % 4 == 0:
				self.shotMain()
			self.gunRad -= 0.025* math.pi
			if self.gunRad < -0.75 * math.pi:
				self.nextState()
		elif self.state == 3:
			if self.cnt % 4 == 0:
				self.shotMain()
			self.gunRad += 0.025* math.pi
			if self.gunRad > 0.75 * math.pi:
				self.setState(1)
			#self.gunRad -= 0.025* math.pi
			#if self.gunRad < 1.5 * math.pi:

		# self.xpolygonsList = []
		# self.xpolygonsList.append(gcommon.getAnglePolygons([self.x + 20.0, self.y],
		# 	self.polygonList, [27.5, 19.5], self.gunRad))

		# self.xpolygons4shotList = []
		# self.xpolygons4shotList.append(gcommon.getAnglePolygons([self.x + 20.0, self.y],
		# 	self.polygonList4shot, [6, 18], self.gunRad))
		# self.xpolygons4shotList.append(gcommon.getAnglePolygons([self.x + 20.0, self.y],
		# 	self.polygonList4shot, [-6, 18], self.gunRad))

		#self.gunRad += math.pi/360
		#if self.cnt % 45 == 0:
		#	self.shot4directions()

	def draw(self):
		pass

	def drawLayer(self, layer):
		if (layer & gcommon.C_LAYER_GRD) != 0:
			# 車輪
			n = (self.wheelCnt>>1) & 3
			pyxel.blt(self.x -16 -16, gcommon.sint(self.y +36 -16), 2, 128 +n*32, 160, 32, 32, 0)
			pyxel.blt(self.x -16 -16, gcommon.sint(self.y -36 -16), 2, 128 +(3-n)*32, 160, 32, 32, 0)
			pyxel.blt(self.x +56 -16, gcommon.sint(self.y +36 -16), 2, 128 +n*32, 160, 32, 32, 0)
			pyxel.blt(self.x +56 -16, gcommon.sint(self.y -36 -16), 2, 128 +(3-n)*32, 160, 32, 32, 0)
			
			pyxel.blt(self.x -48, gcommon.sint(self.y -51.5), 2, 136, 0, 120, 104, 3)


		elif (layer & gcommon.C_LAYER_SKY) != 0:
			pyxel.blt(self.x -48 +24, gcommon.sint(self.y -51.5) +32, 2, 136, 104, 40, 40)

			drawing.Drawing.setRotateImage(200, 192, 2, self.work, self.image, -self.gunRad, 3)
			pyxel.blt(self.x + 20.0 -self.gunWidth/2, self.y -self.gunHeight/2, 2, 200, 192, self.gunWidth, self.gunHeight, 3)
			#for polygons in self.xpolygonsList:
			#	Drawing.drawPolygons(polygons)

			#for polygons in self.xpolygons4shotList:
			#	Drawing.drawPolygons(polygons)

			#pos = gcommon.getAngle(-12, -12, self.gunRad)
			#pyxel.blt(self.gun_cx -3.5 +pos[0], self.gun_cy -3.5 + pos[1], 2, 176, 104, 8, 8, 3)

			# for p in __class__.shot4poss:
			# 	pos = gcommon.getAngle(p[0], p[1], self.gunRad)
			# 	pyxel.blt(self.gun_cx + pos[0] -3.5,
			# 			self.gun_cy + pos[1] -3.5,
			# 			2, 176, 104, 8, 8, 3)


	def broken(self):
		self.remove()
		enemy.removeEnemyShot()
		ObjMgr.objs.append(boss.BossExplosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
		GameSession.addScore(self.score)
		BGM.sound(gcommon.SOUND_LARGE_EXP)
		enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
		ObjMgr.objs.append(enemy.Delay(enemy.StageClear, None, 240))

	def shotMainState(self):
		if self.countMover.cnt > 30 and self.countMover.cnt < 120 and self.countMover.cnt % 10 == 0:
			self.shotMain()
		if self.countMover.cnt >= 60 and self.countMover.cnt % 6 == 0:
			px = self.gun_cx - 8.0 * math.cos(self.gunRad)
			py = self.gun_cy - 8.0 * math.sin(self.gunRad)
			enemy.enemy_shot_rad(px, py, 3.5, 0, self.gunRad + math.pi  - ( 125 -self.countMover.cnt) * math.pi/180)
			enemy.enemy_shot_rad(px, py, 3.5, 0, self.gunRad + math.pi  + ( 125 -self.countMover.cnt) * math.pi/180)

	def shotMain(self):
		r = self.gunRad + math.pi
		px = self.gun_cx + math.cos(r + math.pi/20) * 30
		py = self.gun_cy + math.sin(r + math.pi/20) * 30
		enemy.enemy_shot_rad(px, py, 4.5, 1, r)
		px = self.gun_cx + math.cos(r - math.pi/20) * 30
		py = self.gun_cy + math.sin(r - math.pi/20) * 30
		enemy.enemy_shot_rad(px, py, 4.5, 1, r)


	def shot4directions(self):
		for r in __class__.pos4rads:
			enemy.enemy_shot_rad(self.gun_cx + math.cos(self.gunRad + r) * 16, self.gun_cy + math.sin(self.gunRad +r) * 16, 3, 0, self.gunRad + r)
