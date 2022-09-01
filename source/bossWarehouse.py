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
import enemyOthers
from drawing import Drawing

class BossWarehouse(enemy.EnemyBase):
    moveTable = [
        [0, 5, 150, 95.5, 0.5], 	# 0 前進
        [50, -1],					# 1 砲台射出
        [0, 5, 200, 95.5, 0.5], 	# 2 後ろに下がる
        [120, -1],					# 3 射撃
        [0, 5, 150, 95.5 -64, 0.5],	# 4 前方上
        [120, -1],					# 5 砲台射出
        [0, 5, 200, 95.5 -64, 0.5],	# 6 後方上
        [120, -1],					# 7 射撃
        [0, 5, 150, 95.5+64, 0.5],	# 8 前方下
        [120, -1],					# 9 砲台射出
        [0, 5, 200, 95.5+64, 0.5],	# 10 後方下
        [120, -1],					# 11 射撃
    ]
    pos4rads = [math.pi/5.0, -math.pi/5.0, math.pi -math.pi/5.0, math.pi +math.pi/5.0]
    shot4poss = [[-6, -16], [10, -16], [-6, 16], [10, 16]]
    sideShotIntervalTable = [8, 6, 5]
    crazyShotIntervalTable = [6, 5, 4]
    def __init__(self, t):
        super(BossWarehouse, self).__init__()
        self.isBossRush = t[2]
        self.x = 256 + 48
        self.y = 95.5	#95.5
        self.layer = gcommon.C_LAYER_GRD | gcommon.C_LAYER_SKY
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
        self.ground = True
        self.shotHitCheck = True	# 自機弾との当たり判定
        self.hitCheck = True	# 自機と敵との当たり判定
        self.enemyShotCollision = False	# 敵弾との当たり判定を行う
        self.countMover = enemy.CountMover(self, __class__.moveTable, True)
        self.gunRad = math.pi
        self.gun_cx = self.x + 20.0
        self.gun_cy = self.y
        self.wheelCnt = 0
        self.gunWidth = 56
        self.gunHeight = 56
        self.sideShotInterval = __class__.sideShotIntervalTable[GameSession.difficulty]
        self.crazyShotInterval = __class__.crazyShotIntervalTable[GameSession.difficulty]
        self.image = [None]* self.gunWidth
        self.work = [None]* self.gunHeight
        for y in range(self.gunWidth):
            self.image[y] = [0]*self.gunHeight
        img = pyxel.image(2)
        for y in range(self.gunWidth):
            for x in range(self.gunHeight):
                self.image[y][x] = img.pget(x +176, y +104)
        self.timerObj = None
        if self.isBossRush:
            self.timerObj = enemy.Timer1.create(35)

    def update(self):
        self.countMover.update()
        self.gun_cx = self.x + 20.0
        self.gun_cy = self.y
        self.subCnt += 1
        if abs(self.countMover.dx) > 0.025 or abs(self.countMover.dy) > 0.025:
            self.wheelCnt += 1
        if self.state == 0:
            if self.countMover.tableIndex in (2, 4, 6, 8, 10):
                self.gunRad = gcommon.getRadToShip(self.x, self.y, self.gunRad +math.pi, math.pi/60) - math.pi
            elif self.countMover.tableIndex in (1, 3, 5, 7, 9, 11):
                self.shotMainState()
            if self.countMover.tableIndex == 1:
                if self.countMover.cnt % 45 == 0:
                    ObjMgr.addObj(enemyBattery.MovableBattery1p(self.x -16, self.y, 30, [[100*8, 0, -1.0, 0.0]]))
            elif self.countMover.tableIndex == 5:
                if self.countMover.cnt % 45 == 0:
                    ObjMgr.addObj(enemyBattery.MovableBattery1p(self.x -16, self.y, 30, [[0, 5, 44, self.y, 1.0],[100*8, 0, 0.0, 1.0]]))
            elif self.countMover.tableIndex == 9:
                if self.countMover.cnt % 45 == 0:
                    ObjMgr.addObj(enemyBattery.MovableBattery1p(self.x -16, self.y, 30, [[0, 5, 44, self.y, 1.0],[100*8, 0, 0.0, -1.0]]))
            if self.hp < boss.BOSS_WAREHOUSE_HP/3:
                # 発狂モード
                self.state = 1
        elif self.state == 1:
            # 発狂モード
            if self.gunRad < 0.75 * math.pi:
                self.gunRad += 0.025* math.pi
            else:
                self.nextState()
        elif self.state == 2:
            if self.cnt % self.crazyShotInterval == 0:
                self.shotMain()
            self.gunRad -= 0.025* math.pi
            if self.gunRad < -0.75 * math.pi:
                self.nextState()
        elif self.state == 3:
            if self.cnt % self.crazyShotInterval == 0:
                self.shotMain()
            self.gunRad += 0.025* math.pi
            if self.gunRad > 0.75 * math.pi:
                self.setState(1)

    def draw(self):
        pass

    def drawLayer(self, layer):
        if (layer & gcommon.C_LAYER_GRD) != 0:
            # 車輪
            n = (self.wheelCnt>>1) & 3
            pyxel.blt(self.x -16 -16, gcommon.sint(self.y +36 -16), 2, 128 +n*32, 160, 32, 32, 0)
            pyxel.blt(self.x -16 -16, gcommon.sint(self.y -36 -16), 2, 128 +(3-n)*32, 160, 32, 32, 0)
            pyxel.blt(self.x +56 -16, gcommon.sint(self.y +36 -16), 2, 128 +n*32, 160, 32, 32, 0)
            pyxel.blt(self.x +56 -16, gcommon.sint(self.y -36 -16), 2, 128 +(3-n)*32, 160, 32, 32, 0)
            
            pyxel.blt(self.x -48, gcommon.sint(self.y -51.5), 2, 136, 0, 120, 104, 3)


        elif (layer & gcommon.C_LAYER_SKY) != 0:
            pyxel.blt(self.x -48 +24, gcommon.sint(self.y -51.5) +32, 2, 136, 104, 40, 40)

            drawing.Drawing.setRotateImage(200, 192, 2, self.work, self.image, -self.gunRad, 3)
            pyxel.blt(self.x + 20.0 -self.gunWidth/2, self.y -self.gunHeight/2, 2, 200, 192, self.gunWidth, self.gunHeight, 3)


    def broken(self):
        self.remove()
        enemy.removeEnemyShot()
        ObjMgr.objs.append(boss.BossExplosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
        GameSession.addScore(self.score)
        BGM.sound(gcommon.SOUND_LARGE_EXP)
        enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
        if self.isBossRush:
            if self.timerObj != None:
                self.timerObj.stop()
                self.timerObj = None
            ObjMgr.objs.append(enemy.NextEvent([0, None, 120]))
        else:
            ObjMgr.objs.append(enemy.Delay(enemy.StageClear, None, 240))

    def shotMainState(self):
        if self.countMover.cnt > 30 and self.countMover.cnt < 120 and self.countMover.cnt % 10 == 0:
            self.shotMain()
        if self.countMover.cnt >= 60 and self.countMover.cnt % self.sideShotInterval == 0:
            px = self.gun_cx - 8.0 * math.cos(self.gunRad)
            py = self.gun_cy - 8.0 * math.sin(self.gunRad)
            enemy.enemy_shot_rad(px, py, 3.5, 0, self.gunRad + math.pi  - ( 125 -self.countMover.cnt) * math.pi/180)
            enemy.enemy_shot_rad(px, py, 3.5, 0, self.gunRad + math.pi  + ( 125 -self.countMover.cnt) * math.pi/180)

    def shotMain(self):
        r = self.gunRad + math.pi
        px = self.gun_cx + math.cos(r + math.pi/20) * 30
        py = self.gun_cy + math.sin(r + math.pi/20) * 30
        enemy.enemy_shot_rad(px, py, 4.5, 1, r)
        px = self.gun_cx + math.cos(r + math.pi/20) * 25
        py = self.gun_cy + math.sin(r + math.pi/20) * 25
        enemyOthers.Spark1.create2(px, py, gcommon.C_LAYER_E_SHOT)
        px = self.gun_cx + math.cos(r - math.pi/20) * 30
        py = self.gun_cy + math.sin(r - math.pi/20) * 30
        enemy.enemy_shot_rad(px, py, 4.5, 1, r)
        px = self.gun_cx + math.cos(r - math.pi/20) * 25
        py = self.gun_cy + math.sin(r - math.pi/20) * 25
        enemyOthers.Spark1.create2(px, py, gcommon.C_LAYER_E_SHOT)
        BGM.sound(gcommon.SOUND_SHOT2)


    def shot4directions(self):
        for r in __class__.pos4rads:
            enemy.enemy_shot_rad(self.gun_cx + math.cos(self.gunRad + r) * 16, self.gun_cy + math.sin(self.gunRad +r) * 16, 3, 0, self.gunRad + r)

class BossWarehouseRail(enemy.EnemyBase):
    def __init__(self):
        super(__class__, self).__init__()
        self.layer = gcommon.C_LAYER_UNDER_GRD
        self.shotHitCheck = False		# 自機弾との当たり判定
        self.hitCheck = False			# 自機と敵との当たり判定
        self.enemyShotCollision = False	# 敵弾との当たり判定を行う

    def update(self):
        if self.state == 0:
            # 閉じる
            if self.cnt > 90:
                self.nextState()
        elif self.state == 1:
            pass
            # 閉じた状態
        elif self.state == 2:
            # 開く
            if self.cnt > 90:
                self.remove()

    def draw(self):
        if self.state == 0:
            if self.cnt <= 90:
                # 1 to 0
                x = math.pow(1 - (self.cnt/90.0), 3)
            else:
                x = 0
            Drawing.bltm(x * 256, -4 +200*x, 0, 40, 33, 32, 25, 3)
            Drawing.bltm(x * 256, -4 -200*x, 0, 80, 33, 32, 25, 3)
            Drawing.bltm(x * 256, -4, 0, 40, 1, 32, 25, 3)
            Drawing.bltm(0, -4 + 200*x, 0, 0, 33, 32, 25, 3)
        elif self.state == 1:
            Drawing.bltm(0, -4, 0, 0, 1, 32, 25, 3)
        elif self.state == 2:
            if self.cnt <= 90:
                # 0 to 1
                x = math.pow(self.cnt/90.0, 3)
            else:
                x = 1
            Drawing.bltm(x * 256, -4 +200*x, 0, 40, 33, 32, 25, 3)
            Drawing.bltm(x * 256, -4 -200*x, 0, 80, 33, 32, 25, 3)
            Drawing.bltm(x * 256, -4, 0, 40, 1, 32, 25, 3)
            Drawing.bltm(0, -4 + 200*x, 0, 0, 33, 32, 25, 3)

