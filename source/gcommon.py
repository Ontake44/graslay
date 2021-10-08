
import pyxel
import math
import sys
import os
import random
from enum import Enum
from objMgr import ObjMgr

VERSION = "2.00"
START_GAME_TIMER= 0		# 3600 :3		#2700 :2
START_STAGE = None

DIFFICULTY_EASY = 0
DIFFICULTY_NORMAL = 1
DIFFICULTY_HARD = 2

difficultyText = (" EASY ", "NORMAL", " HARD ")

stageList = ("1A", "2A", "2B", "3A", "3B", "4A", "5A", "5B", "6A")


# 機体種別
class WeaponType:
	TYPE_A = 0		# Axelay
	TYPE_B = 1		# Bic Viper


WEAPON_STRAIGHT = 0
WEAPON_ROUND = 1
WEAPON_WIDE = 2

B_WEAPON_DOUBLE = 0
B_WEAPON_TAILGUN = 1
B_WEAPON_LASER = 2
B_WEAPON_RIPPLE = 3

# これ以上自機に近いと敵弾を発射しないという距離
ENEMY_SHOT_DISTANCE = 32

PAUSE_NONE = 0		# ゲーム中
PAUSE_PAUSE = 1		# PAUSE
PAUSE_CONTINUE = 2	# CONTINUE確認中

GAMEMODE_NORMAL = 0
GAMEMODE_CUSTOM = 1

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
C_LAYER_UNDER_GRD = 1		# マップより下
C_LAYER_GRD = 2				# 普通の地上物
#C_LAYER_HIDE_GRD = 6		# 壁とか
#C_LAYER_EXP_GRD = 4			# 地上爆発
#C_LAYER_UPPER_GRD = 7
C_LAYER_SKY = 4
C_LAYER_EXP_SKY = 8
C_LAYER_ITEM = 16
C_LAYER_E_SHOT = 32
C_LAYER_UPPER_SKY = 64
C_LAYER_TEXT = 128
C_LAYER_NONE = 0

# item
C_ITEM_PWUP = 1

C_COLOR_KEY = 13

SOUND_SHOT = 0
SOUND_MID_EXP = 1
SOUND_SMALL_EXP = 2
SOUND_HIT = 3
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
SOUND_MENUMOVE = 18
SOUND_EXTENDED = 7
SOUND_ITEM_GET = 19
SOUND_WATERSPLASH = 20
SOUND_LASER = 25
SOUND_RIPPLE = 26

# ch
# 0 : 敵の爆発
# 1 : 自機ショット、自機爆発
SOUND_CH0 = 0
SOUND_CH1 = 1
SOUND_CH2 = 2

KEY_HOLD = 20
KEY_PERIOD = 5

START_MY_POWER = 1

SHOT0_POWER = 13		# 5
SHOT1_POWER = 5
SHOT2_POWER = 7
SHOT_POWERS = (SHOT0_POWER, SHOT1_POWER, SHOT2_POWER)

B_SHOT0_POWER = 5		# 5
B_SHOT1_POWER = 5
B_SHOT2_POWER = 3
B_SHOT3_POWER = 5
B_SHOT_POWERS = (B_SHOT0_POWER, B_SHOT1_POWER, B_SHOT2_POWER)

MISSILE0_POWER = 5
MISSILE1_POWER = 5
MISSILE2_POWER = 2
MISSILE_POWERS = (MISSILE0_POWER, MISSILE1_POWER, MISSILE1_POWER)

B_MISSILE0_POWER = 5
B_MISSILE1_POWER = 5
B_MISSILE2_POWER = 5


TP_COLOR = 2

SCREEN_MIN_X = 0
SCREEN_MIN_Y = 0
SCREEN_MAX_X = 255
SCREEN_MAX_Y = 191

SCREEN_WIDTH = 256
SCREEN_HEIGHT = 192

DUMMY_BLOCK_NO = 64

# 壊れないもの
HP_UNBREAKABLE = 999999
# ダメージすら受けない
HP_NODAMAGE = -999999

# 64 direction table
atan_table = []

cos_table = []
sin_table = []

MYSHIP_START_X = 8
MYSHIP_START_Y = 200/2 -8

# 座標系は下の上下逆になることに注意
#       2
#    3     1
#  4         0
#    5     7
#       6
# mapと言いつつ配列
direction_map = [		\
[1,0],[0.701,-0.701],	\
[0,-1],[-0.701,-0.701],	\
[-1,0],[-0.701,0.701],	\
[0,1],[0.701,0.701]]

# 上下は通常
direction_map2 = [		\
[1.0, 0.0], [0.701, 0.701],	\
[0.0, 1.0], [-0.701, 0.701],	\
[-1.0, 0.0], [-0.701, -0.701],	\
[0.0, -1.0],[0.701, -0.701]
]


# ====================================================================
# グローバル変数

game_timer = 0
#score = 0
DebugMode = False
ShowCollision = False
# カスタムモードだけどノーマルと同じような動作
CustomNormal = False

scroll_flag = True
cur_scroll_x = 0.0
cur_scroll_y = 0.0

cur_map_dx = 0.0
cur_map_dy = 0.0

map_x = 0.0
map_y = 0.0
mapHeight = 8 * 256

back_map_x = 0.0
back_map_y = 0.0

sync_map_y = 0

eshot_sync_scroll = False

long_map = False

breakableMapData = False


# 現在未使用（パワーアップ無いので）
#power = START_MY_POWER

POWER_RATE_EASY = 2.0
POWER_RATE_NORMAL = 1.5
POWER_RATE_HARD = 1.0

ENEMY_SHOT_RATE_EASY = 0.65
ENEMY_SHOT_RATE_NORMAL = 0.75
ENEMY_SHOT_RATE_HARD = 0.90

DIFFICULTY_RATE_EASY = 0.75
DIFFICULTY_RATE_NORMAL = 1.0
DIFFICULTY_RATE_HARD = 1.5

draw_star = False
star_pos = 0

app = None

star_ary = []

mapAttribute = []
mapAttribute2 = []


waterSurface_y = 0.0

getMapDataByMapPosHandler = None


# ====================================================================



class ClassicRand:
	def __init__(self):
		self.x = 1

	# 32bit乱数を返す
	def rand(self):
		self.x = (self.x * 1103515245+12345)&2147483647
		return self.x

class BGStarV:
	def __init__(self):
		self.star_pos = 0

	def update(self):
		self.star_pos -= 0.25
		if self.star_pos<0:
			self.star_pos += 200

	def draw(self):
		for i in range(0,96):
			pyxel.pset(star_ary[i][0], int(i*2 + self.star_pos) % 200, star_ary[i][1])

class Pos:
	def __init__(self):
		self.x = 0
		self.y = 0

	@classmethod
	def create(cls, x, y):
		p = Pos()
		p.x = x
		p.y = y
		return p

class Rect:
	def __init__(self, left, top, right, bottom):
		self.left = left
		self.top = top
		self.right = right
		self.bottom = bottom

	@classmethod
	def create(cls, left, top, right, bottom):
		return Rect(left, top, right, bottom)

	@classmethod
	def createWH(cls, left, top, width, height):
		return Rect(left, top, left + width -1, top + height -1)

	@classmethod
	def createFromList(cls, list):
		rects = []
		for item in list:
			rects.append(Rect.create(item[0], item[1], item[2], item[3]))
		return rects

	@classmethod
	def createSingleList(cls, left, top, right, bottom):
		return [Rect.create(left, top, right, bottom)]

	def getWidth(self):
		return self.right - self.left +1

	def getHeight(self):
		return self.bottom - self.top +1

	def contains(self, x, y):
		return self.left <= x and self.top <= y and x <= self.right and y <= self.bottom

	def shift(self, dx, dy):
		self.left += dx
		self.top += dy
		self.right += dx
		self.bottom += dy

class RectObj:
	def __init__(self, x, y, left, top, right, bottom):
		self.x = x
		self.y = y
		self.left = left
		self.top = top
		self.right = right
		self.bottom = bottom

screenRectObj = RectObj(0, 0, SCREEN_MIN_X, SCREEN_MIN_Y, SCREEN_MAX_X, SCREEN_MAX_Y)

class Polygon:
	def __init__(self, points, clr, fill=True):
		self.points = points
		self.clr = clr
		self.fill = fill

class Polygons:
	def __init__(self, polygons):
		self.polygons = polygons


def initStar():
	global star_ary
	for dummy in range(0,96):
		o = [int(random.randrange(0,256)), int(random.randrange(0,2)+5)]
		star_ary.append(o)

def drawStar(star_pos):
	for i in range(0,96):
		pyxel.pset(((int)(star_ary[i][0] +star_pos))&255, i*2, star_ary[i][1])

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


def init_atan_table():
	r = 0.0
	rr =  math.pi*2/64		#1/128
	for dummy in range(0,64):	#   i=0,63 do
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

# radを -pi ～piの間に正規化する
def radNormalize(rad):
	r = math.fmod(rad, math.pi * 2)
	if r > math.pi:
		r -= math.pi * 2
	elif r < -math.pi:
		r += math.pi * 2
	return r

# radを 0 ～2piの間に正規化する
def radNormalizeX(rad):
	r = math.fmod(rad, math.pi * 2)
	if r < 0.0:
		r += math.pi * 2
	return r

def degNormalize(deg):
	d = int(deg) % 360
	if d < 0:
		return 360 -d
	else:
		return d

# 指定した座標・ラジアンから、自機方向にomega回転した値を返す
def getRadToShip(x, y, rad, omega):
	tempDr = get_atan_rad_to_ship(x, y)
	rr = radNormalize(tempDr - rad)
	if rr == 0.0:
		pass
	elif  rr > 0.0 and abs(rr) >= omega:
		rad += omega
		if rad >= math.pi*2:
			rad -= math.pi*2
	elif abs(rr) >= omega:
		rad -= omega
		if rad <= 0.0:
			rad += math.pi*2
	return rad

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

# return 0-63
def get_atan_no_to_ship(x,y):
	return get_atan_no(x, y, ObjMgr.myShip.x+8, ObjMgr.myShip.y+8)

def get_atan_to_ship(x, y):
	return get_atan(x, y, ObjMgr.myShip.x+8, ObjMgr.myShip.y+8, 0)

def get_atan_to_ship2(x, y, offsetdr):
		return get_atan(x, y, ObjMgr.myShip.x +8, ObjMgr.myShip.y+8, offsetdr)

def get_atan_rad_to_ship(x, y):
	return math.atan2(ObjMgr.myShip.y +8 -y, ObjMgr.myShip.x +8 -x)

# r1からみて、r2が右側(-1)か左側(1)のどちらかを返す
def get_leftOrRight(r1, r2):
	rr1 = (r2 - r1) & 63
	rr2 = (r1 - r2) & 63
	if rr1 < rr2:
		return 1
	else:
		return -1

#      6
#    5   7
#   4     0
#    3   1
#      2
# return 0-7
def get_direction_my(x, y):
	return (int((get_atan_no(x, y, ObjMgr.myShip.x+8, ObjMgr.myShip.y+8)+3)/8) & 7)


def get_distance_my(x, y):
	return math.sqrt((ObjMgr.myShip.x+8 -x)*(ObjMgr.myShip.x+8 -x)+(ObjMgr.myShip.y+8 -y)*(ObjMgr.myShip.y+8 -y))

def get_distance_pos2(pos1, pos2):
	return math.sqrt((pos1[0]-pos2[0])*(pos1[0]-pos2[0])+(pos1[1]-pos2[1])*(pos1[1]-pos2[1]))

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

# rectList list of Rect
def check_collision_list(x, y, rectList, obj2):
	for rect in rectList:
		if check_collision2(x, y, rect, obj2):
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
	if pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.GAMEPAD_1_A) or pyxel.btn(pyxel.GAMEPAD_1_Y) or pyxel.btn(pyxel.MOUSE_LEFT_BUTTON):
		return True
	else:
		return False

def checkShotKeyP():
	if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD_1_A) or pyxel.btnp(pyxel.GAMEPAD_1_Y)  or pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON, KEY_HOLD, KEY_PERIOD):
		return True
	else:
		return False

def checkShotKeyRectP(rect):
	if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(pyxel.GAMEPAD_1_A) or pyxel.btnp(pyxel.GAMEPAD_1_Y)  \
	or (rect.contains(pyxel.mouse_x, pyxel.mouse_y) and pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON)):
		return True
	else:
		return False

def checkOpionKey():
	if pyxel.btnp(pyxel.KEY_X) or pyxel.btnp(pyxel.GAMEPAD_1_B) or pyxel.btnp(pyxel.GAMEPAD_1_X) or pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON, KEY_HOLD, KEY_PERIOD):
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


def getCenterX(obj):
	return obj.x + obj.left + (obj.right -obj.left+1)/2

def getCenterY(obj):
	return obj.y + obj.top + (obj.bottom -obj.top+1)/2

def getCenterPos(obj):
	return [obj.x + obj.left + (obj.right -obj.left+1)/2, obj.y + obj.top + (obj.bottom -obj.top+1)/2]

def getSize(obj):
	return [obj.right -obj.left+1, obj.bottom -obj.top+1]


def bltStripe(x, y, img, u, v, w, h, col, p):
	for yy in range(p, h, 2):
		pyxel.blt(x, y +yy, img, u, v +yy, w, 1, col)


def checkLeftP():
	return pyxel.btnp(pyxel.KEY_LEFT, KEY_HOLD, KEY_PERIOD) or pyxel.btnp(pyxel.GAMEPAD_1_LEFT, KEY_HOLD, KEY_PERIOD)

def checkRightP():
	return pyxel.btnp(pyxel.KEY_RIGHT, KEY_HOLD, KEY_PERIOD) or pyxel.btnp(pyxel.GAMEPAD_1_RIGHT, KEY_HOLD, KEY_PERIOD)

def checkUpP():
	return pyxel.btnp(pyxel.KEY_UP, KEY_HOLD, KEY_PERIOD) or pyxel.btnp(pyxel.GAMEPAD_1_UP, KEY_HOLD, KEY_PERIOD)

def checkDownP():
	return pyxel.btnp(pyxel.KEY_DOWN, KEY_HOLD, KEY_PERIOD) or pyxel.btnp(pyxel.GAMEPAD_1_DOWN, KEY_HOLD, KEY_PERIOD)

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


# 倉庫ステージ等に使う
def getMapDataPage(page, x, y):
	global map_x
	global map_y
	global long_map
	mx = int((map_x +x)/8)
	if long_map:
		my = int((map_y +y)/8) & 127
	else:
		my = int((map_y +y)/8)
	return getMapDataByMapPosPage(page, mx, my)

def getMapDataByMapPos(mx, my):
	#return getMapDataByMapPosHandler(mx, my)
	return getMapDataByMapPosimplement(mx, my)

def getMapDataByMapPosimplement(mx, my):
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

# 6Bステージなどの
def getMapDataByMapPosimplement2(mx, my):
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


def getMapDataByMapPosPage(page, mx, my):
	global map_x
	global map_y
	global long_map
	#print("--mx = " + str(mx) + " my=" + str(my))
	if ObjMgr.drawMap == None:
		return -1
	else:
		if long_map:
			# 最大マップ4画面幅 mx<1024
			if mx>=0 and mx<256*4 and my>=0 and my<128:
				tm = int(mx/512) + page
				moffset = (int(mx/256) & 1) * 128
				return pyxel.tilemap(tm).get(mx & 255, (my + moffset) & 255)
			else:
				#print("mx = " + str(mx) + " my=" + str(my))
				return -3
		else:
			if mx>=0 and mx<256 and my>=0 and my<256:
				return pyxel.tilemap(page).get(mx, my)
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

def clearMapData(x, y):
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
				pyxel.tilemap(tm).set(mx & 255, (my + moffset) & 255, pyxel.tilemap(tm+4).get(mx & 255, (my + moffset) & 255))
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

def setMapDataByMapPosPage(page, mx, my, p):
	global long_map
	if ObjMgr.drawMap == None:
		return
	else:
		if long_map:
			# 最大マップ4画面幅 mx<1024
			if mx>=0 and mx<256*4 and my>=0 and my<128:
				tm = int(mx/512) + page
				moffset = (int(mx/256) & 1) * 128
				pyxel.tilemap(tm).set(mx & 255, (my + moffset) & 255, p)
			else:
				return
		else:
			if mx>=0 and mx<256 and my>=0 and my<256:
				pyxel.tilemap(page).set(mx, my, p)
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

# 壁当たり判定有無を返す
def isMapFree(no):
	global mapAttribute
	return mapAttribute[no >> 5][no & 31] != "1"

def isMapZero(no):
	global mapAttribute
	return mapAttribute[no >> 5][no & 31] == "0"

# 敵弾発射可能？
def isShotMapPos(x, y):
	no = getMapData(x, y)
	if no >= 0:
		global mapAttribute
		c = mapAttribute[no >> 5][no & 31]
		return c == "0"
	else:
		return True

def isMapFreePos(x, y) -> bool:
	no = getMapData(x, y)
	if no >= 0:
		return isMapFree(no)
	else:
		return True

def isMapZeroPos(x, y) -> bool:
	no = getMapData(x, y)
	if no >= 0:
		return isMapZero(no)
	else:
		return True

def isMapFreeByMapPos(mx, my) -> bool:
	no = getMapDataByMapPos(mx, my)
	if no >= 0:
		return isMapFree(no)
	else:
		return True

def mapPosToScreenPos(mx, my) -> list:
	global map_x
	global map_y
	global mapHeight
	if ObjMgr.drawMap == None:
		return [-9999,-9999]
	else:
		y = my * 8 - map_y
		if y < 0:
			if y < -int(mapHeight/2):
				y += mapHeight
		else:
			if y > int(mapHeight/2):
				y -= mapHeight
		return [mx * 8 - int(map_x), y]

def mapYToScreenY(y):
	return y - map_y


# destPos   [x,y]
# points    [[x0,y0],[x1,y1],...]
# offsetPos [x,y]
def getAnglePoints(destPos, points, offsetPos, rad):
	xpoints = []
	c = math.cos(rad)
	s = math.sin(rad)
	for p in points:
		x = destPos[0] + (p[0]- offsetPos[0]) * c - (p[1] -offsetPos[1]) * s
		y = destPos[1] + ((p[0] -offsetPos[0]) * s + (p[1] -offsetPos[1]) * c)
		xpoints.append([x,y])
	return xpoints

# destPos   [x,y]
# points    [[x0,y0],[x1,y1],...]
# offsetPos [x,y]
def getShitPoints(destPos, points):
	xpoints = []
	for p in points:
		x = destPos[0] + p[0]
		y = destPos[1] + p[1]
		xpoints.append([x,y])
	return xpoints

def getAngle(x, y, rad):
	return [(x * math.cos(rad) - y * math.sin(rad)), (x * math.sin(rad) + y * math.cos(rad))]

# Polygonsクラス指定で傾いたポリゴンを返す
def getAnglePolygons(destPos, polygons, offsetPos, rad):
	xpolygons = []
	c = math.cos(rad)
	s = math.sin(rad)
	for poly in polygons:
		xpoints = []
		for p in poly.points:
			x = destPos[0] + (p[0] - offsetPos[0]) * c - (p[1] -offsetPos[1]) * s
			y = destPos[1] + ((p[0] -offsetPos[0]) * s + (p[1] -offsetPos[1]) * c)
			xpoints.append([x,y])
		xpoly = Polygon(xpoints, poly.clr, poly.fill)
		xpolygons.append(xpoly)
	return Polygons(xpolygons)

def getAnglePolygons2(destPos, polygons, offsetPos, rad, dx, dy):
	xpolygons = []
	c = math.cos(rad)
	s = math.sin(rad)
	for poly in polygons:
		xpoints = []
		for p in poly.points:
			x = destPos[0] + (p[0]- offsetPos[0]) * c * dx- (p[1] -offsetPos[1]) * s * dy
			y = destPos[1] + ((p[0] -offsetPos[0]) * s * dx+ (p[1] -offsetPos[1]) * c * dy)
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

# 点がポリゴンの中かどうかを返す（ポリゴン座標配列指定）
#  pos = [x, y]
#  polyPoints = [[x1, y1],[x2, y2] ..]
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


# イージング関数
def easeOutBack(x):
	c1 = 1.70158
	c3 = c1 + 1
	return 1 + c3 * math.pow(x - 1, 3) + c1 * math.pow(x - 1, 2)



def setMenuColor(index, menuPos):
	if index == menuPos:
		pyxel.pal()
	else:
		pyxel.pal(7, 12)



def getMirrorDr64(dr64):
	dr = dr64 & 63
	if dr <= 32:
		return 32 -dr
	else:
		return 96 -dr

def inScreen(x, y):
	return x >= SCREEN_MIN_X and x <= SCREEN_MAX_X and y >= SCREEN_MIN_Y and y <= SCREEN_MAX_Y

def outScreenRect(obj):
	return not check_collision(screenRectObj, obj)

# rects Rect型配列
def checkMouseMenuPos(rects):
	for i, rect in enumerate(rects):
		if rect.contains(pyxel.mouse_x, pyxel.mouse_y):
			return i
	return -1

# 符号付整数化
# sint(-1.5) -> -2
def sint(n):
	if n > 0:
		return int(n)
	else:
		return int(n -0.5)

def debugPrint(s):
	if DebugMode:
		print(s)

def getShrinkList(lst):
	newList = []
	for item in lst:
		if item != None and item.removeFlag == False:
			newList.append(item)
	return newList

def breakObjects(objs):
	if objs != None:
		for obj in objs:
			if obj != None and obj.removeFlag == False:
				obj.broken()

def setGetMapDataByMapPosHandler(handler):
	global getMapDataByMapPosHandler
	getMapDataByMapPosHandler = handler

