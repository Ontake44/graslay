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
		self.setStartPosition()
		
	def update(self):
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
					gcommon.bomRemain = gcommon.START_BOM_REMAIN
					self.cnt = 0
					gcommon.power = gcommon.START_MY_POWER
					self.sprite = 1
					self.setStartPosition()
					self.x = -16
		elif self.sub_scene == 3:
			# 復活中
			self.x += 1
			if self.x >= 8:
				self.cnt = 0
				self.sub_scene = 4
		else: # sub_scene=4
			# 無敵中
			self.actionButtonInput()
			if self.cnt == 120:
				self.cnt = 0
				self.sub_scene=1

		self.cnt += 1

	
	
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
			self.y = self.y -2
			self.sprite = 2
			if self.y < 0:
				self.y = 0
		elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.GAMEPAD_1_DOWN):
			self.y = self.y +2
			self.sprite = 1
			if self.y > 176:
				self.y = 176
		if gcommon.game_timer > 30:
			if self.weapon == gcommon.WEAPON_ROUND:
				if gcommon.checkShotKey():
					doShot = False
					if self.prevFlag:
						self.shotCounter += 1
						if self.shotCounter > 5:
							self.shotCounter = 0
							doShot = True
					else:
						self.prevFlag = True
						self.shotCounter = 0
						doShot = True
					if doShot:
						self.shot()
						self.roundAngle += 6
						if self.roundAngle > 62:
							self.roundAngle = 62
				elif self.roundAngle > 0:
					self.shotCounter += 1
					if self.shotCounter > 5:
						self.shotCounter = 0
						self.shot()
						self.roundAngle -= 6
						if self.roundAngle < 0:
							self.roundAngle = 0
			else:
				if gcommon.checkShotKey():
					if self.prevFlag:
						self.shotCounter += 1
						if self.shotCounter > 4:
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
					self.x +7 * math.cos(r) * ((self.cnt/2+i)%20),	\
					self.y +7 * math.sin(r) * ((self.cnt/2+i)%20),	\
					7 + int(self.cnt%2)*3)
				# kore ha tekito
				r += 0.11 + i*0.04
		elif self.sub_scene==3 or self.sub_scene==4:
			if self.cnt%2 ==0:
				self.drawMyShip()
				
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
				self.shotMax = 4
				dx = 8 * math.cos(math.pi - math.pi/64 * self.roundAngle)
				dy = 8 * math.sin(math.pi - math.pi/64 * self.roundAngle)
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+6, self.y +4, dx, dy, 1)))
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+6, self.y +4, dx, -dy, 1)))
			else:
				self.shotMax = 3
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 6, 0, 2)))
				
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 5.5, 2.3, -3)))
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 5.5, -2.3, 3)))
				
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 4.2, 4.2, -3)))
				gcommon.ObjMgr.shots.append(shotGroup.append(self.createShot(self.x+12, self.y +4, 4.2, -4.2, 3)))
			
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
		self.top = -4
		self.right = 11
		self.bottom = 11
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
				no = gcommon.getMapData(self.x + 4, self.y + 4)
				if no >= 0 and gcommon.isMapFree(no) == False:
					self.remove()

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
OPTIONMENU_BOMB_STOCK = 1
OPTIONMENU_START_STAGE = 2
OPTIONMENU_SOUND = 3
OPTIONMENU_EXIT = 4

class OptionMenu:
	def __init__(self):
		self.menuPos = 0
	
	def update(self):
		if gcommon.checkUpP():
			self.menuPos -= 1
			if self.menuPos < 0:
				self.menuPos = 4
		if gcommon.checkDownP():
			self.menuPos += 1
			if self.menuPos > 4:
				self.menuPos = 0
		
		if gcommon.checkRightP():
			if self.menuPos == OPTIONMENU_PLAYER_STOCK:
				gcommon.START_REMAIN += 1
				if gcommon.START_REMAIN > 99:
					gcommon.START_REMAIN = 99
			elif self.menuPos == OPTIONMENU_BOMB_STOCK:
				gcommon.START_BOM_REMAIN += 1
				if gcommon.START_BOM_REMAIN > 5:
					gcommon.START_BOM_REMAIN = 5
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
			elif self.menuPos == OPTIONMENU_BOMB_STOCK:
				gcommon.START_BOM_REMAIN -= 1
				if gcommon.START_BOM_REMAIN < 0:
					gcommon.START_BOM_REMAIN = 0
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
		pyxel.bltm(0, 0, 1, 0, 0, 32, 32)
		gcommon.Text2(8, 8, "OPTION MENU", 7, 5)
		y = 50
		gcommon.Text2(30, y, "DIFFICULTY", 6, 5)
		gcommon.Text2(120, y, "NORMAL", 6, 5)
		y += 20
		
		gcommon.Text2(30, y, "PLAYER STOCK", self.getOptionColor(OPTIONMENU_PLAYER_STOCK), 5)
		gcommon.Text2(120, y, str(gcommon.START_REMAIN), self.getOptionColor(OPTIONMENU_PLAYER_STOCK), 5)
		y += 20

		gcommon.Text2(30, y, "BOMB STOCK", self.getOptionColor(OPTIONMENU_BOMB_STOCK), 5)
		gcommon.Text2(120, y, str(gcommon.START_BOM_REMAIN), self.getOptionColor(OPTIONMENU_BOMB_STOCK), 5)
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
		gcommon.map_x = -32 * 8
		
	def update(self):
		gcommon.map_x += gcommon.cur_scroll_x
		gcommon.map_y += gcommon.cur_scroll_y

	def draw(self):
		if gcommon.map_x < 0:
			pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), 0, 0, (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)
		else:
			pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), 0, (int)(gcommon.map_x/8), (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)


class StartMapDraw:
	def __init__(self, t):
		gcommon.drawMap = MapDraw()

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
		gcommon.ObjMgr.init()
		gcommon.ObjMgr.myShip = MyShip()
		gcommon.cur_scroll_x = 0.5
		self.story_pos = 0
		self.event_pos = 0
		self.stage = stage
		self.mapOffsetX = 0
		self.star_pos = 0
		gcommon.drawMap = None
		gcommon.game_timer = 0
		gcommon.map_x = 0
		gcommon.map_y = 24*8
		self.initStory()
		self.initEvent()
		
		self.skipGameTimer()
		
		if self.stage == 1:
			pyxel.image(1).load(0,0,"assets\graslay1.png")
			self.mapOffsetX = 0
			gcommon.draw_star = True
			loadMapData("assets\graslay1.pyxmap")
		#e#lif self.stage == 2:
		#	pyxel.image(1).load(0,0,"assets\gra-den2.png")
		#	self.mapOffsetX = 32
		#	gcommon.draw_star = False
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
			if gcommon.drawMap != None:
				gcommon.drawMap.update()
			
			gcommon.game_timer = gcommon.game_timer + 1	
	
	def update(self):
		self.ExecuteEvent()
		self.ExecuteStory()
		
		# MAP
		#gcommon.map_x += gcommon.cur_scroll_x
		#gcommon.map_y += gcommon.cur_scroll_y
		if gcommon.drawMap != None:
			gcommon.drawMap.update()
		
		# 自機移動
		gcommon.ObjMgr.myShip.update()
		
		newShots = []
		for shot in gcommon.ObjMgr.shots:
			shot.update()
			if shot.removeFlag == False:
				newShots.append(shot)
		gcommon.ObjMgr.shots = newShots

	
		newObjs = []
		for obj in gcommon.ObjMgr.objs:
			if obj.layer == gcommon.C_LAYER_GRD 	\
				or obj.layer==gcommon.C_LAYER_HIDE_GRD \
				or obj.layer==gcommon.C_LAYER_EXP_GRD \
				or obj.layer==gcommon.C_LAYER_UPPER_GRD \
				or obj.layer==gcommon.C_LAYER_UNDER_GRD:
				obj.x -= gcommon.cur_scroll_x
				obj.y -= gcommon.cur_scroll_y
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
		
		for obj in gcommon.ObjMgr.objs:
			if obj.layer==gcommon.C_LAYER_UNDER_GRD:
				obj.draw()
		
		if self.stage == 1:
			if gcommon.draw_star:
				for i in range(0,96):
					pyxel.pset(((int)(gcommon.star_ary[i][0]+self.star_pos))&255, i*2, gcommon.star_ary[i][1])
				
				self.star_pos -= 0.2
				if self.star_pos<0:
					self.star_pos += 255
			#pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), 0, (int)(gcommon.map_x/8), (int)(gcommon.map_y/8),33,33, gcommon.TP_COLOR)
			if gcommon.drawMap != None:
				gcommon.drawMap.draw()
		elif self.stage == 2:
			if gcommon.draw_star:
				for i in range(0,96):
					pyxel.pset((gcommon.star_ary[i][0]+self.star_pos)&255, self.star_pos+i*2, gcommon.star_ary[i][1])
				
				self.star_pos += 0.2
				if self.star_pos>255:
					self.star_pos -= 255

			#for obj in gcommon.ObjMgr.objs:
			#	if obj.layer==gcommon.C_LAYER_UNDER_GRD:
			#		if obj.hitcolor1 !=0 and obj.hit:
			#			pyxel.pal(obj.hitcolor1, obj.hitcolor2)
			#		obj.draw()
			#		if obj.hitcolor1 !=0 and obj.hit:
			#			pyxel.pal(obj.hitcolor1, obj.hitcolor1)
			# map
			pyxel.bltm(0,-8+int(gcommon.map_y)%8, 0, self.mapOffsetX,(256-33)-(int)(gcommon.map_y/8),32,33, gcommon.TP_COLOR)
		elif self.stage == 3:
			if gcommon.draw_star:
				for i in range(0,128):
					pyxel.pset(gcommon.star_ary[i][0], (self.star_pos+i*2)%255, gcommon.star_ary[i][1])
				
				self.star_pos += 0.2
				if self.star_pos>255:
					self.star_pos -= 255

			for obj in gcommon.ObjMgr.objs:
				if obj.layer==gcommon.C_LAYER_UNDER_GRD:
					if obj.hitcolor1 !=0 and obj.hit:
						pyxel.pal(obj.hitcolor1, obj.hitcolor2)
					obj.draw()
					if obj.hitcolor1 !=0 and obj.hit:
						pyxel.pal(obj.hitcolor1, obj.hitcolor1)
			# map
			if gcommon.map_y < 1664:
				pyxel.bltm(0,-8+int(gcommon.map_y)%8, 0, self.mapOffsetX,(256-33)-(int)(gcommon.map_y/8),32,33, gcommon.TP_COLOR)
		
		
		# enemy(ground)
		for obj in gcommon.ObjMgr.objs:
			if obj.layer==gcommon.C_LAYER_GRD or obj.layer==gcommon.C_LAYER_HIDE_GRD:
				if obj.hitcolor1 !=0 and obj.hit:
					pyxel.pal(obj.hitcolor1, obj.hitcolor2)
				
				obj.draw()
				if obj.hitcolor1 !=0 and obj.hit:
					pyxel.pal(obj.hitcolor1, obj.hitcolor1)

		# explosion(ground)
		for obj in gcommon.ObjMgr.objs:
			if obj.layer==gcommon.C_LAYER_EXP_GRD:
				obj.draw()

		# upper ground
		for obj in gcommon.ObjMgr.objs:
			if obj.layer==gcommon.C_LAYER_UPPER_GRD:
				obj.draw()

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
		pyxel.text(4, 194, "SCORE " + str(gcommon.score), 7)
		# 残機
		pyxel.blt(232, 192, 0, 48, 32, 6, 8, gcommon.C_COLOR_KEY)
		pyxel.text(242, 192, str(gcommon.remain), 7)
		
		# 武器表示
		for i in range(0,3):
			if i == gcommon.ObjMgr.myShip.weapon == i:
				pyxel.blt(72 + 48*i, 192, 0, i * 48, 56, 48, 8)
			else:
				pyxel.blt(72 + 48*i, 192, 0, i * 48, 48, 48, 8)
			
		
		pyxel.text(120, 188, str(gcommon.game_timer), 7)
		#pyxel.text(120, 194, str(gcommon.getMapData(gcommon.ObjMgr.myShip.x, gcommon.ObjMgr.myShip.y)), 7)
		# マップ位置表示
		#pyxel.text(0, 192, str(gcommon.map_x), 7)

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
				if shot.removeFlag == False and gcommon.check_collision(obj, shot):
					obj.hp -= gcommon.SHOT_POWER
					if obj.hp <= 0:
						obj.broken()
					else:
						obj.hit = True
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
					if gcommon.check_collision(obj, gcommon.ObjMgr.myShip):
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
		gcommon.bomRemain = gcommon.START_BOM_REMAIN
		#sfx(4)
		#pyxel.play(0, 4)
		gcommon.sound(gcommon.SOUND_LARGE_EXP)

	def initEvent(self):
		if self.stage == 1:
			self.initEvent1()
	
	def initEvent1(self):
		self.eventTable =[ \
			[660,StartMapDraw],		\
			[1560,SetMapScroll, 0.25, -0.25],	\
			[2180,SetMapScroll, 0.5, 0.0],
			[3260,SetMapScroll, 0.25, 0.25],
			[3460,SetMapScroll, 0, 0.5],
			[3860,SetMapScroll, 0.25, 0.25],
			[4600,SetMapScroll, 0.5, 0.0],
			[5800,EndMapDraw],		\
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
		]

	def initStory3(self):
		self.story=[ \
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

def loadMapData(fileName):
	mapFile = open(fileName, mode = "r")
	lines = mapFile.readlines()
	mapFile.close()
	pyxel.tilemap(0).set(0, 0, lines)

class App:
	def __init__(self):
		gcommon.app = self
	
		# コマンドライン解析
		parseCommandLine()
	
		pyxel.init(256, 200, caption="GRASLAY", fps=60)
 		
		#pyxel.load("assets/graslay.pyxres")
		pyxel.image(0).load(0,0,"assets\graslay0.png")
		
		gcommon.init_atan_table()
		gcommon.initStar()
		
		#self.scene = MainGame()
		self.scene = Title()
		self.stage = 0
		pyxel.run(self.update, self.draw)

	def startTitle(self):
		self.scene = Title()

	def startGame(self, stage):
		self.stage = stage
		gcommon.remain = gcommon.START_REMAIN
		gcommon.power = gcommon.START_MY_POWER
		gcommon.score = 0
		self.scene = MainGame(stage)

	def startStage(self, stage):
		self.stage = stage
		self.scene = MainGame(stage)

	def startNextStage(self):
		self.startStage(self.stage+1)

	def startGameOver(self):
		self.scene = GameOver()

	def startStageClear(self, stage):
		self.scene = StageClear(stage)

	def startGameClear(self):
		self.scene = GameClear()

	def startOption(self):
		self.scene = OptionMenu()

	def update(self):
		if pyxel.btnp(pyxel.KEY_Q):
			pyxel.quit()

		self.scene.update()

	def draw(self):
		self.scene.draw()


App()
