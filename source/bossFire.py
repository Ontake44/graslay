from typing import get_origin
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
from drawing import Drawing

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
        [540, CountMover.MOVE, 1.0, 0.0],
        [0, CountMover.SET_POS, 256 +32, 60],
        [0, CountMover.SET_DEG, 180]
    ]
    stateTable0 = [
        [920, 0],
        [1020, 3],
        [1140, 1],  # 待ち
        [1380, 2],  # 大量ブレス
        [1880, 3],
        [2000, 1],  # 待ち
        [2510, 2],  # 大量ブレス
        [9999, 0],
    ]
    backstateTable0 = [
        [1020, 0],
        [1140, 1],  # 待ち
        [1380, 2],  # 大量ブレス
        [1880, 3],
        [2000, 1],  # 待ち
        [2510, 2],  # 大量ブレス
        [9999, 0],
    ]
    intervaTable = (45, 30, 24)
    def __init__(self, t):
        super(__class__, self).__init__()
        self.isBossRush = t[2]
        self.x = 256 +32
        self.y = 60
        self.moveTable = __class__.moveTable0
        self.mover = CountMover(self, self.moveTable, True)
        self.mover.deg = 180
        self.stater = enemy.CountStater(self, __class__.stateTable0, True, True)
        self.stateTable = None
        self.left = -12
        self.top = -12
        self.right = 12
        self.bottom = 12
        self.hitcolor1 = 10
        self.hitcolor2 = 7
        self.layer = gcommon.C_LAYER_GRD
        self.exptype = gcommon.C_EXPTYPE_SKY_M
        self.ground = True
        self.hitCheck = True
        self.shotHitCheck = True
        self.hp = boss.BOSS_FIRE_HP
        self.score = 15000
        self.cellCount = 13
        self.cellDelay = 30
        self.cellList = []
        self.collisionRects = []
        for i in range(self.cellCount * self.cellDelay):
            self.cellList.append([self.x, self.y, self.mover.deg])
        pyxel.image(2).load(0,0,"assets/bossFire.png")
        self.fireInterval = __class__.intervaTable[GameSession.difficulty]
        self.timerObj = None
        if self.isBossRush:
            self.timerObj = enemy.Timer1.create(80)

    def fire(self, x, y, deg, speed):
        obj = enemyOthers.Fire2(x, y, deg)
        obj.imageSourceIndex = 2
        obj.imageSourceX = 64
        obj.imageSourceY = 64
        obj.speed = speed
        ObjMgr.addObj(obj)

    def fire2(self, x, y, deg, speed):
        obj = enemyOthers.Fire3(x, y, deg)
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
            if self.stater.cnt % self.fireInterval == 0:
                # 先頭部からの炎
                self.shotHead()

                if self.stater.cnt % (self.fireInterval*2) == 0:
                    self.shotMiddle()
                
                # 最後部からの炎
                self.shotTail()
        elif self.stater.state == 2:
            if self.stater.cnt % 8 == 0:
                # 先頭部からの炎
                self.shotHead()
        elif self.stater.state == 3:
            if self.stater.cnt % self.fireInterval == 0:
                # 先頭部からの炎
                self.shotHead2()

                if self.stater.cnt % 60 == 0:
                    self.shotMiddle()
                
                # 最後部からの炎
                self.shotTail()


    def shotHead(self):
        rad = math.radians(self.mover.deg)
        ox = self.x + math.cos(rad) * 20.0
        oy = self.y + math.sin(rad) * 20.0
        self.fire(ox, oy, math.fmod(self.mover.deg +20, 360), 3.0)
        self.fire(ox, oy, math.fmod(self.mover.deg -20, 360), 3.0)
        self.fire(ox, oy, self.mover.deg, 3.0)

    def shotHead2(self):
        rad = math.radians(self.mover.deg)
        ox = self.x + math.cos(rad) * 20.0
        oy = self.y + math.sin(rad) * 20.0
        self.fire2(ox, oy, math.fmod(self.mover.deg +20, 360), 3.0)
        self.fire2(ox, oy, math.fmod(self.mover.deg -20, 360), 3.0)
        self.fire2(ox, oy, self.mover.deg, 3.0)

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
        gcommon.Text2(200, 184, str(self.cnt), 7, 0)
        #gcommon.Text2(200, 184, str(int(self.x)) + " " + str(int(self.y)), 7, 0)

    def drawCell(self, x, y, deg):
        n = int((deg +360/32) * 16/360) & 15
        tbl = __class__.imageTable[n]
        pyxel.blt(x -31.5, y -31.5, 2, tbl[0] *64, tbl[1] *64, 64 * tbl[2], 64 * tbl[3], 3)

    def drawCell2(self, x, y, deg):
        n = int((deg +360/32) * 16/360) & 15
        tbl = __class__.imageTable[n]
        pyxel.blt(x -31.5, y -31.5, 2, tbl[0] *64, 128 +tbl[1] *64, 64 * tbl[2], 64 * tbl[3], 3)


    # 当たった場合の破壊処理
    # 破壊した場合True
    def doShotCollision(self, shot):
        if gcommon.check_collision(self, shot):
            self.hp -= shot.shotPower
            if self.hp <= 0:
                self.broken()
                return True
            if shot.effect and self.shotEffect:
                shot.doEffect(self.shotEffectSound)
            self.hit = True
            return False
        else:
            if shot.effect and self.shotEffect:
                shot.doEffect(self.shotEffectSound)
            self.hit = False
            return False

    # 破壊されたとき
    def broken(self):
        GameSession.addScore(self.score)
        
        enemy.create_explosion2(self.x+(self.right+self.left+1)/2, self.y+(self.bottom+self.top+1)/2, self.layer, self.exptype, self.expsound)
        self.remove()
        self.doExplosion()
        enemy.removeEnemyShot()
        if self.isBossRush:
            if self.timerObj != None:
                self.timerObj.stop()
                self.timerObj = None
            ObjMgr.objs.append(enemy.NextEvent([0, None, 120]))
        else:
            ObjMgr.objs.append(enemy.Delay(enemy.StageClear, None, 180))

    def doExplosion(self):
        index = 0
        for i in range(self.cellCount):
            ObjMgr.addObj(BossFireExplosion(self.cellList[index][0], self.cellList[index][1], False))
            index += self.cellDelay

class BossFireExplosion(enemy.EnemyBase):
    def __init__(self, x, y, head):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.head = head
        self.layer = gcommon.C_LAYER_SKY
        self.hitCheck = False
        self.shotHitCheck = False
        self.enemyShotCollision = False
        #rad = math.radians(random.randrange(360))
        rad = math.atan2(100 - y, 128 -x)
        self.dx = math.cos(rad) * 4
        self.dy = math.sin(rad) * 4
        self.index = 0
        self.life = 20 + random.randrange(30)

    def update(self):
        if self.cnt > self.life:
            enemy.create_explosion2(self.x, self.y, gcommon.C_LAYER_SKY, gcommon.C_EXPTYPE_SKY_M, -1)
            self.remove()
            return
        self.x += self.dx
        self.y += self.dy
        self.index = (self.index + 1) & 15

    def draw(self):
        sy = 0 if self.head else 128
        tbl = BossFire.imageTable[self.index]
        pyxel.blt(self.x -31.5, self.y -31.5, 2, tbl[0] *64, sy +tbl[1] *64, 64 * tbl[2], 64 * tbl[3], 3)

class BossFireProminence(enemy.EnemyBase):
    def __init__(self):
        super(__class__, self).__init__()
        self.layer = gcommon.C_LAYER_GRD
        self.hitCheck = False
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.shiftList = []
        for i in range(32):
            n = int(5* math.sin(i * math.pi/16))
            self.shiftList.append(n)
        self.offsetY = 7 * 8

    def update(self):
        if self.state == 0:
            self.offsetY = math.pow(1 - (self.cnt/90.0), 3) * 56
            if self.cnt >= 90:
                self.nextState()
        elif self.state == 1:
            pass
        elif self.state == 2:
            self.offsetY = math.pow(self.cnt/90.0, 3) * 56
            if self.offsetY >= 90:
                self.remove()

    def draw(self):
        tm = 2
        m = ((self.cnt>>3) % 3) * 7
        mx = int(gcommon.map_x) & 127
        Drawing.bltm(-1 * (mx % 8), 0, tm, int(mx/8), m,33, 7, 3)
        count = 7 *8
        y = 0
        while( count > 0 ):
            #pyxel.blt(0, y -1, 4, 8 + self.shiftList[(int(self.cnt>>3)) & 31], y, 256, 1)
            offset = 8 + self.shiftList[(y +int(self.cnt>>2)) & 31]
            pyxel.blt(0, 192- 7*8 + y +self.offsetY, pyxel.screen, offset, y, 256, 1)
            pyxel.blt(256 -offset, 192- 7*8 + y +self.offsetY, pyxel.screen, 0, y, offset, 1)
            count -=1
            y += 1
        pyxel.blt(0, 0, pyxel.screen, 0, 192 -7*8, 256, -7*8)
