import pyxel
import math
import random
import gcommon
from objMgr import ObjMgr
from drawing import Drawing
from enemy import EnemyBase
from enemy import CountMover
import enemy
from gameSession import GameSession

# 蛇のように動く回虫
class Worm3(EnemyBase):
    def __init__(self, t):
        super(Worm3, self).__init__()
        self.x = t[2]
        self.y = t[3]  - gcommon.map_y
        self.left = 4
        self.top = 2
        self.right = 23
        self.bottom = 13
        self.layer = gcommon.C_LAYER_SKY
        self.hp = 200
        self.hitCheck = True
        self.shotHitCheck = True
        self.enemyShotCollision = False
        self.score = 100
        self.rad = 0.0
        self.cellCount = 6
        self.cellDelay = 6
        self.cellY = []

    def update(self):
        if self.x < -(self.cellCount * 16+24) or self.x > gcommon.SCREEN_MAX_X +16:
            self.remove()
            return
        
        self.x -= 1.0
        self.y += math.sin(self.rad)/2
        self.cellY.insert(0, self.y +gcommon.map_y)
        if len(self.cellY) > (self.cellCount *  self.cellDelay +1):
            self.cellY.pop()

        self.rad += math.pi /40
        if self.rad >= math.pi*2:
            self.rad -= math.pi*2

        if GameSession.difficulty != gcommon.DIFFICULTY_EASY and self.cnt % 90 == 0:
            dr = 4
            count = 8
            angle = 8
            if GameSession.difficulty == gcommon.DIFFICULTY_NORMAL:
                dr = 32
                count = 2
                angle = 2
            else:
                dr = 32
                count = 4
                angle = 2
            enemy.enemy_shot_dr_multi(self.x, self.y + 9, 2, 0, dr, count, angle)

    def draw(self):
        pyxel.blt(self.x, self.y, 2, 0, 80, 24, 16, 3)
        index = 0
        for i in range(self.cellCount):
            index += self.cellDelay
            if index > len(self.cellY)-1:
                return
            if i < self.cellCount-1:
                pyxel.blt(self.x + 20 + i * 14, self.cellY[index] -gcommon.map_y, 2, 24, 80, 16, 16, 3)
            else:
                pyxel.blt(self.x + 20 + i * 14, self.cellY[index] -gcommon.map_y, 2, 40, 80, 16, 16, 3)

    def broken(self):
        super(__class__, self).broken()
        posList = []
        x = 27
        for i in range(0, len(self.cellY), self.cellDelay):
            posList.append([self.x +x, self.cellY[i]-gcommon.map_y + (self.bottom-self.top)/2 ])
            x += 14
        enemy.DelayedExplosions.create(posList, self.layer, self.exptype, 5)

# Cell3を放出する発射台
class CellLauncher1(EnemyBase):
    def __init__(self, t):
        super(CellLauncher1, self).__init__()
        pos = gcommon.mapPosToScreenPos(t[2], t[3])
        self.x = pos[0]
        self.y = pos[1]
        self.mirror = t[4]
        self.first = t[5] * 60
        self.left = 8
        self.top = 6
        self.right = 31
        self.bottom = 15
        if self.mirror:
            self.top = 15 -15
            self.bottom = 15 -6
            self.y -= 4
        self.layer = gcommon.C_LAYER_SKY
        self.exptype = gcommon.C_EXPTYPE_GRD_M
        self.hp = 100
        self.hitCheck = True
        self.shotHitCheck = True
        self.enemyShotCollision = False
        self.score = 100
        self.ground = True

    def update(self):
        if self.x < -40 or self.x > gcommon.SCREEN_MAX_X +16:
            self.remove()
            return
        if self.state == 0 and self.first == self.cnt:
            self.nextState()
        elif self.state == 1:
            if self.cnt > 180:
                self.nextState()
                return
            elif self.cnt % 30 == 0:
                ObjMgr.addObj(Cell3([0, 0, self.x +12, self.y, 0.0, -1.0 + self.mirror * 2.0, 60]))

    def draw(self):
        n = self.cnt % 30
        if self.state == 1 and (n >= 25 or n < 5): 
            pyxel.blt(self.x, self.y, 2, 40, 96, 40, 16 - self.mirror*32, 3)
        else:
            pyxel.blt(self.x, self.y, 2, 0, 96, 40, 16 - self.mirror*32, 3)

class Cell3(EnemyBase):
    def __init__(self, t):
        super(Cell3, self).__init__()
        self.x = t[2]
        self.y = t[3]
        self.dx = t[4]
        self.dy = t[5]
        self.launcherTime = t[6]
        self.left = 2
        self.top = 2
        self.right = 13
        self.bottom = 13
        self.hp = 10
        #self.layer = gcommon.C_LAYER_UNDER_GRD
        self.layer = gcommon.C_LAYER_GRD
        self.score = 100
        self.expsound = gcommon.SOUND_CELL_EXP
        self.shotFlag = True
        self.ground = True

    def update(self):
        if self.cnt > 900:
            self.remove()
        else:
            if self.launcherTime < self.cnt and self.cnt % 4 == 0:
                dr = gcommon.get_direction_my(self.x +8, self.y +8)
                self.dx = gcommon.direction_map[dr][0] * 1.25
                self.dy = -gcommon.direction_map[dr][1] * 1.25
            self.x += self.dx
            self.y += self.dy
        
    def draw(self):
        n = int(self.cnt/5) %3
        pyxel.blt(self.x, self.y, 2, 0 + n* 16, 120, 16, 16, 3)

