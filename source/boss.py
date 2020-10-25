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

	def update(self):
		self.x = self.parentObj.x + self.offsetX
		self.y = self.parentObj.y + self.offsetY
		if self.mode == 1:
			if self.state ==1:
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

class Boss2Cell(enemy.EnemyBase):
	def __init__(self, parentObj, x, y, firstDr):
		super(Boss2Cell, self).__init__()
		self.x = x
		self.y = y
		self.parentObj = parentObj
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
			del self.cells[-1]
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
				#pyxel.play(1, 5)
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
				gcommon.ObjMgr.addObj(Boss3Shot(self.x, self.body.y+12, 2))
				gcommon.ObjMgr.addObj(Boss3Shot(self.x, self.body.y+37, 2))
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
				enemy.enemy_shot(self.x+20, self.y+27, 2, 0)
				enemy.enemy_shot(self.x+20, self.y+160-27, 2, 0)
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
				gcommon.ObjMgr.addObj(Boss3Shot(self.x, self.body.y+12, 2))
				gcommon.ObjMgr.addObj(Boss3Shot(self.x, self.body.y+37, 2))
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
		if gcommon.map_x >= 6800:
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
		gcommon.ObjMgr.objs.append(Boss3Explosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
		gcommon.score += self.score
		self.remove()
		gcommon.sound(gcommon.SOUND_LARGE_EXP)
		enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
		gcommon.ObjMgr.objs.append(enemy.Delay(enemy.StageClear, [0,0,4], 240))


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
	[10, 0],
	[1, 25],
	[15, 15]
]
# clr = 10 黄色の上
bossFactoryFinA2 = [
	[10, 0],
	[16, 10],
	[23, 0]
]
# clr = 4  茶色の左下
bossFactoryFinA3 = [
	[1, 26],
	[7, 30],
	[10, 21]
]
# clr = 4  茶色の真ん中
bossFactoryFinA4 = [
	[7, 30],
	[26, 30],
	[16.5, 7]
]
# clr = 4  茶色の右下
bossFactoryFinA5 = [
	[26, 30],
	[21, 21],
	[32, 26]
]
# clr = 4  茶色の右横
bossFactoryFinA6 = [
	[32, 26],
	[15, 12],
	[23, 0]
]
# clr = 9  オレンジの正面
bossFactoryFinA7 = [
	[12, 3],
	[5, 23],
	[8, 25],
	[24, 25],
	[28, 23],
	[21, 3]
]

class BossFactory(enemy.EnemyBase):
	def __init__(self, t):
		super(BossFactory, self).__init__()
		self.x = 256
		self.y = 60
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
		#self.xpoints1 = []
		#self.xpoints2 = []
		self.rad = 0.0
		self.distance = 22.0
		self.subState = 0
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

	def setSubState(self, subState):
		self.subCnt = 0
		self.subState = subState

	def update(self):
		self.rad += math.pi/64
		if self.rad >= math.pi*2:
			self.rad -= math.pi*2
		if self.state == 0:
			self.x -= gcommon.cur_scroll_x
			if self.x <= 152:
				self.nextState()
		elif self.state == 1:
			if self.subState == 0:
				self.subCnt += 1
				if self.subCnt == 30:
					self.setSubState(1)
			elif self.subState == 1:
				# 開く
				self.distance += 0.5
				if self.distance > 38:
					self.setSubState(2)
			elif self.subState == 2:
				# 開いている（攻撃）
				self.subCnt += 1
				if self.subCnt % 8 == 0:
					if self.finMode == 0:
						for i in range(4):
							enemy.enemy_shot(
								self.x +39.5 +math.cos(self.rad + math.pi/2 * i) * 32,
								self.y +39.5 +math.sin(self.rad + math.pi/2 * i) * 32,
								4, 0)
					else:
						for i in range(4):
							enemy.enemy_shot(
								self.x +39.5 +math.cos(self.rad + math.pi/4 + math.pi/2 * i) * 32,
								self.y +39.5 +math.sin(self.rad + math.pi/4 + math.pi/2 * i) * 32,
								3, 1)
				if self.subCnt == 30:
					self.setSubState(3)
			elif self.subState == 3:
				# 閉まる
				self.distance -= 0.5
				if self.distance < 22:
					self.distance = 22.0
					self.setSubState(0)
					self.finMode = (self.finMode + 1) & 1
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
		pyxel.blt(self.x, self.y, 2, 64, 48, 80, 80, gcommon.TP_COLOR)

		# 中心の玉
		for i in range(4):
			pyxel.blt(
				self.x +39.5 +math.cos(self.rad + math.pi/2 * i) * 14 -7.5,
				self.y +39.5 +math.sin(self.rad + math.pi/2 * i) * 14 -7.5, 
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

