import pyxel
import math
import random
import gcommon
import enemy
import boss
import enemyShot
import enemyBattery
import enemyCreature
import drawing
from objMgr import ObjMgr
from gameSession import GameSession
from audio import BGM


class BossCave(enemy.EnemyBase):
    moveTable = [
        [1, 0, 0.0, 1.0],       # 0
        [60, 2, 0.0, 0.05],     # 1
        [60, 4, 0.0, 0.95],     # 2
        [30, 2, 0.0, -0.025],   # 3
        [40, 4, 0.0, 0.95],
        [120, 0, -0.250, 0.0],
    ]
    moveTable2 = [
        [60, 0, 0.0, 0.125],
        [60, 0, 0.0, -0.125],
    ]
    moveTable2x = [
        [0, 5, 20.0, -9999, -0.125],
        [0, 5, 140.0, -9999, 0.125],
    ]
    # x, y, width, height
    boubleTable = [
        [14, 87, 10, 0],
        [44, 105, 10, 0],
        [73, 114, 10, 0],
        [99, 83, 10, 0],
        [19, 64, 10, 0],
        [96, 132, 10, 0],
    ]
    laserPointTable = [
        [64, 42],
        [77, 51],
        [80, 65],
        [73, 78],
        [60, 83],
        [45, 76],
        [40, 60],
        [49, 46]
    ]
    laserIntervalTable = (240, 200, 180)
    def __init__(self, t):
        super(BossCave, self).__init__()
        self.x = 128
        self.y = (188 -128) * 8 - gcommon.map_y
        self.layer = gcommon.C_LAYER_GRD
        self.collisionRects = gcommon.Rect.createFromList([
            [16, 40, 31, 63], [32, 32, 87, 103], [88, 24, 109, 80], [40, 16, 87, 31], [90, 6, 103, 23], [54, 104, 101, 114], [80, 115, 105, 124]
        ])
        self.hp = boss.BOSS_CAVE_HP
        self.score = 15000
        self.subState = 0
        self.subCnt = 0
        self.hitcolor1 = 0
        self.hitcolor2 = 0
        self.ground = False
        self.shotHitCheck = True	# 自機弾との当たり判定
        self.hitCheck = True	# 自機と敵との当たり判定
        self.enemyShotCollision = False	# 敵弾との当たり判定を行う
        self.countMover = enemy.CountMover(self, __class__.moveTable, False)
        self.countMover2 = None
        self.worm4List = []
        self.bat1List = []
        self.random = gcommon.ClassicRand()
        self.laserInterval = __class__.laserIntervalTable[GameSession.difficulty]
        self.attackState = 0
        self.attackCnt = 0

    def update(self):
        if self.state < 100:
            self.countMover.update()
            if self.countMover2 != None:
                self.countMover2.update()
            if self.state == 0:
                # 出現
                if self.countMover.tableIndex == 2 and self.cnt % 4 == 0 and self.countMover.cnt < 40:
                    wy = gcommon.waterSurface_y - gcommon.map_y
                    for i in range(10):
                        enemy.WaterSplash.appendDr(self.x +20 + i*8, wy, gcommon.C_LAYER_SKY, math.pi * (1.2 + i*0.6/10), math.pi/6, 30)
                    
                    for t in __class__.boubleTable:
                        y = self.y + t[1]
                        if wy < y:
                            rx = 0
                            if t[2] > 0:
                                rx = random.randrange(-t[2], t[2])
                            ry = 0
                            if t[3] > 0:
                                ry = random.randrange(-t[3], t[3])
                            enemy.Splash.appendDr3(self.x +t[0] + rx, y + ry,
                                gcommon.C_LAYER_SKY, math.pi * 1.5, math.pi/6, 1.0, 50, 100, 20)
                elif self.countMover.isEnd:
                    self.countMover = enemy.CountMover(self, __class__.moveTable2, True)
                    self.countMover2 = enemy.CountMover(self, __class__.moveTable2x, True)
                    self.setState(1)
            elif self.state == 1:
                # 攻撃中
                if self.attackState == 0:
                    # 向きを変えるレーザー
                    self.attack0()
                elif self.attackState == 1:
                    # 待ち
                    self.attackCnt += 1
                    if self.attackCnt > 240:
                        self.attackCnt = 0
                        self.attackState += 1
                elif self.attackState == 2:
                    # ８方位レーザー
                    self.attack1()
                elif self.attackState == 3:
                    # 待ち
                    self.attackCnt += 1
                    if self.attackCnt > 60:
                        self.attackCnt = 0
                        self.attackState = 0

                if self.cnt % 200 == 0:
                    # 水中の蟲
                    self.worm4List = gcommon.getShrinkList(self.worm4List)
                    if len(self.worm4List) < 5:
                        dx = 1.0 if self.cnt % 400 == 0 else -1.0
                        dy = 0.20 if self.cnt % 800 == 0 else -0.25
                        obj = enemyCreature.Worm4(self.x + 8*6, self.y + 112, dx, dy)
                        self.worm4List.append(obj)
                        ObjMgr.addObj(obj)
                c = self.cnt % 320
                if c % 20 == 0 and c < 80:
                    # 蝙蝠みたいなやつ
                    self.bat1List = gcommon.getShrinkList(self.bat1List)
                    if len(self.bat1List) < 6:
                        dx = (self.random.rand() % 10 -5)/5.0
                        dy = -4.0
                        obj = enemyCreature.Worm5(self, self.x + 8*6, self.y + 15, dx, dy)
                        self.bat1List.append(obj)
                        ObjMgr.addObj(obj)
        elif self.state >= 100:
            self.updateBroken()

    def appendBat(self, obj):
        self.bat1List.append(obj)

    # 向きを変えるレーザー
    def attack0(self):
        if self.attackCnt % 180 == 0:
            # レーザー
            omega = math.pi/4 if self.cnt % 360 == 0 else -math.pi/4
            for i, pt in enumerate(__class__.laserPointTable):
                ObjMgr.addObj(boss.ChangeDirectionLaser1(self.x + pt[0], self.y + pt[1], -math.pi/2 - math.pi/16 + math.pi/4 * i, omega))
        self.attackCnt +=1
        if self.attackCnt >= 180:
            self.attackCnt = 0
            self.attackState += 1

    def attack1(self):
        if self.attackCnt % 10 == 0:
            n = int(self.attackCnt /10)
            pt = __class__.laserPointTable[n]
            ObjMgr.addObj(boss.DelayedShotLaser1(self.x + pt[0], self.y + pt[1], -math.pi/2 + math.pi/4 * n + math.pi/16))
            ObjMgr.addObj(boss.DelayedShotLaser1(self.x + pt[0], self.y + pt[1], -math.pi/2 + math.pi/4 * n - math.pi/16))
        self.attackCnt +=1
        if self.attackCnt > 10 * 7:
            self.attackCnt = 0
            self.attackState += 1

    def updateBroken(self):
        if self.state == 100:
            self.y += 0.25
            if self.cnt % 10 == 0:
                angle = math.pi *2 * random.randrange(0, 30)/30
                r = random.randrange(20, 60)
                cx = self.x + 59 + math.cos(angle) * r
                cy = self.y + 64 + math.sin(angle) * r
                enemy.create_explosion2(cx, cy, self.layer, gcommon.C_EXPTYPE_GRD_M, -1)
            if self.cnt > 60:
                self.nextState()
        elif self.state == 101:
            self.y += 0.125

    
    def draw(self):
        if self.state < 100:
            pyxel.blt(self.x, self.y, 2, 136, 0, 256-136, 136, 3)
            c = self.cnt % 200
            if c >= 180 and c <= 190:
                pyxel.blt(self.x + 6*8, self.y +96, 2, 224, 136, 32, 32, 3)
            if c > 190:
                pyxel.blt(self.x + 6*8, self.y +96, 2, 192, 136, 32, 32, 3)
            if self.hit:
                pyxel.blt(self.x +32, self.y +40, 2, 136, 136, 56, 48)
            n = (self.cnt>>4) & 3
            pyxel.blt(self.x +80, self.y +8, 2, 96 +n*40, 184, 40, 24, 3)
        elif self.state == 100:
            pyxel.blt(self.x, self.y, 2, 136, 0, 256-136, 136, 3)
        else:
            ox = self.cnt>>5
            if self.cnt & 1 == 0:
                for i in range(136):
                    if i & 1:
                        pyxel.blt(self.x +ox , self.y +i, 2, 136, i, 256-136, 1, 3)
                    else:
                        pyxel.blt(self.x -ox, self.y +i, 2, 136, i, 256-136, 1, 3)
            else:
                for i in range(136):
                    if i & 1:
                        pyxel.blt(self.x -ox , self.y +i, 2, 136, i, 256-136, 1, 3)
                    else:
                        pyxel.blt(self.x +ox, self.y +i, 2, 136, i, 256-136, 1, 3)

    def broken(self):
        gcommon.breakObjects(self.bat1List)
        gcommon.breakObjects(self.worm4List)
        self.setState(100)
        self.shotHitCheck = False
        self.hitCheck = False
        enemy.removeEnemyShot()
        GameSession.addScore(self.score)
        BGM.sound(gcommon.SOUND_LARGE_EXP)
        enemy.Splash.append(self.x + 59,  self.y + 64, gcommon.C_LAYER_EXP_SKY)
        ObjMgr.objs.append(enemy.Delay(enemy.StageClear, None, 200))

