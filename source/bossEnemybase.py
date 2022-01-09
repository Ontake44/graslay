
from enum import IntFlag
import pyxel
import math
import random
import gcommon
import enemy
import boss
import gameSession
from objMgr import ObjMgr
from gameSession import GameSession
from audio import BGM
from enemy import CountMover, DockArm, EnemyShot, Explosion, Splash
import enemyOthers
import enemyShot
import drawing
from drawing import Drawing

def drawCoreCommon(self):
    Drawing.setBrightnessWithoutBlack(self.coreBrightness)
    pyxel.blt(gcommon.sint(self.x) -7.5, gcommon.sint(self.y -55.5)+55.5 -7.5, 1, 88, 40, 16, 16, 3)
    if self.cnt & 3 == 0:
        if self.coreBrightState == 0:
            self.coreBrightness += 1
            if self.coreBrightness >= 4:
                self.coreBrightState = 1
        else:
            self.coreBrightness -= 1
            if self.coreBrightness <= -3:
                self.coreBrightState = 0
    pyxel.pal()

class BossEnemybase(enemy.EnemyBase):
    def __init__(self, t):
        super(__class__, self).__init__()
        self.isBossRush = t[2]
        pos = gcommon.mapPosToScreenPos(172+256, 187-128)
        self.x = 127.5
        self.y = 95.5
        self.hp = gcommon.HP_UNBREAKABLE
        self.layer = gcommon.C_LAYER_GRD | gcommon.C_LAYER_UNDER_GRD
        self.hitCheck = True
        self.shotHitCheck = True
        self.enemyShotCollision = False
        self.ground = True
        self.shotEffect = False
        self.bossBroken = False
        pyxel.image(2).load(0,0,"assets/stage_enemybase-3.png")

    def update(self):
        if self.state == 0:
            if self.cnt == 0:
                BGM.sound(gcommon.SOUND_CLOSING)
            elif self.cnt == 90:
                ObjMgr.addObj(BossEnemybaseBody(self, self.isBossRush))
                BGM.sound(gcommon.SOUND_CLOSED)
        else:
            if self.cnt == 90:
                self.remove()

    def drawLayer(self, layer):
        x = 0.0
        if self.state == 0:
            if self.cnt < 90:
                #x = 1.0 - math.sin(self.cnt*math.pi*0.5/90.0)
                x = math.pow(1 - (self.cnt/90.0), 3)
        else:
            if self.cnt < 90:
                #x = 1.0 - math.sin(self.cnt*math.pi*0.5/90.0)
                x = math.pow(self.cnt/90.0, 3)
            else:
                x = 1.0
        if layer == gcommon.C_LAYER_UNDER_GRD:
            pyxel.blt(self.x-127.5 -127.5*x, self.y -95.5, 2, 128, 96, 128, 96, 3)
            pyxel.blt(self.x-127.5 -127.5*x, self.y +0.5, 2, 128, 96, 128, -96, 3)
            pyxel.blt(self.x+0.5 +127.5*x, self.y -95.5, 2, 128, 96, -128, 96, 3)
            pyxel.blt(self.x+0.5 +127.5*x, self.y +0.5, 2, 128, 96, -128, -96, 3)

            pyxel.blt(self.x-127.5, self.y -95.5 -95.5*x, 2, 128, 0, 128, 96, 3)
            pyxel.blt(self.x+0.5, self.y -95.5 -95.5*x, 2, 128, 0, -128, 96, 3)
            pyxel.blt(self.x-127.5, self.y +0.5 +95.5*x, 2, 128, 0, 128, -96, 3)
            pyxel.blt(self.x+0.5, self.y +0.5 +95.5*x, 2, 128, 0, -128, -96, 3)
        else:
            pyxel.blt(self.x-127.5 -127.5*x, self.y -95.5 -95.5*x, 2, 0, 0, 128, 96, 3)
            pyxel.blt(self.x-127.5 -127.5*x, self.y +0.5 +95.5*x, 2, 0, 0, 128, -96, 3)
            pyxel.blt(self.x+0.5 +127.5*x, self.y -95.5 -95.5*x, 2, 0, 0, -128, 96, 3)
            pyxel.blt(self.x+0.5 +127.5*x, self.y +0.5 +95.5*x, 2, 0, 0, -128, -96, 3)

    def getEllipseCollision(self, px, py):
        x = px -127.5
        y = py -95.5
        a = x*x/(120*120) + y*y/(88*88)
        return a > 1.0

    # 自機弾と敵との当たり判定
    def checkShotCollision(self, shot):
        if self.cnt <= 90:
            return False
        else:
            y = gcommon.getCenterY(shot)
            if self.getEllipseCollision(shot.x +shot.left, y):
                return True
            elif self.getEllipseCollision(shot.x +shot.right, y):
                return True
            else:
                return False

    # 自機と敵との当たり判定
    def checkMyShipCollision(self):
        if self.cnt <= 90:
            return False
        else:
            pos = gcommon.getCenterPos(ObjMgr.myShip)
            return self.getEllipseCollision(pos[0], pos[1])

class BossEnemybaseBody(enemy.EnemyBase):
    moveTable0 = [
        [0, CountMover.MOVE_TO, 127.5+120, 95.5, 1],
    ]
    moveTable1 = [
        [60, CountMover.STOP],
        [40, CountMover.ANGLE_DEG, 1.0],
        [80, CountMover.ANGLE_DEG, -1.0],
        [60, CountMover.ANGLE_DEG, 1.0],
        [20, CountMover.ANGLE_DEG, -1.0],
        #[50, CountMover.ANGLE_DEG, 1.0],
    ]
    moveTable2 = [
        [120, CountMover.ANGLE_DEG, 1.0],
        [240, CountMover.ANGLE_DEG, -1.0],
        [120, CountMover.ANGLE_DEG, 1.0],
        #[50, CountMover.ANGLE_DEG, 1.0],
    ]
    moveTable3 = [
        [360, CountMover.ANGLE_DEG, -1.0],
    ]
    moveTable21 = [
        [240, CountMover.ANGLE_DEG, 1.0],
        [120, CountMover.ANGLE_DEG, -1.0],
        [120, CountMover.ANGLE_DEG, 1.0],
        [240, CountMover.ANGLE_DEG, -1.0],
    ]
    moveTable31 = [
        [40, CountMover.ANGLE_DEG, 0.5],
        [60, CountMover.STOP],
        [80, CountMover.ANGLE_DEG, -0.5],
        [60, CountMover.STOP],
        [80, CountMover.ANGLE_DEG, 0.5],
        [60, CountMover.STOP],
        [80, CountMover.ANGLE_DEG, -0.5],
        [60, CountMover.STOP],
        [80, CountMover.ANGLE_DEG, 0.5],
        [60, CountMover.STOP],
        [40, CountMover.ANGLE_DEG, -0.5],
        [0, CountMover.SET_DEG, 0.0],
    ]


    def __init__(self, parent, isBossRush):
        super(__class__, self).__init__()
        self.parent = parent
        self.isBossRush = isBossRush
        self.x = 256+64
        self.y = 95.5
        self.left = -15.5
        self.top = -15.5
        self.right = 15.5
        self.bottom = 15.5
        self.hp = boss.BOSS_ENEMYBASE_1
        self.score = 5000
        self.layer = gcommon.C_LAYER_UPPER_SKY
        self.exptype = gcommon.C_EXPTYPE_SKY_L
        self.hitCheck = True
        self.shotHitCheck = True
        self.enemyShotCollision = False
        self.hitcolor1 = 13
        self.hitcolor2 = 7
        self.ground = True
        self.gunWidth = 64
        self.gunHeight = 64
        self.image = [None]* self.gunWidth
        self.work = [None]* self.gunHeight
        for y in range(self.gunWidth):
            self.image[y] = [0]*self.gunHeight
        img = pyxel.image(2)
        for y in range(self.gunWidth):
            for x in range(self.gunHeight):
                self.image[y][x] = img.get(x +0, y +192)
        self.rad = 0.0
        self.mode = 0
        self.mover = None
        self.testRad = 0.0
        self.radSave = -9999.0
        self.batteryCount = 0
        self.batteryList = []
        self.gameTimerSave = gcommon.game_timer
        self.timerObj = None
        if self.isBossRush:
            self.timerObj = enemy.Timer1.create(60)

    def update(self):
        if self.mode == 0:
            self.update0()
        elif self.mode == 1:
           self.update1()
        elif self.mode == 2:
           self.update2()
        elif self.mode == 3:
            self.update3()
        if self.mode == 4:
            self.setMode(1)

    def update0(self):
        if self.state == 0:
            if self.cnt == 0:
                self.mover = CountMover(self, __class__.moveTable0, False, True)
            self.mover.update()
            if self.mover.isEnd:
                self.nextMode()

    def update1xxxx(self):
        if self.cnt % 30 == 0:
            rad = math.pi + random.randrange(-45,45) *math.pi /180
            ObjMgr.addObj(BossEnemybaseShot1(self.x, self.y, rad, 2))

    def update1(self):
        if gcommon.START_GAME_TIMER > self.gameTimerSave:
            self.broken()
            return
        if self.state == 0:
            if self.cnt == 0:
                self.mover = CountMover(self, __class__.moveTable1, False)
                ObjMgr.addObj(BossEnemybaseBeam1(self, -32.0, 0,beamTime=360))
            self.mover.update()
            self.rad = math.radians(self.mover.deg)
            if self.cnt % 30 == 0:
                self.shot1()
            if self.mover.isEnd:
                self.nextState()
        elif self.state == 1:
            if self.cnt == 0:
                self.mover = CountMover(self, __class__.moveTable2, False)
            self.mover.update()
            self.rad = math.radians(self.mover.deg)
            if self.cnt % 7 == 0:
                self.shot1()
            # if self.cnt % 40 == 0:
            #     self.rad = math.radians(self.mover.deg)
            #     if self.cnt % 80 == 0:
            #         self.shotSmall(7)
            #     else:
            #         self.shotSmall(8)
            if self.mover.isEnd:
                self.nextState()
        elif self.state == 2:
            if self.cnt == 0:
                self.mover = CountMover(self, __class__.moveTable2, False)
            self.mover.update()
            self.rad = math.radians(self.mover.deg)
            if self.cnt % 40 == 0:
                self.rad = math.radians(self.mover.deg)
                if GameSession.isEasy():
                    if self.cnt % 80 == 0:
                        self.shotSmall(3)
                    else:
                        self.shotSmall(4)
                elif GameSession.isHard():
                    if self.cnt % 80 == 0:
                        self.shotSmall(7)
                    else:
                        self.shotSmall(8)
                else:
                    if self.cnt % 80 == 0:
                        self.shotSmall(5)
                    else:
                        self.shotSmall(6)
            if self.mover.isEnd:
                self.nextMode()
                #self.setState(0)

        self.x = 127.5 + 120 * math.cos(self.rad)
        self.y = 95.5 + 88 * math.sin(self.rad)

    def update2(self):
        if self.state == 0:
            if self.cnt == 0:
                self.batteryCount = 0
            if self.cnt % 16 == 0:
                self.maxAngle = math.pi*150/180 - self.batteryCount * math.pi*16/180
                if self.maxAngle < math.pi*16/180:
                    self.nextState()
                else:
                    maxCount = int(120/16)
                    #ObjMgr.addObj(BossEnemybaseBattery1(0.0, self.maxAngle, int((maxCount - self.batteryCount)*16)))
                    self.batteryList.append(ObjMgr.addObj(BossEnemybaseBattery1(self, 0.0, self.maxAngle, 120)))
                    self.batteryList.append(ObjMgr.addObj(BossEnemybaseBattery1(self, 0.0, -self.maxAngle, 120)))
                    self.batteryCount += 1
                    #if self.batteryCount == maxCount:
                    #    self.nextState()
        elif self.state == 1:
            if self.cnt == 0:
                self.mover = CountMover(self, __class__.moveTable21, False)
            self.mover.update()
            self.rad = math.radians(self.mover.deg)
            if self.mover.isEnd:
                newList = []
                for obj in self.batteryList:
                    if obj.removeFlag == False:
                        newList.append(obj)
                        if obj.state != 3:
                            obj.setState(3)
                self.batteryList = newList
                if len(self.batteryList) == 0:
                    self.nextMode()

        self.x = 127.5 + 120 * math.cos(self.rad)
        self.y = 95.5 + 88 * math.sin(self.rad)

    def update3(self):
        if self.cnt == 0:
            self.mover = CountMover(self, __class__.moveTable31, False)
        self.mover.update()
        self.rad = math.radians(self.mover.deg)
        self.x = 127.5 + 120 * math.cos(self.rad)
        self.y = 95.5 + 88 * math.sin(self.rad)
        if self.cnt % 30 == 0:
            pos = gcommon.getAngle(-32, 0, self.rad)
            enemy.enemy_shot(self.x +pos[0], self.y +pos[1], 2, 0)
        if self.state == 0:
            if self.cnt % 70 == 0:
                if self.cnt % 140 == 0:
                    ObjMgr.addObj(BossEnemybaseBattery2(self, -1))
                else:
                    ObjMgr.addObj(BossEnemybaseBattery2(self, 1))
            if self.mover.isEnd:
                self.nextState()
        else:
            if self.cnt > 240:
                self.nextMode()

    def nextMode(self):
        self.mode += 1
        self.setState(0)
    
    def setMode(self, mode):
        self.mode = 0
        self.setState(0)

    def shot1(self):
        rad = math.pi + random.randrange(-45,45) *math.pi /180 + self.rad
        ObjMgr.addObj(BossEnemybaseShot1(self.x - math.cos(self.rad)*8, self.y- math.sin(self.rad)*8, rad, 2))

    def shotSmall(self, count):
        #enemy.enemy_shot_rad(self.x, self.y, 4, 0, self.rad + math.pi)
        for i in range(count):
            enemy.enemy_shot_rad(self.x - math.cos(self.rad)*8, self.y - math.sin(self.rad)*8, 3, 0, self.rad + math.pi + (i-(count-1)/2.0) * math.pi*15/180 )

    @classmethod
    def getVectorAngle(cls, a, b):
        return math.acos((a[0]*b[0] +a[1]*b[1])/(math.sqrt(a[0]*a[0] + a[1]*a[1])*math.sqrt(b[0]*b[0]+b[1]*b[1])))

    def draw(self):
        if self.radSave != self.rad:
            drawing.Drawing.setRotateImage(64, 192, 2, self.work, self.image, -self.rad, 3)
            self.radSave = self.rad
        if self.hit:
            pyxel.pal(self.hitcolor1, self.hitcolor2)
        pyxel.blt(gcommon.sint(self.x -31.5), gcommon.sint(self.y -31.5), 2, 64, 192, self.gunWidth, self.gunHeight, 3)
        pyxel.pal()
        #pyxel.line(127.5, 95.5, 127.5 + 200 * math.cos(self.rad), 95.5 + 200 * math.sin(self.rad), 7)

    def broken(self):
        self.remove()
        enemy.removeEnemyShot()
        ObjMgr.objs.append(boss.BossExplosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
        GameSession.addScore(self.score)
        BGM.sound(gcommon.SOUND_LARGE_EXP)
        enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
        self.parent.setState(1)
        ObjMgr.objs.append(enemy.Delay(BossEnemybaseBody2, [0, None, self.x, self.y, self.isBossRush], 90))
        gcommon.map_x = 524 * 8
        gcommon.map_y = 87 * 8
        if self.isBossRush:
            if self.timerObj != None:
                self.timerObj.stop()
                self.timerObj = None


# ビーーーーム！！！
class BossEnemybaseBeam1(enemy.EnemyBase):
    beamPoints = [[0,0],[5,-8],[300,-8],[300,8],[5,8]]
    # x,y 弾の中心を指定
    def __init__(self, parent, ox, oy, beamTime=90):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = parent.x + ox
        self.y = parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.beamTime = beamTime
        self.layer = gcommon.C_LAYER_UNDER_GRD | gcommon.C_LAYER_SKY | gcommon.C_LAYER_E_SHOT
        self.hitCheck = True
        self.shotHitCheck = False
        self.polygonList1 = []
        self.polygonList1.append(gcommon.Polygon(__class__.beamPoints, 10))
        self.xpolygonList1 = None
        self.xpolygonList2 = None
        self.xpolygonList3 = None
        self.size = 0.0
        self.rad = 0.0

    def update(self):
        self.rad = self.parent.rad
        if self.state == 0:
            self.size += 0.025
            if self.size > 1.0:
                self.size = 1.0
                self.nextState()
                #gcommon.debugPrint("to State1")
        elif self.state == 1:
            if self.cnt > self.beamTime:
                self.nextState()
                #gcommon.debugPrint("to State2")
        else:
            self.size -= 0.05
            if self.size < 0.05:
                self.remove()
                return

        pos = gcommon.getAngle(self.offsetX, self.offsetY, self.rad)
        self.x = self.parent.x + pos[0]
        self.y = self.parent.y + pos[1]
        self.xpolygonList1 = gcommon.getAnglePolygons2([self.x, self.y], self.polygonList1, [0,0], self.rad +math.pi, 1.0, self.size)
        self.xpolygonList2 = gcommon.getAnglePolygons2([self.x, self.y], self.polygonList1, [0,0], self.rad +math.pi, 1.0, self.size*0.8)
        self.xpolygonList3 = gcommon.getAnglePolygons2([self.x, self.y], self.polygonList1, [0,0], self.rad +math.pi, 1.0, self.size*0.5)
        # if gcommon.isMapFreePos(gcommon.getCenterX(self), gcommon.getCenterY(self)) == False:
        # 	self.removeFlag = True

    def drawLayer(self, layer):
        if layer == gcommon.C_LAYER_UNDER_GRD:
            if self.cnt & 2 == 0:
                self.xpolygonList1.polygons[0].clr = 9
                self.xpolygonList2.polygons[0].clr = 10
                self.xpolygonList3.polygons[0].clr = 7
            else:
                self.xpolygonList1.polygons[0].clr = 8
                self.xpolygonList2.polygons[0].clr = 9
                self.xpolygonList3.polygons[0].clr = 10
            Drawing.drawPolygons(self.xpolygonList1)
            Drawing.drawPolygons(self.xpolygonList2)
            Drawing.drawPolygons(self.xpolygonList3)
        # elif layer == gcommon.C_LAYER_SKY:
        #     n = random.randrange(4, 10)
        #     r = math.pi + self.rad
        #     #enemy.Explosion.drawExplosion(127.5 + 120 * math.cos(r), 95.5 + 88 * math.sin(r), 1, 1, n)
        #     pyxel.circ(127.5 + 120 * math.cos(r), 95.5 + 88 * math.sin(r), 20, 7)

    # 自機と敵との当たり判定
    def checkMyShipCollision(self):
        if self.state == 0:
            return False
        else:
            if self.xpolygonList1 == None:
                return False
            pos = gcommon.getCenterPos(ObjMgr.myShip)
            if gcommon.checkCollisionPointAndPolygon(pos, self.xpolygonList1.polygons[0].points):
                return True
            return False

# わっかショット
class BossEnemybaseShot1(enemy.EnemyBase):
    # x,y 弾の中心を指定
    def __init__(self, x, y, rad, speed):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.dx = speed * math.cos(rad)
        self.dy = speed * math.sin(rad)
        self.left = -6.5
        self.top = -6.5
        self.right = 6.5
        self.bottom = 6.5
        self.hp = 1
        self.layer = gcommon.C_LAYER_E_SHOT
        self.hitCheck = True
        self.shotHitCheck = True

    def update(self):
        if self.cnt > 240:
            self.remove()
            return
        self.x += self.dx
        self.y += self.dy
        x = self.x -127.5
        y = self.y -95.5
        a = (x*x)/(120*120) + (y*y)/(88*88)
        if a > 1.0:
            v = gcommon.getEllipseReflectionVector(127.5, 95.5, 120, 88, self.x, self.y, [self.dx, self.dy])
            self.dx = v[0]
            self.dy = v[1]

    def draw(self):
        pyxel.blt(gcommon.sint(self.x -7.5), gcommon.sint(self.y -7.5), 2, 128, 192, 16, 16, 3)

# 数珠繋ぎになって弾を打ってくる砲台
class BossEnemybaseBattery1(enemy.EnemyBase):
    def __init__(self, parent,  rad, angle, waitCnt):
        super(__class__, self).__init__()
        self.parent = parent
        self.rad = rad
        self.angle = angle
        self.waitCnt = waitCnt
        gcommon.debugPrint("wait:" +str(self.waitCnt))
        self.left = -6.5
        self.top = -6.5
        self.right = 6.5
        self.bottom = 6.5
        self.hp = 200
        self.score = 300
        self.layer = gcommon.C_LAYER_SKY | gcommon.C_LAYER_E_SHOT
        self.hitCheck = True
        self.shotHitCheck = True
        self.hitcolor1 = 5
        self.hitcolor2 = 7
        if self.angle > 0:
            self.omega = math.pi * 1.0/180
        else:
            self.omega = -math.pi * 1.0/180
        self.maxCnt = self.angle/self.omega
        self.shotCnt = 10 + random.randrange(int(self.waitCnt/2))
        self.isBroken = False
    
    def update(self):
        if self.state == 0:
            self.rad += self.omega
            if self.cnt >= self.maxCnt:
                self.nextState()
        elif self.state == 1:
            if self.isBroken == False and self.cnt == self.shotCnt:
                enemy.enemy_shot(self.x, self.y, 2, 0)
            if self.cnt >= 150:
                self.nextState()
            # if self.cnt >= self.waitCnt:
            #     self.omega = -self.omega
            #     self.nextState()
        elif self.state == 2:
            if self.cnt >= 150:
                self.setState(1)
        elif self.state == 3:
            self.rad -= self.omega
            if self.cnt >= self.maxCnt:
                self.remove()

        self.x = 127.5 + 120 * math.cos(self.parent.rad + self.rad)
        self.y = 95.5 + 88 * math.sin(self.parent.rad + self.rad)

    def broken(self):
        if self.isBroken == False:
            gameSession.GameSession.addScore(self.score)
            enemy.create_explosion2(self.x+(self.right+self.left+1)/2, self.y+(self.bottom+self.top+1)/2, self.layer, self.exptype, self.expsound)
            self.isBroken = True
            self.hp = gcommon.HP_NODAMAGE

    def drawLayer(self, layer):
        if layer == gcommon.C_LAYER_SKY:
            if self.isBroken:
                pyxel.blt(gcommon.sint(self.x -11.5), gcommon.sint(self.y -11.5), 2, 152, 208, 24, 24, 3)
            else:
                pyxel.blt(gcommon.sint(self.x -11.5), gcommon.sint(self.y -11.5), 2, 128, 208, 24, 24, 3)

# オレンジアイスバー？ビームを放つ砲台
class BossEnemybaseBattery2(enemy.EnemyBase):
    beamPoints = [[0,0],[5,-4],[100,-4],[105, 0], [100,4],[5,4]]
    def __init__(self, parent, direction):
        super(__class__, self).__init__()
        self.parent = parent
        self.rad = parent.rad
        self.left = -6.5
        self.top = -6.5
        self.right = 6.5
        self.bottom = 6.5
        self.hp = 200
        self.score = 300
        self.layer = gcommon.C_LAYER_SKY | gcommon.C_LAYER_E_SHOT
        self.hitCheck = True
        self.shotHitCheck = True
        if direction == 1:
            self.omega = math.pi * 1.0/180
        else:
            self.omega = -math.pi * 1.0/180
        self.isBroken = False
        self.beamLength = 0
        self.polygonList1 = []
        self.polygonList1.append(gcommon.Polygon(__class__.beamPoints, 10))
        self.xpolygonList1 = None
        self.xpolygonList2 = None
        self.size = 1.0
        self.additionRad = 0.0

    def update(self):
        self.rad += self.omega
        self.additionRad += self.omega
        if math.fabs(self.additionRad) > math.pi:
            rr = gcommon.radNormalizeX(self.rad -self.parent.rad)
            if self.omega > 0.0 and rr < math.pi*3/180:
                self.remove()
                return
            elif self.omega < 0.0 and rr < math.pi*3/180:
                self.remove()
                return

        self.x = 127.5 + 120 * math.cos(self.rad)
        self.y = 95.5 + 88 * math.sin(self.rad)
        if self.state == 0:
            self.beamLength += 0.01
            if self.beamLength >= 1.0:
                self.nextState()
        else:
            self.beamLength -= 0.01
            if self.beamLength <= 0.0:
                self.beamLength = 0.0
                self.setState(0)
        self.xpolygonList1 = gcommon.getAnglePolygons2([self.x, self.y], self.polygonList1, [0,0], self.rad +math.pi, self.beamLength, self.size)
        self.xpolygonList2 = gcommon.getAnglePolygons2([self.x, self.y], self.polygonList1, [0,0], self.rad +math.pi, self.beamLength, self.size*0.8)

    def drawLayer(self, layer):
        if layer == gcommon.C_LAYER_SKY:
            if self.isBroken:
                pyxel.blt(gcommon.sint(self.x -11.5), gcommon.sint(self.y -11.5), 2, 152, 208, 24, 24, 3)
            else:
                pyxel.blt(gcommon.sint(self.x -11.5), gcommon.sint(self.y -11.5), 2, 128, 208, 24, 24, 3)
            #pyxel.line(self.x, self.y, self.x + self.beamLength * math.cos(self.rad +math.pi), self.y + self.beamLength * math.sin(self.rad + math.pi), 7)
            if self.cnt & 2 == 0:
                self.xpolygonList1.polygons[0].clr = 9
                self.xpolygonList2.polygons[0].clr = 10
            else:
                self.xpolygonList1.polygons[0].clr = 8
                self.xpolygonList2.polygons[0].clr = 9
            Drawing.drawPolygons(self.xpolygonList1)
            Drawing.drawPolygons(self.xpolygonList2)

    # 自機と敵との当たり判定
    def checkMyShipCollision(self):
        if self.xpolygonList1 == None:
            return False
        pos = gcommon.getCenterPos(ObjMgr.myShip)
        if gcommon.checkCollisionPointAndPolygon(pos, self.xpolygonList1.polygons[0].points):
            return True
        return False

# 第２形態（下方向スクロール）
class BossEnemybaseBody2(enemy.EnemyBase):
    moveTable0 = [
        [0, CountMover.MOVE_TO, 127.5+64, 95.5, 1],
    ]
    moveTable10 = [
        [0, CountMover.MOVE_TO, 127.5+64, 30, 1],
        [60, CountMover.STOP],
        [0, CountMover.MOVE_TO, 127.5+64, 160, 1],
        [60, CountMover.STOP],
        [0, CountMover.MOVE_TO, 127.5+64, 30, 1],
        [60, CountMover.STOP],
        [0, CountMover.MOVE_TO, 127.5+64, 160, 1],
        [60, CountMover.STOP],
        [0, CountMover.MOVE_TO, 127.5+64, 30, 1],
        [60, CountMover.STOP],
        [0, CountMover.MOVE_TO, 127.5+64, 160, 1],
        [60, CountMover.STOP],
        [0, CountMover.MOVE_TO, 127.5+64, 12, 1],
        [60, CountMover.STOP],
        [0, CountMover.MOVE_TO, 127.5+96, 12, 1],
        [60, CountMover.STOP],
    ]
    moveTable20 = [
        [0, CountMover.MOVE_TO, 127.5+96, 184, 1],
        [0, CountMover.MOVE_TO, 127.5+96, 12, 1],
        [0, CountMover.MOVE_TO, 127.5+96, 184, 1],
        [0, CountMover.MOVE_TO, 127.5+96, 12, 1],
    ]
    def __init__(self, t):
        super(__class__, self).__init__()
        self.x = t[2]
        self.y = t[3]
        self.isBossRush = t[4]
        self.left = -6
        self.top = -6
        self.right = 6
        self.bottom = 6
        self.hp = gcommon.HP_UNBREAKABLE
        self.score = 5000
        self.layer = gcommon.C_LAYER_GRD
        self.hitCheck = True
        self.shotHitCheck = True
        self.enemyShotCollision = False
        self.hitcolor1 = 13
        self.hitcolor2 = 7
        self.mover = CountMover(self, __class__.moveTable0, False, True)
        self.coreBrightState = 0
        self.coreBrightness = 0
        self.mode = 0
        self.omega = 0.0
        self.rad = 0.0
        self.beamObj = None
        self.beamDirection = 1  # 1 or -1
        self.beamChargeCnt = 0
        self.radSave = -9999.0
        self.gunWidth = 32
        self.gunHeight = 32
        self.image = [None]* self.gunWidth
        self.work = [None]* self.gunHeight
        for y in range(self.gunWidth):
            self.image[y] = [0]*self.gunHeight
        img = pyxel.image(2)
        for y in range(self.gunWidth):
            for x in range(self.gunHeight):
                self.image[y][x] = img.get(x +0, y +96)
        self.timerObj = None
        if self.isBossRush:
            self.timerObj = enemy.Timer1.create(45)

    def update(self):
        if self.mode == 0:
            self.update0()
        elif self.mode == 1:
            self.update1()
        else:
            self.update2()

    #def setScrollLoop(self):
    #    if gcommon.map_y <= 4*8:
    #        gcommon.map_y += 32*8

    def update0(self):
        if self.state == 0:
            # 指定位置まで移動
            self.mover.update()
            if self.mover.isEnd:
                self.nextState()
        elif self.state == 1:
            # 合体
            if self.cnt == 90:
                #gcommon.setScroll(0.0, -0.5)
                gcommon.scrollController.nextIndex()
                self.nextState()
                BGM.sound(gcommon.SOUND_COMBINE)
        elif self.state == 2:
            # 合体後のピカーン
            if self.cnt == 60:
                self.nextMode()

    def update1(self):
        if self.cnt == 0:
            self.left = -15.5
            self.top = -15.5
            self.right = 15.5
            self.bottom = 15.5
            self.mover = CountMover(self, __class__.moveTable10, False, True)
        self.mover.update()
        self.rad += self.omega
        if self.beamObj != None and self.beamObj.removeFlag == False:
            if self.omega > 0 and self.rad > math.pi*1.6:
                self.beamObj.remove()
                return
            elif self.omega < 0 and self.rad < math.pi*0.4:
                self.beamObj.remove()
                return
        if self.cnt % 30 == 0:
            if self.beamObj == None or self.beamObj.removeFlag:
                if self.beamDirection == 1:
                    self.rad = math.pi*0.4
                    self.omega = math.pi*0.7/180
                    self.beamDirection = -1
                else:
                    self.rad = math.pi*1.6
                    self.omega = -math.pi*0.7/180
                    self.beamDirection = 1
                self.beamObj = ObjMgr.addObj(BossEnemybaseBeam2(self, 14, 0, self.beamDirection * math.pi*0.7/180))
            #ObjMgr.addObj(BossEnemybaseBeam2(self, -10, 0, -math.pi/180))
        #self.setScrollLoop()
        if self.cnt % 60 == 0:
            self.shotMulti()
        if self.mover.isEnd:
            self.nextMode()
            self.frameCount = 0
            if self.beamObj != None and self.beamObj.removeFlag == False:
                self.beamObj.endBeam()

    # 横スクロールになってから
    def update2(self):
        if self.state == 0:
            # 下方向に移動
            if self.cnt == 0:
                self.ground = True
                self.hp = boss.BOSS_ENEMYBASE_2
            if gcommon.isMapFreePos(self.x, self.y +10) == False:
                self.nextState()
            else:
                self.y += 1
            self.horizonBeam()
        elif self.state == 1:
            if gcommon.isMapFreePos(self.x +20, self.y) == False or self.x>gcommon.SCREEN_MAX_X:
                self.nextState()
            else:
                self.x += 1.25
        elif self.state == 2:
            # 上方向に移動
            if gcommon.isMapFreePos(self.x, self.y -10) == False or self.y +10 >gcommon.SCREEN_MAX_Y:
                self.nextState()
            else:
                self.y -= 1
            self.horizonBeam()
        elif self.state == 3:
            if gcommon.isMapFreePos(self.x +20, self.y) == False or self.x>gcommon.SCREEN_MAX_X:
                self.setState(0)
            else:
                self.x += 1.25
        if self.frameCount % 60 == 0:
            self.shotMulti()
        if self.frameCount > 20*60:
            self.broken()

    def shotMulti(self):
        if GameSession.isEasy():
            enemy.enemy_shot_dr_multi(self.x -10, self.y, 2, 0, 32, 3, 3)
        elif GameSession.isHard():
            enemy.enemy_shot_dr_multi(self.x -10, self.y, 2, 0, 32, 7, 3)
        else:
            enemy.enemy_shot_dr_multi(self.x -10, self.y, 2, 0, 32, 5, 3)

    def horizonBeam(self):
        if self.beamObj == None or self.beamObj.removeFlag:
            self.rad = math.pi
            self.beamChargeCnt += 1
            if self.beamChargeCnt > 120:
                self.beamObj = ObjMgr.addObj(BossEnemybaseBeam2(self, 14, 0, 0.0))
        else:
            self.beamChargeCnt = 0


    def nextMode(self):
        self.mode += 1
        self.setState(0)
    
    def setMode(self, mode):
        self.mode = 0
        self.setState(0)

    def draw(self):
        if self.mode == 0:
            drawCoreCommon(self)
            if self.state == 1:
                x = 0.0
                if self.cnt < 90:
                    #x = 1.0 - math.sin(self.cnt*math.pi*0.5/90.0)
                    x = math.pow(1 - (self.cnt/90.0), 3)
                pyxel.blt(gcommon.sint(self.x -31.5), gcommon.sint(self.y -31.5 -x * 100), 2, 0, 128, 64, 32, 3)
                pyxel.blt(gcommon.sint(self.x -31.5), gcommon.sint(self.y +0.5  +x * 100), 2, 0, 160, 64, 32, 3)
                pyxel.blt(gcommon.sint(self.x -15.5 +x*100), gcommon.sint(self.y -15.5), 2, 80, 144, 48, 32, 3)
                pyxel.blt(gcommon.sint(self.x -15.5 +x*100), gcommon.sint(self.y -15.5), 2, 0, 96, 32, 32, 3)
            elif self.state == 2:
                Drawing.setBrightnessWithoutBlack(5 + int(5 * math.sin(math.pi * self.cnt/60)))
                pyxel.blt(gcommon.sint(self.x -31.5), gcommon.sint(self.y -31.5), 2, 0, 128, 64, 64, 3)
                pyxel.blt(gcommon.sint(self.x -15.5), gcommon.sint(self.y -15.5), 2, 80, 144, 48, 32, 3)
                pyxel.blt(gcommon.sint(self.x -15.5), gcommon.sint(self.y -15.5), 2, 0, 96, 32, 32, 3)
                pyxel.pal()
            elif self.state == 3:
                pyxel.blt(gcommon.sint(self.x -31.5), gcommon.sint(self.y -31.5), 2, 0, 128, 64, 64, 3)
                pyxel.blt(gcommon.sint(self.x -15.5), gcommon.sint(self.y -15.5), 2, 80, 144, 48, 32, 3)
                pyxel.blt(gcommon.sint(self.x -15.5), gcommon.sint(self.y -15.5), 2, 0, 96, 32, 32, 3)
        else:
            drawCoreCommon(self)
            if self.radSave != self.rad:
                drawing.Drawing.setRotateImage(64, 192, 2, self.work, self.image, -self.rad +math.pi, 3)
                self.radSave = self.rad
            if self.hit:
                pyxel.pal(self.hitcolor1, self.hitcolor2)
            pyxel.blt(gcommon.sint(self.x -31.5), gcommon.sint(self.y -31.5), 2, 0, 128, 64, 64, 3)
            pyxel.blt(gcommon.sint(self.x -15.5), gcommon.sint(self.y -15.5), 2, 80, 144, 48, 32, 3)
            pyxel.blt(gcommon.sint(self.x -15.5), gcommon.sint(self.y -15.5), 2, 64, 192, self.gunWidth, self.gunHeight, 3)
            pyxel.pal()

    def broken(self):
        self.remove()
        enemy.removeEnemyShot()
        if self.beamObj != None and self.beamObj.removeFlag == False:
            self.beamObj.remove()
        ObjMgr.objs.append(boss.BossExplosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
        GameSession.addScore(self.score)
        BGM.sound(gcommon.SOUND_LARGE_EXP)
        enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
        gcommon.map_x = (512+152) * 8 + math.fmod(gcommon.map_x, 4*8)
        ObjMgr.objs.append(enemy.Delay(BossEnemybaseBody3, [0, None, self.x, self.y, self.isBossRush], 90))
        gcommon.scrollController.setIndex(21)
        BGM.play(BGM.BOSS_LAST)
        if self.isBossRush:
            if self.timerObj != None:
                self.timerObj.stop()
                self.timerObj = None

# ビーーーーム！！！
class BossEnemybaseBeam2(enemy.EnemyBase):
    # x,y 弾の中心を指定
    def __init__(self, parent, ox, oy, omega, beamTime=300):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = parent.x + ox
        self.y = parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.omega = omega
        self.beamTime = beamTime
        self.layer = gcommon.C_LAYER_SKY
        self.hitCheck = True
        self.shotHitCheck = False
        self.polygonList1 = []
        self.xpolygonList1 = None
        self.xpolygonList2 = None
        self.xpolygonList3 = None
        self.size = 0.0
        self.rad = math.pi
        self.headX = 0
        self.headY = 0
        self.beamPoints = [[0,0],[5,-4],[300,-4],[300,4],[5,4]]

    # 外部からビームを終了させたい場合
    def endBeam(self):
        if self.state == 1:
            self.nextState()

    def update(self):
        self.rad = self.parent.rad
        # if self.omega > 0 and self.rad > math.pi*1.6:
        #     self.remove()
        #     return
        # elif self.omega < 0 and self.rad < math.pi*0.4:
        #     self.remove()
        #     return

        if self.state == 0:
            # ビーム開始
            self.size += 0.02
            if self.size >= 1.0:
                self.nextState()
        elif self.state == 1:
            if self.cnt >= self.beamTime:
                self.nextState()
        else:
            # ビーム終了
            self.size -= 0.025
            if self.size <= 0.0:
                self.remove()
                return

        # 初期座標
        # pos = gcommon.getAngle(self.offsetX, self.offsetY, self.rad)
        # self.x = self.parent.x + pos[0]
        # self.y = self.parent.y + pos[1]
        # x = self.x
        # y = self.y
        # angle = self.rad
        # while(True):
        #     x += 8 * math.cos(self.rad)
        #     y += 8 * math.sin(self.rad)
        #     if gcommon.isMapFreePos(x, y) == False:
        #         enemy.Particle1.append(x, y, self.rad+math.pi, 4)
        #         break
        #     if x < -16 or x > gcommon.SCREEN_MAX_X +16 or y < -16 or y > gcommon.SCREEN_MAX_Y +16:
        #         break
        pos = gcommon.getAngle(self.offsetX, self.offsetY, self.rad)
        self.x = self.parent.x + pos[0]
        self.y = self.parent.y + pos[1]
        length1 = self.getBeamLength(-3.0)
        length2 = self.getBeamLength(3.0)
        length = length1 if length1 < length2 else length2
        pos = gcommon.getAngle(self.offsetX +length, self.offsetY, self.rad)
        # 先端
        self.headX = self.parent.x +pos[0]
        self.headY = self.parent.y +pos[1]
        if gcommon.inScreen(self.headX, self.headY):
            enemy.Particle1.append(self.headX, self.headY, self.rad+math.pi, 4)
        self.beamPoints[2][0] = length
        self.beamPoints[3][0] = length


        polygonList1 = []
        polygonList1.append(gcommon.Polygon(self.beamPoints, 10))
        self.xpolygonList1 = gcommon.getAnglePolygons2([self.x, self.y], polygonList1, [0, 0], self.rad, 1.0, 1.0*self.size)
        self.xpolygonList2 = gcommon.getAnglePolygons2([self.x, self.y], polygonList1, [0,0], self.rad, 1.0, 0.8*self.size)
        self.xpolygonList3 = gcommon.getAnglePolygons2([self.x, self.y], polygonList1, [0,0], self.rad, 1.0, 0.5*self.size)

    def getBeamLength(self, oy):
        pos = gcommon.getAngle(0.0, oy, self.rad)
        # 初期座標
        x = self.x + pos[0]
        y = self.y + pos[1]
        length = 0
        while(True):
            length += 8
            x += 8 * math.cos(self.rad)
            y += 8 * math.sin(self.rad)
            if gcommon.isMapFreePos(x, y) == False:
                #enemy.Particle1.append(x, y, self.rad+math.pi, 4)
                break
            if x < -16 or x > gcommon.SCREEN_MAX_X +16 or y < -16 or y > gcommon.SCREEN_MAX_Y +16:
                break
        return length

    def draw(self):
        #pyxel.line(self.x, self.y, self.headX, self.headY, 7)
        if self.cnt & 2 == 0:
            self.xpolygonList1.polygons[0].clr = 9
            self.xpolygonList2.polygons[0].clr = 10
            self.xpolygonList3.polygons[0].clr = 7
        else:
            self.xpolygonList1.polygons[0].clr = 8
            self.xpolygonList2.polygons[0].clr = 9
            self.xpolygonList3.polygons[0].clr = 10
        Drawing.drawPolygons(self.xpolygonList1)
        Drawing.drawPolygons(self.xpolygonList2)
        Drawing.drawPolygons(self.xpolygonList3)

    # 自機と敵との当たり判定
    def checkMyShipCollision(self):
        if self.xpolygonList1 == None:
            return False
        if self.state != 1:
            return False
        pos = gcommon.getCenterPos(ObjMgr.myShip)
        if gcommon.checkCollisionPointAndPolygon(pos, self.xpolygonList2.polygons[0].points):
            return True
        return False

class BossEnemybaseBeam3(enemy.EnemyBase):
    # x,y 弾の中心を指定
    def __init__(self, parent, ox, oy, slowFlag):
        super(__class__, self).__init__()
        self.parent = parent
        self.offsetX = ox
        self.offsetY = oy
        self.x = parent.x +ox
        self.y = parent.y +oy
        self.firstX = self.x
        self.slowFlag = slowFlag
        self.left = -8
        self.top = -1.5
        self.right = 8
        self.bottom = 1.5
        self.layer = gcommon.C_LAYER_GRD | gcommon.C_LAYER_E_SHOT
        self.hitCheck = True
        self.shotHitCheck = False
        self.dx = -3.0

    def update(self):
        self.x += self.dx
        if self.x >= self.firstX -20:
            self.y = self.parent.y +self.offsetY
        if self.cnt == 8:
            self.layer = gcommon.C_LAYER_E_SHOT
        
        if self.x < -12:
            self.remove()
            return
        if self.slowFlag and self.dx < -1.5:
            self.dx *= 0.98

    def draw(self):
        # たぶん、２回描いてる（レイヤが|指定なので）
        if self.cnt % 3 == 0:
            pyxel.blt(gcommon.sint(self.x) -11.5, gcommon.sint(self.y) -1.5, 2, 0, 208, 24, 4, 3)
        else:
            pyxel.blt(gcommon.sint(self.x) -11.5, gcommon.sint(self.y) -1.5, 2, 0, 212, 24, 4, 3)

# ぐるぐるビーム
class BossEnemybaseArcBeam1(enemy.EnemyBase):
    # x,y 弾の中心を指定
    def __init__(self, x, y, directionFlag):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.left = -8
        self.top = -1.5
        self.right = 8
        self.bottom = 1.5
        self.layer = gcommon.C_LAYER_E_SHOT
        self.hitCheck = True
        self.shotHitCheck = False
        self.xpolygonListA1 = None
        self.xpolygonListA2 = None
        self.xpolygonListB1 = None
        self.xpolygonListB2 = None
        self.size = 0.2
        self.rad = math.pi
        self.headX = 0
        self.headY = 0
        self.lengthRate = 1.0
        if GameSession.isEasy():
            self.lengthRate = 0.7
        elif GameSession.isHard():
            self.lengthRate = 1.3
        self.omega = 20.0 if directionFlag else -20.0
        #                   0     1       2       3      4      5
        self.beamPoints = [[0,0],[3, -3],[5, -3],[8, 0],[5, 3],[3, 3]]

    def update(self):
        self.x -= 1
        if self.x < -40:
            self.remove()
            return
        self.beamPoints[2][0] = 5 * self.size
        self.beamPoints[3][0] = 5 * self.size + 3
        self.beamPoints[4][0] = 5 * self.size
        polygonList1 = []
        polygonList1.append(gcommon.Polygon(self.beamPoints, 10))
        self.xpolygonListA1 = gcommon.getAnglePolygons2([self.x, self.y], polygonList1, [-2 * self.size, 0], self.rad, self.lengthRate, 1.0)
        self.xpolygonListA2 = gcommon.getAnglePolygons2([self.x, self.y], polygonList1, [-2 * self.size, 0], self.rad, self.lengthRate, 0.5)
        self.xpolygonListB1 = gcommon.getAnglePolygons2([self.x, self.y], polygonList1, [-2 * self.size, 0], self.rad +math.pi, self.lengthRate, 1.0)
        self.xpolygonListB2 = gcommon.getAnglePolygons2([self.x, self.y], polygonList1, [-2 * self.size, 0], self.rad +math.pi, self.lengthRate, 0.5)
        self.rad += math.pi * self.omega/180
        self.size += 0.1
        if self.size> 8.0:
            self.size = 8.0
        self.omega *= 0.97
        if self.omega > 0:
            if self.omega < 2.0:
                self.omega = 2.0
        else:
            if self.omega > -2.0:
                self.omega = -2.0
    
    def draw(self):
        if self.cnt & 2 == 0:
            self.xpolygonListA1.polygons[0].clr = 9
            self.xpolygonListA2.polygons[0].clr = 10
            self.xpolygonListB1.polygons[0].clr = 9
            self.xpolygonListB2.polygons[0].clr = 10
        else:
            self.xpolygonListA1.polygons[0].clr = 10
            self.xpolygonListA2.polygons[0].clr = 7
            self.xpolygonListB1.polygons[0].clr = 10
            self.xpolygonListB2.polygons[0].clr = 7
        Drawing.drawPolygons(self.xpolygonListA1)
        Drawing.drawPolygons(self.xpolygonListA2)
        Drawing.drawPolygons(self.xpolygonListB1)
        Drawing.drawPolygons(self.xpolygonListB2)


    # 自機と敵との当たり判定
    def checkMyShipCollision(self):
        pos = gcommon.getCenterPos(ObjMgr.myShip)
        if gcommon.checkCollisionPointAndPolygon(pos, self.xpolygonListA1.polygons[0].points):
            return True
        if gcommon.checkCollisionPointAndPolygon(pos, self.xpolygonListB1.polygons[0].points):
            return True
        return False

class BossEnemybaseBody3(enemy.EnemyBase):
    moveTable0 = [
        [0, CountMover.MOVE_TO, 127.5+52, 95.5, 1],
    ]
    moveTable01 = [
        [120, CountMover.STOP],
        [0, CountMover.MOVE_TO, 127.5+52, 95.5, 1],
    ]
    moveTable10 = [
        [90, CountMover.EAGING1, 127.5 +52, 40],
        [90, CountMover.EAGING1, 127.5 +52, 152],
    ]
    moveTable11 = [
        [0, CountMover.MOVE_TO, CountMover.NO_MOVE, 40, 1],
        [0, CountMover.MOVE_TO, CountMover.NO_MOVE, 152, 1],
    ]
    moveTable30 = [
        [0, CountMover.MOVE_TO, CountMover.NO_MOVE, 96, 1],
    ]
    moveTable40 = [
        [0, CountMover.MOVE_TO, CountMover.NO_MOVE, 40, 1],
    ]
    def __init__(self, t):
        super(__class__, self).__init__()
        self.x = t[2]
        self.y = t[3]
        self.isBossRush = t[4]
        self.left = -6
        self.top = -6
        self.right = 6
        self.bottom = 6
        self.hp = boss.BOSS_ENEMYBASE_3
        self.score = 50000
        self.layer = gcommon.C_LAYER_SKY
        self.hitCheck = True
        self.shotHitCheck = True
        self.enemyShotCollision = False
        self.hitcolor1 = 8
        self.hitcolor2 = 14
        self.mover = CountMover(self, __class__.moveTable0, False, True)
        self.coreBrightState = 0
        self.coreBrightness = 0
        self.mode = 0
        self.beamFlag = False
        self.roundBeamCoverPos = 0
        pyxel.image(2).load(0,0,"assets/stage_enemybase-4.png")
        self.timerObj = None
        if self.isBossRush:
            self.timerObj = enemy.Timer1.create(70)

    def update(self):
        if self.mode == 0:
            self.update0()
        elif self.mode == 1:
            self.update1()
        elif self.mode == 2:
            self.update2()
        elif self.mode == 3:
            self.update3()

    def update0(self):
        if self.state == 0:
            #gcommon.debugPrint("x:" + str(self.x) + " y:" +str(self.y))
            # 指定位置まで移動
            #gcommon.scrollController.setIndex(22)
            self.mover.update()
            if self.mover.isEnd:
                self.nextState()
        elif self.state == 1:
            self.nextState()
        elif self.state == 2:
            # この間に本体がやってくる
            if self.cnt > 90:
                self.nextState()
        elif self.state == 3:
            # カバーを格納
            if self.cnt == 70:
                self.nextMode()
                BGM.sound(gcommon.SOUND_COMBINE)

    def update1(self):
        if self.state == 0:
            if self.cnt == 0:
                # 当たり判定変更
                self.left = -24
                self.top = -16
                self.right = 56
                self.bottom = 16
                self.mover = CountMover(self, __class__.moveTable10, True, True)
            self.mover.update()
            if self.mover.cycleCount > 2:
                self.nextMode()
            if self.cnt % 100 == 0 or self.cnt % 100 == 40:
                self.shotBeam(False)
        elif self.state == 1:
            if self.cnt == 0:
                self.mover = CountMover(self, __class__.moveTable11, True, True)
            self.mover.update()
            if self.mover.cycleCount > 1:
                self.nextMode()
            if self.cnt != 0 and self.cnt % 45 == 0:
                self.shotBeam(False)

    # ぐるぐるビーム
    def update2(self):
        if self.state == 0:
            if self.cnt == 0:
                self.mover = CountMover(self, __class__.moveTable11, True, True)
            self.mover.update()
            self.roundBeamCoverPos += 1
            if self.roundBeamCoverPos >= 14:
                self.nextState()
        elif self.state == 1:
            self.mover.update()
            if self.cnt % 90 == 0:
                ObjMgr.addObj(BossEnemybaseArcBeam1(self.x +33, self.y, self.beamFlag))
                enemyOthers.Spark1.create(self, 33, 0, gcommon.C_LAYER_E_SHOT)
                self.beamFlag = not self.beamFlag
            if self.cnt % 140 == 0:
                enemy.enemy_shot_multi(self.x -10, self.y, 2, 0, 5, 3)
            if self.mover.cycleCount > 3:
                self.nextState()
        elif self.state == 2:
            if self.roundBeamCoverPos > 0:
                self.roundBeamCoverPos -= 1
            if self.cnt > 50:
                self.nextMode()

    # ホーミングビーム
    def update3(self):
        if self.state == 0:
            if self.cnt == 0:
                self.mover = CountMover(self, __class__.moveTable30, False, True)
            self.mover.update()
            if self.cnt != 0 and self.cnt % 60 == 0:
                ObjMgr.addObj(enemyShot.HomingBeam1(self.x, self.y -20, -math.pi*150/180,homingTime=45,colorTableNo=1))
                ObjMgr.addObj(enemyShot.HomingBeam1(self.x, self.y +20, math.pi*150/180,homingTime=45,colorTableNo=1))
                ObjMgr.addObj(enemyShot.HomingBeam1(self.x+32, self.y -40, -math.pi*120/180,homingTime=45,colorTableNo=1))
                ObjMgr.addObj(enemyShot.HomingBeam1(self.x+32, self.y +40, math.pi*120/180,homingTime=45,colorTableNo=1))
            if self.cnt > 240:
                self.nextState()
        elif self.state == 1:
            if self.cnt > 120:
                self.setMode(1)
    

    def shotBeam(self, flag):
        f = self.beamFlag if flag else not self.beamFlag

        ObjMgr.addObj(BossEnemybaseBeam3(self, 10, -35, self.beamFlag))
        ObjMgr.addObj(BossEnemybaseBeam3(self, -5, -20, f))
        ObjMgr.addObj(BossEnemybaseBeam3(self, -30, 0, self.beamFlag))
        ObjMgr.addObj(BossEnemybaseBeam3(self, -5, +20, f))
        ObjMgr.addObj(BossEnemybaseBeam3(self, 10, +35, self.beamFlag))
        enemyOthers.Spark1.create(self, 0, -35, gcommon.C_LAYER_E_SHOT)
        enemyOthers.Spark1.create(self, -15, -20, gcommon.C_LAYER_E_SHOT)
        enemyOthers.Spark1.create(self, -40, 0, gcommon.C_LAYER_E_SHOT)
        enemyOthers.Spark1.create(self, -15, 20, gcommon.C_LAYER_E_SHOT)
        enemyOthers.Spark1.create(self, 0, +35, gcommon.C_LAYER_E_SHOT)
        self.beamFlag = not self.beamFlag

    def nextMode(self):
        self.mode += 1
        self.setState(0)
    
    def setMode(self, mode):
        self.mode = mode
        self.setState(0)

    def drawRoundBeamCover(self, px, py):
        pyxel.blt(gcommon.sint(px -50.5)+64, gcommon.sint(py -55.5) +40 -self.roundBeamCoverPos, 2, 104, 112, 40, 16, 3)
        pyxel.blt(gcommon.sint(px -50.5)+64, gcommon.sint(py -55.5) +56 +self.roundBeamCoverPos, 2, 104, 128, 40, 16, 3)

    def drawMainCover(self, px, py, x):
        # 左
        pyxel.blt(gcommon.sint(px -50.5+24 -x*16), py -7.5, 2, 0, 120, 24, 16, 3)
        # 右
        pyxel.blt(gcommon.sint(px -50.5+56 +x*16), py -7.5, 2, 32, 120, 24, 16, 3)
        # 上
        pyxel.blt(gcommon.sint(px -50.5+40), py -55.5+40 -x*16, 2, 72, 112, 24, 16, 3)
        # 下
        pyxel.blt(gcommon.sint(px -50.5+40), py -55.5+56 +x*16, 2, 72, 128, 24, 16, 3)

    def drawNormal(self):
        # 本体
        pyxel.blt(gcommon.sint(self.x -50.5), gcommon.sint(self.y -55.5), 2, 0, 0, 128, 112, 3)
        self.drawRoundBeamCover(self.x, self.y)
        drawCoreCommon(self)
        pyxel.blt(gcommon.sint(self.x -50.5+24), gcommon.sint(self.y -55.5)+40, 2, 0, 144, 49, 32, 3)

    def draw(self):
        if self.mode == 0:
            if self.state in (0,1):
                drawCoreCommon(self)
            elif self.state == 2:
                x = 1.0
                if self.cnt < 90:
                    x = math.pow(1 - (self.cnt/90.0), 3)
                elif self.cnt >= 90:
                    x = 0.0
                pyxel.blt(gcommon.sint(127.5 +52 -50.5 +x*150), gcommon.sint(95.5 -55.5), 2, 0, 0, 128, 112, 3)
                px = 127.5 +52 +x*150
                py = 95.5
                x = 1.0
                self.drawRoundBeamCover(px, py)
                self.drawMainCover(px, py, x)
                drawCoreCommon(self)
            elif self.state == 3:
                x = 0.0
                if self.cnt < 60:
                    x = math.pow(1 - (self.cnt/60.0), 3)
                px = 127.5 +52
                py = 95.5
                # 本体
                pyxel.blt(gcommon.sint(px -50.5), gcommon.sint(py -55.5), 2, 0, 0, 128, 112, 3)
                self.drawRoundBeamCover(px, py)
                drawCoreCommon(self)
                self.drawMainCover(px, py, x)
        elif self.mode in (1, 2, 3):
            self.drawNormal()

    def broken(self):
        self.remove()
        enemy.removeEnemyShot()
        ObjMgr.objs.append(boss.BossExplosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
        #ObjMgr.objs.append(BossEnemybaseAfterBroken())
        ObjMgr.objs.append(enemy.Delay(BossEnemybaseCore, [0, None, self.x, self.y, self.isBossRush], 120))
        BGM.stop()
        GameSession.addScore(self.score)
        BGM.sound(gcommon.SOUND_LARGE_EXP)
        enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
        if self.isBossRush:
            if self.timerObj != None:
                self.timerObj.stop()
                self.timerObj = None

# 破壊後の処理
# ・基地爆発
# ・スクロール制御
class BossEnemybaseAfterBroken(enemy.EnemyBase):
    def __init__(self):
        super(__class__, self).__init__()
        self.layer = gcommon.C_LAYER_SKY
        self.hitCheck = False
        self.shotHitCheck = False
        self.enemyShotCollision = False
    
    def update(self):
        if self.state == 0:
            if self.cnt == 0:
                gcommon.scrollController.setIndex(24)
            if self.cnt > 60 and self.cnt % 20 == 0:
                ObjMgr.addObj(Explosion(random.randrange(10, 256), 10, gcommon.C_LAYER_GRD, gcommon.C_EXPTYPE_GRD_M))
                ObjMgr.addObj(Explosion(random.randrange(10, 256), gcommon.SCREEN_MAX_Y-10, gcommon.C_LAYER_GRD, gcommon.C_EXPTYPE_GRD_M))
                BGM.sound(gcommon.SOUND_MID_EXP)
            if self.cnt > 240:
                self.nextState()
        elif self.state == 1:
            gcommon.scrollController.setIndex(25)
            if self.cnt % 20 == 0:
                ObjMgr.addObj(Explosion(random.randrange(10, 256), 10, gcommon.C_LAYER_GRD, gcommon.C_EXPTYPE_GRD_M))
                ObjMgr.addObj(Explosion(random.randrange(10, 256), gcommon.SCREEN_MAX_Y-10, gcommon.C_LAYER_GRD, gcommon.C_EXPTYPE_GRD_M))
            if gcommon.map_x > 12032:
                self.nextState()
        elif self.state == 2:
            if self.cnt == 60:
                ObjMgr.addObj(enemy.StageClear())

class BossEnemybaseCore(enemy.EnemyBase):
    def __init__(self, t):
        super(__class__, self).__init__()
        self.x = t[2]
        self.y = t[3]
        self.isBossRush = t[4]
        self.left = -6
        self.top = -6
        self.right = 6
        self.bottom = 6
        self.hp = gcommon.HP_NODAMAGE
        self.layer = gcommon.C_LAYER_SKY
        self.hitCheck = False
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.coreBrightState = 0
        self.coreBrightness = 0
        self.interval = 50

    def update(self):
        if self.state == 0:
            if self.cnt % self.interval == 0:
                rad = random.randrange(0, 360) * math.pi/180
                enemy.Splash.appendDr(self.x, self.y, gcommon.C_LAYER_EXP_SKY, rad, 2.0 * math.pi, 20)
                pyxel.stop(0)
                BGM.sound(gcommon.SOUND_SMASH2)
                self.interval -= 3
                if self.interval < 5:
                    self.interval = 5
                if self.cnt > 300:
                    BGM.sound(gcommon.SOUND_LARGE_EXP)
                    enemy.Splash.append2(self.x, self.y, gcommon.C_LAYER_EXP_SKY, 2000)
                    self.nextState()
        elif self.state == 1:
            if self.cnt > 120:
                if self.isBossRush:
                    ObjMgr.objs.append(enemy.BossRushClear())
                    BGM.playOnce(BGM.ENDING)
                else:
                    ObjMgr.objs.append(BossEnemybaseAfterBroken())
                    BGM.play(BGM.BOSS_LAST)
                self.remove()

    def draw(self):
        if self.state == 0:
            drawCoreCommon(self)
