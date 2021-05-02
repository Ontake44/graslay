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


class Mine1(EnemyBase):
    def __init__(self, t):
        super(Mine1, self).__init__()
        self.x = t[2]
        self.paramY = t[3]
        self.movingFirst = t[4]
        self.movingHeight = t[5]
        self.left = 4
        self.top = 7
        self.right = 19
        self.bottom = 15
        self.layer = gcommon.C_LAYER_SKY
        self.hp = 40
        self.ground = True
        self.hitCheck = True
        self.shotHitCheck = True
        self.enemyShotCollision = False
        self.score = 100
        self.y = self.paramY - gcommon.map_y
        self.initY = self.y
        if self.movingHeight > 0:
            self.dy = 1
        else:
            self.dy = -1

    def appended(self):
        pass
        #self.y = self.paramY - gcommon.map_y
        # self.initY = self.y
        # if self.movingHeight > 0:
        #     self.dy = 1
        # else:
        #     self.dy = -1

    def update(self):
        self.initY -= gcommon.cur_scroll_y
        self.initY -= gcommon.cur_map_dy
        if self.state == 0:
            if self.cnt == self.movingFirst:
                self.nextState()
        elif self.state == 1:
            self.y += self.dy
            if self.movingHeight > 0:
                if self.dy > 0:
                    if self.y > (self.initY + self.movingHeight):
                        self.dy = -self.dy
                else:
                    if self.y < self.initY:
                        self.dy = -self.dy
            else:
                if self.dy > 0:
                    if self.y > self.initY:
                        self.dy = -self.dy
                else:
                    if self.y < (self.initY + self.movingHeight):
                        self.dy = -self.dy

    def draw(self):
        if self.state == 1:
            if self.cnt & 4 == 0:
                pyxel.blt(self.x, self.y, 2, 24, 16, 24, 24, 3)
            else:
                pyxel.blt(self.x, self.y, 2, 48, 16, 24, 24, 3)
        else:
            pyxel.blt(self.x, self.y, 2, 0, 16, 24, 24, 3)

    def broken(self):
        dr = 4
        count = 8
        angle = 8
        if GameSession.difficulty == gcommon.DIFFICULTY_EASY:
            dr = 0
            count = 4
            angle = 16
        elif GameSession.difficulty == gcommon.DIFFICULTY_NORMAL:
            dr = 4
            count = 8
            angle = 8
        else:
            dr = 2
            count = 16
            angle = 4
        enemy.enemy_shot_dr_multi(self.x + 8, self.y + 3, 3, 0, dr, count, angle)
        super(Mine1, self).broken()

