
import pyxel
import math
import random
import gcommon
import enemy
import enemyOthers
import enemyShot
import boss
import drawing
from objMgr import ObjMgr
from gameSession import GameSession
from audio import BGM
from enemy import CountMover
import story



class BossBattleShip(enemy.EnemyBase):
    TILE_LEFT = 4
    TILE_TOP = 15
    TILE_RIGHT = 133
    TILE_BOTTOM = 44
    TILE_WIDTH = 134-3
    TILE_HEIGHT = 45-15
    moveTable0 = [
        [0, CountMover.SET_POS, 256.0, -96.0],
        [3500, CountMover.MOVE, 0.5, 0.0],
        [168, CountMover.MOVE, 0.5, 0.25],
        [200, CountMover.MOVE, 0.5, 0.0],
        [200, CountMover.MOVE, 0.5, -0.25],
        [240, CountMover.MOVE, 0.5, 0.0],
        [120, CountMover.MOVE, 0.5, -0.25],
        [20000, CountMover.MOVE, 0.5, 0.0],
    ]
    # stateTable0 = [
    #     [699, 0],
    #     [1049, 1],
    #     [1499, 2],
    #     [1799, 3],
    #     [5000, 4],
    # ]


    # moveTable0 = [
    #     [0, CountMover.SET_POS, 256.0, -80.0],
    #     [2800 -400, CountMover.MOVE, -0.5, 0.0],
    #     [3200 -400, CountMover.MOVE, 0.0, 0.0],
    #     [6000 -400, CountMover.MOVE, 0.5, 0.0],
    # ]
    # moveTable0 = [
    #     [0, CountMover.SET_POS, 256.0, -100.0],
    #     [90, CountMover.MOVE, -1.0, 0.0],
    #     [60, CountMover.ACCEL_RATE, 0.95, 0.95],
    #     [90, CountMover.MOVE, 0.0, 0.5],
    #     [30, CountMover.ACCEL_RATE, 0.95, 0.95],
    #     [120, CountMover.ACCEL_MAX, 0.0, -0.02, 0.0, -0.5],
    #     [30, CountMover.ACCEL_RATE, 0.95, 0.95],
    #     [120, CountMover.ACCEL_MAX, 0.0, 0.02, 0.0, 0.5],
    #     [30, CountMover.ACCEL_RATE, 0.95, 0.95],
    #     [0, CountMover.STOP],
    #     [120, CountMover.ACCEL_MAX, -0.02, 0.0, -1.0, 0.0],
    #     [60, CountMover.ACCEL_RATE, 0.95, 0.95],
    #     [9000, CountMover.STOP],
    # ]
    def __init__(self, t):
        super(__class__, self).__init__()
        self.x = 0
        self.y = 0
        self.moveTable = __class__.moveTable0
        self.mover = CountMover(self, self.moveTable, True)
        self.left = -12
        self.top = -12
        self.right = 12
        self.bottom = 12
        self.hitcolor1 = 10
        self.hitcolor2 = 7
        self.layer = gcommon.C_LAYER_GRD | gcommon.C_LAYER_UPPER_SKY
        self.exptype = gcommon.C_EXPTYPE_SKY_M
        self.ground = True
        self.hitCheck = True
        self.shotHitCheck = True
        self.shotEffect = False
        self.hp = boss.BOSS_FIRE_HP
        self.score = 15000
        self.bridge = BossBattleShipBridge(self, (63-__class__.TILE_LEFT) *8, (15 -__class__.TILE_TOP)*8)
        self.engine1 = BossBattleShipEngine(self, 0, (26 -15)*8)
        self.engine2 = BossBattleShipEngine(self, 1*8, (32 -15)*8)
        self.engine3 = BossBattleShipEngine(self, 0, (37 -15)*8)
        #self.stater = enemy.CountStater2(self, __class__.stateTable0, False, True)

        self.hatch = BossBattleShipHatch(self, (38-__class__.TILE_LEFT) *8, (42 -__class__.TILE_TOP)*8)
        self.storyManager = story.StoryManager(self, storyList)
        self.batteryList = []
        self.missileLauncherList = []
        self.appendBattery(12, 22, 0)
        self.appendBattery(18, 21, 0)
        self.appendBattery(23, 21, 0)
        self.appendBattery(28, 21, 0)
        self.appendBattery(33, 21, 0)
        self.appendBattery(49, 20, 0)
        self.appendBattery(53, 20, 0)
        self.appendBattery(11, 43, 1)       # 下
        self.appendBattery(73, 20, 0)
        self.appendBattery(84, 21, 0)
        self.appendBattery(88, 21, 0)
        self.appendBattery(92, 21, 0)
        self.appendBattery(103, 21, 0)
        self.appendBattery(107, 21, 0)
        self.appendBattery(111, 21, 0)
        self.appendBattery(109, 42, 1)
        self.appendBattery(94, 42, 1)

    def appendBattery(self, mx, my, direction):
        self.batteryList.append(BattleShipBattery(self, (mx -__class__.TILE_LEFT)*8, (my -__class__.TILE_TOP)*8, direction))

    def appended(self):
        ObjMgr.addObj(self.bridge)
        ObjMgr.addObj(self.engine1)
        ObjMgr.addObj(self.engine2)
        ObjMgr.addObj(self.engine3)
        ObjMgr.addObj(self.hatch)
        for obj in self.batteryList:
            obj.remove_min_x = -128*8
            ObjMgr.addObj(obj)

    def update(self):
        self.mover.update()
        if self.state == 0:
            self.storyManager.doStory()
            if self.storyManager.isEnd:
                self.storyManager = story.StoryManager(self, storyList2, loopFlag=True, diffTime=True)
                self.nextState()
        elif self.state == 1:
            # ハッチ爆発待ち
            self.storyManager.doStory()
            if self.hatch.removeFlag:
                gcommon.debugPrint("storyList3")
                self.removeMissileLauncher()
                self.hatch = None
                self.storyManager = story.StoryManager(self, storyList3, loopFlag=False, diffTime=True)
                self.nextState()
        elif self.state == 2:
            # ハッチから侵入
            self.storyManager.doStory()

        # self.stater.update()
        # if self.stater.state == 1:
        #     if self.stater.cnt % 20 == 0:
        #         p = int((self.stater.cnt-700)/20)
        #         if p <= 3:
        #             ObjMgr.addObj(BattleShipMissileLauncher1(self, (33-__class__.TILE_LEFT + p*5)*8, (32- __class__.TILE_TOP)*8, 33 +p*5, 32, 56))
        # elif self.stater.state == 2:
        #     if self.stater.cnt % 20 == 0:
        #         p = int((self.stater.cnt-1050)/20)
        #         if p <= 3:
        #             ObjMgr.addObj(BattleShipMissileLauncher1(self, (61-__class__.TILE_LEFT + p*5)*8, (32- __class__.TILE_TOP)*8, 61 +p*5, 32, 56))
        # elif self.stater.state == 3:
        #     if self.stater.cnt == 1500:
        #         ObjMgr.addObj(BossBattleShipLaserCannon(self, (91-__class__.TILE_LEFT)*8, (31-__class__.TILE_TOP)*8))
        # elif self.stater.state == 4:
        #     if self.stater.cnt % 20 == 0:
        #         p = int((self.stater.cnt-1800)/20)
        #         if p <= 3:
        #             ObjMgr.addObj(BattleShipMissileLauncher1(self, (102-__class__.TILE_LEFT + p*5)*8, (32- __class__.TILE_TOP)*8, 102 +p*5, 32, 56))

    def missileLauncher(self, params):
        baseMx = params[2]
        p = params[3]
        dr64 = params[4]
        obj = ObjMgr.addObj(BattleShipMissileLauncher1(self, (baseMx-__class__.TILE_LEFT + p*5)*8, (32- __class__.TILE_TOP)*8, baseMx +p*5, 32, dr64))
        self.missileLauncherList.append(obj)
        

    def removeMissileLauncher(self):
        for obj in self.missileLauncherList:
            if obj.removeFlag == False:
                obj.remove()
        self.missileLauncherList = []

    def laserCannon(self, params):
        ObjMgr.addObj(BossBattleShipLaserCannon(self, (91-__class__.TILE_LEFT)*8, (31-__class__.TILE_TOP)*8, params[2]))

    def torpedoLauncher(self, params):
        omx = params[2]
        omy = params[3]
        launcherType = params[4]
        ObjMgr.addObj(Torpedo1Launcher1(self, omx, omy, launcherType))

    def upperBackFire(self, params):
        time = params[2]
        pos = params[3]
        ObjMgr.addObj(BossBattleShipUpperBackFire(self, (98-__class__.TILE_LEFT)*8, (42 -__class__.TILE_TOP)*8, time))
        ObjMgr.addObj(BossBattleShipUpperBackFire(self, (101-__class__.TILE_LEFT)*8, (42 -__class__.TILE_TOP)*8, time))
        ObjMgr.addObj(BossBattleShipUpperBackFire(self, (104-__class__.TILE_LEFT)*8, (42 -__class__.TILE_TOP)*8, time))

    def spark(self, params):
        gcommon.debugPrint("BossBattleShipSpark")
        ObjMgr.addObj(BossBattleShipSpark(self, params[2], params[3], params[4]))

    def drawLayer(self, layer):
        if layer == gcommon.C_LAYER_GRD:
            pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 4, 15, 134-4, 45-15, 2)
            gcommon.Text2(200, 184, str(self.cnt), 7, 0)
        elif layer == gcommon.C_LAYER_UPPER_SKY:
            pyxel.bltm(gcommon.sint(self.x +(121 -__class__.TILE_LEFT) *8), gcommon.sint(self.y + (26 -__class__.TILE_TOP)*8), 1, 16, 91, 9, 2, 2)
            pyxel.bltm(gcommon.sint(self.x +(121 -__class__.TILE_LEFT) *8), gcommon.sint(self.y + (28 -__class__.TILE_TOP)*8), 1, 16, 91, 9, 2, 2)
            pyxel.bltm(gcommon.sint(self.x +(122 -__class__.TILE_LEFT) *8), gcommon.sint(self.y + (32 -__class__.TILE_TOP)*8), 1, 16, 94, 9, 3, 2)

    def setScroll(self, params):
        gcommon.debugPrint("setScroll")
        gcommon.cur_scroll_x = params[2]
        gcommon.cur_scroll_y = params[3]

    # 自機弾と敵との当たり判定
    def checkShotCollision(self, shot):
        if shot.removeFlag:
            return False
        return self.getTileHit(shot.x + (shot.right -shot.left+1)/2, shot.y + (shot.bottom -shot.top+1)/2)

    # 自機と敵との当たり判定
    def checkMyShipCollision(self):
        obj = ObjMgr.myShip
        #return self.getTileHit(obj.x + (obj.right -obj.left+1)/2, obj.y + (obj.bottom -obj.top+1)/2)
        return self.getTileHit(obj.x + 9, obj.y + 7)

    # 当たった場合の破壊処理
    # 破壊した場合True
    def doShotCollision(self, shot):
        return False

    def getTileData(self, mx, my):
        return pyxel.tilemap(1).get(mx, my)

    def getTileHit(self, x, y):
        if x < self.x or y < self.y or x >= (self.x + __class__.TILE_WIDTH*8) or y >= (self.y+ __class__.TILE_HEIGHT*8):
            return False
        mx = int((x -self.x)/8) + __class__.TILE_LEFT
        my = int((y -self.y)/8) + __class__.TILE_TOP
        #gcommon.debugPrint("mx=" + str(mx) + " my=" +str(my))
        no = self.getTileData(mx, my)
        return gcommon.mapAttribute2[no >> 5][no & 31] == "1"

storyList = [
    [700, BossBattleShip.missileLauncher, 33, 0, 56],
    [720, BossBattleShip.missileLauncher, 33, 1, 56],
    [740, BossBattleShip.missileLauncher, 33, 2, 56],
    [760, BossBattleShip.missileLauncher, 33, 3, 56],
    [1130, BossBattleShip.missileLauncher, 61, 0, 56],
    [1150, BossBattleShip.missileLauncher, 61, 1, 56],
    [1170, BossBattleShip.missileLauncher, 61, 2, 56],
    [1190, BossBattleShip.missileLauncher, 61, 3, 56],
    [1500, BossBattleShip.laserCannon, 0],
    [1800, BossBattleShip.missileLauncher, 102, 0, 56],
    [1820, BossBattleShip.missileLauncher, 102, 1, 56],
    [1840, BossBattleShip.missileLauncher, 102, 2, 56],
    [1860, BossBattleShip.missileLauncher, 102, 3, 56],
    [2070, BossBattleShip.missileLauncher, 102, 0, 0],
    [2090, BossBattleShip.missileLauncher, 102, 1, 0],
    [2110, BossBattleShip.missileLauncher, 102, 2, 0],
    [2130, BossBattleShip.missileLauncher, 102, 3, 0],
    [2400, BossBattleShip.torpedoLauncher, (126-BossBattleShip.TILE_LEFT), (26-BossBattleShip.TILE_TOP), 0],
    [2460, BossBattleShip.torpedoLauncher, (126-BossBattleShip.TILE_LEFT), (28-BossBattleShip.TILE_TOP), 0],
    [2520, BossBattleShip.torpedoLauncher, (127-BossBattleShip.TILE_LEFT), (32-BossBattleShip.TILE_TOP), 1],
    [2600, BossBattleShip.torpedoLauncher, (126-BossBattleShip.TILE_LEFT), (28-BossBattleShip.TILE_TOP), 0],
    [2630, BossBattleShip.torpedoLauncher, (127-BossBattleShip.TILE_LEFT), (32-BossBattleShip.TILE_TOP), 1],
    [2700, BossBattleShip.torpedoLauncher, (126-BossBattleShip.TILE_LEFT), (26-BossBattleShip.TILE_TOP), 0],
    [3200, BossBattleShip.missileLauncher, 102, 3, 16],
    [3220, BossBattleShip.missileLauncher, 102, 2, 16],
    [3350, BossBattleShip.missileLauncher, 102, 3, 16],
    [3370, BossBattleShip.missileLauncher, 102, 2, 16],
    [3390, BossBattleShip.missileLauncher, 102, 1, 16],
    [3410, BossBattleShip.missileLauncher, 102, 0, 16],
    [3680, BossBattleShip.spark, (105-BossBattleShip.TILE_LEFT)*8+3, (43-BossBattleShip.TILE_TOP)*8+7, 180],
    [3680, BossBattleShip.spark, (102-BossBattleShip.TILE_LEFT)*8+3, (43-BossBattleShip.TILE_TOP)*8+7, 180],
    [3680, BossBattleShip.spark, (99-BossBattleShip.TILE_LEFT)*8+3, (43-BossBattleShip.TILE_TOP)*8+7, 180],
    [3800, BossBattleShip.laserCannon, 1],
    [3808, BossBattleShip.upperBackFire, 200, 9],
    [4200, BossBattleShip.missileLauncher, 102, 1, 16],
    [4208, BossBattleShip.upperBackFire, 120, 9],
    [4220, BossBattleShip.missileLauncher, 102, 0, 16],
    [4500, BossBattleShip.missileLauncher, 61, 3, 16],
    [4520, BossBattleShip.missileLauncher, 61, 2, 16],
    [4600, BossBattleShip.laserCannon, 1],
    [4700, BossBattleShip.missileLauncher, 61, 3, 16],
    [4720, BossBattleShip.missileLauncher, 61, 1, 16],
    [4900, BossBattleShip.missileLauncher, 61, 0, 16],
    [4920, BossBattleShip.missileLauncher, 61, 2, 16],
    [5200, BossBattleShip.missileLauncher, 61, 0, 16],
    [5220, BossBattleShip.missileLauncher, 61, 1, 16],
    [5240, BossBattleShip.missileLauncher, 61, 2, 16],
    [5260, BossBattleShip.missileLauncher, 61, 3, 16],
    [5400, BossBattleShip.missileLauncher, 33, 3, 16],
    [5440, BossBattleShip.missileLauncher, 33, 2, 16],
    [5540, BossBattleShip.missileLauncher, 61, 1, 16],
    [5580, BossBattleShip.missileLauncher, 61, 0, 16],
]

storyList2 = [
    [90, BossBattleShip.missileLauncher, 33, 1, 16],
    [90, BossBattleShip.missileLauncher, 33, 3, 16],
    [120, None],
    [90, BossBattleShip.missileLauncher, 33, 2, 16],
    [90, BossBattleShip.missileLauncher, 33, 0, 16],
]

storyList3 = [
    [0, BossBattleShip.setScroll, 0.5, -0.25],
    [360, BossBattleShip.setScroll, 0.75, 0.0],
]

# エンジン
class BossBattleShipEngine(enemy.EnemyBase):
    def __init__(self, parent, ox, oy):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = self.parent.x + ox
        self.y = self.parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.left = 0
        self.top = 0
        self.right = 31
        self.bottom = 31
        self.hitcolor1 = 13
        self.hitcolor2 = 7
        self.layer = gcommon.C_LAYER_GRD
        self.exptype = gcommon.C_EXPTYPE_SKY_M
        self.ground = False
        self.hitCheck = True
        self.shotHitCheck = True
        self.hp = 300
        self.score = 500
        self.fire = BossBattleShipBackFire(self, 0, 0)

    def appended(self):
        ObjMgr.addObj(self.fire)

    def update(self):
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY


    def remove(self):
        super(__class__, self).remove()
        if self.fire != None and self.fire.removeFlag == False:
            self.fire.remove()
            self.fire = None

    def draw(self):
        pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 0,87, 3, 4, 2)

    def broken(self):
        super(__class__, self).broken()
        pyxel.tilemap(1).copy(4 +int(self.offsetX/8), 15 +int(self.offsetY/8), 1, 4 +int(self.offsetX/8), 50 +int(self.offsetY/8), 3, 4)

# エンジンバックファイア
class BossBattleShipBackFire(enemy.EnemyBase):
    def __init__(self, parent, ox, oy):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = self.parent.x + ox
        self.y = self.parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.left = -12*8
        self.top = 0
        self.right = -1
        self.bottom = 31
        self.hitcolor1 = 10
        self.hitcolor2 = 7
        self.layer = gcommon.C_LAYER_GRD
        self.exptype = gcommon.C_EXPTYPE_SKY_M
        self.ground = False
        self.hitCheck = False
        self.shotHitCheck = False

    def update(self):
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY
        self.state = int(self.cnt/120) % 4
        if self.state == 2:
            self.hitCheck = True
        else:
            self.hitCheck = False

    def draw(self):
        if self.state == 0:
            return
        elif self.state in (1, 3):
            sx = 0
            sy = 192
            dx = 32
            dy = 32
        elif self.state == 2:
            sx = 0
            sy = 128
            dx = 128
            dy = 32
        fy = 1 if self.cnt & 4 == 0 else -1
        if self.cnt & 2 == 0:
            pyxel.blt(gcommon.sint(self.x -dx), gcommon.sint(self.y), 1, sx, sy, dx, dy *fy, 0)
        else:
            pyxel.blt(gcommon.sint(self.x -dx), gcommon.sint(self.y), 1, sx, sy+32, dx, dy *fy, 0)

# 砲台
class BattleShipBattery(enemy.Battery0):
    # direction  0:上  1:下  2:右  3:左
    def __init__(self, parent, ox, oy, direction):
        super(__class__, self).__init__(parent.x + ox, parent.y + oy, direction)
        self.parent = parent
        self.offsetX = ox
        self.offsetY = oy
        self.ground = False
        self.hp = 50
        self.interval = int(60 / GameSession.enemy_shot_rate)
        self.first = int(60 / GameSession.enemy_shot_rate)

    def update(self):
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY
        self.shotFlag = False
        if self.direction == 0 and self.y > (ObjMgr.myShip.y -20):
            self.shotFlag = True
        elif self.direction == 1 and self.y < (ObjMgr.myShip.y +20):
            self.shotFlag = True

        super(__class__, self).update()

class BattleShipHomingMissile1(enemy.EnemyBase):
    directionTable = [
        [0, 1, 1],	# 0
        [1, 1, 1],	# 1
        [2, 1, 1],	# 2
        [3, 1, 1],	# 3
        [4, 1, 1],	# 4
        [3, -1, 1],	# 5
        [2, -1, 1],	# 6
        [1, -1, 1],	# 7
        [0, -1, 1],	# 8
        [1, -1, -1],	# 9
        [2, -1, -1],	# 10
        [3, -1, -1],	# 11
        [4, -1, -1],	# 12
        [3, 1, -1],		# 13
        [2, 1, -1],		# 14
        [1, 1, -1]		# 15
    ]
    def __init__(self, x, y, dr):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.dr = dr
        self.left = -4
        self.top = -4
        self.right = 4
        self.bottom = 4
        self.hp = 10
        self.layer = gcommon.C_LAYER_E_SHOT
        self.score = 10
        self.hitCheck = True
        self.shotHitCheck = True
        self.enemyShotCollision = False
        self.imageSourceIndex = 1
        self.imageSourceX = 32
        self.imageSourceY = 224
        self.speed = 4.5

    def update(self):
        if self.x < -32 or self.x > (gcommon.SCREEN_MAX_X+32) or self.y <-32 or self.y > (gcommon.SCREEN_MAX_Y+32):
            self.remove()
            return
        if self.cnt < 60 and self.speed > 3.0:
            self.speed -= 0.05
        if self.cnt < 120 and self.cnt & 1 == 0:
            tempDr = gcommon.get_atan_no_to_ship(self.x, self.y)
            self.dr = (self.dr + gcommon.get_leftOrRight(self.dr, tempDr)) & 63
        self.x += math.cos(gcommon.atan_table[self.dr & 63]) * self.speed
        self.y += math.sin(gcommon.atan_table[self.dr & 63]) * self.speed
        if self.cnt % 3 == 0:
            fx = math.cos(gcommon.atan_table[self.dr]) * 12
            fy = math.sin(gcommon.atan_table[self.dr]) * 12
            ObjMgr.addObj(enemyOthers.Smoke1(self.x -fx, self.y -fy))
                
    def draw(self):
        d = ((self.dr + 2) & 63)>>2
        fx = math.cos(gcommon.atan_table[d<<2]) * 8
        fy = math.sin(gcommon.atan_table[d<<2]) * 8
        if self.cnt & 2 == 0:
            if self.cnt & 1 == 0:
                pyxel.blt(self.x -7.5 -fx, self.y -7.5 -fy, self.imageSourceIndex, self.imageSourceX +80, self.imageSourceY, 16, 16, gcommon.TP_COLOR)
            else:
                pyxel.blt(self.x -7.5 -fx, self.y -7.5 -fy, self.imageSourceIndex, self.imageSourceX +96, self.imageSourceY, 16, 16, gcommon.TP_COLOR)
        t = __class__.directionTable[d]
        pyxel.blt(self.x -7.5, self.y -7.5, self.imageSourceIndex, self.imageSourceX + t[0] * 16, self.imageSourceY, 16 * t[1], 16 * -t[2], gcommon.TP_COLOR)

# ミサイル発射管
class BattleShipMissileLauncher1(enemy.EnemyBase):
    stateTable0 = [
        [5, 1],
        [5, 2],
        [5, 3],    # 発射
        [10, 3],    # 発射
        [10, 3],    # 発射
        [5, 2],
        [5, 1],
        [5, 0],
        [5, 4],
    ]
    def __init__(self, parent, ox, oy, mx, my, direction):
        super(__class__, self).__init__()
        self.parent = parent
        self.offsetX = ox
        self.offsetY = oy
        self.mx = mx
        self.my = my
        self.direction = direction
        self.layer = gcommon.C_LAYER_SKY
        self.ground = False
        self.hitCheck = False
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.stater = enemy.CountStater(self, __class__.stateTable0, False, False)

    def update(self):
        self.stater.update()
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY
        state = self.stater.state
        #if state in (0, 1, 2, 3):
        #    #if self.stater.cnt == 0:
        #    #    pyxel.tilemap(1).copy(self.mx, self.my, 1, 3 * state, 84, 3, 3)
        if state == 3:
            if self.stater.cnt == 0:
                px = self.x +12 + gcommon.cos_table[self.direction] * 6.0
                py = self.y +12 + gcommon.sin_table[self.direction] * 6.0
                obj = BattleShipHomingMissile1(px, py, self.direction)
                ObjMgr.addObj(obj)
        if self.stater.isEnd:
            self.remove()

    def draw(self):
        if self.stater.state <= 3:
            pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 3 * self.stater.state, 84, 3, 3)

# 艦橋
class BossBattleShipBridge(enemy.EnemyBase):
    def __init__(self, parent, ox, oy):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = self.parent.x + ox
        self.y = self.parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.left = 0
        self.top = 0
        self.right = 31
        self.bottom = 31
        self.hitcolor1 = 13
        self.hitcolor2 = 7
        self.layer = gcommon.C_LAYER_GRD
        self.exptype = gcommon.C_EXPTYPE_SKY_M
        self.ground = False
        self.hitCheck = True
        self.shotHitCheck = True
        self.hp = 800
        self.score = 2000

    def update(self):
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY

    def draw(self):
        pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 0, 92, 6, 4, 2)

    def broken(self):
        super(__class__, self).broken()
        pyxel.tilemap(1).copy(4 +int(self.offsetX/8), 15 +int(self.offsetY/8), 1, 4 +int(self.offsetX/8), 50 +int(self.offsetY/8), 6, 4)

# レーザー砲
#  state
#   0 : シャッター開く
#   1 : レーザー砲出てくる（明るくなる）
#   2 : 回転しながら攻撃（反時計回り）
#   3 : 回転しながら攻撃（時計回り）
#   4 : レーザー砲隠れる（暗くなる）
#   5 : シャッター閉まる
class BossBattleShipLaserCannon(enemy.EnemyBase):
    def __init__(self, parent, ox, oy, mode):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = self.parent.x + ox
        self.y = self.parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.mode = mode
        self.left = 0
        self.top = 0
        self.right = 31
        self.bottom = 31
        self.layer = gcommon.C_LAYER_SKY
        self.ground = False
        self.hitCheck = False
        self.shotHitCheck = False
        self.rad = 0.0
        self.shotCount = 0
        self.gunWidth = 48
        self.gunHeight = 48
        self.image = [None]* self.gunWidth
        self.work = [None]* self.gunHeight
        for y in range(self.gunWidth):
            self.image[y] = [0]*self.gunHeight
        img = pyxel.image(1)
        for y in range(self.gunWidth):
            for x in range(self.gunHeight):
                self.image[y][x] = img.get(x +128, y +128)

    def update(self):
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY
        if self.state == 0:
            # シャッター開く
            if self.cnt == 30:
                self.nextState()
        elif self.state == 1:
            # レーザー砲出てくる（明るくなる）
            if self.cnt == 30:
                self.nextState()
        elif self.mode == 0 and self.state == 2:
            # 回転しながら攻撃（反時計回り）
            self.rad -= math.pi * 1.5/180
            if self.cnt % 8 == 0:
                ObjMgr.addObj(boss.BossLaserBeam1(
                    self.x +56/2 + math.cos(self.rad) * 8,
                    self.y +40/2 + math.sin(self.rad) * 8, self.rad))
            if self.rad < -math.pi *150/180:
                self.nextState()
        elif self.mode == 0 and self.state == 3:
            self.rad += math.pi * 1.5/180
            # 回転しながら攻撃（時計回り）
            if self.cnt % 8 == 0:
                ObjMgr.addObj(boss.BossLaserBeam1(gcommon.sint(self.x +56/2), gcommon.sint(self.y +40/2), self.rad))
                if self.rad >= 0.0:
                    self.rad = 0.0
                    self.nextState()
        elif self.mode == 1 and self.state == 2:
            self.rad += math.pi * 1.5/180
            # 回転しながら攻撃（時計回り）
            if self.cnt % 8 == 0:
                ObjMgr.addObj(boss.BossLaserBeam1(gcommon.sint(self.x +56/2), gcommon.sint(self.y +40/2), self.rad))
                if self.rad > math.pi *150/180:
                    self.nextState()
        elif self.mode == 1 and self.state == 3:
            # 回転しながら攻撃（反時計回り）
            self.rad -= math.pi * 1.5/180
            if self.cnt % 8 == 0:
                ObjMgr.addObj(boss.BossLaserBeam1(
                    self.x +56/2 + math.cos(self.rad) * 8,
                    self.y +40/2 + math.sin(self.rad) * 8, self.rad))
            if self.rad <= 0.0:
                self.rad = 0.0
                self.nextState()
        elif self.state == 4:
            # レーザー砲隠れる（暗くなる）
            if self.cnt == 30:
                self.nextState()
        elif self.state == 5:
            # シャッター閉まる
            if self.cnt == 30:
                self.remove()

    def draw(self):
        if self.state in (0, 5):
            pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 30, 84, 7, 5)
            # レーザー砲
            drawing.Drawing.setBrightnessWithoutBlack2(-3)
            pyxel.blt(gcommon.sint(self.x +(56-self.gunWidth)/2), gcommon.sint(self.y +(40-self.gunHeight)/2), 1, 128, 128, self.gunWidth, self.gunHeight, 2)
            pyxel.pal()
            # シャッター
            if self.state == 0:
                y = int(self.cnt/2)
            else:
                y = 15 -int(self.cnt/2)
            if y <= 15:
                pyxel.blt(self.x, self.y +5, 1, 128, 176+y, 56, 15-y, 2)
                pyxel.blt(self.x, self.y +20+y, 1, 128, 176, 56, 15-y, 2)
            pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 23, 84, 7, 5, 2)
        elif self.state in (1, 4):
            pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 30, 84, 7, 5)
            # レーザー砲
            if self.state == 1:
                drawing.Drawing.setBrightnessWithoutBlack2(int(self.cnt/10) -3)
            else:
                drawing.Drawing.setBrightnessWithoutBlack2(-int(self.cnt/10))
            pyxel.blt(gcommon.sint(self.x +(56-self.gunWidth)/2), gcommon.sint(self.y +(40-self.gunHeight)/2), 1, 128, 128, self.gunWidth, self.gunHeight, 2)
            pyxel.pal()
        elif self.state in (2, 3):
            pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 30, 84, 7, 5)
            drawing.Drawing.setRotateImage(176, 128, 1, self.work, self.image, -self.rad, 2)
            pyxel.blt(gcommon.sint(self.x +(56-self.gunWidth)/2), gcommon.sint(self.y +(40-self.gunHeight)/2), 1, 176, 128, self.gunWidth, self.gunHeight, 2)
        
# 魚雷発射管
class Torpedo1Launcher1(enemy.EnemyBase):
    def __init__(self, parent, omx, omy, launcherType):
        super(__class__, self).__init__()
        self.parent = parent
        self.offsetX = omx *8
        self.offsetY = omy *8
        self.mx = BossBattleShip.TILE_LEFT + omx
        self.my = BossBattleShip.TILE_TOP +omy
        self.launcherType = launcherType
        self.ground = False
        self.hitCheck = False
        self.shotHitCheck = False
        self.enemyShotCollision = False
        #gcommon.debugPrint("Torpedo1Launcher1 " + str(self.parent.x + self.offsetX) + " " + str(self.parent.y + self.offsetY))

    def update(self):
        if self.launcherType == 0:
            ObjMgr.addObj(enemyShot.Torpedo1(self.parent.x + self.offsetX - 48, self.parent.y + self.offsetY +4))
        else:
            ObjMgr.addObj(enemyShot.Torpedo1(self.parent.x + self.offsetX - 48, self.parent.y + self.offsetY +8))
        self.remove()

# 浮上用エンジンのバックファイア
class BossBattleShipUpperBackFire(enemy.EnemyBase):
    def __init__(self, parent, ox, oy, time):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = self.parent.x + ox
        self.y = self.parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.time = time
        self.hitcolor1 = 10
        self.hitcolor2 = 7
        self.layer = gcommon.C_LAYER_GRD
        self.exptype = gcommon.C_EXPTYPE_SKY_M
        self.ground = False
        self.hitCheck = False
        self.shotHitCheck = False

    def update(self):
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY
        if self.state == 0:
            if self.cnt > 60:
                self.nextState()
        elif self.state == 1:
            if self.cnt > self.time:
                self.nextState()
        elif self.state == 2:
            if self.cnt > 40:
                self.remove()

    def draw(self):
        if self.state in (0, 2):
            if self.cnt % 3 == 0:
                pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 31, 91, 3, 2, 2)
        else:
            pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 31, 91, 3, 2, 2)
            n = self.cnt % 3
            if n == 0:
                pyxel.blt(self.x -39+12, self.y+4, 1, 160, 216, 40, 40, 0)
            elif n == 1:
                pyxel.blt(self.x -47+12, self.y+4, 1, 208, 208, 48, 48, 0)

# 地面との火花
class BossBattleShipSpark(enemy.EnemyBase):
    def __init__(self, parent, ox, oy, time):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = self.parent.x + ox
        self.y = self.parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.time = time
        self.layer = gcommon.C_LAYER_SKY
        self.ground = False
        self.hitCheck = False
        self.shotHitCheck = False

    def update(self):
        self.x = self.parent.x + self.offsetX
        if self.cnt % 10 == 0:
            enemy.Particle1.append(self.x, self.y, math.pi)

        if self.cnt > self.time:
            self.remove()

# 戦艦侵入ハッチ
class BossBattleShipHatch(enemy.EnemyBase):
    def __init__(self, parent, ox, oy):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = self.parent.x + ox
        self.y = self.parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.left = 8
        self.top = 0
        self.right = 12 * 7 -1
        self.bottom = 7
        self.hitcolor1 = 12
        self.hitcolor2 = 7
        self.layer = gcommon.C_LAYER_SKY
        self.hp = 1000
        self.ground = False
        self.hitCheck = True
        self.shotHitCheck = True

    def update(self):
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY
        if self.state == 100:
            if self.cnt % 10 == 0:
                cx = self.x + (self.right - self.left +1)/2 + random.randrange(-40, 40)
                cy = self.y + (self.bottom-self.top+1)/2 + random.randrange(-10, 10)
                enemy.create_explosion(cx, cy, gcommon.C_LAYER_EXP_SKY, gcommon.C_EXPTYPE_SKY_M)
            if self.cnt > 60:
                pyxel.tilemap(1).copy(37, 26, 1, 37, 61, 97-37+1, 76-61+1)
                ObjMgr.addObj(BossBattleShipBarrierWall(self.parent, (66 -BossBattleShip.TILE_LEFT)*8, (31-BossBattleShip.TILE_TOP)*8))
                self.remove()

    def draw(self):
        pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 40, 84, 12, 1, 2)

    def broken(self):
        #super().broken()
        self.setState(100)
        self.hitCheck = False
        self.shotHitCheck = False

# 隔壁
class BossBattleShipBarrierWall(enemy.EnemyBase):
    def __init__(self, parent, ox, oy):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = self.parent.x + ox
        self.y = self.parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.left = 0
        self.top = 0
        self.right = 8 * 3 -1
        self.bottom = 8 * 5 -1
        self.hitcolor1 = 12
        self.hitcolor2 = 7
        self.layer = gcommon.C_LAYER_SKY
        self.exptype = gcommon.C_EXPTYPE_SKY_M
        self.hp = 1000
        self.ground = False
        self.hitCheck = True
        self.shotHitCheck = True

    def update(self):
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY

    def draw(self):
        pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 40, 88, 3, 5, 2)
