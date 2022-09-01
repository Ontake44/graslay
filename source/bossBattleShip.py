
import pyxel
import math
import random
import gcommon
import enemy
import enemyOthers
import enemyShot
import boss
import drawing
import audio
import item
from objMgr import ObjMgr
from gameSession import GameSession
from audio import BGM
from enemy import CountMover
from enemyArmored import Walker2
from drawing import Drawing
import story

walker2MoveTable = [
                [32, CountMover.MOVE, -1.0, 0.0],
                [60, CountMover.STOP, 0.0, 0.0],
                [96, CountMover.MOVE, -1.0, 0.0],
                [60, CountMover.STOP, 0.0, 0.0],
                [32, CountMover.MOVE, 1.0, 0.0],
                [60, CountMover.STOP, 0.0, 0.0],
                [96, CountMover.MOVE, 1.0, 0.0],
                [1, CountMover.STOP, 0.0, 0.0],
]

hangeredFighter3Table = [
    [38, 38],
    [38, 36],
    [38, 29],
    [38, 27],
    [48, 38],
    [48, 36],
    [48, 29],
    [48, 27],
    [51, 38],
    [51, 36],
    [51, 29],
    [51, 27],
    [54, 38],
    [54, 36],
    [54, 29],
    [54, 27],
]


# walker2MoveTable = [
#                 [128, CountMover.MOVE, -1.0, 0.0],
#                 [60, CountMover.STOP, 0.0, 0.0],
#                 [96, CountMover.MOVE, 1.0, 0.0],
#                 [60, CountMover.STOP, 0.0, 0.0],
#                 [64, CountMover.MOVE, -1.0, 0.0],
#                 [60, CountMover.STOP, 0.0, 0.0],
#                 [96, CountMover.MOVE, 1.0, 0.0],
#                 [1, CountMover.STOP, 0.0, 0.0],
# ]

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
    # 機関室の静的オブジェクト
    #   ox, oy, mx, my, mwidth, mheight, left, top, right, bottom, hp):
    staticObjectTableInEngineRoom = [
        [70, 27, 70, 102, 10, 9, 0, 0, 10*8-1, 4*8-1, 100],
        [70, 31, 70, 122, 10, 9, 0, 5*8, 10*8-1, 9*8-1, 100],
        [71, 31, 71, 138, 9, 5, 0, 0, 8*8-1, 5*8-1, 1000],
        [80, 62-35, 80, 150, 10, 4, 0, 0, 10*8-1, 4*8-1, 500],
        [80, 71-35, 80, 159, 10, 4, 0, 0, 10*8-1, 4*8-1, 500],
        [80, 62-35, 80, 166, 10, 13, 3*8, 5*8, 6*8-1, 8*8-1, 1000],
    ]
    staticObjectTableInHangar = [
        [64, 72-35, 64, 94, 4, 3, 0, 0, 3*8-1, 3*8-1, gcommon.HP_NODAMAGE],
        [64, 62-35, 64, 84, 4, 3, 0, 0, 3*8-1, 3*8-1, gcommon.HP_NODAMAGE],
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
        self.layer = gcommon.C_LAYER_GRD | gcommon.C_LAYER_UPPER_SKY
        self.exptype = gcommon.C_EXPTYPE_SKY_M
        self.ground = True
        self.hitCheck = True
        self.shotHitCheck = True
        self.shotEffect = False
        self.hp = boss.BOSS_BATTLESHIP_HP
        self.score = 15000
        self.bridge = BossBattleShipBridge(self, (63-__class__.TILE_LEFT) *8, (15 -__class__.TILE_TOP)*8)
        self.engine1 = BossBattleShipEngine(self, 0, (26 -15)*8)
        self.engine2 = BossBattleShipEngine(self, 1*8, (32 -15)*8)
        self.engine3 = BossBattleShipEngine(self, 0, (37 -15)*8)
        #self.stater = enemy.CountStater2(self, __class__.stateTable0, False, True)

        self.hatch = BossBattleShipHatch(self, (38-__class__.TILE_LEFT) *8, (42 -__class__.TILE_TOP)*8)
        # 隔壁
        self.barrierWall = None
        # コア
        self.coreObj = None
        self.storyManager = story.StoryManager(self, __class__.storyList1)
        self.batteryList = []
        self.missileLauncherList = []
        self.breakableObjectList = []
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
        self.children = []
        self.torpedoLauncherMask = False

    def appendBattery(self, mx, my, direction):
        self.batteryList.append(BattleShipBattery(self, (mx -__class__.TILE_LEFT)*8, (my -__class__.TILE_TOP)*8, direction))

    def appended(self):
        # 戦艦が追加された後に以下を追加する
        self.addChild(self.bridge)
        self.addChild(self.engine1)
        self.addChild(self.engine2)
        self.addChild(self.engine3)
        self.addChild(self.hatch)
        for obj in self.batteryList:
            self.addChild(obj)
            #obj.remove_min_x = -128*8
            #ObjMgr.addObj(obj)

    def addChild(self, obj):
        self.children.append(ObjMgr.addObj(obj))
        return obj


    def update(self):
        self.mover.update()
        if self.state == 0:
            self.storyManager.doStory()
            if self.storyManager.isEnd:
                self.storyManager = story.StoryManager(self, __class__.storyList2, loopFlag=True, diffTime=True)
                self.nextState()
        elif self.state == 1:
            # ハッチ爆発待ち
            self.storyManager.doStory()
            if self.hatch.removeFlag:
                # ハッチが破壊されるとstoryList3を実行
                gcommon.debugPrint("storyList3")
                self.removeMissileLauncher()
                enemy.removeEnemyShot()
                self.enemyShotCollision = True
                self.hatch = None
                self.storyManager = story.StoryManager(self, self.storyList3, loopFlag=False, diffTime=True)
                # ハンガー状態の戦闘機配置
                self.createHangeredFighter3()
                # 中身スケスケ
                #pyxel.tilemap(1).copy(35, 26, 1, 35, 61, 97-35+1, 76-61+1)
                pyxel.tilemap(1).blt(35, 26, 1, 35, 61, 97-35+1, 76-61+1)

                # 1UPアイテム
                self.addChild(item.OneUpItem2(self, (36 -BossBattleShip.TILE_LEFT)*8 +7.5, (27-BossBattleShip.TILE_TOP)*8+7.5, False))

                # 隔壁生成
                self.barrierWall = self.addChild(BossBattleShipBarrierWall(self, (65 -BossBattleShip.TILE_LEFT)*8, (31-BossBattleShip.TILE_TOP)*8))
                # Walker2が出てくる壁
                self.createStaticObjects(__class__.staticObjectTableInHangar, layer=gcommon.C_LAYER_UPPER_SKY)
                self.nextState()
        elif self.state == 2:
            # storyList3
            #if self.cnt == 0:
            # ハッチから侵入
            self.storyManager.doStory()
            if self.cnt % 120 == 0:
                self.createWalker2(1)
            elif (self.cnt -30) % 200 == 0:
                self.createWalker2(-1)

            if self.barrierWall != None and self.barrierWall.removeFlag:
                # 壁が破壊される
                gcommon.debugPrint("storyList4")
                BGM.play(BGM.BOSS)
                self.storyManager = story.StoryManager(self, self.storyList4, loopFlag=False, diffTime=True)
                # 機関室？のオブジェクト生成
                self.createStaticObjectsInEngineRoom()
                # コア生成
                self.coreObj = self.addChild(BossBattleShipCore(self, (89 -__class__.TILE_LEFT)*8, (27 -__class__.TILE_TOP)*8))
                self.nextState()
        elif self.state == 3:
            # storyList4
            self.storyManager.doStory()
            if self.isBreakableObjectAllBroken() and self.storyManager.isEnd:
                gcommon.debugPrint("state 4")
                self.coreObj.setState(1)
                self.nextState()
            else:
                # 絶対壊れないように
                self.coreObj.hp = boss.BOSS_BATTLESHIP_HP
        elif self.state == 4:
            pass

    def remove(self):
        super().remove()
        for obj in self.children:
            if obj != None and obj.removeFlag == False:
                obj.remove()

    def isBreakableObjectAllBroken(self):
        if len(self.breakableObjectList) == 0:
            gcommon.debugPrint("zero!")

        for obj in self.breakableObjectList:
            if obj.removeFlag == False:
                return False
        return True


    # 機関室？のオブジェクト生成
    def createStaticObjectsInEngineRoom(self):
        for p in __class__.staticObjectTableInEngineRoom:
            self.breakableObjectList.append(self.addChild(BossBattleShipStaticPart(self, (p[0]- __class__.TILE_LEFT)*8, (p[1]- __class__.TILE_TOP)*8, p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10])))

    def createStaticObjects(self, table, layer=0):
        first = True
        for p in table:
            obj = self.addChild(BossBattleShipStaticPart(self, (p[0]- __class__.TILE_LEFT)*8, (p[1]- __class__.TILE_TOP)*8, p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10]))
            # if first:
            #     obj.test = True
            #     first = False
            if layer != 0:
                obj.layer = layer


    def createHangeredFighter3(self):
        for pos in hangeredFighter3Table:
            self.addChild(BossBattleShipHangeredFighter3(self, (pos[0] -__class__.TILE_LEFT)*8, (pos[1] -__class__.TILE_TOP)*8))

    def createWalker2(self, position):
        y = (38-BossBattleShip.TILE_TOP)*8 if position == 1 else (27-BossBattleShip.TILE_TOP)*8
        self.addChild(Walker2(self, (64 -BossBattleShip.TILE_LEFT)*8, y, walker2MoveTable, position))            

    def missileLauncher(self, params):
        baseMx = params[2]
        p = params[3]
        dr64 = params[4]
        obj = self.addChild(BattleShipMissileLauncher1(self, (baseMx-__class__.TILE_LEFT + p*5)*8, (32- __class__.TILE_TOP)*8, baseMx +p*5, 32, dr64))
        self.missileLauncherList.append(obj)
        

    def removeMissileLauncher(self):
        for obj in self.missileLauncherList:
            if obj.removeFlag == False:
                obj.remove()
        self.missileLauncherList = []

    def laserCannon(self, params):
        self.addChild(BossBattleShipLaserCannon(self, (91-__class__.TILE_LEFT)*8, (31-__class__.TILE_TOP)*8, params[2]))

    def torpedoLauncher(self, params):
        omx = params[2]
        omy = params[3]
        launcherType = params[4]
        self.addChild(Torpedo1Launcher1(self, omx, omy, launcherType))

    def setTorpedoLauncherMask(self, params):
        self.torpedoLauncherMask = params[2]

    def upperBackFire(self, params):
        time = params[2]
        pos = params[3]
        self.addChild(BossBattleShipUpperBackFire(self, (98-__class__.TILE_LEFT)*8, (42 -__class__.TILE_TOP)*8, time))
        self.addChild(BossBattleShipUpperBackFire(self, (101-__class__.TILE_LEFT)*8, (42 -__class__.TILE_TOP)*8, time))
        self.addChild(BossBattleShipUpperBackFire(self, (104-__class__.TILE_LEFT)*8, (42 -__class__.TILE_TOP)*8, time))

    def spark(self, params):
        gcommon.debugPrint("BossBattleShipSpark")
        self.addChild(BossBattleShipSpark(self, params[2], params[3], params[4]))

    def drawLayer(self, layer):
        if layer == gcommon.C_LAYER_GRD:
            Drawing.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 4, 15, 134-4, 45-15, 2)
            #gcommon.Text2(200, 184, str(self.cnt), 7, 0)
        elif layer == gcommon.C_LAYER_UPPER_SKY and self.torpedoLauncherMask:
            Drawing.bltm(gcommon.sint(self.x +(121 -__class__.TILE_LEFT) *8), gcommon.sint(self.y + (26 -__class__.TILE_TOP)*8), 1, 16, 91, 9, 2, 2)
            Drawing.bltm(gcommon.sint(self.x +(121 -__class__.TILE_LEFT) *8), gcommon.sint(self.y + (28 -__class__.TILE_TOP)*8), 1, 16, 91, 9, 2, 2)
            Drawing.bltm(gcommon.sint(self.x +(122 -__class__.TILE_LEFT) *8), gcommon.sint(self.y + (32 -__class__.TILE_TOP)*8), 1, 16, 94, 9, 3, 2)

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
        pos = ObjMgr.myShip.getCenterPos()
        #return self.getTileHit(obj.x + (obj.right -obj.left+1)/2, obj.y + (obj.bottom -obj.top+1)/2)
        return self.getTileHit(pos[0], pos[1])

    # 敵弾との当たり判定
    def checkEnemyShotCollision(self, shot):
        return self.getTileHit(shot.x + (shot.right -shot.left+1)/2, shot.y + (shot.bottom -shot.top+1)/2)

    # 当たった場合の破壊処理
    # 破壊した場合True
    def doShotCollision(self, shot):
        return False

    def getTileData(self, mx, my):
        #return pyxel.tilemap(1).get(mx, my)
        return gcommon.getTileMapNumber(1, mx, my)

    def getTileHit(self, x, y):
        if x < self.x or y < self.y or x >= (self.x + __class__.TILE_WIDTH*8) or y >= (self.y+ __class__.TILE_HEIGHT*8):
            return False
        mx = int((x -self.x)/8) + __class__.TILE_LEFT
        my = int((y -self.y)/8) + __class__.TILE_TOP
        #gcommon.debugPrint("mx=" + str(mx) + " my=" +str(my))
        no = self.getTileData(mx, my)
        return gcommon.mapAttribute2[no >> 5][no & 31] == "1"

    storyList1 = [
        [520 -400, setScroll, 1.0, -0.25],
        [1014 -400, setScroll, 1.0, 0.0],
        [700, missileLauncher, 33, 0, 56],
        [720, missileLauncher, 33, 1, 56],
        [740, missileLauncher, 33, 2, 56],
        [760, missileLauncher, 33, 3, 56],
        [1130, missileLauncher, 61, 0, 56],
        [1150, missileLauncher, 61, 1, 56],
        [1170, missileLauncher, 61, 2, 56],
        [1190, missileLauncher, 61, 3, 56],
        [1500, laserCannon, 0],
        [1800, missileLauncher, 102, 0, 56],
        [1820, missileLauncher, 102, 1, 56],
        [1840, missileLauncher, 102, 2, 56],
        [1860, missileLauncher, 102, 3, 56],
        [2070, missileLauncher, 102, 0, 0],
        [2090, missileLauncher, 102, 1, 0],
        [2110, missileLauncher, 102, 2, 0],
        [2130, missileLauncher, 102, 3, 0],
        [2800 -400, setScroll, 0.5, 0.25],
        [2400, setTorpedoLauncherMask, True],   # 魚雷管マスクON
        [2400, torpedoLauncher, (126-TILE_LEFT), (26-TILE_TOP), 0],
        [2460, torpedoLauncher, (126-TILE_LEFT), (28-TILE_TOP), 0],
        [2520, torpedoLauncher, (127-TILE_LEFT), (32-TILE_TOP), 1],
        [2600, torpedoLauncher, (126-TILE_LEFT), (28-TILE_TOP), 0],
        [2630, torpedoLauncher, (127-TILE_LEFT), (32-TILE_TOP), 1],
        [2700, torpedoLauncher, (126-TILE_LEFT), (26-TILE_TOP), 0],
        [2730, setTorpedoLauncherMask, False],  # 魚雷管マスクOFF
        [3280 -400, setScroll, 0.25, 0.0],
        [3200, missileLauncher, 102, 3, 16],
        [3220, missileLauncher, 102, 2, 16],
        [3350, missileLauncher, 102, 3, 16],
        [3370, missileLauncher, 102, 2, 16],
        [3390, missileLauncher, 102, 1, 16],
        [3410, missileLauncher, 102, 0, 16],
        [3680, spark, (105-TILE_LEFT)*8+3, (43-TILE_TOP)*8+7, 180],
        [3680, spark, (102-TILE_LEFT)*8+3, (43-TILE_TOP)*8+7, 180],
        [3680, spark, (99-TILE_LEFT)*8+3, (43-TILE_TOP)*8+7, 180],
        [3800, laserCannon, 1],
        [3808, upperBackFire, 200, 9],
        [4200, missileLauncher, 102, 1, 16],
        [4208, upperBackFire, 120, 9],
        [4220, missileLauncher, 102, 0, 16],
        [4500, missileLauncher, 61, 3, 16],
        [4520, missileLauncher, 61, 2, 16],
        [4600, laserCannon, 1],
        [4700, missileLauncher, 61, 3, 16],
        [4720, missileLauncher, 61, 1, 16],
        [4900, missileLauncher, 61, 0, 16],
        [4920, missileLauncher, 61, 2, 16],
        [5200, missileLauncher, 61, 0, 16],
        [5220, missileLauncher, 61, 1, 16],
        [5240, missileLauncher, 61, 2, 16],
        [5260, missileLauncher, 61, 3, 16],
        [5400, missileLauncher, 33, 3, 16],
        [5440, missileLauncher, 33, 2, 16],
        [5540, missileLauncher, 61, 1, 16],
        [5580, missileLauncher, 61, 0, 16],
        [6200 -400, setScroll, 0.5, 0.0],
    ]
    storyList2 = [
        [90, missileLauncher, 33, 1, 16],
        [90, missileLauncher, 33, 3, 16],
        [120, None],
        [90, missileLauncher, 33, 2, 16],
        [90, missileLauncher, 33, 0, 16],
    ]
    storyList3 = [
        [0, setScroll, 0.5, -0.25],
        [360, setScroll, 0.75, 0.0],
        [200, setScroll, 0.5, 0.0],
    ]
    storyList4 = [
        [0, setScroll, 0.75, 0.0],
        [976, setScroll, 0.5, 0.0],
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
        self.fire = BossBattleShipBackFire(self, 0, 15.5)

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
        Drawing.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 0,87, 3, 4, 2)

    def broken(self):
        super(__class__, self).broken()
        #pyxel.tilemap(1).copy(4 +int(self.offsetX/8), 15 +int(self.offsetY/8), 1, 4 +int(self.offsetX/8), 50 +int(self.offsetY/8), 3, 4)
        pyxel.tilemap(1).blt(4 +int(self.offsetX/8), 15 +int(self.offsetY/8), 1, 4 +int(self.offsetX/8), 50 +int(self.offsetY/8), 3, 4)

# エンジンバックファイア
#   右真ん中原点
class BossBattleShipBackFire(enemy.EnemyBase):
    def __init__(self, parent, ox, oy):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = self.parent.x + ox
        self.y = self.parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.collisionRects = gcommon.Rect.createFromList([
			[-92, -1.5, -78, 1.5], [-77, -4.5, -57, 4.5],[-56, -7.5, -30, 7.5], [-29, -11.5, -1, 11.5]
		])
        # self.left = -12*8
        # self.top = -15.5
        # self.right = -1
        # self.bottom = 15.5
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
            pyxel.blt(gcommon.sint(self.x -dx), gcommon.sint(self.y -dy/2), 1, sx, sy, dx, dy *fy, 0)
        else:
            pyxel.blt(gcommon.sint(self.x -dx), gcommon.sint(self.y -dy/2), 1, sx, sy+32, dx, dy *fy, 0)

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
        # 削除されるX座標
        self.remove_min_x = -128*8

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
        # 追尾時間
        self.trackingTime = 120
        if GameSession.isEasy():
            self.trackingTime = 100
        elif GameSession.isHard():
            self.trackingTime = 130

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
    stateTable0Easy = [
        [5, 1],
        [5, 2],
        [5, 3],    # 発射
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
        if GameSession.isEasy():
            self.stater = enemy.CountStater(self, __class__.stateTable0Easy, False, False)
        else:
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
                #gcommon.debugPrint("Ship " + str(self.parent.x) + " MissileLauncher1 " + str(self.x))
                px = self.x +12 + gcommon.cos_table[self.direction] * 6.0
                py = self.y +12 + gcommon.sin_table[self.direction] * 6.0
                obj = BattleShipHomingMissile1(px, py, self.direction)
                ObjMgr.addObj(obj)
        if self.stater.isEnd:
            self.remove()

    def draw(self):
        if self.stater.state <= 3:
            Drawing.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 3 * self.stater.state, 84, 3, 3)

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
        Drawing.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 0, 92, 6, 4, 2)

    def broken(self):
        super(__class__, self).broken()
        pyxel.tilemap(1).blt(4 +int(self.offsetX/8), 15 +int(self.offsetY/8), 1, 4 +int(self.offsetX/8), 50 +int(self.offsetY/8), 6, 4)

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
        self.laserInterval = 10
        if GameSession.isEasy():
            self.laserInterval = 14
        if GameSession.isHard():
            self.laserInterval = 8
        self.gunWidth = 48
        self.gunHeight = 48
        self.image = [None]* self.gunWidth
        self.work = [None]* self.gunHeight
        for y in range(self.gunWidth):
            self.image[y] = [0]*self.gunHeight
        img = pyxel.image(1)
        for y in range(self.gunWidth):
            for x in range(self.gunHeight):
                self.image[y][x] = img.pget(x +128, y +128)

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
            Drawing.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 30, 84, 7, 5)
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
            Drawing.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 23, 84, 7, 5, 2)
        elif self.state in (1, 4):
            Drawing.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 30, 84, 7, 5)
            # レーザー砲
            if self.state == 1:
                drawing.Drawing.setBrightnessWithoutBlack2(int(self.cnt/10) -3)
            else:
                drawing.Drawing.setBrightnessWithoutBlack2(-int(self.cnt/10))
            pyxel.blt(gcommon.sint(self.x +(56-self.gunWidth)/2), gcommon.sint(self.y +(40-self.gunHeight)/2), 1, 128, 128, self.gunWidth, self.gunHeight, 2)
            pyxel.pal()
        elif self.state in (2, 3):
            Drawing.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 30, 84, 7, 5)
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
        self.collisionRects = gcommon.Rect.createFromList([
			[11, 24, 15, 28], [16, 18, 21, 23],[22, 11, 28, 17], [27, 6, 33, 12], [32, 0, 39, 7]
		])
        for rect in self.collisionRects:
            rect.shift(-39+12, 4)
        self.offsetX = ox
        self.offsetY = oy
        self.time = time
        self.hitcolor1 = 10
        self.hitcolor2 = 7
        self.layer = gcommon.C_LAYER_GRD
        self.exptype = gcommon.C_EXPTYPE_SKY_M
        self.ground = False
        self.hitCheck = True
        self.shotHitCheck = False

    def update(self):
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY
        if self.state == 0:
            self.hitCheck = False
            if self.cnt > 60:
                self.nextState()
        elif self.state == 1:
            self.hitCheck = True
            if self.cnt > self.time:
                self.nextState()
        elif self.state == 2:
            self.hitCheck = False
            if self.cnt > 40:
                self.remove()

    def draw(self):
        if self.state in (0, 2):
            if self.cnt % 3 == 0:
                Drawing.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 31, 91, 3, 2, 2)
        else:
            Drawing.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 31, 91, 3, 2, 2)
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
        self.hp = 1000      #1000
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
                #pyxel.tilemap(1).copy(37, 26, 1, 37, 61, 97-37+1, 76-61+1)
                # 隔壁生成
                #self.parent.barrierWall = ObjMgr.addObj(BossBattleShipBarrierWall(self.parent, (66 -BossBattleShip.TILE_LEFT)*8, (31-BossBattleShip.TILE_TOP)*8))

                self.remove()

    def draw(self):
        Drawing.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 40, 84, 12, 1, 2)

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
        Drawing.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 40, 88, 3, 5, 2)

# ハンガーに吊るされた戦闘機
class BossBattleShipHangeredFighter3(enemy.EnemyBase):
    def __init__(self, parent, ox, oy):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = self.parent.x + ox
        self.y = self.parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.left = 2
        self.top = 5
        self.right = 22
        self.bottom = 15
        self.hitcolor1 = 12
        self.hitcolor2 = 7
        self.layer = gcommon.C_LAYER_SKY
        self.hp = 10
        self.score = 100
        self.ground = False
        self.hitCheck = True
        self.shotHitCheck = True

    def update(self):
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY

    def draw(self):
        pyxel.blt(gcommon.sint(self.parent.x) + self.offsetX, gcommon.sint(self.parent.y)+ self.offsetY, 1, 184, 176, 24, 16, 3)

# 静的オブジェクト
class BossBattleShipStaticPart(enemy.EnemyBase):
    def __init__(self, parent, ox, oy, mx, my, mwidth, mheight, left, top, right, bottom, hp):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = self.parent.x + ox
        self.y = self.parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.mx = mx
        self.my = my
        self.mwidth = mwidth
        self.mheight = mheight
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
        self.hp = hp
        self.hitcolor1 = 12
        self.hitcolor2 = 7
        self.layer = gcommon.C_LAYER_SKY
        self.exptype = gcommon.C_EXPTYPE_SKY_M
        self.ground = False
        self.hitCheck = True
        self.shotHitCheck = True
        self.test = False

    def update(self):
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY
        #if self.test:
        #    gcommon.debugPrint(str(self.x) + " " + str(self.parent.x))

    def draw(self):
        Drawing.bltm(gcommon.sint(self.parent.x)  + self.offsetX, gcommon.sint(self.y), 1, self.mx, self.my, self.mwidth, self.mheight, 2)



# コア
#  0 : 攻撃待ち
class BossBattleShipCore(enemy.EnemyBase):
    TILE_LEFT = 54
    TILE_TOP = 84
    TILE_RIGHT = 61
    TILE_BOTTOM = 96
    TILE_WIDTH = 8
    TILE_HEIGHT = 13
    def __init__(self, parent, ox, oy):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = self.parent.x + ox
        self.y = self.parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.left = 8*2
        self.top = 8*5
        self.right = 8*6-1
        self.bottom = 8 * 8 -1
        self.hitcolor1 = 12
        self.hitcolor2 = 7
        self.layer = gcommon.C_LAYER_SKY
        self.exptype = gcommon.C_EXPTYPE_SKY_M
        self.hp = boss.BOSS_BATTLESHIP_HP
        self.score = 15000
        self.ground = False
        self.hitCheck = True
        self.shotHitCheck = True
        self.lightningShutterPos = 0
        self.thunderShooter = None
        self.shotInterval = 120
        if GameSession.isEasy():
            self.shotInterval = 240
        if GameSession.isHard():
            self.shotInterval = 90
        #gcommon.debugPrint("Core")

    # 1: 待ち
    # 2: 開く
    # 3: 雷発射前びりびり
    # 4: 雷発射
    # 5: 閉じる
    def update(self):
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY
        if self.state == 1:
            self.lightningShutterPos = 0
            # 上下雷
            # if self.cnt == 0:
            #     gcommon.debugPrint("Core state 1")
            #     x = (91 -BossBattleShip.TILE_LEFT)*8
            #     y = (38-BossBattleShip.TILE_TOP)*8
            #     ObjMgr.addObj(BossBattleShipThunderShooter(self.parent, x, y))
            #elif self.cnt == 180:
            #    pass
            #elif self.cnt > 240:
            #    self.nextState()
            if self.cnt > 30:
                self.nextState()
        elif self.state == 2:
            # 開く
            self.lightningShutterPos = self.cnt>>1
            if self.cnt > 20:
                self.nextState()
        elif self.state == 3:
            # 雷発射前びりびり
            if self.cnt > 40:
                self.nextState()
        elif self.state == 4:
            if self.cnt % 40 == 0:
                x = self.parent.x + (90 -BossBattleShip.TILE_LEFT)*8+3
                y = self.parent.y + (33-BossBattleShip.TILE_TOP)*8+3
                ObjMgr.addObj(BossBattleShipLightning(x, y))
            if self.cnt > 270:
                self.nextState()
        elif self.state == 5:
            # 閉じる
            self.lightningShutterPos = 10 -(self.cnt>>1)
            if self.cnt > 20:
                self.nextState()
        elif self.state == 6:
            if self.cnt == 0:
                self.thunderShooter = ObjMgr.addObj(BossBattleShipThunderShooter(self.parent, (91 -BossBattleShip.TILE_LEFT)*8, (62-35-BossBattleShip.TILE_TOP)*8))
            if self.cnt > 360:
                self.setState(1)
        elif self.state == 100:
            # 破壊状態
            if self.cnt % 10 == 0:
                pos = gcommon.getCenterPos(self)
                enemy.create_explosion2(pos[0] + random.randrange(-30, 30), pos[1] + random.randrange(-30, 30), self.layer, gcommon.C_EXPTYPE_SKY_M, -1)
            if self.cnt > 60:
                self.nextState()
        elif self.state == 101:
            if self.cnt % 10 == 0:
                pos = gcommon.getCenterPos(self)
                enemy.create_explosion2(pos[0] + random.randrange(-30, 30), pos[1] + random.randrange(-30, 30), self.layer, gcommon.C_EXPTYPE_SKY_M, -1)
                n = int(self.cnt/10)
                if n >= 16:
                    self.nextState()
                    ObjMgr.objs.append(boss.BossExplosion(pos[0], pos[1], gcommon.C_LAYER_EXP_SKY))
        elif self.state == 102:
            if self.cnt > 110:
                self.remove()
                self.parent.remove()
                ObjMgr.addObj(enemy.Delay(enemy.StageClear,None,120))

        if self.state >= 1 and self.state < 100:
            if self.frameCount % self.shotInterval == 0:
                enemy.enemy_shot(self.x + 14, self.y +6, 2.0, 0)
            if self.frameCount % self.shotInterval == self.shotInterval/2:
                enemy.enemy_shot(self.x + 14, self.y +8*13 -6, 2.0, 0)

    def draw(self):
        if self.state < 101:
            Drawing.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 54, 84, 8, 13, 3)
            n = int(4 * math.sin(self.cnt * math.pi/60))
            drawing.Drawing.setBrightnessWithoutBlack(n)
            pyxel.blt(gcommon.sint(self.x +8), gcommon.sint(self.y+ 3*8), 2, 96, 176, 6*8, 7*8, 3)
            pyxel.pal()
            pyxel.blt(gcommon.sint(self.x), gcommon.sint(self.y+ 24 -self.lightningShutterPos), 2, 144, 176, 5*8, 28, 3)
            pyxel.blt(gcommon.sint(self.x), gcommon.sint(self.y+ 52 +self.lightningShutterPos), 2, 144, 204, 5*8, 28, 3)
            if self.state == 3:
                n = (self.cnt>>1) & 3
                if n in (0, 1):
                    fy = (self.cnt>>3) & 1
                    pyxel.blt(gcommon.sint(self.x +4), gcommon.sint(self.y+ 44), 1, 128 + n*16, 80, 16, 16 if fy == 0 else -16, 0)
        # else:
        #     n = int(self.cnt/10)
        #     if n > 15:
        #         n = 15
        #     for y in range(0, 6):
        #         Drawing.bltm(0, y*32, 1, 0, 100+n*4, 32, 4, 2)



    # 自機と敵との当たり判定
    def checkMyShipCollision(self):
        pos = ObjMgr.myShip.getCenterPos()
        return self.getTileHit(pos[0], pos[1])

    # # 自機弾と敵との当たり判定
    # def checkShotCollision(self, shot):
    #     if shot.removeFlag:
    #         return False
    #     return self.getTileHit(shot.x + (shot.right -shot.left+1)/2, shot.y + (shot.bottom -shot.top+1)/2)

    def getTileData(self, mx, my):
        return pyxel.tilemap(1).get(mx, my)

    def getTileHit(self, x, y):
        if x < self.x or y < self.y or x >= (self.x + __class__.TILE_WIDTH*8) or y >= (self.y+ __class__.TILE_HEIGHT*8):
            return False
        mx = int((x -self.x)/8) + __class__.TILE_LEFT
        my = int((y -self.y)/8) + __class__.TILE_TOP
        no = self.getTileData(mx, my)
        return gcommon.mapAttribute2[no >> 5][no & 31] == "1"

    def broken(self):
        if self.thunderShooter != None and self.thunderShooter.removeFlag == False:
            self.thunderShooter.remove()
            self.thunderShooter = None
        self.setState(100)
        GameSession.addScore(self.score)
        self.shotHitCheck = False
        self.hitCheck = False
        enemy.removeEnemyShot()


class BossBattleShipThunderShooter(enemy.EnemyBase):
    moveTable = [
                    [5*8, CountMover.MOVE, -2.0, 0.0],
                    [90, CountMover.STOP, 0.0, 0.0],
                    [5*8, CountMover.MOVE, -2.0, 0.0],
                    [60, CountMover.STOP, 0.0, 0.0],
                    [3*8, CountMover.MOVE, 2.0, 0.0],
                    [90, CountMover.STOP, 0.0, 0.0],
                    [5*8, CountMover.MOVE, 2.0, 0.0],
                    [90, CountMover.STOP, 0.0, 0.0],
                    [10*8, CountMover.MOVE, -2.0, 0.0],
                    [1, CountMover.STOP, 0.0, 0.0],
    ]
    def __init__(self, parent, ox, oy):
        super(__class__, self).__init__()
        self.parent = parent        # parent は戦艦
        self.x = ox
        self.y = oy
        self.left = 4
        self.top = 16
        self.right = 11
        self.bottom = 16+8*9-1
        self.hitcolor1 = 12
        self.hitcolor2 = 7
        self.layer = gcommon.C_LAYER_SKY
        self.exptype = gcommon.C_EXPTYPE_SKY_M
        self.hp = gcommon.HP_UNBREAKABLE
        self.ground = False
        self.hitCheck = False
        self.shotHitCheck = False
        self.mover = enemy.CountMover(self, __class__.moveTable, loopFlag=False, selfMove=False)
        self.thunder = False
        gcommon.debugPrint("BossBattleShipThunderShooter")

    def update(self):
        self.mover.update()
        if self.mover.isEnd:
            self.remove()
            return
        if self.mover.mode == CountMover.STOP and self.mover.cnt >= 30 and self.mover.cnt < 60:
            self.thunder = True
            self.hitCheck = True
        else:
            self.thunder = False
            self.hitCheck = False
        self.x = self.parent.x + self.mover.x
        self.y = self.parent.y + self.mover.y
        #gcommon.debugPrint(str(self.x) + " " + str(self.y))
    def draw(self):
        pyxel.blt(gcommon.sint(self.x), gcommon.sint(self.y), 1, 128, 64, 16, -16, 0)
        pyxel.blt(gcommon.sint(self.x), gcommon.sint(self.y +11*8), 1, 128, 64, 16, 16, 0)
        if self.thunder:
            for i in range(3):
                pyxel.blt(gcommon.sint(self.x+4), gcommon.sint(self.y + 16 + i*24), 1, 224 + random.randrange(0, 3) * 8, 128, 8, 24, 0)



class BossBattleShipLightning(enemy.EnemyBase):
    # 16方向
    # index, fx, fy
    imageTable = [
        [0, 1, 1],      # 0
        [1, 1, 1],      # 1
        [2, 1, 1],      # 2
        [3, 1, 1],      # 3
        [4, 1, 1],      # 4
        [3, -1, 1],     # 5
        [2, -1, 1],     # 6
        [1, -1, 1],     # 7
        [0, -1, 1],     # 8
        [1, -1, -1],    # 9
        [2, -1, -1],    # 10
        [3, -1, -1],    # 11
        [4, -1, -1],    # 12
        [3, 1, -1],     # 13
        [2, 1, -1],     # 14
        [1, 1, -1],     # 15
    ]
    def __init__(self, x, y):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0
        self.hitcolor1 = 12
        self.hitcolor2 = 7
        self.layer = gcommon.C_LAYER_E_SHOT
        self.ground = False
        self.hitCheck = True
        self.shotHitCheck = False
        self.rad = gcommon.get_atan_rad_to_ship(self.x, self.y)
        self.speed = 4.0
        self.dx = math.cos(self.rad) * self.speed
        self.dy = math.sin(self.rad) * self.speed
        self.table =  __class__.imageTable[int(gcommon.degNormalize(math.degrees(self.rad) +360/32) /(360/16))]
        self.posList = []
        #gcommon.debugPrint("BossBattleShipLightning")

    def update(self):
        self.x += self.dx
        self.y += self.dy
        if self.x < -8 or self.x > gcommon.SCREEN_MAX_X+8:
            self.remove()
            return
        if self.y < -8 or self.y > gcommon.SCREEN_MAX_Y+8:
            self.remove()
        if self.cnt % 2 == 0:
            self.posList.insert(0, [self.x, self.y, random.randrange(0, 3)])
            if len(self.posList) > 8:
                self.posList.pop()
            rects = []
            x0 = self.x
            y0 = self.y
            for pos in self.posList:
                x = pos[0] -self.x
                y = pos[1] -self.y
                rects.append(gcommon.Rect.create(x-3, y-3, x+3, y+3))

            self.collisionRects = rects
        #gcommon.debugPrint(str(self.x) + " " + str(self.y))

    def draw(self):
        pyxel.pal(7, random.randrange(6, 8))
        for pos in self.posList:
            pyxel.blt(pos[0] -3, pos[1] -3, 1, pos[2]* 8*5 + self.table[0]*8, 120, self.table[1] * 7, self.table[2] * 7, 0)
        pyxel.pal()
