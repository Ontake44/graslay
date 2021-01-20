import pyxel
import math
import random
import gcommon
import enemy


# ボス処理

class Boss1Base(enemy.EnemyBase):
	def __init__(self, t):
		super(Boss1Base, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.left = 16
		self.top = 16
		self.right = 79
		self.bottom = 45
		self.hp = 999999
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.ground = True
		self.shotHitCheck = False	# 自機弾との当たり判定
		self.hitCheck = False	# 自機と敵との当たり判定
		self.enemyShotCollision = False	# 敵弾との当たり判定を行う
		self.posY = 0

	def update(self):
		if self.x <= -96:
			self.remove()
			return
		if self.cnt > 210:
			if self.posY < 64:
				 self.posY += 1

	def draw(self):
		# 上
		pyxel.blt(self.x, self.y -self.posY -40, 1, 160, 128, 96, -64, gcommon.TP_COLOR)
		# 下
		pyxel.blt(self.x, self.y +31 +self.posY, 1, 160, 128, 96, 64, gcommon.TP_COLOR)
 

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
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.score = 5000
		self.subcnt = 0
		self.hitcolor1 = 9
		self.hitcolor2 = 10
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
				gcommon.sound(gcommon.SOUND_BOSS1PREBEAM)
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
				gcommon.sound(gcommon.SOUND_BOSS1BEAM)
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

	def checkShotCollision(self, shot):
		ret = super(Boss1, self).checkShotCollision(shot)
		if ret:
			rad = math.atan2(shot.dy, shot.dx)
			enemy.Particle1.appendCenter(shot, rad)
		return ret

	def shotFix4(self):
		enemy.enemy_shot_dr(self.x +48, self.y +22, 4, 1, 33)
		enemy.enemy_shot_dr(self.x +52, self.y +16, 4, 1, 37)
		enemy.enemy_shot_dr(self.x +48, self.y +42, 4, 1, 31)
		enemy.enemy_shot_dr(self.x +52, self.y +48, 4, 1, 27)
		gcommon.sound(gcommon.SOUND_SHOT2)

	def shotFix8(self):
		enemy.enemy_shot_dr(self.x +48, self.y +22, 2, 0, 31)
		enemy.enemy_shot_dr(self.x +48, self.y +22, 2, 0, 33)
		
		enemy.enemy_shot_dr(self.x +52, self.y +16, 2, 0, 35)
		enemy.enemy_shot_dr(self.x +52, self.y +16, 2, 0, 37)
		
		enemy.enemy_shot_dr(self.x +48, self.y +42, 2, 0, 31)
		enemy.enemy_shot_dr(self.x +48, self.y +42, 2, 0, 33)
		
		enemy.enemy_shot_dr(self.x +52, self.y +48, 2, 0, 27)
		enemy.enemy_shot_dr(self.x +52, self.y +48, 2, 0, 29)
		gcommon.sound(gcommon.SOUND_SHOT2)

	def broken(self):
		self.setState(100)
		self.shotHitCheck = False
		self.beamObj.remove()
		enemy.removeEnemyShot()
		gcommon.ObjMgr.objs.append(Boss3Explosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
		gcommon.score+=self.score
		self.remove()
		gcommon.sound(gcommon.SOUND_LARGE_EXP)
		enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
		gcommon.ObjMgr.objs.append(enemy.Delay(enemy.StageClear, [0,0,1], 240))


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
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.ground = True
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
		if self.x < -72:
			self.remove()

	def draw(self):
		pyxel.blt(int(self.x), self.y, 1, 32 + self.pos*72, 224, 72, 32, gcommon.TP_COLOR)
		

#
# bossOffsetX : ボスでの相対座標
# toBaseOffsetX : bossOffsetからの総体座標
class Boss2Wire:
	def __init__(self, bossOffsetX, bossOffsetY, toBaseOffsetX, toBaseOffsetY, life, clr):
		self.bossOffsetX = bossOffsetX
		self.bossOffsetY = bossOffsetY
		self.baseOffsetX =  toBaseOffsetX
		self.baseOffsetY =  toBaseOffsetY
		self.x = 0
		self.y = 0
		self.dx = 0
		self.dy = 0
		self.lx = 0
		self.ly = 0
		self.life = life
		self.clr = clr

boss2Base2ColorTable = [1, 3, 5, 6, 8, 11, 12]

# ボス２固定台
class Boss2Base2(enemy.EnemyBase):
	def __init__(self, bossObj):
		super(Boss2Base2, self).__init__()
		self.bossObj = bossObj
		self.x = bossObj.x
		self.y = bossObj.y
		self.left = 16
		self.top = 8
		self.right = 56
		self.bottom = 23
		self.layer = gcommon.C_LAYER_EXP_SKY
		self.hp = 50
		self.hitcolor1 = 3
		self.hitcolor2 = 10
		self.exptype = gcommon.C_EXPTYPE_GRD_M
		self.hitCheck = False
		self.shotHitCheck = False
		self.initTable()

	def initTable(self):
		self.boss2BaseTable = []
		rad = math.pi * 70/180
		while(rad < math.pi * 120/180):
			clr = boss2Base2ColorTable[random.randrange(len(boss2Base2ColorTable))]
			self.boss2BaseTable.append(Boss2Wire(
				40 + math.cos(rad) * (20 + random.random() * 30),
				30 - math.sin(rad) * (15 + random.random() * 10),
				48 +math.cos(rad) * (90 + random.random() * 30),
				30 -math.sin(rad) * (60 + random.random() * 15),
				400 + int(random.random() * 50),
				clr
				))
			self.boss2BaseTable.append(Boss2Wire(
				40 + math.cos(rad) * (20 + random.random() * 30),
				20 + math.sin(rad) * (15 + random.random() * 10),
				48 + math.cos(rad) * (90 + random.random() * 30),
				20 + math.sin(rad) * (60 + random.random() * 15),
				400 + int(random.random() * 50),
				clr
				))
			rad += math.pi * 4/180


	def update(self):
		self.x -= gcommon.cur_scroll_x
		if self.x < -72:
			self.remove()
			return
		for item in self.boss2BaseTable:
			if item.life > self.cnt:
				item.x = self.bossObj.x + item.bossOffsetX
				item.y = self.bossObj.y + item.bossOffsetY
			elif item.life == self.cnt:
				item.lx = abs(self.x + item.baseOffsetX -item.x)
				item.ly = abs(self.y + item.baseOffsetY -item.y)
				rad = math.atan2(self.y + item.baseOffsetY - item.y, self.x + item.baseOffsetX -item.x)
				item.dx = math.cos(rad) * 4
				item.dy = math.sin(rad) * 4
			else:
				item.x += item.dx * abs(self.x + item.baseOffsetX -item.x)/item.lx
				item.y += item.dy * abs(self.y + item.baseOffsetY -item.y)/item.ly

	def draw(self):
		for item in self.boss2BaseTable:
			# ボス -> ベース
			pyxel.line(item.x, item.y, self.x + item.baseOffsetX, self.y + item.baseOffsetY, item.clr)
		


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
		self.layer = gcommon.C_LAYER_GRD
		self.left = 2
		self.top = 2
		self.dr = dr
		self.right = 13
		self.bottom = 13
		self.hp = 32000
		self.cells = []		# 相対座標
		self.mode = 0
		self.subDr = 0
		self.state = 0		# 0:縮小状態 1,2:モードで動作中
		for i in range(0, count):
			self.cells.append([0, 0])
		# 触手セルの当たり判定範囲
		self.cellRect = gcommon.Rect.create(2,2,13,13)

	def setMode(self, mode):
		self.mode = mode
		self.state = 1
		self.cnt = 0
		print("Feeler mode:" +str(mode))

	def update(self):
		self.x = self.parentObj.x + self.offsetX
		self.y = self.parentObj.y + self.offsetY
		if self.mode == 1:
			if self.state ==1:
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
					self.state = 2
					
		elif self.mode == 2:
			# ゆらゆら動く
			if self.state == 1:
				self.subDr = 0.0
				self.state = 2
			elif self.state == 2:
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
			if self.cnt % 30 == 0:
				if len(self.cells) > 0:
					pos = self.cells[len(self.cells)-1]
					enemy.enemy_shot(self.x +pos[0] +8, self.y +pos[1] +8, 2, 0)

		elif self.mode == 3:
			# 縮む
			if self.state ==1:
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
					self.state = 0
		
	def draw(self):
		if self.state != 0:
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
		if self.state != 0 and len(self.cells)> 0:
			# 触手部の当たり判定（先端のみ）
			pos = self.cells[len(self.cells) -1]
			x = self.x +pos[0]
			y = self.y +pos[1]
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
				x = self.x +pos[0]
				y = self.y +pos[1]
				if gcommon.check_collision2(x, y, self.cellRect, gcommon.ObjMgr.myShip):
					return True
			return False

# 伸びる触手
class Boss2Cell(enemy.EnemyBase):
	def __init__(self, parentObj, x, y, firstDr):
		super(Boss2Cell, self).__init__()
		self.x = x
		self.y = y
		self.parentObj = parentObj
		self.layer = gcommon.C_LAYER_GRD
		self.left = 2
		self.top = 2
		self.right = 13
		self.bottom = 13
		self.hp = 32000
		self.dr = firstDr
		self.cells = []

	def update(self):
		if self.state == 0:
			# 伸びる
			if self.cnt < 15:
				pass
			elif self.cnt % 2 == 0:
				tempDr = gcommon.get_atan_no_to_ship(self.x +4, self.y +4)
				rr = tempDr - self.dr
				if rr == 0:
					pass
				elif  (tempDr - self.dr) > 0:
					self.dr = (self.dr + 1) & 63
				else:
					self.dr = (self.dr - 1) & 63
			self.x += gcommon.cos_table[self.dr] * 3
			self.y += gcommon.sin_table[self.dr] * 3
			self.cells.append([self.x, self.y])
			if self.cnt > 60:
				self.nextState()
		elif self.state == 1:
			if self.cnt > 20:
				self.nextState()
		elif self.state == 2:
			del self.cells[-1]	# 最後から消す
			if len(self.cells) == 0:
				self.remove()

	def draw(self):
		index = len(self.cells) -1
		while(index >= 0):
			pos = self.cells[index]
			pyxel.blt(pos[0], pos[1], 1, 0, 128, 16, 16, gcommon.TP_COLOR)
			index -= 4



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
	[0, 0, 0, 240, 1],
#	[4, 0, 0.25, 130, 0],		# 下移動
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
		self.ground = True
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
		
		#self.upperBase = Boss2Base(self,0)
		#self.lowerBase = Boss2Base(self,1)
		#gcommon.ObjMgr.addObj(self.upperBase)
		#gcommon.ObjMgr.addObj(self.lowerBase)
		self.bossBase = Boss2Base2(self)
		gcommon.ObjMgr.addObj(self.bossBase)

	def update(self):
		if self.state == 0:
			if self.x <= 170:
				#if self.upperBase.removeFlag == False:
				#	self.upperBase.broken()
				#if self.lowerBase.removeFlag == False:
				#	self.lowerBase.broken()
				self.nextState()
		elif self.state == 1:
			if self.cnt == 80:
				self.layer = gcommon.C_LAYER_SKY
				self.ground = False
				self.dx = 0.05
				self.dy = 0.0
				self.nextState()
		elif self.state == 2:
			self.x += self.dx
			self.y += self.dy
			if self.x > 150:
				self.dx = 0
				self.hp = 1500
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
			if attack == 1:
				# 触手伸ばす攻撃
				if self.subcnt == 1:
					gcommon.ObjMgr.addObj(Boss2Cell(self, self.x +16, self.y+29, 24))
					gcommon.sound(gcommon.SOUND_FEELER_GROW)
				elif self.subcnt == 20:
					gcommon.ObjMgr.addObj(Boss2Cell(self, self.x +16, self.y+8, 40))
				elif self.subcnt == 40:
					gcommon.ObjMgr.addObj(Boss2Cell(self, self.x +50, self.y+8, 24))
				elif self.subcnt == 60:
					gcommon.ObjMgr.addObj(Boss2Cell(self, self.x +50, self.y+29, 40))
			self.subcnt+=1

	def draw(self):
		pyxel.blt(self.x, self.y, 1, 176, 208, 80, 48, gcommon.TP_COLOR)
		
	def checkShotCollision(self, shot):
		ret = super(Boss2, self).checkShotCollision(shot)
		if ret:
			rad = math.atan2(shot.dy, shot.dx)
			enemy.Particle1.appendCenter(shot, rad)
		return ret

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
		for feeler in self.feelers:
			feeler.remove()
		self.remove()
		enemy.removeEnemyShot()
		gcommon.ObjMgr.objs.append(Boss3Explosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
		gcommon.score+=self.score
		gcommon.sound(gcommon.SOUND_LARGE_EXP)
		enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
		gcommon.ObjMgr.objs.append(enemy.Delay(enemy.StageClear, [0,0,2], 240))


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




class Boss3Explosion(enemy.EnemyBase):
	def __init__(self, cx, cy, layer):
		super(Boss3Explosion, self).__init__()
		self.t = gcommon.T_BOSSEXPLOSION
		self.x = cx
		self.y = cy
		self.layer = layer
		self.hitCheck = False
		self.shotHitCheck = False

	def update(self):
		if self.state == 0:
			if self.cnt == 0:
				gcommon.sound(gcommon.SOUND_BOSS_EXP)
			elif self.cnt>120:
				#self.nextState()
				self.remove()
		elif self.state == 1:
			if self.cnt>40:
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


class Boss3Body:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.left = 3
		self.top = 8
		self.right = 42
		self.bottom = 39

class Boss3Anchor:
	def __init__(self):
		self.x = 0
		self.y = 0
		self.left = 1
		self.top = 4
		self.right = 23
		self.bottom = 11

#  出現
#  2 上端・下端に移動
#  3 下端からショットを打ちながら上端まで移動
#  4 車両側からEnemyShot、本体部が自機に追従
#  5 アンカー射出
#  6 上端に移動
#  7 上端からショットを打ちながら下端まで移動
#  8 本来部が中心まで移動
#  9 体当たり・戻る
#  10 最初に戻る
class Boss3(enemy.EnemyBase):
	def __init__(self, t):
		super(Boss3, self).__init__()
		self.x = 256
		self.y = 16
		self.left = 16
		self.top = 9
		self.right = 63
		self.bottom = 38
		self.hp = 1000
		self.layer = gcommon.C_LAYER_SKY
		self.score = 5000
		self.subcnt = 0
		self.hitcolor1 = 13
		self.hitcolor2 = 7
		self.body = Boss3Body()
		self.body.y = 72
		self.anchor = Boss3Anchor()
		self.upperARect = gcommon.Rect.create(8, 0, 72, 15)
		self.upperBRect = gcommon.Rect.create(24, 16, 71, 29)
		self.shaftRect = gcommon.Rect.create(40, 30, 62, 129)
		self.lowerBRect = gcommon.Rect.create(24, 130, 71, 143)
		self.lowerARect = gcommon.Rect.create(8, 144, 72, 159)
		self.mode = 0
		self.modeCnt = 0
		self.body_min_y = 16
		self.body_max_y = 128

	def nextState(self):
		self.state += 1
		self.cnt = 0
		self.mode = 0
		self.modeCnt = 0

	def setState(self, state):
		self.state = state
		self.cnt = 0
		self.mode = 0
		self.modeCnt = 0

	def nextMode(self):
		self.mode += 1
		self.modeCnt = 0
	
	def setMode(self, mode):
		self.mode = mode
		self.modeCnt = 0

	def setBodyAnchorPos(self):
		self.body.x = self.x +20
		self.anchor.x = self.body.x -8
		self.anchor.y = self.body.y +16

	def update(self):
		if self.state == 0:
			self.x -= 1
			if self.x <= 256 -88:
				self.nextState()
			self.body.x = self.x +20
			self.anchor.x = self.body.x -8
			self.anchor.y = self.body.y +16
		elif self.state == 1:
			if self.cnt > 30:
				self.nextState()
		elif self.state == 2:
			if self.mode == 0:
				# 上に移動
				self.body.y -= 2
				if self.body.y < self.body_min_y:
					self.body.y = self.body_min_y
					self.setMode(1)
			elif self.mode == 1:
				# 下に移動
				self.body.y += 2
				if self.body.y > self.body_max_y:
					self.body.y = self.body_max_y
					self.nextState()
			self.setBodyAnchorPos()
		elif self.state == 3:
			# 下端からショットを打ちながら上端まで移動
			self.body.y -= 1
			if self.body.y < self.body_min_y:
				self.body.y = self.body_min_y
				self.nextState()
			elif self.cnt % 15 == 0:
				gcommon.ObjMgr.addObj(Boss3Shot(self.x, self.body.y+12, 4))
				gcommon.ObjMgr.addObj(Boss3Shot(self.x, self.body.y+37, 4))
				gcommon.sound(gcommon.SOUND_SHOT3)
			self.setBodyAnchorPos()
		elif self.state == 4:
			cy = gcommon.getCenterY(gcommon.ObjMgr.myShip)
			if cy > self.body.y+25:
				self.body.y += 1
				if self.body.y > self.body_max_y:
					self.body.y = self.body_max_y
			elif cy < self.body.y+23:
				self.body.y -= 1
				if self.body.y < self.body_min_y:
					self.body.y = self.body_min_y

			self.setBodyAnchorPos()
			if self.cnt % 20 == 0:
				enemy.enemy_shot(self.x+20, self.y+27, 4, 0)
				enemy.enemy_shot(self.x+20, self.y+160-27, 4, 0)
				gcommon.sound(gcommon.SOUND_SHOT2)
			if self.cnt > 180:
				self.nextState()
		elif self.state == 5:
			if self.mode == 0:
				# アンカーが伸びる
				if self.modeCnt == 0:
					gcommon.sound(gcommon.SOUND_BOSS3_ANCHOR)
				self.anchor.x -= 8
				if self.anchor.x <= 0:
					self.anchor.x = 0
					self.nextMode()
			elif self.mode == 1:
				# アンカーが伸びきった
				if self.modeCnt > 30:
					self.nextMode()
				else:
					self.modeCnt += 1
			elif self.mode == 2:
				# アンカーが縮む
				self.anchor.x += 4
				if self.anchor.x >= self.body.x -8:
					self.anchor.x = self.body.x -8
					self.nextMode()
			elif self.mode == 3:
				if self.modeCnt > 30:
					self.nextState()
				else:
					self.modeCnt += 1
		elif self.state == 6:
			# 上に移動
			self.body.y -= 2
			if self.body.y < self.body_min_y:
				self.body.y = self.body_min_y
				self.nextState()
			self.setBodyAnchorPos()
		elif self.state == 7:
			# 上端からショットを打ちながら下端まで移動
			self.body.y += 1
			if self.body.y > self.body_max_y:
				self.body.y = self.body_max_y
				self.nextState()
			elif self.cnt % 15 == 0:
				gcommon.ObjMgr.addObj(Boss3Shot(self.x, self.body.y+12, 4))
				gcommon.ObjMgr.addObj(Boss3Shot(self.x, self.body.y+37, 4))
			self.setBodyAnchorPos()
		elif self.state == 8:
			# 中心に移動
			self.body.y -= 1
			if self.body.y < 72:
				self.body.y = 72
				self.nextState()
			self.setBodyAnchorPos()
		elif self.state == 9:
			# 体当たり・戻る
			if self.mode == 0:
				# 体当たり
				self.x -= 4
				if self.x <= -8:
					self.x = -8
					self.nextMode()
			elif self.mode == 1:
				# 左端まで移動した後の停止状態
				if self.modeCnt > 30:
					self.nextMode()
				else:
					self.modeCnt += 1
			elif self.mode == 2:
				# 戻る
				self.x += 2
				if self.x >= 256 -88:
					self.x = 256 -88
					self.setState(2)

			self.setBodyAnchorPos()

		# マップループ
		if gcommon.map_x >= 6800 + 256:
			gcommon.map_x -= 8*4

	def draw(self):
		xoffset = 0
		if self.cnt & 2 == 0:
			xoffset = -80
		# 上半分
		pyxel.blt(self.x, self.y, 1, 176 +xoffset, 224, 80, -32, gcommon.TP_COLOR)
		pyxel.blt(self.x+32, self.y+32, 1, 208, 176, 32, -48, gcommon.TP_COLOR)
		# 下半分
		pyxel.blt(self.x+32, self.y+80, 1, 208, 176, 32, 48, gcommon.TP_COLOR)
		pyxel.blt(self.x, self.y+128, 1, 176 +xoffset, 224, 80, 32, gcommon.TP_COLOR)
		# アンカー
		pyxel.blt(self.anchor.x, self.anchor.y, 1, 192, 112, 24, 16, gcommon.TP_COLOR)
		x = self.anchor.x +24
		while(x < self.body.x +8):
			pyxel.blt(x, self.anchor.y, 1, 216, 112, 16, 16, gcommon.TP_COLOR)
			x += 16

		# 本体
		pyxel.blt(self.body.x, self.body.y, 1, 208, 128, 48, 48, gcommon.TP_COLOR)

	# 自機弾と敵との当たり判定と破壊処理
	def checkShotCollision(self, shot):
		if shot.removeFlag:
			return False
		hit = False
		if gcommon.check_collision(self.body, shot):
			hit = True
		
		if hit:
			rad = math.atan2(shot.dy, shot.dx)
			enemy.Particle1.appendCenter(shot, rad)
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
		if gcommon.check_collision(self.body, gcommon.ObjMgr.myShip):
			return True
		if gcommon.check_collision(self.anchor, gcommon.ObjMgr.myShip):
			return True
		if gcommon.check_collision2(self.x, self.y, self.upperARect, gcommon.ObjMgr.myShip):
			return True
		if gcommon.check_collision2(self.x, self.y, self.upperBRect, gcommon.ObjMgr.myShip):
			return True
		if gcommon.check_collision2(self.x, self.y, self.shaftRect, gcommon.ObjMgr.myShip):
			return True
		if gcommon.check_collision2(self.x, self.y, self.lowerBRect, gcommon.ObjMgr.myShip):
			return True
		if gcommon.check_collision2(self.x, self.y, self.lowerARect, gcommon.ObjMgr.myShip):
			return True
		return False

	def broken(self):
		self.remove()
		enemy.removeEnemyShot()
		gcommon.ObjMgr.objs.append(Boss3Explosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
		gcommon.score+=self.score
		gcommon.sound(gcommon.SOUND_LARGE_EXP)
		gcommon.ObjMgr.objs.append(enemy.Delay(enemy.StageClear, [0,0,3], 240))

class Boss3Shot(enemy.EnemyBase):
	# x,y 弾の中心を指定
	# dr  0 -63
	def __init__(self, x, y, speed):
		super(Boss3Shot, self).__init__()
		self.shotHitCheck = False
		self.x = x
		self.y = y -3
		self.speed = speed
		self.layer = gcommon.C_LAYER_E_SHOT
		self.left = 2
		self.top = 2
		self.right = 24 -2-1
		self.bottom = 4

	def update(self):
		self.x -= self.speed
		if self.x <=-24 or self.x >= gcommon.SCREEN_MAX_X or self.y<-16 or self.y >=gcommon.SCREEN_MAX_Y:
			self.removeFlag = True

		if gcommon.isMapFreePos(gcommon.getCenterX(self), gcommon.getCenterY(self)) == False:
			self.removeFlag = True

	def draw(self):
		# pyxel.rect(self.x+ self.left, self.y+self.top, self.right-self.left+1, self.bottom-self.top+1, 8)
		pyxel.blt(self.x, self.y, 1, 192, 96, 24, 8, gcommon.TP_COLOR)


missileTable = [
	[0, 0, 0],
	[0, 1, 0],
	[1, 1, 0],
	[2, 0, 0],
	[0, 1, 2],
	[2, 2, 2]
]

class Boss4(enemy.EnemyBase):
	def __init__(self, t):
		super(Boss4, self).__init__()
		self.x = 256
		self.y = 80
		self.layer = gcommon.C_LAYER_SKY
		self.left = 27
		self.top = 8
		self.right = 87
		self.bottom = 45
		self.hp = 2000
		self.subState = 0
		self.subCnt = 0
		self.hitcolor1 = 9
		self.hitcolor2 = 10
		self.missileState = 0
		self.missileObj = [None, None, None]
		self.missileIndex = 0

	def update(self):
		if self.state == 0:
			self.x -= gcommon.cur_scroll_x
			if self.x <= 152:
				self.nextState()
		elif self.state == 1:
			if self.subState == 0:
				self.y -= 1
				if self.y < 8:
					self.nextSubState()
			elif self.subState == 1:
				self.y += 1
				if self.y > 140:
					self.nextSubState()
			elif self.subState == 2:
				self.y -= 1
				if self.y < 80:
					self.subState = 0
					self.subCnt = 0
					self.nextState()
			if self.cnt & 15 == 15:
				self.shotDanmaku()
		elif self.state == 2:
			self.shotMissle()
		elif self.state == 3:
			if self.subState == 0:
				self.y += 1
				if self.y > 140:
					self.nextSubState()
			elif self.subState == 1:
				self.y -= 1
				if self.y < 8:
					self.nextSubState()
			elif self.subState == 2:
				self.y += 1
				if self.y > 80:
					self.subState = 0
					self.subCnt = 0
					self.nextState()
			if self.cnt & 15 == 15:
				self.shotDanmaku()
		elif self.state in  [4, 5, 6, 7, 8]:
			self.shotMissle()
		elif self.state == 9:
			self.setState(1)

	def shotMissle(self):
		if self.subState == 0:
			cy = gcommon.getCenterY(gcommon.ObjMgr.myShip)
			if cy > self.y+30:
				self.y += 1
				if self.y > 140:
					self.y = 140
			elif cy < self.y+28:
				self.y -= 1
				if self.y < 8:
					self.y = 8			
		if self.subState == 0:
			# ミサイル発射準備
			if self.subCnt == 0:
				# ここでミサイルを決定する
				for i in range(3):
					mt = missileTable[self.missileIndex][i]
					if mt == 0:
						self.missileObj[i] = enemy.Missile1(self.x, self.y +16, 0)
					elif mt == 1:
						self.missileObj[i] = enemy.Missile2(self.x, self.y +16, 0)
					else:
						self.missileObj[i] = enemy.Missile3(self.x, self.y +16, 0)
				self.missileIndex += 1
				if self.missileIndex >= len(missileTable):
					self.missileIndex = 0
				self.subCnt += 1
			elif self.subCnt == 40:
				# ミサイル発射中へ
				self.nextSubState()
				self.missileState = 0
			else:
				self.subCnt += 1
		elif self.subState == 1:
			# ミサイル発射中
			if self.subCnt == 0:
				# ミサイル発射
				m = self.missileObj[self.missileState]
				m.x = self.x
				m.y = self.y +16 +self.missileState*8
				m.layer = gcommon.C_LAYER_GRD
				gcommon.ObjMgr.addObj(m)
				# インクリメント
				self.missileState += 1
				if self.missileState == 3:
					self.missileObj[0] = None
					self.missileObj[1] = None
					self.missileObj[2] = None
					self.nextSubState()
					return
			self.subCnt += 1
			if self.subCnt == 10:
				self.subCnt = 0
		elif self.subState == 2:
			# 待ち
			if self.subCnt == 30:
				self.setSubState(0)
				self.nextState()
				return
			self.subCnt += 1

	def shotDanmaku(self):
		if self.cnt & 31 == 31:
			enemy.enemy_shot_dr(self.x +52, self.y +16, 2, 0, 35)
			enemy.enemy_shot_dr(self.x +52, self.y +16, 2, 0, 37)

			enemy.enemy_shot_dr(self.x +48, self.y +22, 2, 0, 31)
			#enemy.enemy_shot_dr(self.x +48, self.y +22, 2, 0, 33)
			
			#enemy.enemy_shot_dr(self.x +48, self.y +42, 2, 0, 31)
			enemy.enemy_shot_dr(self.x +48, self.y +42, 2, 0, 33)
			
			enemy.enemy_shot_dr(self.x +52, self.y +48, 2, 0, 27)
			enemy.enemy_shot_dr(self.x +52, self.y +48, 2, 0, 29)
		else:
			enemy.enemy_shot_dr(self.x +52, self.y +16, 2, 1, 36)
			enemy.enemy_shot_dr(self.x +48, self.y +22, 2, 1, 34)
						
			enemy.enemy_shot_dr(self.x +48, self.y +42, 2, 1, 30)
			enemy.enemy_shot_dr(self.x +52, self.y +48, 2, 1, 28)
		gcommon.sound(gcommon.SOUND_SHOT2)


	def nextSubState(self):
		self.subState += 1
		self.subCnt = 0

	def setSubState(self, subState):
		self.subState = subState
		self.subCnt = 0

	def draw(self):
		if self.state in [2, 4, 5 ,6 ,7, 8]:
			if self.subState == 0:
				# ミサイル発射準備
				if self.subCnt < 32:
					x = self.x + 31- self.subCnt
				else:
					x = self.x
				for i in range(3):
					#pyxel.blt(x, self.y + 16 + i*8, 1, 48, 64, 32, 8, gcommon.TP_COLOR)
					if self.missileObj[i] != None:
						self.missileObj[i].x = x
						self.missileObj[i].y = self.y + 16 + i*8
						self.missileObj[i].drawMissile()
			elif self.subState == 1:
				# ミサイル発射中
				if self.missileState == 1:
					#pyxel.blt(self.x, self.y + 16 + 1*8, 1, 48, 64, 32, 8, gcommon.TP_COLOR)
					self.missileObj[1].x = self.x
					self.missileObj[1].y = self.y + 16 + 1*8
					self.missileObj[1].drawMissile()
				if self.missileState in [1, 2]:
					#pyxel.blt(self.x, self.y + 16 + 2*8, 1, 48, 64, 32, 8, gcommon.TP_COLOR)
					self.missileObj[2].x = self.x
					self.missileObj[2].y = self.y + 16 + 2*8
					self.missileObj[2].drawMissile()

		pyxel.blt(self.x, self.y, 1, 160, 200, 96, 56, gcommon.TP_COLOR)

	def checkShotCollision(self, shot):
		ret = super(Boss4, self).checkShotCollision(shot)
		if ret:
			enemy.Particle1.appendShotCenter(shot)
		return ret

	def broken(self):
		self.remove()
		enemy.removeEnemyShot()
		gcommon.ObjMgr.objs.append(Boss3Explosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
		gcommon.score += self.score
		gcommon.sound(gcommon.SOUND_LARGE_EXP)
		enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
		gcommon.ObjMgr.objs.append(enemy.Delay(enemy.StageClear, [0,0,4], 240))


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


class BossFactoryBeam1(enemy.EnemyBase):
	def __init__(self, x, y, rad):
		super(BossFactoryBeam1, self).__init__()
		self.x = x
		self.y = y
		self.rad = rad
		self.left = -2
		self.top = -2
		self.right = 2
		self.bottom = 2
		self.hp = 0
		self.layer = gcommon.C_LAYER_E_SHOT
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False
		self.dx = math.cos(self.rad) * 3
		self.dy = math.sin(self.rad) * 3

	def update(self):
		self.x += self.dx
		self.y += self.dy
		if self.x < -20 or self.x > 276:
			self.remove()
		elif self.y < -20 or self.y > gcommon.SCREEN_MAX_Y + 20:
			self.remove()

	def draw(self):
		if self.cnt & 2 == 0:
			pyxel.line(self.x -self.dx * 2, self.y -self.dy * 2, self.x + self.dx * 2, self.y + self.dy * 2, 7)
		else:
			pyxel.line(self.x -self.dx * 2, self.y -self.dy * 2, self.x + self.dx * 2, self.y + self.dy * 2, 10)

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
		self.hp = 2000
		self.score = 10000
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
		self.rad += self.omega
		if self.rad >= math.pi*2:
			self.rad -= math.pi*2
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
						gcommon.ObjMgr.objs.append(
							enemy.Particle1(self.x +39.5, self.y +88, -math.pi/4 -math.pi/4*i))
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
							enemy.Particle1(self.x +39.5, self.y +88, -math.pi/4 -math.pi/4*i))
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
								BossFactoryBeam1(self.x +39.5, self.y + 39.5, rad))
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
				if self.cnt % 4 == 0 and self.cnt <= 30:
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
					self.setState(1)
				elif l < 50:
					self.speed -= 0.25
					if self.speed < 0.5:
						self.speed = 0.5

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
		gcommon.ObjMgr.objs.append(Boss3Explosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
		gcommon.score += self.score
		gcommon.sound(gcommon.SOUND_LARGE_EXP)
		enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
		gcommon.ObjMgr.objs.append(enemy.Delay(enemy.StageClear, [0,0,5], 240))




class MiddleBoss1(enemy.EnemyBase):
	def __init__(self, t):
		super(MiddleBoss1, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.left = 40
		self.top = 24
		self.right = 105
		self.bottom = 71
		self.hp = 700
		self.layer = gcommon.C_LAYER_SKY
		self.ground = False
		self.score = 1000
		self.exptype = gcommon.C_EXPTYPE_GRD_M
		self.dx = 0
		self.dy = 0
		self.moveState = 0
		self.moveCnt = 0
		self.moveCycle = 0

	def update(self):
		if self.state == 0:
			self.x -= 2
			if self.x <= 160:
				self.nextState()
		elif self.state == 1:
			if self.moveCycle & 2 == 0:
				if self.cnt % 40 == 0:
					if self.cnt % 80 == 0:
						for i in range(5):
							enemy.enemy_shot_offset(self.x +43, self.y +47, 3, 0, -4 + i * 2)
					else:
						for i in range(6):
							enemy.enemy_shot_offset(self.x +43, self.y +47, 3, 0, -6 + i * 2)
			else:
				if self.cnt % 30 == 0:
					if self.cnt % 70 == 0:
						for i in range(5):
							enemy.enemy_shot_offset(self.x +43, self.y +47, 3, 0, -4 + i * 2)
					else:
						for i in range(6):
							enemy.enemy_shot_offset(self.x +43, self.y +47, 3, 0, -6 + i * 2)
			if self.moveState == 0:
				# 上に移動
				self.y += self.dy
				if self.y < 40:
					self.dy += 0.05
					if self.dy >= 0.0:
						self.shotAll()
						self.dy = 0.05
						self.moveState = 1
						self.moveCnt = 0
				elif self.dy > -2.0:
					self.dy -= 0.05
			elif self.moveState == 1:
				# 待ち
				self.moveCnt += 1
				if self.moveCnt >= 20:
					self.moveState = 2
			elif self.moveState == 2:
				# 下に移動
				self.y += self.dy
				if self.y > 60:
					self.dy -= 0.05
					if self.dy <= 0.0:
						self.shotAll()
						self.dy = -0.05
						self.moveState = 3
						self.moveCnt = 0
				elif self.dy < 2.0:
					self.dy += 0.05			
			elif self.moveState == 3:
				# 待ち
				self.moveCnt += 1
				if self.moveCnt >= 20:
					self.moveState = 0
					self.moveCycle += 1
					if self.moveCycle >= 5:
						self.moveState = 4
			elif self.moveState == 4:
				# 上に移動
				self.y += self.dy
				if self.y < 70:
					self.dy += 0.05
					if self.dy >= 0.0:
						self.shotAll()
						self.dy = 0.05
						self.state = 2
				elif self.dy > -2.0:
					self.dy -= 0.05
		elif self.state == 2:
			self.x += self.dx
			if self.x <= -88:
				self.remove()
			elif self.dx >= -3:
				self.dx -= 0.05

	def shotAll(self):
		gcommon.ObjMgr.addObj(MiddleBoss1Laser(self.x +39, self.y +7))
		gcommon.ObjMgr.addObj(MiddleBoss1Laser(self.x +24, self.y +20))
		gcommon.ObjMgr.addObj(MiddleBoss1Laser(self.x, self.y +33))
		gcommon.ObjMgr.addObj(MiddleBoss1Laser(self.x, self.y +62))
		gcommon.ObjMgr.addObj(MiddleBoss1Laser(self.x +24, self.y +75))
		gcommon.ObjMgr.addObj(MiddleBoss1Laser(self.x +39, self.y +88))

	def draw(self):
		pyxel.blt(self.x,self.y, 2, 0, 80, 88, 96, 3)

	def broken(self):
		super(MiddleBoss1, self).broken()
		if gcommon.game_timer < 1940:
			gcommon.game_timer = 1940

class MiddleBoss1Laser(enemy.EnemyBase):
	def __init__(self, x, y):
		super(MiddleBoss1Laser, self).__init__()
		self.x = x
		self.y = y
		self.speed = 4
		self.left = 2
		self.top = 0
		self.right = 13
		self.bottom = 3
		self.layer = gcommon.C_LAYER_SKY
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False

	def update(self):
		self.x -= self.speed
		if self.x <= -16:
			self.remove()
	
	def draw(self):
		pyxel.blt(self.x, self.y, 2, 184, 0, 16, 4, gcommon.TP_COLOR)

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
	initHp = 300		# 2000
	hp2 = 200			# 1900
	hp3 = 100			# 1700
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
		self.score = 1000
		self.exptype = gcommon.C_EXPTYPE_GRD_BOSS
		# 破壊状態
		self.brokenState = 0
		self.coreBrightState = 0
		self.coreBrightness = 0
		self.shotType = 1
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
				n = self.cnt & 3
				if n == 0:
					enemy.ContinuousShot.create(self.x + 38, self.y +24, self.shotType, 5, 5, 4)
				elif n == 1:
					enemy.ContinuousShot.create(self.x + 66, self.y +128+15, self.shotType, 5, 5, 4)
				elif n == 2:
					enemy.ContinuousShot.create(self.x + 66, self.y +49, self.shotType, 5, 5, 4)
				elif n == 3:
					enemy.ContinuousShot.create(self.x + 38, self.y +128+40, self.shotType, 5, 5, 4)
				self.shotType = 1 + (self.shotType + 1) % 3
			if self.cnt> 100:
				self.nextState()
		
		elif self.state == 3:
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
			# if self.cnt % 12 == 0 and self.cnt <= 70:
			# 	for i in range(4):
			# 		pos = BossLast1.launcherTable[i]
			# 		obj = BossFactoryShot1(self.x +pos[0] -12, self.y +pos[1]-12)
			# 		obj.imageX = 0
			# 		obj.imageY = 192
			# 		gcommon.ObjMgr.objs.append(obj)
			if self.cnt % 40 == 1:
				gcommon.ObjMgr.objs.append(BossLastBattery1(156, 192, -1))
			elif self.cnt % 40 == 21:
				gcommon.ObjMgr.objs.append(BossLastBattery1(156, -16, 1))
			#elif self.cnt % 30 == 14:
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
			if self.cnt % 8 == 0:
				n = BossLast1.table8[int(self.cnt /8) & 7]
				gcommon.ObjMgr.addObj(BossLastDiamondShot(self.x +32+16+32, self.y +64+16+16+8, 24 -n*2))
				gcommon.ObjMgr.addObj(BossLastDiamondShot(self.x +32+16+32, self.y +64+16+16-8, 40 +n*2))
			if self.cnt > 30:
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
			if self.cnt & 3 == 0:
				gcommon.ObjMgr.addObj(BossLastFallShotGroup(self.x +32+16+32, self.y +64+16+16,
					math.pi + math.pi * (self.random.rand() % 100 -50)/120, 
					(self.random.rand() % 120 -60)/800, 5))
			if self.cnt > 120:
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
		if ret:
			rad = math.atan2(shot.dy, shot.dx)
			enemy.Particle1.appendCenter(shot, rad)
		if self.mode == 0:
			if self.brokenState == 0 and self.hp < BossLast1.hp2:
				# 初期状態
				self.brokenState = 1
				enemy.create_explosion(self.x +32+32, self.y +64+16+16, gcommon.C_LAYER_GRD, gcommon.C_EXPTYPE_GRD_M)
			elif self.brokenState == 1 and self.hp < BossLast1.hp3:
				# 先端が欠けた状態
				self.brokenState = 2
				self.mode = 1
				self.setState(0)
				self.removeAllShot()
				enemy.create_explosion(self.x +32+32, self.y +64+16+16, gcommon.C_LAYER_GRD, gcommon.C_EXPTYPE_GRD_M)
				enemy.Splash.append(self.x +32+32+24, self.y +64+16+16, gcommon.C_LAYER_EXP_SKY)
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
		self.hitCheck = True
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
				if self.size >= 2.0:
					self.size = 2.0
				if self.cnt > 45:
					self.nextState()
			elif self.state == 1:
				if self.cnt > 30:
					self.nextState()
			elif self.state == 2:
				self.rad -= self.omega
				if self.rad < (math.pi -self.angle):
					self.nextState()
			elif self.state == 3:
				self.rad += self.omega
				if self.rad > (math.pi +self.angle):
					self.nextState()
			elif self.state == 4:
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
				if self.size >= 2.0:
					self.size = 2.0
				if self.cnt > 45:
					self.nextState()
			elif self.state == 1:
				if self.cnt > 30:
					self.nextState()
			elif self.state == 2:
				self.rad += self.omega
				if self.rad > (math.pi +self.angle):
					self.nextState()
			elif self.state == 3:
				self.rad -= self.omega
				if self.rad < (math.pi -self.angle):
					self.nextState()
			elif self.state == 4:
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
		self.hp = 2000
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

		if self.cnt & 15 == 15:
			enemy.Particle1.append(self.x, self.y, gcommon.atan_table[self.dr] + math.pi)

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
		self.hp = 1000
		self.score = 10000
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
			if self.cnt % (self.random.rand() % 7 +3) == 0:
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
			if self.cnt % 5 == 0:
				gcommon.ObjMgr.addObj(BossFactoryBeam1(self.x +math.cos(workAngle)* 24, self.y +math.sin(workAngle) * 24, workAngle))
				gcommon.ObjMgr.addObj(BossFactoryBeam1(self.x -math.cos(workAngle)* 24, self.y -math.sin(workAngle) * 24, workAngle + math.pi))
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

	def checkShotCollision(self, shot):
		ret = super(BossLast1Core, self).checkShotCollision(shot)
		if ret:
			rad = math.atan2(shot.dy, shot.dx)
			enemy.Particle1.appendCenter(shot, rad)

	def broken(self):
		self.setState(100)
		self.shotHitCheck = False
		enemy.removeEnemyShot()
		gcommon.ObjMgr.objs.append(Boss3Explosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
		gcommon.score += self.score
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
		self.radOffset += math.pi * 0.05
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
			if self.cnt < 120:
				enemy.create_explosion(32 +random.randrange(64), random.randrange(gcommon.SCREEN_MAX_Y), gcommon.C_LAYER_GRD, gcommon.C_EXPTYPE_SKY_M)
			else:
				# サウンドなし
				gcommon.ObjMgr.addObj(enemy.Explosion(32 +random.randrange(64), random.randrange(gcommon.SCREEN_MAX_Y), gcommon.C_LAYER_GRD, gcommon.C_EXPTYPE_SKY_M))

