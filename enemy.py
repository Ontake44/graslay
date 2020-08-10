
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
		self.hitCheck = True
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
			self.left = 6
			self.top = 6
			self.right = 9
			self.bottom = 9
		else:
			self.left = 4
			self.top = 4
			self.right = 11
			self.bottom = 11

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
		if self.x <-16 or self.x >= 256 or self.y<-16 or self.y >=256:
			self.removeFlag = True

	def draw(self):
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
		





class Tank1(EnemyBase):
	def __init__(self, t):
		super(Tank1, self).__init__()
		self.t = gcommon.T_TANK1
		self.x = t[2]
		self.y = t[3]
		self.direction = t[4]
		self.first = t[5]
		self.interval = t[6]
		self.stop_time = t[7]
		self.left = 2
		self.top = 2
		self.right = 29
		self.bottom = 29
		self.hp = 50
		self.layer = gcommon.C_LAYER_GRD
		self.score = 30
		self.hitcolor1 = 5
		self.hitcolor2 = 6
		self.exptype = gcommon.C_EXPTYPE_GRD_M

	def update(self):
		self.x += gcommon.direction_map[self.direction][0] * 0.2
		if self.stop_time > 0:
			self.y += gcommon.direction_map[self.direction][1] * 0.2
		
		if gcommon.is_outof_bound(self):
			self.removeFlag = True
		else:
			if self.cnt == self.first:
				enemy_shot(self.x +16, self.y+16, 2, 0)
				self.first = -1
				self.cnt =0
			elif self.cnt == self.interval:
				enemy_shot(self.x +16, self.y+16, 2, 0)
				self.cnt = 0
			
			self.stop_time -=1

	def draw(self):
		pyxel.blt(self.x, self.y, 1, tank1_spmap[self.direction], 0, 32, 32, gcommon.TP_COLOR)


class MidTank1(EnemyBase):
	def __init__(self, t):
		super(MidTank1, self).__init__()
		self.t = gcommon.T_MID_TANK1
		self.x = t[2]
		self.y = t[3]
		self.first = t[4]
		self.interval = t[5]
		self.move_first = t[6]
		self.direction = t[7]
		self.move_interval = t[8]
		self.move_cnt = 0
		self.left = 2
		self.top = 4
		self.right = 42
		self.bottom = 26
		self.hp = 80
		self.layer = gcommon.C_LAYER_GRD
		self.score = 50
		self.hitcolor1 = 5
		self.hitcolor2 = 6
		self.exptype = gcommon.C_EXPTYPE_GRD_M
		if self.direction==0:
			# right
			self.left = 1
			self.top = 2
			self.rgith = 42
			self.bottom = 26
		elif self.direction==6:
			# lower
			self.left = 4
			self.top = 2
			self.right = 26
			self.bottom = 42
		self.speed = 0.1*2

	def update(self):
		if self.cnt >= self.move_first:
			c = int(self.cnt/self.move_interval)
			if c % 2 == 0:
				self.x += gcommon.direction_map[self.direction][0] * self.speed *2
				self.y -= gcommon.direction_map[self.direction][1] * self.speed *2
				self.move_cnt+=1
		if gcommon.is_outof_bound(self):
			self.removeFlag = True
		else:
			# mid tank1 shot
			ox = 0
			oy = 0
			ox2 = 0
			oy2 = 0
			ox3 = 0
			oy3 = 0
			if self.direction==0 or self.direction==4:
				ox = 8
				oy = 16
				dx = 6*2
				dy = 0
			elif self.direction==6:
				ox = 16
				oy = 8
				dx = 0
				dy = 6*2
			
			ox2=ox+dx
			oy2=oy+dy
			ox3=ox+dx+dx
			oy3=oy+dy+dy
			if self.cnt == self.first:
				enemy_shot(self.x+ox, self.y+oy, 2, 0)
			elif self.cnt == self.first+20:
				enemy_shot(self.x+ox2, self.y+oy2, 2, 0)
			elif self.cnt == self.first+40:
				enemy_shot(self.x+ox3, self.y+oy3, 2, 0)
			elif self.cnt>self.first+40:
				c=self.cnt-self.first
				if c % self.interval==0:
					enemy_shot(self.x+ox, self.y+oy, 2, 0)
				elif c % self.interval==20:
					enemy_shot(self.x+ox2, self.y+oy2, 2, 0)
				elif c % self.interval==40:
					enemy_shot(self.x+ox3, self.y+oy3, 2, 0)

	def draw(self):
		if self.direction==0:		# Right
			if self.move_cnt & 4 == 0:
				# sspr(0,64,24,20,self.x,self.y)
				pyxel.blt(self.x, self.y, 1, 0, 128, 48, 40, gcommon.TP_COLOR)
			else:
				pyxel.blt(self.x, self.y, 1, 48, 128, 48, 40, gcommon.TP_COLOR)
		elif self.direction==4:		# Left
			if self.move_cnt & 4 == 0:
				# sspr(24,64,24,20,self.x,self.y)
				pyxel.blt(self.x, self.y, 1, 96, 128, 48, 40, gcommon.TP_COLOR)
			else:
				pyxel.blt(self.x, self.y, 1, 144, 128, 48, 40, gcommon.TP_COLOR)
		elif self.direction==6:		# Lower
			if self.move_cnt & 4 == 0:
				pyxel.blt(self.x, self.y, 1, 176, 16, 40, 48, gcommon.TP_COLOR)
			else:
				pyxel.blt(self.x, self.y, 1, 216, 16, 40, 48, gcommon.TP_COLOR)


class Fighter1(EnemyBase):
	def __init__(self, t):
		super(Fighter1, self).__init__()
		self.t = gcommon.T_FIGHTER1
		self.x = t[2]
		self.y = t[3]
		self.first = t[4]
		self.interval = t[5]
		self.speedup = t[6]
		self.left = 4
		self.top = 2
		self.right = 44
		self.bottom = 30
		self.hp = 40
		self.layer = gcommon.C_LAYER_SKY
		self.score = 50
		self.hitcolor1 = 5
		self.hitcolor2 = 6
		self.exptype = gcommon.C_EXPTYPE_SKY_M
		self.imageIndex = 1
		self.imageX = 0
		self.imageY = 32

	def update(self):
		self.y += 0.8
		if self.cnt >= self.speedup:
			self.y += 1.2
		if gcommon.is_outof_bound(self):
			self.removeFlag = True
		else:
			if self.cnt == self.first:
				enemy_shot(self.x+22,self.y+30,2,0)
				enemy_shot_offset(self.x+10,self.y+18,2,0,-1)
				enemy_shot_offset(self.x+38,self.y+18,2,0,1)
			else:
				c = self.cnt-self.first
				if c % self.interval==0:
					enemy_shot(self.x+22,self.y+30,2,0)
					enemy_shot_offset(self.x+10,self.y+18,2,0,-1)
					enemy_shot_offset(self.x+38,self.y+18,2,0,1)

	def draw(self):
		if gcommon.set_color_shadow():
			pyxel.blt(self.x+16, self.y+16, self.imageIndex, self.imageX, self.imageY, 48, 32, gcommon.TP_COLOR)
			pyxel.pal()
		pyxel.blt(self.x, self.y, self.imageIndex, self.imageX, self.imageY, 48, 32, gcommon.TP_COLOR)
		if self.cnt & 1 == 0:
			if self.cnt >= self.speedup:
				#spr(14,o.x+2,o.y-6)
				#spr(14,o.x+17,o.y-6)
				pyxel.blt(self.x+4, self.y-12, self.imageIndex, self.imageX+48, self.imageY, 10, 16, gcommon.TP_COLOR)
				pyxel.blt(self.x+34, self.y-12, self.imageIndex, self.imageX+48, self.imageY, 10, 16, gcommon.TP_COLOR)
			else:
				#spr(15,o.x+2,o.y-6)
				#spr(15,o.x+17,o.y-6)
				pyxel.blt(self.x+4, self.y-12, self.imageIndex, self.imageX+48, self.imageY+16, 10, 16, gcommon.TP_COLOR)
				pyxel.blt(self.x+34, self.y-12, self.imageIndex, self.imageX+48, self.imageY+16, 10, 16, gcommon.TP_COLOR)


class Fighter1B(Fighter1):
	def __init__(self, t):
		super(Fighter1B, self).__init__(t)
		self.imageIndex = 2
		self.imageX = 192
		self.imageY = 16



#
# 砲台
class Battery1(EnemyBase):
	def __init__(self, t):
		super(Battery1, self).__init__()
		self.t = gcommon.T_BATTERY1
		self.x = t[2]
		self.y = t[3]
		self.hidetime = t[4]
		self.left = 0
		self.top = 0
		self.right = 15
		self.bottom = 15
		self.hp = 50
		self.layer = gcommon.C_LAYER_HIDE_GRD
		self.score = 300
		self.hitcolor1 = 5
		self.hitcolor2 = 6
		self.exptype = gcommon.C_EXPTYPE_GRD_S

	@classmethod
	def create(cls, x, y, hidetime):
		tbl = [0, gcommon.T_BATTERY1, x, y, hidetime]
		return Battery1(tbl)

	def update(self):
		if self.state==0:
			if self.cnt==self.hidetime:
				self.state=1
				self.cnt=0
		elif self.state==1:
			if self.cnt==30:
				self.state=2
				self.cnt=0
				self.layer=gcommon.C_LAYER_GRD
		else:
			if self.cnt % 60==0:
				enemy_shot(self.x+8,self.y+6, 2, 0)

	def draw(self):
		if self.state==1:
			if self.cnt<=15:
				#spr(205,self.x,self.y)
				pyxel.blt(self.x, self.y, 1, 208, 192, 16, 16)
			else:
				#spr(206,self.x,self.y)
				pyxel.blt(self.x, self.y, 1, 224, 192, 16, 16)
			
		elif self.state==2:
			#spr(207,self.x,self.y)
			pyxel.blt(self.x, self.y, 1, 240, 192, 16, 16)


class Tank2(EnemyBase):
	def __init__(self, t):
		super(Tank2, self).__init__()
		self.t = gcommon.T_TANK2
		self.x = t[2]*2
		self.y = t[3]*2
		self.first = t[4]
		self.interval = t[5]
		self.move_tbl = t[6]		# index 0:timer 1:direction ただし、ひとつずれている。0は停止
		self.left = 2
		self.top = 2
		self.right = 29
		self.bottom = 29
		self.hp = 40
		self.layer = gcommon.C_LAYER_GRD
		self.score = 30
		self.hitcolor1 = 5
		self.hitcolor2 = 6
		self.exptype = gcommon.C_EXPTYPE_GRD_M
		self.tbl_idx = 0
		self.timer = 0

	def update(self):
		if len(self.move_tbl)>self.tbl_idx:
			t = self.move_tbl[self.tbl_idx]
			if t[1]==0:
				# no move
				pass
			else:
				self.x += gcommon.direction_map[t[1]-1][0] *0.5*2
				self.y += gcommon.direction_map[t[1]-1][1] *0.5*2
			
			if self.timer>=t[0]:
				self.tbl_idx+=1
			
		
		if gcommon.is_outof_bound(self):
			self.removeFlag = True
		else:
			if self.cnt == self.first:
				enemy_shot(self.x+14,self.y+14,2,0)
				self.first = -1
				self.cnt =0
			elif self.cnt == self.interval:
				enemy_shot(self.x+14,self.y+14,2,0)
				self.cnt =0
			
		
		self.timer+=1

	def draw(self):
		pyxel.blt(self.x, self.y, 1, 96, 32, 32, 32, gcommon.TP_COLOR)

class Wall1(EnemyBase):
	def __init__(self, t):
		super(Wall1, self).__init__()
		self.t = gcommon.T_WALL1
		self.x = t[2]*2
		self.y = t[3]*2
		self.pos = t[4]
		self.left = 0
		self.top = 0
		self.right = 0
		self.bottom = 0
		self.layer = gcommon.C_LAYER_UPPER_GRD

	def update(self):
		if self.y>=256:
			self.removeFlag = True

	def draw(self):
		n = self.pos
		ox = n * 16
		#spr(112+n,self.x+n*16,self.y)
		pyxel.blt(self.x+n*16*2, self.y, 1, 0+ox, 112, 16, 16, gcommon.TP_COLOR) 
		
		#spr(100+n,self.x+n*16,self.y+8)
		pyxel.blt(self.x+n*16*2, self.y+8*2, 1, 64+ox, 96, 16, 16, gcommon.TP_COLOR) 
		
		#spr(112+n,self.x+8,self.y+8)
		pyxel.blt(self.x+8*2, self.y+8*2, 1, 0+ox, 112, 16, 16, gcommon.TP_COLOR)

		#spr(84+n,self.x+n*16,self.y+16)
		pyxel.blt(self.x+n*16*2, self.y+16*2, 1, 64+ox, 80, 16, 16, gcommon.TP_COLOR)
	
		#spr(100+n,self.x+8,self.y+16)
		pyxel.blt(self.x+8*2, self.y+16*2, 1, 64+ox, 96, 16, 16, gcommon.TP_COLOR)
		
		#spr(112+n,self.x+16-n*16,self.y+16)
		pyxel.blt(self.x+16*2-n*16*2, self.y+16*2, 1, 0+ox, 112, 16, 16, gcommon.TP_COLOR)

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

class Fighter2(EnemyBase):
	def __init__(self, t):
		super(Fighter2, self).__init__()
		self.t = gcommon.T_FIGHTER2
		self.y = t[2]
		self.pos = t[3]			# -1:left  1:right  0:auto
		if self.pos == 0:
			if gcommon.ObjMgr.myShip.x > 120:
				self.pos = -1
				self.x = -24
			else:
				self.pos = 1
				self.x = 256
		elif self.pos < 0:
			self.x = -24
		else:
			self.x = 256
		
		self.dr = gcommon.get_atan_no_to_ship(self.x +12, self.y + 12)
		self.left = 2
		self.top = 2
		self.right = 21
		self.bottom = 21
		self.hp = 5
		self.layer = gcommon.C_LAYER_SKY
		self.score = 30
		self.hitcolor1 = 5
		self.hitcolor2 = 6
		self.exptype = gcommon.C_EXPTYPE_SKY_S

	def update(self):
		self.x += math.cos(gcommon.atan_table[self.dr & 63]) * 3
		self.y += math.sin(gcommon.atan_table[self.dr & 63]) * 3
		if self.state == 0:
			if True:
				if abs(116 - self.x) < 80 and self.cnt % 8 == 0:
					self.dr -= self.pos
					self.cnt = 0
					if abs(116 - self.x) < 50:
						self.state = 1
						self.cnt = 0
						if gcommon.get_distance_my(self.x + 12, self.y +12) > 30:
							enemy_shot(self.x+12,self.y+12,2,0)
			else:
				if abs(gcommon.ObjMgr.myShip.x - self.x) < 80 and self.cnt % 8 == 0:
					self.dr -= self.pos
					self.cnt = 0
					if abs(gcommon.ObjMgr.myShip.x - self.x) < 50:
						self.state = 1
						self.cnt = 0
						if gcommon.get_distance_my(self.x + 12, self.y +12) > 30:
							enemy_shot(self.x+12,self.y+12,2,0)
		elif self.state == 1:
			self.dr -= self.pos
			self.cnt += 1
			if self.cnt > 30:
				self.state = 3
				self.cnt = 0

	def draw(self):
		d = ((self.dr + 2) & 63)>>2
		if d >= 8:
			pyxel.blt(self.x, self.y, 2, (d -8) * 24, 16+24, 24, 24, gcommon.TP_COLOR)
		else:
			pyxel.blt(self.x, self.y, 2, d * 24, 16, 24, 24, gcommon.TP_COLOR)


class Fighter2Appear(EnemyBase):
	def __init__(self, t):
		super(Fighter2Appear, self).__init__()
		self.t = gcommon.T_FIGHTER2
		self.y = t[2]
		self.interval = t[3]
		self.fcount = t[4]
		self.pos = t[5]
		self.layer = gcommon.C_LAYER_NONE

	def update(self):
		if self.cnt % 20 == 0:
			t = [0, gcommon.T_FIGHTER2, self.y, self.pos]
			gcommon.ObjMgr.objs.append(Fighter2(t))
			self.fcount -= 1
			if self.fcount == 0:
				self.removeFlag = True

	def draw(self):
		pass

#
# 艦砲台
class Battery2(EnemyBase):
	def __init__(self, t):
		super(Battery2, self).__init__()
		self.t = gcommon.T_BATTERY2
		self.x = t[2]
		self.y = t[3]
		self.firsttime = t[4]	# 最初の開くまで
		self.hidetime = t[5]
		self.left = 0
		self.top = 0
		self.right = 15
		self.bottom = 15
		self.hp = 20
		self.layer = gcommon.C_LAYER_HIDE_GRD
		self.score = 300
		self.hitcolor1 = 5
		self.hitcolor2 = 6
		self.exptype = gcommon.C_EXPTYPE_GRD_S

	def update(self):
		if self.y > gcommon.SCREEN_MAX_Y:
			self.removeFlag = True
		else:
			if self.state==0:
				# 隠れている状態
				if self.cnt==self.firsttime:
					self.state=1
					self.cnt=0
			elif self.state==1:
				# 開く途中
				if self.cnt==15:
					self.state=2
					self.cnt=0
					self.layer=gcommon.C_LAYER_GRD
			elif self.state==2:
				# 開いている状態
				if self.cnt==60:
					self.state = 3
					self.cnt=0
					self.layer=gcommon.C_LAYER_HIDE_GRD
				if self.cnt==20 and self.y <gcommon.SCREEN_MAX_Y -16:
					enemy_shot(self.x+8,self.y+6, 2, 0)
			elif self.state==3:
				# 閉じる途中
				if self.cnt==15:
					self.state=4
					self.cnt=0
			elif self.state==4:
				# 隠れている状態
				if self.cnt==self.hidetime:
					self.state=1
					self.cnt=0

	def draw(self):
		if self.state==0 or self.state==4:
			pyxel.blt(self.x, self.y, 1, 0, 48, 16, 16)
		elif self.state==1 or self.state==3:
			pyxel.blt(self.x, self.y, 1, 16, 48, 16, 16)
		elif self.state==2:
			pyxel.blt(self.x, self.y, 1, 32, 48, 16, 16)
		elif self.state==100:
			pyxel.blt(self.x, self.y, 1, 48, 48, 16, 16)


# 中型艦砲台（回転式）
class MidBattery1(EnemyBase):
	def __init__(self, t):
		super(MidBattery1, self).__init__()
		self.t = gcommon.T_MID_BATTERY1
		self.x = t[2]
		self.y = t[3]
		self.firsttime = t[4]	# 最初の攻撃まで
		self.interval = t[5]	# 攻撃間隔
		self.shotTime = t[6]	# 攻撃時間
		self.left = 0
		self.top = 0
		self.right = 31
		self.bottom = 31
		self.hp = 100
		self.layer = gcommon.C_LAYER_GRD
		self.score = 300
		self.hitcolor1 = 5
		self.hitcolor2 = 6
		self.exptype = gcommon.C_EXPTYPE_GRD_M

	def update(self):
		if self.y > gcommon.SCREEN_MAX_Y:
			self.removeFlag = True
		else:
			if self.state==0:
				# 最初の沈黙
				if self.cnt==self.firsttime:
					self.state=1
					self.cnt=0
			elif self.state==1:
				# 攻撃
				if self.cnt & 15 == 15:
					enemy_shot(		\
					 self.x+16 +math.cos(gcommon.atan_table[self.cnt & 63])*6,		\
					 self.y+16 +math.sin(gcommon.atan_table[self.cnt & 63])*6,		\
					 2*2,1)
				if self.cnt==self.shotTime:
					self.state=2
					self.cnt=0
			elif self.state==2:
				# 沈黙
				if self.cnt==self.interval:
					self.state = 1
					self.cnt=0

	def draw(self):
		if self.state==1 and self.cnt & 4 == 0:
			pyxel.blt(self.x, self.y, 1, 112, 160, 32, 32)
		else:
			pyxel.blt(self.x, self.y, 1, 80, 160, 32, 32)

midTank2Tbl = [[260, 0], [30, 1], [100, 0], [30, 1], [200, 0], [80,1]]

class MidTank2(EnemyBase):
	def __init__(self, t):
		super(MidTank2, self).__init__()
		self.t = gcommon.T_LARGE_TANK1
		self.x = t[2]
		self.y = t[3]
		self.left = 8
		self.top = 4
		self.right = 47
		self.bottom = 39
		self.hp = 500
		self.layer = gcommon.C_LAYER_GRD
		self.score = 1000
		self.hitcolor1 = 5
		self.hitcolor2 = 6
		self.exptype = gcommon.C_EXPTYPE_GRD_M
		self.tblIndex = 0
		self.cnt2 = 0		# 攻撃用カウント

	def update(self):
		if self.y > gcommon.SCREEN_MAX_Y:
			self.removeFlag = True
		else:
			if self.state == 0:
				if self.cnt == midTank2Tbl[self.tblIndex][0]:
					self.tblIndex+=1
					self.cnt=0
					if self.tblIndex == len(midTank2Tbl):
						self.state = 1
				else:
					mode = midTank2Tbl[self.tblIndex][1]
					if mode == 0:
						pass
					else:
						self.y -=1
		
		if self.cnt2 & 63==63:
			for i in range(-3,4, 2):
				enemy_shot_offset(self.x+28, self.y+20, 2, 0, i)

		self.cnt2+=1
		

	def draw(self):
		pyxel.blt(self.x, self.y, 1, 80, 112, 56, 40, gcommon.TP_COLOR)

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


