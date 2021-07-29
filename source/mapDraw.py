import math
from typing import get_origin
import pyxel
import gcommon
import enemy
import item
import enemyBattery
import enemyCreature
import enemyOthers
from objMgr import ObjMgr
from gameSession import GameSession
from drawing import Drawing

def doMapCharacter(n, mx, my):
	if n in (426, 427):
		gcommon.setMapDataByMapPos(mx, my, 0)
		item.ScoreItem1.createByMapPos(mx, my, (n==427))
		return True
	elif n in (428, 429):
		gcommon.setMapDataByMapPos(mx, my, 0)
		item.OneUpItem1.createByMapPos(mx, my, (n==429))
		return True
	else:
		return False

# def doMapCharacter2(n, mx, my, tbl):
# 	if n in (tbl[0], tbl[0]+1):
# 		gcommon.setMapDataByMapPos(mx, my, 0)
# 		item.createByMapPos(mx, my, (n==tbl[0]+1))
# 		return True
# 	elif n in (tbl[1], tbl[1]+1):
# 		gcommon.setMapDataByMapPos(mx, my, 0)
# 		item.OneUpItem1.createByMapPos(mx, my, (n==tbl[1]+1))
# 		return True
# 	else:
# 		return False

class MapData:
	@classmethod
	def loadMapData(cls, tm, fileName):
		mapFile = open(gcommon.resource_path(fileName), mode = "r")
		lines = mapFile.readlines()
		mapFile.close()
		pyxel.tilemap(tm).set(0, 0, lines)

	@classmethod
	def loadMapAttribute(cls, fileName):
		attrFile = open(gcommon.resource_path(fileName), mode = "r")
		gcommon.mapAttribute = attrFile.readlines()
		attrFile.close()


class MapDraw1:
	def __init__(self):
		pass
	
	def init(self):
		gcommon.map_x = -32 * 8
		gcommon.map_y = 24*8
		gcommon.mapHeight = 8 * 256

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
					ObjMgr.addObj(obj)
				else:
					# 共通のマップキャラクタ処理
					doMapCharacter(n, mx, my)
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

	def draw2(self):
		pass

class MapDraw2:
	def __init__(self):
		pass
	
	def init(self):
		gcommon.map_x = 0
		gcommon.map_y = 24*8
		gcommon.mapHeight = 8 * 256

	def update0(self, skip):
		pass

	def update(self, skip):
		if skip == False:
			# スキップ時はマップデータやオブジェクト追加しない
			for my in range(0, 128):
				mx = gcommon.screenPosToMapPosX(256)
				n = gcommon.getMapDataByMapPos(mx, my)
				# 共通のマップキャラクタ処理
				doMapCharacter(n, mx, my)
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

	def draw2(self):
		pass

# 洞窟
class MapDrawCave:
	def __init__(self):
		self.shiftList = []
		for i in range(32):
			n = int(3* math.sin(i * math.pi/16))
			self.shiftList.append(n)
	
	def init(self):
		gcommon.map_x = 0
		gcommon.map_y = 8*8
		gcommon.back_map_x = 0		#-32 * 8/2
		gcommon.back_map_y = 0
		gcommon.mapHeight = 8 * 256
		gcommon.waterSurface_y = 93 * 8.0

	def update0(self, skip):
		pass

	def update(self, skip):
		if skip == False:
			# スキップ時はマップデータやオブジェクト追加しない
			for my in range(0, 128):
				mx = gcommon.screenPosToMapPosX(256)
				n = gcommon.getMapDataByMapPosPage(0, mx, my)
				if n in (390, 391):
					# 植物砲台
					gcommon.setMapDataByMapPosPage(0, mx, my, 0)
					mirror = 0
					if n == 391:
						mirror = 1
						my -= 1
					obj = enemyBattery.PlantBattery1([0,0,mx, my, mirror, 90])
					if GameSession.isHard():
						obj.first = 20
					ObjMgr.addObj(obj)
				elif n in (392, 393):
					# 植物砲台
					gcommon.setMapDataByMapPosPage(0, mx, my, 0)
					mirror = 0
					if n == 393:
						mirror = 1
						my -= 1
					obj = enemyBattery.PlantBattery2([0,0,mx, my, mirror, 90])
					if GameSession.isHard():
						obj.first = 20
					ObjMgr.addObj(obj)
				elif n in (394, 395):
					gcommon.setMapDataByMapPosPage(0, mx, my, 0)
					time = gcommon.getMapDataByMapPos(mx+1, my) -416
					gcommon.setMapDataByMapPosPage(0, mx+1, my, 0)
					mirror = 0
					if n == 395:
						mirror = 1
					obj = enemyCreature.CellLauncher1([0,0,mx, my, mirror, time])
					ObjMgr.addObj(obj)
				else:
					doMapCharacter(n, mx, my)
		gcommon.map_x += gcommon.cur_scroll_x
		gcommon.map_y += gcommon.cur_scroll_y
		gcommon.map_y += gcommon.cur_map_dy
		gcommon.back_map_x += gcommon.cur_scroll_x/2
		gcommon.back_map_y += gcommon.cur_scroll_y/2

	def drawBackground(self):
		wy = gcommon.waterSurface_y - gcommon.map_y
		# 通常表示
		bx = int(gcommon.back_map_x)
		if bx < 0:
			pyxel.bltm(-1 * bx, -1 * (int(gcommon.back_map_y) % 8), 1, 0, (int)(gcommon.back_map_y/8), 33, 33)
		else:
			mx = (int)(bx/8)
			pyxel.bltm(-1 * (bx % 8), -1 * (int(gcommon.back_map_y) % 8), 1, mx, (int)(gcommon.back_map_y/8), 33, 33)
		if wy >= 0 and wy <= gcommon.SCREEN_MAX_Y:
			i = 0
			# 8を足しているが、destx > sourcexで、近い場合だと描画がおかしくなるみたいなので
			# ※sourcexがマイナスになるのが問題ではないようだ
			while( wy <= gcommon.SCREEN_MAX_Y ):
				pyxel.blt(0, wy, 4, 8 + self.shiftList[(int(wy + (pyxel.frame_count>>3))) & 31], wy, 256, 1)
				i += 1
				wy += 1


	def draw(self):
		tm = 0
		if gcommon.map_x < 0:
			pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), tm, 0, (int)(gcommon.map_y/8),33,33, 2)
		else:
			#tm = 1 + int(gcommon.map_x/4096)
			moffset = (int(gcommon.map_x/2048) & 1) * 128
			w = int((gcommon.map_x %2048)/8)
			pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm, (int)((gcommon.map_x % 2048)/8), moffset + (int)(gcommon.map_y/8),33,25, 2)
			if w >= 224:
				tm2 = tm + int((gcommon.map_x+256)/4096)
				moffset2 = (int((gcommon.map_x+256)/2048) & 1) * 128
				pyxel.bltm((256-w)*8 -1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm2, 0, moffset2 + (int)(gcommon.map_y/8),33,33, 2)

	def draw2(self):
		wy = int(gcommon.waterSurface_y - gcommon.map_y)
		if wy < 0:
			wy = 0
		if wy <= gcommon.SCREEN_MAX_Y:
			Drawing.setBrightness1()
			pyxel.blt(0, wy, 4, 0, wy, 256, 200)
			pyxel.pal()
		x = -8 + (int(gcommon.map_x) & 7)
		while(x < gcommon.SCREEN_MAX_X):
			pyxel.blt(x, wy, 1, 0, 88, 8 + ((pyxel.frame_count>>2) & 1)*8, 16, 0)
			x += 8


# 倉庫ステージ
class MapDrawWarehouse:
	def __init__(self):
		pass
	
	def init(self):
		gcommon.map_x = -32 * 8
		gcommon.map_y = 20*8
		gcommon.back_map_x = 0		#-32 * 8/2
		gcommon.back_map_y = 0
		gcommon.mapHeight = 8 * 256

	def update0(self, skip):
		pass

	def update(self, skip):
		if skip == False:
			# スキップ時はマップデータやオブジェクト追加しない
			for i in range(0, 128):
				my = 127 -i
				mx = gcommon.screenPosToMapPosX(256)
				n = gcommon.getMapDataByMapPosPage(2, mx, my)
				if n in (390, 391):
					# 砲台
					gcommon.setMapDataByMapPosPage(2, mx, my, 0)
					obj = enemy.Battery1([0,0,mx, my, 0])
					if GameSession.isHard():
						obj.first = 20
						obj.shot_speed = 3
					if n == 391:
						obj.mirror = 1
					ObjMgr.addObj(obj)
				else:
					n = gcommon.getMapDataByMapPosPage(5, mx, my)
					gcommon.setMapDataByMapPosPage(5, mx, my, 0)
					if n in (426, 427):
						item.ScoreItem1.createByMapPos(mx, my, hide=(n==427), offsetX=-4, offsetY=-4)
					elif n in (428, 429):
						item.OneUpItem1.createByMapPos(mx, my, hide=(n==429), offsetX=-4, offsetY=-4)
		gcommon.map_x += gcommon.cur_scroll_x
		gcommon.map_y += gcommon.cur_scroll_y
		gcommon.back_map_x += gcommon.cur_scroll_x/2

	def drawBackground(self):
		if gcommon.back_map_x < 0:
			pyxel.bltm(-1 * int(gcommon.back_map_x), 0, 7, 0, 24,33,33,3)
		else:
			mx = (int)(gcommon.back_map_x/8)
			pyxel.bltm(-1 * (int(gcommon.back_map_x) % 8), 0, 7, mx, 24,33,33, 3)

	def draw(self):
		tm = 2
		if gcommon.map_x < 0:
			pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), tm, 0, (int)(gcommon.map_y/8),33,33, 3)
		else:
			#tm = 1 + int(gcommon.map_x/4096)
			moffset = (int(gcommon.map_x/2048) & 1) * 128
			w = int((gcommon.map_x %2048)/8)
			pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm, (int)((gcommon.map_x % 2048)/8), moffset + (int)(gcommon.map_y/8),33,25, 3)
			if w >= 224:
				tm2 = tm + int((gcommon.map_x+256)/4096)
				moffset2 = (int((gcommon.map_x+256)/2048) & 1) * 128
				pyxel.bltm((256-w)*8 -1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm2, 0, moffset2 + (int)(gcommon.map_y/8),33,33, 3)
		# 上下ループマップなのでややこしい
		# if gcommon.map_x < 0:
		# 	pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), 0, 0, (int)(gcommon.map_y/8),33,33, 3)
		# else:
		# 	tm = int(gcommon.map_x/4096)
		# 	moffset = (int(gcommon.map_x/2048) & 1) * 128
		# 	w = int((gcommon.map_x %2048)/8)
		# 	pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm, (int)((gcommon.map_x % 2048)/8), moffset + (int)(gcommon.map_y/8),33,25, 3)
		# 	if w >= 224:
		# 		tm2 = int((gcommon.map_x+256)/4096)
		# 		moffset2 = (int((gcommon.map_x+256)/2048) & 1) * 128
		# 		pyxel.bltm((256-w)*8 -1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm2, 0, moffset2 + (int)(gcommon.map_y/8),33,33, 3)

	def draw2(self):
		tm = 0
		if gcommon.map_x < 0:
			pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), tm, 0, (int)(gcommon.map_y/8),33,33, 3)
		else:
			#tm = 1 + int(gcommon.map_x/4096)
			moffset = (int(gcommon.map_x/2048) & 1) * 128
			w = int((gcommon.map_x %2048)/8)
			pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm, (int)((gcommon.map_x % 2048)/8), moffset + (int)(gcommon.map_y/8),33,25, 3)
			if w >= 224:
				tm2 = int((gcommon.map_x+256)/4096)
				moffset2 = (int((gcommon.map_x+256)/2048) & 1) * 128
				pyxel.bltm((256-w)*8 -1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm2, 0, moffset2 + (int)(gcommon.map_y/8),33,33, 3)
			# if w >= 224:
			# 	tm2 = int((gcommon.map_x+256)/4096)
			# 	moffset2 = (int((gcommon.map_x+256)/2048) & 1) * 128
			# 	pyxel.bltm((256-w)*8 -1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm2, 1, moffset2 + (int)(gcommon.map_y/8),33,33, 3)


class MapDraw3:
	def __init__(self):
		pass

	def init(self):
		gcommon.map_x = -32 * 8
		gcommon.map_y = 24*8
		gcommon.mapHeight = 8 * 128
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
			if gcommon.game_timer >= 3730+128:
				gcommon.map_y = 336
			else:
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
						if GameSession.isHard():
							obj.first = 20
							obj.shot_speed = 3
						if n == 391:
							obj.mirror = 1
						ObjMgr.addObj(obj)
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
						ObjMgr.addObj(obj)
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
						ObjMgr.addObj(obj)
					elif n == 398:
						# 固定シャッター
						size = gcommon.getMapDataByMapPos(mx+1, my) -576
						if GameSession.isEasy():
							gcommon.setMapDataByMapPos2(mx, my, 0, 2, 1)
							obj = enemy.FixedShutter1(mx, my, size)
							ObjMgr.addObj(obj)
						else:
							gcommon.setMapDataByMapPos2(mx, my, 11, 2, size *2)
					else:
						# 共通のマップキャラクタ処理
						doMapCharacter(n, mx, my)
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

	def draw2(self):
		pass

class MapDraw4:
	def __init__(self):
		pass
	
	def init(self):
		gcommon.map_x = -32 * 8
		gcommon.map_y = 24*8
		gcommon.mapHeight = 8 * 256
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
					ObjMgr.addObj(obj)
				elif n == 395:
					# 床
					size = gcommon.getMapDataByMapPos(mx+1, my) -576
					obj = enemy.RuinFloor1(mx, my, 1, size)
					ObjMgr.addObj(obj)
				if n == 396:
					# 柱
					size = gcommon.getMapDataByMapPos(mx+1, my) -576
					obj = enemy.RuinPillar1(mx, my, -1, size)
					ObjMgr.addObj(obj)
				elif n == 397:
					# 床
					size = gcommon.getMapDataByMapPos(mx+1, my) -576
					obj = enemy.RuinFloor1(mx, my, -1, size)
					ObjMgr.addObj(obj)
				elif n in (390, 391):
					# 砲台
					ObjMgr.addObj(enemy.Battery2(mx, my, 1 if n==390 else -1))
				else:
					# 共通のマップキャラクタ処理
					doMapCharacter(n, mx, my)
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

	def draw2(self):
		pass

class MapDrawFactory:
	def __init__(self):
		pass

	def init(self):
		gcommon.map_x = -32 * 8
		gcommon.map_y = 24*8
		gcommon.mapHeight = 8 * 256
		gcommon.cur_scroll_x = 0.5
		gcommon.cur_scroll_y = 0.0
		gcommon.back_map_x = -32 * 8
		gcommon.back_map_y = 0

	def update0(self, skip):
		if gcommon.game_timer == 3550:
			gcommon.sync_map_y = 0
			gcommon.cur_map_dy = 0

	def update(self, skip):
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
						obj = enemy.Battery1([0,0,mx, my, 0 if n == 390 else 1])
						obj.first = 20
						ObjMgr.addObj(obj)
					elif n in (394, 395):
						# サーキュレーター
						gcommon.setMapDataByMapPos(mx, my, 0)
						pos = gcommon.mapPosToScreenPos(mx, my)
						if n == 394:
							obj = enemy.Circulator1(pos[0] +85, pos[1] +3, 1)
						else:
							obj = enemy.Circulator1(pos[0] +85, pos[1] +3, -1)
						ObjMgr.addObj(obj)
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
						ObjMgr.addObj(obj)
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
						ObjMgr.addObj(enemy.Wind1.create(mx, my, dr, size))
					elif n == 402:
						gcommon.setMapDataByMapPos(mx, my, 0)
						ObjMgr.addObj(enemy.LiftAppear1(mx, my, -1))
					elif n == 403:
						gcommon.setMapDataByMapPos(mx, my, 0)
						ObjMgr.addObj(enemy.LiftAppear1(mx, my, 1))
					else:
						# 共通のマップキャラクタ処理
						doMapCharacter(n, mx, my)
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

	def draw2(self):
		pass

class MapDrawFire:
	def __init__(self):
		self.cnt = 0
		self.shiftList = []
		for i in range(32):
			n = int(5* math.sin(i * math.pi/16))
			self.shiftList.append(n)
	
	def init(self):
		gcommon.map_x = 0 * 8
		gcommon.map_y = 0 *8
		gcommon.back_map_x = 0		#-32 * 8/2
		gcommon.back_map_y = 0
		gcommon.mapHeight = 8 * 256

	def update0(self, skip):
		pass

	def update(self, skip):
		if skip == False:
			# スキップ時はマップデータやオブジェクト追加しない
			for i in range(0, 128):
				my = 127 -i
				mx = gcommon.screenPosToMapPosX(256)
				n = gcommon.getMapDataByMapPosPage(0, mx, my)
				if n in (964, 965):
					# 砲台
					gcommon.setMapDataByMapPos(mx, my, 0)
					ObjMgr.addObj(enemyBattery.FireBattery1(mx, my, 0 if n == 964 else 1))
				elif n in (966, 967):
					# 炎
					p = gcommon.getMapDataByMapPos(mx +1, my)
					gcommon.setMapDataByMapPos2(mx, my, 0, 2, 1)
					if p > 992:
						pattern = p -992
					else:
						pattern = 0
					ObjMgr.addObj(enemyOthers.FireChimney1(mx, my, -1 if n == 966 else 1, pattern))
				elif n in (960, 961):
					gcommon.setMapDataByMapPos(mx, my, 0)
					item.ScoreItem1.createByMapPos(mx, my, (n==961))
				elif n in (962, 963):
					gcommon.setMapDataByMapPos(mx, my, 0)
					item.OneUpItem1.createByMapPos(mx, my, (n==963))

		gcommon.map_x += gcommon.cur_scroll_x
		gcommon.map_y += gcommon.cur_scroll_y
		gcommon.back_map_x += gcommon.cur_scroll_x/2
		self.cnt += 1

	def drawBackground(self):
		pass
		# if gcommon.back_map_x < 0:
		# 	pyxel.bltm(-1 * int(gcommon.back_map_x), 0, 7, 0, 24,33,33,3)
		# else:
		# 	mx = (int)(gcommon.back_map_x/8)
		# 	pyxel.bltm(-1 * (int(gcommon.back_map_x) % 8), 0, 7, mx, 24,33,33, 3)

	def draw(self):
		# プロミネンス？を描く
		tm = 2
		m = ((self.cnt>>3) % 3) * 7
		mx = int(gcommon.map_x) & 127
		pyxel.bltm(-1 * (mx % 8), 0, tm, int(mx/8), m,33, 7, 3)
		count = 7 *8
		y = 0
		while( count > 0 ):
			#pyxel.blt(0, y -1, 4, 8 + self.shiftList[(int(self.cnt>>3)) & 31], y, 256, 1)
			offset = 8 + self.shiftList[(y +int(self.cnt>>2)) & 31]
			pyxel.blt(0, 192- 7*8 + y, 4, offset, y, 256, 1)
			pyxel.blt(256 -offset, 192- 7*8 + y, 4, 0, y, offset, 1)
			count -=1
			y += 1
		pyxel.blt(0, 0, 4, 0, 192 -7*8, 256, -7*8)

	def draw2(self):
		#tm = 0
		#pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm, (int)((gcommon.map_x % 2048)/8), (int)(gcommon.map_y/8),33,25, 3)
		tm = 0
		if gcommon.map_x < 0:
			pyxel.bltm(-1 * int(gcommon.map_x), -1 * (int(gcommon.map_y) % 8), tm, 0, (int)(gcommon.map_y/8),33,33, 3)
		else:
			moffset = (int(gcommon.map_x/2048) & 1) * 128
			w = int((gcommon.map_x %2048)/8)
			pyxel.bltm(-1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm, (int)((gcommon.map_x % 2048)/8), moffset + (int)(gcommon.map_y/8),33,25, 3)
			if w >= 224:
				tm2 = tm + int((gcommon.map_x+256)/4096)
				moffset2 = (int((gcommon.map_x+256)/2048) & 1) * 128
				pyxel.bltm((256-w)*8 -1 * (int(gcommon.map_x) % 8), -1 * (int(gcommon.map_y) % 8), tm2, 0, moffset2 + (int)(gcommon.map_y/8),33,33, 3)


class MapDrawLast:
	def __init__(self):
		pass
	
	def init(self):
		gcommon.map_x = -32 * 8
		gcommon.map_y = 24*8
		gcommon.mapHeight = 8 * 256
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
					ObjMgr.addObj(obj)
					obj = enemy.Shutter2(pos[0] +8, pos[1] -30, True, 180)
					ObjMgr.addObj(obj)
				elif n in (390, 391):
					# 砲台
					gcommon.setMapDataByMapPos(mx, my, 0)
					obj = enemy.Battery2(mx, my, 1)
					if n == 391:
						obj.direction = -1
					ObjMgr.addObj(obj)
				elif n in (422, 423):
					# ミサイル砲台
					gcommon.setMapDataByMapPos(mx, my, 0)
					obj = enemy.MissileBattery1(mx, my, (n == 423))
					ObjMgr.addObj(obj)
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
					ObjMgr.addObj(obj)
				elif n in (424, 425):
					waitCount = gcommon.getMapDataByMapPos(mx+1, my) -224
					gcommon.setMapDataByMapPos(mx, my, 0)
					gcommon.setMapDataByMapPos(mx+1, my, 0)
					if n == 424:
						obj = enemy.Shutter3(mx, my, -1, waitCount* 30)
					else:
						obj = enemy.Shutter3(mx, my, 1, waitCount* 30)
					ObjMgr.addObj(obj)
				else:
					# 共通のマップキャラクタ処理
					doMapCharacter(n, mx, my)

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
				Drawing.setBrightnessMinus1()
			mx = (int)(gcommon.back_map_x/8)
			pyxel.bltm(-1 * (int(gcommon.back_map_x) % 8), 0, 1, mx, 24,33,33, 3)
			if gcommon.back_map_x < 2:
				pyxel.pal()
			
	def draw(self):
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

	def draw2(self):
		pass

class MapDrawLabirinth:
	def __init__(self):
		pass
	
	def init(self):
		gcommon.map_x = -32 * 8
		gcommon.map_y = 8 * 24
		gcommon.mapHeight = 8 * 256
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
				if n == 395:
					# 移動床
					gcommon.debugPrint(str(mx) + " " + str(my))
					startTime = (gcommon.getMapDataByMapPos(mx+1, my) -992) * 10 + (gcommon.getMapDataByMapPos(mx+2, my) -992)
					moveNo = (gcommon.getMapDataByMapPos(mx+3, my) -992) * 10 + (gcommon.getMapDataByMapPos(mx+4, my) -992)
					battery = gcommon.getMapDataByMapPos(mx+5, my) - 458
					gcommon.setMapDataByMapPos2(mx, my, 0, 12, 12)
					obj = enemyOthers.MovableWall(mx, my, 0, startTime*60, moveNo)
					ObjMgr.addObj(obj)
					if battery>=0 and battery <= 3:
						pos = gcommon.mapPosToScreenPos(mx, my)
						if battery == 0:
							ObjMgr.addObj(enemy.Battery4(obj, 5*8, -16, battery))
						elif battery == 1:
							ObjMgr.addObj(enemy.Battery4(obj, 5*8, 12*8, battery))
						elif battery == 2:
							ObjMgr.addObj(enemy.Battery4(obj, 12*8, 5*8, battery))
						elif battery == 3:
							ObjMgr.addObj(enemy.Battery4(obj, -2*8, 5*8, battery))

				elif n in (390, 391, 392, 393):
					# 砲台
					gcommon.setMapDataByMapPos(mx, my, 0)
					ObjMgr.addObj(enemy.Battery1([0,0,mx, my, n -390]))
				else:
					# 共通のマップキャラクタ処理
					doMapCharacter(n, mx, my)
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

	def draw2(self):
		pass

