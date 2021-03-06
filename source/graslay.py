import pyxel
import math
import random
import sys
import os
import gcommon
import enemy
import boss
import boss1
import boss2
import boss3
import boss4
import bossFactory
import bossLast
import pygame.mixer
import customStartMenu
import launch
import ending
import item
import ranking
import story
from optionMenu import OptionMenuScene
from title import TitleScene
from mapDraw import MapDraw1
from mapDraw import MapDraw2
from mapDraw import MapDraw3
from mapDraw import MapDraw4
from mapDraw import MapDrawFactory
from mapDraw import MapDrawLast

# 自機
class MyShip:
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
		# 武器種類 0 - 2
		self.roundAngle = 0
		# 1:ゲーム中 2:爆発中 3:復活中
		self.sub_scene = 3
		self.shotCounter = 0
		self.missileCounter = 0
		self.prevFlag = False
		self.dx = 0
		self.setStartPosition()
		self.mouseManager = parent.mouseManager
		self.setWeapon(gcommon.GameSession.weaponSave)
		
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
				if gcommon.GameSession.playerStock == 0:
					self.sub_scene = 10
					self.cnt = 0
					self.sprite = 1
					self.x = -16
					self.parent.OnPlayerStockOver()
				else:
					gcommon.GameSession.playerStock -= 1
					#--restart_game()
					self.sub_scene=3
					self.cnt = 0
					self.sprite = 1
					self.x = -16
		elif self.sub_scene == 3:
			# 復活中
			self.dx = 0
			self.x += 1
			if self.x >= gcommon.MYSHIP_START_X:
				self.cnt = 0
				self.sub_scene = 4
		elif self.sub_scene == 4:
			# 無敵中
			self.actionButtonInput()
			if self.cnt == 120:
				self.cnt = 0
				self.sub_scene=1
		elif self.sub_scene == 5:	# scene == 5
			# クリア時
			if self.cnt == 0:
				gcommon.sound(gcommon.SOUND_AFTER_BURNER)
			if self.x < 256 + 32:
				if self.dx < 8:
					self.dx += 0.25
				self.x += self.dx
		else:	# sub_scene = 10
			# continue確認中
			pass
		self.cnt += 1

	def setSubScene(self, sub_scene):
		self.sub_scene = sub_scene
		self.cnt = 0	
	
	def actionButtonInput(self):
		cx = self.x + (self.right - self.left +1)/2+ 4
		cy = self.y + (self.bottom - self.top +1)/2+ 6
		mouseDx = 0
		mouseDy = 0
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
			self.x = self.x -2
			if self.x < 0:
				self.x = 0
		elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT) or mouseDx == 1:
			self.x = self.x +2
			self.sprite = 0
			if self.x > 240:
				self.x = 240
		if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP) or mouseDy == -1:
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
				self.setWeapon((self.weapon + 1) % 3)
	
	def setWeapon(self, weapon):
		self.weapon = weapon
		gcommon.GameSession.weaponSave = weapon

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
					if self.missileCounter > MyShip.missileCycles[gcommon.WEAPON_ROUND]:
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
				if self.missileCounter > MyShip.missileCycles[gcommon.WEAPON_ROUND]:
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
					if self.missileCounter > MyShip.missileCycles[self.weapon]:
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

	# 自機弾発射
	def shot(self):
		if len(gcommon.ObjMgr.shotGroups) < self.shotMax:
			shotGroup = MyShotGroup()
			if self.weapon == 0:
				self.shotMax = 6
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 8, 0, 0)))
			elif self.weapon == 1:
				self.shotMax = 5
				dx = 8 * math.cos(math.pi - math.pi/64 * self.roundAngle)
				dy = 8 * math.sin(math.pi - math.pi/64 * self.roundAngle)
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+6, self.y +4, dx, dy, 1)))
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+6, self.y +4, dx, -dy, 1)))
			else:
				self.shotMax = 2
				# 前
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 6, 0, 2)))
				
				# やや斜め前
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 5.5, 2.3, -3)))
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 5.5, -2.3, 3)))
				
				# 斜め前
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 4.2, 4.2, -4)))
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 4.2, -4.2, 4)))

				# 斜め後
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x-2, self.y +4, -4.2, 4.2, 4)))
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x-2, self.y +4, -4.2, -4.2, -4)))

				# 後ろ
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x-2, self.y +4, -6, 0, 2)))

			gcommon.sound(gcommon.SOUND_SHOT)
			gcommon.ObjMgr.shotGroups.append(shotGroup)
	
	# ミサイル発射
	def missile(self):
		if len(gcommon.ObjMgr.missleGroups) < self.missleMax:
			shotGroup = MyShotGroup()
			if self.weapon == 0:
				gcommon.ObjMgr.shots.append(shotGroup.append(MyMissile0(self.x+14, self.y +4, True)))
				gcommon.ObjMgr.shots.append(shotGroup.append(MyMissile0(self.x+14, self.y +12, False)))
			elif self.weapon ==1:
				gcommon.ObjMgr.shots.append(shotGroup.append(MyMissile1(self.x+6, self.y +12)))
			else:
				gcommon.ObjMgr.shots.append(shotGroup.append(MyMissile2(self.x+2, self.y +8)))
			gcommon.ObjMgr.missleGroups.append(shotGroup)


	def createShot(self, x, y, dx, dy, sprite):
		s = MyShot(x, y, dx, dy, self.weapon, sprite)
		return s
	
	def setStartPosition(self):
		self.x = gcommon.MYSHIP_START_X
		self.y = gcommon.MYSHIP_START_Y
		

# return True: 消えた False:消えてない
def checkShotMapCollision(obj, px, py):
	no = gcommon.getMapData(px, py)
	if gcommon.app.stage == 3:
		if no == 4:
			obj.remove()
			gcommon.setMapData(px, py, 0)
			return True
		elif no == 5:
			obj.remove()
			gcommon.setMapData(px, py, 0)
			return True
		elif no == 6:
			obj.remove()
			gcommon.setMapData(px, py, 0)
			return True
	if no >= 0 and gcommon.isMapFree(no) == False:
		obj.remove()
		return True
	return False


class MyShot:
	def __init__(self, x, y, dx, dy, weapon, sprite):
		self.x = x
		self.y = y
		self.left = -4
		self.top = 0  #-2
		self.right = 11
		self.bottom = 7 #9
		self.collisionRects = None		# List of Rect
		self.dx = dx
		self.dy = dy
		self.weapon = weapon
		self.shotPower = gcommon.SHOT_POWERS[self.weapon] * gcommon.GameSession.powerRate
		self.sprite = sprite
		self.group = None
		self.removeFlag = False
		self.effect = True

	def update(self):
		if self.removeFlag == False:
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

	def hit(self):
		self.remove()

	def remove(self):
		self.removeFlag = True
		self.group.remove(self)
		if len(self.group.shots) == 0:
			gcommon.ObjMgr.shotGroups.remove(self.group)

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

# 上下に落ちるようなミサイル
class MyMissile0:
	def __init__(self, cx, cy, isUpper):
		# x,y 座標は中心
		self.x = cx
		self.y = cy
		self.isUpper = isUpper
		self.left = -3.5
		self.top = -3.5
		self.right = 3.5
		self.bottom = 3.5
		self.collisionRects = None		# List of Rect
		self.dx = 2
		self.dy = -2.0 if isUpper else 2
		self.shotPower = gcommon.MISSILE0_POWER * gcommon.GameSession.powerRate
		self.group = None
		self.removeFlag = False
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
					self.hit()
		else:
			# 爆発中
			if self.cnt > 3:
				self.remove()
		self.cnt += 1

	def hit(self):
		if self.state == 0:
			# 当たると爆発になるので大きさが変わる
			self.state = 1
			self.cnt = 0
			self.left = -3.5
			self.top = -3.5
			self.right = 3.5
			self.bottom = 3.5

	def remove(self):
		self.removeFlag = True
		self.group.remove(self)
		if len(self.group.shots) == 0:
			gcommon.ObjMgr.missleGroups.remove(self.group)

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
class MyMissile1:
	def __init__(self, cx, cy):
		# x,y 座標は中心
		self.x = cx
		self.y = cy
		self.left = -7.5
		self.top = -3.5
		self.right = 7.5
		self.bottom = 3.5
		self.collisionRects = None		# List of Rect
		self.dx = 2
		self.dy = 0
		self.shotPower = gcommon.MISSILE1_POWER * gcommon.GameSession.powerRate
		self.group = None
		self.removeFlag = False
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
					self.hit()
		else:
			# 爆発中
			if self.cnt > 6:
				self.remove()
		self.cnt += 1

	def hit(self):
		if self.state == 0:
			# 当たると爆発になるので大きさが変わる
			self.state = 1
			self.cnt = 0
			self.left = -3.5
			self.top = -3.5
			self.right = 3.5
			self.bottom = 3.5
		
	def remove(self):
		self.removeFlag = True
		self.group.remove(self)
		if len(self.group.shots) == 0:
			gcommon.ObjMgr.missleGroups.remove(self.group)

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

# 後方に落ちるミサイル（爆弾だな）
class MyMissile2:
	def __init__(self, cx, cy):
		# x,y 座標は中心
		self.x = cx
		self.y = cy
		self.left = -3.5
		self.top = -3.5
		self.right = 3.5
		self.bottom = 3.5
		self.collisionRects = None		# List of Rect
		self.dx = -1.5
		self.dy = 2
		self.shotPower = gcommon.MISSILE2_POWER * gcommon.GameSession.powerRate
		self.group = None
		self.removeFlag = False
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
					self.hit()
		else:
			# 爆発中
			if self.cnt > 30:
				self.remove()

		self.cnt += 1

	def remove(self):
		self.removeFlag = True
		self.group.remove(self)
		if len(self.group.shots) == 0:
			gcommon.ObjMgr.missleGroups.remove(self.group)

	def hit(self):
		if self.state == 0:
			# 当たると爆発になるので大きさが変わる
			self.state = 1
			self.cnt = 0
			self.left = -8
			self.top = -8
			self.right = 8
			self.bottom = 8

	def draw(self):
		if self.state == 0:
			# 当たり判定描画
			#pyxel.rect(self.x+ self.left, self.y+self.top, self.right-self.left+1, self.bottom-self.top+1, 8)
			if self.dx > 0.25:
				pyxel.blt(self.x -3.5, self.y -3.5, 0, 176, 0, 8, 8, gcommon.TP_COLOR)
			else:
				pyxel.blt(self.x -3.5, self.y -3.5, 0, 184, 0, 8, 8, gcommon.TP_COLOR)
		else:
			if self.cnt & 2 == 0:
				clr = 7 if self.cnt & 4 == 0 else 10
				if self.cnt < 20:
					pyxel.circ(self.x, self.y, 2 + self.cnt/2, clr)
				else:
					pyxel.circ(self.x, self.y, 10, clr)


class MyShotGroup:
	def __init__(self):
		self.shots = []
	
	def append(self, s):
		self.shots.append(s)
		s.group = self
		return s

	def remove(self, s):
		self.shots.remove(s)
		return len(self.shots)

#  ゲームオーバー
#
class GameOver:
	def __init__(self):
		self.cnt = 0
	
	def init(self):
		self.cnt = 0
		gcommon.BGM.playOnce(gcommon.BGM.GAME_OVER)

	def update(self):
		self.cnt+=1
		if self.cnt > 5*60:
			if gcommon.GameSession.gameMode == gcommon.GAMEMODE_NORMAL:
				# クレジットが増えるのは、クレジットを使い切ってゲームオーバーしたときだけ
				if gcommon.GameSession.credits == 0 and gcommon.Settings.credits < 99:
					gcommon.Settings.credits += 1
					gcommon.saveSettings()
				# ランキング入るのはノーマルだけ
				gcommon.app.startRanking()
			else:
				# カスタム
				gcommon.app.startTitle()
	
	def draw(self):
		pyxel.cls(0)
		gcommon.showTextHCenter(90, "GAME OVER")

#
#  ステージクリアー
#
#  stage : クリアーしたステージ
class StageClear:
	def __init__(self, stage):
		self.cnt = 0
		self.stage = stage

	def init(self):
		self.cnt = 0

	def update(self):
		self.cnt+=1
		if self.cnt > 5*60:
			gcommon.app.startStage(self.stage+1)
	
	def draw(self):
		pyxel.rect(0,0,255,255,0)
		pyxel.text(96, 88, "CONGRATULATIONS!", self.cnt & 15)
		pyxel.text(104, 60*2, "STAGE CLEAR", 8)

#
#  ゲームクリアー
#
class GameClear:
	def __init__(self):
		self.cnt = 0
	
	def init(self):
		self.cnt = 0

	def update(self):
		self.cnt+=1
		if self.cnt > 5*60:
			gcommon.app.startTitle()
	
	def draw(self):
		pyxel.rect(0,0,255,255,0)
		pyxel.text(96, 88, "CONGRATULATIONS!", self.cnt & 15)
		gcommon.TextHCenter(60*2, "GAME CLEAR", 8, -1)



class StartMapDraw1:
	def __init__(self, t):
		gcommon.ObjMgr.setDrawMap(MapDraw1())

	def do(self):
		pass


class StartBGM:
	def __init__(self, t):
		gcommon.BGM.play(t[2])

	def do(self):
		pass

class StartMapDraw2:
	def __init__(self, t):
		gcommon.ObjMgr.setDrawMap(MapDraw2())

	def do(self):
		pass

class StartMapDraw3:
	def __init__(self, t):
		gcommon.ObjMgr.setDrawMap(MapDraw3())

	def do(self):
		pass

class StartMapDraw4:
	def __init__(self, t):
		gcommon.ObjMgr.setDrawMap(MapDraw4())

	def do(self):
		pass

class StartMapDrawFactory:
	def __init__(self, t):
		gcommon.ObjMgr.setDrawMap(MapDrawFactory())

	def do(self):
		pass

class StartMapDrawLast:
	def __init__(self, t):
		gcommon.ObjMgr.setDrawMap(MapDrawLast())

	def do(self):
		pass

class EndMapDraw:
	def __init__(self, t):
		gcommon.ObjMgr.removeDrawMap()

	def do(self):
		pass

class SetMapScroll:
	def __init__(self, t):
		gcommon.cur_scroll_x = t[2]
		gcommon.cur_scroll_y = t[3]
		
	def do(self):
		pass

class MainGame:
	def __init__(self, stage, restart=False):
		self.stage = stage
		self.restart = restart
	
	def init(self):
		self.mouseManager = gcommon.MouseManager()
		gcommon.ObjMgr.init()
		gcommon.ObjMgr.myShip = MyShip(self)
		gcommon.cur_scroll_x = 0.5
		gcommon.cur_scroll_y = 0.0
		gcommon.cur_map_dx = 0.0
		gcommon.cur_map_dy = 0.0

		self.story_pos = 0
		self.event_pos = 0
		self.mapOffsetX = 0
		gcommon.drawMap = None
		gcommon.game_timer = 0
		gcommon.map_x = 0
		gcommon.map_y = 0
		gcommon.scroll_flag = True
		self.initStory()
		self.initEvent()
		self.pauseMode = 0		# 0:ゲーム中 1:ポーズ 2:CONTINUE確認
		self.pauseMenuPos = 0
		self.pauseMenuRects = [
			gcommon.Rect.createWH(127-32 +10, 192/2 -32 +15,  80-8, 8),
			gcommon.Rect.createWH(127-32 +10, 192/2 -32 +25,  80-8, 8),
			gcommon.Rect.createWH(127-32 +10, 192/2 -32 +35,  80-8, 8)
		]
		self.pauseCnt = 0
		pyxel.mouse(False)

		if self.stage == 1:
			#pyxel.load("assets/graslay_vehicle01.pyxres", False, False, True, True)
			pyxel.image(1).load(0,0,"assets/graslay1.png")
			self.mapOffsetX = 0
			gcommon.sync_map_y = 0
			gcommon.long_map = False
			gcommon.draw_star = True
			gcommon.eshot_sync_scroll = False
			loadMapData(0, "assets/graslay1.pyxmap")
			loadMapData(1, "assets/graslay1b.pyxmap")
			loadMapAttribute("assets/graslay1.mapatr")
			pyxel.tilemap(1).refimg = 1
			if self.restart or gcommon.GameSession.gameMode == gcommon.GAMEMODE_CUSTOM:
				# 初期スタートは発艦時にBGM開始されているので、BGM流すのはリスタート・カスタム時だけ
				gcommon.BGM.play(gcommon.BGM.STAGE1)
		elif self.stage == 2:
			#pyxel.load("assets/graslay_dangeon22.pyxres", False, False, True, True)
			pyxel.image(1).load(0,0,"assets/graslay2.png")
			self.mapOffsetX = 0
			gcommon.sync_map_y = 0
			gcommon.long_map = False
			gcommon.draw_star = False
			gcommon.eshot_sync_scroll = False
			loadMapData(0, "assets/graslay2.pyxmap")
			loadMapAttribute("assets/graslay2.mapatr")
		elif self.stage == 3:
			#pyxel.load("assets/graslay_rock03.pyxres", False, False, True, True)
			pyxel.image(1).load(0,0,"assets/graslay3.png")
			self.mapOffsetX = 0
			gcommon.sync_map_y = 1
			gcommon.long_map = True
			gcommon.draw_star = True
			gcommon.eshot_sync_scroll = True
			loadMapData(0, "assets/graslay3-0.pyxmap")
			loadMapData(1, "assets/graslay3-1.pyxmap")
			loadMapData(2, "assets/graslay3b.pyxmap")
			loadMapAttribute("assets/graslay3.mapatr")
			pyxel.tilemap(1).refimg = 1
			pyxel.tilemap(2).refimg = 1
		elif self.stage == 4:
			#pyxel.load("assets/graslay_dangeon15.pyxres", False, False, True, True)
			pyxel.image(1).load(0,0,"assets/graslay4.png")
			self.mapOffsetX = 0
			gcommon.sync_map_y = 0
			gcommon.long_map = True
			gcommon.draw_star = True
			gcommon.eshot_sync_scroll = False
			loadMapData(0, "assets/graslay4.pyxmap")
			loadMapData(1, "assets/graslay4b.pyxmap")
			loadMapAttribute("assets/graslay4.mapatr")
			pyxel.tilemap(1).refimg = 1
		elif self.stage == 5:
			#pyxel.load("assets/graslay_dangeon10.pyxres", False, False, True, True)
			pyxel.image(1).load(0,0,"assets/graslay_factory.png")
			pyxel.image(2).load(0,0,"assets/graslay_factory-2.png")
			self.mapOffsetX = 0
			gcommon.sync_map_y = 0
			gcommon.long_map = True
			gcommon.draw_star = True
			gcommon.eshot_sync_scroll = False
			loadMapData(0, "assets/graslay_factory.pyxmap")
			loadMapData(1, "assets/graslay_factoryb.pyxmap")
			loadMapAttribute("assets/graslay_factory.mapatr")
			pyxel.tilemap(1).refimg = 1
		elif self.stage == 6:
			#pyxel.load("assets/graslay_dangeon10.pyxres", False, False, True, True)
			pyxel.image(1).load(0,0,"assets/graslay_last.png")
			pyxel.image(2).load(0,0,"assets/graslay_last-1.png")
			#pyxel.image(2).load(0,0,"assets/graslay_last-2.png")
			self.mapOffsetX = 0
			gcommon.sync_map_y = 0
			gcommon.long_map = True
			gcommon.draw_star = True
			gcommon.eshot_sync_scroll = False
			loadMapData(0, "assets/graslay_last.pyxmap")
			loadMapData(1, "assets/graslay_lastb.pyxmap")
			loadMapAttribute("assets/graslay_last.mapatr")
			pyxel.tilemap(1).refimg = 1
		#elif self.stage == 3:
		#	pyxel.image(1).load(0,0,"assets\gra-den3a.png")
		#	pyxel.image(2).load(0,0,"assets\gra-den3b.png")
		#	self.mapOffsetX = 64
		#	gcommon.draw_star = True

		self.skipGameTimer()

		pyxel.tilemap(0).refimg = 1
		gcommon.mapFreeTable = [0, 32, 33, 34, 65, 66]


	# デバッグ用のゲームタイマースキップ
	def skipGameTimer(self):
		while(gcommon.game_timer < gcommon.START_GAME_TIMER):
			self.ExecuteEvent()
			gcommon.ObjMgr.updateDrawMap0(True)
			gcommon.ObjMgr.updateDrawMap(True)
			
			gcommon.game_timer = gcommon.game_timer + 1	
	
	def doPause(self):
		if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD_1_START):
			self.pauseMode = gcommon.PAUSE_NONE
			pygame.mixer.music.unpause()
		elif gcommon.checkUpP():
			self.pauseMenuPos = (self.pauseMenuPos - 1) % 3
			return
		elif gcommon.checkDownP():
			self.pauseMenuPos = (self.pauseMenuPos + 1) % 3
			return
		if self.mouseManager.visible:
			n = gcommon.checkMouseMenuPos(self.pauseMenuRects)
			if n != -1:
				self.pauseMenuPos = n
		if self.pauseCnt > 30:
			if self.pauseMenuPos == 0:
				# CONTINUE
				if gcommon.checkShotKeyRectP(self.pauseMenuRects[self.pauseMenuPos]):
					self.pauseMode = gcommon.PAUSE_NONE
					pygame.mixer.music.unpause()
			elif self.pauseMenuPos == 1:
				if gcommon.checkShotKeyRectP(self.pauseMenuRects[self.pauseMenuPos]):
					# TITLE
					gcommon.app.startTitle()
			elif self.pauseMenuPos == 2:
				if gcommon.checkShotKeyRectP(self.pauseMenuRects[self.pauseMenuPos]):
					# EXIT
					pyxel.quit()
		self.pauseCnt += 1

	# 自機ストックが無くなったとき
	def OnPlayerStockOver(self):
		if gcommon.GameSession.gameMode == gcommon.GAMEMODE_NORMAL:
			if gcommon.GameSession.credits == 0:
				# クレジットが無くなればゲームオーバー
				gcommon.app.startGameOver()
			else:
				# クレジットがあればCONTINUE確認
				self.pauseMode = gcommon.PAUSE_CONTINUE
				self.pauseCnt = 0
		else:
			# カスタムモード時はゲームオーバー
			gcommon.app.startGameOver()

	def doConfirmContinue(self):
		if gcommon.checkUpP():
			self.pauseMenuPos = (self.pauseMenuPos - 1) % 2
			return
		elif gcommon.checkDownP():
			self.pauseMenuPos = (self.pauseMenuPos + 1) % 2
			return

		if self.mouseManager.visible:
			n = gcommon.checkMouseMenuPos(self.pauseMenuRects)
			if n in (0,1):
				self.pauseMenuPos = n
		if self.pauseCnt > 30:
			if self.pauseMenuPos == 0:
				# コンティニーする
				if gcommon.checkShotKeyRectP(self.pauseMenuRects[self.pauseMenuPos]):
					# YES
					rankingManager = ranking.RankingManager()
					# コンティニー時のランキング追加
					rankingManager.addContinueRecord()
					gcommon.GameSession.execContinue()
					self.pauseMode = gcommon.PAUSE_NONE
					gcommon.ObjMgr.myShip.sub_scene = 3
					#pygame.mixer.music.unpause()
					# # コンティニー時はステージ最初に戻される
					# # gcommon.app.restartStage()

			elif self.pauseMenuPos == 1:
				# ゲームオーバー
				if gcommon.checkShotKeyRectP(self.pauseMenuRects[self.pauseMenuPos]):
					# NO
					gcommon.app.startGameOver()

		self.pauseCnt += 1

	def update(self):
		self.mouseManager.update()
		if self.pauseMode == gcommon.PAUSE_PAUSE:
			self.doPause()
			return
		elif self.pauseMode == gcommon.PAUSE_CONTINUE:
			self.doConfirmContinue()
			return
		else:
			if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD_1_START):
				self.pauseMode = gcommon.PAUSE_PAUSE
				self.pauseCnt = 0
				pygame.mixer.music.pause()
				return

		# 星
		if gcommon.scroll_flag and gcommon.draw_star:
			gcommon.star_pos -= 0.2
			if gcommon.star_pos<0:
				gcommon.star_pos += 255

		self.ExecuteEvent()

		# マップ処理０
		if gcommon.scroll_flag:
			gcommon.ObjMgr.updateDrawMap0(False)

		# 自機移動
		gcommon.ObjMgr.myShip.update()

		# マップ処理
		if gcommon.scroll_flag:
			gcommon.ObjMgr.updateDrawMap(False)

		self.ExecuteStory()

		newShots = []
		for shot in gcommon.ObjMgr.shots:
			if shot.removeFlag == False:
				shot.update()
			if shot.removeFlag == False:
				newShots.append(shot)
		gcommon.ObjMgr.shots = newShots

		newObjs = []
		for obj in gcommon.ObjMgr.objs:
			if obj.removeFlag == False:
				if gcommon.scroll_flag:
					if gcommon.eshot_sync_scroll:
						#if obj.layer in (gcommon.C_LAYER_GRD, gcommon.C_LAYER_UNDER_GRD, gcommon.C_LAYER_E_SHOT):
						if obj.ground:
							obj.x -= gcommon.cur_scroll_x
							obj.y -= gcommon.cur_scroll_y
					else:
						#if obj.layer in (gcommon.C_LAYER_GRD, gcommon.C_LAYER_UNDER_GRD):
						if obj.ground:
							obj.x -= gcommon.cur_scroll_x
							obj.y -= gcommon.cur_scroll_y
					obj.x -= gcommon.cur_map_dx
					obj.y -= gcommon.cur_map_dy
				if obj.nextStateNo != -1:
					obj.state = obj.nextStateNo
					obj.nextStateNo = -1
					obj.cnt = 0
				obj.update()
				obj.cnt += 1
				obj.frameCount += 1
				if obj.removeFlag == False:
					newObjs.append(obj)
		gcommon.ObjMgr.objs = newObjs

		self.Collision()
		
		gcommon.game_timer = gcommon.game_timer + 1
	

	def draw(self):
		pyxel.cls(0)
		pyxel.clip(0, 0, 256, 192)
		
		#pyxel.text(55, 41, "Hello, Pyxel!", pyxel.frame_count % 16)
		#pyxel.blt(61, 66, 0, 0, 0, 38, 16)
		
		# 星
		if gcommon.draw_star:
			gcommon.drawStar(gcommon.star_pos)

		gcommon.ObjMgr.drawDrawMapBackground()

		for obj in gcommon.ObjMgr.objs:
			if (obj.layer & gcommon.C_LAYER_UNDER_GRD) != 0:
				if obj.hitcolor1 !=0 and obj.hit:
					pyxel.pal(obj.hitcolor1, obj.hitcolor2)
				obj.drawLayer(gcommon.C_LAYER_UNDER_GRD)
				if obj.hitcolor1 !=0 and obj.hit:
					pyxel.pal(obj.hitcolor1, obj.hitcolor1)
		
		gcommon.ObjMgr.drawDrawMap()
		
		# enemy(ground)
		for obj in gcommon.ObjMgr.objs:
			if (obj.layer & gcommon.C_LAYER_GRD) != 0:
				if obj.hitcolor1 !=0 and obj.hit:
					pyxel.pal(obj.hitcolor1, obj.hitcolor2)
				
				obj.drawLayer(gcommon.C_LAYER_GRD)
				if obj.hitcolor1 !=0 and obj.hit:
					pyxel.pal(obj.hitcolor1, obj.hitcolor1)

		# # item
		# for obj in gcommon.ObjMgr.objs:
		# 	if (obj.layer != gcommon.C_LAYER_ITEM) != 0:
		# 		obj.draw()
		
		# enemy(sky)
		for obj in gcommon.ObjMgr.objs:
			if (obj.layer & gcommon.C_LAYER_SKY) != 0:
				if obj.hitcolor1 !=0 and obj.hit:
					pyxel.pal(obj.hitcolor1, obj.hitcolor2)
				
				obj.drawLayer(gcommon.C_LAYER_SKY)
				if obj.hitcolor1 !=0 and obj.hit:
					pyxel.pal(obj.hitcolor1, obj.hitcolor1)

		# enemy shot and explosion(sky)
		for obj in gcommon.ObjMgr.objs:
			if (obj.layer & (gcommon.C_LAYER_EXP_SKY | gcommon.C_LAYER_E_SHOT))!= 0:
				obj.drawLayer(gcommon.C_LAYER_EXP_SKY | gcommon.C_LAYER_E_SHOT)

		# my shot
		for shot in gcommon.ObjMgr.shots:
		  shot.draw()

		# my ship
		gcommon.ObjMgr.myShip.draw()

		for obj in gcommon.ObjMgr.objs:
			if (obj.layer & gcommon.C_LAYER_UPPER_SKY) != 0:
				obj.drawLayer(gcommon.C_LAYER_UPPER_SKY)

		for obj in gcommon.ObjMgr.objs:
			if (obj.layer & gcommon.C_LAYER_TEXT) != 0:
				obj.drawLayer(gcommon.C_LAYER_TEXT)
		
		# 当たり判定描画
		if gcommon.ShowCollision:
			for shot in gcommon.ObjMgr.shots:
				if shot.removeFlag == False:
					self.drawObjRect(shot)
			self.drawObjRect(gcommon.ObjMgr.myShip)
			for obj in gcommon.ObjMgr.objs:
				if obj.removeFlag or (obj.shotHitCheck == False and obj.hitCheck == False):
					continue
				self.drawObjRect(obj)

		pyxel.clip()
		# SCORE表示
		gcommon.showText(0,192, "SC " + str(gcommon.GameSession.score).rjust(8))
		# 残機
		pyxel.blt(232, 192, 0, 8, 32, 8, 8, gcommon.TP_COLOR)
		gcommon.showText(242, 192, str(gcommon.GameSession.playerStock).rjust(2))
		
		# 武器表示
		for i in range(0,3):
			if i == gcommon.ObjMgr.myShip.weapon:
				pyxel.blt(96 + 40*i, 192, 0, i * 40, 56, 40, 8)
			else:
				pyxel.blt(96 + 40*i, 192, 0, i * 40, 48, 40, 8)
		
		#pyxel.text(120, 184, str(gcommon.back_map_x), 7)
		if gcommon.DebugMode:
			pyxel.text(120, 184, str(gcommon.game_timer), 7)
			pyxel.text(160, 184, str(len(gcommon.ObjMgr.objs)), 7)
		#pyxel.text(160, 188, str(self.event_pos),7)
		#pyxel.text(120, 194, str(gcommon.getMapData(gcommon.ObjMgr.myShip.x, gcommon.ObjMgr.myShip.y)), 7)
		# マップ位置表示
		#pyxel.text(200, 184, str(gcommon.map_x) + " " +str(gcommon.map_y), 7)

		if self.pauseMode == gcommon.PAUSE_PAUSE:
			self.drawPauseMenu()
		elif self.pauseMode == gcommon.PAUSE_CONTINUE:
			self.drawContinueMenu()

		# マウスカーソル
		if self.mouseManager.visible:
			pyxel.blt(pyxel.mouse_x -7, pyxel.mouse_y -7, 0, 24, 32, 16, 16, 2)
		
	def drawObjRect(self, obj):
		if obj.collisionRects != None:
			for rect in obj.collisionRects:
				pyxel.rectb(obj.x +rect.left, obj.y + rect.top, rect.right -rect.left+1, rect.bottom -rect.top+1, 8)
		else:
			pyxel.rectb(obj.x +obj.left, obj.y + obj.top, obj.right -obj.left+1, obj.bottom -obj.top+1, 8)

	def drawPauseMenu(self):
		pyxel.rect(127 -40, 192/2 -32, 80, 48, 0)
		pyxel.rectb(127 -39, 192/2 -31, 78, 46, 7)
		pyxel.rect(127 -37, 192/2 -29, 74, 8, 1)
		pyxel.text(127 -40 + 28, 192/2 -32 +4, "PAUSE", 7)

		pyxel.rect(127 -40+4, 192/2 -32 +15 + self.pauseMenuPos * 10, 80-8, 8, 2)

		pyxel.text(127-32 +10, 192/2 -32 +16, "CONTINUE", 7)
		pyxel.text(127-32 +10, 192/2 -32 +26, "TITLE", 7)
		pyxel.text(127-32 +10, 192/2 -32 +36, "EXIT", 7)

	def drawContinueMenu(self):
		pyxel.rect(127 -40, 192/2 -32, 80, 48, 0)
		pyxel.rectb(127 -39, 192/2 -31, 78, 46, 7)
		pyxel.rect(127 -37, 192/2 -29, 74, 8, 1)
		gcommon.showTextHCentor2(192/2 -32 +4, "CONTINUE ?", 7)

		pyxel.rect(127 -40+4, 192/2 -32 +15 + self.pauseMenuPos * 10, 80-8, 8, 2)

		pyxel.text(127-32 +10, 192/2 -32 +16, "YES", 7)
		pyxel.text(127-32 +10, 192/2 -32 +26, "NO", 7)

		pyxel.text(127-32 +10, 192/2 -32 +38, "CREDITS " + str(gcommon.GameSession.credits), 7)

	def ExecuteStory(self):
		while True:
			if len(self.story) <= self.story_pos:
				return
		
			s = self.story[self.story_pos]
			if s[0] < gcommon.game_timer:
				pass
			elif s[0] != gcommon.game_timer:
				return
			else:
				t = s[1]	# [1]はクラス型
				obj = t(s)			# ここでインスタンス化
				gcommon.ObjMgr.objs.append(obj)
				obj.appended()
			self.story_pos = self.story_pos + 1

	def ExecuteEvent(self):
		while True:
			if len(self.eventTable) <= self.event_pos:
				return
		
			s = self.eventTable[self.event_pos]
			if s[0] < gcommon.game_timer:
				print("!!ExecuteEvent passed " + str(s[0]) + " " + str(gcommon.game_timer))
				pass
			elif s[0] != gcommon.game_timer:
				return
			else:
				t = s[1]	# [1]はクラス型
				obj = t(s)			# ここでインスタンス化
				obj.do()
			self.event_pos = self.event_pos + 1

	# 衝突判定
	def Collision(self):
	
		# 壁との当たり判定
		if gcommon.ObjMgr.myShip.sub_scene == 1 and \
			gcommon.isMapFreePos(gcommon.ObjMgr.myShip.x+ 7, gcommon.ObjMgr.myShip.y +7) == False:
			self.my_broken()
			return
	
		# shot & enemy
		for obj in gcommon.ObjMgr.objs:
			if obj.removeFlag:
				continue
			obj.hit = False
			
			#if obj.layer!=gcommon.C_LAYER_GRD and obj.layer!=gcommon.C_LAYER_SKY:
			if obj.shotHitCheck == False:
				continue
			
			for shot in gcommon.ObjMgr.shots:
				if obj.checkShotCollision(shot):
					shot.hit()
					#shot.removeFlag = True
					#shot.group.remove(shot)
					#if len(shot.group.shots) == 0:
					#	gcommon.ObjMgr.shotGroups.remove(shot.group)
						
					if obj.removeFlag:
						break
		# enemy shot and wallObj
		for wallObj in gcommon.ObjMgr.objs:
			if wallObj.removeFlag:
				continue
			if wallObj.enemyShotCollision == False:
				continue
			for obj in gcommon.ObjMgr.objs:
				if obj.removeFlag:
					continue
				if obj.layer != gcommon.C_LAYER_E_SHOT:
					continue
				if gcommon.check_collision(wallObj, obj):
					obj.removeFlag = True
					break

		# my ship & enemy
		for obj in gcommon.ObjMgr.objs:
			if obj.removeFlag == False and obj.hitCheck:
				if obj.checkMyShipCollision() and gcommon.ObjMgr.myShip.sub_scene == 1:
					self.my_broken()
					break

	def my_broken(self):
		gcommon.ObjMgr.myShip.sub_scene = 2
		gcommon.ObjMgr.myShip.cnt = 0
		gcommon.sound(gcommon.SOUND_LARGE_EXP, gcommon.SOUND_CH1)

	def initEvent(self):
		if self.stage == 1:
			self.initEvent1()
		elif self.stage == 2:
			self.initEvent2()
		elif self.stage == 3:
			self.initEvent3()
		elif self.stage == 4:
			self.initEvent4()
		elif self.stage == 5:
			self.initEventFactory()
		elif self.stage == 6:
			self.initEventLast()
	
	def initEvent1(self):
		self.eventTable =[ \
			#[0, StartBGM, gcommon.BGM.STAGE1],
			[660,StartMapDraw1],		\
			[1560,SetMapScroll, 0.25, -0.25],	\
			[2180,SetMapScroll, 0.5, 0.0],
			[3260,SetMapScroll, 0.25, 0.25],
			[3460,SetMapScroll, 0, 0.5],
			[3860,SetMapScroll, 0.25, 0.25],
			[4600,SetMapScroll, 0.5, 0.0],
			[4800, StartBGM, gcommon.BGM.BOSS],
			[6000,EndMapDraw],		\
		]

	def initEvent2(self):
		self.eventTable =[ \
			[0,StartMapDraw2],		\
			[0, StartBGM, gcommon.BGM.STAGE2],
			[736,SetMapScroll, 0.25, 0.25],	\
			[1104,SetMapScroll, -0.25, 0.25],	\
			[1856,SetMapScroll, 0.5, 0.0],	\
			[2208,SetMapScroll, 0.25, 0.25],	\
			[2572,SetMapScroll, 0.5, 0.0],	\
			[3104,SetMapScroll, 0.0, -0.5],	\
			[3408,SetMapScroll, -0.25, -0.25],	\
			[4000,SetMapScroll, 0.0, -0.5],	\
			[4128,SetMapScroll, 0.5, 0.0],	\
			[4608,SetMapScroll, 0.25, -0.25],	\
			[5216,SetMapScroll, 0.50, 0.0],	\
			[6300, StartBGM, gcommon.BGM.BOSS],
		]

	def initEvent3(self):
		self.eventTable =[ \
			[0, StartBGM, gcommon.BGM.STAGE3],
			[100,StartMapDraw3],		\
			[3500+128,StartBGM, gcommon.BGM.BOSS],
		]

	def initEvent4(self):
		self.eventTable =[ \
			[0, StartBGM, gcommon.BGM.STAGE4],
			[100+512,StartMapDraw4],		\
			[3900+512, StartBGM, gcommon.BGM.BOSS],
			[4030+512, enemy.Stage4BossAppear1],	\
			[4120+512, enemy.Stage4BossAppear2],	\
			[5100+512,EndMapDraw],		\
		]

	def initEventFactory(self):
		self.eventTable =[ \
			[0, StartBGM, gcommon.BGM.STAGE5],
			[100,StartMapDrawFactory],		\
			[2040,SetMapScroll, 0.25, 0.25],	\
			[3192,SetMapScroll, 0.5, 0.0],	\
			[4400,SetMapScroll, 0.25, -0.25],	\
			[5616,SetMapScroll, 0.5, 0.0],	\
			[6500,StartBGM, gcommon.BGM.BOSS],	\
			[7800,EndMapDraw],		\
		]

	def initEventLast(self):
		baseOffset = 1200
		self.eventTable =[ \
			[0, StartBGM, gcommon.BGM.STAGE6_1],
			[2100 +baseOffset,StartMapDrawLast],		\
			[2100 +baseOffset, StartBGM, gcommon.BGM.STAGE6_2],
			[5800 +baseOffset, StartBGM, gcommon.BGM.STAGE6_3],
			[8200 +baseOffset, StartBGM, gcommon.BGM.BOSS],
		]

	def initStory(self):
		if self.stage == 1:
			self.story = story.Story.getStory1()
		elif self.stage == 2:
			self.story = story.Story.getStory2()
		elif self.stage == 3:
			self.story = story.Story.getStory3()
		elif self.stage == 4:
			self.story = story.Story.getStory4()
		elif self.stage == 5:
			self.story = story.Story.getStoryFactory()
		elif self.stage == 6:
			self.story = story.Story.getStoryLast()


def parseCommandLine():
	idx = 0
	while(idx < len(sys.argv)):
		arg = sys.argv[idx]
		if arg.upper() == "-TIMER":
			if idx+1<len(sys.argv):
				gcommon.START_GAME_TIMER = int(sys.argv[idx+1])
				print("set START_GAME_TIMER = " + str(gcommon.START_GAME_TIMER))
		elif arg.upper() == "-DEBUG":
			print("set Debug")
			gcommon.DebugMode = True
		elif arg.upper() == "-SHOWCOLLISION":
			print("set Show Collision")
			gcommon.ShowCollision = True
		elif arg.upper() == "-CUSTOMNORMAL":
			print("set Custom Normal")
			gcommon.CustomNormal = True
		idx+=1

def loadMapData(tm, fileName):
	mapFile = open(gcommon.resource_path(fileName), mode = "r")
	lines = mapFile.readlines()
	mapFile.close()
	pyxel.tilemap(tm).set(0, 0, lines)

def loadMapAttribute(fileName):
	attrFile = open(gcommon.resource_path(fileName), mode = "r")
	gcommon.mapAttribute = attrFile.readlines()
	attrFile.close()

class App:
	def __init__(self):
		gcommon.app = self
	
		# コマンドライン解析
		parseCommandLine()
		
		pygame.mixer.init()
		pyxel.init(256, 200, caption="GRASLAY", fps=60, quit_key=pyxel.KEY_Q)

		gcommon.loadSettings()
		pyxel.load("assets/graslay.pyxres")
		pyxel.image(0).load(0,0,"assets/graslay0.png")
		
		gcommon.init_atan_table()
		gcommon.initStar()
		
		rm = ranking.RankingManager()
		rm.load()

		#self.scene = MainGame()
		self.nextScene = None
		self.scene = None
		self.stage = 0
		self.startTitle()
		pyxel.run(self.update, self.draw)

	def startTitle(self):
		# クレジット補充
		gcommon.GameSession.credits = gcommon.Settings.credits
		self.setScene(TitleScene())

	def setScene(self, nextScene):
		self.nextScene = nextScene

	def startNormalGame(self, difficulty):
		self.stage = 1
		#print("Difficulty : " + str(difficulty))
		gcommon.Settings.difficulty = difficulty
		gcommon.saveSettings()
		gcommon.GameSession.init(difficulty, gcommon.Defaults.INIT_PLAYER_STOCK, gcommon.GAMEMODE_NORMAL, 1, gcommon.Settings.credits)
		gcommon.GameSession.credits -= 1
		gcommon.GameSession.playerStock -= 1
		# 発艦
		self.setScene(launch.LaunchScene())
		
		# Ending Test
		#self.setScene(ending.EndingScene())

	def startMainGame(self):
		self.setScene(MainGame(1))

	def startCustomGame(self, difficulty, stage, playerStock):
		self.stage = stage
		#print("Difficulty : " + str(difficulty))
		gcommon.Settings.difficulty = difficulty
		gcommon.saveSettings()
		if gcommon.CustomNormal:
			# カスタムでも通常にしたい場合（デバッグ）
			gcommon.GameSession.init(difficulty, playerStock, gcommon.GAMEMODE_NORMAL, stage, 1)
		else:
			# 通常
			gcommon.GameSession.init(difficulty, playerStock, gcommon.GAMEMODE_CUSTOM, stage, 1)
		gcommon.GameSession.playerStock -= 1
		self.setScene(MainGame(stage))

	def startStage(self, stage):
		self.stage = stage
		gcommon.GameSession.stage = self.stage
		self.setScene(MainGame(stage))

	def restartStage(self):
		self.setScene(MainGame(self.stage, True))

	def startNextStage(self):
		if self.stage == 6:
			gcommon.GameSession.stage = -1
			self.startEnding()
		else:
			self.startStage(self.stage +1)
		
	def startGameOver(self):
		self.setScene(GameOver())

	# ランキングに載るかどうかチェックし、
	# 載る場合はネームエントリー、載らない場合はタイトル画面へ遷移
	def startRanking(self):
		rankingManager = ranking.RankingManager()
		rankingManager.load()
		if rankingManager.inTop10(gcommon.GameSession.difficulty, gcommon.GameSession.score):
			self.setScene(ranking.EnterPlayerNameScene())
		else:
			self.startTitle()

	def startGameClear(self):
		if gcommon.GameSession.gameMode == gcommon.GAMEMODE_NORMAL:
			rankingManager = ranking.RankingManager()
			rankingManager.load()
			if rankingManager.inTop10(gcommon.GameSession.difficulty, gcommon.GameSession.score):
				# トップ１０に入るようであればネームエントリー
				self.setScene(ranking.EnterPlayerNameScene())
			else:
				self.startTitle()
		else:
			self.startTitle()

	def startStageClear(self, stage):
		self.setScene(StageClear(stage))

	def startEnding(self):
		self.setScene(ending.EndingScene())

	def startOption(self):
		self.setScene(OptionMenuScene())

	def startScoreRanking(self, exitTo):
		self.setScene(ranking.RankingDispScene(exitTo))

	def startEnterPlayerNameScene(self):
		self.setScene(ranking.EnterPlayerNameScene())

	def startCustomStartMenu(self):
		self.setScene(customStartMenu.CustomStartMenuScene())

	def update(self):
		if pyxel.btnp(pyxel.KEY_Q):
			pyxel.quit()

		if self.nextScene != None:
			self.nextScene.init()
			self.scene = self.nextScene
			self.nextScene = None
		self.scene.update()

	def draw(self):

		self.scene.draw()

App()
