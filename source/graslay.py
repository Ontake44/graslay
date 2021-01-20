import pyxel
import math
import random
import sys
import os
import gcommon
import enemy
import boss
import pygame.mixer
from optionMenu import OptionMenuScene
from title import TitleScene
import customStartMenu

# 自機
class MyShip:
	def __init__(self):
		super().__init__()
		self.sprite = 1
		self.shotMax = 4
		self.missleMax = 2
		self.left = 3
		self.top = 7
		self.right = 10
		self.bottom = 8
		self.cnt = 0
		# 武器種類 0 - 2
		self.weapon = 0
		self.roundAngle = 0
		# 1:ゲーム中 2:爆発中 3:復活中
		self.sub_scene = 3
		self.shotCounter = 0
		self.missileCounter = 0
		self.prevFlag = False
		self.dx = 0
		self.setStartPosition()
		
	def update(self):
		if gcommon.sync_map_y != 0:
			gcommon.cur_map_dy = 0
		if self.sub_scene == 1:
			# ゲーム中
			self.actionButtonInput()
		elif self.sub_scene == 2:
			# 爆発中
			if self.cnt > 90:
				if gcommon.remain == 0:
					gcommon.app.startGameOver()
					#start_gameover()
					#print("GAME OVER")
				else:
					gcommon.remain -= 1
					#--restart_game()
					self.sub_scene=3
					self.cnt = 0
					gcommon.power = gcommon.START_MY_POWER
					self.sprite = 1
					#self.setStartPosition()
					self.x = -16
		elif self.sub_scene == 3:
			# 復活中
			self.dx = 0
			self.x += 1
			if self.x >= 8:
				self.cnt = 0
				self.sub_scene = 4
		elif self.sub_scene == 4:
			# 無敵中
			self.actionButtonInput()
			if self.cnt == 120:
				self.cnt = 0
				self.sub_scene=1
		else:	# scene == 5
			# クリア時
			if self.cnt == 0:
				gcommon.sound(gcommon.SOUND_AFTER_BURNER)
			if self.x < 256 + 32:
				if self.dx < 8:
					self.dx += 0.25
				self.x += self.dx


		self.cnt += 1

	def setSubScene(self, sub_scene):
		self.sub_scene = sub_scene
		self.cnt = 0	
	
	def actionButtonInput(self):
		self.sprite = 0
		if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD_1_LEFT):
			self.x = self.x -2
			if self.x < 0:
				self.x = 0
		elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD_1_RIGHT):
			self.x = self.x +2
			self.sprite = 0
			if self.x > 240:
				self.x = 240
		if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):
			self.sprite = 2
			if gcommon.sync_map_y == 1:
				gcommon.cur_map_dy = -2
			elif gcommon.sync_map_y == 2:
				if self.y > 2:
					gcommon.cur_map_dy = -1
					self.y = self.y -1
			else:
				self.y = self.y -2
				if self.y < 2:
					self.y = 2
		elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
			# 縦は192/8 = 24キャラ
			self.sprite = 1
			if gcommon.sync_map_y == 1:
				gcommon.cur_map_dy = 2
			elif gcommon.sync_map_y == 2:
				if self.y < 176:
					gcommon.cur_map_dy = 1
					self.y = self.y +1
			else:
				self.y = self.y +2
				if self.y > 176:
					self.y = 176
		if gcommon.game_timer > 30:
			self.executeShot()
			if gcommon.checkOpionKey():
				self.weapon = (self.weapon + 1) % 3
	
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
					if self.missileCounter > 10:
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
				if self.missileCounter > 10:
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
					if self.missileCounter > 10:
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
		#if gcommon.set_color_shadow():
		#	pyxel.blt(self.x +16, self.y +16, 0, self.sprite * 16, 0, 16, 16, gcommon.TP_COLOR)
		#	pyxel.pal()
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
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 6, 0, 2)))
				
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 5.5, 2.3, -3)))
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 5.5, -2.3, 3)))
				
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 4.2, 4.2, -4)))
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 4.2, -4.2, 4)))

				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x-2, self.y +4, -4.2, 4.2, 4)))
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x-2, self.y +4, -4.2, -4.2, -4)))
			
			gcommon.sound(gcommon.SOUND_SHOT)
			gcommon.ObjMgr.shotGroups.append(shotGroup)
	
	# ミサイル発射
	def missile(self):
		if len(gcommon.ObjMgr.missleGroups) < self.missleMax:
			shotGroup = MyShotGroup()
			if self.weapon == 0:
				gcommon.ObjMgr.shots.append(shotGroup.append(MyMissile0(self.x+10, self.y, True)))
				gcommon.ObjMgr.shots.append(shotGroup.append(MyMissile0(self.x+10, self.y +8, False)))
			elif self.weapon ==1:
				gcommon.ObjMgr.shots.append(shotGroup.append(MyMissile1(self.x+2, self.y +8)))
			else:
				gcommon.ObjMgr.shots.append(shotGroup.append(MyMissile2(self.x+2, self.y +8)))
			gcommon.ObjMgr.missleGroups.append(shotGroup)


	def createShot(self, x, y, dx, dy, sprite):
		s = MyShot(x, y, dx, dy, self.weapon, sprite)
		return s
	
	def setStartPosition(self):
		self.x = 8
		self.y = pyxel.height/2 -8

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
		self.dx = dx
		self.dy = dy
		self.weapon = weapon
		self.shotPower = gcommon.SHOT_POWERS[self.weapon]
		self.sprite = sprite
		# 敵との接触後残るかどうか（爆弾系だとTrue）
		self.shotKeep = False
		self.group = None
		self.removeFlag = False

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
	def __init__(self, x, y, isUpper):
		self.x = x
		self.y = y
		self.isUpper = isUpper
		self.left = -4
		self.top = 0  #-2
		self.right = 11
		self.bottom = 7 #9
		self.dx = 2
		self.dy = -2.0 if isUpper else 2
		self.shotPower = gcommon.MISSILE0_POWER
		# 敵との接触後残るかどうか（爆弾系だとTrue）
		self.shotKeep = False
		self.group = None
		self.removeFlag = False

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
			if gcommon.isMapFreePos(self.x + 2, self.y + 3) == False:
				self.remove()

	def hit(self):
		self.remove()

	def remove(self):
		self.removeFlag = True
		self.group.remove(self)
		if len(self.group.shots) == 0:
			gcommon.ObjMgr.missleGroups.remove(self.group)

	def draw(self):
		# 当たり判定描画
		#pyxel.rect(self.x+ self.left, self.y+self.top, self.right-self.left+1, self.bottom-self.top+1, 8)
		if abs(self.dy) > 5:
			pyxel.blt(self.x, self.y, 0, 128, 0, 8, 8 if self.isUpper else -8, gcommon.TP_COLOR)
		else:
			pyxel.blt(self.x, self.y, 0, 120, 0, 8, 8 if self.isUpper else -8, gcommon.TP_COLOR)

# まっすぐ飛ぶミサイル
class MyMissile1:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.left = 0
		self.top = 0  #-2
		self.right = 15
		self.bottom = 7 #9
		self.dx = 2
		self.dy = 0
		self.shotPower = gcommon.MISSILE1_POWER
		# 敵との接触後残るかどうか（爆弾系だとTrue）
		self.shotKeep = False
		self.group = None
		self.removeFlag = False
		self.cnt = 0

	def update(self):
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
			if gcommon.isMapFreePos(self.x + 2, self.y + 3) == False:
				self.remove()
		self.cnt += 1

	def hit(self):
		self.remove()

	def remove(self):
		self.removeFlag = True
		self.group.remove(self)
		if len(self.group.shots) == 0:
			gcommon.ObjMgr.missleGroups.remove(self.group)

	def draw(self):
		# 当たり判定描画
		#pyxel.rect(self.x+ self.left, self.y+self.top, self.right-self.left+1, self.bottom-self.top+1, 8)
		if self.cnt & 4 == 0 or self.cnt < 10:
			pyxel.blt(self.x, self.y, 0, 136+16, 0, 16, 8, gcommon.TP_COLOR)
		else:
			pyxel.blt(self.x, self.y, 0, 136, 0, 16, 8, gcommon.TP_COLOR)

# 後方に落ちるミサイル（爆弾だな）
class MyMissile2:
	def __init__(self, cx, cy):
		self.x = cx
		self.y = cy
		self.left = -3.5
		self.top = -3.5
		self.right = 3.5
		self.bottom = 3.5
		self.dx = -1.5
		self.dy = 2
		self.shotPower = gcommon.MISSILE2_POWER
		# 敵との接触後残るかどうか（爆弾系だとTrue）
		self.shotKeep = True
		self.group = None
		self.removeFlag = False
		self.state = 0
		self.cnt = 0

	def update(self):
		if self.state == 0:
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
				if gcommon.isMapFreePos(self.x + 2, self.y + 3) == False:
					# 爆発形態へ
					self.hit()
		else:
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
			gcommon.app.startTitle()
	
	def draw(self):
		pyxel.cls(0)
		gcommon.TextHCenter(90, "GAME OVER", 8, -1)

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


class MapDraw1:
	def __init__(self):
		pass
	
	def init(self):
		gcommon.map_x = -32 * 8
		gcommon.map_y = 24*8

	def update0(self, skip):
		pass

	def update(self, skip):
		if skip == False:
			# スキップ時はマップデータやオブジェクト追加しない
			for my in range(0, 128):
				mx = gcommon.screenPosToMapPosX(256)
				n = gcommon.getMapDataByMapPos(mx, my)
				if n == 394:
					# 固定シャッター
					gcommon.setMapDataByMapPos(mx, my, 0)
					obj = enemy.FixedShutter1(mx, my, 2)
					gcommon.ObjMgr.addObj(obj)
		gcommon.map_x += gcommon.cur_scroll_x
		gcommon.map_y += gcommon.cur_scroll_y

	def drawBackground(self):
		if gcommon.map_x < 0:
			pyxel.bltm(-1 * int(gcommon.map_x/2), 0, 1, 0, 0,33,33, gcommon.TP_COLOR)
		else:
			pyxel.bltm(-1 * (int(gcommon.map_x/2) % 8), 0, 1, (int)(gcommon.map_x/16), 0,33,33, gcommon.TP_COLOR)


	def draw(self):
		if gcommon.map_x < 0:
			pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), 0, 0, (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)
		else:
			pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), 0, (int)(gcommon.map_x/8), (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)

class MapDraw2:
	def __init__(self):
		pass
	
	def init(self):
		gcommon.map_x = 0
		gcommon.map_y = 24*8

	def update0(self, skip):
		pass

	def update(self, skip):
		gcommon.map_x += gcommon.cur_scroll_x
		gcommon.map_y += gcommon.cur_scroll_y
	
	def drawBackground(self):
		dx = -1.0 * (int(gcommon.map_x/2) % 8)
		sx = (int(gcommon.map_x/16)%3)
		pyxel.bltm(dx, 0, 0, sx, 128, 33,33, gcommon.TP_COLOR)

	def draw(self):
		if gcommon.game_timer > 7400:
			return
		if gcommon.map_x < 0:
			pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), 0, 0, (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)
		else:
			pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), 0, int(gcommon.map_x/8), (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)

class MapDraw3:
	def __init__(self):
		pass

	def init(self):
		gcommon.map_x = -32 * 8
		gcommon.map_y = 24*8
		gcommon.back_map_x = -32 * 8/4
		gcommon.back_map_y = 0
		gcommon.cur_scroll_x = 2.0
		gcommon.cur_scroll_y = 0.0
	
	def update0(self, skip):
		if gcommon.game_timer == 3550+128:
			gcommon.sync_map_y = 0
			gcommon.cur_map_dy = 0

	def update(self, skip):
		gcommon.map_x += gcommon.cur_scroll_x
		gcommon.map_y += gcommon.cur_scroll_y
		gcommon.back_map_x += gcommon.cur_scroll_x/4
		if gcommon.game_timer > 3550+128:
			if gcommon.map_y > 336:
				gcommon.map_y -= 0.50
				if gcommon.map_y < 336:
					gcommon.map_y = 336
			elif gcommon.map_y < 336:
				gcommon.map_y += 0.50
				if gcommon.map_y > 336:
					gcommon.map_y = 336
		else:
			if skip == False:
				# スキップ時はマップデータやオブジェクト追加しない
				for my in range(0, 128):
					mx = gcommon.screenPosToMapPosX(256)
					n = gcommon.getMapDataByMapPos(mx, my)
					if n in (390, 391):
						# 砲台
						gcommon.setMapDataByMapPos(mx, my, 0)
						obj = enemy.Battery1([0,0,mx, my, 0])
						obj.first = 20
						obj.shot_speed = 3
						if n == 391:
							obj.mirror = 1
						gcommon.ObjMgr.addObj(obj)
					elif n in (394,395):
						# シャッター
						size = gcommon.getMapDataByMapPos(mx+1, my) -576
						speed = (gcommon.getMapDataByMapPos(mx+2, my) -576) * 0.5
						param1 = (gcommon.getMapDataByMapPos(mx+3, my) -576) * 20
						param2 = (gcommon.getMapDataByMapPos(mx+4, my) -576) * 20
						for i in range(5):
							gcommon.setMapDataByMapPos(mx +i, my, 0)
						pos = gcommon.mapPosToScreenPos(mx, my)
						if n == 394:
							obj = enemy.Shutter1(pos[0], pos[1] +16*size, -1, size, 0, speed, param1, param2)
						else:
							obj = enemy.Shutter1(pos[0], pos[1] -32*size +8, 1, size, 0, speed, param1, param2)
						gcommon.ObjMgr.addObj(obj)
					elif n in (396,397):
						size = gcommon.getMapDataByMapPos(mx+1, my) -576
						speed = (gcommon.getMapDataByMapPos(mx+2, my) -576) * 0.5
						param1 = (gcommon.getMapDataByMapPos(mx+3, my) -576) * 20
						param2 = (gcommon.getMapDataByMapPos(mx+4, my) -576) * 20
						for i in range(5):
							gcommon.setMapDataByMapPos(mx +i, my, 0)
						pos = gcommon.mapPosToScreenPos(mx, my)
						if n == 396:
							obj = enemy.Shutter1(pos[0], pos[1], 1, size, 0, speed, param1, param2)
						else:
							obj = enemy.Shutter1(pos[0], pos[1] -16*size +8, -1, size, 0, speed, param1, param2)
						gcommon.ObjMgr.addObj(obj)
			gcommon.map_y += gcommon.cur_map_dy
			if gcommon.map_y < 0:
				gcommon.map_y = 128 * 8 + gcommon.map_y
			elif gcommon.map_y >= 128 * 8:
				gcommon.map_y = gcommon.map_y - 128 * 8

	def drawBackground(self):
		if gcommon.back_map_x < 0:
			pyxel.bltm(-1 * int(gcommon.back_map_x), 0, 2, 0, 103,33,33, gcommon.TP_COLOR)
		else:
			mx = (int)(gcommon.back_map_x/8)
			if mx >= 183:
				mx = 183 + ((mx - 183)%21)
			pyxel.bltm(-1 * (int(gcommon.back_map_x) % 8), 0, 2, mx, 103,33,33, gcommon.TP_COLOR)

	def draw(self):
		# 上下ループマップなのでややこしい
		if gcommon.map_x < 0:
			if gcommon.map_y > (128 -24) * 8:
				# 上を描く
				pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), 0, 0, (int)(gcommon.map_y/8),
					33, (128 - int(gcommon.map_y/8)), gcommon.TP_COLOR)
				pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), 0, 0, 0,
					33, (24-128) +int(gcommon.map_y/8), gcommon.TP_COLOR)
			else:
				pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), 0, 0, (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)
		else:
			tm = int(gcommon.map_x/4096)
			moffset = (int(gcommon.map_x/2048) & 1) * 128
			w = int((gcommon.map_x %2048)/8)
			if gcommon.map_y > (128 -24) * 8:
				pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm, (int)((gcommon.map_x % 2048)/8), moffset + (int)(gcommon.map_y/8),
					33, 128 - int(gcommon.map_y/8), gcommon.TP_COLOR)
				pyxel.bltm(-1 * (int(gcommon.map_x) % 8), 128 * 8 - int(gcommon.map_y), tm, (int)((gcommon.map_x % 2048)/8), moffset,	
					33, (24 -128) +int(gcommon.map_y/8)+1, gcommon.TP_COLOR)
			else:
				pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm, (int)((gcommon.map_x % 2048)/8), moffset + (int)(gcommon.map_y/8),33,25, gcommon.TP_COLOR)
			if w >= 224:
				tm2 = int((gcommon.map_x+256)/4096)
				moffset2 = (int((gcommon.map_x+256)/2048) & 1) * 128
				if gcommon.map_y > (128 -24) * 8:
					pyxel.bltm((256-w)*8 -1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm2, 0, moffset2 + (int)(gcommon.map_y/8),
						33, 128 - int(gcommon.map_y/8), gcommon.TP_COLOR)
					pyxel.bltm((256-w)*8 -1 * (int(gcommon.map_x) % 8), 128 * 8 - int(gcommon.map_y), tm2, 0, moffset2,
						33, (24 -128) +int(gcommon.map_y/8)+1, gcommon.TP_COLOR)
				else:
					pyxel.bltm((256-w)*8 -1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm2, 0, moffset2 + (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)

class MapDraw4:
	def __init__(self):
		pass
	
	def init(self):
		gcommon.map_x = -32 * 8
		gcommon.map_y = 24*8
		gcommon.back_map_x = -32 * 8/2
		gcommon.back_map_y = 0

	def update0(self, skip):
		pass

	def update(self, skip):
		if skip == False:
			# スキップ時はマップデータやオブジェクト追加しない
			for i in range(0, 128):
				my = 127 -i
				mx = gcommon.screenPosToMapPosX(256)
				n = gcommon.getMapDataByMapPos(mx, my)
				if n == 394:
					# 柱
					size = gcommon.getMapDataByMapPos(mx+1, my) -576
					obj = enemy.RuinPillar1(mx, my, 1, size)
					gcommon.ObjMgr.addObj(obj)
				elif n == 395:
					# 床
					size = gcommon.getMapDataByMapPos(mx+1, my) -576
					obj = enemy.RuinFloor1(mx, my, 1, size)
					gcommon.ObjMgr.addObj(obj)
				if n == 396:
					# 柱
					size = gcommon.getMapDataByMapPos(mx+1, my) -576
					obj = enemy.RuinPillar1(mx, my, -1, size)
					gcommon.ObjMgr.addObj(obj)
				elif n == 397:
					# 床
					size = gcommon.getMapDataByMapPos(mx+1, my) -576
					obj = enemy.RuinFloor1(mx, my, -1, size)
					gcommon.ObjMgr.addObj(obj)
				elif n in (390, 391):
					# 砲台
					obj = enemy.Battery2(mx, my, 1)
					if n == 391:
						obj.direction = -1
					gcommon.ObjMgr.addObj(obj)
		gcommon.map_x += gcommon.cur_scroll_x
		gcommon.map_y += gcommon.cur_scroll_y
		gcommon.back_map_x += gcommon.cur_scroll_x/2

	def drawBackground(self):
		if gcommon.back_map_x < 0:
			pyxel.bltm(-1 * int(gcommon.back_map_x), 0, 1, 0, 24,33,33, gcommon.TP_COLOR)
		else:
			mx = (int)(gcommon.back_map_x/8)
			pyxel.bltm(-1 * (int(gcommon.back_map_x) % 8), 0, 1, mx, 24,33,33, gcommon.TP_COLOR)

	def draw(self):
		# if gcommon.map_x < 0:
		# 	pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), 0, 0, (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)
		# else:
		# 	pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), 0, (int)(gcommon.map_x/8), (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)
		# 上下ループマップなのでややこしい
		if gcommon.map_x < 0:
			pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), 0, 0, (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)
		else:
			tm = int(gcommon.map_x/4096)
			moffset = (int(gcommon.map_x/2048) & 1) * 128
			w = int((gcommon.map_x %2048)/8)
			pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm, (int)((gcommon.map_x % 2048)/8), moffset + (int)(gcommon.map_y/8),33,25, gcommon.TP_COLOR)
			if w >= 224:
				tm2 = int((gcommon.map_x+256)/4096)
				moffset2 = (int((gcommon.map_x+256)/2048) & 1) * 128
				pyxel.bltm((256-w)*8 -1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm2, 0, moffset2 + (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)

class MapDrawFactory:
	def __init__(self):
		pass

	def init(self):
		gcommon.map_x = -32 * 8
		gcommon.map_y = 24*8
		gcommon.cur_scroll_x = 0.5
		gcommon.cur_scroll_y = 0.0
		gcommon.back_map_x = -32 * 8
		gcommon.back_map_y = 0

	def update0(self, skip):
		if gcommon.game_timer == 3550:
			gcommon.sync_map_y = 0
			gcommon.cur_map_dy = 0

	def update(self, skip):
		#gcommon.map_x += gcommon.cur_scroll_x
		#gcommon.map_y += gcommon.cur_scroll_y
		if gcommon.game_timer > 15000:
			# ボス出現
			if gcommon.map_y > 336:
				gcommon.map_y -= 0.50
				if gcommon.map_y < 336:
					gcommon.map_y = 336
			elif gcommon.map_y < 336:
				gcommon.map_y += 0.50
				if gcommon.map_y > 336:
					gcommon.map_y = 336
		else:
			if skip == False:
				for my in range(0, 128):
					mx = gcommon.screenPosToMapPosX(256)
					n = gcommon.getMapDataByMapPos(mx, my)
					if n in (390, 391):
						# 砲台
						gcommon.setMapDataByMapPos(mx, my, 0)
						obj = enemy.Battery1([0,0,mx, my, 0])
						obj.first = 20
						if n == 391:
							obj.mirror = 1
						gcommon.ObjMgr.addObj(obj)
					elif n in (394, 395):
						# サーキュレーター
						gcommon.setMapDataByMapPos(mx, my, 0)
						pos = gcommon.mapPosToScreenPos(mx, my)
						if n == 394:
							obj = enemy.Circulator1(pos[0] +85, pos[1] +3, 1)
						else:
							obj = enemy.Circulator1(pos[0] +85, pos[1] +3, -1)
						gcommon.ObjMgr.addObj(obj)
					elif n in (396,397):
						# シャッター
						size = gcommon.getMapDataByMapPos(mx+1, my) -576
						speed = (gcommon.getMapDataByMapPos(mx+2, my) -576) * 0.5
						param1 = (gcommon.getMapDataByMapPos(mx+3, my) -576) * 20
						param2 = (gcommon.getMapDataByMapPos(mx+4, my) -576) * 20
						for i in range(5):
							gcommon.setMapDataByMapPos(mx +i, my, 0)
						pos = gcommon.mapPosToScreenPos(mx, my)
						if n == 396:
							obj = enemy.Shutter1(pos[0], pos[1], 1, size, 0, speed, param1, param2)
						else:
							obj = enemy.Shutter1(pos[0], pos[1] -16*size +8, -1, size, 0, speed, param1, param2)
						gcommon.ObjMgr.addObj(obj)
					elif n in (398, 399, 400, 401):
						# 排気
						size = gcommon.getMapDataByMapPos(mx+1, my) -576
						for i in range(2):
							gcommon.setMapDataByMapPos(mx +i, my, 0)
						dr = 0
						if n == 398:
							dr = 2
							# 下から上
						elif n == 399:
							# 上から下
							dr = 6
						elif n == 400:
							# 右
							dr = 0
						else:
							# 左
							dr = 4
						gcommon.ObjMgr.addObj(enemy.Wind1.create(mx, my, dr, size))
					elif n == 402:
						gcommon.setMapDataByMapPos(mx, my, 0)
						gcommon.ObjMgr.addObj(enemy.LiftAppear1(mx, my, -1))
					elif n == 403:
						gcommon.setMapDataByMapPos(mx, my, 0)
						gcommon.ObjMgr.addObj(enemy.LiftAppear1(mx, my, 1))
			gcommon.map_x += gcommon.cur_scroll_x
			gcommon.map_y += gcommon.cur_scroll_y
			gcommon.map_y += gcommon.cur_map_dy
			gcommon.back_map_x += gcommon.cur_scroll_x/2
			if gcommon.map_y < 0:
				gcommon.map_y = 128 * 8 + gcommon.map_y
			elif gcommon.map_y >= 128 * 8:
				gcommon.map_y = gcommon.map_y - 128 * 8

	def drawBackground(self):
		if gcommon.back_map_x < 0:
			pyxel.bltm(-1 * int(gcommon.back_map_x), 0, 1, 0, 24,33,33,3)
		else:
			mx = (int)(gcommon.back_map_x/8)
			pyxel.bltm(-1 * (int(gcommon.back_map_x) % 8), 0, 1, mx, 24,33,33, 3)

	def draw(self):
		# 上下ループマップなのでややこしい
		if gcommon.map_x < 0:
			if gcommon.map_y > (128 -24) * 8:
				# 上を描く
				pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), 0, 0, (int)(gcommon.map_y/8),
					33, (128 - int(gcommon.map_y/8)), gcommon.TP_COLOR)
				pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), 0, 0, 0,
					33, (24-128) +int(gcommon.map_y/8), gcommon.TP_COLOR)
			else:
				pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), 0, 0, (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)
		else:
			tm = int(gcommon.map_x/4096)
			moffset = (int(gcommon.map_x/2048) & 1) * 128
			w = int((gcommon.map_x %2048)/8)
			if gcommon.map_y > (128 -24) * 8:
				pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm, (int)((gcommon.map_x % 2048)/8), moffset + (int)(gcommon.map_y/8),
					33, 128 - int(gcommon.map_y/8), gcommon.TP_COLOR)
				pyxel.bltm(-1 * (int(gcommon.map_x) % 8), 128 * 8 - int(gcommon.map_y), tm, (int)((gcommon.map_x % 2048)/8), moffset,	
					33, (24 -128) +int(gcommon.map_y/8)+1, gcommon.TP_COLOR)
			else:
				pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm, (int)((gcommon.map_x % 2048)/8), moffset + (int)(gcommon.map_y/8),33,25, gcommon.TP_COLOR)
			if w >= 224:
				tm2 = int((gcommon.map_x+256)/4096)
				moffset2 = (int((gcommon.map_x+256)/2048) & 1) * 128
				if gcommon.map_y > (128 -24) * 8:
					pyxel.bltm((256-w)*8 -1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm2, 0, moffset2 + (int)(gcommon.map_y/8),
						33, 128 - int(gcommon.map_y/8), gcommon.TP_COLOR)
					pyxel.bltm((256-w)*8 -1 * (int(gcommon.map_x) % 8), 128 * 8 - int(gcommon.map_y), tm2, 0, moffset2,
						33, (24 -128) +int(gcommon.map_y/8)+1, gcommon.TP_COLOR)
				else:
					pyxel.bltm((256-w)*8 -1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm2, 0, moffset2 + (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)


class MapDrawLast:
	def __init__(self):
		pass
	
	def init(self):
		gcommon.map_x = -32 * 8
		gcommon.map_y = 24*8
		gcommon.back_map_x = -32 * 8
		gcommon.back_map_y = 0
		pyxel.image(2).load(0,0,"assets/graslay_last-2.png")

	def update0(self, skip):
		pass

	def update(self, skip):
		if skip == False:
			# スキップ時はマップデータやオブジェクト追加しない
			for i in range(0, 128):
				my = 127 -i
				mx = gcommon.screenPosToMapPosX(256)
				n = gcommon.getMapDataByMapPos(mx, my)
				if n == 392:
					# シャッター
					gcommon.setMapDataByMapPos(mx, my, 0)
					pos = gcommon.mapPosToScreenPos(mx, my)
					obj = enemy.Shutter2(pos[0] +8, pos[1] +28, False, 90)
					gcommon.ObjMgr.addObj(obj)
					obj = enemy.Shutter2(pos[0] +8, pos[1] -30, True, 180)
					gcommon.ObjMgr.addObj(obj)
				elif n in (390, 391):
					# 砲台
					gcommon.setMapDataByMapPos(mx, my, 0)
					obj = enemy.Battery2(mx, my, 1)
					if n == 391:
						obj.direction = -1
					gcommon.ObjMgr.addObj(obj)
				elif n in (422, 423):
					# ミサイル砲台
					gcommon.setMapDataByMapPos(mx, my, 0)
					obj = enemy.MissileBattery1(mx, my, (n == 423))
					gcommon.ObjMgr.addObj(obj)
				elif n in (393, 394, 395, 396):
					# Fan2発生
					waitCount = gcommon.getMapDataByMapPos(mx+1, my) -224
					gcommon.setMapDataByMapPos(mx, my, 0)
					gcommon.setMapDataByMapPos(mx+1, my, 0)
					if n == 393:
						obj = enemy.Fan2Group(mx, my, 2, waitCount * 30)
					elif n == 394:
						obj = enemy.Fan2Group(mx, my, 6, waitCount * 30)
					elif n == 395:
						obj = enemy.Fan2Group(mx, my, 5, waitCount * 30)
					elif n == 396:
						obj = enemy.Fan2Group(mx, my, 3, waitCount * 30)
					gcommon.ObjMgr.addObj(obj)
				elif n in (424, 425):
					waitCount = gcommon.getMapDataByMapPos(mx+1, my) -224
					gcommon.setMapDataByMapPos(mx, my, 0)
					gcommon.setMapDataByMapPos(mx+1, my, 0)
					if n == 424:
						obj = enemy.Shutter3(mx, my, -1, waitCount* 30)
					else:
						obj = enemy.Shutter3(mx, my, 1, waitCount* 30)
					gcommon.ObjMgr.addObj(obj)

		gcommon.map_x += gcommon.cur_scroll_x
		gcommon.map_y += gcommon.cur_scroll_y
		gcommon.map_y += gcommon.cur_map_dy
		gcommon.back_map_x += gcommon.cur_scroll_x/2
		# マップループ
		if gcommon.map_x >= (256*8+164*8):
			gcommon.map_x -= 8*10
		if gcommon.back_map_x >= 48 * 8:
			gcommon.back_map_x -= 24 * 8

	def drawBackground(self):
		if gcommon.back_map_x >= 0:
			if gcommon.back_map_x < 2:
				gcommon.setBrightnessMinus1()
			mx = (int)(gcommon.back_map_x/8)
			pyxel.bltm(-1 * (int(gcommon.back_map_x) % 8), 0, 1, mx, 24,33,33, 3)
			if gcommon.back_map_x < 2:
				pyxel.pal()
			

	def draw(self):
		# if gcommon.map_x < 0:
		# 	pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), 0, 0, (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)
		# else:
		# 	pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), 0, (int)(gcommon.map_x/8), (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)
		# 上下ループマップなのでややこしい
		if gcommon.map_x < 0:
			pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), 0, 0, (int)(gcommon.map_y/8),33,33, 3)
		else:
			tm = int(gcommon.map_x/4096)
			moffset = (int(gcommon.map_x/2048) & 1) * 128
			w = int((gcommon.map_x %2048)/8)
			pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm, (int)((gcommon.map_x % 2048)/8), moffset + (int)(gcommon.map_y/8),33,25, 3)
			if w >= 224:
				tm2 = int((gcommon.map_x+256)/4096)
				moffset2 = (int((gcommon.map_x+256)/2048) & 1) * 128
				pyxel.bltm((256-w)*8 -1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm2, 0, moffset2 + (int)(gcommon.map_y/8),33,33, 3)

class StartMapDraw1:
	def __init__(self, t):
		#gcommon.drawMap = MapDraw()
		#gcommon.map_x = -32 * 8
		#gcommon.map_y = 24*8
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
		#gcommon.drawMap = MapDraw2()
		#gcommon.map_x = 0
		#gcommon.map_y = 24*8
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
	def __init__(self, stage):
		self.stage = stage
	
	def init(self):
		gcommon.ObjMgr.init()
		gcommon.ObjMgr.myShip = MyShip()
		gcommon.cur_scroll_x = 0.5
		gcommon.cur_scroll_y = 0.0
		gcommon.cur_map_dx = 0.0
		gcommon.cur_map_dy = 0.0

		self.story_pos = 0
		self.event_pos = 0
		self.mapOffsetX = 0
		self.star_pos = 0
		gcommon.drawMap = None
		gcommon.game_timer = 0
		gcommon.map_x = 0
		gcommon.map_y = 0
		gcommon.scroll_flag = True
		self.initStory()
		self.initEvent()
		self.pause = False
		self.pauseMenuPos = 0
		
		#self.skipGameTimer()
		
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
			self.pause = False
			pygame.mixer.music.unpause()
		elif gcommon.checkUpP():
			self.pauseMenuPos = (self.pauseMenuPos - 1) % 3
			return
		elif gcommon.checkDownP():
			self.pauseMenuPos = (self.pauseMenuPos + 1) % 3
			return
		elif gcommon.checkShotKey():
			if self.pauseMenuPos == 0:
				# CONTINUE
				self.pause = False
				pygame.mixer.music.unpause()
			elif self.pauseMenuPos == 1:
				# TITLE
				gcommon.app.startTitle()
			else:
				# EXIT
				pyxel.quit()
			
	def update(self):
		if self.pause:
			self.doPause()
			return
		else:
			if pyxel.btnp(pyxel.KEY_ESCAPE) or pyxel.btnp(pyxel.GAMEPAD_1_START):
				self.pause = True
				pygame.mixer.music.pause()
				return

		# 星
		if gcommon.scroll_flag and gcommon.draw_star:
			self.star_pos -= 0.2
			if self.star_pos<0:
				self.star_pos += 255

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
				obj.cnt = obj.cnt + 1
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
			for i in range(0,96):
				pyxel.pset(((int)(gcommon.star_ary[i][0]+self.star_pos))&255, i*2, gcommon.star_ary[i][1])

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
		
		
		pyxel.clip()
		# SCORE表示
		#pyxel.text(4, 194, "SC " + str(gcommon.score), 7)
		#gcommon.showText2(0,192, "SC " + "{:08d}".format(gcommon.score))
		gcommon.showText(0,192, "SC " + str(gcommon.score).rjust(8))
		# 残機
		pyxel.blt(232, 192, 0, 8, 32, 8, 8, gcommon.TP_COLOR)
		gcommon.showText(242, 192, str(gcommon.remain).rjust(2))
		
		# 武器表示
		for i in range(0,3):
			if i == gcommon.ObjMgr.myShip.weapon:
				pyxel.blt(96 + 40*i, 192, 0, i * 40, 56, 40, 8)
			else:
				pyxel.blt(96 + 40*i, 192, 0, i * 40, 48, 40, 8)
		
		#pyxel.text(120, 184, str(gcommon.back_map_x), 7)
		pyxel.text(120, 184, str(gcommon.game_timer), 7)
		#pyxel.text(200, 188, str(len(gcommon.ObjMgr.objs)), 7)
		#pyxel.text(160, 188, str(self.event_pos),7)
		#pyxel.text(120, 194, str(gcommon.getMapData(gcommon.ObjMgr.myShip.x, gcommon.ObjMgr.myShip.y)), 7)
		# マップ位置表示
		#pyxel.text(200, 184, str(gcommon.map_x) + " " +str(gcommon.map_y), 7)

		if self.pause:
			self.drawPauseMenu()

	def drawPauseMenu(self):
		pyxel.rect(127 -40, 192/2 -32, 80, 48, 0)
		pyxel.rectb(127 -39, 192/2 -31, 78, 46, 7)
		pyxel.rect(127 -37, 192/2 -29, 74, 8, 1)
		pyxel.text(127 -40 + 28, 192/2 -32 +4, "PAUSE", 7)

		pyxel.rect(127 -40+4, 192/2 -32 +15 + self.pauseMenuPos * 10, 80-8, 8, 2)

		pyxel.text(127-32 +10, 192/2 -32 +16, "CONTINUE", 7)
		pyxel.text(127-32 +10, 192/2 -32 +26, "TITLE", 7)
		pyxel.text(127-32 +10, 192/2 -32 +36, "EXIT", 7)

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
		if gcommon.ObjMgr.myShip.sub_scene == 1:
			for obj in gcommon.ObjMgr.objs:
				if obj.removeFlag == False and obj.hitCheck:
					if obj.checkMyShipCollision():
						self.my_broken()
						break
				#elif obj.layer==gcommon.C_LAYER_ITEM:
				#	if gcommon.check_collision(obj, gcommon.ObjMgr.myShip):
				#		self.catch_item(obj)
				#		obj.removeFlag = True


	def catch_item(self, obj):
		if obj.itype == gcommon.C_ITEM_PWUP:
			gcommon.sound(gcommon.SOUND_PWUP)
			if gcommon.power < 3:
				gcommon.power += 1

	def my_broken(self):
		gcommon.ObjMgr.myShip.sub_scene = 2
		gcommon.ObjMgr.myShip.cnt = 0
		gcommon.power = gcommon.START_MY_POWER
		gcommon.sound(gcommon.SOUND_LARGE_EXP)

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
			[0, StartBGM, gcommon.BGM.STAGE1],
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
			[100,StartMapDraw4],		\
			[3900, StartBGM, gcommon.BGM.BOSS],
			[4030, enemy.Stage4BossAppear1],	\
			[4120, enemy.Stage4BossAppear2],	\
			[5100,EndMapDraw],		\
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
			self.initStory1()
		elif self.stage == 2:
			self.initStory2()
		elif self.stage == 3:
			self.initStory3()
		elif self.stage == 4:
			self.initStory4()
		elif self.stage == 5:
			self.initStoryFactory()
		elif self.stage == 6:
			self.initStoryLast()

	def initStory1(self):
		self.story=[ \
			[150, enemy.Fan1Group, 8, 10, 6],		\
			[270, enemy.Fan1Group, 170, 10, 6],		\
			[360, enemy.Fan1Group, 8, 10, 6],		\
			[450, enemy.Fan1Group, 170, 10, 6],		\
			[500, enemy.MissileShip, 40, 160],		\
			[530, enemy.MissileShip, 120, 200],		\
			[630, enemy.RollingFighter1Group, 42, 15, 4],		\
			[700, enemy.Battery1, 2+5, 28, 1],		\
			[700, enemy.Battery1, 2+5, 42, 0],		\
			[720, enemy.RollingFighter1Group, 100, 15, 4],		\
			[730, enemy.Battery1, 8+6, 41, 0],		\
			[730, enemy.Battery1, 8+6, 29, 1],		\
			[800, enemy.RollingFighter1Group, 42, 15, 4],		\
			[900, enemy.RollingFighter1Group, 100, 15, 4],		\
			[1100, enemy.Jumper1, 256, 70, 0.1],		\
			[1160, enemy.Jumper1, 256, 100, -0.1],		\
			[1200, enemy.MissileShip, 50, 200],		\
			[1230, enemy.MissileShip, 120, 160],		\
			[1300, enemy.Battery1, 41, 27, 1],		\
			[1360, enemy.Battery1, 45, 23, 1],		\
			[1460, enemy.Battery1, 49, 19, 1],		\
			[1500, enemy.Battery1, 51, 37, 0],		\
			[1500, enemy.Battery1, 53, 15, 1],		\
			[1500, enemy.Battery1, 55, 33, 0],		\
			[1500, enemy.Jumper1, 256, 70, 0.1],		\
			[1530, enemy.Battery1, 57, 11, 1],		\
			[1530, enemy.Battery1, 59, 29, 0],		\
			[1560, enemy.Jumper1, 256, 70, 0.1],		\
			[1600, enemy.Jumper1, 256, 70, 0.1],		\
			[1630, enemy.Jumper1, 256, 70, 0.1],		\
			[1700, enemy.Jumper1, 256, 70, 0.1],		\
			[1830, enemy.Jumper1, 256, 70, 0.1],		\
			[1860, enemy.Jumper1, 256, 70, 0.1],		\
			[1860, enemy.Battery1, 69, 6, 1],		\
			[1860, enemy.Battery1, 70, 25, 0],		\
			[2100, enemy.RollingFighter1Group, 24, 15, 4],		\
			[2130, enemy.RollingFighter1Group, 90, 15, 4],		\
			[2230, enemy.Jumper1, 256, 70, 0.1],		\
			[2260, enemy.Jumper1, 256, 70, 0.1],		\
			[2430, enemy.MissileShip, 82, 200],		\
			[2430, enemy.Battery1, 100, 7, 1],		\
			[2430, enemy.Battery1, 100, 24, 0],		\
		#	[2460, enemy.MissileShip, 82, 200],		\
		#	[2490, enemy.MissileShip, 82, 200],		\
			[2500, enemy.Battery1, 105, 7, 1],		\
			[2500, enemy.Battery1, 105, 24, 0],		\
			[2700, enemy.RollingFighter1Group, 24, 15, 4],		\
			[2760, enemy.RollingFighter1Group, 80, 15, 4],		\
			[2800, enemy.RollingFighter1Group, 40, 15, 4],		\
			[2830, enemy.MissileShip, 40, 160],		\
			[2860, enemy.RollingFighter1Group, 120, 15, 4],		\
			[2900, enemy.MissileShip, 80, 200],		\
			[3000, enemy.RollingFighter1Group, 30, 15, 4],		\
			[3060, enemy.RollingFighter1Group, 120, 15, 4],		\
			[3240, enemy.Jumper1, 256, 30, -0.1],		\
			[3280, enemy.Jumper1, 256, 50, 0.1],		\
			[3350, enemy.Battery1, 144, 33, 1],		\
			[3350, enemy.Battery1, 144, 35, 0],		\
			[3360, enemy.Battery1, 146, 33, 1],		\
			[3360, enemy.Battery1, 146, 35, 0],		\
			[3400, enemy.Battery1, 118, 40, 1],		\
			[3400, enemy.Battery1, 118, 42, 0],		\
			[3420, enemy.Battery1, 144, 43, 1],		\
			[3420, enemy.Battery1, 144, 45, 0],		\
			[3460, enemy.Battery1, 118, 50, 1],		\
			[3460, enemy.Battery1, 118, 52, 0],		\
			[4000, enemy.Jumper1, 256, 150, -0.1],		\
			[4030, enemy.Jumper1, 256, 150, -0.1],		\
			[4060, enemy.Jumper1, 256, 150, -0.1],		\
			[4160, enemy.Jumper1, -16, 50, 0.1],		\
			[4190, enemy.Jumper1, -16, 50, 0.1],		\
			[4200, enemy.Battery1, 162, 60, 1],		\
			[4200, enemy.Battery1, 164, 60, 1],		\
			[4200, enemy.Jumper1, 256, 130, -0.1],		\
			[4230, enemy.Jumper1, 256, 150, -0.1],		\
			[4400, enemy.Jumper1, 256, 100, 0.1],		\
			[4400, enemy.MissileShip, 80, 200],		\
			[4400, enemy.Battery1, 154, 81, 0],		\
			[4420, enemy.Battery1, 156, 81, 0],		\
			[4430, enemy.MissileShip, 120, 200],		\
			[4500, enemy.Jumper1, 256, 100, 0.1],		\
			[4500, enemy.Battery1, 170, 81, 0],		\
			[4520, enemy.Battery1, 172, 81, 0],		\
			[4530, enemy.Jumper1, 256, 120, 0.1],		\
			[4700, enemy.RollingFighter1Group, 50, 15, 4],		\
			[4730, enemy.RollingFighter1Group, 110, 15, 4],		\
			[4830, enemy.MissileShip, 120, 200],		\
			[4860, enemy.MissileShip, 70, 200],		\
			[5100, boss.Boss1, 256, 60],		\
			[5100, boss.Boss1Base, 256, 60],		\
			# [5100, enemy.DockArm, 204, 59, 180],		\
			# [5100, enemy.DockArm, 212, 59, 180],		\
			# [5130, enemy.DockArm, 206, 59, 180],		\
			# [5130, enemy.DockArm, 210, 59, 180],		\
		]

	def initStory2(self):
		self.story=[ \
			[180, enemy.Cell1Group1, 256, 10, 0],		\
			[240, enemy.Cell1Group1, 256, 60, 0],		\
			[260, enemy.Cell1Group1, -16, 60, 0],		\
			[320, enemy.Cell1Group1, 256, 20, 0],		\
			[400, enemy.Cell1Group1, 256, 50, 0],		\
			[1100, enemy.Cell1Group1, 20, 192, 1],		\
			[1500, enemy.Cell1Group1, 0, 192, 1],		\
			[2000, enemy.Cell1Group1, 256, 100, 0],		\
			[2300, enemy.Cell1Group1, 256, 100, 0],		\
			[2400, enemy.Worm1, 90, 91, 2, 4, 60],		\
			[2600, enemy.Cell1Group1, 256, 100, 0],		\
			[2610, enemy.Worm1, 103, 75, 6, 5, 80],		\
			[2760, enemy.Worm1, 111, 69, 0, 5, 90],		\
			[2800, enemy.Worm1, 122, 74, 4, 5, 130],		\
			[3200, enemy.Cell1Group1, 150, -16, 1],		\
			[3360, enemy.Cell1Group1, -16, 10, 0],		\

			[3360, enemy.Worm1, 93, 56, 1, 5, 130],		\

			[3600, enemy.Worm1, 100, 40, 3, 5, 230],		\

			[3800, enemy.Cell1Group1, 30, -16, 1],		\
			[4400, enemy.Cell1Group1, 256, 30, 0],		\
			[4500, enemy.Cell2, 256, 60, -1, -1, 0],		\
			[4510, enemy.Cell2, 256, 80, -1, 1, 0],		\
			[4600, enemy.Cell2, 256, 70, -1, 1, 0],		\

			[4610, enemy.Cell2, 256, 30, -0.5, -1, 0],		\
			[4620, enemy.Cell2, 256, 80, -0.5, 1, 0],		\
			[4640, enemy.Cell2, 256, 70, -0.5, 1, 0],		\
			[4660, enemy.Cell2, 256, 40, -0.5, 1, 0],		\
			[4680, enemy.Cell2, 256, 30, -0.5, 1, 0],		\

			# 斜面に上からへばり付いてるやつ
			[4800, enemy.Worm1, 144, 15, 7, 5, 160],		\
			[5000, enemy.Cell1Group1, -256, 20, 0],		\

			[5300, enemy.Worm1, 175, 28, 2, 5, 160],		\

			[5300, enemy.Worm2Group, 330, 30, 32, 10, enemy.worm2Tbl1],		\

			[5310, enemy.Cell1Group1, 256, 10, 0],		\
			[5360, enemy.Cell1Group1, 256, 60, 0],		\

			[5400, enemy.Worm1, 180, 9, 6, 5, 160],		\
			[5700, enemy.Worm2Group, 200, -24, 16, 10, enemy.worm2Tbl2],		\


			[5700, enemy.Worm1, 195, 26, 2, 5, 160],		\

			[5710, enemy.Cell1Group1, 256, 30, 0],		\
			[5760, enemy.Cell1Group1, 256, 100, 0],		\

			[5800, enemy.Worm2Group, 176, -24, 16, 10, enemy.worm2Tbl3],		\
			
			[5800, enemy.Worm1, 207, 9, 6, 5, 160],		\
			
			[5810, enemy.Cell1Group1, 256, 30, 0],		\
			[5860, enemy.Cell1Group1, 256, 100, 0],		\

			[6000, enemy.Worm2Group, 176, 192, 48, 10, enemy.worm2Tbl4],		\

			[6000, enemy.Worm1, 230, 8, 6, 5, 160],		\
			[6000, enemy.Worm1, 228, 25, 2, 5, 160],		\

			[6400, boss.Boss2, 241, 16],		\
		]

	def initStory3(self):
		self.story=[ \
			[3730+128, boss.Boss3],		\
		]

	def initStory4(self):
		self.story=[ \
			[4230, boss.Boss4, 0, 0],		\
		]

	def initStoryFactory(self):
		self.story=[ \
			[1200, enemy.RollingFighter1Group, 42, 15, 4],		\
			[1300, enemy.RollingFighter1Group, 58, 15, 4],		\
			[2030, enemy.RollingFighter1Group, 42, 15, 4],		\
			[2100, enemy.RollingFighter1Group, 58, 15, 4],		\
			[2200, enemy.RollingFighter1Group, 42, 15, 4],		\
			[3200, enemy.RollingFighter1Group, 32, 15, 4],		\
			[3230, enemy.RollingFighter1Group, 100, 15, 4],		\
			[3260, enemy.RollingFighter1Group, 120, 15, 4],		\
			[3600, enemy.RollingFighter1Group, 42, 15, 4],		\
			[3660, enemy.RollingFighter1Group, 80, 15, 4],		\
			[4500, enemy.Jumper1, 256, 20, 0.05],		\
			[4530, enemy.Jumper1, 256, 30, 0.05],		\
			[4600, enemy.Jumper1, 256, 20, 0.05],		\
			[4630, enemy.Jumper1, 256, 30, 0.05],		\
			[6850, boss.BossFactory, 0, 0],		\
		]

	def initStoryLast(self):
		baseOffset = 1200
		self.story=[ \
			[150, enemy.Fan1Group, 8, 10, 6],		\
			#[200, enemy.EnemyGroup, enemy.Fan1, [0, None, 256, 100], 10, 5],	\
			[270, enemy.Fan1Group, 170, 10, 6],		\
			[330, enemy.Fan1Group, 8, 10, 6],		\
			[370, enemy.Fighter2, 256, 120, 230, -1],	\
			[400, enemy.Fighter2, 256, 30, 190, 1],	\
			[400, enemy.Fan1Group, 170, 10, 6],		\
			[520, enemy.Fighter2, 256, 20, 190, 1],	\
			[580, enemy.Fighter2, 256, 150, 190, -1],	\
			#[700, boss.MiddleBoss1, 256, 50],		\
			[800, enemy.BattleShip1, 256+64, 60, False, [
				[90, 0, -1.0, 0.0],[330, 0, -1.0, 0.25],[600, 0, -1.0,0.0]
				], 0, -1],		\
			[1000, enemy.EnemyGroup, enemy.Fighter3, 
			[
				0, None, 256, 20,
				[
					[40, 0, -3.0, 0.0],[30, 0, -3.0, 0.5],[600, 0, -3.0,0.0]
				], 30
			], 15, 5],	\
			[1300, enemy.EnemyGroup, enemy.Fighter3, 
			[
				0, None, 256, 90,
				[
					[40, 0, -3.0, 0.0],[30, 0, -3.0, -0.5],[600, 0, -3.0,0.0]
				], 30
			], 15, 5],	\
			[1300, enemy.BattleShip1, 256+32, 0, False, [
				[150, 0, -1.0, 0.0],[210, 0, -1.0, -0.25],[180, 0, -1.0,0.0],[180, 0, -1.0,0.25],[600, 0, 0-1.0,0.0]
				], 0, 330],		\
			[1500, enemy.EnemyGroup, enemy.Fighter3, 
			[
				0, None, 256, 90,
				[
					[40, 0, -3.0, 0.0],[30, 0, -3.0, -0.5],[600, 0, -3.0,0.0]
				], 30
			], 15, 5],	\
			[1650, enemy.EnemyGroup, enemy.Fighter3, 
			[
				0, None, 256, 130,
				[
					[30, 0, -3.0, 0.0],[30, 0, -3.0, 0.75],[600, 0, -3.0,0.0]
				], 30
			], 15, 5],	\
			#[1500, enemy.Fighter3, 256, 60, [
			#	[90, 0, -3.0, 0.0],[330, 0, -3.0, 0.25],[600, 0, -3.0,0.0]
			#	]],		\
			# ３隻目
			[1700, enemy.BattleShip1, 256, 160, False, [
				[150, 0, -1.0, 0.0],[210, 0, -1.0, -0.25],[150, 0, -1.0,0.0],[210, 0, -1.0,0.25],[600, 0, -1.0,0.0]
				], 180, -1],		\
			[2000, enemy.EnemyGroup, enemy.Fighter3, 
			[
				0, None, 256, 10,
				[
					[30, 0, -3.0, 0.0],[30, 0, -3.0, 0.75],[600, 0, -3.0,0.0]
				], 20
			], 15, 5],	\
			[2100, enemy.EnemyGroup, enemy.Fighter3, 
			[
				0, None, 256, 100,
				[
					[30, 0, -3.0, 0.0],[30, 0, -3.0, -1.0],[600, 0, -3.0,0.0]
				], 20
			], 15, 5],	\
			[2300, enemy.EnemyGroup, enemy.Fighter3, 
			[
				0, None, 256, 120,
				[
					[30, 0, -3.0, 0.0],[30, 0, -3.0, -0.75],[600, 0, -3.0,0.0]
				], 20
			], 15, 5],	\
			# 赤い艦
			[2400, enemy.BattleShip1, 256 +32, 80, True, [
				[90, 0, -2.0, 0.0],[120, 0, -0.5, 0.0],[210, 0, -1.0, 0.25],[150, 0, -1.0,0.0],[210, 0, -1.0,0.25],[600, 0, -1.0,0.0]
				], 0, -1],		\
			[2600, enemy.EnemyGroup, enemy.Fighter3, 
			[
				0, None, 256, 10,
				[
					[30, 0, -3.0, 0.0],[30, 0, -3.0, 0.75],[600, 0, -3.0,0.0]
				], 15
			], 15, 5],	\
			[2100 +baseOffset, enemy.Fighter2, 256, 30, 190, 1],	\
			[2120 +baseOffset, enemy.Fighter2, 256, 120, 230, -1],	\
			[2260 +baseOffset, enemy.Walker1, 256, 266],		\
			[2380 +baseOffset, enemy.Tank1, 256, 144, 0, 0],	\
			[2400 +baseOffset, enemy.Tank1, 256, 24, 1, 0],	\
			[2450 +baseOffset, enemy.Tank1, 256, 144, 0, 0],	\
			[2520 +baseOffset, enemy.Tank1, 256, 24, 1, 0],	\
			[2630 +baseOffset, enemy.Tank1, -24, 144, 0, 1],	\
			[2650 +baseOffset, enemy.Tank1, -24, 24, 1, 1],	\
			[2800 +baseOffset, enemy.Tank1, -24, 144, 0, 2],	\
			[2830 +baseOffset, enemy.Tank1, -24, 24, 1, 2],	\
			[2900 +baseOffset, enemy.Tank1, -24, 144, 0, 3],	\
			[2930 +baseOffset, enemy.Tank1, -24, 24, 1, 3],	\
			[3100 +baseOffset, enemy.Tank1, -24, 144, 0, 3],	\
			[3130 +baseOffset, enemy.Tank1, -24, 24, 1, 3],	\
			[3500 +baseOffset, enemy.Fighter2, 256, 120, 230, -1],	\
			[3520 +baseOffset, enemy.Fighter2, 256, 30, 190, 1],	\
			[3700 +baseOffset, enemy.Fighter2, 256, 130, 220, -1],	\
			[3720 +baseOffset, enemy.Fighter2, 256, 40, 180, 1],	\

			[4450 +baseOffset, enemy.Fighter2, 256, 30, 190, 1],	\
			[4480 +baseOffset, enemy.Fighter2, 256, 120, 230, -1],	\
			[4520 +baseOffset, enemy.Fighter2, 256, 120, 160, -1],	\
			[4550 +baseOffset, enemy.Fighter2, 256, 30, 130, 1],	\
		#	[4700, enemy.Fighter2, 256, 30, 160, 1],	\
		#	[4730, enemy.Fighter2, 256, 120, 230, -1],	\

			[6000 +baseOffset, enemy.Spider1, 300, 64.5],		\
			[6200 +baseOffset, enemy.Tank1, 256, 152, 0, 0],	\
			[6260 +baseOffset, enemy.Tank1, 256, 16, 1, 0],	\
			[6520 +baseOffset, enemy.Tank1, -24, 152, 0, 2],	\
			[6600 +baseOffset, enemy.Tank1, -24, 16, 1, 2],	\
			[6700 +baseOffset, enemy.Tank1, 256, 152, 0, 0],	\
			[6750 +baseOffset, enemy.Tank1, -24, 16, 1, 3],	\
			[6800 +baseOffset, enemy.Tank1, -24, 16, 1, 2],	\
			[7000 +baseOffset, enemy.Tank1, 256, 16, 1, 0],	\
			[7200 +baseOffset, enemy.Tank1, -24, 152, 0, 2],	\
			[7300 +baseOffset, enemy.Tank1, -24, 16, 1, 3],	\
			[7400 +baseOffset, enemy.Tank1, 256, 16, 1, 0],	\
			[7500 +baseOffset, enemy.Tank1, -24, 16, 1, 3],	\
			[8400 +baseOffset, boss.BossLast1],	\
		]

def parseCommandLine():
	idx = 0
	while(idx < len(sys.argv)):
		arg = sys.argv[idx]
		if arg == "-timer":
			if idx+1<len(sys.argv):
				gcommon.START_GAME_TIMER = int(sys.argv[idx+1])
				print("set START_GAME_TIMER = " + str(gcommon.START_GAME_TIMER))
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
		
		#self.scene = MainGame()
		self.nextScene = None
		self.scene = None
		self.stage = 0
		self.startTitle()
		pyxel.run(self.update, self.draw)

	def startTitle(self):
		self.setScene(TitleScene())

	def setScene(self, nextScene):
		self.nextScene = nextScene

	def startGame(self, stage, playerStock):
		self.stage = stage
		gcommon.remain = playerStock
		gcommon.power = gcommon.START_MY_POWER
		gcommon.score = 0
		self.setScene(MainGame(stage))

	def startStage(self, stage):
		self.stage = stage
		self.setScene(MainGame(stage))

	def startNextStage(self):
		if self.stage == 6:
			self.startGameClear()
		else:
			self.startStage(self.stage+1)

	def startGameOver(self):
		self.setScene(GameOver())

	def startStageClear(self, stage):
		self.setScene(StageClear(stage))

	def startGameClear(self):
		self.setScene(GameClear())

	def startOption(self):
		self.setScene(OptionMenuScene())

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
