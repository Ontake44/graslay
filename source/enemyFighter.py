import pyxel
import math
import random
import gcommon
from objMgr import ObjMgr
from audio import BGM
from drawing import Drawing
from enemy import EnemyBase
from enemy import CountMover
import enemy
from gameSession import GameSession

# 蝙蝠みたい？
class Fighter4(EnemyBase):
    def __init__(self, t):
        super(Fighter4, self).__init__()
        self.x = t[2]
        self.y = t[3]
        self.moveTable = t[4]
        self.shotFirst = t[5]
        self.left = 4
        self.top = 4
        self.right = 13
        self.bottom = 13
        self.layer = gcommon.C_LAYER_SKY
        self.hp = 1
        self.hitCheck = True
        self.shotHitCheck = True
        self.enemyShotCollision = False
        self.mover = CountMover(self, self.moveTable, False)
        self.score = 100

    def update(self):
        self.mover.update()
        #gcommon.debugPrint("x = " + str(self.x) + " y = " + str(self.y))
        if self.x < -16 or self.x > gcommon.SCREEN_MAX_X +16:
            self.remove()
            return
        if self.cnt == self.shotFirst:
            enemy.enemy_shot(self.x +10, self.y+10, 2, 0)

    def draw(self):
        n = 0
        width = 16
        # if self.mover.tableIndex == 1:
        #     if self.mover.cnt <= 20:
        #         n = 1
        #     elif self.mover.cnt <= 60:
        #         n = 2
        #     else:
        #         n = 1
        #         width = -16
        # elif self.mover.tableIndex > 1:
        #     n = 0
        #     width = -16
        if abs(self.mover.dx) < 0.5:
            n = 2
        elif abs(self.mover.dx) < 1.0:
            n = 1
        if self.mover.dx < 0:
            width = 16
        else:
            width = -16
        if self.cnt & 2 == 0:
            pyxel.blt(self.x, self.y, 2, 0 + n*16, 0, width, 16, 0)
        else:
            pyxel.blt(self.x, self.y, 2, 48 + n*16, 0, width, 16, 0)

# 蝙蝠みたいなやつ
class Fighter4Group(EnemyBase):
    # 下から上へ
    moveTable0 = [
        [90, 0, -2.0, 0.0],
        [80, 6, -math.pi, math.pi/80, 2.0],
        [200, 0, 2.0, 0.0],
    ]
    # 上から下へ
    moveTable1 = [
        [90, 0, -2.0, 0.0],
        [80, 6, -math.pi, -math.pi/80, 2.0],
        [200, 0, 2.0, 0.0],
    ]
    # 右上から左上へ
    moveTable2 = [
        [90, 0, -1.5, -1.5],
        [90, 6, -math.pi + math.pi/4, -math.pi/90, 2.0],
        [200, 0, 1.5, 1.5],
    ]
    # 右下から左上へ
    moveTable3 = [
        [150, 0, -1.5, -1.5],
        [90, 6, math.pi + math.pi/4, math.pi/90, 2.0],
        [300, 0, 1.5, 1.5],
    ]
    # 左上から左下へ
    moveTable4 = [
        [90, 0, 1.5, 1.5],
        [90, 6, math.pi/4, -math.pi/90, 2.0],
        [300, 0, -1.5, -1.5],
    ]

    moveTableTable = [moveTable0, moveTable1, moveTable2, moveTable3, moveTable4]
    initYTable = [160, 50, 150, 300, 20]
    def __init__(self, t):
        super(Fighter4Group, self).__init__()
        self.moveTableNo = t[2]
        self.shotFirst = t[3]
        self.interval = t[4]
        self.max = t[5]
        self.cnt2 = 0
        self.hitCheck = False
        self.shotHitCheck = False
        self.initY = 0

    def update(self):
        if self.cnt == 0:
            self.initY = __class__.initYTable[self.moveTableNo] + gcommon.map_y
            #gcommon.debugPrint("init y = " + str(self.initY)) 
        if self.cnt % self.interval == 0:
            shotFirst = self.shotFirst
            if GameSession.difficulty == gcommon.DIFFICULTY_EASY:
                shotFirst = -1
            elif GameSession.difficulty == gcommon.DIFFICULTY_NORMAL:
                if self.cnt2 != self.max -1:
                    shotFirst = -1
            x = 256
            if self.moveTableNo == 4:
                x = -16
            ObjMgr.addObj(Fighter4([0, 0, x, self.initY - gcommon.map_y, __class__.moveTableTable[self.moveTableNo], shotFirst]))
            self.cnt2 += 1
            if self.cnt2 >= self.max:
                self.remove()

    def draw(self):
        pass


class FireBird1(EnemyBase):
    def __init__(self, t):
        super(__class__, self).__init__()
        self.x = t[2]
        self.y = t[3]
        self.left = 4
        self.top = 4
        self.right = 13
        self.bottom = 13
        self.layer = gcommon.C_LAYER_SKY
        self.hp = 50
        self.hitCheck = True
        self.shotHitCheck = True
        self.enemyShotCollision = False
        self.score = 100
        self.imageIndex = 0
        self.first = 60 / GameSession.difficutlyRate
        self.dy = 0.0
        self.dr64 = 0		# 0 to 63

    def update(self):
        self.x -= 1.5
        if self.x < -24:
            self.remove()
        self.y = self.y + self.dy
        self.dy = gcommon.sin_table[int(self.dr64)] * 1.2
        self.dr64 = math.fmod(self.dr64 + 0.5, 63)
        if self.cnt == self.first:
            enemy.enemy_shot(self.x +5, self.y+12, 2, 0)
        self.imageIndex = (self.cnt>>3) & 3
        
    def draw(self):
        pyxel.blt(self.x, self.y, 2, self.imageIndex * 24, 120, 24, 18, 3)


