

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
        self.layer = gcommon.C_LAYER_SKY
        self.hitCheck = True
        self.shotHitCheck = False
        self.enemyShotCollision = False

    def update(self):
        self.x += 3.0 * math.cos(self.rad)
        self.y += 3.0 * math.sin(self.rad)
        if self.x < -12 or self.y < -12 or self.x > (gcommon.SCREEN_MAX_X+12) or self.y > (gcommon.SCREEN_MAX_Y +12):
            self.remove()
            return

    def draw(self):
        pyxel.blt(self.x -11.5, self.y -11.5, 2, 2 * 24, 96, 24, 24, 3)
