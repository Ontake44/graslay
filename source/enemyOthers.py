

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
    def __init__(self, mx, my, direction, first):
        super(__class__, self).__init__()
        pos = gcommon.mapPosToScreenPos(mx, my)
        self.x = pos[0] +3.5
        if direction == -1:
            self.y = pos[1] + 8 +12
        else:
            self.y = pos[1] -12
        self.direction = direction       # -1:上 1:下
        self.first = first
        self.ground = True
        self.layer = gcommon.C_LAYER_GRD
        self.hitCheck = False
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.life = 10
        self.lifeDelta = 0.5

    def update(self):
        if self.x < -24:
            self.remove()
            return
        if self.state == 0 and self.first == self.cnt:
            self.setState(1)
        elif self.state == 1:
            if self.cnt % 12 == 0:
                ObjMgr.insertObj(Fire1(self.x, self.y, self.direction, int(self.life)))
            self.life += self.lifeDelta
            if self.cnt > 120:
                self.lifeDelta = -0.25
                if self.life < 5.0:
                    self.remove()
            



class Fire1(EnemyBase):
    def __init__(self, x, y, direction, life):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.direction = direction       # -1:上 1:下
        self.life = life
        self.ground = True
        self.layer = gcommon.C_LAYER_GRD
        self.hitCheck = True
        self.shotHitCheck = False
        self.enemyShotCollision = False

    def update(self):
        if self.x < -12 or self.cnt > self.life:
            self.remove()
            return
        self.y += self.direction

    def draw(self):
        if self.cnt % 3 == 1:
            return
        x = 0
        if self.cnt > 40:
            x = 48
        elif self.cnt > 20:
            x = 24
        pyxel.blt(self.x -11.5, self.y -11.5, 2, x, 96, 24, 24, 3)
