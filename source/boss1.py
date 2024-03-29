import pyxel
import math
import random
import gcommon
import enemy
import boss
from objMgr import ObjMgr
from gameSession import GameSession
from audio import BGM

# ボス１の固定台
class Boss1Base(enemy.EnemyBase):
	def __init__(self, t):
		super(Boss1Base, self).__init__()
		self.x = t[2]
		self.y = t[3]
		self.left = 16
		self.top = 16
		self.right = 79
		self.bottom = 45
		self.hp = 999999
		self.layer = gcommon.C_LAYER_UNDER_GRD
		self.ground = True
		self.shotHitCheck = False	# 自機弾との当たり判定
		self.hitCheck = False	# 自機と敵との当たり判定
		self.enemyShotCollision = False	# 敵弾との当たり判定を行う
		self.posY = 0

	def update(self):
		if self.x <= -96:
			self.remove()
			return
		if self.cnt > 210:
			if self.posY < 64:
				self.posY += 1

	def draw(self):
		# 上
		pyxel.blt(self.x, self.y -self.posY -40, 1, 160, 128, 96, -64, gcommon.TP_COLOR)
		# 下
		pyxel.blt(self.x, self.y +31 +self.posY, 1, 160, 128, 96, 64, gcommon.TP_COLOR)
 

class Boss1(enemy.EnemyBase):
    beamTimes = (40, 55, 70)
    def __init__(self, t):
        super(Boss1, self).__init__()
        self.x = t[2]
        self.y = t[3]
        self.isBossRush = t[4]
        self.left = 16
        self.top = 16
        self.right = 93
        self.bottom = 45
        self.collisionRects = gcommon.Rect.createFromList([
            [1, 23, 15, 37], [16, 16, 93, 45]
        ])
        self.hp = gcommon.HP_NODAMAGE
        self.layer = gcommon.C_LAYER_UNDER_GRD
        self.score = 5000
        self.subcnt = 0
        self.hitcolor1 = 9
        self.hitcolor2 = 10
        self.brake = False
        self.beam = 0
        self.subState = 0
        self.isLeft = True
        self.beamTime = __class__.beamTimes[GameSession.difficulty]
        #gcommon.debugPrint("beam Time = " + str(self.beamTime))
        self.tbl = []
        self.shotFlag = False
        self.dy = 0.0
        self.beamObj = Boss1Beam(self)
        ObjMgr.addObj(self.beamObj)
        self.timerObj = None
        if self.isBossRush:
            self.y = 36
            self.state = 900

    def update(self):
        # 向き
        self.isLeft = (self.x + 52) > ObjMgr.myShip.x
        self.beam = 0
        if self.state == 0:
            self.x -= gcommon.cur_scroll_x
            if self.cnt % 60 == 0:
                self.shotFix4()
            if self.cnt > 260:
                self.nextState()
        elif self.state == 1:
            # 指定位置まで移動
            self.x -= gcommon.cur_scroll_x
            self.x += 0.625
            self.y -= 0.20		#0.125
            if self.cnt % 60 == 0:
                self.shotFix4()
            if self.cnt > 270:
                self.nextState()
        elif self.state == 2:
            # 指定位置まで移動
            self.y += 0.25
            if self.cnt % 60 == 0:
                self.shotFix4()
            if self.cnt > 120:
                # x=159 y=36
                self.nextState()
                gcommon.debugPrint("x = " + str(self.x) + " y = " + str(self.y))
                self.hp = boss.BOSS_1_HP
        elif self.state == 3:
            # ４、８方向ショット
            if self.subState == 0:
                self.y -= 0.250
                if self.y < 0:
                    self.y = 0
            else:
                self.y += 0.250
                if self.y > 150:
                    self.y = 150
            if self.cnt & 15 == 15:
                if GameSession.isNormalOrLess():
                    self.shotFix4()
                else:
                    self.shotFix8()
                #if self.cnt & 31 == 31:
                #	self.shotFix4()
                #else:
            if self.cnt > 120:
                self.nextState()
                BGM.sound(gcommon.SOUND_BOSS1PREBEAM)
                if self.subState == 0:
                    self.subState = 1
                else:
                    self.subState = 0
        elif self.state == 4:
            # ビーム発射前
            if self.cnt & 1 == 1:
                x = 50 + random.random() * 30
                y = random.random() * 6
                a = 200 + random.random() * 500
                if self.cnt & 3 == 3:
                    a *= -1
                self.tbl.append(Boss1Star(x, y, a))

            newTbl = []
            for s in self.tbl:
                s.x -= 2
                if s.x>=0:
                    newTbl.append(s)
            self.tbl = newTbl

            if self.cnt > 90:
                self.nextState()
                BGM.sound(gcommon.SOUND_BOSS1BEAM)
        elif self.state == 5:
            # ビーム発射開始（移動なし）
            self.beam = int(self.cnt/3) +1
            if self.beam > 5:
                self.nextState()
        elif self.state == 6:
            # ビーム発射中（移動なし）
            self.beam = 6
            self.beamObj.hitCheck = True
            if self.cnt > 60:
                self.nextState()
        elif self.state == 7:
            # ビーム発射中（移動あり）
            self.beam = 6
            zy = abs(self.y +30 - ObjMgr.myShip.y)
            if zy > 80:
                self.dy = 3
            elif zy > 50:
                self.dy = 2
            elif zy > 20:
                self.dy = 1
            else:
                self.dy = 0.25
            if self.y +30 > ObjMgr.myShip.y:
                self.dy = -self.dy
            self.y += self.dy
            if GameSession.isNormal():
                if self.cnt % 45 == 0:
                    self.shotFix4()
            elif GameSession.isHard():
                if self.cnt % 30 == 0:
                    self.shotFix4()
            if self.cnt > self.beamTime:
                self.nextState()
        elif self.state == 8:
            self.dy = 0.0
            # ビーム発射終了（移動なし）
            self.beam = 5- int(self.cnt/3)
            self.beamObj.hitCheck = False
            if self.beam < 0:
                self.setState(3)

        elif self.state == 900:
            # ボスラッシュ時の初期
            self.x -= 1.0
            if self.x <= 159:
                self.timerObj = enemy.Timer1.create(30)
                self.hp = boss.BOSS_1_HP
                self.setState(3)


    def draw(self):
        if self.state == 4:
            if self.cnt > 20:
                if self.cnt & 3 == 0:
                    pyxel.blt(self.x -22, self.y+22, 1, 48, 208, 24, 16, 0)
                elif self.cnt & 3 == 1:
                    pyxel.blt(self.x -22, self.y+22, 1, 48, 224, 24, 16, 0)
            for s in self.tbl:
                y = s.x* s.x/s.a
                pyxel.pset(self.x -s.x, self.y +28 -y + s.y, 7)
        # 本体
        pyxel.blt(self.x, self.y+8, 1, 160, 208, 40, 48, gcommon.TP_COLOR)
        if self.isLeft:
            pyxel.blt(self.x +40, self.y+8 , 1, 200, 208, 32, 48, gcommon.TP_COLOR)
        else:
            pyxel.blt(self.x +40, self.y+8, 1, 128, 136, 32, 48, gcommon.TP_COLOR)
        pyxel.blt(self.x +72, self.y , 1, 232, 200, 24, 56, gcommon.TP_COLOR)

        # バーニア
        if self.dy > 0.1:
            if self.cnt & 3 == 0:
                pyxel.blt(self.x +24, self.y-6, 1, 24, 176, 8, -26, 0)
                pyxel.blt(self.x +72, self.y-6, 1, 24, 176, 8, -26, 0)
            elif self.cnt & 3 == 2:
                pyxel.blt(self.x +24, self.y-6, 1, 32, 176, 8, -26, 0)
                pyxel.blt(self.x +72, self.y-6, 1, 32, 176, 8, -26, 0)
        elif self.dy < -0.1:
            if self.cnt & 3 == 0:
                pyxel.blt(self.x +24, self.y+42, 1, 24, 176, 8, 26, 0)
                pyxel.blt(self.x +72, self.y+42, 1, 24, 176, 8, 26, 0)
            elif self.cnt & 3 == 2:
                pyxel.blt(self.x +24, self.y+42, 1, 32, 176, 8, 26, 0)
                pyxel.blt(self.x +72, self.y+42, 1, 32, 176, 8, 26, 0)

        # ビーム表示
        if self.beam >= 1 and self.beam <=5:
            bx = self.x -12
            while(bx > -8):
                pyxel.blt(bx, self.y +10, 1, (self.beam-1) * 8, 208, 8, 40, gcommon.TP_COLOR)
                bx -=8
            
        if self.beam == 6:
            # ビーーーーーーーーーーーーーーーム！！！
            pyxel.blt(self.x -16, self.y +10, 1, 144, 208, 16, 40, gcommon.TP_COLOR)
            bx = self.x -32
            sx = 128 - ((self.cnt>>1) & 3) * 16
            while(bx > -32):
                pyxel.blt(bx, self.y +10, 1, sx, 208, 16, 40, gcommon.TP_COLOR)
                bx -=16

    def getDirection(self, dr64):
        if self.isLeft:
            return dr64
        else:
            return gcommon.getMirrorDr64(dr64)

    def shotFix4(self):
        ox = 0 if self.isLeft else 8
        if self.shotFlag:
            enemy.enemy_shot_dr(self.x +48 +ox*2, self.y +22, 4, 1, self.getDirection(32+3))
            enemy.enemy_shot_dr(self.x +52 +ox, self.y +16, 4, 1, self.getDirection(32+7))
            enemy.enemy_shot_dr(self.x +48 +ox*2, self.y +42, 4, 1, self.getDirection(32-3))
            enemy.enemy_shot_dr(self.x +52 +ox, self.y +48, 4, 1, self.getDirection(32-7))
            self.shotFlag = False
        else:
            enemy.enemy_shot_dr(self.x +48 +ox*2, self.y +22, 4, 1, self.getDirection(32+1))
            enemy.enemy_shot_dr(self.x +52 +ox, self.y +16, 4, 1, self.getDirection(32+5))
            enemy.enemy_shot_dr(self.x +48 +ox*2, self.y +42, 4, 1, self.getDirection(32-1))
            enemy.enemy_shot_dr(self.x +52 +ox, self.y +48, 4, 1, self.getDirection(32-5))
            self.shotFlag = True
        BGM.sound(gcommon.SOUND_SHOT2)

    def shotFix8(self):
        ox = 0 if self.isLeft else 8

        if self.shotFlag:
            enemy.enemy_shot_dr(self.x +48 +ox*2, self.y +22, 4, 1, self.getDirection(32+3))
            enemy.enemy_shot_dr(self.x +52 +ox, self.y +16, 4, 1, self.getDirection(32+7))
            enemy.enemy_shot_dr(self.x +48 +ox*2, self.y +42, 4, 1, self.getDirection(32-3))
            enemy.enemy_shot_dr(self.x +52 +ox, self.y +48, 4, 1, self.getDirection(32-7))
            self.shotFlag = False
        else:
            enemy.enemy_shot_dr(self.x +48 +ox*2, self.y +22, 4, 1, self.getDirection(32+1))
            enemy.enemy_shot_dr(self.x +52 +ox, self.y +16, 4, 1, self.getDirection(32+5))
            enemy.enemy_shot_dr(self.x +48 +ox*2, self.y +42, 4, 1, self.getDirection(32-1))
            enemy.enemy_shot_dr(self.x +52 +ox, self.y +48, 4, 1, self.getDirection(32-5))
            self.shotFlag = True
        BGM.sound(gcommon.SOUND_SHOT2)

    def broken(self):
        self.setState(100)
        self.shotHitCheck = False
        self.beamObj.remove()
        enemy.removeEnemyShot()
        ObjMgr.objs.append(boss.BossExplosion(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY))
        GameSession.addScore(self.score)
        self.remove()
        BGM.sound(gcommon.SOUND_LARGE_EXP)
        enemy.Splash.append(gcommon.getCenterX(self), gcommon.getCenterY(self), gcommon.C_LAYER_EXP_SKY)
        if self.isBossRush:
            ObjMgr.objs.append(enemy.NextEvent([0, None, 240]))
            if self.timerObj != None:
                self.timerObj.stop()
                self.timerObj = None
        else:
            ObjMgr.objs.append(enemy.Delay(enemy.StageClear, None, 240))


# 波動砲発射前の、あの吸い込むようなやつ
class Boss1Star:
	def __init__(self, x, y, a):
		self.x = x
		self.y = y
		self.a = a
		self.removeFlag = False


class Boss1Beam(enemy.EnemyBase):
	def __init__(self, bossObj):
		super(Boss1Beam, self).__init__()
		self.bossObj = bossObj
		self.hitCheck = False
		self.shotHitCheck = False
	
	def update(self):
		self.x = 0
		self.y = self.bossObj.y + 10
		self.right = self.bossObj.x
		self.bottom = 39

	def draw(self):
		pass

