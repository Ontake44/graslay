
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
import drawing
from drawing import Drawing

class BossEnemybase(enemy.EnemyBase):
    def __init__(self, t):
        super(__class__, self).__init__()
        pos = gcommon.mapPosToScreenPos(172+256, 187-128)
        self.x = pos[0] +127.5
        self.y = pos[1] +95.5
        self.left = 5
        self.top = 5
        self.right = 17
        self.bottom = 17
        self.hp = gcommon.HP_UNBREAKABLE
        self.layer = gcommon.C_LAYER_GRD
        self.hitCheck = False
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.ground = True
        pyxel.image(2).load(0,0,"assets/stage_enemybase-3.png")
        ObjMgr.addObj(BossEnemybaseBody(self.x + 128-16, self.y))

    def update(self):
        pass

    def draw(self):
        pyxel.blt(self.x-127.5, self.y -95.5, 2, 0, 0, 128, 96, 3)
        pyxel.blt(self.x-127.5, self.y +0.5, 2, 0, 0, 128, -96, 3)
        pyxel.blt(self.x+0.5, self.y -95.5, 2, 0, 0, -128, 96, 3)
        pyxel.blt(self.x+0.5, self.y +0.5, 2, 0, 0, -128, -96, 3)


class BossEnemybaseBody(enemy.EnemyBase):
    moveTable0 = [
        [60, CountMover.STOP],
        [40, CountMover.ANGLE_DEG, 1.0],
        [80, CountMover.ANGLE_DEG, -1.0],
        [60, CountMover.ANGLE_DEG, 1.0],
        [20, CountMover.ANGLE_DEG, -1.0],
        #[50, CountMover.ANGLE_DEG, 1.0],
    ]
    moveTable1 = [
        [120, CountMover.ANGLE_DEG, 1.0],
        [240, CountMover.ANGLE_DEG, -1.0],
        [120, CountMover.ANGLE_DEG, 1.0],
        #[50, CountMover.ANGLE_DEG, 1.0],
    ]
    moveTable2 = [
        [360, CountMover.ANGLE_DEG, -1.0],
    ]


    def __init__(self, x, y):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.left = -31.5
        self.top = -31.5
        self.right = 31.5
        self.bottom = 31.5
        self.hp = 9000
        self.layer = gcommon.C_LAYER_SKY
        self.hitCheck = True
        self.shotHitCheck = True
        self.enemyShotCollision = False
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
                self.image[y][x] = img.get(x +0, y +176)
        self.rad = 0.0
        self.mode = 0
        self.mover = None
        self.testRad = 0.0
        self.radSave = -9999.0

    def update(self):
        if self.mode == 0:
            self.update0()
        elif self.mode == 1:
            self.update1()
        #self.testRad = math.fmod(self.testRad + math.pi/180, math.pi*2)

    def update0(self):
        pass
        if self.state == 0:
            if self.cnt > 540:
                self.nextMode()

    def update1xxxx(self):
        if self.cnt % 30 == 0:
            rad = math.pi + random.randrange(-45,45) *math.pi /180
            ObjMgr.addObj(BossEnemybaseShot1(self.x, self.y, rad, 2))

    def update1(self):
        if self.state == 0:
            if self.cnt == 0:
                self.mover = CountMover(self, __class__.moveTable0, False)
                ObjMgr.addObj(BossEnemybaseBeam1(self, -32.0, 0,beamTime=360))
            self.mover.update()
            self.rad = math.radians(self.mover.deg)
            if self.cnt % 30 == 0:
                self.shot1()
            if self.mover.isEnd:
                self.nextState()
        elif self.state == 1:
            if self.cnt == 0:
                self.mover = CountMover(self, __class__.moveTable1, False)
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
                if self.cnt % 80 == 0:
                    self.shotSmall(5)
                else:
                    self.shotSmall(6)
            if self.mover.isEnd:
                self.setState(0)

        self.x = 127.5 + 120 * math.cos(self.rad)
        self.y = 95.5 + 88 * math.sin(self.rad)
            #self.deg += 2
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
            drawing.Drawing.setRotateImage(64, 176, 2, self.work, self.image, -self.rad, 3)
            self.radSave = self.rad
        pyxel.blt(gcommon.sint(self.x -31.5), gcommon.sint(self.y -31.5), 2, 64, 176, self.gunWidth, self.gunHeight, 3)

    def test(self):
        x = 120 * math.cos(self.testRad)
        y = 88 * math.sin(self.testRad)
        px = 127.5 +x
        py = 95.5 + y
        # 法線ベクトルN nx,ny
        nx = -2 * x/(120*120)
        ny = -2 * y/(88*88)
        l = math.sqrt(nx*nx + ny*ny)
        # 単位ベクトル
        nx = nx/l
        ny = ny/l
        n = [nx, ny]
        #gcommon.debugPrint("nx = " + str(nx)+ " ny = " +str(ny))
        # pyxel.circb(127.5 + x, 95.5+ y, 5, 6)
        pyxel.line(127.5 +x, 95.5+y, 127.5 +x + nx*50, 95.5+y + ny*50, 7)


        fx = px - ObjMgr.myShip.x
        fy = py - ObjMgr.myShip.y
        f = [fx, fy]
        a = -gcommon.getInnerProduct(f, n)

        r = gcommon.getVectorPlus(f, [2 * a * n[0], 2 * a * n[1]])
        pyxel.line(px, py, px + r[0], py + r[1], 8)
        pyxel.line(px, py, ObjMgr.myShip.x, ObjMgr.myShip.y, 5)

        # 

        # pyxel.line(px, py, ObjMgr.myShip.x, ObjMgr.myShip.y, 5)
        # wx = -px + ObjMgr.myShip.x
        # wy = -py + ObjMgr.myShip.y

        # angle = math.atan2(vy, vx) - math.atan2(wy, wx)
        # gcommon.debugPrint("angle " + str(angle))
        # pyxel.line(px, py, px + 100 * math.cos(angle), py + 100 * math.sin(angle), 5)



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
        self.layer = gcommon.C_LAYER_UNDER_GRD
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
                gcommon.debugPrint("to State1")
        elif self.state == 1:
            if self.cnt > self.beamTime:
                self.nextState()
                gcommon.debugPrint("to State2")
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

    def draw(self):
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
        pyxel.blt(gcommon.sint(self.x -7.5), gcommon.sint(self.y -7.5), 2, 0, 240, 16, 16, 3)

