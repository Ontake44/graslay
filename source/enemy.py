
import pyxel
import math
import random
import gcommon



enemy1_spmap=[	\
[160,1,1],	\
[144,-1,1],	\
[128,1,1],		\
[144,1,1],		\
[160,-1,1],		\
[144,1,-1],		\
[128,1,-1],		\
[144,-1,-1]		\
]

#tank1_spmap=[208,0,144,0,176,0,144,0]
tank1_spmap=[64,0,0,0,32,0,0,0]


def enemy_shot(x, y, speed, shotType):
	gcommon.ObjMgr.objs.append(EnemyShot.createToMyShip(x, y, speed, shotType, 0))
	#gcommon.ObjMgr.objs.append(EnemyShot(x, y, speed, shotType, -1, 0))

def enemy_shot_offset(x, y, speed, shotType, offsetDr):
	gcommon.ObjMgr.objs.append(EnemyShot.createToMyShip(x, y, speed, shotType, offsetDr))

def enemy_shot_multi(x, y, speed, shotType, count, angleDr):
	for i in range(count):
		gcommon.ObjMgr.objs.append(EnemyShot.createToMyShip(x, y, speed, shotType, int(angleDr * (count/2 -i))))

def enemy_shot_dr(x, y, speed, shotType, dr):
	gcommon.ObjMgr.objs.append(EnemyShot.createSpecifiedDirection(x, y, speed, shotType, dr))

def enemy_shot_dr_multi(x, y, speed, shotType, dr, count, angleDr):
	if count & 1 == 1:
		gcommon.ObjMgr.objs.append(EnemyShot.createSpecifiedDirection(x, y, speed, shotType, dr))
		for i in range(count>>1):
			gcommon.ObjMgr.objs.append(EnemyShot.createSpecifiedDirection(x, y, speed, shotType, dr + angleDr * i))
			gcommon.ObjMgr.objs.append(EnemyShot.createSpecifiedDirection(x, y, speed, shotType, dr - angleDr * i))
	else:
		for i in range(count>>1):
			gcommon.ObjMgr.objs.append(EnemyShot.createSpecifiedDirection(x, y, speed, shotType, dr + int(angleDr/2 + angleDr * i)))
			gcommon.ObjMgr.objs.append(EnemyShot.createSpecifiedDirection(x, y, speed, shotType, dr - int(angleDr/2 + angleDr * i)))


def remove_all_battery():
	for obj in gcommon.ObjMgr.objs:
		if obj.t==gcommon.T_BATTERY1:
			obj.removeFlag = True

# 敵
class EnemyBase:
	def __init__(self):
		self.t = 0
		self.x = 0
		self.y = 0
		self.left = 0
		self.top = 0
		self.right = 0
		self.bottom = 0
		self.collisionRects = None		# List of Rect
		self.hp = 0
		self.state = 0
		self.cnt = 0
		self.frameCount = 0
		self.hit = False
		self.layer = 0
		self.score = 0
		self.hitcolor1 = 0
		self.hitcolor2 = 0
		self.exptype = gcommon.C_EXPTYPE_SKY_S
		self.expsound = -1
		self.score = 0
		self.ground = False			# スクロール同期
		self.shotHitCheck = True	# 自機弾との当たり判定
		self.hitCheck = True	# 自機と敵との当たり判定
		self.enemyShotCollision = False	# 敵弾との当たり判定を行う
		self.shotEffect = True		# 自機弾が当たった時のエフェクト
		self.removeFlag = False
		self.nextStateNo = -1

	def nextState(self):
		self.nextStateNo = self.state + 1
		self.cnt = 0

	def setState(self, state):
		self.nextStateNo = state
		self.cnt = 0

	# 自機弾と敵との当たり判定と破壊処理
	def checkShotCollision(self, shot):
		if shot.removeFlag == False and	\
			((self.collisionRects != None and gcommon.check_collision_list(self.x, self.y, self.collisionRects, shot))	\
			or	\
			(self.collisionRects == None and gcommon.check_collision(self, shot))):
			self.hp -= shot.shotPower
			if self.hp <= 0:
				self.broken()
			else:
				if shot.effect and self.shotEffect:
					# 跳弾表示
					Particle1.appendShotCenter(shot)
					gcommon.sound(gcommon.SOUND_HIT, gcommon.SOUND_CH2)
				self.hit = True
			return True
		else:
			return False

	# 自機と敵との当たり判定
	def checkMyShipCollision(self):
		if self.collisionRects != None:
			return gcommon.check_collision_list(self.x, self.y, self.collisionRects, gcommon.ObjMgr.myShip)
		else:
			return gcommon.check_collision(self, gcommon.ObjMgr.myShip)

	def drawLayer(self, layer):
		self.draw()

	def draw(self):
		pass

	def remove(self):
		self.removeFlag = True

	# 追加されたとき
	def appended(self):
		pass
	
	# 破壊されたとき
	def broken(self):
		layer = gcommon.C_LAYER_EXP_SKY
		if self.layer in (gcommon.C_LAYER_GRD, gcommon.C_LAYER_UNDER_GRD):
			layer = gcommon.C_LAYER_GRD
		
		gcommon.GameSession.addScore(self.score)
		
		create_explosion2(self.x+(self.right+self.left+1)/2, self.y+(self.bottom+self.top+1)/2, layer, self.exptype, self.expsound)
		self.remove()

# [0] to cnt
# [1] mode
#  mode = 0
#    [2] dx
#    [3] dy
#  mode = 1
#    [2] Layer
class CountMover:
	def __init__(self, obj, table, loopFlag):
		self.obj = obj
		self.table = table
		self.tableIndex = 0
		self.loopFlag = loopFlag
		self.isEnd = False
		self.cycleCount = 0
		self.cnt = 0

	def update(self):
		if self.isEnd:
			return
		item = self.table[self.tableIndex]
		if self.cnt < item[0]:
			if item[1] == 0:
				self.obj.x += item[2]
				self.obj.y += item[3]
				self.cnt += 1
			elif item[1] == 1:
				self.obj.layer = item[2]
				self.cnt += 1
				#print("set layer :" + str(self.obj.layer))
			else:
				print("CountMover mode is invalid :" +str(item[1]))
		else:
			self.tableIndex += 1
			self.cnt = 0
			if self.tableIndex == len(self.table):
				if self.loopFlag:
					self.cycleCount += 1
					self.tableIndex = 0
				else:
					self.isEnd = True

# 爆発生成
# cx,cy center
# exlayer explosion layer
def create_explosion(cx, cy, exlayer, exptype):
	if exptype==gcommon.C_EXPTYPE_SKY_S or exptype==gcommon.C_EXPTYPE_GRD_S:
		gcommon.sound(gcommon.SOUND_SMALL_EXP)
	else:
		gcommon.sound(gcommon.SOUND_MID_EXP)
	gcommon.ObjMgr.objs.append(Explosion(cx,cy,exlayer,exptype))

def create_explosion2(cx, cy, exlayer, exptype, expsound):
	if expsound != -1:
		gcommon.sound(expsound)
	else:
		if exptype==gcommon.C_EXPTYPE_SKY_S or exptype==gcommon.C_EXPTYPE_GRD_S:
			gcommon.sound(gcommon.SOUND_SMALL_EXP)
		else:
			gcommon.sound(gcommon.SOUND_MID_EXP)
	gcommon.ObjMgr.objs.append(Explosion(cx,cy,exlayer,exptype))

#
# アイテム生成
def create_item(cx, cy, itype):
	if itype == gcommon.C_ITEM_PWUP:
		gcommon.ObjMgr.objs.append(PowerUp(cx,cy))



class EnemyShot(EnemyBase):
	# x,y 弾の中心を指定
	# dr  0 -63
	def __init__(self, x, y, speed, shotType):
		super(EnemyShot, self).__init__()
		self.shotType = shotType
		self.shotHitCheck = False
		if self.shotType==0:
			self.x = x -4
			self.y = y -4
			self.left = 2
			self.top = 2
			self.right = 5
			self.bottom = 5
		elif self.shotType == 1:
			self.x = x -6
			self.y = y -6
			self.left = 2
			self.top = 2
			self.right = 9
			self.bottom = 9
		elif self.shotType == 2:
			self.x = x -8
			self.y = y -8
			self.left = 2
			self.top = 2
			self.right = 13
			self.bottom = 13
		else:
			self.shotHitCheck = True
			self.x = x -8
			self.y = y -8
			self.left = 2
			self.top = 2
			self.right = 13
			self.bottom = 13
		self.speed = speed
		self.type = gcommon.T_E_SHOT1
		self.layer = gcommon.C_LAYER_E_SHOT

	@classmethod
	def createToMyShip(cls, x, y, speed, shotType, offsetDr):
		shot = EnemyShot(x, y, speed, shotType)
		r = gcommon.get_atan_to_ship2(x,y,offsetDr)
		shot.dx = math.cos(r) * speed * gcommon.enemy_shot_rate
		shot.dy = math.sin(r) * speed * gcommon.enemy_shot_rate
		return shot
	
	@classmethod
	def createSpecifiedDirection(cls, x, y, speed, shotType, dr):
		shot = EnemyShot(x, y, speed, shotType)
		r = dr & 63
		shot.dx = math.cos(gcommon.atan_table[r]) * speed * gcommon.enemy_shot_rate
		shot.dy = math.sin(gcommon.atan_table[r]) * speed * gcommon.enemy_shot_rate
		return shot

	def update(self):
		self.x += self.dx
		self.y += self.dy
		if self.x <-16 or self.x >= gcommon.SCREEN_MAX_X or self.y<-16 or self.y >=gcommon.SCREEN_MAX_Y:
			self.removeFlag = True

		if gcommon.isMapFreePos(gcommon.getCenterX(self), gcommon.getCenterY(self)) == False:
			self.removeFlag = True

	def draw(self):
		# pyxel.rect(self.x+ self.left, self.y+self.top, self.right-self.left+1, self.bottom-self.top+1, 8)
		if self.shotType==0:
			pyxel.blt(self.x, self.y, 0, 4, 20, 8, 8, gcommon.TP_COLOR)
		elif self.shotType == 1:
			pyxel.blt(self.x, self.y, 0, 18, 18, 12, 12, gcommon.TP_COLOR)
		elif self.shotType == 2:
			pyxel.blt(self.x, self.y, 0, 32, 16, 16, 16, gcommon.TP_COLOR)
		else:
			pyxel.blt(self.x, self.y, 0, 48, 16, 16, 16, gcommon.TP_COLOR)




#
# 爆発
# 
class Explosion(EnemyBase):
	# sx, sy, width, height
	patternTable = [
		[0, 144, 16,16],		# 0
		[16, 144, 16,16],		# 1
		[32, 144, 16,16],		# 2
		[48, 144, 16,16],		# 3
		[64, 144, 16,16],		# 4 : 爆発終了パターン
		[136, 64, 32, 32],		# 5
		[0, 64, 48, 48],		# 6
		[48 ,64, 48, 48],		# 7 : 爆発終了パターン１
		[96, 64, 40, 40],		# 8 : 爆発終了パターン２
		[96, 144, 40, 40]
	]
	def __init__(self, cx,cy,exlayer,exptype):
		super(Explosion, self).__init__()
		self.t = gcommon.T_SKY_EXP
		self.x = cx
		self.y = cy
		self.particle = True
		self.particleCount = 8
		self.layer = exlayer
		self.exptype = exptype
		self.size = 0
		self.hitCheck = False
		self.shotHitCheck = False
		if exlayer in (gcommon.C_LAYER_GRD, gcommon.C_LAYER_UNDER_GRD):
			self.ground = True
		if exptype == gcommon.C_EXPTYPE_SKY_S or exptype==gcommon.C_EXPTYPE_GRD_S:
			self.size = 1
		elif exptype == gcommon.C_EXPTYPE_SKY_M or exptype==gcommon.C_EXPTYPE_GRD_M:
			self.size = 2
			self.particleCount = 100
		else:
			self.size = 3
			self.particleCount = 16

	def update(self):
		if self.cnt == 0 and self.particle:
			Particle2.append(self.x, self.y, self.particleCount)
		if self.size==1:
			if self.cnt >= 25:
				self.removeFlag = True
		elif self.size == 2:
			if self.cnt>40:
				self.remove()
		else:
			if self.cnt>40:
				self.remove()

	def drawPattern(self, no):
		ptn = Explosion.patternTable[no]
		pyxel.blt( self.x-ptn[2]/2, self.y-ptn[3]/2, 0, ptn[0], ptn[1],
			ptn[2] -(self.cnt &2) * ptn[2],
			ptn[3] -(self.cnt &4) * ptn[3]/2,
		0)

	def draw(self):
		if self.size==1:
			#pyxel.circb(self.x, self.y, self.cnt*2+1, 10)
			n = self.cnt>>2
			if n <= 5:
				pyxel.blt( self.x-8, self.y-8, 0, 0 + n*16, 144,
					16, 16,
					0)
		elif self.size==2:
			if self.cnt%2 ==0:
				if self.cnt<6:
					pyxel.circ(self.x, self.y, self.cnt*2+1, 10)
				elif self.cnt < 12:
					self.drawPattern(5)
				elif self.cnt < 18:
					self.drawPattern(6)
				elif self.cnt < 24:
					self.drawPattern(7)
				elif self.cnt < 32:
					self.drawPattern(8)
				elif self.cnt < 40:
					self.drawPattern(9)

			# elif self.cnt < 25:
			# 	if self.cnt%2 ==0:
			# 		pyxel.blt( self.x-24, self.y-24, 0, 0, 64,
			# 			24*2 -(self.cnt &2) * 48,
			# 			24*2 -(self.cnt &4) * 24,
			# 			0)
			# else:
			# 	if self.cnt%2 ==0:
			# 		pyxel.blt( self.x-24, self.y-24, 0, 0, 64,
			# 			24*2 -(self.cnt &2) * 48,
			# 			24*2 -(self.cnt &4) * 24,
			# 			0)
		else:
			if self.cnt<8:
				pyxel.circ(self.x, self.y, self.cnt*2+1, 10)
			elif self.cnt < 25:
				if self.cnt%2 ==0:
					pyxel.blt( self.x-36, self.y-36, 0, 184, 88,
						72 -(self.cnt &2) * 72,
						72 -(self.cnt &4) * 36,
						gcommon.TP_COLOR)
			else:
				if self.cnt%2 ==0:
					pyxel.pal(7, gcommon.TP_COLOR)
					pyxel.blt( self.x-36, self.y-36, 0, 184, 88,
						72 -(self.cnt &2) * 72,
						72 -(self.cnt &4) * 36,
						gcommon.TP_COLOR)
					pyxel.pal()

#
# アイテム
#
class PowerUp(EnemyBase):
	def __init__(self, cx, cy):
		super(PowerUp, self).__init__()
		d = random.randrange(1,8,2)		# 1,3,5,7
		self.x = cx
		self.y = cy
		self.left = 0
		self.top = 0
		self.right = 15
		self.bottom = 15
		self.dx = gcommon.direction_map[d][0] * 2
		self.dy = gcommon.direction_map[d][1] * 2
		self.itype = gcommon.C_ITEM_PWUP
		self.layer = gcommon.C_LAYER_ITEM

	def update(self):
		self.x += self.dx
		self.y += self.dy
		if gcommon.is_outof_bound(self):
			self.removeFlag = True
		elif self.cnt < 20 * 60:
			if self.x<0:
				self.x = 0
				self.dx = -self.dx
			elif self.x>240:
				self.x = 240
				self.dx = -self.dx
			
			if self.y<0:
				self.y = 0
				self.dy = -self.dy
			elif self.y>240:
				self.y = 240
				self.dy = -self.dy

	def draw(self):
		pyxel.blt(self.x, self.y, 0, 64, 16, 16, 16, gcommon.TP_COLOR)
		

class Jumper1(EnemyBase):
	def __init__(self, t):
		super(Jumper1, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.ay = t[4]
		self.left = 2
		self.top = 2
		self.right = 13
		self.bottom = 13
		self.hp = 20
		self.layer = gcommon.C_LAYER_SKY
		self.score = 50
		self.hitcolor1 = 5
		self.hitcolor2 = 6
		self.exptype = gcommon.C_EXPTYPE_SKY_S
		self.dx = -1
		if self.x == -16:
			self.dx = 1
		self.dy = 0.0

	def update(self):
		self.x = self.x + self.dx
		if self.x < -16 or self.x > 256:
			self.remove()
			return
		self.y = self.y + self.dy
		self.dy = self.dy + self.ay
		if self.dy > 0:
			if gcommon.isMapFreePos(self.x + 8, self.y + 16 + self.dy) == False:
				self.dy = -self.dy
		else:
			if gcommon.isMapFreePos(self.x + 8, self.y + self.dy) == False:
				self.dy = -self.dy
		#elif gcommon.isMapFreePos(self.x + 8, self.y -4) == False:
		#	self.dy = -self.dy
		if self.cnt == 30 and gcommon.GameSession.isNormalOrMore():
			enemy_shot(self.x +8, self.y +8, 2, 0)

	def draw(self):
		pyxel.blt(self.x, self.y, 1, 80, 64, 16, 16, gcommon.TP_COLOR)



class RollingFighter1(EnemyBase):
	def __init__(self, t):
		super(RollingFighter1, self).__init__()
		self.x = 256
		self.y = t[2]
		self.left = 2
		self.top = 2
		self.right = 15
		self.bottom = 13
		self.hp = 1
		self.layer = gcommon.C_LAYER_SKY
		self.score = 50
		self.hitcolor1 = 5
		self.hitcolor2 = 6
		self.exptype = gcommon.C_EXPTYPE_SKY_S
		self.dy = 0.0
		self.dr = 0		# 0 to 63

	def update(self):
		self.x = self.x -1.5
		self.y = self.y + self.dy
		self.dy = gcommon.sin_table[self.dr] * 2.0
		self.dr = (self.dr + 1) & 63
		if self.cnt == 30 and gcommon.GameSession.isNormalOrMore():
			enemy_shot(self.x +8, self.y +8, 2, 0)

	def draw(self):
		pyxel.blt(self.x, self.y, 1, ((self.cnt>>1) &7) * 16, 80, 16, 16, gcommon.TP_COLOR)

class RollingFighter1Group(EnemyBase):
	def __init__(self, t):
		super(RollingFighter1Group, self).__init__()
		self.y = t[2]
		self.interval = t[3]
		self.max = t[4]
		self.cnt2 = 0
		self.hitCheck = False
		self.shotHitCheck = False

	def update(self):
		if self.cnt % self.interval == 0:
			gcommon.ObjMgr.addObj(RollingFighter1([0, 0, self.y]))
			self.cnt2 += 1
			if self.cnt2 >= self.max:
				self.remove()

	def draw(self):
		pass



#
# 砲台
class Battery1(EnemyBase):
	def __init__(self, t):
		super(Battery1, self).__init__()
		pos = gcommon.mapPosToScreenPos(t[2], t[3])
		self.x = pos[0]		# map x
		self.y = pos[1]		# map y
		self.mirror = t[4]	# 0: normal 1:上下逆
		self.left = 2
		self.right = 13
		if self.mirror == 0:
			self.top = 5
			self.bottom = 15
		else:
			self.top = 0
			self.bottom = 10
		self.hp = 10
		self.layer = gcommon.C_LAYER_GRD
		self.ground = True
		self.score = 300
		self.hitcolor1 = 8
		self.hitcolor2 = 14
		self.exptype = gcommon.C_EXPTYPE_GRD_S
		self.interval = int(120 / gcommon.enemy_shot_rate)
		self.first = int(120 / gcommon.enemy_shot_rate)
		self.shot_speed = 2
		self.remove_min_x = -16

	def update(self):
		if self.x < self.remove_min_x:
			self.remove()
			return
		if self.first == self.cnt or self.cnt % self.interval ==0:
			enemy_shot(self.x+8,self.y+6, self.shot_speed, 0)

	def draw(self):
		drawBattery1(self.x, self.y, self.mirror)

def drawBattery1(x, y, mirror):
	dr8 = 0
	dr8 = gcommon.get_direction_my(x+8, y +8)
	y = int(y)
	if mirror == 0:
		if dr8  in (0, 1):
			pyxel.blt(x, y, 1, 0, 96, -16, 16, gcommon.TP_COLOR)
		elif dr8 == 2:
			pyxel.blt(x, y, 1, 32, 96, 16, 16, gcommon.TP_COLOR)
		elif dr8 in (3, 4):
			pyxel.blt(x, y, 1, 0, 96, 16, 16, gcommon.TP_COLOR)
		elif dr8 in (5, 6):
			pyxel.blt(x, y, 1, 16, 96, 16, 16, gcommon.TP_COLOR)
		elif dr8 == 7:
			pyxel.blt(x, y, 1, 16, 96, -16, 16, gcommon.TP_COLOR)
	else:
		if dr8 == 0:
			pyxel.blt(x, y, 1, 0, 96, -16, -16, gcommon.TP_COLOR)
		elif dr8 == 1:
			pyxel.blt(x, y, 1, 16, 96, -16, -16, gcommon.TP_COLOR)
		elif dr8 == 2:
			pyxel.blt(x, y, 1, 32, 96, 16, -16, gcommon.TP_COLOR)
		elif dr8 == 3:
			pyxel.blt(x, y, 1, 16, 96, 16, -16, gcommon.TP_COLOR)
		elif dr8 == 4:
			pyxel.blt(x, y, 1, 0, 96, 16, -16, gcommon.TP_COLOR)
		elif dr8 == 5:
			pyxel.blt(x, y, 1, 0, 96, 16, -16, gcommon.TP_COLOR)
		elif dr8 == 6:
			pyxel.blt(x, y, 1, 32, 96, 16, -16, gcommon.TP_COLOR)
		elif dr8 == 7:
			pyxel.blt(x, y, 1, 16, 96, -16, -16, gcommon.TP_COLOR)

class StageClearText(EnemyBase):
	def __init__(self, stage):
		super(StageClearText, self).__init__()
		self.x = 0
		self.y = 0
		self.stage = stage
		self.left = 0
		self.top = 0
		self.right = 0
		self.bottom = 0
		self.layer = gcommon.C_LAYER_TEXT

	def update(self):
		pass

	def draw(self):
		pyxel.blt(127-16*5/2, 90, 0, 0, 240, 80, 16, gcommon.TP_COLOR)
		pyxel.blt(127-16/2, 114, 0, 146+ (self.stage -1)*16, 176, 16, 16, gcommon.TP_COLOR)
		pyxel.blt(127-16*5/2, 138, 0, 80, 240, 80, 16, gcommon.TP_COLOR)


# class Splash(EnemyBase):
# 	def __init__(self, x, y, layer):
# 		super(Splash, self).__init__()
# 		self.t = gcommon.T_SKY_EXP
# 		self.x = x
# 		self.y = y
# 		self.layer = layer
# 		self.offset = random.random()

# 	def update(self):
# 		self.cnt += 1
# 		if self.cnt > 100:
# 			self.removeFlag = True

# 	def draw(self):
# 		gcommon.draw_splash2(self, self.offset)


# 	def draw(self):
# 		d = ((self.dr + 2) & 63)>>2
# 		if d >= 8:
# 			pyxel.blt(self.x, self.y, 2, (d -8) * 24, 16+24, 24, 24, gcommon.TP_COLOR)
# 		else:
# 			pyxel.blt(self.x, self.y, 2, d * 24, 16, 24, 24, gcommon.TP_COLOR)


class SplashItem:
	def __init__(self, x, y, dx, dy, cnt):
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy
		self.cnt = cnt
		self.life = cnt
		self.removeFlag = False


class Splash(EnemyBase):
	def __init__(self, cx, cy, layer):
		super(Splash, self).__init__()
		self.x = cx
		self.y = cy
		self.layer = layer
		self.tbl = []
		self.count = 200
		self.direction = 0		# ラジアン
		self.angle = 2 * math.pi
		self.hitCheck = False
		self.shotHitCheck = False

	@classmethod
	def append(cls, x, y, layer):
		gcommon.ObjMgr.addObj(Splash(x, y, layer))

	@classmethod
	def append2(cls, x, y, layer, count):
		obj = Splash(x, y, layer)
		obj.count = count
		gcommon.ObjMgr.addObj(obj)

	@classmethod
	def appendDr(cls, x, y, layer, dr, angle, count):
		obj = Splash(x, y, layer)
		obj.direction = dr
		obj.angle = angle
		obj.count = count
		gcommon.ObjMgr.addObj(obj)

	def update(self):
		if self.cnt == 0:
			for i in range(0,self.count):
				r = self.direction + random.random() * self.angle - self.angle/2
				speed = random.random() * 6
				s = SplashItem(self.x, self.y, speed * math.cos(r), speed * math.sin(r), random.randrange(100, 240))
				self.tbl.append(s)

		newTbl = []
		for s in self.tbl:
			s.cnt -= 1
			if s.cnt > 0:
				newTbl.append(s)
				s.x += s.dx
				s.y += s.dy
				s.dx *= 0.97
				s.dy *= 0.97
		self.tbl = newTbl
		if len(self.tbl) == 0:
			self.remove()

	def draw(self):
		for s in self.tbl:
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



class EnemyGroup(EnemyBase):
	def __init__(self, t):
		super(EnemyGroup, self).__init__()
		self.cls = t[2]
		self.params = t[3]
		self.interval = t[4]
		self.max = t[5]
		self.cnt2 = 0
		self.hitCheck = False
		self.shotHitCheck = False

	def update(self):
		if self.cnt % self.interval == 0:
			gcommon.ObjMgr.addObj(self.cls(self.params))
			self.cnt2 += 1
			if self.cnt2 >= self.max:
				self.remove()

	def draw(self):
		pass

# x,y座標はキャラクタ中心
class Fan1a(EnemyBase):
	def __init__(self, t):
		super(Fan1a, self).__init__()
		self.dr = t[2]		# rad
		self.left = -8
		self.top = -8
		self.right = 8
		self.bottom = 8
		self.collisionRects = gcommon.Rect.createSingleList(-5.5, -5.5, 5.5, 5.5)
		self.hp = 1
		self.dx = 0
		self.dy = 0
		self.time1 = 30
		self.layer = gcommon.C_LAYER_SKY
		self.score = 10
		self.targetX = (gcommon.SCREEN_MAX_X - gcommon.SCREEN_MIN_X)/2.0
		self.targetY = (gcommon.SCREEN_MAX_Y - gcommon.SCREEN_MIN_Y)/2.0
		self.x = self.targetX + math.cos(self.dr) * 180
		self.y = self.targetY + math.sin(self.dr) * 150
		self.dr += math.pi 	#+ math.pi/8
		self.inFlag = False

	def update(self):
		if self.state == 0:
			self.x += 1.5 * math.cos(self.dr)
			self.y += 1.5 * math.sin(self.dr)
			if self.cnt == 40:
				self.nextState()
		elif self.state == 1:
			if self.cnt == 30:
				self.nextState()
		else:
			self.x += 2.0 * math.cos(self.dr)
			self.y += 2.0 * math.sin(self.dr)
			#self.dr -= math.pi/180

		if self.inFlag:
			if gcommon.outScreenRect(self):
				#print("Fan1a remove")
				self.remove()
				return
		else:
			if gcommon.inScreen(self.x, self.y):
				self.inFlag = True
			


	def draw(self):
		pyxel.blt(self.x -7.5, self.y -7.5, 1, 0 + (self.cnt & 4) * 4, 64, 16, 16, gcommon.TP_COLOR)

class Fan1aGroup(EnemyBase):
	def __init__(self, t):
		super(Fan1aGroup, self).__init__()
		self.max = t[2]
		self.hitCheck = False
		self.shotHitCheck = False
		r = 0.0
		for i in range(self.max):
			if r != 0.0 or gcommon.GameSession.isNormalOrMore():
				gcommon.ObjMgr.addObj(Fan1a([0, 0, r +math.pi]))
			r += math.pi * 2.0 /self.max
		self.remove()

	def update(self):
		pass

	def draw(self):
		pass

class Fan1Group(EnemyBase):
	def __init__(self, t):
		super(Fan1Group, self).__init__()
		self.y = t[2]
		self.interval = t[3]
		self.max = t[4]
		self.shotFlag = t[5] if len(t) > 5 else False
		self.cnt2 = 0
		self.hitCheck = False
		self.shotHitCheck = False

	def update(self):
		if self.cnt % self.interval == 0:
			gcommon.ObjMgr.addObj(Fan1([0, 0, 256, self.y, self.shotFlag]))
			self.cnt2 += 1
			if self.cnt2 >= self.max:
				self.remove()

	def draw(self):
		pass

class Fan1(EnemyBase):
	def __init__(self, t):
		super(Fan1, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.shotFlag = t[4] if len(t) > 4 else False
		self.left = 2
		self.top = 2
		self.right = 14
		self.bottom = 14
		self.hp = 1
		self.dx = 0
		self.dy = 0
		#self.time1 = 60
		#self.time2 = 90
		self.layer = gcommon.C_LAYER_SKY
		self.score = 10
	
	def update(self):
		if self.state == 0:
			self.x -= 3
			if self.x < 100:
				self.nextState()
		elif self.state == 1:
			self.x += 2
			if self.x > 170:
				self.nextState()
		else:
			self.x -= 3

		if self.state in (1, 2):
			if gcommon.ObjMgr.myShip.y < self.y +2:
				self.y -= 1.5
			elif gcommon.ObjMgr.myShip.y > self.y -2:
				self.y += 1.5
		if self.x <= -16:
			self.remove()
			return
		if self.shotFlag and self.frameCount == 60 and gcommon.GameSession.isNormalOrMore():
			enemy_shot(self.x +8, self.y +8, 2, 0)

	def draw(self):
		pyxel.blt(self.x, self.y, 1, 0 + (self.cnt & 4) * 4, 64, 16, 16, gcommon.TP_COLOR)

class MissileShip(EnemyBase):
	def __init__(self, t):
		super(MissileShip, self).__init__()
		self.x = 256+8
		self.y = t[2]
		self.stop_x = t[3]
		self.left = 2
		self.top = 2
		self.right = 14
		self.bottom = 14
		self.hp = 30
		self.hitcolor1 = 12
		self.hitcolor2 = 7
		self.dx = -2
		self.dy = 0
		self.layer = gcommon.C_LAYER_SKY
		self.score = 100

	def update(self):
		if self.state == 0:
			self.x += self.dx
			if self.x < self.stop_x:
				self.dx += 0.2
				if self.dx > -0.1:
					self.dx = 0
					self.nextState()
		elif self.state == 1:
			if self.cnt > 30:
				# ミサイル発射
				self.dx = 0.1
				self.nextState()
				gcommon.ObjMgr.addObj(Missile1(self.x -8, self.y -5, -1))
				gcommon.ObjMgr.addObj(Missile1(self.x -8, self.y +14, 1))
		elif self.state == 2:
			self.x += self.dx
			self.dx += 0.1
			if self.dx >= 2:
				self.dx = 2
			if self.x >= 256:
				self.remove()
		else:
			self.x += self.dx
		
	def draw(self):
		if self.state in (0,1):
			pyxel.blt(self.x -10, self.y -5, 1, 48, 64, 32, 8, gcommon.TP_COLOR)
			pyxel.blt(self.x -10, self.y +14, 1, 48, 64, 32, 8, gcommon.TP_COLOR)
		pyxel.blt(self.x, self.y, 1, 32, 64, 16, 16, gcommon.TP_COLOR)


class Missile1(EnemyBase):
	def __init__(self, x, y, dy):
		super(Missile1, self).__init__()
		self.x = x
		self.y = y
		self.left = 2
		self.top = 0
		self.right = 31
		self.bottom = 6
		self.hp = 15
		self.dx = dy
		self.dy = 0
		self.layer = gcommon.C_LAYER_SKY
		self.score = 100
	def update(self):
		if self.state == 0:
			self.y += self.dy
			self.dy *= 0.95
			if abs(self.dy) < 0.1:
				self.dx = 0
				self.nextState()
		elif self.state == 1:
			self.x += self.dx
			self.dx -= 0.2
			if self.dx > 3:
				self.dx = 3
		
	def drawMissile(self):
		pyxel.blt(self.x, self.y, 1, 48, 64, 32, 7, gcommon.TP_COLOR)
				
	def draw(self):
		self.drawMissile()
		if self.cnt & 2 == 0:
			if self.cnt & 4 == 0:
				pyxel.blt(self.x + 32, self.y, 1, 48, 72, 32, 7, gcommon.TP_COLOR)
			else:
				pyxel.blt(self.x + 32, self.y-1, 1, 48, 72, 32, -7, gcommon.TP_COLOR)

class Missile2(EnemyBase):
	def __init__(self, x, y, dy):
		super(Missile2, self).__init__()
		self.x = x
		self.y = y
		self.left = 2
		self.top = 0
		self.right = 31
		self.bottom = 6
		self.hp = 30
		self.dx = dy
		self.dy = 0
		self.layer = gcommon.C_LAYER_SKY
		self.score = 100
	def update(self):
		if self.state == 0:
			self.y += self.dy
			self.dy *= 0.95
			if abs(self.dy) < 0.1:
				self.dx = 0
				self.nextState()
		elif self.state == 1:
			self.x += self.dx
			self.dx -= 0.2
			if self.dx > 3:
				self.dx = 3
		if self.x < 120:
			enemy_shot_dr(self.x + 8, self.y + 3, 3, 0, 31)
			enemy_shot_dr(self.x + 8, self.y + 3, 3, 0, 33)
			self.remove()
		
	def drawMissile(self):
		pyxel.blt(self.x, self.y, 1, 80, 64, 32, 7, gcommon.TP_COLOR)
		
	def draw(self):
		self.drawMissile()
		if self.cnt & 2 == 0:
			if self.cnt & 4 == 0:
				pyxel.blt(self.x + 32, self.y, 1, 48, 72, 32, 7, gcommon.TP_COLOR)
			else:
				pyxel.blt(self.x + 32, self.y-1, 1, 48, 72, 32, -7, gcommon.TP_COLOR)

class Missile3(EnemyBase):
	def __init__(self, x, y, dy):
		super(Missile3, self).__init__()
		self.x = x
		self.y = y
		self.left = 2
		self.top = 0
		self.right = 31
		self.bottom = 6
		self.hp = 30
		self.dx = dy
		self.dy = 0
		self.layer = gcommon.C_LAYER_SKY
		self.score = 100
	def update(self):
		if self.state == 0:
			self.y += self.dy
			self.dy *= 0.95
			if abs(self.dy) < 0.1:
				self.dx = 0
				self.nextState()
		elif self.state == 1:
			self.x += self.dx
			self.dx -= 0.2
			if self.dx > 3:
				self.dx = 3
		if self.x < 32:
			for i in range(16):
				enemy_shot_dr(self.x + 8, self.y + 3, 2, 0, i*4)
			self.remove()
		
	def drawMissile(self):
		pyxel.blt(self.x, self.y, 1, 80, 72, 32, 7, gcommon.TP_COLOR)
		
	def draw(self):
		self.drawMissile()
		if self.cnt & 2 == 0:
			if self.cnt & 4 == 0:
				pyxel.blt(self.x + 32, self.y, 1, 48, 72, 32, 7, gcommon.TP_COLOR)
			else:
				pyxel.blt(self.x + 32, self.y-1, 1, 48, 72, 32, -7, gcommon.TP_COLOR)


class DockArm(EnemyBase):
	def __init__(self, t):
		super(DockArm, self).__init__()
		pos = gcommon.mapPosToScreenPos(t[2], t[3])
		self.x = pos[0]
		self.y = pos[1]
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.ground = True
		self.shotHitCheck = False
		self.hitCheck = False
		self.startCnt = t[4]
		self.shift = 0

	def update(self):
		if self.cnt > self.startCnt:
			self.shift += 1
			if self.shift >= 80:
				self.remove()

	def draw(self):
		pyxel.blt(self.x, self.y -self.shift, 1, 240, 64, 16, 80, gcommon.TP_COLOR)
		pyxel.blt(self.x, self.y+ 96 +self.shift, 1, 240, 64, 16, 80, gcommon.TP_COLOR)
		

class Cell1(EnemyBase):
	def __init__(self, t):
		super(Cell1, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.left = 2
		self.top = 2
		self.right = 13
		self.bottom = 13
		self.hp = 10
		#self.layer = gcommon.C_LAYER_UNDER_GRD
		self.layer = gcommon.C_LAYER_SKY
		self.score = 100
		self.expsound = gcommon.SOUND_CELL_EXP
		self.shotFlag = True

	def update(self):
		if self.cnt > 900:
			self.remove()
		else:
			if self.cnt & 32 == 0:
				dr = gcommon.get_direction_my(self.x +8, self.y +8)
				self.x += gcommon.direction_map[dr][0] * 1.25
				self.y -= gcommon.direction_map[dr][1] * 1.25
			if self.cnt & 127 == 127 and self.shotFlag:
				enemy_shot(self.x +8, self.y +8, 2, 0)
		
	def draw(self):
		n = int(self.cnt/5) %3
		pyxel.blt(self.x, self.y, 1, 0 + n* 16, 168, 16, 16, gcommon.TP_COLOR)


class Cell1Group1(EnemyBase):
	def __init__(self, t):
		super(Cell1Group1, self).__init__()
		self.startX = t[2]
		self.startY = t[3]
		self.hv = t[4]			# 0 横から出現   1: 上下から出現
		self.hitCheck = False
		self.shotHitCheck = False

	def update(self):
		if self.hv == 0:
			if self.cnt == 0:
				obj = gcommon.ObjMgr.addObj(Cell1([0,0, self.startX, self.startY]))
				obj.shotFlag = gcommon.GameSession.isNormalOrMore()
			elif self.cnt == 20:
				obj = gcommon.ObjMgr.addObj(Cell1([0,0, self.startX, self.startY + 50]))
				obj.shotFlag = gcommon.GameSession.isNormalOrMore()
			elif self.cnt == 40:
				obj = gcommon.ObjMgr.addObj(Cell1([0,0, self.startX, self.startY + 20]))
			elif self.cnt == 60:
				obj = gcommon.ObjMgr.addObj(Cell1([0,0, self.startX, self.startY + 70]))
				obj.shotFlag = gcommon.GameSession.isNormalOrMore()
			elif self.cnt == 80:
				obj = gcommon.ObjMgr.addObj(Cell1([0,0, self.startX, self.startY + 30]))
				obj.shotFlag = gcommon.GameSession.isNormalOrMore()
				self.remove()
		else:
			if self.cnt == 0:
				obj = gcommon.ObjMgr.addObj(Cell1([0,0, self.startX, self.startY]))
				obj.shotFlag = gcommon.GameSession.isNormalOrMore()
			elif self.cnt == 20:
				obj = gcommon.ObjMgr.addObj(Cell1([0,0, self.startX +50, self.startY]))
				obj.shotFlag = gcommon.GameSession.isNormalOrMore()
			elif self.cnt == 40:
				gcommon.ObjMgr.addObj(Cell1([0,0, self.startX +20, self.startY]))
			elif self.cnt == 60:
				obj = gcommon.ObjMgr.addObj(Cell1([0,0, self.startX +70, self.startY]))
				obj.shotFlag = gcommon.GameSession.isNormalOrMore()
			elif self.cnt == 80:
				obj = gcommon.ObjMgr.addObj(Cell1([0,0, self.startX +30, self.startY]))
				obj.shotFlag = gcommon.GameSession.isNormalOrMore()
				self.remove()

	def draw(self):
		pass

class Cell2(EnemyBase):
	def __init__(self, t):
		super(Cell2, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.dx = t[4]
		self.dy = t[5]
		self.dr = t[6]		# 0: 水平方向
		self.left = 4
		self.top = 4
		self.right = 19
		self.bottom = 19
		self.hp = 100
		#self.layer = gcommon.C_LAYER_UNDER_GRD
		self.layer = gcommon.C_LAYER_GRD
		self.ground = True
		self.score = 200

	def update(self):
		self.x += self.dx
		self.y += self.dy
		if self.dr == 0:
			if self.x <= -24 or self.x > gcommon.SCREEN_MAX_X+1:
				self.remove()
			else:
				if self.dy < 0:
					if gcommon.isMapFreePos(self.x +4, self.y + 2 * self.dy) == False:
						self.dy = -1 * self.dy
					elif gcommon.isMapFreePos(self.x +4, self.y + 4 * self.dy) == False:
						self.dy = -1 * self.dy
				else:
					if gcommon.isMapFreePos(self.x +4, self.y +24 + 2 * self.dy) == False:
						self.dy = -1 * self.dy
					elif gcommon.isMapFreePos(self.x +4, self.y +24 + 4 * self.dy) == False:
						self.dy = -1 * self.dy

		#if self.cnt & 127 == 127:
		#	enemy_shot(self.x +8, self.y +8, 2, 0)
		
	def draw(self):
		n = int(self.cnt/5) %3
		pyxel.blt(self.x, self.y, 1, 48 + n* 24, 144, 24, 24, gcommon.TP_COLOR)


#
# 土台付触手
class Worm1(EnemyBase):
	def __init__(self, t):
		super(Worm1, self).__init__()
		pos = gcommon.mapPosToScreenPos(t[2], t[3])
		self.x = pos[0]
		self.y = pos[1]
		self.baseDr = t[4]		# 0:右向き 2:上向き 4:左向き 6:下向き
								# 1:右上  3:左上 5:左下 7:右下
		self.cellCount = t[5]
		self.growCount = t[6]
		self.left = 2
		self.top = 2
		self.right = 21
		self.bottom = 15
		self.hp = 60
		#self.layer = gcommon.C_LAYER_UNDER_GRD
		self.layer = gcommon.C_LAYER_GRD
		self.ground = True
		self.score = 200
		self.dr = 48
		self.offsetX = 4
		self.offsetY = 0
		if gcommon.GameSession.difficulty == gcommon.DIFFICULTY_EASY:
			self.shotCycle  = 63
		else:
			self.shotCycle  = 31

		if self.baseDr ==0:
			self.dr = 0
			self.offsetX = 0
			self.offsetY = 4
		elif self.baseDr ==1:
			self.dr = 56
			self.offsetX = 8
			self.offsetY = 8
		elif self.baseDr ==2:
			self.dr = 48
			self.offsetX = 4
			self.offsetY = 0
		elif self.baseDr ==3:
			self.dr = 40
			self.offsetX = 8
			self.offsetY = 8
		elif self.baseDr ==4:
			self.dr = 32
			self.offsetX = 0
			self.offsetY = 4
		elif self.baseDr ==6:
			self.dr = 16
			self.offsetX = 4
			self.offsetY = 0
		elif self.baseDr ==7:
			self.dr = 8
			self.offsetX = 8
			self.offsetY = 8
		else:
			pass
		self.subDr = 0
		self.cells = []
		for i in range(0, self.cellCount):
			self.cells.append([0,0])

		# 触手セルの当たり判定範囲
		self.cellRect = gcommon.Rect.create(2,2,13,13)

	def update(self):
		if self.state != 0 and self.x < -32 or self.y > 250:
			self.remove()
			return
		if self.state == 0:
			# 待機状態
			if self.cnt > self.growCount:
				self.nextState()
		elif self.state == 1:
			# 触手伸ばす
			x = 0
			y = 0
			for pos in self.cells:
				pos[0] = x + math.cos(gcommon.atan_table[(self.dr) & 63]) * 12 * (self.cnt) /30.0
				pos[1] = y + math.sin(gcommon.atan_table[(self.dr) & 63]) * 12 * (self.cnt) /30.0
				x = pos[0]
				y = pos[1]
			if self.cnt == 30:
				self.nextState()
		elif self.state == 2:
			if self.cnt & self.shotCycle == self.shotCycle:
				self.shot()
			i = 0
			x = 0
			y = 0
			for pos in self.cells:
				pos[0] = x + math.cos(gcommon.atan_table[(int(self.dr + i * self.subDr)) & 63]) * 12
				pos[1] = y + math.sin(gcommon.atan_table[(int(self.dr + i * self.subDr)) & 63]) * 12
				x = pos[0]
				y = pos[1]
				i += 1
			self.subDr += 0.05
			if self.subDr >= 3.0:
				self.state = 3
		elif self.state == 3:
			if self.cnt & self.shotCycle == self.shotCycle:
				self.shot()
			i = 0
			x = 0
			y = 0
			for pos in self.cells:
				pos[0] = x + math.cos(gcommon.atan_table[(int(self.dr + i * self.subDr)) & 63]) * 12
				pos[1] = y + math.sin(gcommon.atan_table[(int(self.dr + i * self.subDr)) & 63]) * 12
				x = pos[0]
				y = pos[1]
				i += 1
			self.subDr -= 0.05
			if self.subDr <= -3.0:
				self.state = 2
		elif self.state == 100:
			if self.cnt > 2:
				if len(self.cells) > 0:
					# 最後の要素
					pos = self.cells.pop()
					create_explosion(self.x+pos[0] +8, self.y+pos[1]+8, self.layer, self.exptype)
					self.cnt = 0
				else:
					create_explosion(self.x+(self.right-self.left+1)/2, self.y+(self.bottom-self.top+1)/2, self.layer, self.exptype)
					self.remove()
		
	
	def shot(self):
		pos = self.cells[len(self.cells) -1]
		enemy_shot(self.x +self.offsetX +pos[0] +8, self.y +self.offsetY +pos[1] +8, 2, 0)

	
	def draw(self):
		size = len(self.cells)
		i = 0
		while(i<size):
			pos = self.cells[size -1 -i]
			if i == 0:
				pyxel.blt(self.x +self.offsetX + pos[0], self.y +self.offsetY +pos[1], 1, 64, 168, 16, 16, 3)
			else:
				pyxel.blt(self.x +self.offsetX + pos[0], self.y +self.offsetY +pos[1], 1, 48, 168, 16, 16, 3)
			i += 1

		#	if len(self.cells)> 0:
		#		# 触手部の当たり判定（先端のみ）
		#		pos = self.cells[len(self.cells) -1]
		#		x = self.x +self.offsetX +pos[0]
		#		y = self.y +self.offsetY +pos[1]
		#		pyxel.rect(x+ self.cellRect.left, y +self.cellRect.top, self.cellRect.right-self.cellRect.left+1, self.cellRect.bottom-self.cellRect.top+1, 7)

		if self.baseDr == 0:
			pyxel.blt(self.x, self.y, 1, 104, 168, 16, 24, 3)
		elif self.baseDr == 1:
			pyxel.blt(self.x, self.y, 1, 120, 168, 32, 32, 3)
		elif self.baseDr == 2:
			pyxel.blt(self.x, self.y, 1, 80, 168, 24, 16, 3)
		elif self.baseDr == 3:
			pyxel.blt(self.x, self.y, 1, 120, 168, -32, 32, 3)
		elif self.baseDr == 4:
			pyxel.blt(self.x, self.y, 1, 104, 168, -16, 24, 3)
		elif self.baseDr == 6:
			pyxel.blt(self.x, self.y, 1, 80, 168, 24, -16, 3)
		elif self.baseDr == 7:
			pyxel.blt(self.x, self.y, 1, 120, 168, 32, -32, 3)

	# 自機弾と敵との当たり判定と破壊処理
	def checkShotCollision(self, shot):
		if shot.removeFlag:
			return False
		hit = False
		if gcommon.check_collision(self, shot):
			hit = True
		else:
			if len(self.cells)> 0:
				# 触手部の当たり判定（先端のみ）
				pos = self.cells[len(self.cells) -1]
				x = self.x +self.offsetX +pos[0]
				y = self.y +self.offsetY +pos[1]
				if gcommon.check_collision2(x, y, self.cellRect, shot):
					hit = True
		
		if hit:
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
		if gcommon.check_collision(self, gcommon.ObjMgr.myShip):
			return True
		else:
			# 触手部の当たり判定
			for pos in self.cells:
				x = self.x +self.offsetX +pos[0]
				y = self.y +self.offsetY +pos[1]
				if gcommon.check_collision2(x, y, self.cellRect, gcommon.ObjMgr.myShip):
					return True
			return False

	def broken(self):
		gcommon.GameSession.addScore(self.score)
		self.state = 100
		self.cnt = 0
		self.shotHitCheck = False


class Worm2Cell:
	def __init__(self, offsetX, offsetY, dr, cnt):
		self.offsetX = offsetX
		self.offsetY = offsetY
		self.dr = dr
		self.cnt = cnt


class Worm2(EnemyBase):
	def __init__(self, t):
		super(Worm2, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.dr = t[4]
		self.tbl = t[5]
		self.left = 2
		self.top = 2
		self.right = 21
		self.bottom = 21
		self.hp = 600
		#self.layer = gcommon.C_LAYER_UNDER_GRD
		self.layer = gcommon.C_LAYER_GRD
		self.ground = True
		self.score = 100
		self.tblIndex = 0
		self.subcnt = self.tbl[self.tblIndex][0]

	def update(self):
		self.x += gcommon.cos_table[int(self.dr) & 63]
		self.y += gcommon.sin_table[int(self.dr) & 63]
		if self.x < -24 or self.y < -24 or self.y > gcommon.SCREEN_MAX_Y:
			self.remove()
		else:
			if self.tblIndex < len(self.tbl):
				self.dr += self.tbl[self.tblIndex][1]
				self.subcnt -=1
				if self.subcnt <= 0:
					self.tblIndex += 1
					if self.tblIndex < len(self.tbl):
						self.subcnt =  self.tbl[self.tblIndex][0]
	
	def draw(self):
		n = int(self.cnt/11) %3
		pyxel.blt(self.x, self.y, 1, 48, 144, 24, 24, gcommon.TP_COLOR)


worm2Tbl1 = [
	[74, 0],
	[32, -0.5],
]

worm2Tbl2 = [
	[74, 0],
	[32, 0.5],
]

worm2Tbl3 = [
	[49, 0],
	[32, -0.5],
	[128, 0.25],
]

worm2Tbl4 = [
	[50, 0],
	[32, 0.5],
	[128, -0.25],
	[50, 0],
]

class Worm2Group(EnemyBase):
	def __init__(self, t):
		super(Worm2Group, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.dr = t[4]
		self.cellCount = t[5]
		self.tbl = t[6]
		self.layer = gcommon.C_LAYER_GRD
		self.ground = True
		self.hitCheck = False
		self.shotHitCheck = False

	def update(self):
		if self.cnt % 15 == 0:
			gcommon.ObjMgr.addObj(Worm2([0, 0, self.x, self.y, self.dr, self.tbl]))
			self.cellCount -= 1
			if self.cellCount == 0:
				self.remove()

	def draw(self):
		pass

# 遅延発生イベント
class Delay(EnemyBase):
	def __init__(self, cls, t, delayTime):
		super(Delay, self).__init__()
		self.cls = cls
		self.t = t
		self.delayTime = delayTime
		self.hitCheck = False
		self.shotHitCheck = False

	def update(self):
		if self.cnt == self.delayTime:
			gcommon.ObjMgr.addObj(self.cls(self.t))
			self.remove()

	def draw(self):
		pass


class StageClear(EnemyBase):
	def __init__(self, t):
		super(StageClear, self).__init__()
		self.layer = gcommon.C_LAYER_TEXT
		self.x = gcommon.SCREEN_MAX_X +1
		self.y = 90
		self.hitCheck = False
		self.shotHitCheck = False
		self.stageNo = t[2]
		self.text = "STAGE " + str(self.stageNo) + " CLEAR"
		gcommon.BGM.playOnce(gcommon.BGM.STAGE_CLEAR)
		gcommon.ObjMgr.myShip.setSubScene(5)

	def update(self):
		if self.state == 0:
			self.x -= 4
			if self.x < 80:
				self.nextState()
		elif self.state == 1:
			if self.cnt > 180:
				self.remove()
				gcommon.app.startNextStage()

	def draw(self):
		if self.stageNo != 6:
			gcommon.showText(self.x, self.y, self.text)

class FixedShutter1(EnemyBase):
	def __init__(self, mx, my, size):
		super(FixedShutter1, self).__init__()
		pos = gcommon.mapPosToScreenPos(mx, my)
		self.x = pos[0]		# screen x
		self.y = pos[1]		# screen y
		self.size = size	# 大きさ（16ドット単位）
		self.left = 0
		self.right = 15
		self.top = 0
		self.bottom = 16 * self.size -1
		self.hp = 200
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.exptype = gcommon.C_EXPTYPE_GRD_M
		self.hitcolor1 = 13
		self.hitcolor2 = 7
		self.ground = True
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = True
		self.score = 400

	def update(self):
		pass

	def draw(self):
		for i in range(self.size):
			pyxel.blt(self.x, self.y + i * 16, 1, 64, 96, 16, 16)

# 上下シャッター
class Shutter1(EnemyBase):
	def __init__(self, x, y, direction, size, mode, speed, param1, param2):
		super(Shutter1, self).__init__()
		self.x = x		# screen x
		self.y = y		# screen y
		self.direction = direction	# 1: 上から下 -1:下から上
		self.size = size	# 大きさ（16ドット単位）
		self.speed = speed
		self.mode = mode	# 動作モード
			# 0:閉まる→開く（繰り返し）
			#   param1 : 閉まり始めるまでの時間
			#   param2 : 開くまでの時間
		self.param1 = param1
		self.param2 = param2
		self.dy = 0
		self.left = 0
		self.right = 15
		self.top = 0
		self.bottom = 16 * self.size
		self.hp = gcommon.HP_UNBREAKABLE
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.ground = True
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = True
		self.shotEffect = False

	def update(self):
		if self.x <= -16:
			self.remove()
			return
		if self.mode == 0:
			if self.state == 0 and self.cnt >= self.param1:
				self.dy += self.speed
				self.y += self.direction * self.speed
				if self.dy >= self.size * 16:
					self.nextState()
			elif self.state == 1 and self.cnt >= self.param2:
				self.nextState()
			elif self.state == 2:
				self.dy -= self.speed
				self.y -= self.direction * self.speed
				if self.dy <=0:
					self.setState(0)

	def draw(self):
		for i in range(self.size):
			pyxel.blt(self.x, self.y + i * 16, 1, 64, 96, 16, 16)

# 落下物基本クラス
class FallingObject(EnemyBase):
	def __init__(self, mx, my, direction, mWidth, mHeight, needDummyBlock):
		super(FallingObject, self).__init__()
		pos = gcommon.mapPosToScreenPos(mx, my)
		self.x = pos[0]		# screen x
		self.y = pos[1]		# screen y
		self.mx = mx
		self.my = my
		self.direction = direction		# 1 or -1
		self.mWidth = mWidth	# 幅（8ドット単位）
		self.mHeight = mHeight	# 高さ（8ドット単位）
		self.left = 0
		self.right = self.mWidth * 8 -1
		self.top = 0
		self.bottom = self.mHeight * 8 -1
		self.hp = 999999
		self.layer = gcommon.C_LAYER_GRD
		self.ground = True
		self.hitCheck = True
		self.shotHitCheck = True
		self.needDummyBlock = needDummyBlock	# 砲台などの場合False、壁はTrue
		if self.needDummyBlock:
			gcommon.setMapDataByMapPos2(self.mx, self.my, gcommon.DUMMY_BLOCK_NO, self.mWidth, self.mHeight)
		else:
			gcommon.setMapDataByMapPos2(self.mx, self.my, 0, self.mWidth, self.mHeight)

	def update(self):
		# if self.cnt == 0:
		# 	if self.needDummyBlock:
		# 		gcommon.setMapDataByMapPos2(self.mx, self.my, gcommon.DUMMY_BLOCK_NO, self.mWidth, self.mHeight)
		# 	else:
		# 		gcommon.setMapDataByMapPos2(self.mx, self.my, 0, self.mWidth, self.mHeight)
		if self.x + self.right < 0:
			self.remove()
			return
		exist = False
		for i in range(self.mWidth):
			check = False
			if self.direction == 1:
				check = gcommon.isMapFreePos(self.x + i*8, self.y +self.mHeight * 8)
			else:
				check = gcommon.isMapFreePos(self.x + i*8, self.y -1)
			if check == False:
				# 何かある
				exist = True
				if self.state == 1:
					if self.needDummyBlock:
						# 落ちている状態だったら、そこを障害物として埋める
						mpos = gcommon.screenPosToMapPos(self.x, self.y)
						gcommon.setMapDataByMapPos2(mpos[0], mpos[1], gcommon.DUMMY_BLOCK_NO, self.mWidth, self.mHeight)
					# 落ちていない状態とする
					self.state = 0
				break
		if exist == False:
			# 下に何もない
			if self.state == 0:
				if self.needDummyBlock:
					# 今の場所をクリアする
					mpos = gcommon.screenPosToMapPos(self.x, self.y)
					gcommon.setMapDataByMapPos2(mpos[0], mpos[1], 0, self.mWidth, self.mHeight)
				# 落ちる状態に移行
				self.state = 1
			self.y += self.direction
			if self.y >= 384 or self.y + self.bottom < -192:
				self.remove()

	# 破壊されたとき
	def broken(self):
		super(FallingObject, self).broken()
		mpos = gcommon.screenPosToMapPos(self.x, self.y)
		gcommon.setMapDataByMapPos2(mpos[0], mpos[1], 0, self.mWidth, self.mHeight)


# 遺跡柱
class RuinPillar1(FallingObject):
	def __init__(self, mx, my, direction, size):
		super(RuinPillar1, self).__init__(mx, my, direction, 2, size, True)
		self.size = size	# 高さ（8ドット単位） 2 - 6
		self.hp = 30
		self.score = 50
		self.bx = (self.size -2) * 2
		self.enemyShotCollision = True

	def draw(self):
		pyxel.bltm(int(self.x), self.y, 0, self.bx, 0, 2, self.size * 8, gcommon.TP_COLOR)
		#pyxel.rectb(self.x +self.left, self.y + self.top, self.right -self.left+1, self.bottom -self.top+1, 7)


# 遺跡床
class RuinFloor1(FallingObject):
	def __init__(self, mx, my, direction, size):
		super(RuinFloor1, self).__init__(mx, my, direction, size*2, 2, True)
		self.size = size
		self.left = 0
		self.top = 4
		self.right = self.mWidth * 8
		self.bottom = self.mHeight * 8 -5
		self.by = (self.size -2) * 2
		self.enemyShotCollision = True
		self.shotEffect = False

	def update(self):
		super(RuinFloor1, self).update()
		if self.direction == 1:
			if self.y > gcommon.SCREEN_MAX_Y:
				self.remove()
				return
		else:
			if self.y <= -16:
				self.remove()
				return

	def draw(self):
		pyxel.bltm(self.x, self.y, 0, 14, self.by, self.size *2, 2, gcommon.TP_COLOR)
		#pyxel.rectb(self.x +self.left, self.y + self.top, self.right -self.left+1, self.bottom -self.top+1, 7)

# 遺跡と落ちる砲台
class Battery2(FallingObject):
	def __init__(self, mx, my, direction):
		# direction  1:通常 -1:上下逆
		super(Battery2, self).__init__(mx, my, direction, 2, 2, False)
		self.left = 2
		self.right = 13
		self.interval = int(63 / gcommon.enemy_shot_rate)
		if self.direction == 1:
			self.top = 5
			self.bottom = 15
		else:
			self.top = 0
			self.bottom = 10
		self.hp = 10
		self.score = 300

	def update(self):
		super(Battery2, self).update()
		if self.cnt % self.interval == self.interval -1:
			enemy_shot(self.x+8,self.y+6, 2, 0)

	def draw(self):
		if self.direction == 1:
			drawBattery1(self.x, self.y, 0)
		else:
			drawBattery1(self.x, self.y, 1)

# 指定した方向にパーティクル
class Particle1(EnemyBase):
	def __init__(self, cx, cy, rad, count, life):
		super(Particle1, self).__init__()
		self.x = cx
		self.y = cy
		self.rad = rad
		self.tbl = []
		self.count = count
		self.layer = gcommon.C_LAYER_EXP_SKY
		self.hitCheck = False
		self.shotHitCheck = False
		self.speedDown = True		# Falseにするとスピード落ちない
		for i in range(0, count):
			r = rad + random.random() * math.pi/4 - math.pi/8
			speed = random.random() * 6
			s = SplashItem(cx, cy, speed * math.cos(r), speed * math.sin(r), random.randrange(int(life/5), life))
			self.tbl.append(s)

	@classmethod
	def append(cls, x, y, rad):
		return gcommon.ObjMgr.addObj(Particle1(x, y, rad, 8, 50))

	@classmethod
	def appendPos(cls, pos, rad):
		return gcommon.ObjMgr.addObj(Particle1(pos[0], pos[1], rad, 8, 50))

	@classmethod
	def appendCenter(cls, obj, rad):
		pos = gcommon.getCenterPos(obj)
		return gcommon.ObjMgr.addObj(Particle1(pos[0], pos[1], rad, 8, 50))

	@classmethod
	def appendShotCenter(cls, obj):
		rad = math.atan2(obj.dy, obj.dx)
		pos = gcommon.getCenterPos(obj)
		return gcommon.ObjMgr.addObj(Particle1(pos[0], pos[1], rad, 8, 50))

	@classmethod
	def appendShotCenterReverse(cls, obj):
		rad = math.atan2(-obj.dy, -obj.dx)
		pos = gcommon.getCenterPos(obj)
		return gcommon.ObjMgr.addObj(Particle1(pos[0], pos[1], rad, 2, 10))

	def update(self):
		newTbl = []
		for s in self.tbl:
			s.cnt -= 1
			if s.cnt > 0:
				newTbl.append(s)
				s.x += s.dx
				s.y += s.dy
				if self.speedDown:
					s.dx *= 0.97
					s.dy *= 0.97
		self.tbl = newTbl
		if len(self.tbl) == 0:
			self.remove()

	def draw(self):
		for s in self.tbl:
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

# 爆発パーティクル
class Particle2(EnemyBase):
	def __init__(self, cx, cy, count):
		super(Particle2, self).__init__()
		self.x = cx
		self.y = cy
		self.count = count
		self.tbl = []
		self.layer = gcommon.C_LAYER_EXP_SKY
		self.hitCheck = False
		self.shotHitCheck = False
		for i in range(0, self.count):
			r = random.random() * math.pi * 2
			speed = random.random() * 6
			s = SplashItem(cx, cy, speed * math.cos(r), speed * math.sin(r), random.randrange(10, 50))
			self.tbl.append(s)

	@classmethod
	def append(cls, x, y, count):
		gcommon.ObjMgr.objs.append(Particle2(x, y, count))

	@classmethod
	def appendPos(cls, pos, count):
		gcommon.ObjMgr.objs.append(Particle2(pos[0], pos[1], count))

	@classmethod
	def appendCenter(cls, obj, count):
		pos = gcommon.getCenterPos(obj)
		gcommon.ObjMgr.objs.append(Particle2(pos[0], pos[1], count))

	def update(self):
		newTbl = []
		for s in self.tbl:
			s.cnt -= 1
			if s.cnt > 0:
				newTbl.append(s)
				s.x += s.dx
				s.y += s.dy
				s.dx *= 0.97
				s.dy *= 0.97
		self.tbl = newTbl
		if len(self.tbl) == 0:
			self.remove()

	def draw(self):
		for s in self.tbl:
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

class Stage4BossAppear1:
	def __init__(self, t):
		#gcommon.setMapDataByMapPos2(256 +5, 152-128, 0, 18, 1)
		#gcommon.setMapDataByMapPos2(256 +5, 175-128, 0, 18, 1)
		gcommon.setMapDataByMapPos2(232, 24, 0, 12, 1)
		gcommon.setMapDataByMapPos2(232, 47, 0, 12, 1)

	def do(self):
		pass

class Stage4BossAppear2:
	def __init__(self, t):
		#gcommon.setMapDataByMapPos2(256 +23, 152-128, 0, 18, 1)
		#gcommon.setMapDataByMapPos2(256 +23, 175-128, 0, 18, 1)
		gcommon.setMapDataByMapPos2(244, 24, 0, 12, 1)
		gcommon.setMapDataByMapPos2(244, 47, 0, 12, 1)

	def do(self):
		pass


class Wind1(EnemyBase):
	def __init__(self, t):
		super(Wind1, self).__init__()
		pos = gcommon.mapPosToScreenPos(t[2], t[3])
		self.x = pos[0]
		self.y = pos[1]
		self.direction = t[4] # direction_mapに従う 2:下から上  6:上から下 0:右  4:左
		self.size = t[5]	# 24ドット単位
		self.left = 0
		self.top = 0
		if self.direction == 2:
			self.x += 4
			self.right = 23
			self.top = -24 * self.size
			self.bottom = 7
		elif self.direction == 6:
			self.x += 5
			self.right = 23
			self.top = 0
			self.bottom = 24 * self.size
		elif self.direction == 0:
			self.y += 4
			self.right = 24 * self.size
			self.bottom = 23
		elif self.direction == 4:
			self.y += 4
			self.left = -24 * self.size
			self.right = 15
			self.bottom = 23
		self.hp = 999999
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.ground = True
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False

	@classmethod
	def create(cls, x, y, direction, size):
		return Wind1([0, 0, x, y, direction, size])

	def update(self):
		if self.x + self.right < 0:
			self.remove()

	def draw(self):
		if self.direction == 6:
			# 上から下
			sy = self.y -24
			if self.cnt & 1 == 1:
				for i in range(self.size):
					y = sy + i * 24 + (self.cnt % 24)
					pyxel.blt(self.x, y, 2, 0, 0, 24, 24, gcommon.TP_COLOR)
			else:
				for i in range(self.size):
					y = sy + i * 24 + (self.cnt % 48)/2
					pyxel.blt(self.x, y, 2, 0, 0, -24, 24, gcommon.TP_COLOR)
		elif self.direction == 2:
			# 下から上
			sy = self.y +8
			if self.cnt & 1 == 1:
				for i in range(self.size):
					y = sy - i * 24 - (self.cnt % 24)
					pyxel.blt(self.x, y, 2, 0, 0, 24, 24, gcommon.TP_COLOR)
			else:
				for i in range(self.size):
					y = sy - i * 24 - (self.cnt % 48)/2
					pyxel.blt(self.x, y, 2, 0, 0, -24, 24, gcommon.TP_COLOR)
		elif self.direction == 0:
			# 右
			sx = self.x -24
			if self.cnt & 1 == 1:
				for i in range(self.size):
					x = sx + i * 24 + (self.cnt % 24)
					pyxel.blt(x, self.y, 2, 0, 0, 24, 24, gcommon.TP_COLOR)
			else:
				for i in range(self.size):
					x = sx + i * 24 + (self.cnt % 48)/2
					pyxel.blt(x, self.y, 2, 0, 0, -24, 24, gcommon.TP_COLOR)
		elif self.direction == 4:
			# 右
			sx = self.x +8
			if self.cnt & 1 == 1:
				for i in range(self.size):
					x = sx - i * 24 - (self.cnt % 24)
					pyxel.blt(x, self.y, 2, 0, 0, 24, 24, gcommon.TP_COLOR)
			else:
				for i in range(self.size):
					x = sx - i * 24 - (self.cnt % 48)/2
					pyxel.blt(x, self.y, 2, 0, 0, -24, 24, gcommon.TP_COLOR)

	# 自機と敵との当たり判定
	# ここで自機が動かされる
	def checkMyShipCollision(self):
		if gcommon.check_collision(self, gcommon.ObjMgr.myShip):
			#gcommon.cur_map_dy = self.direction/2
			gcommon.ObjMgr.myShip.x += gcommon.direction_map[self.direction][0]/2
			if gcommon.ObjMgr.myShip.x < 0:
				gcommon.ObjMgr.myShip.x = 0
			elif gcommon.ObjMgr.myShip.x > 240:
				gcommon.ObjMgr.myShip.x = 240
			gcommon.ObjMgr.myShip.y += gcommon.direction_map[self.direction][1]/2
			if gcommon.ObjMgr.myShip.y < 2:
				gcommon.ObjMgr.myShip.y = 2
			elif gcommon.ObjMgr.myShip.y > 176:
				gcommon.ObjMgr.myShip.y = 176
		return False		

circulatorBladePoints1 = [
	[0,0],[0,61],[6,60],[12,0]
]

circulatorBladePoints2 = [
	[0,0],[0,61],[-6,60],[-12,0]
]

class Circulator1(EnemyBase):
	def __init__(self, x, y, direction):
		super(Circulator1, self).__init__()
		self.x = x
		self.y = y
		self.direction = direction
		self.left = 4
		self.top = 4
		self.hp = 999999
		self.layer = gcommon.C_LAYER_GRD
		self.ground = True
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.rad = 0
		self.xpoints1 = []
		self.xpoints2 = []

	def update(self):
		if self.x < -80:
			self.remove()
			return
		global circulatorBladePoints1
		global circulatorBladePoints2
		if self.direction == 1:
			self.rad += math.pi /180
			if self.rad > math.pi * 2:
				self.rad -= math.pi *2
		else:
			self.rad -= math.pi /180
			if self.rad < 0:
				self.rad = math.pi *2 + self.rad
		self.xpoints1 = []
		self.xpoints2 = []
		for i in range(4):
			self.xpoints1.append(gcommon.getAnglePoints([self.x, self.y],
				circulatorBladePoints1, [0, -8], self.rad + math.pi*i/2))
			self.xpoints2.append(gcommon.getAnglePoints([self.x, self.y],
				circulatorBladePoints2, [0, -8], self.rad + math.pi*i/2))

	def draw(self):
		for p in self.xpoints1:
			gcommon.drawQuadrangle(p, 6)
		for p in self.xpoints2:
			gcommon.drawQuadrangle(p, 5)
		#pyxel.blt(self.x-20, self.y-20, 1, 128, 56, 40, 40, gcommon.TP_COLOR)
		pyxel.blt(self.x-12, self.y-12, 2, 24, 0, 24, 24, gcommon.TP_COLOR)

	# 自機と敵との当たり判定
	def checkMyShipCollision(self):
		pos = gcommon.getCenterPos(gcommon.ObjMgr.myShip)
		for p in self.xpoints1:
			if gcommon.checkCollisionPointAndPolygon(pos, p):
				return True
		for p in self.xpoints2:
			if gcommon.checkCollisionPointAndPolygon(pos, p):
				return True
		return False
	
	def checkShotCollision(self, shot):
		pos = gcommon.getCenterPos(shot)
		for p in self.xpoints1:
			if gcommon.checkCollisionPointAndPolygon(pos, p):
				return True
		for p in self.xpoints2:
			if gcommon.checkCollisionPointAndPolygon(pos, p):
				return True
		return False

# リフトで移動する砲台
class Battery3(EnemyBase):
	def __init__(self, x, y, direction):
		# direction  1:下 -1:上
		super(Battery3, self).__init__()
		self.x = x
		self.y = y
		self.direction = direction
		self.layer = gcommon.C_LAYER_GRD
		self.ground = True
		self.left = 2
		self.right = 13
		if self.direction == 1:
			self.top = 5
			self.bottom = 15
		else:
			self.top = 0
			self.bottom = 10
		self.hp = 10
		self.score = 300

	def update(self):
		self.y += self.direction * 0.5
		if self.direction == 1 and self.y > gcommon.SCREEN_MAX_Y:
			self.remove()
			return
		elif self.direction == -1 and self.y + self.bottom < 0:
			self.remove()
			return
		elif self.x < -16:
			self.remove()
			return
		if self.cnt & 63 == 63:
			enemy_shot(self.x+8,self.y+6, 2, 0)

	def draw(self):
		drawBattery1(self.x, self.y, 0)


class Lift1(EnemyBase):
	def __init__(self, x, y, direction):
		super(Lift1, self).__init__()
		self.x = x
		self.y = y
		self.direction = direction	# 1:下  -1:上
		self.left = 4
		self.top = 0
		self.right = 63
		self.bottom = 15
		self.hp = 999999
		self.shotEffect = False
		self.layer = gcommon.C_LAYER_GRD
		self.ground = True
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = True

	def update(self):
		self.y += self.direction * 0.5
		if self.direction == 1 and self.y > gcommon.SCREEN_MAX_Y:
			self.remove()
		elif self.direction == -1 and self.y + self.bottom < 0:
			self.remove()

	def draw(self):
		pyxel.blt(self.x, self.y, 2, 48, 0, 64, 16, gcommon.TP_COLOR)


class LiftAppear1(EnemyBase):
	def __init__(self, mx, my, direction):
		super(LiftAppear1, self).__init__()
		pos = gcommon.mapPosToScreenPos(mx, my)
		self.x = pos[0]
		self.y = pos[1]
		self.direction = direction	# 1:下  -1:上
		self.left = 4
		self.top = 4
		self.right = 6
		self.bottom = 15
		self.hp = 999999
		self.layer = gcommon.C_LAYER_GRD
		self.ground = True
		self.hitCheck = False
		self.shotHitCheck = False
		self.enemyShotCollision = False
		self.interval = 120

	def update(self):
		if self.cnt % self.interval == 0:
			self.createLift()
		if self.x + self.right < 0:
			self.remove()

	def draw(self):
		pass

	def createLift(self):
		if self.direction == 1:
			# 下
			gcommon.ObjMgr.addObj(Lift1(self.x, -16, self.direction))
			gcommon.ObjMgr.addObj(Battery3(self.x +16, -32, self.direction))
		else:
			# 上
			gcommon.ObjMgr.addObj(Lift1(self.x, gcommon.SCREEN_MAX_Y+1+16, self.direction))
			gcommon.ObjMgr.addObj(Battery3(self.x +16, gcommon.SCREEN_MAX_Y+1, self.direction))

# 脚下側左
waker1LowerLeg1 = [
	[2,34],[15,3],[5,37]
]

# 
# waker1LowerLeg2 = [
# 	[5,37],[15,3],[24,3],[20,37],[15,39]
# ]
waker1LowerLeg2 = [
	[5,37],[15,3],[20,3],[12,39]
]

# waker1LowerLeg3 = [
# 	[20,37],[24,3],[26,5],[26,34]
# ]
waker1LowerLeg3 = [
	[12,39],[20,3],[22,5],[16,37]
]

waker1UpperLeg1 = [
	[0,2],[3,0],[3,28],[0,26]
]
waker1UpperLeg2 = [
	[3,0],[8,0],[8,28],[3,28]
]
waker1UpperLeg3 = [
	[8,0],[11,2],[11,26],[8,28]
]

# ２円の交点を求める
def get2CirclesIntersection(pos1, r1, pos2, r2):
	a = 2 * (pos2[0] - pos1[0])
	b = 2 * (pos2[1] - pos1[1])
	c = (pos1[0]+pos2[0])*(pos1[0] -pos2[0])+ (pos1[1]+pos2[1])*(pos1[1]-pos2[1]) + (r2+r1)*(r2-r1)
	D = abs(a * pos1[0] + b * pos1[1] + c)
	x1 = (a * D - b * math.sqrt((a*a + b*b) * r1*r1 - D*D))/(a*a + b*b) + pos1[0]
	y1 = (b * D + a * math.sqrt((a*a + b*b) * r1*r1 - D*D))/(a*a + b*b) + pos1[1]
	x2 = (a * D + b * math.sqrt((a*a + b*b) * r1*r1 - D*D))/(a*a + b*b) + pos1[0]
	y2 = (b * D - a * math.sqrt((a*a + b*b) * r1*r1 - D*D))/(a*a + b*b) + pos1[1]
	return [[x1, y1], [x2, y2]]


class HomingMissile1(EnemyBase):
	directionTable = [
		[0, 1, 1],	# 0
		[1, 1, 1],	# 1
		[2, 1, 1],	# 2
		[3, 1, 1],	# 3
		[4, 1, 1],	# 4
		[3, -1, 1],	# 5
		[2, -1, 1],	# 6
		[1, -1, 1],	# 7
		[0, -1, 1],	# 8
		[1, -1, -1],	# 9
		[2, -1, -1],	# 10
		[3, -1, -1],	# 11
		[4, -1, -1],	# 12
		[3, 1, -1],		# 13
		[2, 1, -1],		# 14
		[1, 1, -1]		# 15
	]
	def __init__(self, x, y, dr):
		super(HomingMissile1, self).__init__()
		self.x = x
		self.y = y
		self.left = -4
		self.top = -4
		self.right = 4
		self.bottom = 4
		self.hp = 10
		self.dr = dr
		self.layer = gcommon.C_LAYER_SKY
		self.score = 10
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
	
	def update(self):
		if self.x < -16 or self.x > gcommon.SCREEN_MAX_X or self.y <-16 or self.y > gcommon.SCREEN_MAX_Y:
			self.remove()
			return
		if self.cnt < 120 and self.cnt & 1 == 0:
			tempDr = gcommon.get_atan_no_to_ship(self.x, self.y)
			self.dr = (self.dr + gcommon.get_leftOrRight(self.dr, tempDr)) & 63
		self.x += math.cos(gcommon.atan_table[self.dr & 63]) * 2
		self.y += math.sin(gcommon.atan_table[self.dr & 63]) * 2
		
				
	def draw(self):
		d = ((self.dr + 2) & 63)>>2
		fx = math.cos(gcommon.atan_table[d<<2]) * 8
		fy = math.sin(gcommon.atan_table[d<<2]) * 8
		if self.cnt & 2 == 0:
			if self.cnt & 1 == 0:
				pyxel.blt(self.x -7.5 -fx, self.y -7.5 -fy, 2, 200, 64, 16, 16, gcommon.TP_COLOR)
			else:
				pyxel.blt(self.x -7.5 -fx, self.y -7.5 -fy, 2, 216, 64, 16, 16, gcommon.TP_COLOR)
		t = HomingMissile1.directionTable[d]
		pyxel.blt(self.x -7.5, self.y -7.5, 2, 120 + t[0] * 16, 64, 16 * t[1], 16 * -t[2], gcommon.TP_COLOR)

class SpotLight(EnemyBase):
	def __init__(self, parent):
		super(SpotLight, self).__init__()
		self.parent = parent
		self.x = parent.x + 11
		self.y = parent.y + 31
		self.layer = gcommon.C_LAYER_SKY
		self.ground = False
		self.hitCheck = False
		self.shotHitCheck = False
		self.enemyShotCollision = False
		self.lightRad = math.pi

	def update(self):
		self.x = self.parent.x + 11
		self.y = self.parent.y + 31
		self.lightRad = math.atan2(gcommon.ObjMgr.myShip.y - self.y, gcommon.ObjMgr.myShip.x - self.x)

	def draw(self):
		# ライト
		x = self.x
		y = self.y
		poly = [[x, y], 
			[x + 300 * math.cos(self.lightRad + math.pi*10/180), y + 300 * math.sin(self.lightRad + math.pi*10/180)],
			[x + 300 * math.cos(self.lightRad - math.pi*10/180), y + 300 * math.sin(self.lightRad - math.pi*10/180)]
		]
		xpoly = gcommon.clipPolygon(poly)
		gcommon.setBrightness1()
		gcommon.drawPolygonSystemImage(xpoly)
		pyxel.pal()

#    P
#      Q
#   R
class Walker1(EnemyBase):
	A_length = 24  # Pを中心とする円の半径
	B_length = 34  # Rを中心とする円の半径
	C_length = 15
	def __init__(self, t):
		super(Walker1, self).__init__()
		self.x = t[2]
		self.y = gcommon.mapYToScreenY(t[3])
		self.left = 16
		self.top = 24
		self.right = 55
		self.bottom = 47
		self.hp = 500
		self.layer = gcommon.C_LAYER_GRD
		self.ground = True
		self.score = 1000
		self.exptype = gcommon.C_EXPTYPE_GRD_M
		self.gy = 50

			
		self.PPoint = [0, 0]

		#self.RStart = [-19, self.gy]
		self.RStart = [-12, self.gy]
		self.REnd = [14, self.gy]

		self.QStart = []
		self.QEnd = []

		self.SPoint = [(self.REnd[0]+self.RStart[0])/2.0, self.RStart[1]+15]
		self.SRadius = 0

		self.counter = 0
		self.stepCount = 35
		self.stateCycle = 0
		self.mode = 0
		
		self.RArray = []
		self.colorTable = [[12,5,1],[6,12,5]]

		# R中心の円と、P中心の円から、Q点を求める
		tt = get2CirclesIntersection(self.RStart, Walker1.B_length, self.PPoint, Walker1.A_length)
		self.QStart = tt[0]
		tt = get2CirclesIntersection(self.REnd, Walker1.B_length, self.PPoint, Walker1.A_length)
		self.QEnd = tt[0]
		
		self.SRadius = math.sqrt( math.pow(self.RStart[0] - self.SPoint[0], 2) + math.pow(self.RStart[1] - self.SPoint[1], 2))

		self.atanStart = math.atan2((self.RStart[1] - self.SPoint[1]), (self.RStart[0] - self.SPoint[0]))
		self.atanEnd = math.atan2((self.REnd[1] - self.SPoint[1]), (self.REnd[0] - self.SPoint[0]))

		self.lightRad = math.pi
		self.lightRound = 1

		for i in range(self.stepCount):
			rad2 = self.atanStart + (self.atanEnd - self.atanStart) * i /self.stepCount
			R2 = [self.SPoint[0] + math.cos(rad2) * self.SRadius, self.SPoint[1] + math.sin(rad2) * self.SRadius]
			
			self.RArray.append(R2)
		
		for i in range(self.stepCount):
			R2 = [self.RStart[0] + (self.REnd[0]-self.RStart[0]) * (self.stepCount -i)/self.stepCount,
				self.RStart[1] + (self.REnd[1]-self.RStart[1]) * (self.stepCount -i)/self.stepCount]
			self.RArray.append(R2)

		# スポットライト
		self.spotLight = SpotLight(self)
		gcommon.ObjMgr.addObj(self.spotLight)

	def update(self):
		if self.x < -60:
			self.remove()
			return
		if self.mode == 0:
			if (self.stateCycle % 3 == 0 and self.x < 150) or (self.stateCycle % 3 != 0 and self.x < 100):
				mx = gcommon.screenPosToMapPosX(self.x)
				if mx > 44:
					# 停止
					self.setMode(4)
				else:
					self.nextMode()
		elif self.mode == 1:
			self.x += 1
			self.counter += 1
			if self.counter == len(self.RArray)/2:
				self.nextMode()
		elif self.mode == 2:
			if (self.stateCycle % 3 == 0 and self.x < 150) or (self.stateCycle % 3 != 0 and self.x < 100):
				self.nextMode()
		elif self.mode == 3:
			self.x += 1
			self.counter += 1
			if self.counter == len(self.RArray):
				self.counter = 0
				self.stateCycle += 1
				self.setMode(0)
		if self.cnt > 120 and self.cnt & 31 ==0:
			gcommon.ObjMgr.addObj(HomingMissile1(self.x + 20, self.y +10, 32))
			enemy_shot(self.x +35, self.y +31, 2, 0)
		if self.mode in (0, 1,2,3):
			self.RountLight()

	def RountLight(self):
		if self.lightRound == 1:
			self.lightRad += math.pi /120
			if self.lightRad > math.pi + math.pi/4:
				 self.lightRound = -1
		elif self.lightRound == -1:
			self.lightRad -= math.pi /120
			if self.lightRad < math.pi - math.pi/4:
				 self.lightRound = 1

	def nextMode(self):
		self.mode = self.mode + 1

	def setMode(self, mode):
		self.mode = mode

	# def checkShotCollision(self, shot):
	# 	ret = super(Walker1, self).checkShotCollision(shot)
	# 	if ret:
	# 		rad = math.atan2(shot.dy, shot.dx)
	# 		Particle1.appendCenter(shot, rad)
	# 	return ret

	def remove(self):
		super(Walker1, self).remove()
		if self.spotLight != None:
			self.spotLight.remove()
			self.spotLight = None

	# 破壊されたとき
	def broken(self):
		super(Walker1, self).broken()

	def draw(self):
		#pyxel.tri(x, y,
		#	x + 128 * math.cos(self.lightRad + math.pi*10/180),
		# 	y + 128 * math.sin(self.lightRad + math.pi*10/180),
		# 	x + 128 * math.cos(self.lightRad - math.pi*10/180),
		# 	y + 128 * math.sin(self.lightRad - math.pi*10/180),
		# 	10)

		ox = 44 -8
		oy = 36
		# 足のループ
		for i in range(2):
			if i == 1:
				# 本体の描画（足の間に描く必要がある）
				pyxel.blt(self.x, self.y, 2, 0, 0, 58, 48, gcommon.TP_COLOR)

			R2 = self.RArray[(self.counter + self.stepCount * i) % (self.stepCount*2)]
			# 足首
			pyxel.blt(self.x +8 +R2[0], self.y +28 +R2[1], 2, 0, 56, 48, 16, gcommon.TP_COLOR)
			
			tt = get2CirclesIntersection(R2, Walker1.B_length, self.PPoint, Walker1.A_length)
			Q2 = tt[0]

			polygonList = []
			polygonList.append(gcommon.Polygon(waker1UpperLeg1, self.colorTable[1][0]))
			polygonList.append(gcommon.Polygon(waker1UpperLeg2, self.colorTable[1][1]))
			polygonList.append(gcommon.Polygon(waker1UpperLeg3, self.colorTable[1][2]))
			rad = math.atan2(Q2[1] -self.PPoint[1], Q2[0] -self.PPoint[0])
			gcommon.drawPolygons(gcommon.getAnglePolygons([self.x +ox +self.PPoint[0], self.y +oy +self.PPoint[1]], polygonList, [6.5,3], rad - math.pi/2))

			polygonList = []
			polygonList.append(gcommon.Polygon(waker1LowerLeg1, self.colorTable[1][0]))
			polygonList.append(gcommon.Polygon(waker1LowerLeg2, self.colorTable[1][1]))
			polygonList.append(gcommon.Polygon(waker1LowerLeg3, self.colorTable[1][2]))
			rad = math.atan2(R2[1]- Q2[1], R2[0]-Q2[0])
			gcommon.drawPolygons(gcommon.getAnglePolygons([self.x +ox +Q2[0], self.y +oy +Q2[1]], polygonList, [20,6], rad - math.pi/2 - math.pi/32))

			pyxel.blt(self.x, self.y, 2, 0, 0, 58, 39, gcommon.TP_COLOR)
			if i == 1:
				pyxel.blt(self.x +ox -16 +Q2[0], self.y +oy -12 +Q2[1], 2, 48, 48, 24, 24, gcommon.TP_COLOR)

# シリンダー一番太い部分
spider1Leg1a = [
	[0,0],[11,0],[11,25],[0,25]
]
spider1Leg1b = [
	[2,0],[9,0],[9,25],[2,25]
]
spider1Leg1c = [
	[4,0],[7,0],[7,25],[4,25]
]

# 次に太い部分
spider1Leg2a = [
	[0,0],[9,0],[9,25],[0,25]
]
spider1Leg2b = [
	[2,0],[7,0],[7,25],[2,25]
]
spider1Leg2c = [
	[4,0],[5,0],[5,25],[4,25]
]

# 一番細い部分
spider1Leg3a = [
	[0,0],[5,0],[5,25],[0,25]
]
spider1Leg3b = [
	[1,0],[4,0],[4,25],[1,25]
]
spider1Leg3c = [
	[2,0],[3,0],[3,25],[2,25]
]

class Spider1Leg():
	def __init__(self):
		self.rad = 0.0
		self.xpolygonList1 = None
		self.xpolygonList2 = None
		self.xpolygonList3 = None
		self.x2 = 0
		self.y2 = 0


class Spider1(EnemyBase):
	# 動作, 時間
	#   動作  0:停止  1:左に移動  2:右に移動
	moveTable = [
		[1, 180],
		[0, 40],
		[2, 300],
		[0, 40],	# 下の穴に逃げ込む
		[1, 90],
		[0, 40],
		[2, 360],
		[0, 20],	# 上の穴に逃げ込む
		[1, 90],	# 左に行っている間に前に逃げる
		[0, 60],
		[2, 270],	# 前でぎりぎり
		[0, 20],
		[1, 60],
		[0, 20],
		[2, 160],
		[0, 20],
		[2, 200],
		[0, 10],
		[1, 360],
	]

	def __init__(self, t):
		super(Spider1, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.left = 8
		self.top = 9
		self.right = 103
		self.bottom = 54
		self.hp = 9999999
		self.layer = gcommon.C_LAYER_GRD
		self.ground = True
		self.score = 200
		self.legPos = 0
		self.legMax = 36
		self.legAngle = 40		#35
		self.rad1 = 0
		self.legHeight = 48.5
		self.moveState = 0
		self.state = 2
		self.polygonList1 = []
		self.polygonList1.append(gcommon.Polygon(spider1Leg3a, 5))
		self.polygonList1.append(gcommon.Polygon(spider1Leg3b, 13))
		self.polygonList1.append(gcommon.Polygon(spider1Leg3c, 7))
		self.polygonList2 = []
		self.polygonList2.append(gcommon.Polygon(spider1Leg2a, 5))
		self.polygonList2.append(gcommon.Polygon(spider1Leg2b, 13))
		self.polygonList2.append(gcommon.Polygon(spider1Leg2c, 7))
		self.polygonList3 = []
		self.polygonList3.append(gcommon.Polygon(spider1Leg1a, 4))
		self.polygonList3.append(gcommon.Polygon(spider1Leg1b, 9))
		self.polygonList3.append(gcommon.Polygon(spider1Leg1c, 10))
		self.legs = []
		for i in range(6):
			self.legs.append(Spider1Leg())
		# くつ？の当たり判定Rect
		self.upperShoe = gcommon.Rect.create(4, 0, 19, 6)
		self.lowerShoe = gcommon.Rect.create(4, 9, 19, 15)
		self.moveIndex = 0
		self.moveCnt = 0

	def update(self):
		self.rad1 = self.legPos * math.pi * 2  * self.legAngle /360 /self.legMax
		if self.moveIndex >= len(Spider1.moveTable):
			pass
		else:
			t = Spider1.moveTable[self.moveIndex]
			if t[0] == 0:
				# 停止
				pass
			elif t[0] == 1:
				# 左に移動
				self.walkLeft()
			elif t[0] == 2:
				# 右に移動
				self.walkRight()
			self.moveCnt += 1
			if self.moveCnt >= t[1]:
				self.moveIndex +=1
				self.moveCnt = 0

		# if self.state == 0:
		# 	if self.x < 90:
		# 		self.nextState()
		# elif self.state == 1:
		# 	self.walkForward()
		# 	if self.x >= 180:
		# 		self.nextState()
		# elif self.state == 2:
		# 	self.walkBackward()
		# 	if self.x < 30:
		# 		self.setState(1)

		# 1
		self.updateLeg(self.legs[0], self.x +7.5, self.y+8, math.pi * 2 * (90 + self.legAngle/2 +20)/360, -1, 0, -1)
		# 2
		self.updateLeg(self.legs[1], self.x +54, self.y+8, math.pi * 2 * (90 -self.legAngle/2)/360, 1, 1, -1)
		# 3
		self.updateLeg(self.legs[2], self.x +103.5, self.y+8, math.pi * 2 * (90 + self.legAngle/2 -20)/360, -1, 0, -1)

		# 4
		self.updateLeg(self.legs[3], self.x +7.5, self.y+55, math.pi * 2 * (-90 +self.legAngle/2 -20)/360, -1, 1, 1)
		# 5
		self.updateLeg(self.legs[4], self.x +54, self.y+55, math.pi * 2 * (-90 -self.legAngle/2)/360, 1, 0, 1)
		# 6
		self.updateLeg(self.legs[5], self.x +103.5, self.y+55, math.pi * 2 * (-90 +self.legAngle/2 +20)/360, -1, 1, 1)

	# 右に歩く
	def walkRight(self):
		self.x += 1
		if self.moveState == 0:
			self.legPos += 1
			if self.legPos >= self.legMax:
				self.moveState = 1
		else:
			self.legPos -= 1
			if self.legPos <= 0:
				self.moveState = 0
	# 左に歩く
	def walkLeft(self):
		self.x -= 1
		if self.moveState == 0:
			self.legPos -= 1
			if self.legPos <= 0:
				self.moveState = 1
		else:
			self.legPos += 1
			if self.legPos >= self.legMax:
				self.moveState = 0

	# objにはmyShipかshot
	def checkLegCollision(self, obj):
		pos = gcommon.getCenterPos(obj)
		for i in range(6):
			leg = self.legs[i]
			if gcommon.checkCollisionPointAndPolygon(pos, leg.xpolygonList1.polygons[0].points):
				return True
			if gcommon.checkCollisionPointAndPolygon(pos, leg.xpolygonList2.polygons[0].points):
				return True
			if gcommon.checkCollisionPointAndPolygon(pos, leg.xpolygonList3.polygons[0].points):
				return True
			if i >= 0 and i <= 2:
				if gcommon.check_collision2(leg.x2 - 11.5, leg.y2 -8, self.upperShoe, obj):
					return True
			else:
				if gcommon.check_collision2(leg.x2 - 11.5, leg.y2 -8, self.lowerShoe, obj):
					return True
		return False

	# 自機と敵との当たり判定
	def checkMyShipCollision(self):
		if super(Spider1, self).checkMyShipCollision():
			return True
		return self.checkLegCollision(gcommon.ObjMgr.myShip)
		
	def checkShotCollision(self, shot):
		if super(Spider1, self).checkShotCollision(shot):
			return True
		return self.checkLegCollision(shot)

	# 1  2  3
	# 4  5  6
	def draw(self):
		pyxel.blt(self.x, self.y, 2, 72, 0, 112, 64, gcommon.TP_COLOR)
		# 1
		self.drawLeg2(self.legs[0], self.x +7.5, self.y+8, -1)
		# 2
		self.drawLeg2(self.legs[1], self.x +54, self.y+8, -1)
		# 3
		self.drawLeg2(self.legs[2], self.x +103.5, self.y+8, -1)

		# 4
		self.drawLeg2(self.legs[3], self.x +7.5, self.y+55, 1)
		# 5
		self.drawLeg2(self.legs[4], self.x +54, self.y+55, 1)
		# 6
		self.drawLeg2(self.legs[5], self.x +103.5, self.y+55, 1)

		# # 1
		# self.drawLeg(self.x +7.5, self.y+8, math.pi * 2 * (90 + self.legAngle/2 +20)/360, -1, 0, -1)
		# # 2
		# self.drawLeg(self.x +54, self.y+8, math.pi * 2 * (90 -self.legAngle/2)/360, 1, 1, -1)
		# # 3
		# self.drawLeg(self.x +103.5, self.y+8, math.pi * 2 * (90 + self.legAngle/2 -20)/360, -1, 0, -1)

		# # 4
		# self.drawLeg(self.x +7.5, self.y+55, math.pi * 2 * (-90 +self.legAngle/2 -20)/360, -1, 1, 1)
		# # 5
		# self.drawLeg(self.x +54, self.y+55, math.pi * 2 * (-90 -self.legAngle/2)/360, 1, 0, 1)
		# # 6
		# self.drawLeg(self.x +103.5, self.y+55, math.pi * 2 * (-90 +self.legAngle/2 +20)/360, -1, 1, 1)

	def updateLeg(self, leg, x, y, angleOffset, signFlag, shrinkState, isLower):
		x1 = x
		y1 = y
		rad = angleOffset  + signFlag * self.rad1
		# Y方向の長さから、斜辺の長さを得る
		length = abs(self.legHeight / math.sin(rad))
		if shrinkState == self.moveState:
			# 脚が上がっているので縮む
			length = length -  math.sin(self.legPos * math.pi/ self.legMax) * length * 0.4
		# x2,y2は先端の座標
		leg.x2 = x1 + math.cos(rad) * length
		leg.y2 = y1 - math.sin(rad) * length
		#pyxel.line(x1, y1, x2, y2, 7)
		px = x1 + math.cos(rad) * (length -25)
		py = y1 - math.sin(rad) * (length -25)
		leg.xpolygonList1 = gcommon.getAnglePolygons([px, py], self.polygonList1, [2.5,0], -rad - math.pi/2)
		px = x1 + math.cos(rad) * (length -25)/2
		py = y1 - math.sin(rad) * (length -25)/2
		leg.xpolygonList2 = gcommon.getAnglePolygons([px, py], self.polygonList2, [4.5,0], -rad - math.pi/2)
		leg.xpolygonList3 = gcommon.getAnglePolygons([x1, y1], self.polygonList3, [5.5,0], -rad - math.pi/2)

	# def drawLeg(self, x, y, angleOffset, signFlag, shrinkState, isLower):
	# 	x1 = x
	# 	y1 = y
	# 	rad = angleOffset  + signFlag * self.rad1
	# 	# Y方向の長さから、斜辺の長さを得る
	# 	length = abs(self.legHeight / math.sin(rad))
	# 	if shrinkState == self.moveState:
	# 		# 脚が上がっているので縮む
	# 		length = length -  math.sin(self.legPos * math.pi/ self.legMax) * length * 0.3
	# 	# x2,y2は先端の座標
	# 	x2 = x1 + math.cos(rad) * length
	# 	y2 = y1 - math.sin(rad) * length
	# 	#pyxel.line(x1, y1, x2, y2, 7)
	# 	px = x1 + math.cos(rad) * (length -25)
	# 	py = y1 - math.sin(rad) * (length -25)
	# 	gcommon.drawPolygons(gcommon.getAnglePolygons([px, py], self.polygonList1, [2.5,0], -rad - math.pi/2))
	# 	px = x1 + math.cos(rad) * (length -25)/2
	# 	py = y1 - math.sin(rad) * (length -25)/2
	# 	gcommon.drawPolygons(gcommon.getAnglePolygons([px, py], self.polygonList2, [4.5,0], -rad - math.pi/2))
	# 	gcommon.drawPolygons(gcommon.getAnglePolygons([x1, y1], self.polygonList3, [5.5,0], -rad - math.pi/2))
	# 	# 付け根の丸いやつ
	# 	pyxel.blt(x -7.5, y -7.5, 2, 96, 128, 16, 16, gcommon.TP_COLOR)
	# 	# かかとを描く
	# 	pyxel.blt(x2 - 11.5, y2 -8, 2, 80, 64, 24, 16 * isLower, gcommon.TP_COLOR)

	def drawLeg2(self, leg, x, y, isLower):
		gcommon.drawPolygons(leg.xpolygonList1)
		gcommon.drawPolygons(leg.xpolygonList2)
		gcommon.drawPolygons(leg.xpolygonList3)
		# 付け根の丸いやつ
		pyxel.blt(x -7.5, y -7.5, 2, 104, 64, 16, 16, gcommon.TP_COLOR)
		# かかとを描く
		pyxel.blt(leg.x2 - 11.5, leg.y2 -8, 2, 80, 64, 24, 16 * isLower, gcommon.TP_COLOR)

# 回転するシャッター
class Shutter2(EnemyBase):
	poly1 = [
		[2, 32], [5,0], [10,0], [13,32]
	]
	poly2 = [
		[2, 32], [5,0], [4,32]
	]
	poly3 = [
		[11, 32], [10,0], [13,32]
	]
	def __init__(self, x, y, isUpper, waitTime):
		super(Shutter2, self).__init__()
		self.x = x
		self.y = y
		self.left = -4
		self.top = -4
		self.right = 4
		self.bottom = 4
		self.rad1 = 0
		self.isUpper = isUpper
		self.waitTime = waitTime
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.ground = True
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False
		self.polygonList1 = []
		self.polygonList1.append(gcommon.Polygon(Shutter2.poly1, 13))
		self.polygonList1.append(gcommon.Polygon(Shutter2.poly2, 6))
		self.polygonList1.append(gcommon.Polygon(Shutter2.poly3, 5))
		self.xpolygonList1 = []

	def update(self):
		if self.cnt > self.waitTime and self.rad1 < math.pi:
			self.rad1 += math.pi * 2/360
			if self.rad1 > math.pi:
				self.rad1 = math.pi
		 
		if self.isUpper:
			self.xpolygonList1 = gcommon.getAnglePolygons2([self.x, self.y], self.polygonList1, [7.5,28], -self.rad1 +math.pi, 1, -1)
		else:
			self.xpolygonList1 = gcommon.getAnglePolygons2([self.x, self.y], self.polygonList1, [7.5,28], self.rad1 -math.pi, 1, 1)

	def draw(self):
		if self.isUpper:
			gcommon.drawPolygons(self.xpolygonList1)
		else:
			gcommon.drawPolygons(self.xpolygonList1)

	# 自機と敵との当たり判定
	def checkMyShipCollision(self):
		pos = gcommon.getCenterPos(gcommon.ObjMgr.myShip)
		if gcommon.checkCollisionPointAndPolygon(pos, self.xpolygonList1.polygons[0].points):
			return True
		return False
	
	def checkShotCollision(self, shot):
		pos = gcommon.getCenterPos(shot)
		if gcommon.checkCollisionPointAndPolygon(pos, self.xpolygonList1.polygons[0].points):
			return True
		return False

def drawTank1(x, y, mirror):
	dr8 = 0
	dr8 = gcommon.get_direction_my(x+8, y +8)
	sx = 0
	sy = 224
	width = 24
	height = 24
	y = int(y)
	if mirror == 0:
		if dr8  in (0, 1):
			pyxel.blt(x, y, 1, sx, sy, -width, height, gcommon.TP_COLOR)
		elif dr8 == 2:
			pyxel.blt(x, y, 1, sx +96, sy, width, height, gcommon.TP_COLOR)
		elif dr8 in (3, 4):
			pyxel.blt(x, y, 1, sx, sy, width, height, gcommon.TP_COLOR)
		elif dr8 in (5, 6):
			pyxel.blt(x, y, 1, sx +72, sy, width, height, gcommon.TP_COLOR)
		elif dr8 == 7:
			pyxel.blt(x, y, 1, sx +72, sy, -width, height, gcommon.TP_COLOR)
	else:
		if dr8 == 0:
			pyxel.blt(x, y, 1, sx, sy, -width, -height, gcommon.TP_COLOR)
		elif dr8 == 1:
			pyxel.blt(x, y, 1, sx +72, sy, -width, -height, gcommon.TP_COLOR)
		elif dr8 == 2:
			pyxel.blt(x, y, 1, sx +96, sy, width, -height, gcommon.TP_COLOR)
		elif dr8 == 3:
			pyxel.blt(x, y, 1, sx +72, sy, width, -height, gcommon.TP_COLOR)
		elif dr8 == 4:
			pyxel.blt(x, y, 1, sx, sy, width, -height, gcommon.TP_COLOR)
		elif dr8 == 5:
			pyxel.blt(x, y, 1, sx, sy, width, -height, gcommon.TP_COLOR)
		elif dr8 == 6:
			pyxel.blt(x, y, 1, sx +96, sy, width, -height, gcommon.TP_COLOR)
		elif dr8 == 7:
			pyxel.blt(x, y, 1, sx +72, sy, -width, -height, gcommon.TP_COLOR)

# TANKと言いつつ、歩行型移動砲台
class Tank1(EnemyBase):
	# 0 :左に移動, 移動先座標
	# 1 :右に移動, 移動先座標
	# 2 :攻撃, 0
	actionPatterns = [
		[[0, 50], [2, 0], [1, 200], [2, 0], [0, -30]],
		[[1, 200],[2, 0], [0, 50], [2, 0], [1, 150], [0, -30]],
		[[1, 150],[2, 0], [0, 50], [2, 0], [1, 100], [2, 0], [0, -30]],
		[[1, 60], [2, 0], [0, -30]],
	]
	def __init__(self, t):
		super(Tank1, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.mirror = t[4]	# 0: normal 1:上下逆
		self.actionPattern = t[5]
		if self.mirror:
			self.top = 6
			self.bottom = 20
		else:
			self.top = 3
			self.bottom = 17
		self.left = 5
		self.right = 19
		self.hp = 10
		self.layer = gcommon.C_LAYER_GRD
		self.ground = True
		self.actions = Tank1.actionPatterns[self.actionPattern]
		self.score = 100

	def update(self):
		action = self.actions[self.state][0]
		param = self.actions[self.state][1]
		if action == 0:
			# 右から左に移動
			self.x -= 1
			if self.x <= -24:
				self.remove()
			elif self.x <= param:
				self.nextState()
		elif action == 1:
			# 左から右に移動
			self.x += 1
			self.x += gcommon.cur_scroll_x
			if self.x > gcommon.SCREEN_MAX_X:
				self.remove()
			elif self.x >= param:
				self.nextState()
		elif action == 2:
			if self.cnt == 30:
				enemy_shot(self.x+8,self.y+10, 2, 0)
			if self.cnt >= 60:
				self.nextState()

	def draw(self):
		action = self.actions[self.state][0]
		if action == 2:
			drawTank1(self.x, self.y, self.mirror)
		else:
			height = 24
			if self.mirror == 1:
				height = -height
			sx = ((self.cnt>>2) % 3) * 24
			if action == 0:
				pyxel.blt(self.x, self.y, 1, sx, 224, 24, height, gcommon.TP_COLOR)
			elif action == 1:
				pyxel.blt(self.x, self.y, 1, sx, 224, -24, height, gcommon.TP_COLOR)


class Laser1(EnemyBase):
	def __init__(self, x, y):
		super(Laser1, self).__init__()
		self.x = x
		self.y = y
		self.speed = 4
		self.left = 2
		self.top = 0
		self.right = 13
		self.bottom = 1
		self.layer = gcommon.C_LAYER_SKY
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False

	def update(self):
		self.x -= self.speed
		if self.x <= -16:
			self.remove()
	
	def draw(self):
		pyxel.blt(self.x, self.y, 1, 64, 168, 16, 2, gcommon.TP_COLOR)

# レーザーを打ってくる戦闘機
class Fighter2(EnemyBase):
	def __init__(self, t):
		super(Fighter2, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.brakeX = t[4]
		self.dx = -3
		self.direction = t[5]	# -1: 上  1:下
		self.left = 5
		self.top = 4
		self.right = 21
		self.bottom = 27
		self.hp = 30
		self.layer = gcommon.C_LAYER_SKY
		self.ground = False
		self.score = 300


	def update(self):
		if self.state == 0:
			self.x += self.dx
			if self.x <= self.brakeX:
				self.dx += 0.1
				if self.dx >= -0.1:
					self.nextState()
		elif self.state == 1:
			self.y += self.direction * 0.5
			if self.cnt % 20 == 0:
				gcommon.ObjMgr.addObj(Laser1(self.x, self.y +4))
				gcommon.ObjMgr.addObj(Laser1(self.x, self.y +26))
			if self.cnt > 120:
				self.dx = 0.0
				self.nextState()
		elif self.state == 2:
			self.x += self.dx
			if self.dx > -4.0:
				self.dx -= 0.05
			if self.x <= -32:
				self.remove()

	def draw(self):
		pyxel.blt(self.x, self.y, 1, 32, 168, 32, 32, gcommon.TP_COLOR)

# ミサイル砲台
class MissileBattery1(EnemyBase):
	def __init__(self, mx, my, mirror):
		super(MissileBattery1, self).__init__()
		pos = gcommon.mapPosToScreenPos(mx, my)
		self.x = pos[0]
		self.y = pos[1]
		self.mirror = mirror
		self.left = 2
		self.top = 2
		self.right = 13
		self.bottom = 13
		self.hp = 30
		self.layer = gcommon.C_LAYER_GRD
		self.ground = True
		self.first = 120
		self.interval = 120
		self.score = 200

	def update(self):
		if self.cnt == self.first or (self.cnt != 0 and (self.cnt % self.interval == 0)):
			if self.mirror:
				gcommon.ObjMgr.addObj(HomingMissile1(self.x + 7.5, self.y +12, 16))
			else:
				gcommon.ObjMgr.addObj(HomingMissile1(self.x + 7.5, self.y +4, 48))

	def draw(self):
		if self.mirror:
			pyxel.blt(self.x, self.y, 1, 0, 184, 16, -16, gcommon.TP_COLOR)
		else:
			pyxel.blt(self.x, self.y, 1, 0, 184, 16, 16, gcommon.TP_COLOR)

# ファン２
class Fan2(EnemyBase):
	def __init__(self, x, y, direction):
		super(Fan2, self).__init__()
		self.x = x
		self.y = y
		self.direction = direction	# 0 - 7
		self.left = 2
		self.top = 2
		self.right = 13
		self.bottom = 13
		self.hp = 1
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.ground = True
		self.score = 10

	def update(self):
		if self.state == 0:
			dy = gcommon.direction_map[self.direction][1]
			self.x += gcommon.direction_map[self.direction][0]
			self.y += dy
			if dy > 0:
				if self.y > gcommon.ObjMgr.myShip.y:
					self.nextState()
			else:
				if self.y < gcommon.ObjMgr.myShip.y:
					self.nextState()
		else:
			self.x -= 2

	def draw(self):
		if self.cnt % 2 == 0:
			pyxel.blt(self.x, self.y, 1, 0, 168, 16, 16, gcommon.TP_COLOR)
		else:
			pyxel.blt(self.x, self.y, 1, 16, 168, 16, 16, gcommon.TP_COLOR)

class Fan2Group(EnemyBase):
	def __init__(self, mx, my, direction, waitTime):
		super(Fan2Group, self).__init__()
		pos = gcommon.mapPosToScreenPos(mx, my)
		self.x = pos[0]
		self.y = pos[1]
		self.ground = True
		self.direction = direction
		self.waitTime = waitTime
		self.interval = 20
		self.max = 10
		self.cnt2 = 0
		self.hitCheck = False
		self.shotHitCheck = False
		self.enemyShotCollision = False

	def update(self):
		if self.state == 0:
			if self.cnt > self.waitTime:
				self.nextState()
		elif self.state == 1:
			if self.cnt % self.interval == 0:
				offsetX = 0
				offsetY = 0
				if self.direction == 2:
					offsetY = 8
				elif self.direction == 6:
					offsetY = -16
				elif self.direction == 3:
					offsetX = 16
					offsetY = 16
				elif self.direction == 5:
					offsetX = 16
					offsetY = -24
				gcommon.ObjMgr.addObj(Fan2(self.x + offsetX, self.y +offsetY, self.direction))
				self.cnt2 += 1
				if self.cnt2 >= self.max:
					self.remove()

	def draw(self):
		pass

# 上下シャッター
class Shutter3(EnemyBase):
	def __init__(self, mx, my, direction, waitTime):
		super(Shutter3, self).__init__()
		pos = gcommon.mapPosToScreenPos(mx, my)
		self.x = pos[0]
		self.direction = direction		# -1:上 1:下
		if self.direction == -1:
			# 下から上に閉まる
			self.stopY = pos[1]
			self.y = gcommon.SCREEN_MAX_Y +1
			self.height = self.y -self.stopY
			self.top = 0
			self.bottom = self.height -1
		else:
			# 上から下に閉まる
			# Y座標より上に突き出るようになっている
			self.stopY = pos[1] +7
			self.y = gcommon.SCREEN_MIN_Y -1
			self.height = self.stopY -self.y
			self.top = -self.height +1
			self.bottom = -1
		self.left = 0
		self.right = 15
		self.rad1 = 0
		self.waitTime = waitTime
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.hp = gcommon.HP_UNBREAKABLE
		self.ground = True
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False

	def update(self):
		if self.x <= -16:
			self.remove()
		else:
			if self.cnt > self.waitTime:
				if self.direction == -1:
					# 上
					self.y -= 1
					if self.y < self.stopY:
						self.y = self.stopY
				else:
					# 下
					self.y += 1
					if self.y > self.stopY:
						self.y = self.stopY
	def draw(self):
		yy = 0
		while(yy < self.height):
			pyxel.blt(self.x, self.y +self.top +yy, 1, 0, 200, 16, 16, gcommon.TP_COLOR)
			yy += 16

class ContinuousShot(EnemyBase):
	def __init__(self, x, y, shotType, shotCount, shotInterval, speed):
		super(ContinuousShot, self).__init__()
		self.x = x
		self.y = y
		self.dr64 = gcommon.get_atan_no_to_ship(self.x, self.y)
		self.shotType = shotType
		self.shotCount = shotCount
		self.shotInterval = shotInterval
		self.speed = speed
		# layerをC_LAYER_E_SHOTにすることで、removeEnemyShotで削除される
		self.layer = gcommon.C_LAYER_E_SHOT
		self.ground = False
		self.hitCheck = False
		self.shotHitCheck = False
		self.enemyShotCollision = False

	@classmethod
	def create(cls, x, y, shotType, shotCount, shotInterval, speed):
		gcommon.ObjMgr.addObj(ContinuousShot(x, y, shotType, shotCount, shotInterval, speed))

	def update(self):
		if self.cnt % self.shotInterval == 0:
			enemy_shot_dr(self.x, self.y, self.speed, self.shotType, self.dr64)
			self.shotCount -= 1
			if self.shotCount == 0:
				self.remove()

	def draw(self):
		pass


# 画面の敵弾を消去する
def removeEnemyShot():
	newObjs = []
	for obj in gcommon.ObjMgr.objs:
		if obj.removeFlag == False and obj.layer == gcommon.C_LAYER_E_SHOT:
			obj.remove()
		else:
			newObjs.append(obj)
	gcommon.ObjMgr.objs = newObjs

class BattleShip1(EnemyBase):
	def __init__(self, t):
		super(BattleShip1, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.isRed = t[4]
		self.moveTable = t[5]
		self.laserTime = t[6]
		self.fighterTime = t[7]
		self.hp = gcommon.HP_UNBREAKABLE
		self.collisionRects = gcommon.Rect.createFromList(
			[[21,23,188,72],[190,14,258,87],[260,2,339,100],[340,9,511,77]])
		self.layer = gcommon.C_LAYER_SKY
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.cnt2 = 0
		self.mover = CountMover(self, self.moveTable, False)
		self.laser = None
		self.guns = []
		self.appendGun(BattleShip1Gun(self, 149, 11, True, self.isRed, 60))
		self.appendGun(BattleShip1Gun(self, 186, 7, True, self.isRed, 90))
		self.appendGun(BattleShip1Gun(self, 223, 3, True, self.isRed, 120))
		self.appendGun(BattleShip1Gun(self, 366, 1, True, self.isRed, 60))
		self.appendGun(BattleShip1Gun(self, 150, 79, False, self.isRed, 60))
		self.appendGun(BattleShip1Gun(self, 388, 82, False, self.isRed, 60))
		self.bridge = gcommon.ObjMgr.addObj(BattleShip1Bridge(self.x +272, self.y -48, self.isRed))

	def appendGun(self, obj):
		self.guns.append(obj)
		gcommon.ObjMgr.addObj(obj)

	def update(self):
		self.bridge.x = self.x +272
		self.bridge.y = self.y -48
		# 移動はCountMoverクラス
		self.mover.update()
		if self.state == 0:
			if self.cnt2 == self.fighterTime:
				self.nextState()
		elif self.state == 1:
			# 戦闘機射出
			if self.cnt % 15 == 0:
				gcommon.ObjMgr.addObj(Fighter3([0, None, self.x +288, self.y +80,
					[
						[1, 1, gcommon.C_LAYER_GRD],
						[30, 0, -1.0, 2.0],[30, 0, -3.0, 0.5],[600, 0, -3.0,0.0]
					], 30]))
			if self.cnt > 60:
				self.nextState()
		if self.cnt2 == self.laserTime:
			self.laser = BattleShip1Laser(self.x, self.y +41)
			gcommon.ObjMgr.addObj(self.laser)
		if self.laser != None:
			self.laser.x = self.x
			self.laser.y = self.y +41
		if self.x <= -512:
			if self.laser != None and self.laser.removeFlag == False:
				self.laser.remove()
				self.laser = None
			self.remove()
		self.cnt2 += 1
	
	def draw(self):
		if self.isRed:
			pyxel.pal(4,2)
			pyxel.pal(9,8)
			pyxel.pal(10,14)
		# 前半分
		pyxel.blt(self.x, self.y, 2, 0, 0, 256, 104, 3)
		# 後半分
		pyxel.blt(self.x +256, self.y, 2, 0, 104, 256, 104, 3)
		if self.isRed:
			pyxel.pal()

class BattleShip1Bridge(EnemyBase):
	def __init__(self, x, y, isRed):
		super(BattleShip1Bridge, self).__init__()
		self.x = x
		self.y = y
		self.isRed = isRed
		self.collisionRects = gcommon.Rect.createFromList(
			[[24,17,50,34],[16,35,53,47]])
		self.hp = 300
		self.score = 2000
		self.layer = gcommon.C_LAYER_SKY
		if self.isRed:
			self.hitcolor1 = 8
			self.hitcolor2 = 14
		else:
			self.hitcolor1 = 9
			self.hitcolor2 = 10
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
	def update(self):
		if self.x <= -64:
			self.remove()
			return

	def draw(self):
		# 艦橋
		# if self.isRed:
		# 	pyxel.pal(4,2)
		# 	pyxel.pal(9,8)
		# 	pyxel.pal(10,14)
		if self.state == 100:
			if self.isRed:
				pyxel.pal(4,2)
				pyxel.pal(9,8)
				pyxel.pal(10,14)
			pyxel.blt(self.x, self.y +24, 2, 192, 232, 64, 24, 3)
			if self.isRed:
				pyxel.pal()
		else:
			if self.isRed:
				pyxel.blt(self.x, self.y, 2, 64, 208, 64, 48, 3)
			else:
				pyxel.blt(self.x, self.y, 2, 0, 208, 64, 48, 3)
		# if self.isRed:
		# 	pyxel.pal()

	# 破壊されたとき
	def broken(self):
		self.state = 100
		gcommon.GameSession.addScore(self.score)
		self.hitCheck = False
		self.shotHitCheck = False
		create_explosion2(self.x+36, self.y+34, gcommon.C_LAYER_EXP_SKY, gcommon.C_EXPTYPE_SKY_M, gcommon.SOUND_MID_EXP)
		# removeはしない

class BattleShip1Laser(EnemyBase):
	def __init__(self, x, y):
		super(BattleShip1Laser, self).__init__()
		self.x = x
		self.y = y
		self.layer = gcommon.C_LAYER_E_SHOT
		self.hitCheck = False
		self.shotHitCheck = False
		self.enemyShotCollision = False
		self.laserSize = 0
	def update(self):
		if self.x < 0:
			self.remove()
			return
		if self.state == 0:
			self.left = -self.x
			self.top = 0
			self.right = 0
			self.bottom = 0
			self.laserSize = 0
			self.hitCheck = False
			if self.cnt > 60:
				self.nextState()
		elif self.state == 1:
			self.laserSize += 0.25
			self.left = -self.x
			self.top = -int(self.laserSize)
			self.right = 0
			self.bottom = int(self.laserSize)
			self.hitCheck = False
			if self.cnt > 40:
				self.nextState()
		elif self.state == 2:
			self.hitCheck = True
			if self.cnt > 30:
				self.nextState()
		else:
			self.remove()		

	def draw(self):
		if self.cnt % 3 == 0:
			return
		if self.state == 0:
			clr = 1
			if self.cnt < 20:
				clr = 1
			if self.cnt < 40:
				clr = 5
			else:
				clr = 6
			pyxel.rect(self.x +self.left, self.y, self.right -self.left+1, 1, clr)
		else:
			pyxel.rect(self.x +self.left, self.y +self.top, self.right -self.left+1, self.bottom -self.top+1, 5)

# 艦砲台
class BattleShip1Gun(EnemyBase):
	def __init__(self, parentObj, offsetX, offsetY, isUpper, isRed, shotFirst):
		super(BattleShip1Gun, self).__init__()
		self.parentObj = parentObj
		self.offsetX = offsetX
		self.offsetY = offsetY
		self.isUpper = isUpper
		self.isRed = isRed
		self.shotFirst = shotFirst
		self.left = 2
		self.top = 0
		self.right = 23
		self.bottom = 7
		self.layer = gcommon.C_LAYER_SKY
		self.hp = 25
		self.hitcolor1 = 9
		self.hitcolor2 = 10
		self.ground = True
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.shotInterval = 90
		self.shotCount = 0
		self.shotTime = 0
		self.shotDr64 = 0
		self.score = 500
	
	def update(self):
		self.x = self.parentObj.x + self.offsetX
		self.y = self.parentObj.y + self.offsetY
		if self.x < -28:
			self.remove()
			return
		if self.shotFirst == self.cnt or ((self.cnt -self.shotFirst) % self.shotInterval) ==0:
			if (self.isUpper and self.y > gcommon.ObjMgr.myShip.y) or (self.isUpper == False and self.y < gcommon.ObjMgr.myShip.y):
				self.shotCount = 3
				self.shotTime = 0
				self.shotDr64 = gcommon.get_atan_no_to_ship(self.x+13, self.y+3)
		
		if self.shotCount > 0:
			if self.shotTime == 0:
				enemy_shot_dr(self.x+13,self.y+3, 3, 0, self.shotDr64)
				self.shotTime = 10
				self.shotCount -= 1
			else:
				self.shotTime -= 1

	def draw(self):
		if self.isUpper:
			sy = 208
		else:
			sy = 216
		if self.shotCount> 0 and self.cnt & 4 != 0:
			sx = 160
		else:
			sx = 128
		if self.isRed:
			pyxel.pal(4,2)
			pyxel.pal(9,8)
			pyxel.pal(10,14)
		pyxel.blt(self.x, self.y, 2, sx, sy, 26, 7, 3)
		if self.isRed:
			pyxel.pal()


class Fighter3(EnemyBase):
	def __init__(self, t):
		super(Fighter3, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.moveTable = t[4]
		self.shotFirst = t[5]
		self.left = 4
		self.top = 7
		self.right = 19
		self.bottom = 15
		self.layer = gcommon.C_LAYER_SKY
		self.hp = 1
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.mover = CountMover(self, self.moveTable, False)
		self.score = 30

	def update(self):
		self.mover.update()
		if self.cnt == self.shotFirst:
			enemy_shot(self.x +10, self.y+10, 3, 0)

	def draw(self):
		pyxel.blt(self.x, self.y, 1, 32, 200, 24, 22, 3)
		if self.cnt & 2 == 0:
			if self.cnt & 4 == 0:
				pyxel.blt(self.x +22, self.y +10-3, 1, 112, 64, 16, 6, 3)
			else:
				pyxel.blt(self.x +22, self.y +10-3, 1, 112, 72, 16, 6, 3)


