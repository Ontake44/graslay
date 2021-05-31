import pyxel
import math
import random
import gcommon
import enemy
import boss
from objMgr import ObjMgr
from gameSession import GameSession
from audio import BGM
from enemy import CountMover
import enemyOthers

class BossFire(enemy.EnemyBase):
    # x, y, dx, dy
    imageTable = [
        [0, 0, 1, 1], [1, 0, 1, 1], [2, 0, 1, 1], [3, 0, 1, 1],
        [0, 1, 1, 1], [3, 0, -1, 1], [2, 0, -1, 1], [1, 0, -1, 1],
        [0, 0, -1, 1], [1, 0, -1, -1], [2, 0, -1, -1], [3, 0, -1, -1],
        [0, 1, 1, -1], [3, 0, 1, -1], [2, 0, 1, -1], [1, 0, 1, -1]
    ]
    moveTable0 = [
        [60, CountMover.MOVE, -1.0, 0.0],
        [90, CountMover.ROTATE_DEG2, -1.0, 1.0],
        [180, CountMover.ROTATE_DEG2, 1.0, 1.0],
        [240, CountMover.MOVE, 0.0, -1.0],      # 上に出ていく
        [90, CountMover.ROTATE_DEG2, 1.0, 1.0],
        [60, CountMover.MOVE, 1.0, 0.0],
        [90, CountMover.ROTATE_DEG2, 1.0, 1.0] ,
        [240, CountMover.MOVE, 0.0, 1.0],       # 上から出現
        [180, CountMover.ROTATE_DEG2, 1.0, 1.0] ,
        [90, CountMover.ROTATE_DEG2, -1.0, 1.0] ,
        [120, CountMover.MOVE, -1.0, 0.0],
        [180, CountMover.ROTATE_DEG2, -1.0, 1.0] ,
        [240, CountMover.MOVE, 1.0, 0.0],
        [270, CountMover.ROTATE_DEG2, -1.0, 1.0] ,
        [30, CountMover.MOVE, 0.0, 1.0],
        [270, CountMover.ROTATE_DEG2, 1.0, 1.0] ,
        [510, CountMover.MOVE, 1.0, 0.0],
        [0, CountMover.SET_POS, 256 +32, 60],
        [0, CountMover.SET_DEG, 180]
    ]
    stateTable0 = [
        [1020, 0],
        [1140, 1],
        [1380, 2],  # 大量ブレス
        [1880, 0],
        [2000, 1],
        [2480, 2],  # 大量ブレス
        [9999, 0],
    ]
    def __init__(self, t):
        super(__class__, self).__init__()
        self.x = 256 +32
        self.y = 60
        self.moveTable = __class__.moveTable0
        self.mover = CountMover(self, self.moveTable, True)
        self.mover.deg = 180
        self.stater = enemy.CountStater(self, __class__.stateTable0, True, True)
        self.stateTable = None
        self.layer = gcommon.C_LAYER_GRD
        self.ground = True
        self.hitCheck = True
        self.shotHitCheck = True
        self.hp = gcommon.HP_UNBREAKABLE
        self.cellCount = 13
        self.cellDelay = 30
        self.cellList = []
        self.collisionRects = []
        for i in range(self.cellCount * self.cellDelay):
            self.cellList.append([self.x, self.y, self.mover.deg])
        pyxel.image(2).load(0,0,"assets/bossFire.png")


    def fire(self, x, y, deg, speed):
        obj = enemyOthers.Fire2(x, y, deg)
        obj.imageSourceIndex = 2
        obj.imageSourceX = 64
        obj.imageSourceY = 64
        obj.speed = speed
        ObjMgr.addObj(obj)

    def update(self):
        self.mover.update()
        if self.mover.isEnd:
            # 移動テーブル終わりで削除
            self.remove()
            return
        if self.mover.cycleFlag:
            # ループした瞬間に0に戻す
            self.cnt = 0
            self.stater.reset()
        self.stater.update()
        for c in self.cellList:
            c[0] -= gcommon.cur_scroll_x
        self.cellList.insert(0, [self.x, self.y, self.mover.deg])
        if len(self.cellList) > (self.cellCount *  self.cellDelay +1):
            self.cellList.pop()
        
        # 当たり判定設定
        self.collisionRects.clear()
        index = 0
        x = self.x
        y = self.y
        for i in range(self.cellCount):
            c = self.cellList[index]
            cx = c[0] -self.x
            cy = c[1] -self.y
            self.collisionRects.append(gcommon.Rect.create(cx -12, cy-12, cx+12, cy+12))

            # 
            if c[1] > 190 and c[1] < 193:
                x = c[0] + random.randrange(-20, 20)
                enemy.Splash.appendParam(x, c[1], gcommon.C_LAYER_SKY, math.pi*1.5, math.pi*0.2,
                    speed=5, lifeMin=50, lifeMax=100, count=20, ground=True, color=10)
            elif c[1] > 4 and c[1] < 10:
                x = c[0] + random.randrange(-20, 20)
                enemy.Splash.appendParam(x, c[1], gcommon.C_LAYER_SKY, math.pi*0.5, math.pi*0.2,
                    speed=5, lifeMin=50, lifeMax=100, count=20, ground=True, color=10)

            index += self.cellDelay

        if self.stater.state == 0:
            if self.stater.cnt % 30 == 0:
                # 先頭部からの炎
                self.shotHead()

                if self.stater.cnt % 60 == 0:
                    self.shotMiddle()
                
                # 最後部からの炎
                self.shotTail()
        elif self.stater.state == 2:
            if self.stater.cnt % 8 == 0:
                # 先頭部からの炎
                self.shotHead()

    def shotHead(self):
        rad = math.radians(self.mover.deg)
        ox = self.x + math.cos(rad) * 20.0
        oy = self.y + math.sin(rad) * 20.0
        self.fire(ox, oy, math.fmod(self.mover.deg +20, 360), 3.0)
        self.fire(ox, oy, math.fmod(self.mover.deg -20, 360), 3.0)
        self.fire(ox, oy, self.mover.deg, 3.0)

    def shotMiddle(self):
        index = self.cellDelay * 3
        for i in range(int(self.cellCount/3) -1):
            cell = self.cellList[index]
            n = int((int((cell[2] +360/32) * 16/360) & 15) * 360/16)
            self.fire(cell[0], cell[1], n +90, 1.5)
            self.fire(cell[0], cell[1], n -90, 1.5)
            index += self.cellDelay * 3

    def shotTail(self):
        index = (self.cellCount -1) * self.cellDelay
        cell = self.cellList[index]
        rad = math.radians(cell[2])
        ox = cell[0] - math.cos(rad) * 20.0
        oy = cell[1] - math.sin(rad) * 20.0
        self.fire(ox, oy, math.fmod(cell[2] +180 +20, 360), 1.5)
        self.fire(ox, oy, math.fmod(cell[2] +180 -20, 360), 1.5)

    def draw(self):
        length = self.cellCount
        index = 0
        drawList = []
        for i in range(length):
            if index == 0:
                drawList.append([0, index])
            elif i == length -1:
                drawList.append([1, index])
            else:
                drawList.insert(0, [2, index])
            index += self.cellDelay
        for item in drawList:
            index = item[1]
            if item[0] == 0:
                self.drawCell(self.cellList[index][0], self.cellList[index][1], self.cellList[index][2])
            elif item[0] == 1:  
                self.drawCell(self.cellList[index][0], self.cellList[index][1], self.cellList[index][2] +180)
            else:
                self.drawCell2(self.cellList[index][0], self.cellList[index][1], self.cellList[index][2])
                if index % (self.cellDelay * 3) == 0:
                    pyxel.blt(self.cellList[index][0] -11.5, self.cellList[index][1] -11.5, 2, 64, 88, 24, 24, 3)
        #gcommon.Text2(200, 184, str(self.cnt), 7, 0)
        gcommon.Text2(200, 184, str(int(self.x)) + " " + str(int(self.y)), 7, 0)

    def drawCell(self, x, y, deg):
        n = int((deg +360/32) * 16/360) & 15
        tbl = __class__.imageTable[n]
        pyxel.blt(x -31.5, y -31.5, 2, tbl[0] *64, tbl[1] *64, 64 * tbl[2], 64 * tbl[3], 3)

    def drawCell2(self, x, y, deg):
        n = int((deg +360/32) * 16/360) & 15
        tbl = __class__.imageTable[n]
        pyxel.blt(x -31.5, y -31.5, 2, tbl[0] *64, 128 +tbl[1] *64, 64 * tbl[2], 64 * tbl[3], 3)


