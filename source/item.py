import pyxel
import math
import random
import gcommon
import enemy
from objMgr import ObjMgr
from gameSession import GameSession
from audio import BGM

class ScoreItem1(enemy.EnemyBase):
	def __init__(self, mx, my, hide=False):
		super(ScoreItem1, self).__init__()
		pos = gcommon.mapPosToScreenPos(mx, my)
		self.x = pos[0]
		self.y = pos[1]
		self.hide = hide
		self.left = -2
		self.top = -2
		self.right = 17
		self.bottom = 17
		self.layer = gcommon.C_LAYER_GRD
		self.ground = True
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False
		if self.hide == False:
			self.state = 2
		# hide == Trueの場合
		#   state
		#    0 : 隠れている
		#    1 : 自機が通った（表示するが当たり判定なし）
		#    2 : 表示、当たり判定あり
		#    3 : スコア表示
		# hide == False
		#   state
		#    2 : 表示
		#    3 : スコア表示

	# 自機と敵との当たり判定
	def checkMyShipCollision(self):
		if gcommon.check_collision(self, ObjMgr.myShip):
			self.hitCheck = False
			if self.state == 0:
				# しばらくすると当たり判定
				self.setState(1)
			else:
				self.setState(3)
				BGM.sound(gcommon.SOUND_ITEM_GET, gcommon.SOUND_CH2)
				if self.hide:
					GameSession.addScore(1000)
				else:
					GameSession.addScore(500)
		return False

	def update(self):
		if self.x <= -16:
			self.remove()
			return
		if self.state == 1:
			if self.cnt > 20:
				self.setState(2)
				self.hitCheck = True
		elif self.state == 3:
			if self.cnt > 30:
				self.remove()

	def draw(self):
		if self.state == 0:
			pass	#pyxel.blt(self.x, self.y, 0, ((self.cnt>>3)&3) * 16, 192, 16, 16, gcommon.TP_COLOR)
		elif self.state in (1, 2):
			pyxel.blt(self.x, self.y, 0, ((self.cnt>>3)&3) * 16, 176, 16, 16, gcommon.TP_COLOR)
		else:	# 3
			if self.hide:
				pyxel.blt(self.x, self.y +4 -(self.cnt>>1), 0, 16, 208, 16, 8, 0)
			else:
				pyxel.blt(self.x, self.y +4 -(self.cnt>>1), 0, 0, 208, 16, 8, 0)


class OneUpItem1(enemy.EnemyBase):
	def __init__(self, mx, my, hide=False):
		super(OneUpItem1, self).__init__()
		pos = gcommon.mapPosToScreenPos(mx, my)
		self.x = pos[0]
		self.y = pos[1]
		self.hide = hide
		self.left = 0
		self.top = 0
		self.right = 15
		self.bottom = 15
		self.layer = gcommon.C_LAYER_GRD
		self.ground = True
		self.score = 1000
		self.hitCheck = True
		self.shotHitCheck = False
		self.enemyShotCollision = False
		if self.hide == False:
			self.state = 2
		# hide == Trueの場合
		#   state
		#    0 : 隠れている
		#    1 : 自機が通った（表示するが、当たり判定なし）
		#    2 : 表示
		#    3 : 1UP表示
		# hide == False
		#   state
		#    2 : 表示
		#    3 : 1UP表示

	# 自機と敵との当たり判定
	def checkMyShipCollision(self):
		if gcommon.check_collision(self, ObjMgr.myShip):
			self.hitCheck = False
			if self.state == 0:
				# しばらくすると当たり判定
				self.setState(1)
			else:
				self.setState(3)
				GameSession.addPlayerStock()
		return False

	def update(self):
		if self.x <= -16:
			self.remove()
			return
		if self.state == 1:
			if self.cnt > 20:
				self.setState(2)
				self.hitCheck = True
		elif self.state == 3:
			if self.cnt > 45:
				self.remove()

	def draw(self):
		if self.state == 0:
			pass
		elif self.state in (1, 2):
			pyxel.blt(self.x, self.y, 0, ((self.cnt>>3)&3) * 16, 192, 16, 16, gcommon.TP_COLOR)
		else:	# 3
			pyxel.blt(self.x, self.y +4 -(self.cnt>>1), 0, 0, 216, 16, 8, 0)

