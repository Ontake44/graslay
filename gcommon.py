
import pyxel
import math
import json
import os.path

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
# BOM
T_BOM = -110

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
C_LAYER_HIDE_GRD = 6		# 壁とか
C_LAYER_EXP_GRD = 4			# 地上爆発
C_LAYER_UPPER_GRD = 7
C_LAYER_SKY = 1
C_LAYER_EXP_SKY = 5
C_LAYER_ITEM = 3
C_LAYER_E_SHOT = 2
C_LAYER_TEXT = 8
C_LAYER_NONE = -1

# item
C_ITEM_PWUP = 1
C_ITEM_BOM = 2

C_COLOR_KEY = 13

SOUND_SHOT = 0
SOUND_MID_EXP = 1
SOUND_SMALL_EXP = 2
SOUND_ITEM_GET = 3
SOUND_LARGE_EXP = 4
SOUND_BOM_EXP = 5
SOUND_PWUP = 6
SOUND_FULLPOWER = 7
SOUND_BOSS_EXP = 8
SOUND_SHOT2 = 9
SOUND_GAMESTART = 10

#                 0 1 2 3 4 5 6 7 8 9 10
sound_priority = [0,2,1,4,5,3,6,0,8,0, 0]

START_BOM_REMAIN = 3
START_MY_POWER = 1

# 残機
START_REMAIN = 2		# 2

SHOT_POWER = 5		# 5
#SHOT_POWER = 200

BOM_POWER = 3

TP_COLOR = 2

SCREEN_MAX_X = 255
SCREEN_MAX_Y = 255

# 64 direction table
atan_table = []


#       2
#    3     1
#  4         0
#    5     7
#       6
direction_map = [		\
[1,0],[0.701,0.701],	\
[0,-1],[-0.701,-0.701],	\
[-1,0],[-0.701,0.701],	\
[0,1],[0.701,0.701]]



# ====================================================================
# グローバル変数


game_timer = 0
score = 0

cur_scroll_x = 0
cur_scroll_y = 0

map_x = 0
map_y = 0

power = START_MY_POWER
remain = START_REMAIN		# 残機
bomRemain = START_BOM_REMAIN

enemy_shot_rate = 1

draw_star = False

app = None

drawMap = None

mapFreeTable = []


# ====================================================================

SETTINGS_FILE = ".graden"

def loadSettings():
	try:
		settingsPath = os.path.join(os.path.expanduser("~"), SETTINGS_FILE)

		json_file = open(settingsPath, "r")
		json_data = json.load(json_file)
		if "playerStock" in json_data:
			playerStock = int(json_data["playerStock"])
		if "bombStock" in json_data:
			bombStock = int(json_data["bombStock"])
		if "startStage" in json_data:
			startStage = int(json_data["startStage"])
		if "sound" in json_data:
			soundFlag = int(json_data["sound"])		# 0 or 1

		global START_REMAIN
		global START_BOM_REMAIN
		global START_STAGE
		global SOUND_ON
		if playerStock >= 1 and playerStock <= 99:
			START_REMAIN = playerStock
		if bombStock >= 0 and bombStock <= 5:
			START_BOM_REMAIN = bombStock
		if startStage >= 1 and startStage <= 3:
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
	global START_BOM_REMAIN
	global START_STAGE
	global SOUND_ON
	json_data = { "playerStock": START_REMAIN, "bombStock": START_BOM_REMAIN, "startStage": START_STAGE}
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
	r = 0
	rr =  math.pi*2/64		#1/128
	for i in range(0,64):	#   i=0,63 do
		atan_table.append(r)
		r = r + rr

# -piからpiでは使いにくいので
# 0 から 2piとする
def atan2x(x, y):
	r = math.atan2(y, x)
	if y < 0:
		r = r + math.pi * 2;
	return r


def get_atan(x1,y1,x2,y2,offsetdr):
	return atan_table[get_atan_no(x1,y1,x2,y2)+offsetdr & 63]


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
		return 0

def get_atan_no_to_ship(x,y):
	return get_atan_no(x, y, ObjMgr.myShip.x+8, ObjMgr.myShip.y+8)

def get_atan_to_ship(x, y):
	return get_atan(x, y, ObjMgr.myShip.x+8, ObjMgr.myShip.y+8, 0)

def get_atan_to_ship2(x, y, offsetdr):
		return get_atan(x, y, ObjMgr.myShip.x +8, ObjMgr.myShip.y+8, offsetdr)

# return 0-7
def get_direction_my(x, y):
	return (int((get_atan_no(x, y, ObjMgr.myShip.x+8, ObjMgr.myShip.y+8)+3)/8) & 7)


def get_distance_my(x, y):
	return math.sqrt((ObjMgr.myShip.x+8 -x)*(ObjMgr.myShip.x+8 -x)+(ObjMgr.myShip.y+8 -y)*(ObjMgr.myShip.y+8 -y))

def check_collision(o, s):
	if (o.x+o.left<=s.x+s.left and s.x+s.left<=o.x+o.right)	\
		or (o.x+o.left<=s.x+s.right and s.x+s.right<=o.x+o.right):
		if (o.y+o.top<=s.y+s.top and s.y+s.top<=o.y+o.bottom)	\
			or (o.y+o.top<=s.y+s.bottom and s.y+s.bottom<=o.y+o.bottom):
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
	if pyxel.btn(pyxel.KEY_SHIFT) or pyxel.btn(pyxel.GAMEPAD_1_A) or pyxel.btn(pyxel.GAMEPAD_1_Y):
		return True
	else:
		return False

def checkBomKey():
	if pyxel.btn(pyxel.KEY_Z) or pyxel.btn(pyxel.GAMEPAD_1_B) or pyxel.btn(pyxel.GAMEPAD_1_X):
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
				pyxel.stop(0)
				pyxel.play(0, snd)


def getCenterX(obj):
	return obj.x + (obj.right -obj.left+1)/2

def getCenterY(obj):
	return obj.y + (obj.bottom -obj.top+1)/2

class ObjMgr:
	myShip = None
	# 自機弾
	shots = []
	shotGroups = []

	# BOM
	myBom = None

	# 敵
	objs = []
	
	@classmethod
	def init(cls):
		cls.myShip = None
		cls.shots.clear()
		cls.shotGroups.clear()
		cls.objs.clear()

	@classmethod
	def addObj(cls, obj):
		cls.objs.append(obj)



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
	if pyxel.btnp(pyxel.KEY_SHIFT) or pyxel.btnp(pyxel.GAMEPAD_1_A) or pyxel.btnp(pyxel.GAMEPAD_1_Y):
		return True
	else:
		return False

def getMapData(x, y):
	global drawMap
	global map_x
	global map_y
	if drawMap == None:
		return -1
	else:
		mx = int(map_x/8) + int((int(map_x)%8 + int(x))/8)
		my = int(map_y/8) + int((int(map_y)%8 + int(y))/8)
		if mx>=0 and mx<256 and my>=0 and my<256:
			return pyxel.tilemap(0).get(mx, my)
		else:
			return -1


def isMapFree(no):
	global mapFreeTable
	if no >= 512:
		return True
	else:
		return no in mapFreeTable
