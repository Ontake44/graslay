

import pyxel
import math
import random
import gcommon
from drawing import Drawing
from enemy import EnemyBase
from enemy import CountMover
import enemy


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
        gcommon.debugPrint("Arrow " + str(x) + " " + str(y))
        gcommon.debugPrint(str(gcommon.map_x) + " " + str(gcommon.map_y))

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

