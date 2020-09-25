import pyxel
import math
import random
import sys

import gcommon
import enemy
import boss


# 自機
class MyShip:
	def __init__(self):
		super().__init__()
		self.sprite = 1
		self.shotMax = 4
		self.left = 3
		self.top = 7
		self.right = 10
		self.bottom = 8
		self.cnt = 0
		self.weapon = 0
		self.roundAngle = 0
		# 1:ゲーム中 2:爆発中 3:復活中
		self.sub_scene = 3
		self.shotCounter = 0
		self.prevFlag = False
		self.dx = 0
		self.setStartPosition()
		
	def update(self):
		if gcommon.sync_map_y:
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
					self.setStartPosition()
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
			self.sprite = 2
			if self.x > 240:
				self.x = 240
		if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.GAMEPAD_1_UP):
			self.sprite = 2
			if gcommon.sync_map_y:
				gcommon.cur_map_dy = -2
			else:
				self.y = self.y -2
				if self.y < 0:
					self.y = 0
		elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
			# 縦は192/8 = 24キャラ
			self.sprite = 1
			if gcommon.sync_map_y:
				gcommon.cur_map_dy = 2
			else:
				self.y = self.y +2
				if self.y > 176:
					self.y = 176
		elif pyxel.btn(pyxel.KEY_ESCAPE):
			pass
		if gcommon.game_timer > 30:
			if self.weapon == gcommon.WEAPON_ROUND:
				if gcommon.checkShotKey():
					doShot = False
					if self.prevFlag:
						self.shotCounter += 1
						if self.shotCounter > 2:
							self.shotCounter = 0
							doShot = True
					else:
						self.prevFlag = True
						self.shotCounter = 0
						doShot = True
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
			else:
				if gcommon.checkShotKey():
					if self.prevFlag:
						self.shotCounter += 1
						if self.shotCounter > 3:
							self.shotCounter = 0
							self.shot()
					else:
						self.prevFlag = True
						self.shotCounter = 0
						self.shot()
				else:
					self.prevFlag = False
					self.shotCounter = 0
					self.roundAngle = 0
			
			if gcommon.checkOpionKey():
				self.weapon = (self.weapon + 1) % 3
	
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
					pyxel.blt(self.x-32, self.y+4, 0, 48, 8, 32, 8, gcommon.TP_COLOR)
				
		# 当たり判定領域描画
		#pyxel.rect(self.x+ self.left, self.y+self.top, self.right-self.left+1, self.bottom-self.top+1, 8)

	def drawMyShip(self):
		#if gcommon.set_color_shadow():
		#	pyxel.blt(self.x +16, self.y +16, 0, self.sprite * 16, 0, 16, 16, gcommon.TP_COLOR)
		#	pyxel.pal()
		pyxel.blt(self.x, self.y, 0, self.sprite * 16, 0, 16, 16, gcommon.TP_COLOR)

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
			
			#if pyxel.play_pos(0) == -1:
			#	pyxel.play(0, 0)
			gcommon.sound(gcommon.SOUND_SHOT)
			gcommon.ObjMgr.shotGroups.append(shotGroup)
	
	def createShot(self, x, y, dx, dy, sprite):
		s = MyShot(self.weapon, sprite)
		s.init(x, y, dx, dy)
		return s
	
	def setStartPosition(self):
		self.x = 8
		self.y = pyxel.height/2 -8


class MyShot:
	def __init__(self, weapon, sprite):
		self.x = 0
		self.y = 0
		self.left = -4
		self.top = -2
		self.right = 11
		self.bottom = 9
		self.dx = 0
		self.dy = 0
		self.sprite = sprite
		self.group = None
		self.removeFlag = False

	def init(self, x, y, dx, dy):
		self.x = x
		self.y = y
		self.dx = dx
		self.dy = dy

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
					no = gcommon.getMapData(px, self.y + 3)
					if gcommon.app.stage == 3:
						if no == 4:
							self.remove()
							gcommon.setMapData(px, self.y + 3, 0)
							return
						elif no == 5:
							self.remove()
							gcommon.setMapData(px, self.y + 3, 4)
							return
						elif no == 6:
							self.remove()
							gcommon.setMapData(px, self.y + 3, 5)
							return
					if no >= 0 and gcommon.isMapFree(no) == False:
						self.remove()
						return

	def remove(self):
		self.removeFlag = True
		self.group.remove(self)
		if len(self.group.shots) == 0:
			gcommon.ObjMgr.shotGroups.remove(self.group)

	def draw(self):
		# 当たり判定描画
		#pyxel.rect(self.x+ self.left, self.y+self.top, self.right-self.left+1, self.bottom-self.top+1, 8)
		if self.sprite > 0:
			pyxel.blt(self.x, self.y, 0, 48 + self.sprite * 8, 0, 8, 8, gcommon.TP_COLOR)
		else:
			pyxel.blt(self.x, self.y, 0, 48 - self.sprite * 8, 0, 8, -8, gcommon.TP_COLOR)


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


#
#  タイトル表示
#
class Title:
	def __init__(self):
		gcommon.map_y = 0
		self.cnt = 0
		pyxel.image(1).load(0,0,"assets/title.png")
		pyxel.tilemap(0).refimg = 1
		self.menuPos = 0
		self.timer = 0
		self.state = 0
		self.star_pos = 0
		gcommon.loadSettings()
	
	def init(self):
		pass

	def update(self):
		if self.cnt >= 6*60:
			self.cnt = 0
		
		if self.state == 0:
			
			if gcommon.checkShotKey() and self.cnt > 30:
				if self.menuPos == 0:
					gcommon.sound(gcommon.SOUND_GAMESTART)
					self.state = 1
					self.cnt = 0
				else:
					gcommon.app.startOption()
				#app.startStageClear()
			
			if gcommon.checkUpP() or gcommon.checkDownP():
				self.menuPos = (self.menuPos + 1) & 1
		else:
			# GAME START
			if self.cnt > 40:
				gcommon.app.startGame(gcommon.START_STAGE)
			
		
		self.cnt+=1

	def draw(self):
		pyxel.cls(0)

		for i in range(0,96):
			pyxel.pset(((int)(gcommon.star_ary[i][0]+self.star_pos))&255, i*2, gcommon.star_ary[i][1])
		
		self.star_pos -= 0.2
		if self.star_pos<0:
			self.star_pos += 255

		pyxel.blt(0, 48, 1, 0, 48, 256, 72, gcommon.TP_COLOR)
		if self.state == 0:
			gcommon.Text2(110, 150, "GAME START", 7, 5)
		else:
			if self.cnt & 2 == 0:
				gcommon.Text2(110, 150, "GAME START", 7, 5)
			else:
				gcommon.Text2(110, 150, "GAME START", 8, 5)
		gcommon.Text2(110, 165, "OPTION", 7, 5)
		pyxel.blt(98, 149 + self.menuPos * 15, 0, 0, 32, 8, 8, gcommon.TP_COLOR)
		

OPTIONMENU_PLAYER_STOCK = 0
OPTIONMENU_START_STAGE = 1
OPTIONMENU_SOUND = 2
OPTIONMENU_EXIT = 3

class OptionMenu:
	def __init__(self):
		self.menuPos = 0
	
	def init(self):
		self.menuPos = 0

	def update(self):
		if gcommon.checkUpP():
			self.menuPos -= 1
			if self.menuPos < 0:
				self.menuPos = 3
		if gcommon.checkDownP():
			self.menuPos += 1
			if self.menuPos > 3:
				self.menuPos = 0
		
		if gcommon.checkRightP():
			if self.menuPos == OPTIONMENU_PLAYER_STOCK:
				gcommon.START_REMAIN += 1
				if gcommon.START_REMAIN > 99:
					gcommon.START_REMAIN = 99
			elif self.menuPos == OPTIONMENU_START_STAGE:
				gcommon.START_STAGE += 1
				if gcommon.START_STAGE > 3:
					gcommon.START_STAGE = 3
			elif self.menuPos == OPTIONMENU_SOUND:
				gcommon.SOUND_ON = not gcommon.SOUND_ON
		elif gcommon.checkLeftP():
			if self.menuPos == OPTIONMENU_PLAYER_STOCK:
				gcommon.START_REMAIN -= 1
				if gcommon.START_REMAIN < 1:
					gcommon.START_REMAIN = 1
			elif self.menuPos == OPTIONMENU_START_STAGE:
				gcommon.START_STAGE -= 1
				if gcommon.START_STAGE < 1:
					gcommon.START_STAGE = 1
			elif self.menuPos == OPTIONMENU_SOUND:
				gcommon.SOUND_ON = not gcommon.SOUND_ON
		
		if gcommon.checkShotKeyP() and self.menuPos == OPTIONMENU_EXIT:
			gcommon.saveSettings()
			gcommon.app.startTitle()

	def draw(self):
		pyxel.cls(1)
		gcommon.Text2(8, 8, "OPTION MENU", 7, 5)
		y = 50
		gcommon.Text2(30, y, "DIFFICULTY", 6, 5)
		gcommon.Text2(120, y, "NORMAL", 6, 5)
		y += 20
		
		gcommon.Text2(30, y, "PLAYER STOCK", self.getOptionColor(OPTIONMENU_PLAYER_STOCK), 5)
		gcommon.Text2(120, y, str(gcommon.START_REMAIN), self.getOptionColor(OPTIONMENU_PLAYER_STOCK), 5)
		y += 20

		gcommon.Text2(30, y, "START STAGE", self.getOptionColor(OPTIONMENU_START_STAGE), 5)
		gcommon.Text2(120, y, str(gcommon.START_STAGE), self.getOptionColor(OPTIONMENU_START_STAGE), 5)
		y += 20
		gcommon.Text2(30, y, "SOUND", self.getOptionColor(OPTIONMENU_SOUND), 5)
		if gcommon.SOUND_ON:
			gcommon.Text2(120, y, "ON", self.getOptionColor(OPTIONMENU_SOUND), 5)
		else:
			gcommon.Text2(120, y, "OFF", self.getOptionColor(OPTIONMENU_SOUND), 5)
	
		y += 20
		gcommon.Text2(30, y, "EXIT", self.getOptionColor(OPTIONMENU_EXIT), 5)


	def getOptionColor(self, index):
		if index == self.menuPos:
			return 8
		else:
			return 7

#
#  ゲームオーバー
#
class GameOver:
	def __init__(self):
		self.cnt = 0
	
	def init(self):
		self.cnt = 0

	def update(self):
		self.cnt+=1
		if self.cnt > 5*60:
			gcommon.app.startTitle()
	
	def draw(self):
		pyxel.cls(0)
		gcommon.TextHCenter(60*2, "GAME OVER", 8, -1)

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


class MapDraw:
	def __init__(self):
		pass
	
	def init(self):
		gcommon.map_x = -32 * 8
		gcommon.map_y = 24*8

	def update0(self):
		pass

	def update(self):
		gcommon.map_x += gcommon.cur_scroll_x
		gcommon.map_y += gcommon.cur_scroll_y

	def drawBackground(self):
		pass

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

	def update0(self):
		pass

	def update(self):
		gcommon.map_x += gcommon.cur_scroll_x
		gcommon.map_y += gcommon.cur_scroll_y
	
	def drawBackground(self):
		dx = -1.0 * (int(gcommon.map_x/2) % 8)
		sx = (int(gcommon.map_x/16)%3)
		pyxel.bltm(dx, 0, 0, sx, 128, 33,33, gcommon.TP_COLOR)

	def draw(self):
		dx = -1.0 * (int(gcommon.map_x/2) % 8)
		dy = -1.0 * (int(gcommon.map_y/2) % 8)
		#sx = (int(gcommon.map_x/16)%3)
		#sy = 128 +(int(gcommon.map_y/16)%3)
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
		gcommon.cur_scroll_x = 2.0
		gcommon.cur_scroll_y = 0.0
	
	def update0(self):
		if gcommon.game_timer == 3550:
			gcommon.sync_map_y = False
			gcommon.cur_map_dy = 0

	def update(self):
		if gcommon.game_timer > 3550:
			if gcommon.map_y > 336:
				gcommon.map_y -= 0.50
				if gcommon.map_y < 336:
					gcommon.map_y = 336
			elif gcommon.map_y < 336:
				gcommon.map_y += 0.50
				if gcommon.map_y > 336:
					gcommon.map_y = 336
		else:
			for my in range(0, 128):
				mx = gcommon.screenPosToMapPosX(256)
				n = gcommon.getMapDataByMapPos(mx, my)
				if n in (390, 391):
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
		gcommon.map_x += gcommon.cur_scroll_x
		gcommon.map_y += gcommon.cur_scroll_y

	def drawBackground(self):
		pass

	def draw(self):
		if gcommon.map_x < 0:
			if gcommon.map_y > (128 -24) * 8:
				# 上を描く
				pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), 0, 0, (int)(gcommon.map_y/8),
					33, (128 - int(gcommon.map_y/8)), gcommon.TP_COLOR)
				pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), 0, 0, 0,
					33, (24-128) +int(gcommon.map_y/8), gcommon.TP_COLOR)
			else:
				pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), 0, 0, (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)
		#elif gcommon.map_x > (256 -32) * 8 and gcommon.map_x < :
		#	pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), 0, (int)(gcommon.map_x/8), (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)
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


class StartMapDraw1:
	def __init__(self, t):
		#gcommon.drawMap = MapDraw()
		#gcommon.map_x = -32 * 8
		#gcommon.map_y = 24*8
		gcommon.ObjMgr.setDrawMap(MapDraw())

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
		# gcommon.drawMap = MapDraw3()
		# gcommon.map_x = -32 * 8
		# gcommon.map_y = 24*8
		# gcommon.cur_scroll_x = 2.0
		# gcommon.cur_scroll_y = 0.0
		gcommon.ObjMgr.setDrawMap(MapDraw3())

	def do(self):
		pass

class EndMapDraw:
	def __init__(self, t):
		gcommon.drawMap = None

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
		self.initStory()
		self.initEvent()
		
		self.skipGameTimer()
		
		if self.stage == 1:
			pyxel.image(1).load(0,0,"assets/graslay1.png")
			self.mapOffsetX = 0
			gcommon.sync_map_y = False
			gcommon.long_map = False
			gcommon.draw_star = True
			loadMapData(0, "assets/graslay1.pyxmap")
		elif self.stage == 2:
			pyxel.image(1).load(0,0,"assets/graslay2.png")
			self.mapOffsetX = 0
			gcommon.sync_map_y = False
			gcommon.long_map = False
			gcommon.draw_star = False
			loadMapData(0, "assets/graslay2.pyxmap")
		elif self.stage == 3:
			pyxel.image(1).load(0,0,"assets/graslay3.png")
			self.mapOffsetX = 0
			gcommon.sync_map_y = True
			gcommon.long_map = True
			gcommon.draw_star = True
			loadMapData(0, "assets/graslay3-0.pyxmap")
			loadMapData(1, "assets/graslay3-1.pyxmap")
			pyxel.tilemap(1).refimg = 1
		#elif self.stage == 3:
		#	pyxel.image(1).load(0,0,"assets\gra-den3a.png")
		#	pyxel.image(2).load(0,0,"assets\gra-den3b.png")
		#	self.mapOffsetX = 64
		#	gcommon.draw_star = True
		pyxel.tilemap(0).refimg = 1
		gcommon.mapFreeTable = [0, 32, 33, 34, 65, 66]

	def skipGameTimer(self):
		while(gcommon.game_timer < gcommon.START_GAME_TIMER):
			self.ExecuteEvent()
			gcommon.ObjMgr.updateDrawMap0()
			gcommon.ObjMgr.updateDrawMap()
			
			gcommon.game_timer = gcommon.game_timer + 1	
	
	def update(self):
		self.ExecuteEvent()

		# マップ処理０
		gcommon.ObjMgr.updateDrawMap0()

		# 自機移動
		gcommon.ObjMgr.myShip.update()

		# マップ処理
		gcommon.ObjMgr.updateDrawMap()

		self.ExecuteStory()

		newShots = []
		for shot in gcommon.ObjMgr.shots:
			shot.update()
			if shot.removeFlag == False:
				newShots.append(shot)
		gcommon.ObjMgr.shots = newShots

	
		newObjs = []
		for obj in gcommon.ObjMgr.objs:
			if obj.layer == gcommon.C_LAYER_GRD 	\
				or obj.layer==gcommon.C_LAYER_UNDER_GRD:
				obj.x -= gcommon.cur_scroll_x
				obj.y -= gcommon.cur_scroll_y
			obj.x -= gcommon.cur_map_dx
			obj.y -= gcommon.cur_map_dy
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
			self.star_pos -= 0.2
			if self.star_pos<0:
				self.star_pos += 255

		gcommon.ObjMgr.drawDrawMapBackground()

		for obj in gcommon.ObjMgr.objs:
			if obj.layer==gcommon.C_LAYER_UNDER_GRD:
				obj.draw()
		
		gcommon.ObjMgr.drawDrawMap()
		
		# enemy(ground)
		for obj in gcommon.ObjMgr.objs:
			if obj.layer==gcommon.C_LAYER_GRD:
				if obj.hitcolor1 !=0 and obj.hit:
					pyxel.pal(obj.hitcolor1, obj.hitcolor2)
				
				obj.draw()
				if obj.hitcolor1 !=0 and obj.hit:
					pyxel.pal(obj.hitcolor1, obj.hitcolor1)

		# item
		for obj in gcommon.ObjMgr.objs:
			if obj.layer==gcommon.C_LAYER_ITEM:
				obj.draw()
		
		# enemy(sky)
		for obj in gcommon.ObjMgr.objs:
			if obj.layer==gcommon.C_LAYER_SKY:
				if obj.hitcolor1 !=0 and obj.hit:
					pyxel.pal(obj.hitcolor1, obj.hitcolor2)
				
				obj.draw()
				if obj.hitcolor1 !=0 and obj.hit:
					pyxel.pal(obj.hitcolor1, obj.hitcolor1)

		# enemy shot and explosion(sky)
		for obj in gcommon.ObjMgr.objs:
			if obj.layer==gcommon.C_LAYER_EXP_SKY or obj.layer==gcommon.C_LAYER_E_SHOT:
				obj.draw()

		# my shot
		for shot in gcommon.ObjMgr.shots:
		  shot.draw()

		# my ship
		gcommon.ObjMgr.myShip.draw()

		for obj in gcommon.ObjMgr.objs:
			if obj.layer==gcommon.C_LAYER_TEXT:
				obj.draw()
		
		
		pyxel.clip()
		# SCORE表示
		#pyxel.text(4, 194, "SC " + str(gcommon.score), 7)
		gcommon.showText2(0,192, "SC " + str(gcommon.score))
		# 残機
		pyxel.blt(232, 192, 0, 8, 32, 8, 8, gcommon.TP_COLOR)
		gcommon.showText2(242, 192, str(gcommon.remain))
		
		# 武器表示
		for i in range(0,3):
			if i == gcommon.ObjMgr.myShip.weapon == i:
				pyxel.blt(72 + 48*i, 192, 0, i * 48, 56, 48, 8)
			else:
				pyxel.blt(72 + 48*i, 192, 0, i * 48, 48, 48, 8)
			
		
		#pyxel.text(120, 184, str(gcommon.game_timer), 7)
		#pyxel.text(200, 188, str(len(gcommon.ObjMgr.objs)), 7)
		#pyxel.text(160, 188, str(self.event_pos),7)
		#pyxel.text(120, 194, str(gcommon.getMapData(gcommon.ObjMgr.myShip.x, gcommon.ObjMgr.myShip.y)), 7)
		# マップ位置表示
		#pyxel.text(200, 184, str(gcommon.map_x) + " " +str(gcommon.map_y), 7)

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
					shot.removeFlag = True
					shot.group.remove(shot)
					if len(shot.group.shots) == 0:
						gcommon.ObjMgr.shotGroups.remove(shot.group)
						
					if obj.removeFlag:
						break
		
		# my ship & enemy
		if gcommon.ObjMgr.myShip.sub_scene == 1:
			for obj in gcommon.ObjMgr.objs:
				if obj.hitCheck:
					if obj.checkMyShipCollision():
						self.my_broken()
						break
				#elif obj.layer==gcommon.C_LAYER_ITEM:
				#	if gcommon.check_collision(obj, gcommon.ObjMgr.myShip):
				#		self.catch_item(obj)
				#		obj.removeFlag = True


	def catch_item(self, obj):
		if obj.itype == gcommon.C_ITEM_PWUP:
			#pyxel.play(0, 7)
			gcommon.sound(gcommon.SOUND_PWUP)
			if gcommon.power < 3:
				gcommon.power += 1

	def my_broken(self):
		gcommon.ObjMgr.myShip.sub_scene = 2
		gcommon.ObjMgr.myShip.cnt = 0
		gcommon.power = gcommon.START_MY_POWER
		#sfx(4)
		#pyxel.play(0, 4)
		gcommon.sound(gcommon.SOUND_LARGE_EXP)

	def initEvent(self):
		if self.stage == 1:
			self.initEvent1()
		elif self.stage == 2:
			self.initEvent2()
		elif self.stage == 3:
			self.initEvent3()
	
	def initEvent1(self):
		self.eventTable =[ \
			[660,StartMapDraw1],		\
			[1560,SetMapScroll, 0.25, -0.25],	\
			[2180,SetMapScroll, 0.5, 0.0],
			[3260,SetMapScroll, 0.25, 0.25],
			[3460,SetMapScroll, 0, 0.5],
			[3860,SetMapScroll, 0.25, 0.25],
			[4600,SetMapScroll, 0.5, 0.0],
			[5800,EndMapDraw],		\
		]

	def initEvent2(self):
		self.eventTable =[ \
			[0,StartMapDraw2],		\
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
		]

	def initEvent3(self):
		self.eventTable =[ \
			[100,StartMapDraw3],		\
		]

	def initStory(self):
		if self.stage == 1:
			self.initStory1()
		elif self.stage == 2:
			self.initStory2()
		elif self.stage == 3:
			self.initStory3()

	def initStory1(self):
		self.story=[ \
			[150, enemy.Fan1Group, 8, 10, 6],		\
			[270, enemy.Fan1Group, 170, 10, 6],		\
			[360, enemy.Fan1Group, 8, 10, 6],		\
			[450, enemy.Fan1Group, 170, 10, 6],		\
			[500, enemy.MissileShip, 40, 160],		\
			[530, enemy.MissileShip, 120, 200],		\
			[630, enemy.RollingFighter1Group, 42, 15, 4],		\
			[700, enemy.Battery1, 2, 28, 1],		\
			[700, enemy.Battery1, 2, 42, 0],		\
			[720, enemy.RollingFighter1Group, 100, 15, 4],		\
			[730, enemy.Battery1, 8, 41, 0],		\
			[730, enemy.Battery1, 8, 29, 1],		\
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
			[2230, enemy.Jumper1, 256, 70, 0.1],		\
			[2260, enemy.Jumper1, 256, 70, 0.1],		\
			[2430, enemy.MissileShip, 82, 200],		\
			[2430, enemy.Battery1, 100, 7, 1],		\
			[2430, enemy.Battery1, 100, 24, 0],		\
			[2460, enemy.MissileShip, 82, 200],		\
			[2490, enemy.MissileShip, 82, 200],		\
			[2500, enemy.Battery1, 105, 7, 1],		\
			[2500, enemy.Battery1, 105, 24, 0],		\
			[2700, enemy.RollingFighter1Group, 24, 15, 4],		\
			[2760, enemy.RollingFighter1Group, 80, 15, 4],		\
			[3100, enemy.MissileShip, 40, 160],		\
			[3100, enemy.MissileShip, 80, 200],		\
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
			[4200, enemy.Battery1, 162, 60, 1],		\
			[4200, enemy.Battery1, 164, 60, 1],		\
			[4200, enemy.Jumper1, 256, 130, -0.1],		\
			[4400, enemy.Jumper1, 256, 100, 0.1],		\
			[4400, enemy.MissileShip, 80, 200],		\
			[4400, enemy.Battery1, 154, 81, 0],		\
			[4420, enemy.Battery1, 156, 81, 0],		\
			[4430, enemy.MissileShip, 120, 200],		\
			[4500, enemy.Jumper1, 256, 100, 0.1],		\
			[4500, enemy.Battery1, 170, 81, 0],		\
			[4520, enemy.Battery1, 172, 81, 0],		\
			[4530, enemy.Jumper1, 256, 120, 0.1],		\
			[4700, enemy.RollingFighter1Group, 60, 15, 4],		\
			[4730, enemy.RollingFighter1Group, 120, 15, 4],		\
			[4830, enemy.MissileShip, 120, 200],		\
			[4860, enemy.MissileShip, 80, 200],		\
			[5100, boss.Boss1, 256, 60],		\
			[5100, enemy.DockArm, 204, 59, 180],		\
			[5100, enemy.DockArm, 212, 59, 180],		\
			[5130, enemy.DockArm, 206, 59, 180],		\
			[5130, enemy.DockArm, 210, 59, 180],		\
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
			[2400, enemy.Worm1, 90, 91, 2, 4, 60],		\
			[2610, enemy.Worm1, 103, 75, 6, 5, 80],		\
			[2760, enemy.Worm1, 111, 69, 0, 5, 90],		\
			[2800, enemy.Worm1, 122, 74, 4, 5, 130],		\
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
			[3730, boss.Boss3],		\
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
	mapFile = open(fileName, mode = "r")
	lines = mapFile.readlines()
	mapFile.close()
	pyxel.tilemap(tm).set(0, 0, lines)

class App:
	def __init__(self):
		gcommon.app = self
	
		# コマンドライン解析
		parseCommandLine()
	
		pyxel.init(256, 200, caption="GRASLAY", fps=60)
 		
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
		self.setScene(Title())

	def setScene(self, nextScene):
		self.nextScene = nextScene

	def startGame(self, stage):
		self.stage = stage
		gcommon.remain = gcommon.START_REMAIN
		gcommon.power = gcommon.START_MY_POWER
		gcommon.score = 0
		self.setScene(MainGame(stage))

	def startStage(self, stage):
		self.stage = stage
		self.setScene(MainGame(stage))

	def startNextStage(self):
		if self.stage == 3:
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
		self.setScene(OptionMenu())

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
