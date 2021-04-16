import pyxel
import math
import random
import sys
import os
import gcommon
import enemy
from myShip import MyShipA
from myShip import MyShipB
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
from mapDraw import MapDrawWarehouse
from mapDraw import MapDraw3
from mapDraw import MapDraw4
from mapDraw import MapDrawFactory
from mapDraw import MapDrawLast


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

class StartMapDraw:
	def __init__(self, t):
		gcommon.ObjMgr.setDrawMap(t[2]())

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
		if gcommon.GameSession.weaponType == gcommon.WeaponType.TYPE_A:
			gcommon.ObjMgr.myShip = MyShipA(self)
		else:
			gcommon.ObjMgr.myShip = MyShipB(self)
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
			gcommon.Rect.createWH(127-32 +10, 192/2 -32 +35,  80-8, 8),
			gcommon.Rect.createWH(127-32 +10, 192/2 -32 +45,  80-8, 8)
		]
		self.pauseMouseOnOffRects = [
			gcommon.Rect.createWH(127-32 +10 +26, 192/2 -32 +26 -1,  8, 8),
			gcommon.Rect.createWH(127-32 +10 +48, 192/2 -32 +26 -1,  8, 8)
		]
		self.pauseCnt = 0
		pyxel.mouse(False)

		#elif self.stage == 3:
		#	pyxel.image(1).load(0,0,"assets\gra-den3a.png")
		#	pyxel.image(2).load(0,0,"assets\gra-den3b.png")
		#	self.mapOffsetX = 64
		#	gcommon.draw_star = True
		self.initStage()

		self.skipGameTimer()

		pyxel.tilemap(0).refimg = 1
		gcommon.mapFreeTable = [0, 32, 33, 34, 65, 66]

	def initStage(self):
		self.initStageRouteA()

	def initStageRouteA(self):
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
			# 倉庫
			pyxel.image(1).load(0,0,"assets/stage_warehouse.png")
			pyxel.image(2).load(0,0,"assets/stage_warehouse-2.png")
			self.mapOffsetX = 0
			gcommon.sync_map_y = 0
			gcommon.long_map = True
			gcommon.draw_star = False
			gcommon.eshot_sync_scroll = False
			loadMapData(0, "assets/stage_warehouse0.pyxmap")
			loadMapData(2, "assets/stage_warehouse1.pyxmap")
			loadMapData(7, "assets/stage_warehouseb.pyxmap")
			pyxel.tilemap(0).refimg = 1
			pyxel.tilemap(2).refimg = 1
			pyxel.tilemap(7).refimg = 1  # background
			loadMapAttribute("assets/stage_warehouse.mapatr")
		elif self.stage == 4:
			# 高速スクロール
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
		elif self.stage == 5:
			# 遺跡
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
		elif self.stage == 6:
			# ファクトリー
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
		elif self.stage == 7:
			# 最終ステージ
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
			self.pauseMenuPos = (self.pauseMenuPos - 1) % 4
			return
		elif gcommon.checkDownP():
			self.pauseMenuPos = (self.pauseMenuPos + 1) % 4
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
				# MOUSE OFF/ON
				n = -1
				if self.mouseManager.visible:
					n = gcommon.checkMouseMenuPos(self.pauseMouseOnOffRects)
				if gcommon.checkRightP() or (gcommon.checkShotKeyP() and n == 1):
					gcommon.Settings.mouseEnabled = True
				elif gcommon.checkLeftP() or (gcommon.checkShotKeyP() and n == 0):
					gcommon.Settings.mouseEnabled = False
			elif self.pauseMenuPos == 2:
				if gcommon.checkShotKeyRectP(self.pauseMenuRects[self.pauseMenuPos]):
					# TITLE
					gcommon.app.startTitle()
			elif self.pauseMenuPos == 3:
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

		# my ship
		gcommon.ObjMgr.myShip.draw0()

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

		gcommon.ObjMgr.drawDrawMap2()

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
		if gcommon.GameSession.weaponType == gcommon.WeaponType.TYPE_A:
			for i in range(0,3):
				if i == gcommon.ObjMgr.myShip.weapon:
					pyxel.blt(96 + 40*i, 192, 0, 128+ i * 40, 248, 40, 8)
				else:
					pyxel.blt(96 + 40*i, 192, 0, 128+ i * 40, 240, 40, 8)
		else:
			for i in range(0,4):
				if i == gcommon.ObjMgr.myShip.weapon:
					pyxel.blt(96 + 32*i, 192, 0, 128+ i * 32, 232, 40, 8)
				else:
					pyxel.blt(96 + 32*i, 192, 0, 128+ i * 32, 224, 40, 8)
		
		#pyxel.text(120, 184, str(gcommon.back_map_x), 7)
		if gcommon.DebugMode:
			pyxel.text(120, 184, str(gcommon.game_timer), 7)
			pyxel.text(160, 184, str(len(gcommon.ObjMgr.objs)), 7)
			#pyxel.text(160, 184, str(len(gcommon.ObjMgr.shots)), 7)
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
		# PAUSEメニューはベタ描き
		pyxel.rect(127 -40, 192/2 -32, 80, 60, 0)
		pyxel.rectb(127 -39, 192/2 -31, 78, 58, 7)
		pyxel.rect(127 -37, 192/2 -29, 74, 8, 1)
		pyxel.text(127 -40 + 28, 192/2 -32 +4, "PAUSE", 7)

		pyxel.rect(127 -40+4, 192/2 -32 +15 + self.pauseMenuPos * 10, 80-8, 8, 2)

		pyxel.text(127-32 +4, 192/2 -32 +16, "CONTINUE", 7)
		
		#MOUSE
		y = 192/2 -32 +26
		pyxel.text(127-32 +4, y, "MOUSE", 7)

		leftMarker = (gcommon.Settings.mouseEnabled == True)
		pyxel.text(127-32 +10 +36, y, "ON " if gcommon.Settings.mouseEnabled else "OFF", 7)
		gcommon.drawLeftMarker(127-32 +10 +26, y -1, leftMarker)
		gcommon.drawRightMarker(127-32 +10 +48, y -1, not leftMarker)

		pyxel.text(127-32 +4, 192/2 -32 +36, "TITLE", 7)
		pyxel.text(127-32 +4, 192/2 -32 +46, "EXIT", 7)

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
					broken = obj.doShotCollision(shot)
					shot.hit(obj, broken)
					if broken or obj.removeFlag:
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
			self.initEventWarehouse()
		elif self.stage == 4:
			self.initEvent3()
		elif self.stage == 5:
			self.initEvent4()
		elif self.stage == 6:
			self.initEventFactory()
		elif self.stage == 7:
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

	def initEventWarehouse(self):
		self.eventTable =[ \
			[0, StartBGM, gcommon.BGM.STAGE5],
			[0,StartMapDraw, MapDrawWarehouse],		\
			[2184,SetMapScroll, 0.0, 0.5],
			[3384,SetMapScroll, 0.5, 0.0],
			[4712,SetMapScroll, 0.0, -0.5],
			[5504,SetMapScroll, 0.5, 0.0],
			[6800, StartBGM, gcommon.BGM.BOSS],
			[7320,SetMapScroll, 0.0, 0.0],
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
			self.story = story.Story.getStoryWarehouse()
		elif self.stage == 4:
			self.story = story.Story.getStory3()
		elif self.stage == 5:
			self.story = story.Story.getStory4()
		elif self.stage == 6:
			self.story = story.Story.getStoryFactory()
		elif self.stage == 7:
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
		gcommon.GameSession.initNormal(difficulty)
		gcommon.GameSession.credits -= 1
		gcommon.GameSession.playerStock -= 1
		gcommon.GameSession.weaponType = gcommon.WeaponType.TYPE_A
		# 発艦
		self.setScene(launch.LaunchScene())
		
		# Ending Test
		#self.setScene(ending.EndingScene())

	def startMainGame(self):
		self.setScene(MainGame(1))

	def startCustomGame(self):
		#print("Difficulty : " + str(difficulty))
		if gcommon.CustomNormal:
			# カスタムでも通常にしたい場合（デバッグ）
			gcommon.GameSession.init(gcommon.Settings.difficulty, gcommon.Settings.playerStock, gcommon.GAMEMODE_NORMAL, gcommon.Settings.startStage, 1)
		else:
			# 通常
			gcommon.GameSession.init(gcommon.Settings.difficulty, gcommon.Settings.playerStock, gcommon.GAMEMODE_CUSTOM, gcommon.Settings.startStage, 1)
		gcommon.GameSession.playerStock -= 1
		gcommon.GameSession.weaponType = gcommon.Settings.weaponType
		gcommon.GameSession.multipleCount = gcommon.Settings.multipleCount
		self.stage = gcommon.Settings.startStage
		self.setScene(MainGame(self.stage))

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
