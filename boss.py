import pyxel
import math
import random
import gcommon
import enemy


# ボス処理

class Boss1(enemy.EnemyBase):
	def __init__(self, t):
		super(Boss1, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.left = 16
		self.top = 16
		self.right = 79
		self.bottom = 45
		self.hp = 999999
		self.layer = gcommon.C_LAYER_SKY
		self.score = 5000
		self.subcnt = 0
		self.hitcolor1 = 3
		self.hitcolor2 = 14
		self.brake = False
		self.beam = 0
		self.subState = 0
		self.tbl = []
		self.beamObj = Boss1Beam(self)
		gcommon.ObjMgr.addObj(self.beamObj)

	def update(self):
		self.beam = 0
		if self.state == 0:
			self.x -= gcommon.cur_scroll_x
			if self.cnt % 60 == 0:
				self.shotFix4()
			if self.cnt > 260:
				self.nextState()
		elif self.state == 1:
			self.x -= gcommon.cur_scroll_x
			self.x += 0.625
			self.y -= 0.125
			if self.cnt % 60 == 0:
				self.shotFix4()
			if self.cnt > 220:
				self.nextState()
		elif self.state == 2:
			self.y += 0.125
			if self.cnt % 60 == 0:
				self.shotFix4()
			if self.cnt > 180:
				self.nextState()
				self.hp = 1000
		elif self.state == 3:
			# ４、８方向ショット
			if self.subState == 0:
				self.y -= 0.250
				if self.y < 0:
					self.y = 0
			else:
				self.y += 0.250
				if self.y > 150:
					self.y = 150
			if self.cnt & 15 == 15:
				self.shotFix8()
				#if self.cnt & 31 == 31:
				#	self.shotFix4()
				#else:
			if self.cnt > 120:
				self.nextState()
				if self.subState == 0:
					self.subState = 1
				else:
					self.subState = 0
		elif self.state == 4:
			# ビーム発射前

			if self.cnt & 1 == 1:
				x = 50 + random.random() * 30
				y = random.random() * 6
				a = 200 + random.random() * 500
				if self.cnt & 3 == 3:
					a *= -1
				self.tbl.append(Boss1Star(x, y, a))

			newTbl = []
			for s in self.tbl:
				s.x -= 2
				if s.x>=0:
					newTbl.append(s)
			self.tbl = newTbl

			if self.cnt > 90:
				self.nextState()
		elif self.state == 5:
			# ビーム発射開始（移動なし）
			self.beam = int(self.cnt/3) +1
			if self.beam > 5:
				self.nextState()
		elif self.state == 6:
			# ビーム発射中（移動なし）
			self.beam = 6
			self.beamObj.hitCheck = True
			if self.cnt > 60:
				self.nextState()
		elif self.state == 7:
			# ビーム発射中（移動あり）
			self.beam = 6
			zy = abs(self.y +30 - gcommon.ObjMgr.myShip.y)
			if zy > 80:
				dy = 3
			elif zy > 50:
				dy = 2
			elif zy > 20:
				dy = 1
			else:
				dy = 0.25
			if self.y +30 > gcommon.ObjMgr.myShip.y:
				dy = -dy
			self.y += dy
			if self.cnt > 90:
				self.nextState()
		elif self.state == 8:
			# ビーム発射終了（移動なし）
			self.beam = 5- int(self.cnt/3)
			self.beamObj.hitCheck = False
			if self.beam < 0:
				self.state = 3
				self.cnt = 0

	def draw(self):
		if self.state == 4:
			for s in self.tbl:
				y = s.x* s.x/s.a
				pyxel.pset(self.x -s.x, self.y +28 -y + s.y, 7)

		pyxel.blt(self.x, self.y , 1, 160, 200, 96, 56, gcommon.TP_COLOR)
		if self.beam >= 1 and self.beam <=5:
			bx = self.x -12
			while(bx > -8):
				pyxel.blt(bx, self.y +10, 1, (self.beam-1) * 8, 208, 8, 40, gcommon.TP_COLOR)
				bx -=8
			
		if self.beam == 6:
			# ビーーーーーーーーーーーーーーーム！！！
			pyxel.blt(self.x -16, self.y +10, 1, 144, 208, 16, 40, gcommon.TP_COLOR)
			bx = self.x -32
			sx = 128 - ((self.cnt>>1) & 3) * 16
			while(bx > -32):
				pyxel.blt(bx, self.y +10, 1, sx, 208, 16, 40, gcommon.TP_COLOR)
				bx -=16

	def shotFix4(self):
		enemy.enemy_shot_dr(self.x +48, self.y +22, 4, 1, 33);
		enemy.enemy_shot_dr(self.x +52, self.y +16, 4, 1, 37);
		enemy.enemy_shot_dr(self.x +48, self.y +42, 4, 1, 31);
		enemy.enemy_shot_dr(self.x +52, self.y +48, 4, 1, 27);

	def shotFix8(self):
		enemy.enemy_shot_dr(self.x +48, self.y +22, 2, 0, 31);
		enemy.enemy_shot_dr(self.x +48, self.y +22, 2, 0, 33);
		
		enemy.enemy_shot_dr(self.x +52, self.y +16, 2, 0, 35);
		enemy.enemy_shot_dr(self.x +52, self.y +16, 2, 0, 37);
		
		enemy.enemy_shot_dr(self.x +48, self.y +42, 2, 0, 31);
		enemy.enemy_shot_dr(self.x +48, self.y +42, 2, 0, 33);
		
		enemy.enemy_shot_dr(self.x +52, self.y +48, 2, 0, 27);
		enemy.enemy_shot_dr(self.x +52, self.y +48, 2, 0, 29);

	def broken(self):
		self.setState(100)
		self.shotHitCheck = False
		self.beamObj.remove()
		gcommon.ObjMgr.objs.append(Boss3Explosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_GRD))
		gcommon.score+=self.score
		self.remove()
		gcommon.sound(gcommon.SOUND_LARGE_EXP)


# 波動砲発射前の、あの吸い込むようなやつ
class Boss1Star:
	def __init__(self, x, y, a):
		self.x = x
		self.y = y
		self.a = a
		self.removeFlag = False


class Boss1Beam(enemy.EnemyBase):
	def __init__(self, bossObj):
		super(Boss1Beam, self).__init__()
		self.bossObj = bossObj
		self.hitCheck = False
		self.shotHitCheck = False
	
	def update(self):
		self.x = 0
		self.y = self.bossObj.y + 10
		self.right = self.bossObj.x
		self.bottom = 39

	def draw(self):
		pass

# ボス２固定台
class Boss2Base(enemy.EnemyBase):
	def __init__(self, bossObj, pos):
		super(Boss2Base, self).__init__()
		self.bossObj = bossObj
		self.left = 16
		self.top = 8
		self.right = 56
		self.bottom = 23
		self.layer = gcommon.C_LAYER_UPPER_GRD
		self.hp = 50
		self.hitcolor1 = 3
		self.hitcolor2 = 10
		self.pos = pos
		self.exptype = gcommon.C_EXPTYPE_GRD_M
		if pos ==0:
			# 上側
			self.x = self.bossObj.x +4
			self.y = self.bossObj.y -24
		else:
			# 下側
			self.x = self.bossObj.x +4
			self.y = self.bossObj.y +36

	def update(self):
		pass

	def draw(self):
		pyxel.blt(int(self.x), self.y, 1, 32 + self.pos*72, 224, 72, 32, gcommon.TP_COLOR)
		


# 触手
# dr: 生えてる角度
# count : 粒の数

# mode
#   1 : まっすぐ伸びる
#   2 : ゆらゆら開始
#   3 : 縮む
class Feeler(enemy.EnemyBase):
	def __init__(self, parentObj, offsetX, offsetY, dr, count):
		super(Feeler, self).__init__()
		self.x = parentObj.x + offsetX
		self.y = parentObj.y + offsetY
		self.parentObj = parentObj
		self.offsetX = offsetX
		self.offsetY = offsetY
		self.left = 0
		self.top = 0
		self.dr = dr
		self.right = 71
		self.bottom = 67
		self.hp = 32000
		self.cells = []		# 相対座標
		self.mode = 0
		self.subDr = 0
		for i in range(0, count):
			self.cells.append([0, 0])
		# 触手セルの当たり判定範囲
		self.cellRect = gcommon.Rect.create(2,2,13,13)

	def setMode(self, mode):
		self.mode = mode
		self.status = 1
		self.cnt = 0

	def update(self):
		self.x = self.parentObj.x + self.offsetX
		self.y = self.parentObj.y + self.offsetY
		if self.mode == 1:
			if self.status ==1:
				#print("cnt = " + str(self.cnt))
				i = 1
				x = 0
				y = 0
				for pos in self.cells:
					pos[0] = x + math.cos(gcommon.atan_table[int(self.dr + i * self.subDr) & 63]) * 12 * (self.cnt) /30.0
					pos[1] = y + math.sin(gcommon.atan_table[int(self.dr + i * self.subDr) & 63]) * 12 * (self.cnt) /30.0
					x = pos[0]
					y = pos[1]
					i += 1
				if self.cnt == 30:
					self.status = 0
					
		elif self.mode == 2:
			# ゆらゆら動く
			if self.status == 1:
				self.subDr = 0.0
				self.status = 2
			elif self.status == 2:
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
					self.status = 3
			elif self.status == 3:
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
					self.status = 2
			if self.cnt % 30 == 0:
				if len(self.cells) > 0:
					pos = self.cells[len(self.cells)-1]
					enemy.enemy_shot(self.x +pos[0] +8, self.y +pos[1] +8, 2, 0)

		elif self.mode == 3:
			# 縮む
			if self.status ==1:
				#print("cnt = " + str(self.cnt))
				i = 1
				x = 0
				y = 0
				for pos in self.cells:
					pos[0] = x + math.cos(gcommon.atan_table[int(self.dr + i * self.subDr) & 63]) * 12 * (30 -self.cnt) /30.0
					pos[1] = y + math.sin(gcommon.atan_table[int(self.dr + i * self.subDr) & 63]) * 12 * (30 -self.cnt) /30.0
					x = pos[0]
					y = pos[1]
					i += 1
				if self.cnt == 30:
					self.status = 0
		
	def draw(self):
		size = len(self.cells)
		i = 0
		while(i<size):
			pos = self.cells[size -1 -i]
			if i == 0:
				pyxel.blt(self.x + pos[0], self.y + pos[1], 1, 32, 128, 16, 16, gcommon.TP_COLOR)
			else:
				pyxel.blt(self.x + pos[0], self.y + pos[1], 1, 0, 128, 16, 16, gcommon.TP_COLOR)
			i += 1

	# 自機弾と敵との当たり判定と破壊処理
	def checkShotCollision(self, shot):
		if shot.removeFlag:
			return False
		hit = False
		if len(self.cells)> 0:
			# 触手部の当たり判定（先端のみ）
			pos = self.cells[len(self.cells) -1]
			x = self.x +pos[0]
			y = self.y +pos[1]
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
				x = self.x +pos[0]
				y = self.y +pos[1]
				if gcommon.check_collision2(x, y, self.cellRect, gcommon.ObjMgr.myShip):
					return True
			return False

# 0:mode
#   0: 停止
#   1: X座標がこれより小さくなると減速、次のインデックスへ
#   2: X座標がこれより大きくなると減速、次のインデックスへ
#   3: Y座標がこれより小さくなると減速、次のインデックスへ
#   4: Y座標がこれより大きくなると減速、次のインデックスへ
#   5: 触手伸ばす
#   6: 触手縮める
#   100: 指定インデックスへ
# 1:ax, 2: ay, 
# 3: X or Y or 停止時間
# 4: 攻撃パターン
#   0: なし
#   1: 最初の全体攻撃（左右から）
#   2: 正面
#   3: 波状
#   4: 時計回り攻撃
#   5: 反時計回り攻撃
# mode, ax, ay, X or Y or 停止時間 or 移動先インデックス, 攻撃パターン]
boss2tbl = [
	[2, 0.25, 0, 140, 0],		# 右の定位置に移動
	[5, 0, 0, 60, 0],			# 触手伸ばす
	[3, 0, -0.25, 30, 0],		# 上移動
	[4, 0, 0.25, 130, 0],		# 下移動
	[3, 0, -0.25, 64, 0],		# 上移動
	[6, 0, 0, 60, 0],			# 触手縮める
	[4, 0, 0.25, 130, 0],		# 下移動
	[100, 0.0, 0.0, 1, 0],
	]

class Boss2(enemy.EnemyBase):
	def __init__(self, t):
		super(Boss2, self).__init__()
		self.t = gcommon.T_BOSS1
		pos = gcommon.mapPosToScreenPos(t[2], t[3])
		self.x = pos[0]
		self.y = pos[1]
		self.left = 16
		self.top = 9
		self.right = 63
		self.bottom = 38
		self.hp = 32000
		self.layer = gcommon.C_LAYER_GRD
		self.score = 5000
		self.subcnt = 0
		self.dx = 0.5
		self.dy = 0
		self.hitcolor1 = 3
		self.hitcolor2 = 7
		self.tblIndex = 0
		self.brake = False
		self.feelers = []
		self.feelers.append(Feeler(self, 50, 29, 8, 6))
		self.feelers.append(Feeler(self, 16, 29, 24, 6))
		self.feelers.append(Feeler(self, 16, 8, 40, 6))
		self.feelers.append(Feeler(self, 50, 8, 56, 6))
		#self.feelers[0].setMode(1)
		#self.feelers[1].setMode(1)
		#self.feelers[2].setMode(1)
		#self.feelers[3].setMode(1)
		gcommon.ObjMgr.addObj(self.feelers[0])
		gcommon.ObjMgr.addObj(self.feelers[1])
		gcommon.ObjMgr.addObj(self.feelers[2])
		gcommon.ObjMgr.addObj(self.feelers[3])
		
		self.upperBase = Boss2Base(self,0)
		self.lowerBase = Boss2Base(self,1)
		gcommon.ObjMgr.addObj(self.upperBase)
		gcommon.ObjMgr.addObj(self.lowerBase)

	def update(self):
		if self.state == 0:
			if self.x <= 168:
				if self.upperBase.removeFlag == False:
					self.upperBase.broken()
				if self.lowerBase.removeFlag == False:
					self.lowerBase.broken()
				self.nextState()
		elif self.state == 1:
			if self.cnt == 120:
				self.layer = gcommon.C_LAYER_SKY
				self.nextState()
				self.dx = 0.25
				self.dy = 0.0
		elif self.state == 2:
			self.x += self.dx
			self.y += self.dy
			if self.x > 150:
				self.dx = 0
				self.setState(4)
		elif self.state == 4:
			self.x += self.dx
			self.y += self.dy
			self.brake = False
			mode = boss2tbl[self.tblIndex][0]
			if mode == 0:
				if self.subcnt == boss2tbl[self.tblIndex][3]:
					self.nextTbl()
			elif mode == 1:
				if self.x < boss2tbl[self.tblIndex][3]:
					self.dx *= 0.95
					self.dy *= 0.95
					self.brake = True
					if abs(self.dx) < 0.01:
						self.dx = 0
						self.nextTbl()
				else:
					self.addDxDy()
			elif mode == 2:
				if self.x > boss2tbl[self.tblIndex][3]:
					self.dx *= 0.95
					self.dy *= 0.95
					self.brake = True
					if abs(self.dx) < 0.01:
						self.dx = 0
						self.nextTbl()
				else:
					self.addDxDy()
			elif mode == 3:
				# 上制限（上移動）
				if self.y < boss2tbl[self.tblIndex][3]:
					self.dx *= 0.95
					self.dy *= 0.95
					self.brake = True
					if abs(self.dy) <=0.01:
						self.nextTbl()
				else:
					self.addDxDy()
			elif mode == 4:
				# 下制限（下移動）
				if self.y > boss2tbl[self.tblIndex][3]:
					self.dx *= 0.95
					self.dy *= 0.95
					self.brake = True
					if abs(self.dy) <= 0.01:
						self.nextTbl()
				else:
					self.addDxDy()
			elif mode == 5:
				# 触手伸ばす
				if self.subcnt == 1:
					self.feelers[0].subDr = -1
					self.feelers[1].subDr = 1
					self.feelers[2].subDr = -1
					self.feelers[3].subDr = 1
					self.feelers[0].setMode(1)
					self.feelers[1].setMode(1)
					self.feelers[2].setMode(1)
					self.feelers[3].setMode(1)
				if self.subcnt == boss2tbl[self.tblIndex][3]:
					self.feelers[0].setMode(2)
					self.feelers[1].setMode(2)
					self.feelers[2].setMode(2)
					self.feelers[3].setMode(2)
					self.nextTbl()
			elif mode == 6:
				# 触手縮める
				if self.subcnt == 1:
					print("mode 6 :1")
					self.feelers[0].setMode(3)
					self.feelers[1].setMode(3)
					self.feelers[2].setMode(3)
					self.feelers[3].setMode(3)
				if self.subcnt == boss2tbl[self.tblIndex][3]:
					self.nextTbl()
			elif mode == 100:
				self.tblIndex = boss2tbl[self.tblIndex][3]
				self.subcnt = 0
			
			attack = boss2tbl[self.tblIndex][4]
			attack = 0
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

	def draw(self):
		pyxel.blt(self.x, self.y, 1, 176, 208, 80, 48, gcommon.TP_COLOR)
		

	def nextTbl(self):
		self.tblIndex +=1
		if self.tblIndex >= len(boss2tbl):
			self.tblIndex = 0
		self.dx = boss2tbl[self.tblIndex][1]
		self.dy = boss2tbl[self.tblIndex][2]
		self.subcnt = 0

	def addDxDy(self):
		if abs(self.dx) < 0.5:
			self.dx +=  boss2tbl[self.tblIndex][1]
		if abs(self.dy) < 0.5:
			self.dy +=  boss2tbl[self.tblIndex][2]

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





def nextstate(self, cnt, nextstate):
	if self.cnt>cnt:
		self.state = nextstate
		self.cnt = 0


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

