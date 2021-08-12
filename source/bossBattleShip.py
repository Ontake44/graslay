
import pyxel
import math
import random
import gcommon
import enemy
import boss
import drawing
from objMgr import ObjMgr
from gameSession import GameSession
from audio import BGM
from enemy import CountMover

class BossBattleShip(enemy.EnemyBase):
    TILE_LEFT = 4
    TILE_TOP = 15
    TILE_RIGHT = 133
    TILE_BOTTOM = 44
    TILE_WIDTH = 134-3
    TILE_HEIGHT = 45-15
    moveTable0 = [
        [0, CountMover.SET_POS, 256.0, -96.0],
        [9000, CountMover.MOVE, 0.5, 0.0],
    ]
    stateTable0 = [
        [699, 0],
        [1049, 1],
        [1499, 2],
        [1799, 3],
        [5000, 4],
    ]
    # moveTable0 = [
    #     [0, CountMover.SET_POS, 256.0, -80.0],
    #     [2800 -400, CountMover.MOVE, -0.5, 0.0],
    #     [3200 -400, CountMover.MOVE, 0.0, 0.0],
    #     [6000 -400, CountMover.MOVE, 0.5, 0.0],
    # ]
    # moveTable0 = [
    #     [0, CountMover.SET_POS, 256.0, -100.0],
    #     [90, CountMover.MOVE, -1.0, 0.0],
    #     [60, CountMover.ACCEL_RATE, 0.95, 0.95],
    #     [90, CountMover.MOVE, 0.0, 0.5],
    #     [30, CountMover.ACCEL_RATE, 0.95, 0.95],
    #     [120, CountMover.ACCEL_MAX, 0.0, -0.02, 0.0, -0.5],
    #     [30, CountMover.ACCEL_RATE, 0.95, 0.95],
    #     [120, CountMover.ACCEL_MAX, 0.0, 0.02, 0.0, 0.5],
    #     [30, CountMover.ACCEL_RATE, 0.95, 0.95],
    #     [0, CountMover.STOP],
    #     [120, CountMover.ACCEL_MAX, -0.02, 0.0, -1.0, 0.0],
    #     [60, CountMover.ACCEL_RATE, 0.95, 0.95],
    #     [9000, CountMover.STOP],
    # ]
    def __init__(self, t):
        super(__class__, self).__init__()
        self.x = 0
        self.y = 0
        self.moveTable = __class__.moveTable0
        self.mover = CountMover(self, self.moveTable, True)
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
        self.shotEffect = False
        self.hp = boss.BOSS_FIRE_HP
        self.score = 15000
        self.bridge = BossBattleShipBridge(self, (63-__class__.TILE_LEFT) *8, (15 -__class__.TILE_TOP)*8)
        self.engine1 = BossBattleShipEngine(self, 0, (26 -15)*8)
        self.engine2 = BossBattleShipEngine(self, 1*8, (32 -15)*8)
        self.engine3 = BossBattleShipEngine(self, 0, (37 -15)*8)
        self.stater = enemy.CountStater2(self, __class__.stateTable0, False, True)
        self.batteryList = []
        self.appendBattery(12, 22, 0)
        self.appendBattery(18, 21, 0)
        self.appendBattery(23, 21, 0)
        self.appendBattery(28, 21, 0)
        self.appendBattery(33, 21, 0)
        self.appendBattery(49, 20, 0)
        self.appendBattery(53, 20, 0)
        self.appendBattery(11, 43, 1)       # 下
        self.appendBattery(73, 20, 0)
        self.appendBattery(84, 21, 0)
        self.appendBattery(88, 21, 0)
        self.appendBattery(92, 21, 0)
        self.appendBattery(103, 21, 0)
        self.appendBattery(107, 21, 0)
        self.appendBattery(111, 21, 0)

    def appendBattery(self, mx, my, direction):
        self.batteryList.append(BattleShipBattery(self, (mx -__class__.TILE_LEFT)*8, (my -__class__.TILE_TOP)*8, direction))

    def appended(self):
        ObjMgr.addObj(self.bridge)
        ObjMgr.addObj(self.engine1)
        ObjMgr.addObj(self.engine2)
        ObjMgr.addObj(self.engine3)
        for obj in self.batteryList:
            obj.remove_min_x = -128*8
            ObjMgr.addObj(obj)

    def update(self):
        self.mover.update()
        self.stater.update()
        if self.stater.state == 1:
            if self.stater.cnt % 20 == 0:
                p = int((self.stater.cnt-700)/20)
                if p <= 3:
                    ObjMgr.addObj(BattleShipMissileLauncher1(self, (33-__class__.TILE_LEFT + p*5)*8, (32- __class__.TILE_TOP)*8, 33 +p*5, 32, 56))
        elif self.stater.state == 2:
            if self.stater.cnt % 20 == 0:
                p = int((self.stater.cnt-1050)/20)
                if p <= 3:
                    ObjMgr.addObj(BattleShipMissileLauncher1(self, (61-__class__.TILE_LEFT + p*5)*8, (32- __class__.TILE_TOP)*8, 61 +p*5, 32, 56))
        elif self.stater.state == 3:
            if self.stater.cnt == 1500:
                ObjMgr.addObj(BossBattleShipLaserCannon(self, (91-__class__.TILE_LEFT)*8, (31-__class__.TILE_TOP)*8))
        elif self.stater.state == 4:
            if self.stater.cnt % 20 == 0:
                p = int((self.stater.cnt-1800)/20)
                if p <= 3:
                    ObjMgr.addObj(BattleShipMissileLauncher1(self, (102-__class__.TILE_LEFT + p*5)*8, (32- __class__.TILE_TOP)*8, 102 +p*5, 32, 56))

    def draw(self):
        pyxel.bltm(self.x, self.y, 1, 4, 15, 134-4, 45-15, 2)
        gcommon.Text2(200, 184, str(self.stater.cnt), 7, 0)

    # 自機弾と敵との当たり判定
    def checkShotCollision(self, shot):
        if shot.removeFlag:
            return False
        return self.getTileHit(shot.x + (shot.right -shot.left+1)/2, shot.y + (shot.bottom -shot.top+1)/2)

    # 自機と敵との当たり判定
    def checkMyShipCollision(self):
        obj = ObjMgr.myShip
        return self.getTileHit(obj.x + (obj.right -obj.left+1)/2, obj.y + (obj.bottom -obj.top+1)/2)

    # 当たった場合の破壊処理
    # 破壊した場合True
    def doShotCollision(self, shot):
        return False

    def getTileData(self, mx, my):
        return pyxel.tilemap(1).get(mx, my)

    def getTileHit(self, x, y):
        if x < self.x or y < self.y or x >= (self.x + __class__.TILE_WIDTH*8) or y >= (self.y+ __class__.TILE_HEIGHT*8):
            return False
        mx = int((x -self.x)/8) + __class__.TILE_LEFT
        my = int((y -self.y)/8) + __class__.TILE_TOP
        #gcommon.debugPrint("mx=" + str(mx) + " my=" +str(my))
        no = self.getTileData(mx, my)
        return gcommon.mapAttribute2[no >> 5][no & 31] == "1"

# エンジン
class BossBattleShipEngine(enemy.EnemyBase):
    def __init__(self, parent, ox, oy):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = self.parent.x + ox
        self.y = self.parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.left = 0
        self.top = 0
        self.right = 31
        self.bottom = 31
        self.hitcolor1 = 13
        self.hitcolor2 = 7
        self.layer = gcommon.C_LAYER_GRD
        self.exptype = gcommon.C_EXPTYPE_SKY_M
        self.ground = False
        self.hitCheck = True
        self.shotHitCheck = True
        self.hp = 300
        self.score = 500
        self.fire = BossBattleShipBackFire(self, 0, 0)

    def appended(self):
        ObjMgr.addObj(self.fire)

    def update(self):
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY


    def remove(self):
        super(__class__, self).remove()
        if self.fire != None and self.fire.removeFlag == False:
            self.fire.remove()
            self.fire = None

    def draw(self):
        pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 0,87, 3, 4, 2)

    def broken(self):
        super(__class__, self).broken()
        pyxel.tilemap(1).copy(4 +int(self.offsetX/8), 15 +int(self.offsetY/8), 1, 4 +int(self.offsetX/8), 50 +int(self.offsetY/8), 3, 4)

# エンジンバックファイア
class BossBattleShipBackFire(enemy.EnemyBase):
    def __init__(self, parent, ox, oy):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = self.parent.x + ox
        self.y = self.parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.left = -12*8
        self.top = 0
        self.right = -1
        self.bottom = 31
        self.hitcolor1 = 10
        self.hitcolor2 = 7
        self.layer = gcommon.C_LAYER_GRD
        self.exptype = gcommon.C_EXPTYPE_SKY_M
        self.ground = False
        self.hitCheck = False
        self.shotHitCheck = False

    def update(self):
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY
        self.state = int(self.cnt/120) % 4
        if self.state == 2:
            self.hitCheck = True
        else:
            self.hitCheck = False

    def draw(self):
        if self.state == 0:
            return
        elif self.state in (1, 3):
            sx = 0
            sy = 192
            dx = 32
            dy = 32
        elif self.state == 2:
            sx = 0
            sy = 128
            dx = 128
            dy = 32
        fy = 1 if self.cnt & 4 == 0 else -1
        if self.cnt & 2 == 0:
            pyxel.blt(gcommon.sint(self.x -dx), gcommon.sint(self.y), 1, sx, sy, dx, dy *fy, 0)
        else:
            pyxel.blt(gcommon.sint(self.x -dx), gcommon.sint(self.y), 1, sx, sy+32, dx, dy *fy, 0)

# 砲台
class BattleShipBattery(enemy.Battery0):
    # direction  0:上  1:下  2:右  3:左
    def __init__(self, parent, ox, oy, direction):
        super(__class__, self).__init__(parent.x + ox, parent.y + oy, direction)
        self.parent = parent
        self.offsetX = ox
        self.offsetY = oy
        self.ground = False
        self.hp = 50
        self.interval = int(60 / GameSession.enemy_shot_rate)
        self.first = int(60 / GameSession.enemy_shot_rate)

    def update(self):
        super(__class__, self).update()
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY

class BattleShipHomingMissile1(enemy.EnemyBase):
    directionTable = [
        [0, 1, 1],	# 0
        [1, 1, 1],	# 1
        [2, 1, 1],	# 2
        [3, 1, 1],	# 3
        [4, 1, 1],	# 4
        [3, -1, 1],	# 5
        [2, -1, 1],	# 6
        [1, -1, 1],	# 7
        [0, -1, 1],	# 8
        [1, -1, -1],	# 9
        [2, -1, -1],	# 10
        [3, -1, -1],	# 11
        [4, -1, -1],	# 12
        [3, 1, -1],		# 13
        [2, 1, -1],		# 14
        [1, 1, -1]		# 15
    ]
    def __init__(self, x, y, dr):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.dr = dr
        self.left = -4
        self.top = -4
        self.right = 4
        self.bottom = 4
        self.hp = 10
        self.layer = gcommon.C_LAYER_E_SHOT
        self.score = 10
        self.hitCheck = True
        self.shotHitCheck = True
        self.enemyShotCollision = False
        self.imageSourceIndex = 1
        self.imageSourceX = 32
        self.imageSourceY = 224
        self.speed = 4.5

    def update(self):
        if self.x < -32 or self.x > (gcommon.SCREEN_MAX_X+32) or self.y <-32 or self.y > (gcommon.SCREEN_MAX_Y+32):
            self.remove()
            return
        if self.cnt < 60 and self.speed > 3.0:
            self.speed -= 0.05
        if self.cnt < 120 and self.cnt & 1 == 0:
            tempDr = gcommon.get_atan_no_to_ship(self.x, self.y)
            self.dr = (self.dr + gcommon.get_leftOrRight(self.dr, tempDr)) & 63
        self.x += math.cos(gcommon.atan_table[self.dr & 63]) * self.speed
        self.y += math.sin(gcommon.atan_table[self.dr & 63]) * self.speed
        if self.cnt % 3 == 0:
            fx = math.cos(gcommon.atan_table[self.dr]) * 12
            fy = math.sin(gcommon.atan_table[self.dr]) * 12
            ObjMgr.addObj(Smoke1(self.x -fx, self.y -fy))
                
    def draw(self):
        d = ((self.dr + 2) & 63)>>2
        fx = math.cos(gcommon.atan_table[d<<2]) * 8
        fy = math.sin(gcommon.atan_table[d<<2]) * 8
        if self.cnt & 2 == 0:
            if self.cnt & 1 == 0:
                pyxel.blt(self.x -7.5 -fx, self.y -7.5 -fy, self.imageSourceIndex, self.imageSourceX +80, self.imageSourceY, 16, 16, gcommon.TP_COLOR)
            else:
                pyxel.blt(self.x -7.5 -fx, self.y -7.5 -fy, self.imageSourceIndex, self.imageSourceX +96, self.imageSourceY, 16, 16, gcommon.TP_COLOR)
        t = __class__.directionTable[d]
        pyxel.blt(self.x -7.5, self.y -7.5, self.imageSourceIndex, self.imageSourceX + t[0] * 16, self.imageSourceY, 16 * t[1], 16 * -t[2], gcommon.TP_COLOR)

# ミサイル発射管
class BattleShipMissileLauncher1(enemy.EnemyBase):
    stateTable0 = [
        [5, 1],
        [5, 2],
        [5, 3],    # 発射
        [10, 3],    # 発射
        [10, 3],    # 発射
        [5, 2],
        [5, 1],
        [5, 0],
        [5, 4],
    ]
    def __init__(self, parent, ox, oy, mx, my, direction):
        super(__class__, self).__init__()
        self.parent = parent
        self.offsetX = ox
        self.offsetY = oy
        self.mx = mx
        self.my = my
        self.direction = direction
        self.ground = False
        self.hitCheck = False
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.stater = enemy.CountStater(self, __class__.stateTable0, False, False)

    def update(self):
        self.stater.update()
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY
        state = self.stater.state
        if state in (0, 1, 2, 3):
            if self.stater.cnt == 0:
                pyxel.tilemap(1).copy(self.mx, self.my, 1, 3 * state, 84, 3, 3)
        if state == 3:
            if self.stater.cnt == 0:
                px = self.x +12 + gcommon.cos_table[self.direction] * 6.0
                py = self.y +12 + gcommon.sin_table[self.direction] * 6.0
                obj = BattleShipHomingMissile1(px, py, self.direction)
                ObjMgr.addObj(obj)
        if self.stater.isEnd:
            self.remove()

class Smoke1(enemy.EnemyBase):
    def __init__(self, x, y):
        super(__class__, self).__init__()
        self.x = x
        self.y = y
        self.layer = gcommon.C_LAYER_SKY
        self.ground = False
        self.hitCheck = False
        self.shotHitCheck = False
        self.enemyShotCollision = False
        self.nextCnt = random.randrange(7,11)
        self.index = 0

    def update(self):
        newIndex = int(self.cnt/self.nextCnt)
        if newIndex > 5:
            self.remove()
            return
        else:
            if newIndex != self.index:
                self.index = newIndex
                self.nextCnt = random.randrange(5,12)
    
    def draw(self):
        dx = 1 if self.cnt & 1 == 0 else -1
        dy = 1 if self.cnt & 2 == 0 else -1
        pyxel.blt(self.x -7.5, self.y -7.5, 1, 32 + self.index*16, 240, 16 * dx, 16 * dy, 0)

# 艦橋
class BossBattleShipBridge(enemy.EnemyBase):
    def __init__(self, parent, ox, oy):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = self.parent.x + ox
        self.y = self.parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.left = 0
        self.top = 0
        self.right = 31
        self.bottom = 31
        self.hitcolor1 = 13
        self.hitcolor2 = 7
        self.layer = gcommon.C_LAYER_GRD
        self.exptype = gcommon.C_EXPTYPE_SKY_M
        self.ground = False
        self.hitCheck = True
        self.shotHitCheck = True
        self.hp = 800
        self.score = 2000

    def update(self):
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY

    def draw(self):
        pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 0, 92, 6, 4, 2)

    def broken(self):
        super(__class__, self).broken()
        pyxel.tilemap(1).copy(4 +int(self.offsetX/8), 15 +int(self.offsetY/8), 1, 4 +int(self.offsetX/8), 50 +int(self.offsetY/8), 6, 4)

# レーザー砲
#  state
#   0 : シャッター開く
#   1 : レーザー砲出てくる（明るくなる）
#   2 : 回転しながら攻撃（反時計回り）
#   3 : 回転しながら攻撃（時計回り）
#   4 : レーザー砲隠れる（暗くなる）
#   5 : シャッター閉まる
class BossBattleShipLaserCannon(enemy.EnemyBase):
    def __init__(self, parent, ox, oy):
        super(__class__, self).__init__()
        self.parent = parent
        self.x = self.parent.x + ox
        self.y = self.parent.y + oy
        self.offsetX = ox
        self.offsetY = oy
        self.left = 0
        self.top = 0
        self.right = 31
        self.bottom = 31
        self.layer = gcommon.C_LAYER_SKY
        self.ground = False
        self.hitCheck = False
        self.shotHitCheck = False
        self.rad = 0.0
        self.shotCount = 0
        self.gunWidth = 48
        self.gunHeight = 48
        self.image = [None]* self.gunWidth
        self.work = [None]* self.gunHeight
        for y in range(self.gunWidth):
            self.image[y] = [0]*self.gunHeight
        img = pyxel.image(1)
        for y in range(self.gunWidth):
            for x in range(self.gunHeight):
                self.image[y][x] = img.get(x +128, y +128)

    def update(self):
        self.x = self.parent.x + self.offsetX
        self.y = self.parent.y + self.offsetY
        if self.state == 0:
            # シャッター開く
            if self.cnt == 30:
                self.nextState()
        elif self.state == 1:
            # レーザー砲出てくる（明るくなる）
            if self.cnt == 30:
                self.nextState()
        elif self.state == 2:
            # 回転しながら攻撃（反時計回り）
            self.rad -= math.pi * 1.5/180
            if self.cnt % 8 == 0:
                ObjMgr.addObj(boss.BossLaserBeam1(
                    self.x +56/2 + math.cos(self.rad) * 8,
                    self.y +40/2 + math.sin(self.rad) * 8, self.rad))
            if self.rad < -math.pi *150/180:
                self.nextState()
        elif self.state == 3:
            self.rad += math.pi * 1.5/180
            # 回転しながら攻撃（時計回り）
            if self.cnt % 8 == 0:
                ObjMgr.addObj(boss.BossLaserBeam1(gcommon.sint(self.x +56/2), gcommon.sint(self.y +40/2), self.rad))
                if self.rad >= 0.0:
                    self.rad = 0.0
                    self.nextState()
        elif self.state == 4:
            # レーザー砲隠れる（暗くなる）
            if self.cnt == 30:
                self.nextState()
        elif self.state == 5:
            # シャッター閉まる
            if self.cnt == 30:
                self.remove()

    def draw(self):
        if self.state in (0, 5):
            pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 30, 84, 7, 5)
            # レーザー砲
            drawing.Drawing.setBrightnessWithoutBlack2(-3)
            pyxel.blt(gcommon.sint(self.x +(56-self.gunWidth)/2), gcommon.sint(self.y +(40-self.gunHeight)/2), 1, 128, 128, self.gunWidth, self.gunHeight, 2)
            pyxel.pal()
            # シャッター
            if self.state == 0:
                y = int(self.cnt/2)
            else:
                y = 15 -int(self.cnt/2)
            if y <= 15:
                pyxel.blt(self.x, self.y +5, 1, 128, 176+y, 56, 15-y, 2)
                pyxel.blt(self.x, self.y +20+y, 1, 128, 176, 56, 15-y, 2)
            pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 23, 84, 7, 5, 2)
        elif self.state in (1, 4):
            pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 30, 84, 7, 5)
            # レーザー砲
            if self.state == 1:
                drawing.Drawing.setBrightnessWithoutBlack2(int(self.cnt/10) -3)
            else:
                drawing.Drawing.setBrightnessWithoutBlack2(-int(self.cnt/10))
            pyxel.blt(gcommon.sint(self.x +(56-self.gunWidth)/2), gcommon.sint(self.y +(40-self.gunHeight)/2), 1, 128, 128, self.gunWidth, self.gunHeight, 2)
            pyxel.pal()
        elif self.state in (2, 3):
            pyxel.bltm(gcommon.sint(self.x), gcommon.sint(self.y), 1, 30, 84, 7, 5)
            drawing.Drawing.setRotateImage(176, 128, 1, self.work, self.image, -self.rad, 2)
            pyxel.blt(gcommon.sint(self.x +(56-self.gunWidth)/2), gcommon.sint(self.y +(40-self.gunHeight)/2), 1, 176, 128, self.gunWidth, self.gunHeight, 2)
        
