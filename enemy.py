
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

	def remove(self):
		self.removeFlag = True

	# 追加されたとき
	def appended(self):
		pass
	
	# 破壊されたとき
	def broken(self):
		layer = gcommon.C_LAYER_EXP_SKY
		if self.layer == gcommon.C_LAYER_GRD:
			layer = gcommon.C_LAYER_EXP_GRD
		
		gcommon.score += self.score
		
		create_explosion(self.x+(self.right-self.left+1)/2, self.y+(self.bottom-self.top+1)/2, layer, self.exptype)
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
					pyxel.blt( self.x-24, self.y-24, 0, 208, 208,
						24*2 -(self.cnt &2) * 48,
						24*2 -(self.cnt &4) * 24,
						gcommon.C_COLOR_KEY)
			else:
				if self.cnt%2 ==0:
					pyxel.pal(7, gcommon.TP_COLOR)
					pyxel.blt( self.x-24, self.y-24, 0, 208, 208,
						24*2 -(self.cnt &2) * 48,
						24*2 -(self.cnt &4) * 24,
						gcommon.C_COLOR_KEY)
					pyxel.pal()
		else:
			if self.cnt<8:
				pyxel.circ(self.x, self.y, self.cnt*2+1, 10)
			elif self.cnt < 25:
				if self.cnt%2 ==0:
					pyxel.blt( self.x-36, self.y-36, 0, 184, 88,
						72 -(self.cnt &2) * 72,
						72 -(self.cnt &4) * 36,
						gcommon.C_COLOR_KEY)
			else:
				if self.cnt%2 ==0:
					pyxel.pal(7, gcommon.TP_COLOR)
					pyxel.blt( self.x-36, self.y-36, 0, 184, 88,
						72 -(self.cnt &2) * 72,
						72 -(self.cnt &4) * 36,
						gcommon.C_COLOR_KEY)
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

	def update(self):
		if self.cnt % 120==0:
			enemy_shot(self.x+8,self.y+6, 2, 0)

	def draw(self):
		dr8 = gcommon.get_direction_my(self.x+8, self.y +8)
		y = int(self.y+0.5)
		if self.mirror == 0:
			if dr8 == 0:
				pyxel.blt(self.x, y, 1, 0, 96, -16, 16, gcommon.TP_COLOR)
			elif dr8 == 1:
				pyxel.blt(self.x, y, 1, 0, 96, -16, 16, gcommon.TP_COLOR)
			elif dr8 == 2:
				pyxel.blt(self.x, y, 1, 32, 96, 16, 16, gcommon.TP_COLOR)
			elif dr8 == 3:
				pyxel.blt(self.x, y, 1, 0, 96, 16, 16, gcommon.TP_COLOR)
			elif dr8 == 4:
				pyxel.blt(self.x, y, 1, 0, 96, 16, 16, gcommon.TP_COLOR)
			elif dr8 == 5:
				pyxel.blt(self.x, y, 1, 16, 96, 16, 16, gcommon.TP_COLOR)
			elif dr8 == 6:
				pyxel.blt(self.x, y, 1, 32, 96, 16, 16, gcommon.TP_COLOR)
			elif dr8 == 7:
				pyxel.blt(self.x, y, 1, 16, 96, -16, 16, gcommon.TP_COLOR)
		else:
			if dr8 == 0:
				pyxel.blt(self.x, y, 1, 0, 96, -16, -16, gcommon.TP_COLOR)
			elif dr8 == 1:
				pyxel.blt(self.x, y, 1, 16, 96, -16, -16, gcommon.TP_COLOR)
			elif dr8 == 2:
				pyxel.blt(self.x, y, 1, 32, 96, 16, -16, gcommon.TP_COLOR)
			elif dr8 == 3:
				pyxel.blt(self.x, y, 1, 16, 96, 16, -16, gcommon.TP_COLOR)
			elif dr8 == 4:
				pyxel.blt(self.x, y, 1, 0, 96, 16, -16, gcommon.TP_COLOR)
			elif dr8 == 5:
				pyxel.blt(self.x, y, 1, 0, 96, 16, -16, gcommon.TP_COLOR)
			elif dr8 == 6:
				pyxel.blt(self.x, y, 1, 32, 96, 16, -16, gcommon.TP_COLOR)
			elif dr8 == 7:
				pyxel.blt(self.x, y, 1, 16, 96, -16, -16, gcommon.TP_COLOR)



class StageClearText(EnemyBase):
	def __init__(self, stage):
		super(StageClearText, self).__init__()
		self.t = gcommon.T_STAGE_START
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


class Splash(EnemyBase):
	def __init__(self, x, y, layer):
		super(Splash, self).__init__()
		self.t = gcommon.T_SKY_EXP
		self.x = x
		self.y = y
		self.layer = layer
		self.offset = random.random()

	def update(self):
		self.cnt += 1
		if self.cnt > 100:
			self.removeFlag = True

	def draw(self):
		gcommon.draw_splash2(self, self.offset)


	def draw(self):
		d = ((self.dr + 2) & 63)>>2
		if d >= 8:
			pyxel.blt(self.x, self.y, 2, (d -8) * 24, 16+24, 24, 24, gcommon.TP_COLOR)
		else:
			pyxel.blt(self.x, self.y, 2, d * 24, 16, 24, 24, gcommon.TP_COLOR)




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
		for i in range(0,200):
			r = random.random() * 2 * 3.141592653
			speed = random.random() * 6
			s = SplashItem(cx, cy, speed * math.cos(r), speed * math.sin(r), random.randrange(50, 200))
			self.tbl.append(s)

	@classmethod
	def append(cls, x, y, layer):
		gcommon.ObjMgr.objs.append(Splash(x, y, layer))
	
	def update(self):
		for s in self.tbl:
			s.x += s.dx
			s.y += s.dy
			s.dx *= 0.97
			s.dy *= 0.97
	
	def draw(self):
		newTbl = []
		for s in self.tbl:
			s.cnt -= 1
			if s.cnt != 0:
				newTbl.append(s)
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
		self.tbl = newTbl


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
		pass
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
		self.hp = 15
		#self.layer = gcommon.C_LAYER_UNDER_GRD
		self.layer = gcommon.C_LAYER_SKY
		self.score = 100

	def update(self):
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


class Worm1(EnemyBase):
	def __init__(self, t):
		super(Worm1, self).__init__()
		pos = gcommon.mapPosToScreenPos(t[2], t[3])
		self.x = pos[0]
		self.y = pos[1]
		self.downward = t[4]		# 0:上向き  1:下向き
		self.left = 2
		self.top = 2
		self.right = 21
		self.bottom = 15
		self.hp = 40
		#self.layer = gcommon.C_LAYER_UNDER_GRD
		self.layer = gcommon.C_LAYER_GRD
		self.score = 100
		self.dr = 48
		self.cells = []
		for i in range(0,6):
			self.cells.append([0,0])

	def update(self):
		if self.state == 0:
			# 待機状態
			if gcommon.get_distance_my(self.x + 12, self.y) < 100:
				print("get_distance")
				self.nextState()
		elif self.state == 1:
			# 触手伸ばす
			x = 0
			y = 0
			r = 0
			for pos in self.cells:
				pos[0] = x + math.cos(gcommon.atan_table[(self.dr + r) & 63]) * 12 * (self.cnt) /30.0
				pos[1] = y + math.sin(gcommon.atan_table[(self.dr + r) & 63]) * 12 * (self.cnt) /30.0
				x = pos[0]
				y = pos[1]
				r += 1
			if self.cnt == 30:
				self.nextState()
		
	def draw(self):
		size = len(self.cells)
		i = 0
		while(i<size):
			pos = self.cells[size -1 -i]
			pyxel.blt(self.x + 4 + pos[0], self.y + pos[1], 1, 48, 168, 16, 16, 3)
			i += 1
		pyxel.blt(self.x, self.y, 1, 64, 168, 24, 16, 3)
