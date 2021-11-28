from drawing import Drawing
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
import myShip

class BossLabyrinth(enemy.EnemyBase):
    moveTable0 = [
        [0, CountMover.SET_POS, 256+48, 96.0],  # 0
        [104, CountMover.MOVE, -1.0, 0.0],      # 1
    ]
    moveTable1 = [
        [30, CountMover.STOP],                  # 0 開く
        [70, CountMover.MOVE, 0.0, 1.0],        # 1
        [140, CountMover.MOVE, 0.0, -1.0],       # 2
        [140, CountMover.MOVE, 0.0, 1.0],        # 3
        [0, CountMover.MOVE_TO, 54.0, CountMover.NO_MOVE, 2.0],      # 4
        [0, CountMover.MOVE_TO, 54.0, 96, 1.0],      # 5
        [70, CountMover.MOVE, 0.0, -1.0],        # 6
        [140, CountMover.MOVE, 0.0, 1.0],        # 7
        [140, CountMover.MOVE, 0.0, -1.0],       # 8
        [0, CountMover.MOVE_TO, 200.0, CountMover.NO_MOVE, 2.0],      # 9
        [0, CountMover.MOVE_TO, 200.0, 96, 1.0],      # 10
        [30, CountMover.STOP],                  # 11 閉じる
    ]
    moveTable100 = [
        [0, CountMover.STOP],
    ]
    moveTable101 = [
        [0, CountMover.MOVE_TO, 200.0, 96, 2.0],      # 10
    ]
    def __init__(self, t):
        super(__class__, self).__init__()
        self.x = t[2]
        self.y = t[3]
        self.left = -45
        self.top = -45
        self.right = 45
        self.bottom = 45
        self.hp = 4000
        self.layer = gcommon.C_LAYER_UNDER_GRD
        self.score = 5000
        self.hitcolor1 = 9
        self.hitcolor2 = 10
        # 第ｎ形態
        self.state = 0
        self.mover = CountMover(self, self.moveTable0, False)
        self.shiftPos = 0

    def update(self):
        self.mover.update()
        if self.state == 1:
            if self.mover.tableIndex == 0:
                # STOP
                self.shiftPos = (self.mover.cnt/30) * 8
            elif self.mover.tableIndex == 11:
                # STOP
                self.shiftPos = 8 -(self.mover.cnt/30) * 8
            elif self.mover.tableIndex >= 1:
                if self.mover.mode == CountMover.MOVE:
                    fx = 1
                    dr = 32
                    if self.x < ObjMgr.myShip.x:
                        fx = -1
                        dr = 0
                    if self.cnt % 60 == 0:
                        enemy.enemy_shot_dr_multi(self.x -48 * fx, self.y-20, 3, 0, dr, 4, 3)
                        enemy.enemy_shot_dr_multi(self.x -48 * fx, self.y+20, 3, 0, dr, 4, 3)
                        # ObjMgr.addObj(BossLabyrinthShot1(self.x -48, self.y-20-16, 4))
                        # ObjMgr.addObj(BossLabyrinthShot1(self.x -48, self.y-20, 4))
                        # ObjMgr.addObj(BossLabyrinthShot1(self.x -48, self.y+20, 4))
                        # ObjMgr.addObj(BossLabyrinthShot1(self.x -48, self.y+20+16, 4))
        elif self.state == 2:
            if self.mover.tableIndex == 0:
                # STOP
                self.shiftPos = (self.mover.cnt/30) * 8
            elif self.mover.tableIndex == 11:
                # STOP
                self.shiftPos = 8 -(self.mover.cnt/30) * 8
            elif self.mover.tableIndex >= 1:
                if self.mover.mode == CountMover.MOVE:
                    fx = 1
                    if self.x < ObjMgr.myShip.x:
                        fx = -1
                    speed = -4.0
                    if self.x < ObjMgr.myShip.x:
                        speed = 4.0
                    if self.cnt % 60 == 0:
                        #enemy.enemy_shot_dr_multi(self.x -48 * fx, self.y-20, 3, 0, dr, 4, 3)
                        #enemy.enemy_shot_dr_multi(self.x -48 * fx, self.y+20, 3, 0, dr, 4, 3)
                        ObjMgr.addObj(BossLabyrinthShot1(self.x -48 * fx, self.y, speed))
                        # ObjMgr.addObj(BossLabyrinthShot1(self.x -48, self.y-20, 4))
                        # ObjMgr.addObj(BossLabyrinthShot1(self.x -48, self.y+20, 4))
                        # ObjMgr.addObj(BossLabyrinthShot1(self.x -48, self.y+20+16, 4))
                    if self.mover.cnt == 30:
                        ObjMgr.addObj(BossLabyrinthBeam1(self, 32, -32, math.pi * 1.75))
                        ObjMgr.addObj(BossLabyrinthBeam1(self, -32, -32, math.pi * 1.25))
                        ObjMgr.addObj(BossLabyrinthBeam1(self, -32, 32, math.pi * 0.75))
                        ObjMgr.addObj(BossLabyrinthBeam1(self, 32, 32, math.pi * 0.25))
        elif self.state == 100:
            # 破壊状態
            if self.cnt % 10 == 0:
                enemy.create_explosion2(self.x + random.randrange(-30, 30), self.y + random.randrange(-30, 30), self.layer, gcommon.C_EXPTYPE_SKY_M, -1)
            if self.cnt > 120:
                self.mover = CountMover(self, self.moveTable101, False)
                self.nextState()
        elif self.state == 101:
            # 破壊状態
            if self.cnt > 90:
                self.remove()
                ObjMgr.addObj(BossLabyrinth2())
        if self.state < 100 and self.mover.isEnd:
            if self.state == 0:
                self.setState(1)
                self.mover = CountMover(self, self.moveTable1, False)
            elif self.state == 1:
                self.setState(2)
                self.mover = CountMover(self, self.moveTable1, False)
            elif self.state == 2:
                self.setState(1)
                self.mover = CountMover(self, self.moveTable1, False)

    def draw(self):
        if self.state == 0:
            # 上
            pyxel.bltm(self.x -47.5, self.y-15.5-32 -self.shiftPos, 0, 0, 0, 12, 4)
            # 中心
            pyxel.bltm(self.x -47.5, self.y-15.5, 0, 0, 4, 12, 4)
            # 下
            pyxel.bltm(self.x -47.5, self.y-15.5+32 +self.shiftPos, 0, 0, 8, 12, 4)
        elif self.state == 1:
            if self.shiftPos > 0:
                Drawing.blt(self.x -47.5, self.y-15.5-8, 2, 0, 40, 96, 8, 3)
                Drawing.blt(self.x -47.5, self.y-15.5+32, 2, 0, 40, 96, 8, 3)

            # 上
            Drawing.bltm(self.x -47.5, self.y-15.5-32 -self.shiftPos, 0, 0, 0, 12, 4)
            # 中心
            Drawing.bltm(self.x -47.5, self.y-15.5, 0, 0, 4, 12, 4)
            # 下
            Drawing.bltm(self.x -47.5, self.y-15.5+32 +self.shiftPos, 0, 0, 8, 12, 4)
        elif self.state == 2:
            # －○
            Drawing.blt(self.x -15.5 -24-self.shiftPos*2, self.y-7.5, 2, 0, 0, 40, 16, 3)
            # ○－
            Drawing.blt(self.x +15.5 -16+self.shiftPos*2, self.y-7.5, 2, 0, 0, -40, 16, 3)
            # ┃
            # ○
            Drawing.blt(self.x -15.5+8, self.y-15.5-24 -self.shiftPos*2, 2, 40, 0, 16, 40, 3)
            # ○
            # ┃
            Drawing.blt(self.x -15.5+8, self.y-15.5+16 +self.shiftPos*2, 2, 40, 0, 16, -40, 3)
            # 上＼
            Drawing.blt(self.x -15.5 -16, self.y-15.5-16, 2, 0, 16, 24, 24, 3)
            # 上／
            Drawing.blt(self.x -15.5 +24, self.y-15.5-16, 2, 0, 16, -24, 24, 3)
            # 下＼
            Drawing.blt(self.x -15.5 -16, self.y-15.5+24, 2, 0, 16, 24, -24, 3)
            # 下／
            Drawing.blt(self.x -15.5 +24, self.y-15.5+24, 2, 0, 16, -24, -24, 3)
            # 上左
            Drawing.blt(self.x -15.5-32 -self.shiftPos, self.y-15.5-32 -self.shiftPos*2, 2, 128, 0, 48, 32, 2)
            # 上右
            Drawing.blt(self.x -15.5+16 +self.shiftPos, self.y-15.5-32 -self.shiftPos*2, 2, 176, 0, 48, 32, 2)
            # 左上
            Drawing.blt(self.x -15.5-32 -self.shiftPos*2, self.y-15.5-32 -self.shiftPos, 2, 96, 0, 32, 48, 2)
            # 右上
            Drawing.blt(self.x -15.5+32 +self.shiftPos*2, self.y-15.5-32 -self.shiftPos, 2, 224, 0, 32, 48, 2)
            # 左下
            Drawing.blt(self.x -15.5-32 -self.shiftPos*2, self.y-15.5+16 +self.shiftPos, 2, 96, 48, 32, 48, 2)
            # 右下
            Drawing.blt(self.x -15.5+32 +self.shiftPos*2, self.y-15.5+16 +self.shiftPos, 2, 224, 48, 32, 48, 2)
            
            # 下左
            Drawing.blt(self.x -15.5-32 -self.shiftPos, self.y-15.5+32 +self.shiftPos*2, 2, 128, 32, 48, 32, 2)
            # 下右
            Drawing.blt(self.x -15.5+16 +self.shiftPos, self.y-15.5+32 +self.shiftPos*2, 2, 176, 32, 48, 32, 2)
                        
            # 中心
            Drawing.blt(self.x -15.5, self.y-15.5, 2, 56, 0, 32, 32)
        elif self.state == 100:
            pyxel.bltm(self.x -47.5, self.y-15.5-32, 0, 0, 0, 12, 12)
            #Drawing.blt(self.x -15.5, self.y-15.5, 2, 56, 0, 32, 32)
        elif self.state == 101:
            # 中心
            Drawing.blt(self.x -15.5, self.y-15.5, 2, 56, 0, 32, 32)

    def broken(self):
        self.setState(100)
        self.shotHitCheck = False
        self.hitCheck = False
        self.mover = CountMover(self, self.moveTable100, False)
        enemy.removeEnemyShot()

# スプレッドレーザー
class BossLabyrinthShot1(enemy.EnemyBase):
    # x,y 弾の中心を指定
    def __init__(self, x, y, speed, spreadTime=120):
        super(__class__, self).__init__()
        self.shotHitCheck = False
        self.x = x
        self.y = y
        self.speed = speed
        self.spreadTime = spreadTime
        self.layer = gcommon.C_LAYER_E_SHOT
        self.left = -4
        self.top = -1.5
        self.right = 4
        self.bottom = 1.5
        self.radius = 1
        self.hitCheck = True

    def update(self):
        if self.state == 0:
            self.x += self.speed
            if self.x <=-12 or self.x >= gcommon.SCREEN_MAX_X+12 or self.y<-8 or self.y >=gcommon.SCREEN_MAX_Y+8:
                self.removeFlag = True
            if self.speed < 0 and self.x < (ObjMgr.myShip.x +myShip.MyShipBase.CENTER_X):
                if self.cnt == 0:
                    self.remove()
                else:
                    self.nextState()
            elif self.speed > 0 and self.x > (ObjMgr.myShip.x +myShip.MyShipBase.CENTER_X):
                if self.cnt == 0:
                    self.remove()
                else:
                    self.nextState()
        elif self.state == 1:
            self.radius += 1
            if self.radius > 22:
                self.nextState()
        else:
            if self.cnt > self.spreadTime:
                self.remove()

        # if gcommon.isMapFreePos(gcommon.getCenterX(self), gcommon.getCenterY(self)) == False:
        # 	self.removeFlag = True

    def draw(self):
        if self.state == 0:
            # pyxel.rect(self.x+ self.left, self.y+self.top, self.right-self.left+1, self.bottom-self.top+1, 8)
            pyxel.blt(self.x -5.5, self.y -1.5, 2, 0, 48, 12, 4, gcommon.TP_COLOR)
        else:
            pyxel.circ(self.x, self.y, self.radius, random.randrange(1,15))

    # 自機と敵との当たり判定
    def checkMyShipCollision(self):
        if self.state == 0:
            super().checkMyShipCollision()
        else:
            return gcommon.get_distance_my(self.x, self.y) < self.radius



class BossLabyrinthBeam1(enemy.EnemyBase):
    beamPoints = [[0,0],[5,-5],[300,-5],[300,5],[5,5]]
    # x,y 弾の中心を指定
    def __init__(self, parent, ox, oy, rad, beamTime=90):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = parent.x + ox
        self.y = parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.rad = rad
        self.beamTime = beamTime
        self.layer = gcommon.C_LAYER_E_SHOT
        self.hitCheck = True
        self.shotHitCheck = False
        self.polygonList1 = []
        self.polygonList1.append(gcommon.Polygon(__class__.beamPoints, 10))
        self.xpolygonList1 = None
        self.xpolygonList2 = None
        self.xpolygonList3 = None
        self.size = 0.0

    def update(self):
        if self.state == 0:
            self.size += 0.05
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

        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY
        self.xpolygonList1 = gcommon.getAnglePolygons2([self.x, self.y], self.polygonList1, [0,0], self.rad, 1.0, self.size)
        self.xpolygonList2 = gcommon.getAnglePolygons2([self.x, self.y], self.polygonList1, [0,0], self.rad, 1.0, self.size*0.8)
        self.xpolygonList3 = gcommon.getAnglePolygons2([self.x, self.y], self.polygonList1, [0,0], self.rad, 1.0, self.size*0.5)
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
        if self.xpolygonList1 == None:
            return False
        pos = gcommon.getCenterPos(ObjMgr.myShip)
        if gcommon.checkCollisionPointAndPolygon(pos, self.xpolygonList1.polygons[0].points):
            return True
        return False

# ボス
class BossLabyrinth2(enemy.EnemyBase):
    # moveTable0 = [
    #     [0, CountMover.SET_POS, 256+48, 96.0],  # 0
    #     [104, CountMover.MOVE, -1.0, 0.0],      # 1
    # ]
    bodyRect1 = gcommon.Rect(-6*8-3.5, -15.5, -15.5, 15.5)
    bodyRect2 = gcommon.Rect(-14.5, -21.5, 39.5, 21.5)
    def __init__(self):
        super(__class__, self).__init__()
        self.x = 200
        self.y = 96
        # 自機弾との当たり判定
        self.left = -6*8-3.5
        self.top = -15.5
        self.right = 32
        self.bottom = 15.5
        self.hp = 6000
        self.layer = gcommon.C_LAYER_UNDER_GRD
        self.score = 15000
        self.hitcolor1 = 8
        self.hitcolor2 = 14
        self.exptype = gcommon.C_EXPTYPE_SKY_L
        self.state = 0
        self.arm1Pos = 0
        self.arm2Pos = 0
        self.beamPrepareEffect = None
        self.dx = 0.0

    def update(self): 
        if self.state == 0:
            # 出現
            if self.cnt >= 79:
                self.nextState()
        elif self.state == 1:
            # 光る
            if self.cnt >= 60:
                self.nextState()
        elif self.state == 2:
            # スプレッドレーザー攻撃（攻撃前の伸び）
            self.arm1Pos += 1
            if self.arm1Pos >= 48:
                self.nextState()
        elif self.state == 3:
            # 待ち
            if self.cnt > 30:
                self.nextState()
        elif self.state == 4:
            # スプレッドレーザー発射
            if self.cnt % 30 == 0:
                n = int(self.cnt /30)
                if n <= 2:
                    y = self.y-39.5 +16 -48 + n * 16 +3
                    ObjMgr.addObj(BossLabyrinthShot1(self.x -22, y, -4, spreadTime=30))
                    y = self.y+23.5 -16 +48 - n * 16 +11
                    ObjMgr.addObj(BossLabyrinthShot1(self.x -22, y, -4, spreadTime=30))
                else:
                    ObjMgr.addObj(BossLabyrinthShot1(self.x -58, self.y -13, -4, spreadTime=30))
                    ObjMgr.addObj(BossLabyrinthShot1(self.x -58, self.y +13, -4, spreadTime=30))
                    self.nextState()
        elif self.state == 5:
            self.arm1Pos -= 1
            self.arm2Pos += 1
            if self.arm2Pos >= 48:
                #gcommon.debugPrint("arm1 " + str(self.arm1Pos) + " arm2 " + str(self.arm2Pos))
                self.nextState()
        elif self.state == 6:
            # ダイアモンドビーム
            if self.cnt % 30 == 0:
                ObjMgr.addObj(BossLabyrinthBeam2(self.x +27, self.y-32, -math.pi/2))
                ObjMgr.addObj(BossLabyrinthBeam2(self.x +27, self.y+32, +math.pi/2))
                # dr64 = 16 + 4 + int(self.cnt/10)
                # enemy.enemy_shot_dr(self.x +16.5, self.y-39.5 -self.arm2Pos +8, 3, 0, dr64)
                # dr64 = 48 -4 -18 + int(self.cnt/10)
                # enemy.enemy_shot_dr(self.x +16.5, self.y+23.5 +self.arm2Pos +8, 3, 0, dr64)
            if self.cnt >= 180:
                self.nextState()
        elif self.state == 7:
            # ARM2収納
            self.arm2Pos -= 1
            if self.arm2Pos == 0:
                self.nextState()
        elif self.state == 8:
            # 艦首ビーム砲準備
            if self.cnt == 0:
                # ビーム発射前の吸い込むようなやつ
                self.beamPrepareEffect = ObjMgr.addObj(boss.BeamPrepareEffect1(self, -7*8, 0.0))
            elif self.cnt > 120:
                if self.beamPrepareEffect != None:
                    self.beamPrepareEffect.remove()
                    self.beamPrepareEffect = None
                self.nextState()
            else:
                # 自機を追いかける
                self.chaseToMyShip()
        elif self.state == 9:
            if self.cnt == 0:
                self.dx = 4.0
            self.x += self.dx
            if self.dx > -1.0:
                self.dx -= 0.1
            if self.x <= 200:
                self.dx = 0.0
                self.x = 200        # ぴったりじゃないと気が済まない
                self.nextState()
            # 艦首ビーム発射
            if self.cnt == 0:
                ObjMgr.addObj(BossLabyrinthBeam1(self, -7*8, 0.0, math.pi, beamTime=180))
                self.dx = 4.0
        elif self.state == 10:
            # ビーム発射しつつ、移動
            self.chaseToMyShip()
            if self.cnt > 60:
                self.nextState()
        elif self.state == 11:
            # Y座標調整
            if self.y > 96:
                self.y -= 1.0
            elif self.y < 96:
                self.y += 1.0
            if math.fabs(self.y -96) < 1.0:
                self.y = 96.0
                self.setState(2)
        self.collisionRects = []
        self.collisionRects.append(__class__.bodyRect1)
        self.collisionRects.append(__class__.bodyRect2)
        self.collisionRects.append(gcommon.Rect.createWH(-31.5 +14, -39.5 +6 -self.arm1Pos, 30, 8))
        self.collisionRects.append(gcommon.Rect.createWH(-31.5 +14, 24.5 +2 +self.arm1Pos, 30, 8))
        self.collisionRects.append(gcommon.Rect.createWH(+16.5+4, -39.5 +4 -self.arm2Pos/3, 25, 12))
        self.collisionRects.append(gcommon.Rect.createWH(+16.5+4, 24.5 +self.arm2Pos/3, 25, 12))
        if self.arm1Pos > 0:
            self.collisionRects.append(gcommon.Rect.createWH(-31.5 +28, -39.5 +16 -self.arm1Pos, 11, self.arm1Pos))
            self.collisionRects.append(gcommon.Rect.createWH(-31.5 +28, 24.5, 11, self.arm1Pos))

    def chaseToMyShip(self):
        y = ObjMgr.myShip.y + myShip.MyShipBase.CENTER_Y
        if math.fabs(y - self.y) > 2.0:
            if y -self.y < 0:
                self.y -= 1.0
            else:
                self.y += 1.0

    def draw(self):
        #pyxel.blt(self.x -15.5, self.y-15.5, 2, 56, 0, 32, 32)
        if self.state == 0:
            # 出現
            p = self.cnt>>1
            pyxel.blt(self.x -15.5, self.y-15.5, 2, 56, 0, 32, 32)
            pyxel.blt(self.x -63.5, self.y -p, 2, 144, 112 +39-p, 14*8, p+1, 3)
            pyxel.blt(self.x -63.5, self.y +1, 2, 144, 112 +40, 14*8, p+1, 3)
            y = self.y -p -1
            while y >= 0:
                pyxel.blt(self.x -63.5, y, 2, 144, 112 +39-p, 14*8, 1, 3)
                y -= 1
            y = self.y +p +1
            while y <= gcommon.SCREEN_MAX_Y:
                 pyxel.blt(self.x -63.5, y, 2, 144, 112 +41+p, 14*8, 1, 3)
                 y += 1

        elif self.state == 1:
            # 光る
            c = self.cnt>>1
            if c < 16:
                Drawing.setBrightnessWithoutBlack(c)
            else:
                Drawing.setBrightnessWithoutBlack(30 - c)
            pyxel.blt(self.x -63.5, self.y-39.5, 2, 144, 112, 14*8, 80, 3)
            pyxel.pal()
        else:
            # アーム前上の隠れている箇所
            y = self.y-39.5 +16 -self.arm1Pos
            while(y < self.y-23.5):
                pyxel.blt(self.x -15.5, y, 2, 16, 72, 24, 16, 3)
                y += 16
            # アーム前下の隠れている箇所
            y = self.y+23.5 -16 +self.arm1Pos
            while(y > self.y+7.5):
                pyxel.blt(self.x -15.5, y, 2, 16, 72, 24, -16, 3)
                y -= 16

            # # アーム後上
            # y = self.y-39.5 +16 -self.arm2Pos
            # while(y < self.y-23.5):
            #     pyxel.blt(self.x +24.5, y, 2, 64, 72, 16, 16, 3)
            #     y += 16
            # # アーム後ろ下
            # y = self.y+24.5 -16 +self.arm2Pos
            # while(y > self.y+7.5):
            #     pyxel.blt(self.x +24.5, y, 2, 64, 72, 16, -16, 3)
            #     y -= 16
            # アーム部
            pyxel.blt(self.x -31.5, self.y-39.5 -self.arm1Pos, 2, 0, 56, 48, 16, 3)
            pyxel.blt(self.x -31.5, self.y+24.5 +self.arm1Pos, 2, 0, 56, 48, -16, 3)
            pyxel.blt(self.x +16.5, self.y-39.5 -self.arm2Pos/3, 2, 56, 56, 32, 32, 3)
            pyxel.blt(self.x +16.5, self.y+24.5 -16 +self.arm2Pos/3, 2, 56, 56, 32, -32, 3)

            # 中心
            pyxel.blt(self.x -63.5, self.y-23.5, 2, 16, 128, 14*8, 48, 3)

            # 前カバー
            p = self.arm1Pos -24
            if p <= 0:
                p = 0
            elif p >= 10:
                p = 10
            pyxel.blt(self.x -63.5, self.y-23.5 -p, 2, 16, 184, 50, 17, 3)
            pyxel.blt(self.x -63.5, self.y+ 8.5 +p, 2, 16, 208, 50, 17, 3)

    def broken(self):
        self.shotHitCheck = False
        enemy.removeEnemyShot()
        ObjMgr.objs.append(boss.BossExplosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
        GameSession.addScore(self.score)
        self.remove()
        BGM.sound(gcommon.SOUND_LARGE_EXP)
        enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
        ObjMgr.objs.append(enemy.Delay(enemy.StageClear, None, 240))

    # 自機弾と敵との当たり判定
    def checkShotCollision(self, shot):
        if shot.removeFlag == False and gcommon.check_collision(self, shot):
            return True
        else:
            return False

# 回転した後、自機狙いのダイアモンドビーム
class BossLabyrinthBeam2(enemy.EnemyBase):
    # x,y 弾の中心を指定
    beamPoints = [[0,4],[14,0],[28,4],[14,8]]
    #beamPoints = [[0,1],[7,0],[14,1],[7,2]]
    #beamPoints = [[0.0,1.5],[7.0,0.0],[14.0,1.5],[7.0,3.0]]
    def __init__(self, x, y, rad):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.rad = rad
        self.left = -2
        self.top = -2
        self.right = 2
        self.bottom = 2
        self.hp = 0
        self.layer = gcommon.C_LAYER_E_SHOT
        self.hitCheck = True
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.dx = math.cos(self.rad) * 0.5
        self.dy = math.sin(self.rad) * 0.5
        self.polygonList = []
        self.angle = 0.0
    
    def update(self):
        self.x += self.dx
        self.y += self.dy
        if self.x < -20 or self.x > 276:
            self.remove()
            return
        elif self.y < -20 or self.y > gcommon.SCREEN_MAX_Y + 20:
            self.remove()
            return
        if self.state == 0:
            self.angle += math.pi/8
            if self.angle >= math.pi * 2:
                self.angle -= math.pi * 2
            if self.cnt > 60:
                self.angle = gcommon.get_atan_to_ship(self.x, self.y)
                self.dx = math.cos(self.angle) * 7.0
                self.dy = math.sin(self.angle) * 7.0
                self.nextState()

        self.polygonList = gcommon.getAnglePoints([0,0], __class__.beamPoints, [14,4], self.angle)

    def draw(self):
        if self.cnt & 2 == 0:
            Drawing.drawPolygonPos(self.x, self.y, self.polygonList, 7)
        else:
            Drawing.drawPolygonPos(self.x, self.y, self.polygonList, 10)

