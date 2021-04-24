import pyxel
import math
import random
import sys
import os
import gcommon
import enemy
from gcommon import Pos
from objMgr import ObjMgr
from gameSession import GameSession
from audio import BGM

# 自機
class MyShipBase:
	missileCycles = (10, 10, 20)
	def __init__(self, parent):
		super().__init__()
		self.x = 0
		self.y = 0
		self.parent = parent
		self.sprite = 1
		self.shotMax = 4
		self.missleMax = 2
		self.left = 3
		self.top = 7
		self.right = 10
		self.bottom = 8
		self.collisionRects = None		# List of Rect
		self.cnt = 0
		# 移動をかけた場合にTrue
		self.moveActionFlag = False
		# 1:ゲーム中 2:爆発中 3:復活中 4:無敵中 5:クリア時
		self.sub_scene = 3
		self.shotCounter = 0
		self.missileCounter = 0
		self.prevFlag = False
		self.dx = 0
		self.setStartPosition()
		self.mouseManager = parent.mouseManager
		self.setWeapon(GameSession.weaponSave)

	def update(self):
		if gcommon.sync_map_y != 0:
			gcommon.cur_map_dy = 0
		if self.sub_scene == 1:
			# ゲーム中
			self.actionButtonInput()
		elif self.sub_scene == 2:
			# 爆発中
			if self.cnt > 90:
				# 爆発中を終了
				if GameSession.playerStock == 0:
					#self.sub_scene = 10
					self.setSubScene(10)
					self.cnt = 0
					self.sprite = 1
					self.x = -16
					self.parent.OnPlayerStockOver()
				else:
					GameSession.playerStock -= 1
					#--restart_game()
					#self.sub_scene=3
					self.setSubScene(3)
					self.cnt = 0
					self.sprite = 1
					self.x = -16
		elif self.sub_scene == 3:
			# 復活中
			self.dx = 0
			self.x += 1
			if self.x >= gcommon.MYSHIP_START_X:
				self.cnt = 0
				#self.sub_scene = 4
				self.setSubScene(4)
		elif self.sub_scene == 4:
			# 無敵中
			self.actionButtonInput()
			if self.cnt == 120:
				self.cnt = 0
				self.sub_scene=1
		elif self.sub_scene == 5:	# scene == 5
			# クリア時
			if self.cnt == 0:
				BGM.sound(gcommon.SOUND_AFTER_BURNER)
			if self.x < 256 + 32:
				if self.dx < 8:
					self.dx += 0.25
				self.x += self.dx
		else:	# sub_scene = 10
			# continue確認中
			pass
		self.cnt += 1

	def actionButtonInput(self):
		cx = self.x + (self.right - self.left +1)/2+ 4
		cy = self.y + (self.bottom - self.top +1)/2+ 6
		mouseDx = 0
		mouseDy = 0
		self.moveActionFlag = False
		self.sprite = 0
		dy = 0
		if self.mouseManager.visible:
			if cx < pyxel.mouse_x -2:
				mouseDx = 1
			elif cx > pyxel.mouse_x +2:
				mouseDx = -1
			if cy < pyxel.mouse_y -2:
				mouseDy = 1
			elif cy > pyxel.mouse_y +2:
				mouseDy = -1
		if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT) or mouseDx == -1:
			self.moveActionFlag = True
			self.x = self.x -2
			if self.x < 0:
				self.x = 0
		elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT) or mouseDx == 1:
			self.moveActionFlag = True
			self.x = self.x +2
			self.sprite = 0
			if self.x > 240:
				self.x = 240
		if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP) or mouseDy == -1:
			self.moveActionFlag = True
			self.sprite = 2
			if gcommon.sync_map_y == 1:
				if self.y <= 56:
					gcommon.cur_map_dy = -2
					self.y = 56
				elif self.y < 88:
					gcommon.cur_map_dy = -2 * (88 - self.y)/(88-56)
					self.y -= 2 * (self.y -56)/(88-56)
				else:
					self.y -= 2
			else:
				if self.y >= (2+2):
					dy = -2
				else:
					dy = -(self.y -2)
				self.y += dy
		elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN) or mouseDy == 1:
			self.moveActionFlag = True
			# 縦は192/8 = 24キャラ
			self.sprite = 1
			if gcommon.sync_map_y == 1:
				if self.y >= 136:
					gcommon.cur_map_dy = 2
					self.y = 136
				elif self.y >= 104:
					gcommon.cur_map_dy = 2 * (self.y - 104)/(136-104)
					self.y += 2 * (136 -self.y)/(136-104)
				else:
					self.y += 2
			else:
				if self.y <= (176 -2):
					dy = 2
				else:
					dy = (176 -self.y)
				self.y += dy
		
		if gcommon.game_timer > 30:
			self.executeShot()
			if gcommon.checkOpionKey():
				if GameSession.weaponType == gcommon.WeaponType.TYPE_A:
					self.setWeapon((self.weapon + 1) % 3)
				else:
					self.setWeapon((self.weapon + 1) % 4)
	
	def executeShot(self):
		pass

	def appendShot(self, shotGroup, shot):
		ObjMgr.shots.append(shotGroup.append(shot))

	def setSubScene(self, sub_scene):
		self.sub_scene = sub_scene
		self.cnt = 0	

	def setWeapon(self, weapon):
		self.weapon = weapon
		GameSession.weaponSave = weapon

	def draw0(self):
		pass

	def draw(self):
		if self.sub_scene == 1:
			self.drawMyShip()
		elif self.sub_scene == 2:
			pyxel.circ(self.x +7, self.y +7, self.cnt % 16, 10)
			pyxel.circ(self.x +7, self.y +7, (self.cnt+8) % 16, 7)
			r = 0
			for i in range(1,50):
				pyxel.pset(							\
					self.x+7 +7 * math.cos(r) * ((self.cnt/2+i)%20),	\
					self.y+7 +7 * math.sin(r) * ((self.cnt/2+i)%20),	\
					7 + int(self.cnt%2)*3)
				# kore ha tekito
				r += 0.11 + i*0.04
		elif self.sub_scene in (3,4,5):
			if self.cnt%2 ==0:
				self.drawMyShip()
				if self.sub_scene == 5:
					pyxel.blt(self.x-32, self.y+4, 0, 72, 8, 32, 8, gcommon.TP_COLOR)
				
		# 当たり判定領域描画
		#pyxel.rect(self.x+ self.left, self.y+self.top, self.right-self.left+1, self.bottom-self.top+1, 8)

	def drawMyShip(self):
		pyxel.blt(self.x, self.y, 0, self.sprite * 24, 0, 24, 16, gcommon.TP_COLOR)

	def setStartPosition(self):
		self.x = gcommon.MYSHIP_START_X
		self.y = gcommon.MYSHIP_START_Y

class MyShipA(MyShipBase):
	missileCycles = (10, 10, 20)
	def __init__(self, parent):
		super(MyShipA, self).__init__(parent)
		# 1:ゲーム中 2:爆発中 3:復活中
		self.sub_scene = 3
		self.shotCounter = 0
		self.missileCounter = 0
		# 武器種類 0 - 2
		self.roundAngle = 0

	# 自機ショット実行
	def executeShot(self):
		if self.weapon == gcommon.WEAPON_ROUND:
			# ラウンドバルカンは特殊
			doMissile = False
			if gcommon.checkShotKey():
				doShot = False
				if self.prevFlag:
					self.shotCounter += 1
					if self.shotCounter > 2:
						self.shotCounter = 0
						doShot = True
					self.missileCounter += 1
					if self.missileCounter > __class__.missileCycles[gcommon.WEAPON_ROUND]:
						self.missileCounter = 0
						doMissile = True
				else:
					self.prevFlag = True
					self.shotCounter = 0
					self.missileCounter = 0
					doShot = True
					doMissile = True
				if doShot:
					self.shot()
					self.roundAngle += 4
					if self.roundAngle > 62:
						self.roundAngle = 62
			elif self.roundAngle > 0:
				self.shotCounter += 1
				if self.shotCounter > 2:
					self.shotCounter = 0
					self.shot()
					self.roundAngle -= 4
					if self.roundAngle < 0:
						self.roundAngle = 0
				self.missileCounter += 1
				if self.missileCounter > __class__.missileCycles[gcommon.WEAPON_ROUND]:
					self.missileCounter = 0
					doMissile = True
			if doMissile:
				self.missile()
		else:
			# ラウンドバルカン以外
			if gcommon.checkShotKey():
				if self.prevFlag:
					self.shotCounter += 1
					if self.shotCounter > 3:
						self.shotCounter = 0
						self.shot()
					self.missileCounter += 1
					if self.missileCounter > __class__.missileCycles[self.weapon]:
						self.missileCounter = 0
						self.missile()
				else:
					self.prevFlag = True
					self.shotCounter = 0
					self.shot()
					self.missile()
			else:
				self.prevFlag = False
				self.shotCounter = 0
				self.roundAngle = 0

	# 自機弾発射
	def shot(self):
		if len(ObjMgr.shotGroups) < self.shotMax:
			shotGroup = MyShotGroup(ObjMgr.shotGroups)
			if self.weapon == 0:
				self.shotMax = 6
				ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 8, 0, 0)))
			elif self.weapon == 1:
				self.shotMax = 5
				dx = 8 * math.cos(math.pi - math.pi/64 * self.roundAngle)
				dy = 8 * math.sin(math.pi - math.pi/64 * self.roundAngle)
				ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+6, self.y +4, dx, dy, 1)))
				ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+6, self.y +4, dx, -dy, 1)))
			else:
				self.shotMax = 2
				# 前
				ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 6, 0, 2)))
				
				# やや斜め前
				ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 5.5, 2.3, -3)))
				ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 5.5, -2.3, 3)))
				
				# 斜め前
				ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 4.2, 4.2, -4)))
				ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 4.2, -4.2, 4)))

				# 斜め後
				ObjMgr.shots.append(shotGroup.append(self.createShot(self.x-2, self.y +4, -4.2, 4.2, 4)))
				ObjMgr.shots.append(shotGroup.append(self.createShot(self.x-2, self.y +4, -4.2, -4.2, -4)))

				# 後ろ
				ObjMgr.shots.append(shotGroup.append(self.createShot(self.x-2, self.y +4, -6, 0, 2)))

			BGM.sound(gcommon.SOUND_SHOT)
			ObjMgr.shotGroups.append(shotGroup)
	
	# ミサイル発射
	def missile(self):
		if len(ObjMgr.missleGroups) < self.missleMax:
			shotGroup = MyShotGroup(ObjMgr.missleGroups)
			if self.weapon == 0:
				ObjMgr.shots.append(shotGroup.append(MyMissile0(self.x+14, self.y +4, True)))
				ObjMgr.shots.append(shotGroup.append(MyMissile0(self.x+14, self.y +12, False)))
			elif self.weapon ==1:
				ObjMgr.shots.append(shotGroup.append(MyMissile1(self.x+6, self.y +12)))
			else:
				ObjMgr.shots.append(shotGroup.append(MyMissile2(self.x+2, self.y +8, 1)))
			ObjMgr.missleGroups.append(shotGroup)


	def createShot(self, x, y, dx, dy, sprite):
		s = MyShot(x, y, dx, dy, self.weapon, sprite)
		return s

# TYPE_B
class MyShipB(MyShipBase):
	missileCycles = (10, 10, 20, 10)
	def __init__(self, parent):
		self.posLate = 12
		self.posList = []
		for i in range(GameSession.multipleCount * self.posLate):
			self.posList.append(Pos.create(0 ,0))
		super(MyShipB, self).__init__(parent)
		# 1:ゲーム中 2:爆発中 3:復活中
		self.sub_scene = 3
		self.shotCounter = 0
		self.missileCounter = 0
		self.roundAngle = 0

	# 自機ショット実行
	def executeShot(self):
		if gcommon.checkShotKey():
			if self.prevFlag:
				self.shotCounter += 1
				if self.shotCounter > 3:
					self.shotCounter = 0
					self.shot()
				self.missileCounter += 1
				if self.missileCounter > __class__.missileCycles[self.weapon]:
					self.missileCounter = 0
					self.missile()
			else:
				self.prevFlag = True
				self.shotCounter = 0
				self.shot()
				self.missile()
		else:
			self.prevFlag = False
			self.shotCounter = 0
			self.roundAngle = 0

	# 自機弾発射
	def shot(self):
		self.doShot(ObjMgr.shotGroups, self.x, self.y, -1)
		index = self.posLate-1
		for i in range(GameSession.multipleCount):
			x = self.posList[index].x
			y = self.posList[index].y
			self.doShot(ObjMgr.mshotGroupsList[i], x, y, i)
			index += self.posLate
	
	def doShot(self, shotGroups, x, y, n):
		if len(shotGroups) < self.shotMax:
			shotGroup = MyShotGroup(shotGroups)
			#shotGroup.shotGroups = shotGroups
			if self.weapon == 0:
				# Double
				self.shotMax = 2
				#self.appendShot(shotGroup, self.createShot(x+12, y +4, 8, 0, 0))
				self.appendShot(shotGroup, MyShotBDouble(x +14, y+7.5, 0))
				self.appendShot(shotGroup, MyShotBDouble(x +10, y+4, 1))
				if n == -1:
					BGM.sound(gcommon.SOUND_SHOT)
			elif self.weapon == 1:
				self.shotMax = 2
				self.appendShot(shotGroup, MyShotBDouble(x +14, y+7.5, 0))
				self.appendShot(shotGroup, MyShotBDouble(x, y+7.5, 2))
				if n == -1:
					BGM.sound(gcommon.SOUND_SHOT)
			elif self.weapon == 2:
				self.shotMax = 1
				self.appendShot(shotGroup, MyShotBLaser(self.posList, self.posLate, n))
				if n == -1:
					BGM.sound(gcommon.SOUND_SHOT)
			else:
				self.shotMax = 2
				self.appendShot(shotGroup, MyShotBRipple(x +16, y+7))
				if n == -1:
					BGM.sound(gcommon.SOUND_SHOT)
			shotGroups.append(shotGroup)
	

	def missile(self):
		self.doMissile(ObjMgr.missleGroups, self.x, self.y)
		index = self.posLate-1
		for i in range(GameSession.multipleCount):
			x = self.posList[index].x
			y = self.posList[index].y
			self.doMissile(ObjMgr.mmissileGroupsList[i], x, y)
			index += self.posLate

	# ミサイル発射
	def doMissile(self, missleGroups, x, y):
		if len(missleGroups) < self.missleMax:
			shotGroup = MyShotGroup(missleGroups)
			if self.weapon == gcommon.B_WEAPON_DOUBLE:
				self.missleMax = 1
				ObjMgr.shots.append(shotGroup.append(MyMissileB0(x+14, y +12)))
			elif self.weapon == gcommon.B_WEAPON_TAILGUN:
				self.missleMax = 1
				#ObjMgr.shots.append(shotGroup.append(MyMissile2(x+12, y +8, 0)))
				ObjMgr.shots.append(shotGroup.append(MyMissileB1(x+14, y +4, True)))
				ObjMgr.shots.append(shotGroup.append(MyMissileB1(x+14, y +12, False)))
			elif self.weapon == gcommon.B_WEAPON_LASER:
				self.missleMax = 1
				#ObjMgr.shots.append(shotGroup.append(MyMissile0(x+14, y +4, True)))
				ObjMgr.shots.append(shotGroup.append(MyMissileB0(x+14, y +12)))
			else:
				self.missleMax = 1
				ObjMgr.shots.append(shotGroup.append(MyMissileB1(x+14, y +4, True)))
				ObjMgr.shots.append(shotGroup.append(MyMissileB1(x+14, y +12, False)))
			missleGroups.append(shotGroup)


	def createShot(self, x, y, dx, dy, sprite):
		s = MyShot(x, y, dx, dy, self.weapon, sprite)
		return s

	def update(self):
		if self.moveActionFlag:
			self.posList.insert(0, Pos.create(self.x, self.y -gcommon.cur_map_dy))
			self.posList.pop()
			if gcommon.sync_map_y == 1:
				for pos in self.posList:
					pos.y -= gcommon.cur_map_dy
		super(MyShipB, self).update()

	def draw0(self):
		if self.sub_scene in (2, 5):
			pass
		else:
			for i in range(self.posLate-1, len(self.posList), self.posLate):
				pyxel.blt(self.posList[i].x+2, self.posList[i].y+4, 0, 64 + ((pyxel.frame_count>>3)%3)*16, 16, 16, 8, gcommon.TP_COLOR)

	def draw(self):
		super(MyShipB, self).draw()

	def resetPosList(self):
		for o in self.posList:
			o.x = self.x
			o.y = self.y

	def setStartPosition(self):
		super(MyShipB, self).setStartPosition()
		self.x = gcommon.MYSHIP_START_X
		self.y = gcommon.MYSHIP_START_Y
		self.resetPosList()

	def setSubScene(self, sub_scene):
		super(MyShipB, self).setSubScene(sub_scene)
		self.resetPosList()

# return True: 消えた False:消えてない
def checkShotMapCollision(obj, px, py):
	no = gcommon.getMapData(px, py)
	if gcommon.breakableMapData:
		if no in (4, 5, 6):
			obj.remove()
			gcommon.setMapData(px, py, 0)
			return True
	if no >= 0 and gcommon.isMapFree(no) == False:
		obj.remove()
		return True
	return False

# return True: 壁 False:壁じゃない
def checkShotMapCollisionPerfonate(px, py):
	no = gcommon.getMapData(px, py)
	if gcommon.breakableMapData:
		if no in (4, 5, 6):
			gcommon.setMapData(px, py, 0)
			return False
	if no >= 0 and gcommon.isMapFree(no) == False:
		return True
	return False

def clearDeletableMapData(px, py, width):
	if gcommon.app.stage != 4:
		return
	for i in range(width):
		no = gcommon.getMapData(px + i*8, py)
		if no in (4, 5, 6):
			gcommon.setMapData(px + i*8, py, 0)

class MyShotBase:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.left = -4
		self.top = 0  #-2
		self.right = 11
		self.bottom = 7 #9
		self.collisionRects = None		# List of Rect
		# 跳弾処理でdx,dyを使用している
		self.dx = 4
		self.dy = 0
		self.shotPower = 0
		self.group = None
		self.removeFlag = False
		self.effect = True
		self.cnt = 0

	def hit(self, obj, brokenFlag):
		self.remove()

	def remove(self):
		self.removeFlag = True
		self.group.remove(self)
		if len(self.group.shots) == 0:
			self.group.shotGroups.remove(self.group)

	def doEffect(self, effectSound):
		# 跳弾表示
		enemy.Particle1.appendShotCenter(self)
		if effectSound:
			BGM.sound(gcommon.SOUND_HIT, gcommon.SOUND_CH2)


class MyShot(MyShotBase):
	def __init__(self, x, y, dx, dy, weapon, sprite):
		super(MyShot, self).__init__(x, y)
		self.left = -4
		self.top = 0  #-2
		self.right = 11
		self.bottom = 7 #9
		self.dx = dx
		self.dy = dy
		self.weapon = weapon
		self.shotPower = gcommon.SHOT_POWERS[self.weapon] * GameSession.powerRate
		self.sprite = sprite

	def update(self):
		self.x = self.x + self.dx
		self.y = self.y + self.dy
		if self.x <= -8 or self.x >= 256:
			self.remove()
		elif self.y <= -8 or self.y >= 192:
			self.remove()
		else:
			# ストレートの場合8ドット移動なので、２箇所マップチェックする
			for i in range(2):
				px = self.x + 2 + i * 4
				if checkShotMapCollision(self, px, self.y + 3):
					enemy.Particle1.appendShotCenterReverse(self)
					return

	def draw(self):
		# 当たり判定描画
		#pyxel.rect(self.x+ self.left, self.y+self.top, self.right-self.left+1, self.bottom-self.top+1, 8)
		if self.sprite == 0:
			pyxel.blt(self.x, self.y, 0, 104, 8, 16, 8, gcommon.TP_COLOR)
		else:
			if self.sprite > 0:
				pyxel.blt(self.x, self.y, 0, 72 + self.sprite * 8, 0, 8, 8, gcommon.TP_COLOR)
			else:
				pyxel.blt(self.x, self.y, 0, 72 - self.sprite * 8, 0, 8, -8, gcommon.TP_COLOR)

class MyShotBDouble(MyShotBase):
	# direction 0 : 前方
	#           1 : 斜め上
	#           2 : 後方
	def __init__(self, x, y, direction):
		super(MyShotBDouble, self).__init__(x, y)
		self.direction = direction
		if direction == 0:
			self.left = -5
			self.top = -3.5
			self.right = 5
			self.bottom = 3.5
			self.dx = 6
			self.dy = 0
		elif direction == 1:
			self.left = -5
			self.top = -3.5
			self.right = 5
			self.bottom = 3.5
			self.dx = 4
			self.dy = -4
		else:
			self.left = -5
			self.top = -3.5
			self.right = 5
			self.bottom = 3.5
			self.dx = -6
			self.dy = 0
		self.shotPower = gcommon.B_SHOT0_POWER * GameSession.powerRate

	def update(self):
		self.x = self.x + self.dx
		self.y = self.y + self.dy
		if self.x <= -8 or self.x >= 256:
			self.remove()
		elif self.y <= -8 or self.y >= 192:
			self.remove()
		else:
			if checkShotMapCollision(self, self.x, self.y):
				enemy.Particle1.appendShotCenterReverse(self)
				return

	def draw(self):
		# 当たり判定描画
		#pyxel.rect(self.x+ self.left, self.y+self.top, self.right-self.left+1, self.bottom-self.top+1, 8)
		if self.direction in (0,2):
			pyxel.blt(self.x -4.5, self.y -0.5, 0, 128, 19, 8 if self.direction == 0 else -8, 2, gcommon.TP_COLOR)
		else:
			pyxel.blt(self.x -2.5, self.y -2.5, 0, 136, 16, 5, 5, gcommon.TP_COLOR)

class MyShotBLaser(MyShotBase):
	def __init__(self, posList, posLate, n):
		super(MyShotBLaser, self).__init__(0, 0)
		self.posList = posList
		self.posLate = posLate
		self.mulipleNumber = n
		self.left = -4
		self.top = -3.5
		self.right = 7
		self.bottom = 3.5
		self.dx = 8
		self.dy = 0
		self.laserCount = 1
		# ショットキーを離すとFalse
		self.laserFlag = True
		self.shotPower = gcommon.B_SHOT2_POWER * GameSession.powerRate
		self.effect = True
		self.y = 0
		if self.mulipleNumber == -1:
			self.x = ObjMgr.myShip.x + 18
		else:
			self.x = self.posList[self.posLate-1 + self.mulipleNumber * self.posLate].x +18

	def update(self):
		if self.laserFlag:
			if self.mulipleNumber == -1:
				self.y = ObjMgr.myShip.y + 7
			else:
				self.y = self.posList[self.posLate-1 + self.mulipleNumber * self.posLate].y +7
	
		if gcommon.checkShotKey() == False:
			self.laserFlag = False
		if self.laserCount < 24 and self.laserFlag:
			# 伸びる
			self.laserCount += 1
			if self.mulipleNumber == -1:
			 	self.x = ObjMgr.myShip.x + 18
			else:
			 	self.x = self.posList[self.posLate-1 + self.mulipleNumber * self.posLate].x +18
			self.right += 8
		else:
			self.x += 8
		if self.x <= -8 or self.x >= 256:
			self.remove()
		elif self.y <= -8 or self.y >= 192:
			self.remove()
		else:
			# レーザー範囲のマップをクリア
			clearDeletableMapData(self.x, self.y, int((self.right+7)/8))
			# 壁に当たると縮む
			while(checkShotMapCollisionPerfonate(self.x +self.right, self.y)):
				self.right -= 8
			if self.right < 8:
				self.remove()

	def hit(self, obj, brokenFlag):
		if brokenFlag:
			return
		while True:
			self.right -= 8
			if self.right <= 8:
				self.remove()
				return
			if obj.checkShotCollision(self) == False:
				return

	def draw(self):
		l = 0
		while(l < self.right):
			pyxel.blt(self.x +l, self.y, 0, 144, 19, 8, 2, gcommon.TP_COLOR)
			l += 8

	def doEffect(self, effectSound):
		# 跳弾表示
		ObjMgr.addObj(enemy.Particle1(self.x +self.right, self.y, 0.0, 4, 50))
		if effectSound:
			BGM.sound(gcommon.SOUND_HIT, gcommon.SOUND_CH2)

# リップル
class MyShotBRipple(MyShotBase):
	# 9
	IMAGE_SOURCE = [[64,24,4,16],[72,24,5,20],[80,24,6,24],[88,24,6,28],[96,24,7,32],[104,24,8,36],[112,24,9,40],[152,8,10,44],[168,8,11,48]]
	SIZE_COUNT = 9
	def __init__(self, x, y):
		super(MyShotBRipple, self).__init__(x, y)
		self.x = x
		self.y = y
		self.dx = 6
		self.dy = 0
		self.shotPower = gcommon.B_SHOT0_POWER * GameSession.powerRate
		self.sizeIndex = 0
		self.setRect()

	def setRect(self):
		self.image = __class__.IMAGE_SOURCE[self.sizeIndex]
		self.left = -self.image[2]/2
		self.top = -self.image[3]/2
		self.right = self.image[2]/2
		self.bottom = self.image[3]/2

	def update(self):
		self.x += self.dx
		self.y += self.dy
		if self.cnt >= 4:
			self.cnt = 0
			if self.sizeIndex < __class__.SIZE_COUNT -1:
				self.sizeIndex += 1
				self.setRect()
		if self.x <= -8 or (self.x +self.left) >= 256:
			self.remove()
		elif (self.y +self.top) <= -8 or (self.y +self.bottom) >= 192:
			self.remove()
		else:
			if checkShotMapCollision(self, self.x, self.y):
				enemy.Particle1.appendShotCenterReverse(self)
				return
		self.cnt += 1

	def draw(self):
		# 当たり判定描画
		#pyxel.rect(self.x+ self.left, self.y+self.top, self.right-self.left+1, self.bottom-self.top+1, 8)
		pyxel.blt(self.x +self.left, self.y +self.top, 0, self.image[0], self.image[1], self.image[2], self.image[3], gcommon.TP_COLOR)

# 上下に落ちるようなミサイル（小スプレッド）
class MyMissile0(MyShotBase):
	def __init__(self, cx, cy, isUpper):
		super(MyMissile0, self).__init__(cx, cy)
		# x,y 座標は中心
		self.isUpper = isUpper
		self.left = -3.5
		self.top = -3.5
		self.right = 3.5
		self.bottom = 3.5
		self.dx = 2
		self.dy = -2.0 if isUpper else 2
		self.shotPower = gcommon.MISSILE0_POWER * GameSession.powerRate
		self.state = 0
		self.cnt = 0
		self.effect = False

	def update(self):
		if self.state == 0:
			self.x = self.x + self.dx
			self.y = self.y + self.dy
			if self.x <= -8 or self.x >= 256:
				self.remove()
			elif self.y <= -8 or self.y >= 192:
				self.remove()
			else:
				if abs(self.dy) <= 6:
					self.dy *= 1.05
				if gcommon.isMapFreePos(self.x, self.y) == False:
					# 爆発形態へ
					self.setExplotion()
		else:
			# 爆発中
			if self.cnt > 3:
				self.remove()
		self.cnt += 1

	def setExplotion(self):
		if self.state == 0:
			# 当たると爆発になるので大きさが変わる
			self.state = 1
			self.cnt = 0
			self.left = -3.5
			self.top = -3.5
			self.right = 3.5
			self.bottom = 3.5

	def hit(self, obj, brokenFlag):
		self.setExplotion()

	def draw(self):
		if self.state == 0:
			# 当たり判定描画
			#pyxel.rect(self.x+ self.left, self.y+self.top, self.right-self.left+1, self.bottom-self.top+1, 8)
			if abs(self.dy) > 5:
				pyxel.blt(self.x -3.5, self.y -3.5, 0, 128, 0, 8, 8 if self.isUpper else -8, gcommon.TP_COLOR)
			else:
				pyxel.blt(self.x -3.5, self.y -3.5, 0, 120, 0, 8, 8 if self.isUpper else -8, gcommon.TP_COLOR)
		else:
			if self.cnt & 2 == 0:
				clr = 7 if self.cnt & 4 == 0 else 10
				if self.cnt < 4:
					pyxel.circ(self.x, self.y, 2 + self.cnt/2, clr)
				else:
					pyxel.circ(self.x, self.y, 4, clr)

# まっすぐ飛ぶミサイル
class MyMissile1(MyShotBase):
	def __init__(self, cx, cy):
		super(MyMissile1, self).__init__(cx, cy)
		# x,y 座標は中心
		self.left = -7.5
		self.top = -3.5
		self.right = 7.5
		self.bottom = 3.5
		self.dx = 2
		self.dy = 0
		self.shotPower = gcommon.MISSILE1_POWER * GameSession.powerRate
		self.state = 0
		self.cnt = 0
		self.effect = False

	def update(self):
		if self.state == 0:
			if self.cnt < 10:
				self.y += 0.5
			else:
				self.x = self.x + self.dx
			if self.x <= -8 or self.x >= 256:
				self.remove()
			elif self.y <= -8 or self.y >= 192:
				self.remove()
			else:
				if abs(self.dx) <= 8:
					self.dx *= 1.05
				if gcommon.isMapFreePos(self.x, self.y) == False:
					# 爆発形態へ
					self.setExplosion()
		else:
			# 爆発中
			if self.cnt > 6:
				self.remove()
		self.cnt += 1

	def setExplosion(self):
		if self.state == 0:
			# 当たると爆発になるので大きさが変わる
			self.state = 1
			self.cnt = 0
			self.left = -3.5
			self.top = -3.5
			self.right = 3.5
			self.bottom = 3.5

	def hit(self, obj, brokenFlag):
		self.setExplosion()

	def draw(self):
		if self.state == 0:
			# 当たり判定描画
			#pyxel.rect(self.x+ self.left, self.y+self.top, self.right-self.left+1, self.bottom-self.top+1, 8)
			if self.cnt & 4 == 0 or self.cnt < 10:
				pyxel.blt(self.x -7.5, self.y -3.5, 0, 136+16, 0, 16, 8, gcommon.TP_COLOR)
			else:
				pyxel.blt(self.x -7.5, self.y -3.5, 0, 136, 0, 16, 8, gcommon.TP_COLOR)
		else:
			if self.cnt & 2 == 0:
				clr = 7 if self.cnt & 4 == 0 else 10
				if self.cnt < 4:
					pyxel.circ(self.x, self.y, 2 + self.cnt/2, clr)
				else:
					pyxel.circ(self.x, self.y, 4, clr)

# スプレッドボム
# direction 0: 前方
#           1: 後方
class MyMissile2(MyShotBase):
	def __init__(self, cx, cy, direction):
		super(MyMissile2, self).__init__(cx, cy)
		# x,y 座標は中心
		self.direction = direction
		self.left = -3.5
		self.top = -3.5
		self.right = 3.5
		self.bottom = 3.5
		if direction == 0:
			self.dx = 2
		else:
			self.dx = -1.5
		self.dy = 2
		self.shotPower = gcommon.MISSILE2_POWER * GameSession.powerRate
		self.state = 0
		self.cnt = 0
		self.effect = False

	def update(self):
		if self.state == 0:
			# 落下中
			if self.cnt < 15:
				self.dx *= 0.9
			else:
				self.dx = 0
			self.x += self.dx
			self.y += self.dy
			if abs(self.dy) <= 3.0:
				self.dy *= 1.05
			if self.x <= -8 or self.x >= 256:
				self.remove()
			elif self.y <= -8 or self.y >= 192:
				self.remove()
			else:
				if gcommon.isMapFreePos(self.x, self.y) == False:
					# 爆発形態へ
					self.setExplosion()
		else:
			# 爆発中
			if self.cnt > 30:
				self.remove()

		self.cnt += 1

	def setExplosion(self):
		if self.state == 0:
			# 当たると爆発になるので大きさが変わる
			self.state = 1
			self.cnt = 0
			self.left = -8
			self.top = -8
			self.right = 8
			self.bottom = 8

	def hit(self, obj, brokenFlag):
		self.setExplosion()

	def draw(self):
		if self.state == 0:
			# 当たり判定描画
			#pyxel.rect(self.x+ self.left, self.y+self.top, self.right-self.left+1, self.bottom-self.top+1, 8)
			wFlag = -1 if self.direction == 0 else 1
			if self.dx > 0.25:
				pyxel.blt(self.x -3.5, self.y -3.5, 0, 176, 0, 8 * wFlag, 8, gcommon.TP_COLOR)
			else:
				pyxel.blt(self.x -3.5, self.y -3.5, 0, 184, 0, 8 * wFlag, 8, gcommon.TP_COLOR)
		else:
			if self.cnt & 2 == 0:
				clr = 7 if self.cnt & 4 == 0 else 10
				if self.cnt < 20:
					pyxel.circ(self.x, self.y, 2 + self.cnt/2, clr)
				else:
					pyxel.circ(self.x, self.y, 10, clr)

# グラディウス風ミサイル（地面這う）
class MyMissileB0(MyShotBase):
	def __init__(self, cx, cy):
		super(MyMissileB0, self).__init__(cx, cy)
		# x,y 座標は中心
		self.left = -3.5
		self.top = -3.5
		self.right = 3.5
		self.bottom = 3.5
		self.dx = 2
		self.dy = 2
		self.shotPower = gcommon.B_MISSILE0_POWER * GameSession.powerRate
		self.state = 0
		self.cnt = 0
		self.effect = False

	def update(self):
		if self.state == 0:
			# 落下中
			if gcommon.isMapFreePos(self.x +self.dx, self.y +2) == False:
				self.state = 1
				self.dx = 2
				self.dy = 0
		else:
			if gcommon.isMapFreePos(self.x +self.dx, self.y +2):
				self.state = 0
				self.dx = 2
				self.dy = 2

		self.x += self.dx
		self.y += self.dy
		if self.state == 1:
			self.y += gcommon.cur_map_dy
		if self.x <= -8 or self.x >= 256:
			self.remove()
		elif self.y <= -8 or self.y >= 192:
			self.remove()
		else:
			if gcommon.isMapFreePos(self.x, self.y) == False:
				self.remove()

	def draw(self):
		if self.state == 0:
			pyxel.blt(self.x -3.5, self.y -3.5, 0, 112, 17, 6, 6, gcommon.TP_COLOR)
		else:
			pyxel.blt(self.x -4.5, self.y -2.5, 0, 120, 18, 8, 3, gcommon.TP_COLOR)

# 上下に落ちるようなミサイル（スプレッド無）
class MyMissileB1(MyShotBase):
	def __init__(self, cx, cy, isUpper):
		super(MyMissileB1, self).__init__(cx, cy)
		# x,y 座標は中心
		self.isUpper = isUpper
		self.left = -3.5
		self.top = -3.5
		self.right = 3.5
		self.bottom = 3.5
		self.dx = 2
		self.dy = -2.0 if isUpper else 2
		self.shotPower = gcommon.B_MISSILE1_POWER * GameSession.powerRate
		self.cnt = 0
		self.effect = False

	def update(self):
		self.x = self.x + self.dx
		self.y = self.y + self.dy
		if self.x <= -8 or self.x >= 256:
			self.remove()
		elif self.y <= -8 or self.y >= 192:
			self.remove()
		else:
			if abs(self.dy) <= 6:
				self.dy *= 1.05
			if gcommon.isMapFreePos(self.x, self.y) == False:
				self.remove()

	def draw(self):
		if abs(self.dy) > 5:
			pyxel.blt(self.x -3.5, self.y -3.5, 0, 128, 0, 8, 8 if self.isUpper else -8, gcommon.TP_COLOR)
		else:
			pyxel.blt(self.x -3.5, self.y -3.5, 0, 120, 0, 8, 8 if self.isUpper else -8, gcommon.TP_COLOR)

class MyShotGroup:
	def __init__(self, shotGroups):
		self.shots = []
		self.shotGroups = shotGroups
	
	def append(self, s):
		self.shots.append(s)
		s.group = self
		return s

	def remove(self, s):
		self.shots.remove(s)
		return len(self.shots)
