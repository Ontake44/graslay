import pyxel
import math
import random
import gcommon
import enemy
import boss
from objMgr import ObjMgr
from gameSession import GameSession
from audio import BGM

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
	shotCycles = (70, 50, 30)
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
		self.hp = gcommon.HP_UNBREAKABLE
		self.cells = []		# 相対座標
		self.mode = 0
		self.subDr = 0
		self.state = 0		# 0:縮小状態 1,2:モードで動作中
		self.shotCycle = __class__.shotCycles[GameSession.difficulty]
		for dummy in range(0, count):
			self.cells.append([0, 0])
		# 触手セルの当たり判定範囲
		self.cellRect = gcommon.Rect.create(2,2,13,13)

	def setMode(self, mode):
		self.mode = mode
		self.state = 1
		self.cnt = 0
		#print("Feeler mode:" +str(mode))

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
			if self.cnt % self.shotCycle == 0:
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
		return hit

	# def doShotCollision(self, shot):
	# 	self.hp -= shot.shotPower
	# 	if self.hp <= 0:
	# 		self.broken()
	# 		return True
	# 	else:
	# 		self.hit = True
	# 		return False

	# 自機と敵との当たり判定
	def checkMyShipCollision(self):
		if gcommon.check_collision(self, ObjMgr.myShip):
			return True
		else:
			# 触手部の当たり判定
			for pos in self.cells:
				x = self.x +pos[0]
				y = self.y +pos[1]
				if gcommon.check_collision2(x, y, self.cellRect, ObjMgr.myShip):
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
			else:
				pos = self.cells[len(self.cells)-1]
				self.x = pos[0]
				self.y = pos[1]

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
	[0, 0, 0, 240, 1],			# 触手伸ばす攻撃
#	[4, 0, 0.25, 130, 0],		# 下移動
	[100, 0.0, 0.0, 1, 0],		# インデックス移動
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
		self.hp = 999999		# 破壊できない
		self.layer = gcommon.C_LAYER_GRD
		self.ground = True
		self.score = 7000
		self.subcnt = 0
		self.dx = 0.5
		self.dy = 0
		self.hitcolor1 = 3
		self.hitcolor2 = 7
		self.tblIndex = 0
		self.cycleCount = 0
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
		ObjMgr.addObj(self.feelers[0])
		ObjMgr.addObj(self.feelers[1])
		ObjMgr.addObj(self.feelers[2])
		ObjMgr.addObj(self.feelers[3])
		self.bossCells = []
		#self.upperBase = Boss2Base(self,0)
		#self.lowerBase = Boss2Base(self,1)
		#ObjMgr.addObj(self.upperBase)
		#ObjMgr.addObj(self.lowerBase)
		self.bossBase = Boss2Base2(self)
		ObjMgr.addObj(self.bossBase)

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
				self.hp = boss.BOSS_2_HP		# ここでHPを入れなおす
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
				# 指定インデックスに移動
				self.tblIndex = boss2tbl[self.tblIndex][3]
				self.cycleCount += 1
				self.subcnt = 0
			
			attack = boss2tbl[self.tblIndex][4]
			if attack == 1:
				# 触手伸ばす攻撃
				if self.cycleCount & 1 == 0:
					if self.subcnt == 1:
						self.bossCells.append(ObjMgr.addObj(Boss2Cell(self, self.x +16, self.y+29, 24)))
						BGM.sound(gcommon.SOUND_FEELER_GROW)
					elif self.subcnt == 20:
						self.bossCells.append(ObjMgr.addObj(Boss2Cell(self, self.x +16, self.y+8, 40)))
					elif self.subcnt == 40:
						self.bossCells.append(ObjMgr.addObj(Boss2Cell(self, self.x +50, self.y+8, 24)))
					elif self.subcnt == 60:
						self.bossCells.append(ObjMgr.addObj(Boss2Cell(self, self.x +50, self.y+29, 40)))
				else:
					if self.subcnt == 1:
						self.bossCells.append(ObjMgr.addObj(Boss2Cell(self, self.x +14, self.y+16, 32)))
						BGM.sound(gcommon.SOUND_FEELER_GROW)
					elif self.subcnt == 15:
						self.bossCells.append(ObjMgr.addObj(Boss2Cell(self, self.x +33, self.y+5, 20)))
					elif self.subcnt == 30:
						self.bossCells.append(ObjMgr.addObj(Boss2Cell(self, self.x +31, self.y+33, 40)))
					#elif self.subcnt == 45:
					#	ObjMgr.addObj(Boss2Cell(self, self.x +48, self.y+6, 24))
					#elif self.subcnt == 60:
					#	ObjMgr.addObj(Boss2Cell(self, self.x +48, self.y+33, 38))
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
		for feeler in self.feelers:
			feeler.remove()
		for cell in self.bossCells:
			if cell.removeFlag == False:
				cell.remove()
		self.remove()
		enemy.removeEnemyShot()
		ObjMgr.objs.append(boss.BossExplosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
		GameSession.addScore(self.score)
		BGM.sound(gcommon.SOUND_LARGE_EXP)
		enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
		ObjMgr.objs.append(enemy.Delay(enemy.StageClear, [0,0,"2A"], 240))

