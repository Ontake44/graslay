import pyxel
import math
import random
import gcommon
import enemy
import boss
import enemyShot

bossWarehouseOutline = [
	#[18,-1],[41, -1], [52, 10], [52, 31], [41, 42], [18, 42], [7, 30], [7, 10]
	[18, 0],[41, 0], [51, 10], [51, 31], [41, 41], [18, 41], [8, 31], [8, 10]
]

# clr = 7 左上
bossWarehouse0 = [
	[18, 0], [18, 10], [8, 10]
]
# clr = 6
bossWarehouse1 = [
	[18, 0], [41, 0], [51, 10], [18, 10]
]
# clr = 5 右の部分
bossWarehouse2 = [
	[41, 10], [51, 10], [51, 31], [41, 41]
]
# clr = 12 左下
bossWarehouse3 = [
	[18, 31], [18, 41], [8, 31]
]
# clr = 5 下の部分
bossWarehouse4 = [
	[18, 31], [51, 31], [41, 41], [18, 41]
]
# clr = 6 左の部分
bossWarehouse5 = [
	[17, 31], [8, 31], [8, 10], [17, 10]
]
bossWarehouseUpper = [
	[18, 8], [41, 8], [43, 10], [43, 31], [41, 33], [18, 33], [16, 31], [16, 10]
]

# # clr = 0
# bossWarehouseGun0 = [
# 	[0, 15], [23, 15], [23, 26], [0, 26]
# ]
# # clr = 5
# bossWarehouseGun1 = [
# 	[1, 16], [22, 16], [22, 25], [1, 25]
# ]
# # clr = 12
# bossWarehouseGun2 = [
# 	[1, 18], [22, 18], [22, 23], [1, 23]
# ]
# bossWarehouseGun3 = [
# 	[1, 19], [22, 19], [22, 22], [1, 22]
# ]
# bossWarehouseGun4 = [
# 	[1, 20], [22, 20], [22, 21], [1, 21]
# ]
# clr = 1
bossWarehouseGun0 = [
	[4, 13], [14, 13], [14, 28], [4, 28]
]
# clr = 5
bossWarehouseGun1 = [
	[4, 14], [13, 14], [13, 19], [4, 19]
]
# clr = 5
bossWarehouseGun2 = [
	[4, 22], [13, 22], [13, 27], [4, 27]
]
# clr = 12
bossWarehouseGun3 = [
	[4, 15], [13, 15], [13, 18], [4, 18]
]
# clr = 12
bossWarehouseGun4 = [
	[4, 23], [13, 23], [13, 26], [4, 26]
]
# clr = 7
bossWarehouseGun5 = [
	[4, 16], [13, 16]
]
# clr = 7
bossWarehouseGun6 = [
	[4, 24], [13, 24]
]

class BossWarehouse(enemy.EnemyBase):
	moveTable = [
		[0, 5, 150, 95.5, 0.5], 	# 0 前進
		[30, -1],					# 1
		[0, 5, 200, 95.5, 0.5], 	# 2 後ろに下がる
		[120, -1],					# 3 射撃
		[0, 5, 150, 95.5 -64, 0.5],	# 4 前方上
		[120, -1],					# 5
		[0, 5, 200, 95.5 -64, 0.5],	# 6 後方上
		[120, -1],					# 7 射撃
		[0, 5, 150, 95.5+64, 0.5],	# 8 前方下
		[120, -1],					# 9
		[0, 5, 200, 95.5+64, 0.5],	# 10 後方下
		[120, -1],					# 11 射撃
	]
	def __init__(self, t):
		super(BossWarehouse, self).__init__()
		self.x = 256 + 48
		self.y = 95.5	#95.5
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
		self.ground = True
		self.shotHitCheck = True	# 自機弾との当たり判定
		self.hitCheck = True	# 自機と敵との当たり判定
		self.enemyShotCollision = False	# 敵弾との当たり判定を行う
		self.countMover = enemy.CountMover(self, __class__.moveTable, True)
		self.polygonList = []
		self.polygonList.append(gcommon.Polygon(bossWarehouse0, 7))
		self.polygonList.append(gcommon.Polygon(bossWarehouse1, 6))
		self.polygonList.append(gcommon.Polygon(bossWarehouse2, 5))
		self.polygonList.append(gcommon.Polygon(bossWarehouse3, 12))
		self.polygonList.append(gcommon.Polygon(bossWarehouse4, 5))
		self.polygonList.append(gcommon.Polygon(bossWarehouse5, 6))
		self.polygonList.append(gcommon.Polygon(bossWarehouseUpper, 12))
		self.polygonList.append(gcommon.Polygon(bossWarehouseOutline, 1, fill=False))
		self.polygonList.append(gcommon.Polygon(bossWarehouseGun0, 1))
		self.polygonList.append(gcommon.Polygon(bossWarehouseGun1, 5))
		self.polygonList.append(gcommon.Polygon(bossWarehouseGun2, 5))
		self.polygonList.append(gcommon.Polygon(bossWarehouseGun3, 12))
		self.polygonList.append(gcommon.Polygon(bossWarehouseGun4, 12))
		self.polygonList.append(gcommon.Polygon(bossWarehouseGun5, 7, False))
		self.polygonList.append(gcommon.Polygon(bossWarehouseGun6, 7, False))
		self.xpolygonsList = []
		self.gunRad = math.pi
		self.gun_cx = self.x + 20.0
		self.gun_cy = self.y

	def update(self):
		self.countMover.update()
		self.gun_cx = self.x + 20.0
		self.gun_cy = self.y
		self.subCnt += 1
		if self.countMover.tableIndex in (2, 6, 10):
			self.gunRad = gcommon.getRadToShip(self.x, self.y, self.gunRad +math.pi, math.pi/60) - math.pi
		if self.countMover.tableIndex in (3, 7, 11):
			self.shotMainState()
		self.xpolygonsList = []
		self.xpolygonsList.append(gcommon.getAnglePolygons([self.x + 20.0, self.y],
			self.polygonList, [27.5, 19.5], self.gunRad))
		#self.gunRad += math.pi/360
		if self.cnt % 45 == 0:
			self.shot4directions()

	def draw(self):
		pyxel.blt(self.x -48, self.y -51.5, 2, 136, 0, 120, 104, 3)
		for polygons in self.xpolygonsList:
			gcommon.drawPolygons(polygons)

	def shotMainState(self):
		if self.countMover.cnt > 30 and self.countMover.cnt < 120 and self.countMover.cnt % 10 == 0:
			self.shotMain()
		if self.countMover.cnt >= 60 and self.countMover.cnt % 8 == 0:
			enemy.enemy_shot_rad(self.gun_cx, self.gun_cy, 3.5, 0, self.gunRad + math.pi  - ( 125 -self.countMover.cnt) * math.pi/180)
			enemy.enemy_shot_rad(self.gun_cx, self.gun_cy, 3.5, 0, self.gunRad + math.pi  + ( 125 -self.countMover.cnt) * math.pi/180)

	def shotMain(self):
		r = self.gunRad + math.pi
		px = self.gun_cx + math.cos(r + math.pi/20) * 30
		py = self.gun_cy + math.sin(r + math.pi/20) * 30
		enemy.enemy_shot_rad(px, py, 5, 1, r)
		px = self.gun_cx + math.cos(r - math.pi/20) * 30
		py = self.gun_cy + math.sin(r - math.pi/20) * 30
		enemy.enemy_shot_rad(px, py, 5, 1, r)


	def shot4directions(self):
		r = math.pi/4.0
		for i in range(4):
			enemy.enemy_shot_rad(self.gun_cx + math.cos(self.gunRad + r) * 16, self.gun_cy + math.sin(self.gunRad +r) * 16, 3, 0, self.gunRad + r)
			r += math.pi/2
