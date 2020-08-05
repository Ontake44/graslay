import pyxel
import math
import random
import gcommon
import enemy


# ボス処理

class Boss1(enemy.EnemyBase):
	def __init__(self, t):
		super(Boss1, self).__init__()
		self.t = gcommon.T_BOSS1
		self.x = t[2]
		self.y = t[3]
		self.left = 0
		self.top = 0
		self.right = 71
		self.bottom = 67
		self.hp = 32000
		self.layer = gcommon.C_LAYER_GRD
		self.score = 5000
		self.sd = 0
		self.subcnt = 0
		self.hitcolor1 = 5
		self.hitcolor2 = 6


	def update(self):
		if gcommon.game_timer==3720:
			gcommon.cur_scroll=0
		
		if gcommon.is_outof_bound(self):
			self.removeFlag = True
		else:
			if self.state==0:
				if self.cnt>240:
					self.cnt=0
					self.state=1
				
			elif self.state==1:
				if gcommon.cur_scroll==0:
					self.y -= 0.5 * 2
				elif self.cnt & 64==0:
					self.y -= 0.35 * 2
				
				self.boss1_shot_cross()
				if self.y<=0:
					self.state=2
					self.cnt=0
				
			elif self.state==2:
				remove_all_battery()
				if self.subcnt==0:
					self.hp=1000
				
				if self.cnt & 7==7 and self.cnt & 127 !=127:
					enemy.enemy_shot(		\
					 self.x+18*2 +math.cos(gcommon.atan_table[self.cnt & 63])*8,		\
					 self.y+10*2 +math.sin(gcommon.atan_table[self.cnt & 63])*8,		\
					 2*2,1)
					gcommon.sound(gcommon.SOUND_SHOT2)
				
				self.sd = (self.cnt & 4)>>2
				if self.cnt==300:
					self.state=3
					self.cnt=0
				
			elif self.state==3:
				if self.cnt & 15 ==15:
					shot_cross(self.x+18*2, self.y+12*2, self.cnt>>2)
					gcommon.sound(gcommon.SOUND_SHOT2)
				
				self.sd = (self.cnt & 4)>>2
				if self.cnt==300:
					self.state=4
					self.subcnt = 0
					self.cnt=0
				
			elif self.state==4:
				if self.cnt & 31== 31:
					if self.cnt & 63==63:
						for i in range(1,6):
							enemy.enemy_shot_offset(self.x+18*2, self.y+10*2, 2*2,1,(i-3)*2)
						
					else:
						for i in range(1,7):
							enemy.enemy_shot_offset(self.x+18*2, self.y+10*2, 2*2,1,(i-4)*2+1)
						
					gcommon.sound(gcommon.SOUND_SHOT2)
				
				
				if self.cnt==120:
					create_battery1(12*2,16*2,1)
					create_battery1(28*2,16*2,240)
					create_battery1(92*2,16*2,240)
					create_battery1(108*2,16*2,1)

				if self.cnt==300:
					self.state=5
					self.cnt=0

				##	self.subcnt+=1
				#	if self.subcnt==1:
				#		self.state=5
				#		create_battery1(12*2,16*2,1)
				#		create_battery1(28*2,16*2,240)
				#		create_battery1(92*2,16*2,240)
				#		create_battery1(108*2,16*2,1)
				#		self.cnt=0
				#		self.subcnt=0
				#	else:
				#		self.subcnt = 0
				#		self.state=2
				#		self.cnt=0
				#
				
			elif self.state==5:
				self.y += 0.25*2
				self.boss1_shot_cross()
				if self.y>=50:
					self.state=6
					self.cnt=0
				
			elif self.state==6:
				self.boss1_shot_cross()
				if self.cnt==300:
					self.state=7
					self.cnt=0
				
			elif self.state==7:
				self.y -= 0.25*2
				self.boss1_shot_cross()
				if self.y<=8:
					self.state=2
					self.cnt=0
					self.subcnt+=1
				
			elif self.state==100:
				if self.cnt>120:
					self.state=101
					self.cnt=0
				
			elif self.state==101:
				if self.cnt % 12 == 0:
					enemy.create_explosion(
					self.x+(self.right-self.left)/2 +random.randrange(36)-18,
					self.y+(self.bottom-self.top)/2 +random.randrange(24)-12,
					self.layer,gcommon.C_EXPTYPE_GRD_M)
				
				if self.cnt>240:
					self.state=102
					self.cnt=0
					#pyxel.play(1, 5)
					gcommon.sound(gcommon.SOUND_LARGE_EXP)
				
			elif self.state==102:
				#sfx(4)
				if self.cnt>150:
					self.state=103
					self.cnt=0
				
			elif self.state==103:
				if self.cnt>180:
					self.state=104
					self.cnt=0
					gcommon.cur_scroll=0.4
					gcommon.ObjMgr.objs.append(enemy.StageClearText(1))


	def boss1_shot_cross(self):
		if self.cnt % 60 ==0:
			gcommon.sound(gcommon.SOUND_SHOT2)
			if self.cnt % 120==0:
				self.sd=1
				shot_cross(self.x+18*2, self.y+12*2, 8)
			else:
				self.sd=0
				shot_cross(self.x+18*2, self.y+12*2, 0)


	def draw(self):
		if self.state< 100:
			#spr(192,self.x,self.y,5,4)
			#spr(197+self.sd*2,self.x+10,self.y+4,2,2)
			pyxel.blt(self.x, int(self.y), 1, 0, 192, 80, 64, gcommon.TP_COLOR)
			pyxel.blt(self.x +20, int(self.y) +8, 1, 80 + self.sd*32, 192, 32, 32, gcommon.TP_COLOR)
		elif self.state < 103:
			#spr(192,self.x,self.y,5,4)
			pyxel.blt(self.x, int(self.y), 1, 0, 192, 80, 64, gcommon.TP_COLOR)
		else:
			#spr(203,self.x+10,self.y+10,2,2)
			pyxel.blt(self.x+20, int(self.y)+20, 1, 176, 192, 32, 32, gcommon.TP_COLOR)
		
		if self.state==102:
			pyxel.circb(self.x+(self.right-self.left)/2,
				self.y+(self.bottom-self.top)/2, self.cnt*2*2,7)
			gcommon.circfill_obj_center(self, self.cnt*2, 7)
			r = 0
			for i in range(1,201):
				rr = math.sqrt((self.cnt*2+i)*20)*2
				pyxel.pset(			\
					self.x+(self.right-self.left+1)/2+math.cos(r) * rr,		\
					self.y+(self.bottom-self.top+1)/2+math.sin(r) * rr,		\
					7 + int(self.cnt%2)*3)
				# kore ha tekito
				r += 0.11 + i*0.04
			
		elif self.state==103:
			d=True
			r=20
			clr=7
			if self.cnt<60:
				d = (self.cnt & 1)==1
			elif self.cnt<120:
				d = (self.cnt & 3)==3
				r = 16
				clr = 10
			else:
				d = (self.cnt & 7)==7
				r = 12
				clr = 9
			
			if d:
				gcommon.circfill_obj_center(self, r, clr)

	def broken(self):
		if self.state<100:
			self.layer = gcommon.C_LAYER_EXP_GRD
			self.cnt=0
			self.state=100
			enemy.create_explosion(
				self.x+(self.right -self.left+1)/2,
				self.y+(self.bottom -self.top+1)/2-4,
				self.layer, gcommon.C_EXPTYPE_GRD_M)
			gcommon.score += 10000
			remove_all_battery()

def create_battery1(x,y,hidetime):
	#local s={0,t_battery1,x,y,hidetime}
	#local o=battery1:new(s)
	#add(objs,o)
	gcommon.ObjMgr.objs.append(enemy.Battery1.create(x,y,hidetime))

def remove_all_battery():
	for obj in gcommon.ObjMgr.objs:
		if obj.t == gcommon.T_BATTERY1:
			obj.removeFlag = True

def shot_cross(cx,cy,dr):
	for i in range(0,64,16):
		enemy.enemy_shot_dr(
			cx + math.cos(gcommon.atan_table[(i+dr) & 63])*8,
			cy + math.sin(gcommon.atan_table[(i+dr) & 63])*8,
			2*2, 1, (i+dr) & 63)


class Boss2(enemy.EnemyBase):
	def __init__(self, t):
		super(Boss2, self).__init__()
		self.t = gcommon.T_BOSS2
		self.x = t[2]*2
		self.y = t[3]*2
		self.left = 0
		self.top = 0
		self.right = 71
		self.bottom = 67
		self.hp = 32000
		self.layer = gcommon.C_LAYER_UPPER_GRD
		self.score = 5000
		self.subcnt = 0
		self.hitcolor1 = 5
		self.hitcolor2 = 6
		self.material_cnt=6
		self.material_offset=0
		self.dy=0
		self.dr=0

	def appended(self):
		gcommon.ObjMgr.objs.append(Boss2Side(self, -20*2, False))
		gcommon.ObjMgr.objs.append(Boss2Side(self, 36*2, True))

	def update(self):
		st = self.state
		if st<10:
			if gcommon.map_y >= (680+17*8)*2:
				# scroll loop
				gcommon.map_y = (632+17*8)*2
			
		else:
			if gcommon.map_y>=2048*2:
				# scroll loop
				gcommon.map_y=1280*2
			
		if st==0:
			if self.cnt>270:
				self.cnt=0
				self.state=1
				#-gcommon.cur_scroll=0
			
		elif st==1:
			if self.subcnt==0:
				self.y -= 0.1*2
			else:
				self.y-=gcommon.cur_scroll
			
			if self.cnt % 10 == 0:
				#add(objs,material:new(
				#	self.x-16+(6-self.material_cnt)*4,self.y+8))
				#add(objs,material:new(
				#	self.x+41-(6-self.material_cnt)*4,self.y+8))
				gcommon.ObjMgr.objs.append(
					Material(self.x-16*2+(6-self.material_cnt)*4*2, self.y+8*2))
				gcommon.ObjMgr.objs.append(
					Material(self.x+41*2+(6-self.material_cnt)*4*2, self.y+8*2))
								
				self.material_cnt-=1
				if self.material_cnt==0:
					self.cnt=0
					self.state=2
				
			
			if self.cnt%60==0:
				boss2_shot_offset(self)
			
		elif st==2:
			if self.subcnt==0:
				self.y-=0.3
			else:
				self.y-=gcommon.cur_scroll
			
			if self.cnt%60==0:
				boss2_shot_offset(self)
			
			if self.cnt>60:
				self.cnt=0
				self.state=3
				self.subcnt+=1
				if self.subcnt>2:
					self.state=4
				
			
		elif st==3:
			if self.subcnt==0:
				self.y -= 0.4
			else:
				self.y-=gcommon.cur_scroll
			
			if self.material_cnt<6:
				#-self.material_offset+=1
				if self.cnt % 6 == 0:
					self.material_cnt+=1
				
			
			if self.cnt%30==0:
				boss2_shot_offset(self)
			
			if self.cnt>60:
				self.cnt=0
				self.state=1
			
		elif st==4:
			self.y -= gcommon.cur_scroll
			if self.cnt%30==0:
				boss2_shot_offset(self)
			
			if self.cnt>60:
				self.cnt=0
				self.state=5
				self.dx=-0.2
				gcommon.cur_scroll=0.4
			
		elif st==5:
			self.y -= gcommon.cur_scroll
			self.y += self.dx
			self.dx-=0.025
			if self.cnt>60:
				self.cnt=0
				self.state=6
				boss2_shot_offset(self)
			
		elif st==6:
			self.y -= gcommon.cur_scroll
			#gcommon.cur_scroll+=0.05
			gcommon.cur_scroll+=0.1
			if self.cnt>60:
				self.cnt=0
				self.state=7
			
		elif st==7:
			self.y -= gcommon.cur_scroll
			if self.y < 8:
				self.y += 0.2
			
			if self.cnt%30==0:
				boss2_shot_offset(self)
			
			if self.cnt>420:
				self.cnt=0
				self.state=10
				self.hp=2000
				gcommon.draw_star = True
			
		elif st==10:
			self.y -= gcommon.cur_scroll
			if self.cnt==120:
				self.state=11
				self.cnt=0
				self.layer = gcommon.C_LAYER_SKY
				self.subcnt=0
				#--create_explosion(
				#-- self.x+8,
				#-- self.y+16,
				#-- c_layer_sky,c_exptype_sky_m)
				#--create_explosion(
				#-- self.x+24,
				#-- self.y+16,
				#-- c_layer_sky,c_exptype_sky_m)
			
		elif st==11:
			#-- wait
			#--if self.cnt>60 then
			#-- self.cnt=0 self.state=12
			#--end
			nextstate(self, 60, 12)

		elif st==12:
			if self.cnt%10==0:
				dr=0
				if self.subcnt%2==1:
					dr+=1
				
				if self.cnt%20==0:
					dr+=2
				shot_radial(self, dr)
			
			nextstate(self, 120, 13)
		elif st==13:
			self.x-=0.5
			self.y-=0.125
			if self.x<4:
				self.state=14
				self.cnt=0
				self.dr=2
			
		elif st==14:
			self.x+=1	#0.5
			boss2_shot_side(self)
			if self.cnt%8==0:
				enemy.enemy_shot_dr(			\
					self.x+17*2,		\
					self.y+12*2,		\
					2*2, 1, (self.dr & 63))
				self.dr+=1
			
			if self.x>96*2:
				self.state=15
				self.dr=32
			
		elif st==15:
			self.x-=1		#0.5
			boss2_shot_side(self)
			if self.cnt%8==0:
				enemy.enemy_shot_dr(
					self.x+17*2,
					self.y+12*2,
				2*2,  1, (self.dr & 63))
				self.dr-=1
			
			if self.x<4*2:
				self.state=16
				self.cnt=0
			
		elif st==16:
			if self.x<63-14:
				self.x+=0.5
			
			if self.y<4:
				self.y+=0.125
			
			if self.cnt>120:
				self.cnt=0
				self.state=12
				self.subcnt+=1
			
		elif st==102:
			#sfx(4)
			#--circfill(self.x+(self.r-self.l)/2,
			#-- self.y+(self.b-self.u)/2, self.cnt,7)
			if self.cnt>150:
				self.state=103
				self.cnt=0
				#pyxel.play(1, 5)
				gcommon.sound(gcommon.SOUND_LARGE_EXP)
			
		elif st==103:
			if self.cnt>240:
				self.state=104
				self.cnt=0
				#--gcommon.cur_scroll=0.2
				gcommon.ObjMgr.objs.append(enemy.StageClearText(2))
			
		elif st==104:
			if self.cnt>240:
				self.removeFlag = True
				gcommon.app.startStage(3)
				

	def draw(self):
		#-- left
		#--spr(132,self.x-20,self.y+8,2,4)
		#--sspr(48,72,8,12,self.x-4,self.y+17)
		#-- right
		#--spr(132,self.x+36,self.y+8,2,4,true)
		#--sspr(48,72,8,12,self.x+28,self.y+17,8,12,true)
		#-- middle
		if self.state<=10:
			#spr(128,self.x,self.y,4,4)
			gcommon.spr1(128,self.x,self.y,4,4)
			draw_material(self.x,self.y,
				self.material_offset,
				self.material_cnt)
			if self.state<=4:
				lx=0
				if self.state==4:
					lx=self.cnt/2
				
				if lx<26:
					#sspr(48,84,4,12,self.x-20+lx,self.y+2)
					gcommon.sspr1(48, 84, 4, 12, self.x-20*2+lx*2, self.y+2*2)
					#sspr(48,64,8,6,self.x-16+lx,self.y+4)
					gcommon.sspr1(48, 64, 8, 6, self.x-16*2+lx*2, self.y+4*2)
					#sspr(48,64,8,6,self.x-8+lx,self.y+4)
					gcommon.sspr1(48, 64, 8, 6, self.x-8*2+lx*2, self.y+4*2)
					if lx<8:
						#sspr(48,64,8,6,self.x+lx,self.y+4)
						gcommon.sspr1(48, 64, 8, 6, self.x+lx*2, self.y+4*2)
						#-- right
						#sspr(48,64,8,6,self.x+24-lx,self.y+4)
						gcommon.sspr1(48, 64, 8, 6, self.x+24*2-lx*2, self.y+4*2)
					
					#-- right
					#sspr(48,84,4,12,self.x+48-lx,self.y+2,4,12,true)
					gcommon.sspr1(48, 84, -4, 12, self.x+48*2-lx*2, self.y+2*2)
					#sspr(48,64,8,6,self.x+32-lx,self.y+4)
					gcommon.sspr1(48, 64, 8, 6, self.x+32*2-lx*2, self.y+4*2)
					#sspr(48,64,8,6,self.x+40-lx,self.y+4)
					gcommon.sspr1(48, 64, 8, 6, self.x+40*2-lx*2, self.y+4*2)
				
			
			#--spr(136,self.x+8,self.y,2,3)

			#sspr(7,68,18,12,self.x+7,self.y+4)
			gcommon.sspr1(7, 68, 18, 12, self.x+7*2, self.y+4*2)
			#sspr(7,72,18,24,self.x+7,self.y+16)
			gcommon.sspr1(7, 72, 18, 24, self.x+7*2, self.y+16*2)

			if self.state==5:
				#-- fire
				#--if self.cnt%2 ==0 then
				#-- spr(138,self.x,self.y+32,1,2)
				#--end
				pass
			
		elif self.state<100:
			#--change
			#spr(192,self.x-4,self.y,5,4)
			gcommon.spr1(192, self.x-4*2, self.y, 5, 4)
			if self.state==11:
				gcommon.draw_splash(self)
			
		elif self.state==102:
			pyxel.circb(self.x+(self.right-self.left)/2,
				self.y+(self.bottom-self.top)/2, self.cnt*2,7)
			#--circfill(self.x+(self.r-self.l)/2,
			#-- self.y+(self.b-self.u)/2, self.cnt,7)
			gcommon.circfill_obj_center(self, self.cnt, 7)
			gcommon.draw_splash(self)
			#--local r = 0
			#--for i=1,200 do
			#-- local rr = sqrt((self.cnt*2+i)*20)
			#-- pset(
			#--  self.x+(self.r-self.l+1)/2+cos(r) * rr,
			#--  self.y+(self.b-self.u+1)/2+sin(r) * rr,
			#--  7 + flr(self.cnt%2)*3)
			#--  -- kore ha tekito
			#--  r += 0.11 + i*0.04
			#--end
		elif self.state==103:
			d = True
			r = 20
			clr = 7
			if self.cnt<60:
				d = (self.cnt & 1)==1
			elif self.cnt<120:
				d = (self.cnt & 3)==3
				r=16
				clr=10
			else:
				d = (self.cnt & 7)==7
				r=12
				clr=9
			
			if d:
				gcommon.circfill_obj_center(self, r, clr)

	def broken(self):
		if self.state<100:
			self.layer = gcommon.C_LAYER_EXP_SKY
			self.cnt = 0
			self.state= 102
			enemy.create_explosion(
				self.x+(self.right-self.left+1)/2,
				self.y+(self.bottom-self.top+1)/2-4,
				self.layer, gcommon.C_EXPTYPE_GRD_M)
			gcommon.score+=10000

class Boss2Side(enemy.EnemyBase):
	def __init__(self, bossobj, cx, flag):
		super(Boss2Side, self).__init__()
		self.t = gcommon.T_BOSS2SIDE
		self.bossobj = bossobj
		self.x = bossobj.x + cx
		self.y = bossobj.y
		self.left = 0
		self.top = 0
		self.right = 31
		self.bottom = 63
		self.hp = 300
		self.layer = gcommon.C_LAYER_GRD
		self.score = 1000
		self.subcnt = 0
		self.hitcolor1 = 5
		self.hitcolor2 = 6
		self.cx = cx
		self.flag = flag
		self.brokenflag = 0


	def update(self):
		if self.bossobj.state==11 and self.bossobj.cnt>0:
			if self.flag:
				self.x+=2
			else:
				self.x-=2
			
			self.y = self.bossobj.y
			if gcommon.is_outof_bound(self):
				self.removeFlag = True
			
		else:
			self.x = self.bossobj.x+self.cx
			self.y = self.bossobj.y
			if self.brokenflag==0 and self.bossobj.state>0 and self.bossobj.state<=10:
				if self.cnt%60 ==0:
					enemy.enemy_shot(self.x+8*2,self.y+35*2,2,1)
				
			
	def draw(self):
		#local fireflag=(bossobj.state==11)

		if self.flag:
			gcommon.spr1(132+self.brokenflag*4, self.x, self.y+8*2, -2, 4)
			gcommon.sspr1(48,72, -8,12, self.x-8*2, self.y+17*2)
		else:
			gcommon.spr1(132+self.brokenflag*4, self.x, self.y+8*2, 2, 4)
			gcommon.sspr1(48,72,8,12, self.x+16*2, self.y+17*2)

	def broken(self):
		self.brokenflag = 1
		self.layer = gcommon.C_LAYER_HIDE_GRD
		enemy.create_explosion(
			self.x+(self.right-self.left+1)/2,
			self.y+30*2,
			gcommon.C_LAYER_SKY, gcommon.C_EXPTYPE_SKY_M)
		gcommon.score += self.score


# BOSS2 Material
class Material(enemy.EnemyBase):
	def __init__(self, x, y):
		super(Material, self).__init__()
		self.t = gcommon.T_MATERIAL
		self.x = x
		self.y = y
		self.left = 0
		self.top = 0
		self.right = 15
		self.bottom = 33
		self.hp = 0
		self.layer = gcommon.C_LAYER_SKY
		self.score = 10
		self.hitcolor1 = 5
		self.hitcolor2 = 6
		self.dx = 0
		self.exptype = gcommon.C_EXPTYPE_SKY_S
		if abs(x - gcommon.ObjMgr.myShip.x)<8:
			self.dx = 0
		elif x<gcommon.ObjMgr.myShip.x:
			self.dx = 2
		else:
			self.dx = -2

	def update(self):
		self.x += self.dx
		self.y += 6
		if gcommon.is_outof_bound(self):
			self.removeFlag = True


	def draw(self):
		gcommon.spr1(135, self.x, self.y, 1, 2)

def draw_material(x,y,offset,count):
	for i in range(1,count+1):
		gcommon.spr1(135,
			x-20*2+(6-count+i)*4*2-offset,
			y+8*2,1,2)
		gcommon.spr1(135,x+32*2+13*2-(6-count+i)*4*2+offset*2,y+8*2,1,2)



def boss2_shot_side(self):
	if self.subcnt>=1 and self.cnt%80==0:
		enemy.enemy_shot(self.x,self.y+18*2,2,0)
		enemy.enemy_shot(self.x+31*2,self.y+18*2,2,0)

def nextstate(self, cnt, nextstate):
	if self.cnt>cnt:
		self.state = nextstate
		self.cnt = 0


def boss2_shot_offset(self):
	enemy.enemy_shot_offset(
		self.x+22*2, self.y+26*2, 2*2,2,-1)
	enemy.enemy_shot_offset(
		self.x+10*2, self.y+26*2, 2*2,2,1)

def shot_radial(self, dr):
	#for i=1,64,4 do
	for i in range(0, 64, 4):
		enemy.enemy_shot_dr(
			self.x+32,
			self.y+18,
			2, 1, (i+dr) & 63)

# ax, ay, 
# 1: X座標がこれより小さくなると減速、次のインデックスへ
# 2: X座標がこれより大きくなると減速、次のインデックスへ
# 3: Y座標がこれより小さくなると減速、次のインデックスへ
# 4: Y座標がこれより大きくなると減速、次のインデックスへ
# ax, ay, mode, X or Y]
boss3tbl = [
	[0, -0.0125, 3, 10], 
	[0, 0.0125, 4, 40],
	[0.012, -0.012, 3, 10], 
	[-0.013, -0.002, 1, -10],
	[0, 0.01, 4, 30],			# 下移動
	[0.012, 0, 2, 160],			# 横移動
	[-0.012, -0.012, 3, 0],		# 左上へ
	[0.012, 0, 2, 100],
	[-0.012, 0.012, 4, 40],
	]

class Boss3(enemy.EnemyBase):
	def __init__(self, t):
		super(Boss3, self).__init__()
		self.t = gcommon.T_BOSS3
		self.x = t[2]
		self.y = t[3]
		self.left = 0
		self.top = 0
		self.right = 159
		self.bottom = 135
		self.hp = 32000
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.score = 5000
		self.subcnt = 0
		self.hitcolor1 = 5
		self.hitcolor2 = 6
		self.dy = -0.5
		self.dx = 0
		self.tblIndex = 0
		
	def update(self):
		if self.state == 0:
			if self.cnt == 600:
				gcommon.ObjMgr.objs.append(Boss3Body(self))
				self.nextState()
		
		if self.state in (0,1):
			self.x += self.dx
			self.y += self.dy
			mode = boss3tbl[self.tblIndex][2]
			if mode == 1:
				if self.x < boss3tbl[self.tblIndex][3]:
					self.dx *= 0.95
					self.dy *= 0.95
					if abs(self.dx) < 0.01:
						self.nextTbl()
				else:
					self.addDxDy()
			elif mode == 2:
				if self.x > boss3tbl[self.tblIndex][3]:
					self.dx *= 0.95
					self.dy *= 0.95
					if abs(self.dx) < 0.01:
						self.nextTbl()
				else:
					self.addDxDy()
			elif mode == 3:
				# 上制限（上移動）
				if self.y < boss3tbl[self.tblIndex][3]:
					self.dx *= 0.95
					self.dy *= 0.95
					if abs(self.dy) <=0.01:
						self.nextTbl()
				else:
					self.addDxDy()
			elif mode == 4:
				# 下制限（下移動）
				if self.y > boss3tbl[self.tblIndex][3]:
					self.dx *= 0.95
					self.dy *= 0.95
					if abs(self.dy) <= 0.01:
						self.nextTbl()
				else:
					self.addDxDy()
		elif self.state == 100:		# broken
			self.dx = 0
			self.dy = 0
			if self.cnt == 80:
				self.nextState()
		
		elif self.state == 101:
			self.y += gcommon.cur_scroll
			if self.cnt == 40:
				self.nextState()
		
		elif self.state == 102:
			self.y += gcommon.cur_scroll
			if self.cnt % 10 == 0:
				enemy.create_explosion(
				self.x+(self.right-self.left)/2 +random.randrange(80)-40,
				self.y+(self.bottom-self.top)/2 +random.randrange(80)-30,
				self.layer,gcommon.C_EXPTYPE_GRD_M)
			if self.cnt == 120:
				gcommon.ObjMgr.objs.append(Boss3Explosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_GRD))
				self.nextState()
		elif self.state == 103:
			self.y += gcommon.cur_scroll
			if self.cnt == 120:
				self.remove()

	def nextTbl(self):
		self.tblIndex +=1
		if self.tblIndex >= len(boss3tbl):
			self.tblIndex = 0
		self.dx = boss3tbl[self.tblIndex][0]
		self.dy = boss3tbl[self.tblIndex][1]

	def addDxDy(self):
		if abs(self.dx) < 0.5:
			self.dx +=  boss3tbl[self.tblIndex][0]
		if abs(self.dy) < 0.5:
			self.dy +=  boss3tbl[self.tblIndex][1]

	def draw(self):
		pyxel.blt(self.x, self.y, 2, 0, 120, 160, 136, gcommon.TP_COLOR)
		if self.state == 0:
			pyxel.blt(self.x +48, self.y +48, 2, 160, 120, 64, 72, gcommon.TP_COLOR)
		if self.cnt & 1 != 0:
			# バーニア
			if abs(self.dx) <= 0.01:
				pass
			elif self.dx < 0:
				pyxel.blt(self.x+92, self.y +16, 2, 96, 64, 32, 16 -(self.cnt & 2)*16, gcommon.TP_COLOR)
				pyxel.blt(self.x+144, self.y +114, 2, 96, 64, 32, 16 -(self.cnt & 2)*16, gcommon.TP_COLOR)
			else:
				pyxel.blt(self.x+35, self.y +16, 2, 96, 64, -32, 16 -(self.cnt & 2)*16, gcommon.TP_COLOR)
				pyxel.blt(self.x-16, self.y +114, 2, 96, 64, -32, 16 -(self.cnt & 2)*16, gcommon.TP_COLOR)

			# メインエンジン
			if self.dy == 0:
				pass
			elif self.dy <= 0:
				pyxel.blt(self.x+20, self.y +136, 2, 208, 48, 24 -(self.cnt & 2)*24, 72, gcommon.TP_COLOR)
				pyxel.blt(self.x+113, self.y +136, 2, 208, 48, 24 -(self.cnt & 2)*24, 72, gcommon.TP_COLOR)
			else:
				pyxel.blt(self.x+20, self.y +136, 2, 232, 48, 24 -(self.cnt & 2)*24, 72, gcommon.TP_COLOR)
				pyxel.blt(self.x+113, self.y +136, 2, 232, 48, 24 -(self.cnt & 2)*24, 72, gcommon.TP_COLOR)

			

class Boss3Body(enemy.EnemyBase):
	def __init__(self, obj):
		super(Boss3Body, self).__init__()
		self.t = gcommon.T_BOSS3
		self.x = obj.x + 48
		self.y = obj.y + 48
		self.left = 0
		self.top = 0
		self.right = 63
		self.bottom = 71
		self.hp = 2000
		self.layer = gcommon.C_LAYER_GRD
		self.score = 5000
		self.subcnt = 0
		self.hitcolor1 = 5
		self.hitcolor2 = 6
		self.outside = obj
		self.dr1 = 0
		self.dr2 = 0
		self.shotcnt = 0
		self.crosscnt = 0

	def update(self):
		self.x = int(self.outside.x) + 48
		self.y = int(self.outside.y) + 48
		if self.cnt % 28 == 0:
			shot_cross(self.x+32, self.y-8, self.crosscnt)
			gcommon.sound(gcommon.SOUND_SHOT2)
			self.crosscnt += 3
			
			#self.dr1 = gcommon.get_atan_no_to_ship(self.x + 67, self.y + 37)
			#print("dr " + str(self.dr1))
			#enemy.enemy_shot_dr(self.x + 67, self.y + 37, 2, 0, self.dr1)
			#enemy.enemy_shot(self.x+67, self.y+37,2,0)
			pass
		if self.state == 0:
			if self.cnt == 1:
				self.dr1 = gcommon.get_atan_no_to_ship(self.x + 80, self.y + 48)
			if self.cnt & 7 ==7 and self.shotcnt < 4:
				enemy.enemy_shot_dr(self.x + 80, self.y + 48, 4, 0, self.dr1)
				gcommon.sound(gcommon.SOUND_SHOT2)
				self.shotcnt += 1
			if self.cnt == 50:
				self.cnt = 0
				self.shotcnt = 0
				self.state = 1
		elif self.state == 1:
			if self.cnt == 1:
				self.dr2 = gcommon.get_atan_no_to_ship(self.x -16, self.y + 48)
			if self.cnt & 7 ==7 and self.shotcnt < 4:
				enemy.enemy_shot_dr(self.x -16, self.y + 48, 4, 0, self.dr2)
				gcommon.sound(gcommon.SOUND_SHOT2)
				self.shotcnt += 1
			if self.cnt == 50:
				self.cnt = 0
				self.shotcnt = 0
				self.state = 0
	
	
	def draw(self):
		pyxel.blt(self.x, self.y, 2, 160, 120, 64, 72, gcommon.TP_COLOR)

	def broken(self):
		enemy.create_explosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY, gcommon.C_EXPTYPE_SKY_L)
		#gcommon.ObjMgr.objs.append(Boss3Explosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_GRD))
		gcommon.ObjMgr.objs.append(Boss3B(gcommon.getCenterX(self), self.y + 50))
		enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
		self.remove()
		self.outside.setState(100)
		gcommon.score+=10000

class Boss3Explosion(enemy.EnemyBase):
	def __init__(self, cx, cy, layer):
		super(Boss3Explosion, self).__init__()
		self.t = gcommon.T_BOSSEXPLOSION
		self.x = cx
		self.y = cy
		self.layer = layer

	def update(self):
		if self.state == 0:
			if self.cnt == 0:
				gcommon.sound(gcommon.SOUND_BOSS_EXP)
			elif self.cnt>170:
				#self.nextState()
				self.remove()
				#pyxel.play(1, 5)
		elif self.state == 1:
			if self.cnt>20:
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



# 0:mode
#   0: 停止
#   1: X座標がこれより小さくなると減速、次のインデックスへ
#   2: X座標がこれより大きくなると減速、次のインデックスへ
#   3: Y座標がこれより小さくなると減速、次のインデックスへ
#   4: Y座標がこれより大きくなると減速、次のインデックスへ
# 1:ax, 2: ay, 
# 3: X or Y or 停止時間
# 4: 攻撃パターン
#   0: なし
#   1: 最初の全体攻撃（左右から）
#   2: 正面
#   3: 波状
#   4: 時計回り攻撃
#   5: 反時計回り攻撃
# mode, ax, ay, X or Y or 停止時間, 攻撃パターン]
boss3Btbl = [
	[4, 0, 0.125,  10, 0],
	[0, 0, 0,  140, 1],				# 全体攻撃
	[0, 0, 0,  30, 0],
	[2, 0.125, 0.02, 160, 2],			# 右移動 正面攻撃
	[0, 0, 0,  30, 0],
	[3, -0.125, -0.0625,  20, 0],		# 左上へ
	[2, 0.125, 0, 100, 3],				# 右移動 波状攻撃
	[1, -0.125, 0, 20, 4],			# 左移動 時計回り攻撃
	[2, 0.125, 0, 120, 5],			# 左移動 時計回り攻撃
	]

class Boss3B(enemy.EnemyBase):
	def __init__(self, x, y):
		super(Boss3B, self).__init__()
		self.t = gcommon.T_BOSS3
		self.left = 0
		self.top = 0
		self.right = 47
		self.bottom = 31
		self.x = x - 24
		self.y = y - 48/2
		self.hp = 3000
		self.layer = gcommon.C_LAYER_SKY
		self.score = 20000
		self.subcnt = 0
		self.hitcolor1 = 8
		self.hitcolor2 = 14
		self.dy = 0
		self.dx = 0
		self.tblIndex = 0
		self.firstX = 128-48/2
		self.firstY = -49
		self.subcnt = 0
		self.brake = False
		
	def update(self):
		if self.state == 0:
			# 格納庫
			if self.cnt == 80:
				self.nextState()
		elif self.state == 1:
			# 初期位置まで移動
			if abs(self.firstY - self.y) < 1 and abs(self.firstX - self.x) < 1:
				self.nextState()
				self.dx = 0
				self.dy = 0
			else:
				r = math.atan2(self.firstY - self.y, self.firstX - self.x)
				self.dx = math.cos(r) * 1
				self.dy = math.sin(r) * 1
				self.x += self.dx
				self.y += self.dy

		elif self.state == 2:
			self.brake = False
			if self.cnt == 60:
				self.nextState()
		elif self.state == 3:
			self.x += self.dx
			self.y += self.dy
			self.brake = False
			mode = boss3Btbl[self.tblIndex][0]
			if mode == 0:
				if self.subcnt == boss3Btbl[self.tblIndex][3]:
					self.nextTbl()
			elif mode == 1:
				if self.x < boss3Btbl[self.tblIndex][3]:
					self.dx *= 0.95
					self.dy *= 0.95
					self.brake = True
					if abs(self.dx) < 0.01:
						self.nextTbl()
				else:
					self.addDxDy()
			elif mode == 2:
				if self.x > boss3Btbl[self.tblIndex][3]:
					self.dx *= 0.95
					self.dy *= 0.95
					self.brake = True
					if abs(self.dx) < 0.01:
						self.nextTbl()
				else:
					self.addDxDy()
			elif mode == 3:
				# 上制限（上移動）
				if self.y < boss3Btbl[self.tblIndex][3]:
					self.dx *= 0.95
					self.dy *= 0.95
					self.brake = True
					if abs(self.dy) <=0.01:
						self.nextTbl()
				else:
					self.addDxDy()
			elif mode == 4:
				# 下制限（下移動）
				if self.y > boss3Btbl[self.tblIndex][3]:
					self.dx *= 0.95
					self.dy *= 0.95
					self.brake = True
					if abs(self.dy) <= 0.01:
						self.nextTbl()
				else:
					self.addDxDy()

			attack = boss3Btbl[self.tblIndex][4]
			if attack == 1:
				# 全体攻撃
				if self.subcnt & 7 == 0:
					enemy.enemy_shot_dr(self.x +24, self.y + 18, 6, 1, 49 + (self.subcnt>>3)*2)
					enemy.enemy_shot_dr(self.x +24, self.y + 18, 6, 1, 47 - (self.subcnt>>3)*2)
					gcommon.sound(gcommon.SOUND_SHOT2)
			elif attack == 2:
				# 正面攻撃
				if self.subcnt & 15 == 0:
					enemy.enemy_shot_dr(self.x +24 +16, self.y + 32, 4, 1, 16)
					enemy.enemy_shot_dr(self.x +24 -16, self.y + 32, 4, 1, 16)
					gcommon.sound(gcommon.SOUND_SHOT2)
			elif attack == 3:
				# 波状攻撃
				if self.subcnt & 15 == 0:
					if self.subcnt & 31 == 0:
						for i in range(1,6):
							enemy.enemy_shot_offset(self.x+24, self.y+18, 2*2,1, -(i-2)*2)
						gcommon.sound(gcommon.SOUND_SHOT2)
					else:
						for i in range(1,6):
							enemy.enemy_shot_offset(self.x+24, self.y+18, 2*2,1, (i-2)*2)
						gcommon.sound(gcommon.SOUND_SHOT2)
			
			elif attack == 4:
				# 時計回り攻撃
				if self.subcnt & 7 == 0:
					enemy.enemy_shot_dr(self.x +24, self.y + 18, 5, 1, (self.subcnt>>3)+2)
					enemy.enemy_shot_dr(self.x +24, self.y + 18, 6, 1, (self.subcnt>>3)-2)
					gcommon.sound(gcommon.SOUND_SHOT2)

			elif attack == 5:
				# 反時計回り攻撃
				if self.subcnt & 7 == 0:
					enemy.enemy_shot_dr(self.x +24, self.y + 18, 6, 1, (34 -(self.subcnt>>3)))
					enemy.enemy_shot_dr(self.x +24, self.y + 18, 5, 1, (30 -(self.subcnt>>3)))
					gcommon.sound(gcommon.SOUND_SHOT2)
				
			self.subcnt+=1

		elif self.state == 100:
			# broken
			self.dx = 0
			self.dy = 0
			self.subcnt = 0
			if self.cnt > 120:
				gcommon.ObjMgr.objs.append(Boss3Explosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_GRD))
				gcommon.score+=self.score
				self.nextState()

		elif self.state == 101:
			if self.cnt > 300:
				self.nextState()

		elif self.state == 102:
			gcommon.ObjMgr.objs.append(enemy.StageClearText(3))
			if self.cnt > 240:
				self.nextState()

		elif self.state == 103:
			self.remove()
			gcommon.app.startGameClear()

	def nextTbl(self):
		self.tblIndex +=1
		if self.tblIndex >= len(boss3Btbl):
			self.tblIndex = 0
		self.dx = boss3Btbl[self.tblIndex][1]
		self.dy = boss3Btbl[self.tblIndex][2]
		self.subcnt = 0

	def addDxDy(self):
		if abs(self.dx) < 1:
			self.dx +=  boss3Btbl[self.tblIndex][1]
		if abs(self.dy) < 1:
			self.dy +=  boss3Btbl[self.tblIndex][2]

	def draw(self):
		if self.state >= 101:
			return
		elif self.state == 100:
			pyxel.blt(self.x, self.y, 2, 160, 192, 48, 48, gcommon.TP_COLOR)
			pyxel.blt(self.x +48, self.y, 2, 72, 64, 24, 24, gcommon.TP_COLOR)
			pyxel.blt(self.x -24, self.y, 2, 0, 64, 24, 24, gcommon.TP_COLOR)
			return
		if self.cnt & 1 == 0:
			tl = False
			tr = False
			bl = False
			br = False
			if self.dy > 0.01:
				if self.dx > 0.01:
					tl = True
				elif self.dx < -0.01:
					tr = True
				else:
					tl = True
					tr = True
			elif self.dy < -0.01:
				if self.dx > 0.01:
					bl = True
				elif self.dx < -0.01:
					br = True
				else:
					bl = True
					br = True
			else:
				if self.dx > 0.01:
					bl = True
					tl = True
				elif self.dx < -0.01:
					br = True
					tr = True

			if self.brake:
				if tl:
					pyxel.blt(self.x +48, self.y +26, 2, 128, 80, 24, 24, gcommon.TP_COLOR)
				if tr:
					pyxel.blt(self.x -24, self.y +26, 2, 128, 80, -24, 24, gcommon.TP_COLOR)
				if bl:
					pyxel.blt(self.x +48, self.y -24, 2, 128, 80, 24, -24, gcommon.TP_COLOR)
				if br:
					pyxel.blt(self.x -24, self.y -24, 2, 128, 80, -24, -24, gcommon.TP_COLOR)
			else:
				if tl:
					pyxel.blt(self.x -32, self.y -24, 2, 96, 80, -32, -32, gcommon.TP_COLOR)
				if tr:
					pyxel.blt(self.x +48, self.y -24, 2, 96, 80, 32, -32, gcommon.TP_COLOR)
				if bl:
					pyxel.blt(self.x -32, self.y +26, 2, 96, 80, -32, 32, gcommon.TP_COLOR)
				if br:
					pyxel.blt(self.x +48, self.y +26, 2, 96, 80, 32, 32, gcommon.TP_COLOR)
			
		if self.state == 1:
			if self.cnt >= 0 and self.cnt<24:
				pyxel.blt(self.x +48, self.y, 2, 95 -self.cnt, 64, self.cnt+1, 24, gcommon.TP_COLOR)
				pyxel.blt(self.x -self.cnt -1, self.y, 2, 0, 64, self.cnt+1, 24, gcommon.TP_COLOR)
			elif self.cnt>=24:
				pyxel.blt(self.x +48, self.y, 2, 72, 64, 24, 24, gcommon.TP_COLOR)
				pyxel.blt(self.x -24, self.y, 2, 0, 64, 24, 24, gcommon.TP_COLOR)
		elif self.state in  (2, 3):
				pyxel.blt(self.x +48, self.y, 2, 72, 64, 24, 24, gcommon.TP_COLOR)
				pyxel.blt(self.x -24, self.y, 2, 0, 64, 24, 24, gcommon.TP_COLOR)
		
		pyxel.blt(self.x, self.y, 2, 24, 64, 48, 48, gcommon.TP_COLOR)

	def broken(self):
		self.setState(100)
		# 当たり判定がないレイヤに移動しないと何度もbrokenが呼ばれてしまう
		self.layer = gcommon.C_LAYER_HIDE_GRD
		enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
		gcommon.sound(gcommon.SOUND_LARGE_EXP)

