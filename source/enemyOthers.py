

from objMgr import ObjMgr
import pyxel
import math
import random
import gcommon
from drawing import Drawing
from enemy import EnemyBase
from enemy import CountMover
import enemy

# 警告表示用の矢印
class Arrow(EnemyBase):
    def __init__(self, x, y, direction, ground, text, dispTime):
        super(Arrow, self).__init__()
        self.x = x
        self.y = y
        self.direction = direction       # 0:上 1:下
        self.text = text
        self.ground = ground
        self.dispTime = dispTime
        self.layer = gcommon.C_LAYER_SKY
        self.hitCheck = False
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.ground = ground
        #gcommon.debugPrint("Arrow " + str(x) + " " + str(y))
        #gcommon.debugPrint(str(gcommon.map_x) + " " + str(gcommon.map_y))

    def update(self):
        if self.cnt >= self.dispTime:
            self.remove()

    def draw(self):
        if self.cnt & 4 == 0:
            if self.direction == 0:
                # 上
                pyxel.blt(self.x -7, self.y, 0, 0, 240, 15, 13, 0)
            else:
                # 下
                pyxel.blt(self.x -7, self.y -13, 0, 0, 240, 15, -13, 0)
        if self.text != None and self.text != "":
            pyxel.pal(7, 8)
            if self.direction == 0:
                Drawing.showText(self.x +10, self.y + 4, self.text)
            else:
                Drawing.showText(self.x +10, self.y -9, self.text)
            pyxel.pal()

# 矢印（マップ位置指定）
# mx, my, direction, text, dispTime
class ArrowOnMap(Arrow):
    def __init__(self, t):
        pos = gcommon.mapPosToScreenPos(t[2], t[3])
        super(ArrowOnMap, self).__init__(pos[0], pos[1], t[4], True, t[5], t[6])

# 矢印（スクリーン座標指定）
# x, y, direction, text, dispTime
class ArrowOnScreen(Arrow):
    def __init__(self, t):
        super(ArrowOnScreen, self).__init__(t[2], t[3], t[4], False, t[5], t[6])


# 炎の煙突
class FireChimney1(EnemyBase):
    def __init__(self, mx, my, direction, pattern):
        super(__class__, self).__init__()
        pos = gcommon.mapPosToScreenPos(mx, my)
        self.x = pos[0] +3.5
        if direction == -1:
            self.y = pos[1] + 8 +12
        else:
            self.y = pos[1] -12
        self.direction = direction       # -1:上 1:下
        if pattern == 0:
            self.first = 60
            self.length = 120
            self.lifeDelta1 = 0.5
            self.lifeDelta2 = -0.25
        else:
            self.first = 30
            self.length = 80
            self.lifeDelta1 = 0.5
            self.lifeDelta2 = -0.5
        self.ground = True
        self.layer = gcommon.C_LAYER_GRD
        self.hitCheck = False
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.life = 10

    def update(self):
        if self.x < -24:
            self.remove()
            return
        if self.state == 0 and self.first == self.cnt:
            self.setState(1)
        elif self.state == 1:
            if self.cnt % 12 == 0:
                ObjMgr.insertObj(Fire1(self.x, self.y, self.direction, int(self.life)))
            self.life += self.lifeDelta1
            if self.cnt > self.length:
                self.setState(2)
        elif self.state == 2:
            if self.cnt % 12 == 0:
                ObjMgr.insertObj(Fire1(self.x, self.y, self.direction, int(self.life)))
            self.life += self.lifeDelta2
            if self.life < 5.0:
                self.life = 10
                self.setState(0)
            
# 炎煙突から出る炎
class Fire1(EnemyBase):
    # x,y 中心座標
    def __init__(self, x, y, direction, life):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.direction = direction       # -1:上 1:下
        self.life = life
        self.left = -3.5
        self.top = -3.5
        self.right = 3.5
        self.bottom = 3.5
        self.ground = True
        self.layer = gcommon.C_LAYER_GRD
        self.hitCheck = True
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.imageIndex = 0

    def update(self):
        if self.x < -12 or self.cnt > self.life:
            self.remove()
            return
        self.y += self.direction
        if self.cnt > 40:
            self.imageIndex = 2
            self.left = -6.5
            self.top = -6.5
            self.right = 6.5
            self.bottom = 6.5
        elif self.cnt > 20:
            self.imageIndex = 1
            self.left = -4.5
            self.top = -4.5
            self.right = 4.5
            self.bottom = 4.5

    def draw(self):
        if self.cnt % 3 == 1:
            return
        pyxel.blt(self.x -11.5, self.y -11.5, 2, self.imageIndex * 24, 96, 24, 24, 3)


# ドラゴンが吐く炎（直線移動）
class Fire2(EnemyBase):
    # x,y 中心座標
    def __init__(self, x, y, deg):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.rad = math.radians(deg)
        self.left = -3.5
        self.top = -3.5
        self.right = 3.5
        self.bottom = 3.5
        self.layer = gcommon.C_LAYER_E_SHOT
        self.hitCheck = True
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.imageSourceX = 2 * 24
        self.imageSourceY = 96
        self.imageSourceIndex = 2
        self.speed = 3.0

    def update(self):
        self.x += self.speed * math.cos(self.rad)
        self.y += self.speed * math.sin(self.rad)
        if self.x < -12 or self.y < -12 or self.x > (gcommon.SCREEN_MAX_X+12) or self.y > (gcommon.SCREEN_MAX_Y +12):
            self.remove()
            return

    def draw(self):
        fx = 1 if self.cnt & 2 == 0 else -1
        fy = 1 if self.cnt & 4 == 0 else -1
        pyxel.blt(self.x -11.5, self.y -11.5, self.imageSourceIndex, self.imageSourceX, self.imageSourceY, 24 * fx, 24 * fy, 3)

# ドラゴンが吐く炎（誘導）
class Fire3(EnemyBase):
    # x,y 中心座標
    def __init__(self, x, y, deg):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.rad = math.radians(deg)
        self.speed = 2.0
        self.dx = self.speed * math.cos(self.rad)
        self.dy = self.speed * math.sin(self.rad)
        self.left = -3.5
        self.top = -3.5
        self.right = 3.5
        self.bottom = 3.5
        self.layer = gcommon.C_LAYER_E_SHOT
        self.hitCheck = True
        self.shotHitCheck = True
        self.hp = 1
        self.score = 20
        self.enemyShotCollision = False
        self.imageSourceX = 88
        self.imageSourceY = 64
        self.imageSourceIndex = 2
        self.omega1 = math.pi/20
        self.omega2 = math.pi/40

    def update(self):
        if self.cnt > 5 and (self.cnt & 1 == 0) and self.cnt < 100:
            if self.cnt < 40:
                self.omega = self.omega1
            else:
                self.omega = self.omega2
            rad = gcommon.get_atan_to_ship(self.x, self.y)
            rad = gcommon.radNormalize(rad - self.rad)
            if math.fabs(rad) > 0.1:
                if rad > 0:
                    self.rad += self.omega
                else:
                    self.rad -= self.omega
        self.x += self.speed * math.cos(self.rad)
        self.y += self.speed * math.sin(self.rad)
        if self.x < -12 or self.y < -12 or self.x > (gcommon.SCREEN_MAX_X+12) or self.y > (gcommon.SCREEN_MAX_Y +12):
            self.remove()
            return

    def draw(self):
        sx = 0 if self.cnt & 2 == 0 else 24
        pyxel.blt(self.x -11.5, self.y -11.5, self.imageSourceIndex, self.imageSourceX +sx, self.imageSourceY, 24, 24, 3)


class Prominence2Appear(EnemyBase):
    table = [
        [0, 0, 70],
        [5, 1, 70],
        [6, 2, 70],
        [7, 3, 70],
        [8, 4, 70],
        [9, 5, 70],
        [9, 4, 70],
        [8, 3, 70],
        [7, 2, 70],
        [6, 1, 70],
        [5, 0, 70],
    ]
    def __init__(self, t):
        super(__class__, self).__init__()
        self.x = t[2]
        self.y = t[3]
        self.left = -3.5
        self.top = -3.5
        self.right = 3.5
        self.bottom = 3.5
        self.layer = gcommon.C_LAYER_SKY
        self.ground = True
        self.hitCheck = True
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.rad = -math.pi/4
        self.radius = 70.0
        self.tableIndex = 0
        self.prevCnt = 0

    def update(self):
        while True:
            t = __class__.table[self.tableIndex]
            if t[0] == (self.cnt -self.prevCnt):
                ObjMgr.addObj(Prominence1(self.x, self.y, t[2], t[1]))
                self.tableIndex += 1
                if self.tableIndex >= len(__class__.table):
                    self.remove()
                    return
                self.prevCnt = self.cnt
            else:
                return

    def draw(self):
        pass

class Prominence1Appear(EnemyBase):
    def __init__(self, t):
        super(__class__, self).__init__()
        self.x = t[2]
        self.y = t[3]
        self.direction = t[4]        # 1:反時計回り -1:時計回り
        self.position = t[5]         # 1:下  -1:上
        self.left = -3.5
        self.top = -3.5
        self.right = 3.5
        self.bottom = 3.5
        self.layer = gcommon.C_LAYER_SKY
        self.ground = True
        self.hitCheck = True
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.rad = -math.pi/4
        self.radius = 100.0
        self.tableIndex = 0
        self.pCount = 1

    def update(self):
        if self.cnt % 5 == 0:
            if self.state == 0:
                self.addProminence()
                self.pCount += 1
                if self.pCount > 10:
                    self.state = 1
            else:
                self.addProminence()
                self.pCount -= 1
                if self.pCount < 1:
                    self.remove()
        
    def addProminence(self):
        s = 1.0
        for i in range(self.pCount):
            #ObjMgr.addObj(Prominence1(self.x, self.y, self.radius + (i -self.pCount/2)*3 , 1))
            if i > (self.pCount>>1):
                ObjMgr.addObj(Prominence2(self.x, self.y, self.radius + s * self.pCount *(self.pCount -i)/self.pCount, 1, self.direction, self.position))
            else:
                ObjMgr.addObj(Prominence2(self.x, self.y, self.radius + s * self.pCount *(self.pCount -i)/self.pCount, 0, self.direction, self.position))
            s = -1.0 if s==1.0 else 1


    def addProminenceTest(self):
        if self.pCount < 3:
            s = 1
            for i in range(self.pCount):
                #ObjMgr.addObj(Prominence1(self.x, self.y, self.radius + (i -self.pCount/2)*3 , 1))
                if i == 2:
                    ObjMgr.addObj(Prominence2(self.x, self.y, self.radius + s * 3 *(self.pCount -i)/self.pCount, 1))
                else:
                    ObjMgr.addObj(Prominence2(self.x, self.y, self.radius + s * 3 *(self.pCount -i)/self.pCount, 0))
                s = -1 if s==1 else 1
        elif self.pCount < 5:
            s = 1
            for i in range(self.pCount):
                #ObjMgr.addObj(Prominence1(self.x, self.y, self.radius + (i -self.pCount/2)*3 , 1))
                if i >= 3:
                    ObjMgr.addObj(Prominence2(self.x, self.y, self.radius + s * 5 *(self.pCount -i)/self.pCount, 1))
                else:
                    ObjMgr.addObj(Prominence2(self.x, self.y, self.radius + s * 5 *(self.pCount -i)/self.pCount, 0))
                s = -1 if s==1 else 1
        elif self.pCount < 6:
            s = 1
            for i in range(int(self.pCount)):
                #ObjMgr.addObj(Prominence1(self.x, self.y, self.radius + (i -self.pCount/3)*4 , 3))
                if i >= 3:
                    ObjMgr.addObj(Prominence2(self.x, self.y, self.radius + s * 7 * (self.pCount -i)/self.pCount , 1))
                else:
                    ObjMgr.addObj(Prominence2(self.x, self.y, self.radius + s * 7 * (self.pCount -i)/self.pCount , 0))
                s = -1 if s==1 else 1
        else:
            s = 1
            for i in range(int(self.pCount)):
                #ObjMgr.addObj(Prominence1(self.x, self.y, self.radius + (i -self.pCount/3)*4 , 3))
                if i >= 7:
                    ObjMgr.addObj(Prominence2(self.x, self.y, self.radius + s * 8 * (self.pCount -i)/self.pCount , 1))
                else:
                    ObjMgr.addObj(Prominence2(self.x, self.y, self.radius + s * 8 * (self.pCount -i)/self.pCount , 0))
                s = -1 if s==1 else 1

    def draw(self):
        pass


class Prominence1(EnemyBase):
    imageTable = [
        [176, 0, 16],
        [176, 16, 16],
        [176, 32, 16],
        [176, 48, 16],
        [176, 64, 24],
        [176, 88, 24]
    ]
    drTable = [
        [1, 1],
        [1, -1],
        [-1, 1],
        [-1, -1]
    ]
    # x,y 中心座標
    def __init__(self, x, y, radius, index):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.index = index
        self.left = -3.5
        self.top = -3.5
        self.right = 3.5
        self.bottom = 3.5
        self.layer = gcommon.C_LAYER_SKY
        self.ground = True
        self.hitCheck = True
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.rad = -math.pi/4

    def update(self):
        if self.x + self.radius + 20 < 0:
            self.remove()
            return
        self.rad += math.pi/120

    def draw(self):
        #gcommon.debugPrint(str(self.x) + " " + str(self.y))
        t = __class__.imageTable[self.index]
        dr = __class__.drTable[(self.cnt>>1) & 3]
        ss = t[2]/4
        x = self.x + self.radius * math.cos(self.rad) -t[2]/2 + random.randrange(-ss, ss)
        y = self.y -t[2]/2 - 1.1 * self.radius * math.sin(self.rad) + random.randrange(-ss, ss)
        pyxel.blt(x, y, 1, t[0], t[1], dr[0] * t[2], dr[1] * t[2], 0)

class Prominence2(EnemyBase):
    # sx, sy, fx, fy
    imageTable = [
        [176, 0, 1, 1], [176, 24, 1, 1], [176, 48, 1, 1], [176, 72, 1, 1],
        [176, 96, 1, 1], [176, 72, -1, 1], [176, 48, -1, 1], [176, 24, -1, 1],
        [176, 0, -1, 1], [176, 24, -1, -1], [176, 48, -1, -1], [176, 72, -1, -1],
        [176, 96, 1, -1], [176, 72, 1, -1], [176, 48, 1, -1], [176, 24, 1, -1]
    ]
    # x,y 中心座標
    def __init__(self, x, y, radius, index, direction, position):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.index = index
        self.direction = direction    # 1:反時計回り  -1:時計回り
        self.position = position        # 1:下  -1:上
        self.left = -3.5
        self.top = -3.5
        self.right = 3.5
        self.bottom = 3.5
        self.layer = gcommon.C_LAYER_SKY
        self.ground = True
        self.hitCheck = True
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.rad = -math.pi/4 * direction      # rad は -pi/4～pi*3/4
        self.omega = math.pi/120 
    def update(self):
        if self.x + self.radius + 20 < 0:
            self.remove()
            return
        self.rad += self.omega * self.direction
        if self.direction == 1 and self.rad >= math.pi * 2:
            self.rad -= math.pi * 2
        elif self.direction == -1 and self.rad <= 0.0:
            self.rad += math.pi * 2

        # if self.direction == 1:
        #     if self.rad >= math.pi*0.25 and self.rad <= math.pi*0.5:
        #         self.omega -= math.pi/11000
        #     elif self.rad >= math.pi*0.5 and self.rad <= math.pi*0.75:
        #         self.omega += math.pi/11000
        # else:
        #     if self.rad >= math.pi*1.25 and self.rad <= math.pi*1.5:
        #         self.omega += math.pi/10000
        #     elif self.rad >= math.pi*1.5 and self.rad <= math.pi*1.75:
        #         self.omega -= math.pi/10000
            

        # 当たり判定
        x = self.radius * math.cos(self.rad)
        y = -self.radius * 1.1 * math.sin(self.rad)
        self.left = x -3.5
        self.top = y -3.5
        self.right = x +3.5
        self.bottom = y +3.5

        if self.cnt % 30 == 0:
            if self.position == 1:
                if self.rad >= math.pi*1.875 or self.rad < math.pi/8:
                    #gcommon.DebugPrint("Splash")
                    enemy.Splash.appendParam(self.x +self.radius * math.cos(self.rad), self.y, gcommon.C_LAYER_SKY, self.rad - math.pi*0.5, math.pi*0.2,
                        speed=5, lifeMin=50, lifeMax=100, count=5, ground=True, color=10)
                elif self.rad >= math.pi*0.875 and self.rad < math.pi*1.125:
                    enemy.Splash.appendParam(self.x +self.radius * math.cos(self.rad), self.y, gcommon.C_LAYER_SKY, self.rad + math.pi*0.5, math.pi*0.2,
                        speed=5, lifeMin=50, lifeMax=100, count=5, ground=True, color=10)
            else:
                if self.rad >= math.pi*1.875 or self.rad < math.pi/8:
                    #gcommon.DebugPrint("Splash")
                    enemy.Splash.appendParam(self.x +self.radius * math.cos(self.rad), self.y, gcommon.C_LAYER_SKY, self.rad + math.pi*0.5, math.pi*0.2,
                        speed=5, lifeMin=50, lifeMax=100, count=5, ground=True, color=10)
                elif self.rad >= math.pi*0.875 and self.rad < math.pi*1.125:
                    enemy.Splash.appendParam(self.x +self.radius * math.cos(self.rad), self.y, gcommon.C_LAYER_SKY, self.rad - math.pi*0.5, math.pi*0.2,
                        speed=5, lifeMin=50, lifeMax=100, count=5, ground=True, color=10)

    def draw(self):
        #gcommon.debugPrint(str(self.x) + " " + str(self.y))
        deg = math.degrees(self.rad + math.pi/2)
        #gcommon.debugPrint("r =" + str(r))
        t = __class__.imageTable[int(gcommon.degNormalize(deg +360/32) /(360/16))]
        x = self.x + self.radius * math.cos(self.rad)  + random.randrange(-2, 2)
        y = self.y - 1.1 * self.radius * math.sin(self.rad) + random.randrange(-2, 2)
        if self.index == 1:
            pyxel.pal(8, 9)
            pyxel.pal(9, 10)
            pyxel.pal(10, 7)
        pyxel.blt(x -11.5, y -11.5, 1, t[0], t[1], 24 * t[2], 24 * t[3], 0)
        pyxel.pal()


# 移動壁
class MovableWall(EnemyBase):
    posTable = [
        [2, 2],         # 0
    ]
    sizeTable = [
        [12, 12],       # 0
    ]
    MoveTable = [
        [   # 0  下に12移動
            [96, enemy.CountMover.MOVE, 0.0, 1.0],
        ],
        [   # 1  上に12移動
            [96, enemy.CountMover.MOVE, 0.0, -1.0],
        ],
        [   # 2  右に12移動
            [96, enemy.CountMover.MOVE, 1.0, 0.0],
        ],
        [   # 3  左に12移動
            [96, enemy.CountMover.MOVE, -1.0, 0.0],
        ],
        [   # 4  左、右に移動
            [48, enemy.CountMover.MOVE, -1.0, 0.0],
            [120, enemy.CountMover.STOP],
            [48, enemy.CountMover.MOVE, 1.0, 0.0],
        ],
        [   # 5  下に6移動
            [48, enemy.CountMover.MOVE, 0.0, 1.0],
        ],
        [   # 6  上に6移動
            [48, enemy.CountMover.MOVE, 0.0, -1.0],
        ],
        [   # 7  右に6移動
            [48, enemy.CountMover.MOVE, 1.0, 0.0],
        ],
        [   # 8  左に6移動
            [48, enemy.CountMover.MOVE, -1.0, 0.0],
        ],
        [   # 9  下に6移動、上に12移動
            [48, enemy.CountMover.MOVE, 0.0, 1.0],
            [120, enemy.CountMover.STOP],
            [96, enemy.CountMover.MOVE, 0.0, -1.0],
        ],
        [   # 10  上に6移動、下に6移動、上に6移動
            [48, enemy.CountMover.MOVE, 0.0, -1.0],
            [60, enemy.CountMover.STOP],
            [48, enemy.CountMover.MOVE, 0.0, 1.0],
            [60, enemy.CountMover.STOP],
            [48, enemy.CountMover.MOVE, 0.0, -1.0],
        ],
        [   # 11  下に6移動、上に6移動、下に6移動
            [48, enemy.CountMover.MOVE, 0.0, 1.0],
            [60, enemy.CountMover.STOP],
            [48, enemy.CountMover.MOVE, 0.0, -1.0],
            [60, enemy.CountMover.STOP],
            [48, enemy.CountMover.MOVE, 0.0, 1.0],
        ],
        [   # 12  左に24移動、上に4移動
            [48, enemy.CountMover.MOVE, -2.0, 0.0],
            [60, enemy.CountMover.STOP],
            [96, enemy.CountMover.MOVE, 0.0, -0.25],
        ],
        [   # 13  左に24移動、下に4移動
            [48, enemy.CountMover.MOVE, -2.0, 0.0],
            [60, enemy.CountMover.STOP],
            [96, enemy.CountMover.MOVE, 0.0, 0.25],
        ],
        [   # 14  左に24移動、下に4移動、上に8移動
            [48, enemy.CountMover.MOVE, -2.0, 0.0],
            [30, enemy.CountMover.STOP],
            [48, enemy.CountMover.MOVE, 0.0, 0.5],
            [15, enemy.CountMover.STOP],
            [96, enemy.CountMover.MOVE, 0.0, -0.5],
        ],
    ]

    def __init__(self, mx, my, patternNo, startCount, moveNo):
        super(__class__, self).__init__()
        pos = gcommon.mapPosToScreenPos(mx, my)
        self.x = pos[0]
        self.y = pos[1]
        self.patternNo = patternNo
        self.moveNo = moveNo
        self.startCount = startCount
        self.left = 2
        self.top = 2
        self.tablePos = __class__.posTable[patternNo]
        self.tableSize = __class__.sizeTable[patternNo]
        self.right = self.tableSize[0] * 8 -2
        self.bottom = self.tableSize[1] * 8 -2
        self.layer = gcommon.C_LAYER_GRD
        self.hp = gcommon.HP_UNBREAKABLE
        self.ground = True
        self.hitCheck = True
        self.shotHitCheck = True
        self.enemyShotCollision = True
        self.shotEffect = False
        self.mover = CountMover(self, __class__.MoveTable[moveNo], False)

    def update(self):
        if self.state == 0:
            if self.cnt == self.startCount:
                self.nextState()
        else:
            self.mover.update()
        if self.x < -12*10:
            self.remove()

    def draw(self):
        pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, self.tablePos[0], self.tablePos[1], self.tableSize[0], self.tableSize[1], 2)

class Smoke1(enemy.EnemyBase):
    def __init__(self, x, y):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.layer = gcommon.C_LAYER_SKY
        self.ground = False
        self.hitCheck = False
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.nextCnt = random.randrange(7,11)
        self.index = 0

    def update(self):
        newIndex = int(self.cnt/self.nextCnt)
        if newIndex > 5:
            self.remove()
            return
        else:
            if newIndex != self.index:
                self.index = newIndex
                self.nextCnt = random.randrange(5,12)
    
    def draw(self):
        dx = 1 if self.cnt & 1 == 0 else -1
        dy = 1 if self.cnt & 2 == 0 else -1
        pyxel.blt(self.x -7.5, self.y -7.5, 1, 32 + self.index*16, 240, 16 * dx, 16 * dy, 0)

class Lift2(enemy.EnemyBase):
    def __init__(self, x, y, dy):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.dy = dy
        self.left = 0
        self.top = 0
        self.right = 63
        self.bottom = 23
        self.layer = gcommon.C_LAYER_UNDER_GRD
        self.ground = True
        self.hitCheck = True
        self.shotHitCheck = True
        self.enemyShotCollision = False
        self.hp = gcommon.HP_UNBREAKABLE

    def update(self):
        self.y += self.dy
        # if self.x < -64 or self.x >= 256:
        #     self.remove()
        #     return
        if self.dy > 0 and self.y >= gcommon.SCREEN_MAX_Y:
            self.remove()
            return
        elif self.dy < 0 and self.y < gcommon.SCREEN_MIN_Y -24:
            self.remove()
            return

    
    def draw(self):
        pyxel.blt(self.x, self.y, 2, 0, 0, 64, 24, 3)

class Lift2Appear(enemy.EnemyBase):
    def __init__(self, t):
        super(__class__, self).__init__()
        self.mx = t[2]
        self.my = t[3]
        self.dy = t[4]
        self.removeTime = t[5]
        self.ground = False
        self.hitCheck = False
        self.shotHitCheck = False
        self.enemyShotCollision = False

    def update(self):
        if gcommon.game_timer >= self.removeTime:
            self.remove()
            return
        if self.cnt % 120 == 0:
            pos = gcommon.mapPosToScreenPos(self.mx, self.my)
            ObjMgr.addObj(Lift2(pos[0], pos[1], self.dy))



class BarrierWallV1(enemy.EnemyBase):
    def __init__(self, t):
        super(__class__, self).__init__()
        pos = gcommon.mapPosToScreenPos(t[2], t[3])
        self.x = pos[0]
        self.y = pos[1]
        self.size = t[4]        # ２以上
        self.left = 0
        self.top = 0
        self.right = 15
        self.bottom = 16 * self.size -1
        self.layer = gcommon.C_LAYER_GRD
        self.exptype = gcommon.C_EXPTYPE_GRD_M
        self.ground = True
        self.hitCheck = True
        self.shotHitCheck = True
        self.enemyShotCollision = False
        self.hp = 500

    def update(self):
        if self.x < -16:
             self.remove()
             return
    
    def draw(self):
        pyxel.blt(self.x, self.y, 1, 240, 0, 16, 16, 0)
        for i in range(self.size-2):
            pyxel.blt(self.x, self.y +16 + 16*i, 1, 240, 8, 16, 16, 0)
        pyxel.blt(self.x, self.y+ 16*(self.size-1), 1, 240, 16, 16, 16, 0)



# [100, SET_SCROLL, 0.5, 0.0],
# [0, LOOP_Y, start, end]
#  0  1        2     3     4   5
# [0, MOVE_TO, MAPX, MAPY, DX, DY]
# [0, ACCEL_SCROLL_X, 2.0, 0.03125]
class ScrollController1(enemy.EnemyBase):
    SET_SCROLL = 0
    LOOP_X = 5
    LOOP_Y = 1
    WAIT = 2        # これが来ると外からnextIndex等をされるまで次に遷移しない
    MOVE_TO = 3
    STOP = 4
    ACCEL_SCROLL_X = 6
    WAIT_TIME = 7   # 指定した時間[2]次のindexに遷移しない

    def __init__(self, t):
        super(__class__, self).__init__()
        self.table = t
        self.hitCheck = False
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.tableIndex = 0

    def update(self):
        while(True):
            if self.tableIndex >= len(self.table):
                return
            t = self.table[self.tableIndex]
            n = t[1]
            if n == __class__.LOOP_Y:
                start = t[2]
                end = t[3]
                if gcommon.cur_scroll_y > 0.0:
                    if gcommon.map_y >= end:
                        gcommon.map_y = start
                else:
                    if gcommon.map_y <= end:
                        gcommon.map_y = start
                return
            elif n == __class__.LOOP_X:
                start = t[2]
                end = t[3]
                if gcommon.cur_scroll_x > 0.0:
                    if gcommon.map_x >= end:
                        gcommon.map_x = start
                else:
                    if gcommon.map_x <= end:
                        gcommon.map_x = start
                return
            elif n == __class__.WAIT:
                return
            elif n == __class__.WAIT_TIME:
                if self.cnt >= t[2]:
                    #gcommon.debugPrint("STOP NEXT")
                    self.nextIndex()
                else:
                    return
            elif n == __class__.MOVE_TO:
                gcommon.cur_scroll_x = t[4]
                gcommon.cur_scroll_y = t[5]
                indexFlag = False
                if gcommon.cur_scroll_x > 0.0:
                    if gcommon.map_x >= t[2]:
                        indexFlag = True
                elif gcommon.cur_scroll_x < 0.0:
                    if gcommon.map_y <= t[2]:
                        indexFlag = True
                if gcommon.cur_scroll_y > 0.0:
                    if gcommon.map_y >= t[3]:
                        indexFlag = True
                elif gcommon.cur_scroll_y < 0.0:
                    if gcommon.map_y <= t[3]:
                        indexFlag = True
                if indexFlag:
                    self.nextIndex()
                else:
                    return
            elif n == __class__.STOP:
                gcommon.cur_scroll_x = 0.0
                gcommon.cur_scroll_y = 0.0
                if self.cnt >= t[2]:
                    #gcommon.debugPrint("STOP NEXT")
                    self.nextIndex()
                else:
                    return
            elif n == __class__.ACCEL_SCROLL_X:
                gcommon.cur_scroll_x += t[3]
                if t[2] > 0 and gcommon.cur_scroll_x >= t[2]:
                    gcommon.cur_scroll_x = t[2]
                    self.nextIndex()
                elif t[2] < 0 and gcommon.cur_scroll_x <= t[2]:
                    gcommon.cur_scroll_x = t[2]
                    self.nextIndex()
                else:
                    return
            else:
                if t[0] == 0 or gcommon.game_timer == t[0]:
                    gcommon.setScroll(t[2], t[3])
                    self.nextIndex()
                    return
                else:
                    return
        
    def nextIndex(self):
        self.cnt = 0
        if self.tableIndex < len(self.table) -1:
            self.tableIndex += 1

    def setIndex(self, index):
        self.cnt = 0
        self.tableIndex = index

class Spark1(enemy.EnemyBase):
    def __init__(self, parent, ox, oy, layer):
        super(__class__, self).__init__()
        self.parent = parent
        if self.parent != None:
            self.offsetX = ox
            self.offsetY = oy
        else:
            self.x = ox
            self.y = oy
        self.layer = layer
        self.ground = False
        self.hitCheck = False
        self.shotHitCheck = False
        self.enemyShotCollision = False

    @classmethod
    def create(cls, parent, x, y, layer):
        ObjMgr.addObj(Spark1(parent, x, y, layer))

    def update(self):
        if self.parent != None:
            self.x = self.parent.x + self.offsetX
            self.y = self.parent.y + self.offsetY
        if self.cnt >= 8:
            self.remove()

    def draw(self):
        pyxel.blt(self.x -7.5, self.y -7.5, 0, (self.cnt>>1) * 16, 160, 16, 16, 0)
