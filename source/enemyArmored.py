

from objMgr import ObjMgr
import pyxel
import math
import random
import gcommon
import enemy
import myShip
from enemy import EnemyBase, enemy_shot
from enemy import CountMover

class Armored1(EnemyBase):
	srcXTable = (0, 40, 80, 120)
	def __init__(self, t):
		super(Armored1, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.mover = enemy.CountMover(self, t[4], False)
		self.left = 12
		self.top = 3
		self.right = 27
		self.bottom = 32
		self.layer = gcommon.C_LAYER_SKY
		self.exptype = gcommon.C_EXPTYPE_SKY_M
		self.hp = 50
		self.hitcolor1 = 5
		self.hitcolor2 = 12
		self.dx = -1.5
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.score = 500

	def update(self):
		#	if self.cnt % 15 == 1:
		#		enemy.enemy_shot_dr(self.x, self.y +12, 4, 0, 32)
		self.mover.update()
		if abs(self.mover.dy) > 0.01:
			if self.cnt % 12 == 1:
				enemy.enemy_shot_dr(self.x, self.y +12, 4, 0, 32)


	def draw(self):
		n = self.cnt % 3
		if n != 2:
			pyxel.blt(self.x +28, self.y, 2, n * 16, 224, 16, 24, 2)

		spNo = 0
		if abs(self.mover.dy) > 0.01:
			spNo = 2
		elif abs(self.mover.dx) < 1.0:
			spNo = 1
		pyxel.blt(self.x, self.y, 2, __class__.srcXTable[spNo], 184, 40, 40, 2)


class Walker2(EnemyBase):
	# position : 1:下  -1：上
	def __init__(self, parent, x, y, moveTable, position):
		super(__class__, self).__init__()
		self.parent = parent
		self.x = x
		self.y = y
		self.mover = enemy.CountMover(self, moveTable, loopFlag=False, selfMove=False)
		self.position = position
		self.left = 4
		self.right = 12
		if self.position == 1:
			self.top = 3
			self.bottom = 15
		else:
			self.top = 0
			self.bottom = 12
		self.layer = gcommon.C_LAYER_SKY
		self.exptype = gcommon.C_EXPTYPE_SKY_S
		self.hp = 50
		self.hitcolor1 = 5
		self.hitcolor2 = 12
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.score = 200
		self.fdx = 1

	def update(self):
		self.mover.update()
		if self.mover.isEnd:
			self.remove()
			return
		if self.mover.mode == CountMover.STOP:
			if self.mover.cnt == 20:
				enemy_shot(self.x + (self.right -self.left)/2, self.y + (self.bottom -self.top)/2, 2, 0)
		if self.mover.dx < 0.0:
			self.fdx = 1
		elif self.mover.dx > 0.0:
			self.fdx = -1
		self.x = self.parent.x + self.mover.x
		self.y = self.parent.y + self.mover.y
		#gcommon.debugPrint(str(self.x) + " " + str(self.y))

	def draw(self):
		n = 0
		if abs(self.mover.dx) > 0.1:
			n = 1 + (self.cnt>>2) & 3
		pyxel.blt(self.x, self.y, 1, 56 + n * 16, 208, 16 * self.fdx, 16 * self.position, 0)



class Ducker1(EnemyBase):
	def __init__(self, t):
		super(__class__, self).__init__()
		self.x = -16
		self.position = t[2]		# 1:下 -1:上
		self.y = self.getInitialY(self.position)
		#gcommon.debugPrint("inity=" +str(self.y) +" " + str(gcommon.game_timer))
		self.left = -6
		self.right = 6
		self.top = -6
		self.bottom = 6
		self.layer = gcommon.C_LAYER_GRD
		self.exptype = gcommon.C_EXPTYPE_GRD_S
		self.hp = 1
		self.hitcolor1 = 5
		self.hitcolor2 = 12
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.ground = True
		self.score = 200
		self.direction = 1
		self.cycleCount = 0
		self.upDownFlag = False

	def getInitialY(self, pos):
		y = 96
		if pos == 1:
			while(True):
				pos = gcommon.getMapPos(-16, y)
				#gcommon.debugPrint("mx=" + str(pos[0]) + " my=" +str(pos[1]))
				n = gcommon.getMapData(-16, y)
				if n == 0:
					y += 8
				else:
					break
			return y -8 - (int(gcommon.map_y) & 7)
		else:
			while(True):
				n = gcommon.getMapData(-16, y)
				if n == 0:
					y -= 8
				else:
					break
			return y +8 - (int(gcommon.map_y) & 7)

	def move(self):
		self.dx = 0
		# 移動
		if self.position == 1:
			# 下位置
			n = gcommon.getMapData(self.x +8*self.direction, self.y+7)
			if n != 0:
				self.upDownFlag = True
				self.y -= 4
			else:
				n = gcommon.getMapData(self.x +16*self.direction, self.y+7)
				if n != 0:
					self.upDownFlag = True
					self.dx = 2 *self.direction
					self.y -= 4
				else:
					n = gcommon.getMapData(self.x, self.y +8)
					if n == 0:
						# 下が空間
						self.upDownFlag = True
						self.dx = 2 *self.direction
						self.y += 2
					else:
						self.dx = 2 *self.direction
		else:
			# 上位置
			n = gcommon.getMapData(self.x +8*self.direction, self.y-8)
			if n != 0:
				self.upDownFlag = True
				self.y += 4
			else:
				n = gcommon.getMapData(self.x +16*self.direction, self.y-8)
				if n != 0:
					self.upDownFlag = True
					self.dx = 2 *self.direction
					self.y += 4
				else:
					n = gcommon.getMapData(self.x, self.y -9)
					if n == 0:
						# 上が空間
						self.upDownFlag = True
						self.dx = 2 *self.direction
						self.y -= 2
					else:
						self.dx = 2 *self.direction
		self.x += self.dx

	def update(self):
		if self.state == 0:
			self.upDownFlag = False
			self.move()
			if self.upDownFlag == False:
				if ObjMgr.myShip.x + myShip.MyShipBase.CENTER_X >= 128:
					# 画面右側
					l = abs(ObjMgr.myShip.y + myShip.MyShipBase.CENTER_Y - self.y)
					if self.x > ObjMgr.myShip.x + myShip.MyShipBase.CENTER_X - l:
						self.nextState()
				else:
					# 画面左側
					l = abs(ObjMgr.myShip.y + myShip.MyShipBase.CENTER_Y - self.y)
					if self.x > ObjMgr.myShip.x + myShip.MyShipBase.CENTER_X + l +40:
						self.nextState()
		elif self.state == 1:
			self.dx = 0
			if self.cnt == 20:
				enemy.enemy_shot(self.x, self.y, 2, 0)
			elif self.cnt >= 60:
				self.cycleCount += 1
				if self.cycleCount > 3:
					# 撤退
					self.direction = -1
					self.nextState()
				else:
					#self.direction = -1 * self.direction
					self.setState(0)
		elif self.state == 2:
			# 撤退
			self.move()
		if self.x > 256 or self.x < -32:
			self.remove()
			#gcommon.debugPrint("cnt=" + str(self.frameCount) + " " + str(self.y))
			return

	def draw(self):
		if self.dx == 0:
			fx = 1 if ObjMgr.myShip.x + myShip.MyShipBase.CENTER_X > self.x else -1
			pyxel.blt(self.x -8, self.y-8, 1, 64, 112, 16 * fx, 16 * self.position, 3)
		else:
			pyxel.blt(self.x -8, self.y-8, 1, ((self.cnt>>2) & 3) *16, 112, 16 *self.direction, 16 * self.position, 3)

class CylinderCrab2(EnemyBase):
	STOP = 0,
	MOVE_LEFT = 1,
	MOVE_RIGHT = 2,
	moveTable = [
		[450, MOVE_LEFT],
		[850, MOVE_RIGHT],
		[180, MOVE_LEFT],
		[530, MOVE_RIGHT],
		[900, MOVE_LEFT],
	]
	moveTableXX = [
		[400, MOVE_LEFT],
		[800, MOVE_RIGHT],
		[180, MOVE_LEFT],
		[480, MOVE_RIGHT],
		[900, MOVE_LEFT],
	]
	# state
	#  0: 
	def __init__(self, t):
		super(__class__, self).__init__()
		self.x = 256+96
		self.y = 10*8
		self.left = -6
		self.right = 6
		self.top = -6
		self.bottom = 6
		self.layer = gcommon.C_LAYER_SKY
		self.hp = 50000
		self.hitCheck = True
		self.shotHitCheck = True
		self.enemyShotCollision = False
		self.ground = True
		self.score = 200
		self.foregroundLegX = -6 *8
		# 上|0 1|
		# 下|2 3|
		self.legXOffsetArray = [-16, 80, -16, 80]
		self.foregroundLegYArray = [5 * 8] * 4
		self.backgroundLegX = 0
		self.backgroundLegYArray = [5 * 8] * 4

		# self.foregroundLegX = 5 * 8
		# self.backgroundLegX = 0
		self.moveIndex = 0
		self.moveCnt = 0
		self.dx = 1
		self.speed = 2.0

	def update(self):
		if self.moveIndex >= len(__class__.moveTable):
			pass
		else:
			t = __class__.moveTable[self.moveIndex]
			cmd = t[1]
			if cmd == __class__.STOP:
				# 停止
				pass
			elif cmd == __class__.MOVE_LEFT:
				# 左に移動
				self.dx = 1
			elif cmd == __class__.MOVE_RIGHT:
				# 右に移動
				self.dx = -1
			self.moveCnt += 1
			if self.moveCnt >= t[0]:
				self.moveIndex +=1
				self.moveCnt = 0
		if self.state == 0:
			# ボディ部の移動
			self.x -= self.speed * self.dx
			self.foregroundLegX += self.speed * self.dx
			self.backgroundLegX += self.speed * self.dx
			if (self.dx == 1 and self.foregroundLegX >= 0) or \
			  (self.dx == -1 and self.foregroundLegX <= 0):
				self.nextState()
		elif self.state == 1:
			# 奥側の脚を縮める
			nextFlag = 0
			for i in range(4):
				if self.backgroundLegYArray[i] > 0:
					self.backgroundLegYArray[i] -= 1
				else:
					nextFlag |= (1<<i)
			# 4ビット全部が立ったら
			if nextFlag == 15:
				self.nextState()
		elif self.state == 2:
			# 奥側の脚を進める
			self.backgroundLegX -= self.speed * self.dx
			if (self.dx == 1 and self.backgroundLegX <= -6 * 8) or \
				(self.dx == -1 and self.backgroundLegX >= 6 * 8):
				self.nextState()
		elif self.state == 3:
			# 奥側の脚を伸ばす
			nextFlag = 0
			for i in range(4):
				x = self.x + self.backgroundLegX +self.legXOffsetArray[i] +8
				if i in (0, 1):
					y = self.y -32 -self.backgroundLegYArray[i] -1
				else:
					y = self.y +64 +self.backgroundLegYArray[i]
				if gcommon.isMapFreePos(x, y):
					self.backgroundLegYArray[i] += 1
				else:
					nextFlag |= (1<<i)
			# 4ビット全部が立ったら
			if nextFlag == 15:
				self.nextState()
		elif self.state == 4:
			# ボディ部の移動
			self.x -= self.speed * self.dx
			self.foregroundLegX += self.speed * self.dx
			self.backgroundLegX += self.speed * self.dx
			if (self.dx == 1 and self.backgroundLegX >= 0) or \
				(self.dx == -1 and self.backgroundLegX <= 0):
				self.nextState()
		elif self.state == 5:
			# 手前の脚を上げる
			nextFlag = 0
			for i in range(4):
				if self.foregroundLegYArray[i] > 0:
					self.foregroundLegYArray[i] -= 1
				else:
					nextFlag |= (1<<i)
			# 4ビット全部が立ったら
			if nextFlag == 15:
				self.nextState()
			# for i in range(4):
			# 	self.foregroundLegYArray[i] -= 1
			# 	if self.foregroundLegYArray[i] == 0:
			# 		self.nextState()
		elif self.state == 6:
			# 手前の脚を進める
			self.foregroundLegX -= self.speed * self.dx
			if (self.dx == 1 and self.foregroundLegX <= -6 * 8) or \
				(self.dx == -1 and self.foregroundLegX >= 6 * 8):
				self.nextState()
		elif self.state == 7:
			# 手前の脚を下げる
			nextFlag = 0
			for i in range(4):
				x = self.x + self.foregroundLegX +self.legXOffsetArray[i] +8
				if i in (0, 1):
					y = self.y -32 -self.foregroundLegYArray[i] -1
				else:
					y = self.y +64 +self.foregroundLegYArray[i]
				if gcommon.isMapFreePos(x, y):
					self.foregroundLegYArray[i] += 1
				else:
					nextFlag |= (1<<i)
			# 4ビット全部が立ったら
			if nextFlag == 15:
				self.setState(0)
			# for i in range(4):
			# 	self.foregroundLegYArray[i] += 1
			# 	if self.foregroundLegYArray[i] == 5 * 8:
			# 		self.setState(0)
		# コリジョン更新
		rects = []
		rects.append(gcommon.Rect.create(5, 2, 79-5, 31-2))
		# バー
		rects.append(gcommon.Rect.createWH(self.backgroundLegX -16, -8, 112, 8))
		rects.append(gcommon.Rect.createWH(self.backgroundLegX -16, +32, 112, 8))
		rects.append(gcommon.Rect.createWH(self.foregroundLegX -16, -8, 112, 8))
		rects.append(gcommon.Rect.createWH(self.foregroundLegX -16, +32, 112, 8))
		# シリンダー
		rects.append(gcommon.Rect.createWH(self.backgroundLegX -16+4, -32-self.backgroundLegYArray[0],  8, self.backgroundLegYArray[0] +24))
		rects.append(gcommon.Rect.createWH(self.backgroundLegX +80+4, -32-self.backgroundLegYArray[1],  8, self.backgroundLegYArray[1] +24))
		rects.append(gcommon.Rect.createWH(self.backgroundLegX -16+4, 40,  8, self.backgroundLegYArray[2] +24))
		rects.append(gcommon.Rect.createWH(self.backgroundLegX +80+4, 40,  8, self.backgroundLegYArray[3] +24))
		rects.append(gcommon.Rect.createWH(self.foregroundLegX -16+4, -32-self.foregroundLegYArray[0],  8, self.foregroundLegYArray[0] +24))
		rects.append(gcommon.Rect.createWH(self.foregroundLegX +80+4, -32-self.foregroundLegYArray[1],  8, self.foregroundLegYArray[1] +24))
		rects.append(gcommon.Rect.createWH(self.foregroundLegX -16+4, 40,  8, self.foregroundLegYArray[2] +24))
		rects.append(gcommon.Rect.createWH(self.foregroundLegX +80+4, 40,  8, self.foregroundLegYArray[3] +24))
		self.collisionRects = rects
		if self.x < -160:
			self.remove()

	def draw(self):
		# ボディ
		pyxel.blt(self.x, self.y, 2, 0, 112, 80, 32, 3)

		# 奥側シリンダー
		self.drawLowerBar(self.backgroundLegX, True)
		self.drawUpperBar(self.backgroundLegX, True)
		#self.drawLegLower2(self.backgroundLegX, self.backgroundLegYArray[0], True)
		self.drawLegUpper(self.backgroundLegX, self.backgroundLegYArray[0], -16)
		self.drawLegUpper(self.backgroundLegX, self.backgroundLegYArray[1], 80)
		self.drawLegLower(self.backgroundLegX, self.backgroundLegYArray[2], -16)
		self.drawLegLower(self.backgroundLegX, self.backgroundLegYArray[3], 80)
		#self.drawLegUpper2(self.backgroundLegX, self.backgroundLegYArray[0], True)

		# 手前シリンダー
		self.drawLowerBar(self.foregroundLegX, False)
		self.drawUpperBar(self.foregroundLegX, False)
		#self.drawLegLower2(self.foregroundLegX, self.foregroundLegYArray[0], False)
		self.drawLegUpper(self.foregroundLegX, self.foregroundLegYArray[0], -16)
		self.drawLegUpper(self.foregroundLegX, self.foregroundLegYArray[1], 80)
		self.drawLegLower(self.foregroundLegX, self.foregroundLegYArray[2], -16)
		self.drawLegLower(self.foregroundLegX, self.foregroundLegYArray[3], 80)

		#self.drawLegUpper2(self.foregroundLegX, self.foregroundLegYArray[0], False)

		## 下側手前シリンダー右
		#pyxel.blt(self.x + self.foregroundLegX -8+8*10, self.y +32, 2, 80, 112, 16, 24, 3)

	def drawLowerBar(self, legX, backSide):
		pyxel.blt(self.x + legX -16, self.y +32, 2, 0, 152 if backSide else 144, 112, 8, 3)

	def drawUpperBar(self, legX, backSide):
		pyxel.blt(self.x + legX -16, self.y -8, 2, 0, 152 if backSide else 144, 112, 8, 3)

	# def drawLegLower2(self, legX, legY, backSide):
	# 	# 下側スライド部
	# 	#pyxel.blt(self.x + legX -16, self.y +32, 2, 0, 152 if backSide else 144, 112, 8, 3)
	# 	self.drawLegLower(legX, legY, -16)
	# 	self.drawLegLower(legX, legY, 80)

	# def drawLegUpper2(self, legX, legY, backSide):
	# 	# 上側スライド部
	# 	#pyxel.blt(self.x + legX -16, self.y -8, 2, 0, 152 if backSide else 144, 112, 8, 3)
	# 	self.drawLegUpper(legX, legY, -16)
	# 	self.drawLegUpper(legX, legY, 80)

	def drawLegLower(self, legX, legY, offsetX):
		# シリンダー
		pyxel.blt(self.x + legX +offsetX, self.y +40+legY, 2, 128, 112, 16, 16, 3)
		pyxel.blt(self.x + legX +offsetX, self.y +40+(legY*0.66), 2, 112, 112, 16, 16, 3)
		pyxel.blt(self.x + legX +offsetX, self.y +40+(legY/3), 2, 96, 112, 16, 16, 3)
		# シリンダー下端
		pyxel.blt(self.x + legX +offsetX, self.y +56+legY, 2, 96, 128, 16, 8, 3)
		# シリンダー上端
		pyxel.blt(self.x + legX +offsetX, self.y +32, 2, 80, 112, 16, 24, 3)

	def drawLegUpper(self, legX, legY, offsetX):
		# シリンダー
		pyxel.blt(self.x + legX +offsetX, self.y -24-legY, 2, 128, 112, 16, 16, 3)
		pyxel.blt(self.x + legX +offsetX, self.y -24-(legY*0.66), 2, 112, 112, 16, 16, 3)
		pyxel.blt(self.x + legX +offsetX, self.y -24-(legY/3), 2, 96, 112, 16, 16, 3)
		# シリンダー上端
		pyxel.blt(self.x + legX +offsetX, self.y -32-legY, 2, 96, 128, 16, -8, 3)
		# シリンダー下端
		pyxel.blt(self.x + legX +offsetX, self.y -24, 2, 80, 112, 16, -24, 3)



