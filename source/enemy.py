
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

def enemy_shot_dr(x, y, speed, shotType, dr):
	gcommon.ObjMgr.objs.append(EnemyShot.createSpecifiedDirection(x, y, speed, shotType, dr))

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
		self.hp = 0
		self.state = 0
		self.cnt = 0
		self.hit = False
		self.layer = 0
		self.score = 0
		self.hitcolor1 = 0
		self.hitcolor2 = 0
		self.exptype = gcommon.C_EXPTYPE_SKY_S
		self.expsound = -1
		self.score = 0
		self.shotHitCheck = True	# 自機弾との当たり判定
		self.hitCheck = True	# 自機と敵との当たり判定
		self.removeFlag = False

	def nextState(self):
		self.state += 1
		self.cnt = 0

	def setState(self, state):
		self.state = state
		self.cnt = 0

	# 自機弾と敵との当たり判定と破壊処理
	def checkShotCollision(self, shot):
		if shot.removeFlag == False and gcommon.check_collision(self, shot):
			self.hp -= gcommon.SHOT_POWER
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
			return False

	def remove(self):
		self.removeFlag = True

	# 追加されたとき
	def appended(self):
		pass
	
	# 破壊されたとき
	def broken(self):
		layer = gcommon.C_LAYER_EXP_SKY
		#if self.layer == gcommon.C_LAYER_GRD:
		#	layer = gcommon.C_LAYER_EXP_GRD
		
		gcommon.score += self.score
		
		create_explosion2(self.x+(self.right-self.left+1)/2, self.y+(self.bottom-self.top+1)/2, layer, self.exptype, self.expsound)
		self.removeFlag = True


# 爆発生成
# cx,cy center
# exlayer explosion layer
def create_explosion(cx, cy, exlayer, exptype):
	if exptype==gcommon.C_EXPTYPE_SKY_S or exptype==gcommon.C_EXPTYPE_GRD_S:
		#pyxel.play(1, 2)
		gcommon.sound(gcommon.SOUND_SMALL_EXP)
	else:
		#pyxel.play(1, 1)
		gcommon.sound(gcommon.SOUND_MID_EXP)
	#add(objs,explosion:new(cx,cy,exlayer,exptype))
	gcommon.ObjMgr.objs.append(Explosion(cx,cy,exlayer,exptype))

def create_explosion2(cx, cy, exlayer, exptype, expsound):
	if expsound != -1:
		gcommon.sound(expsound)
	else:
		if exptype==gcommon.C_EXPTYPE_SKY_S or exptype==gcommon.C_EXPTYPE_GRD_S:
			gcommon.sound(gcommon.SOUND_SMALL_EXP)
		else:
			gcommon.sound(gcommon.SOUND_MID_EXP)
	#add(objs,explosion:new(cx,cy,exlayer,exptype))
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
		else:
			self.x = x -6
			self.y = y -6
		self.speed = speed
		self.type = gcommon.T_E_SHOT1
		self.layer = gcommon.C_LAYER_E_SHOT
		if shotType==0:
			self.left = 2
			self.top = 2
			self.right = 5
			self.bottom = 5
		else:
			self.left = 2
			self.top = 2
			self.right = 9
			self.bottom = 9

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
		else:
			pyxel.blt(self.x, self.y, 0, 18, 18, 12, 12, gcommon.TP_COLOR)



#
# 爆発
# 
class Explosion(EnemyBase):
	def __init__(self, cx,cy,exlayer,exptype):
		super(Explosion, self).__init__()
		self.t = gcommon.T_SKY_EXP
		self.x = cx
		self.y = cy
		self.layer = exlayer
		self.exptype = exptype
		self.size = 0
		self.hitCheck = False
		self.shotHitCheck = False
		if exptype == gcommon.C_EXPTYPE_SKY_S or exptype==gcommon.C_EXPTYPE_GRD_S:
			self.size = 1
		elif exptype == gcommon.C_EXPTYPE_SKY_M or exptype==gcommon.C_EXPTYPE_GRD_M:
			self.size = 2
		else:
			self.size = 3

	def update(self):
		if self.size==1:
			if self.cnt > 4*self.size:
				self.removeFlag = True
		elif self.size == 2:
			if self.cnt>30:
				self.remove()
		else:
			if self.cnt>40:
				self.remove()
		
	
	def draw(self):
		if self.size==1:
			pyxel.circb(self.x, self.y, self.cnt*2+1, 10)
		elif self.size==2:
			if self.cnt<8:
				pyxel.circ(self.x, self.y, self.cnt*2+1, 10)
			elif self.cnt < 25:
				if self.cnt%2 ==0:
					pyxel.blt( self.x-24, self.y-24, 0, 0, 64,
						24*2 -(self.cnt &2) * 48,
						24*2 -(self.cnt &4) * 24,
						gcommon.TP_COLOR)
			else:
				if self.cnt%2 ==0:
					pyxel.pal(7, gcommon.TP_COLOR)
					pyxel.blt( self.x-24, self.y-24, 0, 0, 64,
						24*2 -(self.cnt &2) * 48,
						24*2 -(self.cnt &4) * 24,
						gcommon.TP_COLOR)
					pyxel.pal()
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
		self.dy = 0.0

	def update(self):
		self.x = self.x + self.dx
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
		self.score = 300
		self.hitcolor1 = 5
		self.hitcolor2 = 6
		self.exptype = gcommon.C_EXPTYPE_GRD_S
		self.interval = 120
		self.first = 120
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
		t = gcommon.T_STAGE_START
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
		self.hitCheck = False
		self.shotHitCheck = False
		for i in range(0,200):
			r = random.random() * 2 * math.pi
			speed = random.random() * 6
			s = SplashItem(cx, cy, speed * math.cos(r), speed * math.sin(r), random.randrange(100, 240))
			self.tbl.append(s)

	@classmethod
	def append(cls, x, y, layer):
		gcommon.ObjMgr.objs.append(Splash(x, y, layer))
	
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


class Fan1Group(EnemyBase):
	def __init__(self, t):
		super(Fan1Group, self).__init__()
		self.y = t[2]
		self.interval = t[3]
		self.max = t[4]
		self.cnt2 = 0
		self.hitCheck = False

	def update(self):
		if self.cnt % self.interval == 0:
			gcommon.ObjMgr.addObj(Fan1([0, 0, 256, self.y]))
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
		self.left = 2
		self.top = 2
		self.right = 14
		self.bottom = 14
		self.hp = 1
		self.dx = 0
		self.dy = 0
		self.time1 = 30
		self.layer = gcommon.C_LAYER_SKY
		self.score = 10
	
	def update(self):
		self.x -= 3
		if self.time1 < self.cnt:
			if gcommon.ObjMgr.myShip.y < self.y +2:
				self.y -= 1.5
			elif gcommon.ObjMgr.myShip.y > self.y -2:
				self.y += 1.5

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
		
		
	def draw(self):
		pyxel.blt(self.x, self.y, 1, 48, 64, 32, 7, gcommon.TP_COLOR)
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

	def update(self):
		if self.cnt > 900:
			self.remove()
		else:
			if self.cnt & 32 == 0:
				dr = gcommon.get_direction_my(self.x +8, self.y +8)
				self.x += gcommon.direction_map[dr][0] * 1.25
				self.y -= gcommon.direction_map[dr][1] * 1.25
			if self.cnt & 127 == 127:
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
				gcommon.ObjMgr.addObj(Cell1([0,0, self.startX, self.startY]))
			elif self.cnt == 20:
				gcommon.ObjMgr.addObj(Cell1([0,0, self.startX, self.startY + 50]))
			elif self.cnt == 40:
				gcommon.ObjMgr.addObj(Cell1([0,0, self.startX, self.startY + 20]))
			elif self.cnt == 60:
				gcommon.ObjMgr.addObj(Cell1([0,0, self.startX, self.startY + 70]))
			elif self.cnt == 80:
				gcommon.ObjMgr.addObj(Cell1([0,0, self.startX, self.startY + 30]))
				self.remove()
		else:
			if self.cnt == 0:
				gcommon.ObjMgr.addObj(Cell1([0,0, self.startX, self.startY]))
			elif self.cnt == 20:
				gcommon.ObjMgr.addObj(Cell1([0,0, self.startX +50, self.startY]))
			elif self.cnt == 40:
				gcommon.ObjMgr.addObj(Cell1([0,0, self.startX +20, self.startY]))
			elif self.cnt == 60:
				gcommon.ObjMgr.addObj(Cell1([0,0, self.startX +70, self.startY]))
			elif self.cnt == 80:
				gcommon.ObjMgr.addObj(Cell1([0,0, self.startX +30, self.startY]))
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
		self.score = 100
		self.dr = 48
		self.offsetX = 4
		self.offsetY = 0
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
			#if gcommon.get_distance_my(self.x + 12, self.y) < 100:
			#	print("get_distance")
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
			if self.cnt & 31 == 31:
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
			if self.cnt & 31 == 31:
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
			self.hp -= gcommon.SHOT_POWER
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
		gcommon.score += self.score
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
		self.hitCheck = False
		self.shotHitCheck = False
		gcommon.ObjMgr.myShip.setSubScene(5)

	def update(self):
		if self.cnt > 60:
			self.remove()
			gcommon.app.startNextStage()

	def draw(self):
		pass

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
		self.hp = 999999
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.hitCheck = True
		self.shotHitCheck = True

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

# 遺跡基本クラス
class RuinBase(EnemyBase):
	def __init__(self, mx, my, direction, mWidth, mHeight, needDummyBlock):
		super(RuinBase, self).__init__()
		pos = gcommon.mapPosToScreenPos(mx, my)
		self.x = pos[0]		# screen x
		self.y = pos[1]		# screen y
		self.direction = direction
		self.mWidth = mWidth	# 幅（8ドット単位）
		self.mHeight = mHeight	# 高さ（8ドット単位）
		self.left = 0
		self.right = self.mWidth * 8 -1
		self.top = 0
		self.bottom = self.mHeight * 8 -1
		self.hp = 999999
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.hitCheck = True
		self.shotHitCheck = True
		self.needDummyBlock = needDummyBlock
		if needDummyBlock:
			gcommon.setMapDataByMapPos2(mx, my, gcommon.DUMMY_BLOCK_NO, mWidth, mHeight)
		else:
			gcommon.setMapDataByMapPos2(mx, my, 0, mWidth, mHeight)

	def update(self):
		if self.x + self.right < 0:
			self.remove()
			return
		exist = False
		for i in range(self.mWidth):
			check = False
			if self.direction == 1:
				check = gcommon.isMapFreePos(self.x + i*8, self.y +self.mHeight * 8)
			else:
				pos = gcommon.screenPosToMapPos(self.x + i*8, self.y -1)
				check = gcommon.isMapFreeByMapPos(pos[0], pos[1])
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
			if self.y > 192 or self.y + self.bottom < 0:
				self.remove()

	# 破壊されたとき
	def broken(self):
		super(RuinBase, self).broken()
		mpos = gcommon.screenPosToMapPos(self.x, self.y)
		gcommon.setMapDataByMapPos2(mpos[0], mpos[1], 0, self.mWidth, self.mHeight)


# 遺跡柱
class RuinPillar1(RuinBase):
	def __init__(self, mx, my, direction, size):
		super(RuinPillar1, self).__init__(mx, my, direction, 2, size, True)
		self.size = size	# 高さ（8ドット単位） 2 - 6
		self.hp = 30
		self.bx = (self.size -2) * 2

	def draw(self):
		pyxel.bltm(int(self.x), self.y, 0, self.bx, 0, 2, self.size * 8, gcommon.TP_COLOR)
		#pyxel.rectb(self.x +self.left, self.y + self.top, self.right -self.left+1, self.bottom -self.top+1, 7)


# 遺跡床
class RuinFloor1(RuinBase):
	def __init__(self, mx, my, direction, size):
		super(RuinFloor1, self).__init__(mx, my, direction, size*2, 2, True)
		self.size = size
		self.left = 0
		self.top = 4
		self.right = self.mWidth * 8
		self.bottom = self.mHeight * 8 -5
		self.by = (self.size -2) * 2

	def draw(self):
		pyxel.bltm(self.x, self.y, 0, 10, self.by, self.size *2, 2, gcommon.TP_COLOR)
		#pyxel.rectb(self.x +self.left, self.y + self.top, self.right -self.left+1, self.bottom -self.top+1, 7)

# 遺跡と落ちる砲台
class Battery2(RuinBase):
	def __init__(self, mx, my, direction):
		# direction  1:通常 -1:上下逆
		super(Battery2, self).__init__(mx, my, direction, 2, 2, False)
		self.left = 2
		self.right = 13
		if self.direction == 1:
			self.top = 5
			self.bottom = 15
		else:
			self.top = 0
			self.bottom = 10
		self.hp = 10

	def update(self):
		super(Battery2, self).update()
		if self.cnt & 63 == 63:
			enemy_shot(self.x+8,self.y+6, 2, 0)

	def draw(self):
		if self.direction == 1:
			drawBattery1(self.x, self.y, 0)
		else:
			drawBattery1(self.x, self.y, 1)


class Particle1(EnemyBase):
	def __init__(self, cx, cy, rad):
		super(Particle1, self).__init__()
		self.x = cx
		self.y = cy
		self.rad = rad
		self.tbl = []
		self.hitCheck = False
		self.shotHitCheck = False
		for i in range(0, 8):
			r = rad + random.random() * math.pi/4 - math.pi/8
			speed = random.random() * 6
			s = SplashItem(cx, cy, speed * math.cos(r), speed * math.sin(r), random.randrange(10, 50))
			self.tbl.append(s)

	@classmethod
	def append(cls, x, y, rad):
		gcommon.ObjMgr.objs.append(Particle1(x, y, rad))

	@classmethod
	def appendPos(cls, pos, rad):
		gcommon.ObjMgr.objs.append(Particle1(pos[0], pos[1], rad))

	@classmethod
	def appendCenter(cls, obj, rad):
		pos = gcommon.getCenterPos(obj)
		gcommon.ObjMgr.objs.append(Particle1(pos[0], pos[1], rad))

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
