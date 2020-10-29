
import pyxel
import math
import json
import os.path
import random

START_GAME_TIMER= 0		# 3600 :3		#2700 :2

START_STAGE = 1

SOUND_ON = True

WEAPON_STRAIGHT = 0
WEAPON_ROUND = 1
WEAPON_WIDE = 2


# defines
T_COPTER1 = 1
T_I_CARRIOR = 2
T_TANK1 = 3
T_MID_TANK1 = 4
T_FIGHTER1 = 5
T_BOSS1 = 6
T_BATTERY1 = 7
T_TANK2 = 8
T_WALL1 = 9
T_BOSS2 = 10
T_BOSS2SIDE = 11
T_MATERIAL = 12
T_STAGE_START = 13
T_FIGHTER2 = 14
T_FIGHTER2APPEAR = 15
T_BATTERY2 = 16
T_MID_BATTERY1 = 17
T_LARGE_TANK1 = 18
T_BOSS3 = 19
T_BOSSEXPLOSION = 20

# ENEMY SHOT
T_E_SHOT1 = 100
# SKY EXPLOSION
T_SKY_EXP = -1
# GROUND EXPLOSION
T_GRD_EXP = -2
# POWER UP
T_PWUP = -100

# explosion type
C_EXPTYPE_SKY_S=1
C_EXPTYPE_SKY_M = 2
C_EXPTYPE_SKY_L = 3 
C_EXPTYPE_GRD_S = 11
C_EXPTYPE_GRD_M = 12
C_EXPTYPE_GRD_L = 13 
C_EXPTYPE_GRD_BOSS = 14

# layer
C_LAYER_UNDER_GRD = 9		# マップより下
C_LAYER_GRD = 0				# 普通の地上物
#C_LAYER_HIDE_GRD = 6		# 壁とか
#C_LAYER_EXP_GRD = 4			# 地上爆発
#C_LAYER_UPPER_GRD = 7
C_LAYER_SKY = 1
C_LAYER_EXP_SKY = 5
C_LAYER_ITEM = 3
C_LAYER_E_SHOT = 2
C_LAYER_TEXT = 8
C_LAYER_NONE = -1

# item
C_ITEM_PWUP = 1

C_COLOR_KEY = 13

SOUND_SHOT = 0
SOUND_MID_EXP = 1
SOUND_SMALL_EXP = 2
SOUND_ITEM_GET = 3
SOUND_LARGE_EXP = 4
SOUND_PWUP = 6
SOUND_FULLPOWER = 7
SOUND_BOSS_EXP = 8
SOUND_SHOT2 = 9
SOUND_GAMESTART = 10
SOUND_BOSS1BEAM = 11
SOUND_BOSS1PREBEAM = 12
SOUND_CELL_EXP = 13
SOUND_FEELER_GROW = 14
SOUND_BOSS3_ANCHOR = 15
SOUND_AFTER_BURNER = 16
SOUND_SHOT3 = 17

#                 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17
sound_priority = [0,2,1,4,5,3,6,0,8,1, 0, 6, 6, 1, 6, 6, 6, 1]

START_MY_POWER = 1

# 残機
START_REMAIN = 2		# 2

SHOT_POWER = 5		# 5
#SHOT_POWER = 200

TP_COLOR = 2

SCREEN_MAX_X = 255
SCREEN_MAX_Y = 191

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 192

DUMMY_BLOCK_NO = 64

# 64 direction table
atan_table = []

cos_table = []
sin_table = []


# 座標系は下の上下逆になることに注意
#       2
#    3     1
#  4         0
#    5     7
#       6
direction_map = [		\
[1,0],[0.701,-0.701],	\
[0,-1],[-0.701,-0.701],	\
[-1,0],[-0.701,0.701],	\
[0,1],[0.701,0.701]]



# ====================================================================
# グローバル変数


game_timer = 0
score = 0

cur_scroll_x = 0.0
cur_scroll_y = 0.0

cur_map_dx = 0.0
cur_map_dy = 0.0

map_x = 0.0
map_y = 0.0

sync_map_y = 0

eshot_sync_scroll = False

long_map = False

power = START_MY_POWER
remain = START_REMAIN		# 残機

enemy_shot_rate = 1

draw_star = False

app = None

mapFreeTable = []

star_ary = []

mapAttribute = []

# ====================================================================

SETTINGS_FILE = ".graslay"


class Rect:
	def __init__(self):
		self.left = 0
		self.top = 0
		self.right = 0
		self.bottom = 0

	@classmethod
	def create(cls, left, top, right, bottom):
		rect = Rect()
		rect.left = left
		rect.top = top
		rect.right = right
		rect.bottom = bottom
		return rect
	
	def width(self):
		return self.right - self.left +1

	def height(self):
		return self.height - self.top +1

class Polygon:
	def __init__(self, points, clr):
		self.points = points
		self.clr = clr

class Polygons:
	def __init__(self, polygons):
		self.polygons = polygons


def initStar():
	global star_ary
	for i in range(0,96):
		o = [int(random.randrange(0,256)), int(random.randrange(0,2)+5)]
		star_ary.append(o)

	

def loadSettings():
	try:
		settingsPath = os.path.join(os.path.expanduser("~"), SETTINGS_FILE)

		json_file = open(settingsPath, "r")
		json_data = json.load(json_file)
		if "playerStock" in json_data:
			playerStock = int(json_data["playerStock"])
		if "startStage" in json_data:
			startStage = int(json_data["startStage"])
		if "sound" in json_data:
			soundFlag = int(json_data["sound"])		# 0 or 1

		global START_REMAIN
		global START_STAGE
		global SOUND_ON
		if playerStock >= 1 and playerStock <= 99:
			START_REMAIN = playerStock
		if startStage >= 1 and startStage <= 5:
			START_STAGE = startStage
		if soundFlag == 0:
			SOUND_ON = False
		elif soundFlag == 1:
			SOUND_ON = True

		json_file.close()

	except IOError:
		pass


def saveSettings():
	
	global START_REMAIN
	global START_STAGE
	global SOUND_ON
	json_data = { "playerStock": START_REMAIN, "startStage": START_STAGE}
	if SOUND_ON:
		json_data["sound"] = 1
	else:
		json_data["sound"] = 0
	try:
		settingsPath = os.path.join(os.path.expanduser("~"), SETTINGS_FILE)

		json_file = open(settingsPath, "w")
		json.dump(json_data, json_file)
		json_file.close()

	except IOError:
		pass

def init_atan_table():
	r = 0.0
	rr =  math.pi*2/64		#1/128
	for i in range(0,64):	#   i=0,63 do
		atan_table.append(r)
		cos_table.append(math.cos(r))
		sin_table.append(math.sin(r))
		r = r + rr
		

# -piからpiでは使いにくいので
# 0 から 2piとする
def atan2x(x, y):
	r = math.atan2(y, x)
	if y < 0:
		r = r + math.pi * 2
	return r


def get_atan(x1,y1,x2,y2,offsetdr):
	return atan_table[get_atan_no(x1,y1,x2,y2)+offsetdr & 63]

# (x1,y1)から見て(x2,y2)の方向
# return 0-63
def get_atan_no(x1,y1,x2,y2):
	r = atan2x(x2-x1, y2-y1)
	rr = math.pi*2/128		# 1/128
	if r<(atan_table[0]+rr):
		return 0
	else:
		for i in range(1,63): # i=2,64 do
			if r<(atan_table[i]+rr):
				return i
		return 63

def get_atan_no_to_ship(x,y):
	return get_atan_no(x, y, ObjMgr.myShip.x+8, ObjMgr.myShip.y+8)

def get_atan_to_ship(x, y):
	return get_atan(x, y, ObjMgr.myShip.x+8, ObjMgr.myShip.y+8, 0)

def get_atan_to_ship2(x, y, offsetdr):
		return get_atan(x, y, ObjMgr.myShip.x +8, ObjMgr.myShip.y+8, offsetdr)

# r1からみて、r2が右側(-1)か左側(1)のどちらかを返す
def get_leftOrRight(r1, r2):
	rr1 = (r2 - r1) & 63
	rr2 = (r1 - r2) & 63
	if rr1 < rr2:
		return 1
	else:
		return -1

# return 0-7
def get_direction_my(x, y):
	return (int((get_atan_no(x, y, ObjMgr.myShip.x+8, ObjMgr.myShip.y+8)+3)/8) & 7)


def get_distance_my(x, y):
	return math.sqrt((ObjMgr.myShip.x+8 -x)*(ObjMgr.myShip.x+8 -x)+(ObjMgr.myShip.y+8 -y)*(ObjMgr.myShip.y+8 -y))

def check_collision(o, s):
	if (o.x+o.left<=s.x+s.left and s.x+s.left<=o.x+o.right)	\
		or (o.x+o.left<=s.x+s.right and s.x+s.left<=o.x+o.right):
		if (o.y+o.top<=s.y+s.top and s.y+s.top<=o.y+o.bottom)	\
			or (o.y+o.top<=s.y+s.bottom and s.y+s.top<=o.y+o.bottom):
			return True
	return False

# ox,oyのo(left,top,right,bottom)と、sとの衝突判定
def check_collision2(ox, oy, o, s):
	if (ox+o.left<=s.x+s.left and s.x+s.left<=ox+o.right)	\
		or (ox+o.left<=s.x+s.right and s.x+s.left<=ox+o.right):
		if (oy+o.top<=s.y+s.top and s.y+s.top<=oy+o.bottom)	\
			or (oy+o.top<=s.y+s.bottom and s.y+s.top<=oy+o.bottom):
			return True
	return False



def is_draw_shadow():
	if game_timer & 1 ==1:
		return True
	else:
		return False

def set_color_shadow():
	if game_timer & 1 ==1:
		for c in range(0,13):
			pyxel.pal(c, 0)
		pyxel.pal(13, 0)
		pyxel.pal(14, 0)
		pyxel.pal(15, 0)
		return True
	else:
		return False

def is_outof_bound(obj):
	if obj.x+obj.right<-16 or obj.x>=256:
		return True
	
	if obj.y>=256 or obj.y+obj.bottom<-16:
		return True
	
	return False 


def checkShotKey():
	if pyxel.btn(pyxel.KEY_SHIFT) or pyxel.btn(pyxel.KEY_X) or pyxel.btn(pyxel.GAMEPAD_1_A) or pyxel.btn(pyxel.GAMEPAD_1_Y):
		return True
	else:
		return False

def checkOpionKey():
	if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD_1_B) or pyxel.btnp(pyxel.GAMEPAD_1_X):
		return True
	else:
		return False

def circfill_obj_center(obj, r, col):
	pyxel.circ(obj.x+(obj.right -obj.left+1)/2,
	  obj.y+(obj.bottom-obj.top+1)/2, r, col)

def TextHCenter(y, str, col1, col2):
	x = 128 -len(str)*4/2
	if col2 != -1:
		pyxel.text(x+1, y+1, str, col2)
	pyxel.text(x, y, str, col1)

def Text2(x, y, str, col1, col2):
	if col2 != -1:
		pyxel.text(x+1, y+1, str, col2)
	pyxel.text(x, y, str, col1)

def spr1(spno, dx, dy, sx, sy):
	pyxel.blt(dx, dy, 1, int(spno % 16) * 16, int(spno/16) * 16, sx *16, sy *16, TP_COLOR)

def sspr1(sx, sy, sw, sh, dx, dy):
	pyxel.blt(dx, dy, 1, sx*2, sy*2, sw*2, sh*2, TP_COLOR)


def draw_splash(o):
	draw_splash2(o, 0)

def draw_splash2(o, offset):
	r = offset
	for i in range(1,201):
		rr = math.sqrt((o.cnt*2+i)*20)
		pyxel.pset(
			o.x+(o.right-o.left+1)/2 +math.cos(r) * rr,
			o.y+(o.bottom-o.top+1)/2+math.sin(r) * rr,
			7 + int(o.cnt%2)*3)
		#- kore ha tekito
		r += 0.11 + i*0.04

def sound(snd):
	if (SOUND_ON):
		n = pyxel.play_pos(0)
		if n >=0:
			pass
			#print("snd=" + hex(n))
		if (n == -1):
			pyxel.play(0, snd)
		else:
			if sound_priority[int(n/10)]<sound_priority[snd]:
				#pyxel.stop(0)
				pyxel.play(0, snd)

def playBGM():
	pass
	if (SOUND_ON):
		pyxel.playm(0, loop=True)

def playBossBGM():
	pass
	if (SOUND_ON):
		pyxel.playm(1, loop=False)

def getCenterX(obj):
	return obj.x + obj.left + (obj.right -obj.left+1)/2

def getCenterY(obj):
	return obj.y + obj.top + (obj.bottom -obj.top+1)/2

def getCenterPos(obj):
	return [obj.x + obj.left + (obj.right -obj.left+1)/2, obj.y + obj.top + (obj.bottom -obj.top+1)/2]

def getSize(obj):
	return [obj.right -obj.left+1, obj.bottom -obj.top+1]

class ObjMgr:
	myShip = None
	# 自機弾
	shots = []
	shotGroups = []

	# 敵
	objs = []

	nextDrawMap = None
	drawMap = None


	@classmethod
	def init(cls):
		cls.myShip = None
		cls.shots.clear()
		cls.shotGroups.clear()
		cls.objs.clear()
		cls.nextDrawMap = None
		cls.drawMap = None

	@classmethod
	def addObj(cls, obj):
		cls.objs.append(obj)

	@classmethod
	def setDrawMap(cls, obj):
		cls.nextDrawMap = obj

	@classmethod
	def updateDrawMap0(cls, skip):
		if cls.nextDrawMap != None:
			cls.nextDrawMap.init()
			cls.drawMap = cls.nextDrawMap
			cls.nextDrawMap = None
		if cls.drawMap != None:
			cls.drawMap.update0(skip)

	@classmethod
	def updateDrawMap(cls, skip):
		if cls.drawMap != None:
			cls.drawMap.update(skip)

	@classmethod
	def drawDrawMapBackground(cls):
		if cls.drawMap != None:
			cls.drawMap.drawBackground()

	@classmethod
	def drawDrawMap(cls):
		if cls.drawMap != None:
			cls.drawMap.draw()

def bltStripe(x, y, img, u, v, w, h, col, p):
	for yy in range(p, h, 2):
		pyxel.blt(x, y +yy, img, u, v +yy, w, 1, col)


def checkLeftP():
	return pyxel.btnp(pyxel.KEY_LEFT) or pyxel.btnp(pyxel.GAMEPAD_1_LEFT)

def checkRightP():
	return pyxel.btnp(pyxel.KEY_RIGHT) or pyxel.btnp(pyxel.GAMEPAD_1_RIGHT)

def checkUpP():
	return pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD_1_UP)

def checkDownP():
	return pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD_1_DOWN)

def checkShotKeyP():
	if pyxel.btnp(pyxel.KEY_SHIFT) or pyxel.btnp(pyxel.KEY_ENTER) or pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.GAMEPAD_1_A) or pyxel.btnp(pyxel.GAMEPAD_1_Y):
		return True
	else:
		return False

def getMapData(x, y):
	global map_x
	global map_y
	global long_map
	mx = int((map_x +x)/8)
	if long_map:
		my = int((map_y +y)/8) & 127
	else:
		my = int((map_y +y)/8)
	return getMapDataByMapPos(mx, my)

def getMapDataByMapPos(mx, my):
	global map_x
	global map_y
	global long_map
	#print("--mx = " + str(mx) + " my=" + str(my))
	if ObjMgr.drawMap == None:
		return -1
	else:
		if long_map:
			# 2 * 3 = 6画面分
			if mx>=0 and mx<256*6 and my>=0 and my<128:
				tm = int(mx/512)
				moffset = (int(mx/256) & 1) * 128
				return pyxel.tilemap(tm).get(mx & 255, (my + moffset) & 255)
			else:
				#print("mx = " + str(mx) + " my=" + str(my))
				return -3
		else:
			if mx>=0 and mx<256 and my>=0 and my<256:
				return pyxel.tilemap(0).get(mx, my)
			else:
				return -1

def setMapData(x, y, p):
	global map_x
	global map_y
	global long_map
	if ObjMgr.drawMap == None:
		return
	else:
		mx = int((map_x +x)/8)
		if long_map:
			my = int((map_y +y)/8) & 127
			# 2 * 3 = 6画面分
			if mx>=0 and mx<256*6 and my>=0 and my<128:
				tm = int(mx/512)
				moffset = (int(mx/256) & 1) * 128
				pyxel.tilemap(tm).set(mx & 255, (my + moffset) & 255, p)
			else:
				return
		else:
			my = int((map_y +y)/8)
			if mx>=0 and mx<256 and my>=0 and my<256:
				pyxel.tilemap(0).set(mx, my, p)
			else:
				return

def setMapDataByMapPos2(mx, my, p, cx, cy):
	for yy in range(cy):
		for xx in range(cx):
			setMapDataByMapPos(mx +xx, my +yy, p)

def setMapDataByMapPos(mx, my, p):
	global long_map
	if ObjMgr.drawMap == None:
		return
	else:
		if long_map:
			# 2 * 3 = 6画面分
			if mx>=0 and mx<256*6 and my>=0 and my<128:
				tm = int(mx/512)
				moffset = (int(mx/256) & 1) * 128
				pyxel.tilemap(tm).set(mx & 255, (my + moffset) & 255, p)
			else:
				return
		else:
			if mx>=0 and mx<256 and my>=0 and my<256:
				pyxel.tilemap(0).set(mx, my, p)
			else:
				return

def screenPosToMapPos(x, y):
	global map_x
	global map_y
	global long_map
	if long_map:
		#return [int(map_x/8) + int((int(map_x)%8 + int(x))/8), int(int(map_y/8) + int((int(map_y)%8 + int(y))/8)) & 127]
		return [int((map_x +x)/8), int((map_y +y)/8) & 127]
	else:
		return [int((map_x +x)/8), int((map_y +y)/8)]

def screenPosToMapPosX(x):
	global map_x
	return int((map_x +x)/8)

def isMapFree(no):
	global mapAttribute
	return mapAttribute[no >> 5][no & 31] == "0"
	#global mapFreeTable
	#if no >= 512:
	#	return True
	#else:
	#	return no in mapFreeTable


def isMapFreePos(x, y):
	no = getMapData(x, y)
	if no >= 0:
		return isMapFree(no)
	else:
		return True

def isMapFreeByMapPos(mx, my):
	no = getMapDataByMapPos(mx, my)
	if no >= 0:
		return isMapFree(no)
	else:
		return True

def mapPosToScreenPos(mx, my):
	global map_x
	global map_y
	if ObjMgr.drawMap == None:
		return [-9999,-9999]
	else:
		return [mx * 8 - int(map_x), my * 8 - map_y]

def showText(x, y, s):
	for c in s:
		code = ord(c)
		if code >= 65 and code <= 90:
			pyxel.blt(x, y, 0, (code-65)*8, 128, 8, 8, TP_COLOR)
		elif code >= 48 and code <= 57:
			pyxel.blt(x, y, 0, (code-48)*8, 136, 8, 8, TP_COLOR)
		x += 8

def showText2(x, y, s):
	if x == -999:
		x = 127 - len(s)/2 *6
	if y == -999:
		y = 192/2 - 8/2
	for c in s:
		code = ord(c)
		if code >= 65 and code <= 90:
			pyxel.blt(x, y, 0, (code-65)*8, 112, 6, 8, TP_COLOR)
		elif code >= 48 and code <= 57:
			pyxel.blt(x, y, 0, (code-48)*8, 120, 6, 8, TP_COLOR)
		x += 6

# ただの４角形（長方形とは限らない）
#  points = [[0,0],[1,0], [1,1],[0,1]]
def drawQuadrangle(points, clr):
		pyxel.tri(points[0][0], points[0][1],
		 points[1][0], points[1][1],
		 points[2][0], points[2][1], clr)
		pyxel.tri(
		 points[0][0], points[0][1],
		 points[2][0], points[2][1],
		 points[3][0], points[3][1], clr)

def drawPolygon(poly, clr):
	sx = poly[0][0]
	sy = poly[0][1]
	for i in range(len(poly)-2):
		pyxel.tri(sx, sy, 
			poly[i+1][0], poly[i+1][1],
			poly[i+2][0], poly[i+2][1], clr)	

def drawPolygon2(poly, clr1, clr2):
	drawPolygon(poly, clr1)
	last = len(poly) -1
	for i in range(last):
		pyxel.line(poly[i][0], poly[i][1], poly[i+1][0], poly[i+1][1], clr2)
	pyxel.line(poly[last][0], poly[last][1], poly[0][0], poly[0][1], clr2)

# Polygonクラス指定で描く
def drawPolygon3(polygon):
	poly = polygon.points
	sx = poly[0][0]
	sy = poly[0][1]
	for i in range(len(poly)-2):
		pyxel.tri(sx, sy, 
			poly[i+1][0], poly[i+1][1],
			poly[i+2][0], poly[i+2][1], polygon.clr)	

def drawPolygons(polys):
	for p in polys.polygons:
		drawPolygon3(p)

def getAnglePoints(destPos, points, offsetPos, rad):
	xpoints = []
	c = math.cos(rad)
	s = math.sin(rad)
	for p in points:
		x = destPos[0] + (p[0]- offsetPos[0]) * c - (p[1] -offsetPos[1]) * s
		y = destPos[1] + ((p[0] -offsetPos[0]) * s + (p[1] -offsetPos[1]) * c)
		xpoints.append([x,y])
	return xpoints

def getAnglePolygons(destPos, polygons, offsetPos, rad):
	xpolygons = []
	c = math.cos(rad)
	s = math.sin(rad)
	for poly in polygons:
		xpoints = []
		for p in poly.points:
			x = destPos[0] + (p[0]- offsetPos[0]) * c - (p[1] -offsetPos[1]) * s
			y = destPos[1] + ((p[0] -offsetPos[0]) * s + (p[1] -offsetPos[1]) * c)
			xpoints.append([x,y])
		xpoly = Polygon(xpoints, poly.clr)
		xpolygons.append(xpoly)
	return Polygons(xpolygons)


def checkCollisionPointAndPolygonSub(pos, poly1, poly2):
	if ((poly1[1] <= pos[1]) and (poly2[1] > pos[1])) or	\
		((poly1[1] > pos[1]) and (poly2[1] <= pos[1])):
		vt = (pos[1] -poly1[1])/(poly2[1] - poly1[1])
		if pos[0] < (poly1[0] + (vt * (poly2[0] - poly1[0]))):
			return 1
	return 0

# 点がポリゴンの中かどうかを返す
def checkCollisionPointAndPolygon(pos, polyPoints):
	cn = 0
	last = len(polyPoints) -1
	for i in range(last):
		cn += checkCollisionPointAndPolygonSub(pos, polyPoints[i], polyPoints[i+1])
	cn += checkCollisionPointAndPolygonSub(pos, polyPoints[last], polyPoints[0])
	if cn % 2 == 1:
		return True
	else:
		return False



		


