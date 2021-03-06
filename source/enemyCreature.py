from enum import EnumMeta
from typing import get_origin
import pyxel
import math
import random
import gcommon
from objMgr import ObjMgr
from drawing import Drawing
from enemy import EnemyBase
from enemy import CountMover
import enemy
import enemyOthers
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
        self.hp = 150
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
            dr = 32
            count = 2
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
            if self.launcherTime < self.cnt and self.cnt % 4 == 0 and self.cnt < 180:
                dr = gcommon.get_direction_my(self.x +8, self.y +8)
                self.dx = gcommon.direction_map[dr][0] * 1.25
                self.dy = -gcommon.direction_map[dr][1] * 1.25
            self.x += self.dx
            self.y += self.dy
            if self.cnt % 90 == 89 and self.shotFlag:
                enemy.enemy_shot(self.x +8, self.y +8, 2, 0)
        
    def draw(self):
        n = int(self.cnt/5) %3
        pyxel.blt(self.x, self.y, 2, 0 + n* 16, 120, 16, 16, 3)


# 洞窟ボスから射出される蟲（水面下）
class Worm4(EnemyBase):
    shotIntervalTable = [240, 120, 90]
    def __init__(self, x, y, dx, dy):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.left = 2
        self.top = 2
        self.right = 13
        self.bottom = 13
        self.hp = 100
        self.layer = gcommon.C_LAYER_UNDER_GRD
        self.score = 300
        self.expsound = gcommon.SOUND_CELL_EXP
        self.ground = True
        self.cycleCount = 0
        self.bx = self.x
        self.shotInterval = __class__.shotIntervalTable[GameSession.difficulty]
        self.allCnt = 0

    def update(self):
        if self.state == 0:
            self.y += 1.0
            self.x -= 1.0
            self.bx = self.x
            if self.cnt > 30:
                self.nextState()
        elif self.state == 1:
            self.x += self.dx
            self.y += self.dy
            if self.x < 16 or self.x > 240:
                self.dx = -self.dx
            if self.cnt > 20:
                self.nextState()
        else:
            if self.bx < self.x:
                self.bx += 1
            elif self.bx > self.x:
                self.bx -= 1
            if self.cnt > 20:
                self.setState(1)
                self.cycleCount += 1
                if self.cycleCount % 6 == 0:
                    self.dx = -self.dx
                if self.cycleCount % 4 == 0:
                    self.dy = -self.dy
        self.allCnt += 1
        if self.allCnt % self.shotInterval == 0 and self.state in (1, 2):
            enemy.enemy_shot(self.x +8, self.y +8, 2, 0)
        
    def draw(self):
        if self.x < self.bx:
            pyxel.blt(self.x, self.y, 2, 0, 184, 8, 16, 0)
            pyxel.blt(self.bx +8, self.y, 2, 8, 184, 8, 16, 0)
            l = int(self.bx - self.x)
            if l > 0:
                pyxel.blt(self.x +8, self.y, 2, 16, 184, l, 16, 0)
        else:
            pyxel.blt(self.bx, self.y, 2, 0, 184, 8, 16, 0)
            pyxel.blt(self.x +8, self.y, 2, 8, 184, 8, 16, 0)
            l = int(self.x - self.bx)
            if l > 0:
                pyxel.blt(self.bx +8, self.y, 2, 16, 184, l, 16, 0)

# 洞窟ボスから射出される蝙蝠の卵（水面）
class Worm5(EnemyBase):
    coolTimeTable = [360, 240, 120]
    def __init__(self, parent, x, y, dx, dy):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.left = 2
        self.top = 2
        self.right = 13
        self.bottom = 13
        self.hp = 100
        self.layer = gcommon.C_LAYER_UNDER_GRD
        self.score = 300
        self.expsound = gcommon.SOUND_CELL_EXP
        self.ground = True
        self.cycleCount = 0

    def update(self):
        if self.state == 0:
            # 上に射出
            if self.dy < 4.0:
                self.dy += 0.060
            elif self.dy > 0:
                # ボスから射出されるときはレイヤが後ろなので
                self.layer = gcommon.C_LAYER_SKY
            self.x += self.dx
            self.y += self.dy
            if self.y + gcommon.map_y +8 > gcommon.waterSurface_y:
                enemy.WaterSplash.appendDr(self.x +8, gcommon.waterSurface_y -gcommon.map_y, gcommon.C_LAYER_SKY, math.pi * 1.5, math.pi/6, 30)
                self.nextState()
        elif self.state == 1:
            self.dx *= 0.5
            self.dy -= 0.5
            self.x += self.dx
            self.y += self.dy
            if self.dy < -2.0:
                self.nextState()
        elif self.state == 2:
            self.dx *= 0.8
            self.dy *= 0.8
            self.x += self.dx
            self.y += self.dy
            if abs(self.dy) < 0.1:
                self.nextState()
        elif self.state == 3:
            if self.cnt >= 60:
                self.remove()
                enemy.Particle2.append(self.x +8, self.y+8, 20)
                rad = math.pi*1.25 if self.x < 112 else math.pi*1.75
                obj = Bat1a(self.parent, self.x, self.y, rad)
                self.parent.appendBat(obj)
                ObjMgr.addObj(obj)
        
    def draw(self):
        pyxel.blt(self.x, self.y, 2, 0, 200, 16, 16, 0)

    def broken(self):
        super().broken()
        self.parent.appendBat(ObjMgr.addObj(enemy.DummyEnemy(__class__.coolTimeTable[GameSession.difficulty])))

# 蝙蝠？みたいなの
# BossCaveから射出される卵から出現
class Bat1a(EnemyBase):
    shotIntervalTable = [240, 120, 90]
    coolTimeTable = [360, 240, 120]
    def __init__(self, parent, x, y, rad):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = x
        self.y = y
        self.rad = rad
        self.speed = 2.0
        self.dx = math.cos(self.rad) * self.speed
        self.dy = math.sin(self.rad) * self.speed
        self.left = 4
        self.top = 4
        self.right = 13
        self.bottom = 13
        self.layer = gcommon.C_LAYER_SKY
        self.hp = 1
        self.hitCheck = True
        self.shotHitCheck = True
        self.enemyShotCollision = False
        self.score = 100
        self.shotInterval = __class__.shotIntervalTable[GameSession.difficulty]
        self.allCnt = 0

    def update(self):
        self.x += self.dx
        self.y += self.dy
        if (self.x <= 2 and self.dx < 0 ) or (self.x >= gcommon.SCREEN_MAX_Y -2 and self.dx > 0):
            self.dx = -self.dx
        if (self.y < (72*8 - gcommon.map_y) and self.dy < 0) or ((self.y +16) > (gcommon.waterSurface_y -gcommon.map_y) and self.dy > 0):
            self.dy = -self.dy
        self.allCnt += 1
        if self.allCnt % self.shotInterval == 0:
            enemy.enemy_shot(self.x +8, self.y +8, 2, 0)

    def draw(self):
        width = 16
        if self.dx < 0:
            width = 16
        else:
            width = -16
        if self.cnt & 2 == 0:
            pyxel.blt(self.x, self.y, 2, 0, 0, width, 16, 0)
        else:
            pyxel.blt(self.x, self.y, 2, 48, 0, width, 16, 0)

    def broken(self):
        super().broken()
        self.parent.appendBat(ObjMgr.addObj(enemy.DummyEnemy(__class__.coolTimeTable[GameSession.difficulty])))

class FireWorm1(EnemyBase):
    imageTable = [
        [0, -1, 1], [1, -1, 1], [2, -1, 1], [3, -1, 1],
        [4, 1, 1], [3, 1, 1], [2, 1, 1], [1, 1, 1],
        [0, 1, 1], [1, 1, -1], [2, 1, -1], [3, 1, -1],
        [4, 1, -1], [3, -1, -1], [2, -1, -1], [1, -1, -1]
    ]
    def __init__(self, t):
        super(__class__, self).__init__()
        self.x = t[2]
        self.y = t[3]
        self.moveTable = t[5]
        self.stateTable = t[6]
        self.layer = gcommon.C_LAYER_GRD
        self.ground = True
        self.hitCheck = True
        self.shotHitCheck = True
        self.hp = gcommon.HP_UNBREAKABLE
        self.mover = CountMover(self, self.moveTable, False)
        if self.stateTable != None:
            self.stater = enemy.CountStater(self, self.stateTable)
        else:
            self.stater = None
        self.mover.deg = t[4]
        self.cellCount = 12
        self.cellDelay = 22
        self.cellList = []
        self.collisionRects = []
        for i in range(self.cellCount * self.cellDelay):
            self.cellList.append([self.x, self.y, self.mover.deg])
    
    def update(self):
        self.mover.update()
        if self.mover.isEnd:
            # 移動テーブル終わりで削除
            self.remove()
            return
        if self.stater != None:
            self.stater.update()
            if self.stater.state == 1:
                if self.stater.cnt % 10 == 0:
                    #enemy.enemy_shot(self.x, self.y, 3, 0)
                    ObjMgr.addObj(enemyOthers.Fire2(self.x, self.y, self.mover.deg))
                    ObjMgr.addObj(enemyOthers.Fire2(self.x, self.y, math.fmod(self.mover.deg +20, 360)))
                    ObjMgr.addObj(enemyOthers.Fire2(self.x, self.y, math.fmod(self.mover.deg -20, 360)))

        for c in self.cellList:
            c[0] -= gcommon.cur_scroll_x
        self.cellList.insert(0, [self.x, self.y, self.mover.deg])
        if len(self.cellList) > (self.cellCount *  self.cellDelay +1):
            self.cellList.pop()
        
        self.collisionRects.clear()
        index = 0
        x = self.x
        y = self.y
        for i in range(self.cellCount):
            # 当たり判定設定
            c = self.cellList[index]
            cx = c[0] -self.x
            cy = c[1] -self.y
            self.collisionRects.append(gcommon.Rect.create(cx -12, cy-12, cx+12, cy+12))

            # 火の粉
            if c[1] > 190 and c[1] < 193:
                x = c[0] + random.randrange(-20, 20)
                enemy.Splash.appendParam(x, c[1], gcommon.C_LAYER_SKY, math.pi*1.5, math.pi*0.2,
                    speed=5, lifeMin=50, lifeMax=100, count=20, ground=True, color=10)
            elif c[1] > 4 and c[1] < 10:
                x = c[0] + random.randrange(-20, 20)
                enemy.Splash.appendParam(x, c[1], gcommon.C_LAYER_SKY, math.pi*0.5, math.pi*0.2,
                    speed=5, lifeMin=50, lifeMax=100, count=20, ground=True, color=10)

            index += self.cellDelay

    def draw(self):
        # index = self.cellCount * self.cellDelay -self.cellDelay
        # tail = True
        # for i in range(self.cellCount):
        #     if index >= 0 and index < len(self.cellList):
        #         if tail:
        #             self.drawCell(self.cellList[index][0], self.cellList[index][1], self.cellList[index][2] +180)
        #             tail = False
        #         else:
        #             self.drawCell(self.cellList[index][0], self.cellList[index][1], self.cellList[index][2])
        #         index -= self.cellDelay
        length = self.cellCount
        index = int(self.cellDelay/2)
        for i in range(length -1):
            pyxel.blt(self.cellList[index][0] -19.5, self.cellList[index][1] -19.5, 2, 200, 0, 40, 40, 2)
            index += self.cellDelay
        index = 0
        for i in range(length):
            if index == 0:
                self.drawCell(self.cellList[index][0], self.cellList[index][1], self.cellList[index][2])
            elif i == length -1:
                self.drawCell(self.cellList[index][0], self.cellList[index][1], self.cellList[index][2] +180)
            else:
                self.drawCell2(self.cellList[index][0], self.cellList[index][1], self.cellList[index][2])
            index += self.cellDelay

    def drawCell(self, x, y, deg):
        n = int((deg +360/32) * 16/360) & 15
        tbl = __class__.imageTable[n]
        pyxel.blt(x -19.5, y -19.5, 2, tbl[0] *40, 0, 40 * tbl[1], 40 * tbl[2], 2)

    def drawCell2(self, x, y, deg):
        n = int((deg +360/32) * 16/360) & 15
        tbl = __class__.imageTable[n]
        pyxel.blt(x -19.5, y -19.5, 2, tbl[0] *40, 40, 40 * tbl[1], 40 * tbl[2], 2)

