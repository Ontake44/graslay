import pyxel
import math
import random
import gcommon
import enemy
import boss
import enemyShot
import enemyBattery
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
    def __init__(self, t):
        super(BossCave, self).__init__()
        self.x = 128
        self.y = -136
        self.layer = gcommon.C_LAYER_GRD
        self.left = -36
        self.top = -44
        self.right = 64
        self.bottom = 44
        self.hp = boss.BOSS_WAREHOUSE_HP
        self.score = 15000
        self.subState = 0
        self.subCnt = 0
        self.hitcolor1 = 12
        self.hitcolor2 = 6
        self.ground = False
        self.shotHitCheck = True	# 自機弾との当たり判定
        self.hitCheck = True	# 自機と敵との当たり判定
        self.enemyShotCollision = False	# 敵弾との当たり判定を行う
        self.countMover = enemy.CountMover(self, __class__.moveTable, False)

    def update(self):
        self.countMover.update()
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

    def draw(self):
        pyxel.blt(self.x, self.y, 2, 136, 0, 256-136, 136, 3)


    def broken(self):
        self.remove()
        enemy.removeEnemyShot()
        ObjMgr.objs.append(boss.BossExplosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
        GameSession.addScore(self.score)
        BGM.sound(gcommon.SOUND_LARGE_EXP)
        enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
        ObjMgr.objs.append(enemy.Delay(enemy.StageClear, [0,0,"2B"], 240))

