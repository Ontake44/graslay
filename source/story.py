
from bossBattleShip import BossBattleShip
import pyxel
import math
import random
import gcommon
import enemy
import boss
import boss1
import boss2
import boss3
import boss4
import bossFactory
import bossLast
import bossWarehouse
import bossCave
import bossFire
import bossBattleShip
import bossLabyrinth
from enemyBattery import MovableBattery1
from enemyBattery import ContainerCarrier1
from enemyBattery import Tractor1
from enemyBattery import HorizonBattery1
from enemyArmored import Armored1, CylinderCrab2
from gameSession import GameSession
from objMgr import ObjMgr
from enemy import CountMover
import enemyFighter
import enemyMine
import enemyOthers
import enemyCreature
import enemyArmored

class StoryManager:

	def __init__(self, obj, story, loopFlag=False, diffTime=False):
		self.obj = obj
		self.story = story
		self.story_pos = 0
		self.cnt = 0
		self.loopFlag = loopFlag
		self.diffTime = diffTime
		self.isEnd = False
		self.cycleCount = 0

	def doStory(self):
		while True:
			if len(self.story) <= self.story_pos:
				if self.loopFlag:
					self.cnt = 0
					self.story_pos = 0
				else:
					self.isEnd = True
					return
			s = self.story[self.story_pos]
			if s[0] < self.cnt:
				pass
			elif s[0] != self.cnt:
				self.cnt += 1
				return
			else:
				method = s[1]	# [1]はメソッド
				if method != None:
					method(self.obj, s)
				if self.diffTime:
					self.cnt = 0
			self.story_pos = self.story_pos + 1

class Story:
	@classmethod
	def getStory1(cls):
		return [
			[150, enemy.Fan1Group, 8, 10, 6],	
			[270, enemy.Fan1Group, 170, 10, 6],	
			[360, enemy.Fan1Group, 8, 10, 6],	
			[450, enemy.Fan1Group, 170, 10, 6],
			[500, enemy.MissileShip, 40, 160],
			[530, enemy.MissileShip, 120, 200],
			[630, enemy.RollingFighter1Group, 42, 15, 4],
			[700, enemy.Battery1, 2+5, 28, 1],
			[700, enemy.Battery1, 2+5, 42, 0],
			[720, enemy.RollingFighter1Group, 100, 15, 4],
			[730, enemy.Battery1, 8+6, 41, 0],
			[730, enemy.Battery1, 8+6, 29, 1],
			[800, enemy.RollingFighter1Group, 42, 15, 4],
			[900, enemy.RollingFighter1Group, 100, 15, 4],
			[1100, enemy.Jumper1, 256, 70, 0.1],
			[1160, enemy.Jumper1, 256, 100, -0.1],
			[1200, enemy.MissileShip, 50, 200],
			[1230, enemy.MissileShip, 120, 160],
			[1300, enemy.Battery1, 41, 27, 1],
			[1360, enemy.Battery1, 45, 23, 1],
			[1460, enemy.Battery1, 49, 19, 1],		\
			[1500, enemy.Battery1, 51, 37, 0],		\
			[1500, enemy.Battery1, 53, 15, 1],		\
			[1500, enemy.Battery1, 55, 33, 0],		\
			[1500, enemy.Jumper1, 256, 70, 0.1],		\
			[1530, enemy.Battery1, 57, 11, 1],		\
			[1530, enemy.Battery1, 59, 29, 0],		\
			[1560, enemy.Jumper1, 256, 70, 0.1],		\
			[1600, enemy.Jumper1, 256, 70, 0.1],		\
			[1630, enemy.Jumper1, 256, 70, 0.1],		\
			[1700, enemy.Jumper1, 256, 70, 0.1],		\
			[1830, enemy.Jumper1, 256, 70, 0.1],		\
			[1860, enemy.Jumper1, 256, 70, 0.1],		\
			[1860, enemy.Battery1, 69, 6, 1],		\
			[1860, enemy.Battery1, 70, 25, 0],		\
			[2100, enemy.RollingFighter1Group, 24, 15, 4],		\
			[2130, enemy.RollingFighter1Group, 90, 15, 4],		\
			[2230, enemy.Jumper1, 256, 70, 0.1],		\
			[2260, enemy.Jumper1, 256, 70, 0.1],		\
			[2430, enemy.MissileShip, 82, 200],		\
			[2430, enemy.Battery1, 100, 7, 1],		\
			[2430, enemy.Battery1, 100, 24, 0],		\
		#	[2460, enemy.MissileShip, 82, 200],		\
		#	[2490, enemy.MissileShip, 82, 200],		\
			[2500, enemy.Battery1, 105, 7, 1],		\
			[2500, enemy.Battery1, 105, 24, 0],		\
			[2700, enemy.RollingFighter1Group, 24, 15, 4],		\
			[2760, enemy.RollingFighter1Group, 80, 15, 4],		\
			[2800, enemy.RollingFighter1Group, 40, 15, 4],		\
			[2830, enemy.MissileShip, 40, 160],		\
			[2860, enemy.RollingFighter1Group, 120, 15, 4],		\
			[2900, enemy.MissileShip, 80, 200],		\
			[3000, enemy.RollingFighter1Group, 30, 15, 4],		\
			[3060, enemy.RollingFighter1Group, 120, 15, 4],		\
			[3240, enemy.Jumper1, 256, 30, -0.1],		\
			[3280, enemy.Jumper1, 256, 50, 0.1],		\
			[3350, enemy.Battery1, 144, 33, 1],		\
			[3350, enemy.Battery1, 144, 35, 0],		\
			[3360, enemy.Battery1, 146, 33, 1],		\
			[3360, enemy.Battery1, 146, 35, 0],		\
			[3400, enemy.Battery1, 118, 40, 1],		\
			[3400, enemy.Battery1, 118, 42, 0],		\
			[3420, enemy.Battery1, 144, 43, 1],		\
			[3420, enemy.Battery1, 144, 45, 0],		\
			[3460, enemy.Battery1, 118, 50, 1],		\
			[3460, enemy.Battery1, 118, 52, 0],		\
			[4000, enemy.Jumper1, 256, 150, -0.1],		\
			[4030, enemy.Jumper1, 256, 150, -0.1],		\
			[4060, enemy.Jumper1, 256, 150, -0.1],		\
			[4160, enemy.WhereAppear, GameSession.isNormalOrMore(), enemy.Jumper1, [-16, 50, 0.1]],
			[4190, enemy.WhereAppear, GameSession.isNormalOrMore(), enemy.Jumper1, [-16, 50, 0.1]],
			[4200, enemy.Battery1, 162, 60, 1],		\
			[4200, enemy.Battery1, 164, 60, 1],		\
			[4200, enemy.Jumper1, 256, 130, -0.1],		\
			[4230, enemy.Jumper1, 256, 150, -0.1],		\
			[4400, enemy.Jumper1, 256, 100, 0.1],		\
			[4400, enemy.MissileShip, 80, 200],		\
			[4400, enemy.Battery1, 154, 81, 0],		\
			[4420, enemy.Battery1, 156, 81, 0],		\
			[4430, enemy.MissileShip, 120, 200],		\
			[4500, enemy.Jumper1, 256, 100, 0.1],		\
			[4500, enemy.Battery1, 170, 81, 0],		\
			[4520, enemy.Battery1, 172, 81, 0],		\
			[4530, enemy.Jumper1, 256, 120, 0.1],		\
			[4700, enemy.RollingFighter1Group, 50, 15, 4],		\
			[4730, enemy.RollingFighter1Group, 110, 15, 4],		\
			[4830, enemy.MissileShip, 120, 200],		\
			[4860, enemy.MissileShip, 70, 200],		\
			[5100, boss1.Boss1, 256, 60],		\
			[5100, boss1.Boss1Base, 256, 60],		\
			# [5100, enemy.DockArm, 204, 59, 180],		\
			# [5100, enemy.DockArm, 212, 59, 180],		\
			# [5130, enemy.DockArm, 206, 59, 180],		\
			# [5130, enemy.DockArm, 210, 59, 180],		\
		]

	@classmethod
	def getStory2(cls):
		return [ \
			[180, enemy.Cell1Group1, 256, 10, 0],		\
			[240, enemy.Cell1Group1, 256, 60, 0],		\
			[260, enemy.WhereAppear, GameSession.isNormalOrMore(), enemy.Cell1Group1, [-16, 60, 0]],		\
			[320, enemy.Cell1Group1, 256, 20, 0],		\
			[400, enemy.Cell1Group1, 256, 50, 0],		\
			[1100, enemy.Cell1Group1, 20, 192, 1],		\
			[1500, enemy.Cell1Group1, 0, 192, 1],		\
			[2000, enemy.Cell1Group1, 256, 100, 0],		\
			[2300, enemy.Cell1Group1, 256, 100, 0],		\
			[2400, enemy.Worm1, 90, 91, 2, 4, 60],		\
			[2600, enemy.Cell1Group1, 256, 100, 0],		\
			[2610, enemy.Worm1, 103, 75, 6, 5, 80],		\
			[2760, enemy.Worm1, 111, 69, 0, 5, 90],		\
			[2800, enemy.Worm1, 122, 74, 4, 5, 130],		\
			[3200, enemy.Cell1Group1, 150, -16, 1],		\
			[3360, enemy.Cell1Group1, -16, 10, 0],		\

			[3360, enemy.Worm1, 93, 56, 1, 5, 130],		\

			[3600, enemy.Worm1, 100, 40, 3, 5, 230],		\

			[3800, enemy.Cell1Group1, 30, -16, 1],		\
			[4400, enemy.Cell1Group1, 256, 30, 0],		\
			[4500, enemy.Cell2, 256, 60, -1, -1, 0],		\
			[4510, enemy.Cell2, 256, 80, -1, 1, 0],		\
			[4600, enemy.Cell2, 256, 70, -1, 1, 0],		\

			[4610, enemy.Cell2, 256, 30, -0.5, -1, 0],		\
			[4620, enemy.Cell2, 256, 80, -0.5, 1, 0],		\
			[4640, enemy.Cell2, 256, 70, -0.5, 1, 0],		\
			[4660, enemy.Cell2, 256, 40, -0.5, 1, 0],		\
			[4680, enemy.Cell2, 256, 30, -0.5, 1, 0],		\

			# 斜面に上からへばり付いてるやつ
			[4800, enemy.Worm1, 144, 15, 7, 5, 160],		\
			[5000, enemy.WhereAppear, GameSession.isNormalOrMore(), enemy.Cell1Group1, [-256, 20, 0]],

			[5300, enemy.Worm1, 175, 28, 2, 5, 160],		\

			[5300, enemy.Worm2Group, 330, 30, 32, 10, enemy.worm2Tbl1],		\

			[5310, enemy.Cell1Group1, 256, 10, 0],		\
			[5360, enemy.Cell1Group1, 256, 60, 0],		\

			[5400, enemy.Worm1, 180, 9, 6, 5, 160],		\
			[5700, enemy.Worm2Group, 200, -24, 16, 10, enemy.worm2Tbl2],		\


			[5700, enemy.Worm1, 195, 26, 2, 5, 160],		\

			[5710, enemy.Cell1Group1, 256, 30, 0],		\
			[5760, enemy.Cell1Group1, 256, 100, 0],		\

			[5800, enemy.Worm2Group, 176, -24, 16, 10, enemy.worm2Tbl3],		\
			
			[5800, enemy.Worm1, 207, 9, 6, 5, 160],		\
			
			[5810, enemy.Cell1Group1, 256, 30, 0],		\
			[5860, enemy.Cell1Group1, 256, 100, 0],		\

			[6000, enemy.Worm2Group, 176, 192, 48, 10, enemy.worm2Tbl4],		\

			[6000, enemy.Worm1, 230, 8, 6, 5, 160],		\
			[6000, enemy.Worm1, 228, 25, 2, 5, 160],		\

			[6400, boss2.Boss2, 241, 16],		\
		]

	@classmethod
	def getStoryCave(cls):
		return [
			[100, enemyFighter.Fighter4Group, 0, 60, 20, 5],
			[240, enemyFighter.Fighter4Group, 1, 60, 20, 5],
			[300, enemyMine.Mine1, 256, 12 *8, 90, 150],
			[360, enemyMine.Mine1, 256, 12 *8, 90, 150],
			#[460, enemyFighter.Fighter4Group, 1, 60, 20, 5],
			#[580, enemyFighter.Fighter4Group, 0, 60, 20, 5],
			[800, enemyFighter.Fighter4Group, 0, 60, 20, 5],
			[940, enemyFighter.Fighter4Group, 1, 60, 20, 5],
			[1200, enemyFighter.Fighter4Group, 2, 120, 20, 5],
			[1260, enemyMine.Mine1, 256, 45 *8, 150, -150],
			[1320, enemyMine.Mine1, 256, 47 *8, 150, -150],
			[1320, enemyFighter.Fighter4Group, 3, 150, 20, 5],
			[1800, enemyFighter.Fighter4Group, 2, 120, 20, 5],
			[1920, enemyFighter.Fighter4Group, 3, 150, 20, 5],
			[2100, enemyFighter.Fighter4Group, 2, 120, 20, 5],
			[2120, enemyFighter.Fighter4Group, 3, 150, 20, 5],
			[2400, enemyFighter.Fighter4Group, 4, 150, 20, 5],
			[3100, enemyFighter.Fighter4Group, 3, 150, 20, 5],
			[3240, enemyFighter.Fighter4Group, 4, 150, 20, 5],
			[3300, enemy.WaterSurface, 0, 200],
			[3500, enemyFighter.Fighter4Group, 0, 60, 20, 5],
			[3600, enemyCreature.Worm3, 256, 8 * 85],
			[3640, enemyFighter.Fighter4Group, 1, 60, 20, 5],
			[3720, enemyCreature.Worm3, 256, 8 * 89],
			[3890, enemyMine.Mine1, 256, 77 *8, 90, 150],
			[3950, enemyMine.Mine1, 256, 77 *8, 90, 150],
			[4010, enemyMine.Mine1, 256, 97 *8, 90, -150],
			[4400, enemyCreature.Worm3, 256, 8 * 87],
			[4600, enemyCreature.Worm3, 256, 8 * 94],
			[4900, enemyCreature.Worm3, 256, 8 * 87],
			[4960, enemyCreature.Worm3, 256, 8 * 90],
			[5020, enemyCreature.Worm3, 256, 8 * 94],
			[5600, enemyCreature.Worm3, 256, 8 * 94],
			[5690, enemyCreature.Worm3, 256, 8 * 87],
			[5780, enemyCreature.Worm3, 256, 8 * 90],
			[6360, bossCave.BossCave],
		]

	@classmethod
	def getStoryWarehouse(cls):
		tbl1 = [[300, 0, 0.0, -1.0],[30, 0, -3.0, 0.5],[600, 0, -3.0,0.0]]
		baseOffset = 0
		return [
			[150, Armored1, 256, 120,
				[
					[50, 0, -2.0, 0.0],	# 0: 右から出現
					[40, 4, 0.9, 0.0],  # 1: 減速
					[1, 0, 0.0, 0.0],	# 2: 速度リセット
					[30, 2, 0.0, -0.1], # 3: 上に移動
					[20, 4, 0.95, 0.95], # 4: 上移動減速
					[1, 0, 0.0, 0.0],	# 5: 速度リセット
					[120, 2, -0.05, 0.0]	#  5: 左に移動
				]
			],
			[210, Armored1, 256, 20,
				[
					[20, 0, -2.0, 0.0],	# 0: 右から出現
					[40, 4, 0.9, 0.0],  # 1: 減速
					[1, 0, 0.0, 0.0],	# 2: 速度リセット
					[30, 2, 0.0, 0.1], # 3: 下に移動
					[20, 4, 0.95, 0.95], # 4: 上移動減速
					[1, 0, 0.0, 0.0],	# 5: 速度リセット
					[120, 2, -0.05, 0.0]	#  5: 左に移動
				]
			],
			[baseOffset + 600, MovableBattery1, 33, 45, 60,
				tbl1
			],
			[baseOffset + 630, ContainerCarrier1, 33, 45, tbl1],
			[baseOffset + 660, MovableBattery1, 40, 18, 60,
				[[96, 0, 0.0, 1.0],[56, 0, -1.0, 0.0],[150, 0, 0.0, 1.0]]
			],
			[baseOffset + 780, MovableBattery1, 47, 18, 60,
				[[300, 0, 0.0, 1.0]]
			],
			[baseOffset + 810, ContainerCarrier1, 47, 18, 
				[[300, 0, 0.0, 1.0]]
			],
			[baseOffset + 870, MovableBattery1, 40, 18, 60,
				[[48, 0, 0.0, 1.0], [26*8, 0, 1.0, 0.0], [6*8, 0, 0.0, 1.0], [8*8, 0, 1.0, 0.0], [300, 0, 0.0, 1.0]]
			],
			[baseOffset + 910, ContainerCarrier1, 40, 18,
				[[48, 0, 0.0, 1.0], [26*8, 0, 1.0, 0.0], [6*8, 0, 0.0, 1.0], [8*8, 0, 1.0, 0.0], [300, 0, 0.0, 1.0]]
			],
			[baseOffset + 950, ContainerCarrier1, 40, 18,
				[[48, 0, 0.0, 1.0], [26*8, 0, 1.0, 0.0], [6*8, 0, 0.0, 1.0], [8*8, 0, 1.0, 0.0], [300, 0, 0.0, 1.0]]
			],
			[baseOffset + 1100, MovableBattery1, 47, 45, 60,
				[[300, 0, 0.0, -1.0]]
			],
			[baseOffset + 1230, MovableBattery1, 66, 45, 60,
				[[300, 0, 0.0, -1.0]]
			],
			[baseOffset + 1260, MovableBattery1, 74, 18, 60,
				[[300, 0, 0.0, 1.0]]
			],
			[baseOffset + 1300, ContainerCarrier1, 74, 18,
				[[300, 0, 0.0, 1.0]]
			],
			[baseOffset + 1600, MovableBattery1, 89, 44, 60,
				[[14*8, 0, 0.0, -1.0],[42*8, 0, 1.0, 0.0]]
			],
			[baseOffset + 1640, ContainerCarrier1, 89, 44,
				[[14*8, 0, 0.0, -1.0],[42*8, 0, 1.0, 0.0]]
			],
			[baseOffset + 1780, MovableBattery1, 89, 44, 60,
				[[14*8, 0, 0.0, -1.0],[16*8, 0, 1.0, 0.0],[300, 0, 0.0, 1.0]]
			],
			# 一時停止する
			[baseOffset + 1780, MovableBattery1, 105, 18, 60,
				[[8*8, 0, 0.0, 1.0],[6*8, 0, 0.0, 0.0],[4*8, 0, 0.0, 1.0],[14*8, 0, 1.0, 0.0],[30*8, 0, 0.0, -1.0]]
			],
			[baseOffset + 1820, ContainerCarrier1, 89, 44,
				[[14*8, 0, 0.0, -1.0],[16*8, 0, 1.0, 0.0],[300, 0, 0.0, 1.0]]
			],
			[baseOffset + 2100, MovableBattery1, 132, 30, 60,
				[[13*8, 0, -1.0, 0.0], [30*8, 0, 0.0, -1.0]]
			],
			[baseOffset + 2130, MovableBattery1, 100, 30, 60,
				[[40*8, 0, 1.0, 0.0]]
			],
			[baseOffset + 2380, MovableBattery1, 102, 53, 60,
				[[80*8, 0, 1.0, 0.0]]
			],
			[baseOffset + 2400, MovableBattery1, 136, 53, 60,
				[[13*8, 0, -1.0, 0.0], [80*8, 0, 0.0, 1.0]]
			],
			[baseOffset + 2410, MovableBattery1, 102, 53, 60,
				[[15*8, 0, 1.0, 0.0], [80*8, 0, 0.0, 1.0]]
			],
			[baseOffset + 2470, MovableBattery1, 102, 53, 60,
				[[21*8, 0, 1.0, 0.0], [80*8, 0, 0.0, 1.0]]
			],
			[baseOffset + 2700, MovableBattery1, 102, 68, 60,
				[[15*8, 0, 1.0, 0.0], [80*8, 0, 0.0, 1.0]]
			],
			[baseOffset + 2760, MovableBattery1, 134, 68, 60,
				[[11*8, 0, -1.0, 0.0], [80*8, 0, 0.0, 1.0]]
			],
			[baseOffset + 2790, MovableBattery1, 102, 72, 60,
				[[15*8, 0, 1.0, 0.0], [80*8, 0, 0.0, 1.0]]
			],
			[baseOffset + 2920, MovableBattery1, 134, 72, 60,
				[[11*8, 0, -1.0, 0.0], [80*8, 0, 0.0, 1.0]]
			],
			[baseOffset + 3100, MovableBattery1, 101, 96, 60,
				[[16*8, 0, 1.0, 0.0], [80*8, 0, 0.0, 1.0]]
			],
			[baseOffset + 3160, MovableBattery1, 135, 96, 60,
				[[12*8, 0, -1.0, 0.0], [80*8, 0, 0.0, 1.0]]
			],
			[baseOffset + 3360, MovableBattery1, 101, 96, 180,
				[[16*8, 0, 1.0, 0.0], [80*8, 0, 0.0, 1.0]]
			],
			[baseOffset + 3400, Armored1, 256, 130,
				[
					[40, 0, -2.0, 0.0],	# 0: 右から出現
					[40, 4, 0.9, 0.0],  # 1: 減速
					[1, 0, 0.0, 0.0],	# 2: 速度リセット
					[25, 2, 0.0, -0.1], # 3: 上に移動
					[20, 4, 0.95, 0.95], # 4: 上移動減速
					[20, 0, 0.0, 0.0],	# 5: 速度リセット
					[30, 2, 0.0, 0.075], # 3: 下に移動
					[20, 4, 0.95, 0.95], # 4: 下移動減速
					[1, 0, 0.0, 0.0],	# 5: 速度リセット
					[120, 2, -0.05, 0.0]	#  5: 左に移動
				]
			],
			[baseOffset + 3400, MovableBattery1, 135, 96, 60,
				[[12*8, 0, -1.0, 0.0], [80*8, 0, 0.0, 1.0]]
			],
			[baseOffset + 3460, Armored1, 256, 60,
				[
					[20, 0, -2.0, 0.0],	# 0: 右から出現
					[40, 4, 0.9, 0.0],  # 1: 減速
					[1, 0, 0.0, 0.0],	# 2: 速度リセット
					[25, 2, 0.0, 0.1], # 3: 下に移動
					[20, 4, 0.95, 0.95], # 4: 下移動減速
					[20, 0, 0.0, 0.0],	# 5: 速度リセット
					[30, 2, 0.0, -0.075], # 3: 上に移動
					[20, 4, 0.95, 0.95], # 4: 上移動減速
					[1, 0, 0.0, 0.0],	# 5: 速度リセット
					[120, 2, -0.05, 0.0]	#  5: 左に移動
				]
			],
			[baseOffset + 3460, Tractor1, 147, 120,
				[[64*8, 0, 0.0, -0.5]]
			],
			[baseOffset + 3560, enemy.Jumper1, 256, 70, 0.1],
			[baseOffset + 3590, enemy.Jumper1, -16, 70, 0.1],
			[baseOffset + 3590, enemy.Jumper1, 256, 70, 0.1],
			[baseOffset + 3620, enemy.Jumper1, -16, 70, 0.1],
			[baseOffset + 3800, MovableBattery1, 163, 119, 60,
				[[80*8, 0, 0.0, -1.0]]
			],
			[baseOffset + 3860, MovableBattery1, 163, 119, 60,
				[[80*8, 0, 0.0, -1.0]]
			],
			[baseOffset + 3960, enemy.Jumper1, 256, 70, 0.1],
			[baseOffset + 3990, enemy.Jumper1, -16, 70, 0.1],
			[baseOffset + 3990, enemy.Jumper1, 256, 70, 0.1],
			[baseOffset + 4020, enemy.Jumper1, -16, 70, 0.1],

			[baseOffset + 4100, Armored1, 256, 130,
				[
					[40, 0, -2.0, 0.0],	# 0: 右から出現
					[40, 4, 0.9, 0.0],  # 1: 減速
					[1, 0, 0.0, 0.0],	# 2: 速度リセット
					[25, 2, 0.0, -0.1], # 3: 上に移動
					[20, 4, 0.95, 0.95], # 4: 上移動減速
					[20, 0, 0.0, 0.0],	# 5: 速度リセット
					[30, 2, 0.0, 0.075], # 3: 下に移動
					[20, 4, 0.95, 0.95], # 4: 下移動減速
					[1, 0, 0.0, 0.0],	# 5: 速度リセット
					[120, 2, -0.05, 0.0]	#  5: 左に移動
				]
			],
			[baseOffset + 4160, Armored1, 256, 60,
				[
					[20, 0, -2.0, 0.0],	# 0: 右から出現
					[40, 4, 0.9, 0.0],  # 1: 減速
					[1, 0, 0.0, 0.0],	# 2: 速度リセット
					[25, 2, 0.0, 0.1], # 3: 下に移動
					[20, 4, 0.95, 0.95], # 4: 下移動減速
					[20, 0, 0.0, 0.0],	# 5: 速度リセット
					[30, 2, 0.0, -0.075], # 3: 上に移動
					[20, 4, 0.95, 0.95], # 4: 上移動減速
					[1, 0, 0.0, 0.0],	# 5: 速度リセット
					[120, 2, -0.05, 0.0]	#  5: 左に移動
				]
			],

			[baseOffset + 4230, enemy.Jumper1, 256, 80, 0.1],
			[baseOffset + 4260, enemy.Jumper1, 256, 80, 0.1],
			[baseOffset + 4300, enemy.Jumper1, -16, 70, 0.1],
			[baseOffset + 4330, enemy.Jumper1, -16, 60, 0.1],

			[baseOffset + 4400, enemy.Jumper1, 256, 60, 0.1],
			[baseOffset + 4600, enemy.Jumper1, -16, 70, 0.1],
			# 4712上スクロール
			[baseOffset + 4700, enemy.EnemyGroup, ContainerCarrier1,
				[0, None, 188, 96,
					[[50*8, 0, 1.0, 0.0]]
				],
				30, 5
			],
			[baseOffset + 4800, enemy.EnemyGroup, ContainerCarrier1,
				[0, None, 218, 83,
					[[50*8, 0, -1.0, 0.0]]
				],
				30, 9
			],
			[baseOffset + 4830, enemy.Jumper2, 90, -16, -0.075],
			[baseOffset + 4850, enemy.Jumper2, 90, -16, -0.075],
			[baseOffset + 4890, enemy.Jumper2, 150, -16, 0.075],
			[baseOffset + 4910, enemy.Jumper2, 150, -16, 0.075],
			[baseOffset + 4960, enemy.Jumper2, 90, -16, -0.075],
			[baseOffset + 5020, enemy.Jumper2, 150, -16, 0.075],
			[baseOffset + 5160, enemy.EnemyGroup, MovableBattery1, 
				[0, None, 199, 61, 90,
					[[80*8, 0, 0.0, 1.0]]
				],
				30, 3
			],
			[baseOffset + 5400, enemy.EnemyGroup, MovableBattery1, 
				[0, None, 207, 77, 90,
					[[80*8, 0, 0.0, -1.0]]
				],
				30, 3
			],
			[baseOffset + 5400, MovableBattery1, 219, 78, 60,
				[[25*8, 0, 0.0, -1.0], [100*8, 0, 1.0, 0.0]]
			],
			# 5512右スクロール
			[baseOffset + 5660, enemy.EnemyGroup, MovableBattery1, 
				[0, None, 235, 61, 60,
					[[16*8, 0, -1.0, 0.0], [100*8, 0, 0.0, -1.0]]
				], 48, 2
			],
			[baseOffset + 5660, enemy.EnemyGroup, MovableBattery1, 
				[0, None, 219, 42, 150,
					[[11*8, 0, 0.0, 1.0], [100*8, 0, 1.0, 0.0]]
				], 48, 2
			],
			# [baseOffset + 5860, MovableBattery1, 219, 71, 60,
			# 	[[19*8, 0, 0.0, -1.0], [100*8, 0, 1.0, 0.0]]
			# ],
			[baseOffset + 5860, enemy.EnemyGroup, MovableBattery1, 
				[0, None, 219, 71, 60,
					[[10*8, 0, 0.0, -1.0], [30*8, 0, 1.0, 0.0], [100*8, 0, 0.0, -1.0], [100*8, 0, 1.0, 0.0]]
				], 48, 2
			],
			[baseOffset + 6060, enemy.EnemyGroup, MovableBattery1, 
				[0, None, 249, 42, 60,
					[[11*8, 0, 0.0, 1.0], [100*8, 0, -1.0, 0.0]]
				], 48, 2
			],
			[baseOffset + 6200, enemy.EnemyGroup, MovableBattery1, 
				[0, None, 6+256, 200-128, 60,
					[[11*8, 0, 0.0, -1.0], [100*8, 0, -1.0, 0.0]]
				], 48, 3
			],
			[baseOffset + 6400, enemy.EnemyGroup, MovableBattery1, 
				[0, None, 6+256, 170-128, 60,
					[[100*8, 0, 0.0, 1.0]]
				], 48, 3
			],
			[baseOffset + 6500, enemy.EnemyGroup, MovableBattery1, 
				[0, None, 30+256, 170-128, 60,
					[[11*8, 0, 0.0, 1.0], [100*8, 0, -1.0, 0.0]]
				], 48, 3
			],
			[baseOffset + 6550, enemy.EnemyGroup, MovableBattery1, 
				[0, None, 30+256, 200-128, 60,
					[[11*8, 0, 0.0, -1.0], [100*8, 0, -1.0, 0.0]]
				], 48, 3
			],
			[baseOffset + 6600, enemy.EnemyGroup, MovableBattery1, 
				[0, None, 38+256, 170-128, 60,
					[[11*8, 0, 0.0, 1.0], [100*8, 0, -1.0, 0.0]]
				], 48, 3
			],
			[baseOffset + 6650, enemy.EnemyGroup, MovableBattery1, 
				[0, None, 38+256, 200-128, 60,
					[[11*8, 0, 0.0, -1.0], [100*8, 0, -1.0, 0.0]]
				], 48, 3
			],
			[baseOffset + 7200, bossWarehouse.BossWarehouse],
		]

	@classmethod
	def getStory3(cls):
		return [ \
			[3730+128, boss3.Boss3],		\
		]

	@classmethod
	def getStory4(cls):
		return [ \
			[200, enemy.Fan1aGroup, 12],
			[240, enemy.RollingFighter1Group, 120, 15, 4],		\
			[400, enemy.Fan1aGroup, 12],
			[430, enemy.RollingFighter1Group, 30, 15, 4],		\
			[500, enemy.RollingFighter1Group, 120, 15, 4],		\
			[600, enemy.RollingFighter1Group, 30, 15, 4],		\
			[1712, enemy.Fan1bLauncher, 76, 48, 48, 20],	\
			#[1712, enemy.Fan1bLauncher, 78, 22, 16, 20],	\
			[2500, enemy.RollingFighter1Group, 120, 15, 4],		\
			[3300, enemy.RollingFighter1Group, 30, 15, 4],		\
			[4230 +512, boss4.Boss4, 0, 0],		\
		]

	@classmethod
	def getStoryFactory(cls):
		return [ \
			[1200, enemy.RollingFighter1Group, 42, 15, 4],		\
			[1300, enemy.RollingFighter1Group, 58, 15, 4],		\
			[2030, enemy.RollingFighter1Group, 42, 15, 4],		\
			[2100, enemy.RollingFighter1Group, 58, 15, 4],		\
			[2200, enemy.RollingFighter1Group, 42, 15, 4],		\
			[3200, enemy.RollingFighter1Group, 32, 15, 4],		\
			[3230, enemy.RollingFighter1Group, 100, 15, 4],		\
			[3260, enemy.RollingFighter1Group, 120, 15, 4],		\
			[3600, enemy.RollingFighter1Group, 42, 15, 4],		\
			[3660, enemy.RollingFighter1Group, 80, 15, 4],		\
			[4500, enemy.Jumper1, 256, 20, 0.05],		\
			[4530, enemy.Jumper1, 256, 30, 0.05],		\
			[4600, enemy.Jumper1, 256, 20, 0.05],		\
			[4630, enemy.Jumper1, 256, 30, 0.05],		\
			[6700, enemyOthers.ArrowOnScreen, 120, 50, 0, "WARNING!", 180],
			[6850, bossFactory.BossFactory, 0, 0],		\
		]

	@classmethod
	def getStoryFire(cls):
		return [
			[200, enemyFighter.FireBird1Group, 256, 30, 20, 3, 20],
			[300, enemyFighter.FireBird1Group, 256, 80, 20, 3, 20],
			[300, enemyCreature.FireWorm1, 240, 230, 270,
				[
					[90, CountMover.MOVE, 0.0, -1.0],
					[90, CountMover.ROTATE_DEG, 270, -1.0, 1.0],
					[90, CountMover.ROTATE_DEG, 270-90, 1.0, 1.0],
					[360, CountMover.MOVE, 0.0, -1.0],
				],
				None
			],
			[500, enemyFighter.FireBird1Group, 256, 40, 20, 3, 20],

			[600, enemyFighter.FireBird1Group, 256, 90, 20, 3, 20],
			
			[700, enemyFighter.FireBird1Group, 256, 80, 20, 3, -20],

			[800, enemyFighter.FireBird1, 256, 40],
			[820, enemyFighter.FireBird1, 256, 60],

			[900, enemyFighter.FireBird1Group, 256, 40, 20, 3, 20],

			[1100, enemyFighter.FireBird1, 256, 60],
			[1120, enemyFighter.FireBird1, 256, 80],

			[1200, enemyFighter.FireBird1, 256, 40],
			[1220, enemyFighter.FireBird1, 256, 60],
			[1280, enemyFighter.FireBird1, 256, 60],
			[1300, enemyFighter.FireBird1, 256, 80],
			[1500, enemyFighter.FireBird1, 256, 40],
			[1520, enemyFighter.FireBird1, 256, 60],
			[1530, enemyCreature.FireWorm1, 260, -30, 90,
				[
					[90, CountMover.MOVE, 0.0, 1.0],
					[45, CountMover.ROTATE_DEG, 90, 1.0, 1.0],
					[45, CountMover.ROTATE_DEG, 90+45, -1.0, 1.0],
					[360, CountMover.MOVE, 0.0, 1.0],
				],
				None
			],
			[1700, enemyFighter.FireBird1, 256, 40],
			[1720, enemyFighter.FireBird1, 256, 60],
			[2200, enemyCreature.FireWorm1, 170, 230, 270,
				[
					[90, CountMover.MOVE, 0.0, -1.0],
					[90, CountMover.ROTATE_DEG, 270, 1.0, 1.0],
					[150, CountMover.MOVE, 1.0, 0.0],
					[90, CountMover.ROTATE_DEG, 0, 1.0, 1.0],
					[360, CountMover.MOVE, 0.0, 1.0],
				],
				None
			],
			[2600, enemyFighter.FireBird1Group, 256, 40, 20, 3, 20],
			[2800, enemyFighter.FireBird1Group, 256, 100, 20, 3, -20],
			[2960, enemyCreature.FireWorm1, 280, -30, 90,
				[
					[90, CountMover.MOVE, 0.0, 1.0],
					[90, 8, 90, 1.0, 1.0],
					[400, CountMover.MOVE, -1.0, 0.0],
				], None
			],
			[3000, enemyFighter.FireBird1, 256, 40],
			[3020, enemyFighter.FireBird1, 256, 60],
			[3100, enemyFighter.FireBird1Group, 256, 100, 20, 3, -20],
			[3150, enemyCreature.FireWorm1, 280, 230, 270,
				[
					[90, CountMover.MOVE, 0.0, -1.0],
					[90, 8, 270, -1.0, 1.0],
					[400, CountMover.MOVE, -1.0, 0.0],
				], None
			],
			[3250, enemyFighter.FireBird1Group, 256, 40, 20, 3, 30],
			[3400, enemyFighter.FireBird1, 256, 80],
			[3420, enemyFighter.FireBird1, 256, 60],
			[3460, enemyFighter.FireBird1, 256, 120],
			[3520, enemyFighter.FireBird1, 256, 80],
			[3720, enemyFighter.FireBird1, 256, 40],
			[3740, enemyFighter.FireBird1, 256, 80],
			[3760, enemyOthers.Prominence1Appear, 256, 200, 1, 1],
			# [3740, enemyCreature.FireWorm1, 300, 230, 225,
			# 	[
			# 		[90, CountMover.MOVE, -0.7, -0.7],
			# 		[90, 8, 225, 1.0, 1.0],
			# 		[400, CountMover.MOVE, 0.7, -0.7],
			# 	],
			# 	[
			# 		[90, 0],
			# 		[90, 1],
			# 		[0, 100]
			# 	]
			# ],
			[3760, enemyFighter.FireBird1, 256, 80],
			[3780, enemyFighter.FireBird1, 256, 60],
			[3800, enemyFighter.FireBird1, 256, 120],

			[3800, enemyFighter.FireBird1, 256, 40],
			[3820, enemyFighter.FireBird1, 256, 80],
			[3880, enemyOthers.Prominence1Appear, 256, 0, -1, -1],
			[4000, enemyOthers.Prominence1Appear, 380, 200, -1, 1],
			[4100, enemyFighter.FireBird1Group, 256, 40, 20, 3, 30],
			[4200, enemyFighter.FireBird1, 256, 80],
			[4220, enemyFighter.FireBird1, 256, 60],
			[4400, enemyOthers.Prominence1Appear, 256, 0, -1, -1],
			[4500, enemyFighter.FireBird1Group, 256, 70, 20, 3, 20],
			# [4250, enemyCreature.FireWorm1, 300, -30, 135,
			# 	[
			# 		[90, CountMover.MOVE, -0.7, 0.7],
			# 		[90, 8, 135, -1.0, 1.0],
			# 		[400, CountMover.MOVE, 0.7, 0.7],
			# 	],
			# 	[
			# 		[90, 0],
			# 		[90, 1],
			# 		[0, 100]
			# 	]
			# ],
			[4600, enemyFighter.FireBird1Group, 256, 100, 20, 3, -20],
			[4700, enemyFighter.FireBird1Group, 256, 60, 20, 3, 20],
			[4800, enemyFighter.FireBird1Group, 256, 40, 20, 3, 20],

			[4900, enemyFighter.FireBird1Group, 256, 100, 20, 3, -20],

			[5300, enemyFighter.FireBird1Group, 256, 30, 20, 3, 20],
			
			[5370, enemyFighter.FireBird1Group, 256, 100, 20, 3, 20],
			
			[6000, bossFire.BossFire, 240, 230, 270,
				[
					[90, CountMover.MOVE, 0.0, -1.0],
					[90, CountMover.ROTATE_DEG, 270, -1.0, 1.0],
					[90, CountMover.ROTATE_DEG, 270-90, 1.0, 1.0],
					[360, CountMover.MOVE, 0.0, -1.0],
				],
				None
			],
		]

	@classmethod
	def getStoryLast(cls):
		baseOffset = 1200
		return [ \
			[150, enemy.Fan1Group, 8, 10, 6, True],		\
			#[200, enemy.EnemyGroup, enemy.Fan1, [0, None, 256, 100], 10, 5],	\
			[270, enemy.Fan1Group, 170, 10, 6, True],		\
			[330, enemy.Fan1Group, 8, 10, 6],		\
			[370, enemy.Fighter2, 256, 120, 230, -1],	\
			[400, enemy.Fighter2, 256, 30, 190, 1],	\
			[400, enemy.Fan1Group, 170, 10, 6],		\
			[520, enemy.Fighter2, 256, 20, 190, 1],	\
			[580, enemy.Fighter2, 256, 150, 190, -1],	\
			#[700, boss.MiddleBoss1, 256, 50],		\
			[800, enemy.BattleShip1, 256+64, 60, False, [
				[90, 0, -1.0, 0.0],[330, 0, -1.0, 0.25],[600, 0, -1.0,0.0]
				], 0, -1],		\
			[1000, enemy.EnemyGroup, enemy.Fighter3, 
				[
					0, None, 256, 20,
					[
						[40, 0, -3.0, 0.0],[30, 0, -3.0, 0.5],[600, 0, -3.0,0.0]
					], 30
				], 15, 5],	\
			[1300, enemy.EnemyGroup, enemy.Fighter3, 
				[
					0, None, 256, 90,
					[
						[40, 0, -3.0, 0.0],[30, 0, -3.0, -0.5],[600, 0, -3.0,0.0]
					], 30
				], 15, 5],	\
			[1300, enemy.BattleShip1, 256+32, 0, False, [
				[150, 0, -1.0, 0.0],[210, 0, -1.0, -0.25],[180, 0, -1.0,0.0],[180, 0, -1.0,0.25],[600, 0, 0-1.0,0.0]
				], 0, 330],		\
			[1500, enemy.EnemyGroup, enemy.Fighter3, 
				[
					0, None, 256, 90,
					[
						[40, 0, -3.0, 0.0],[30, 0, -3.0, -0.5],[600, 0, -3.0,0.0]
					], 30
				], 15, 5],	\
			[1650, enemy.EnemyGroup, enemy.Fighter3, 
			[
				0, None, 256, 130,
				[
					[30, 0, -3.0, 0.0],[30, 0, -3.0, 0.75],[600, 0, -3.0,0.0]
				], 30
			], 15, 5],	\
			#[1500, enemy.Fighter3, 256, 60, [
			#	[90, 0, -3.0, 0.0],[330, 0, -3.0, 0.25],[600, 0, -3.0,0.0]
			#	]],		\
			# ３隻目
			[1700, enemy.BattleShip1, 256, 160, False, [
				[150, 0, -1.0, 0.0],[210, 0, -1.0, -0.25],[150, 0, -1.0,0.0],[210, 0, -1.0,0.25],[600, 0, -1.0,0.0]
				], 180, -1],		\
			[2000, enemy.EnemyGroup, enemy.Fighter3, 
			[
				0, None, 256, 10,
				[
					[30, 0, -3.0, 0.0],[30, 0, -3.0, 0.75],[600, 0, -3.0,0.0]
				], 20
			], 15, 5],	\
			[2100, enemy.EnemyGroup, enemy.Fighter3, 
			[
				0, None, 256, 100,
				[
					[30, 0, -3.0, 0.0],[30, 0, -3.0, -1.0],[600, 0, -3.0,0.0]
				], 20
			], 15, 5],	\
			[2300, enemy.EnemyGroup, enemy.Fighter3, 
			[
				0, None, 256, 120,
				[
					[30, 0, -3.0, 0.0],[30, 0, -3.0, -0.75],[600, 0, -3.0,0.0]
				], 20
			], 15, 5],	\
			# 赤い艦
			[2400, enemy.BattleShip1, 256 +32, 80, True, [
				[90, 0, -2.0, 0.0],[120, 0, -0.5, 0.0],[210, 0, -1.0, 0.25],[150, 0, -1.0,0.0],[210, 0, -1.0,0.25],[600, 0, -1.0,0.0]
				], 0, -1],		\
			[2600, enemy.EnemyGroup, enemy.Fighter3, 
			[
				0, None, 256, 10,
				[
					[30, 0, -3.0, 0.0],[30, 0, -3.0, 0.75],[600, 0, -3.0,0.0]
				], 15
			], 15, 5],	\
			[2100 +baseOffset, enemy.Fighter2, 256, 30, 190, 1],	\
			[2120 +baseOffset, enemy.Fighter2, 256, 120, 230, -1],	\
			[2260 +baseOffset, enemy.Walker1, 256, 266],		\
			[2380 +baseOffset, enemy.Tank1, 256, 144, 0, 0],	\
			[2400 +baseOffset, enemy.Tank1, 256, 24, 1, 0],	\
			[2450 +baseOffset, enemy.Tank1, 256, 144, 0, 0],	\
			[2520 +baseOffset, enemy.Tank1, 256, 24, 1, 0],	\
			[2630 +baseOffset, enemy.Tank1, -24, 144, 0, 1],	\
			[2650 +baseOffset, enemy.Tank1, -24, 24, 1, 1],	\
			[2800 +baseOffset, enemy.Tank1, -24, 144, 0, 2],	\
			[2830 +baseOffset, enemy.Tank1, -24, 24, 1, 2],	\
			[2900 +baseOffset, enemy.Tank1, -24, 144, 0, 3],	\
			[2930 +baseOffset, enemy.Tank1, -24, 24, 1, 3],	\
			[3100 +baseOffset, enemy.Tank1, -24, 144, 0, 3],	\
			[3130 +baseOffset, enemy.Tank1, -24, 24, 1, 3],	\
			[3500 +baseOffset, enemy.Fighter2, 256, 120, 230, -1],	\
			[3520 +baseOffset, enemy.Fighter2, 256, 30, 190, 1],	\
			[3700 +baseOffset, enemy.Fighter2, 256, 130, 220, -1],	\
			[3720 +baseOffset, enemy.Fighter2, 256, 40, 180, 1],	\

			[4450 +baseOffset, enemy.Fighter2, 256, 30, 190, 1],	\
			[4480 +baseOffset, enemy.Fighter2, 256, 120, 230, -1],	\
			[4520 +baseOffset, enemy.Fighter2, 256, 120, 160, -1],	\
			[4550 +baseOffset, enemy.Fighter2, 256, 30, 130, 1],	\
		#	[4700, enemy.Fighter2, 256, 30, 160, 1],	\
		#	[4730, enemy.Fighter2, 256, 120, 230, -1],	\

			[6000 +baseOffset, enemy.Spider1, 300, 64.5],		\
			[6200 +baseOffset, enemy.Tank1, 256, 152, 0, 0],	\
			[6260 +baseOffset, enemy.Tank1, 256, 16, 1, 0],	\
			[6320 +baseOffset, enemyOthers.ArrowOnMap, 259, 46, 1, "HIDE", 180],
			[6520 +baseOffset, enemy.Tank1, -24, 152, 0, 2],	\
			[6600 +baseOffset, enemy.Tank1, -24, 16, 1, 2],	\
			[6700 +baseOffset, enemy.Tank1, 256, 152, 0, 0],	\
			[6750 +baseOffset, enemy.Tank1, -24, 16, 1, 3],	\
			[6800 +baseOffset, enemy.Tank1, -24, 16, 1, 2],	\
			[6900 +baseOffset, enemyOthers.ArrowOnMap, 256 +39, 154-128, 0, "HIDE", 180],
			[7000 +baseOffset, enemy.Tank1, 256, 16, 1, 0],	\
			[7200 +baseOffset, enemy.Tank1, -24, 152, 0, 2],	\
			[7300 +baseOffset, enemy.Tank1, -24, 16, 1, 3],	\
			[7400 +baseOffset, enemy.Tank1, 256, 16, 1, 0],	\
			[7500 +baseOffset, enemy.Tank1, -24, 16, 1, 3],	\
			[8400 +baseOffset, bossLast.BossLast1],	\
		]

	@classmethod
	def getStoryLabyrinth(cls):
		return [
			[600, enemy.Fan1cLauncher, 26, 49, 6, 20,
				[
					[30, 0, 0.0, -2.0], [300, 0, -2.0, 0.0]
				],
			],
			[1100, enemy.Fan1cLauncher, 40, 49, 6, 20,
				[
					[45, 0, 0.0, -2.0], [300, 0, -2.0, 0.0]
				],
			],
			[1300, enemy.Fan1cLauncher, 62, 20, 20, 20,
				[
					[74, 0, 0.0, 2.0], [300, 0, -2.0, 0.0]
				],
			],
			[1550, enemy.Fan1cLauncher, 81, 49, 6, 20,
				[
					[45, 0, 0.0, -2.0], [300, 0, -2.0, 0.0]
				],
			],
			[1700, enemy.Fan1cLauncher, 81, 20, 20, 20,
				[
					[74, 0, 0.0, 2.0], [300, 0, -2.0, 0.0]
				],
			],
			[4600, enemy.Fan1cLauncher, 206, 84, 6, 20,
				[
					[64, 0, 0.0, 2.0], [300, 0, -2.0, 0.0]
				],
			],
			[4720, enemy.Fan1cLauncher, 206, 111, 6, 20,
				[
					[32, 0, 0.0, -2.0], [300, 0, -2.0, 0.0]
				],
			],
			[4880, enemy.Fan1cLauncher, 224, 84, 6, 20,
				[
					[88, 0, 0.0, 2.0], [300, 0, -2.0, 0.0]
				],
			],
			[5200, enemy.Fan1cLauncher, 245, 84, 6, 20,
				[
					[32, 0, 0.0, 2.0], [300, 0, -2.0, 0.0]
				],
			],
			[5600, enemy.Fan1cLauncher, 256+8, 111, 6, 20,
				[
					[18, 0, 0.0, -2.0], [300, 0, -2.0, 0.0]
				],
			],
			[6000, enemy.Fan1cLauncher, 256+29, 84, 6, 20,
				[
					[32, 0, 0.0, 2.0], [300, 0, -2.0, 0.0]
				],
			],
			[6650, bossLabyrinth.BossLabyrinth, 0, 0 ],
		]

	@classmethod
	def getStoryBattileShip(cls):
		baseOffset = 0
		return [
			[baseOffset +100, enemy.EnemyGroup, enemy.Fighter3, 
				[
					0, None, 256, 20,
					[
						[40, 0, -3.0, 0.0],[30, 0, -3.0, 0.5],[600, 0, -3.0,0.0]
					], 30
				], 15, 5],
			[baseOffset +220, enemy.EnemyGroup, enemy.Fighter3, 
				[
					0, None, 256, 120,
					[
						[40, 0, -3.0, 0.0],[30, 0, -3.0, -0.5],[600, 0, -3.0,0.0]
					], 30
				], 15, 5],
			[baseOffset +300, enemy.EnemyGroup, enemy.Fighter3, 
				[
					0, None, 256, 50,
					[
						[60, 0, -3.0, 0.0],[30, 0, -3.0, 0.75],[600, 0, -3.0,0.0]
					], 30
				], 15, 5],
			[baseOffset +400, bossBattleShip.BossBattleShip],
			[baseOffset +480, enemy.EnemyGroup, enemy.Fighter3, 
				[
					0, None, 256, 140,
					[
						[40, 0, -3.0, 0.0],[30, 0, -3.0, -0.5],[600, 0, -3.0,0.0]
					], 30
				], 15, 5],
			[baseOffset +900, enemy.EnemyGroup, enemy.Fighter3, 
				[
					0, None, 256, 10,
					[
						[900, 0, -3.0, 0.0]
					], 30
				], 15, 5],
			[baseOffset +1020, enemy.EnemyGroup, enemy.Fighter3, 
				[
					0, None, 256, 10,
					[
						[900, 0, -3.0, 0.0]
					], 30
				], 15, 5],
			[baseOffset +2380, enemy.EnemyGroup, enemy.Fighter3, 
				[
					0, None, 256, 10,
					[
						[900, 0, -3.0, 0.0]
					], 30
				], 15, 5],
			[baseOffset +2700, enemy.EnemyGroup, enemy.Fighter3, 
				[
					0, None, 256, 100,
					[
						[90, 0, -3.0, -1.0], [900, 0, -3.0, 0.0]
					], 30
				], 15, 5],
			[baseOffset +2800, enemy.EnemyGroup, enemy.Fighter3, 
				[
					0, None, -24, 10,
					[
						[900, 0, 3.0, 0.0]
					], 30
				], 15, 5],
			[baseOffset +3200, enemy.EnemyGroup, enemy.Fighter3, 
				[
					0, None, 256, 120,
					[
						[90, 0, -3.0, 0.5], [900, 0, -3.0, 0.0]
					], 30
				], 15, 5],
			[baseOffset +3400, enemy.EnemyGroup, enemy.Fighter3, 
				[
					0, None, -24, 154,
					[
						[900, 0, 3.0, 0.0]
					], 30
				], 15, 5],
		]
	
	@classmethod
	def getStoryEnemyBase(cls):
		baseOffset = 1200
		return [
			[150, enemy.Fan1Group, 8, 10, 6, True],		\
			[270, enemy.Fan1Group, 170, 10, 6, True],		\
			[330, enemy.Fan1Group, 8, 10, 6],		\
			[370, enemyFighter.Fighter5, 120],
			[400, enemyFighter.Fighter5, 30],
			[400, enemy.Fan1Group, 170, 10, 6],		\
			[800, enemyOthers.BarrierWallV1, 2, 34, 2],
			[800, HorizonBattery1, 0, 31, [
					[40, CountMover.MOVE, 0.0, -2.0],
					[20, CountMover.STOP],
					[20, CountMover.MOVE, 0.0, 2.0],
					[10, CountMover.STOP],
					[10, CountMover.MOVE, 0.0, -2.0],
					[20, CountMover.STOP],
					[30, CountMover.MOVE, 0.0, 2.0],
					[10, CountMover.STOP],
				]
			],
			[800, HorizonBattery1, 0, 38, [
					[40, CountMover.MOVE, 0.0, 2.0],
					[10, CountMover.STOP],
					[20, CountMover.MOVE, 0.0, -2.0],
					[20, CountMover.STOP],
					[10, CountMover.MOVE, 0.0, 2.0],
					[10, CountMover.STOP],
					[30, CountMover.MOVE, 0.0, -2.0],
					[20, CountMover.STOP],
				]
			],
			[baseOffset+ 540, enemyArmored.Ducker1, 1],
			[baseOffset+ 570, enemyArmored.Ducker1, -1],
			[baseOffset+ 660, enemyArmored.Ducker1, 1],
			[baseOffset+ 690, enemyArmored.Ducker1, -1],
			[baseOffset+ 780, enemyArmored.Ducker1, 1],
			[baseOffset+ 810, enemyArmored.Ducker1, -1],
			[baseOffset+ 900, enemyArmored.Ducker1, 1],
			[baseOffset+ 930, enemyArmored.Ducker1, -1],
			[baseOffset+ 1000, enemyArmored.Ducker1, -1],
			[baseOffset+ 1040, enemyArmored.Ducker1, 1],
			[baseOffset+ 1100, enemyArmored.Ducker1, -1],
			[baseOffset+ 1170, enemyArmored.Ducker1, 1],
			[baseOffset+ 1200, enemyOthers.Lift2Appear, 115, 0, 1.0, 4000],
			[baseOffset+ 1200, enemyOthers.Lift2Appear, 154, 51, -1.0, 4800],
			[baseOffset+ 1170, enemyArmored.Ducker1, 1],
			[baseOffset+ 5800, enemyFighter.Fighter6, 13+256, 184-128,
				# 上から出てくる
				[
					[0, CountMover.SET_DEG, 270],
					[47, CountMover.MOVE, 0.0, 1.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[31, CountMover.MOVE, -1.0, 0.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[63, CountMover.MOVE, 0.0, 1.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[100, CountMover.MOVE, -1.0, 0.0],
				]
				],
			[baseOffset+ 5830, enemyFighter.Fighter6, 17+256, 212-128,
				# 下から出てくる
				[
					[0, CountMover.SET_DEG, 90],
					[47, CountMover.MOVE, 0.0, -1.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[31, CountMover.MOVE, 1.0, 0.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[63, CountMover.MOVE, 0.0, -1.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[256, CountMover.MOVE, -1.0, 0.0],
				]
				],
			[baseOffset+ 5890, enemyFighter.Fighter6, 13+256, 184-128,
				# 上から出てくる
				[
					[0, CountMover.SET_DEG, 270],
					[47, CountMover.MOVE, 0.0, 1.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[31, CountMover.MOVE, -1.0, 0.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[63, CountMover.MOVE, 0.0, 1.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[100, CountMover.MOVE, -1.0, 0.0],
				]
				],
			[baseOffset+ 5940, enemyFighter.Fighter6, 17+256, 212-128,
				# 下から出てくる
				[
					[0, CountMover.SET_DEG, 90],
					[47, CountMover.MOVE, 0.0, -1.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[31, CountMover.MOVE, 1.0, 0.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[63, CountMover.MOVE, 0.0, -1.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[256, CountMover.MOVE, -1.0, 0.0],
				]
				],
			[baseOffset+ 6060, enemyFighter.Fighter6, 17+256, 212-128,
				# 下から出てくる
				[
					[0, CountMover.SET_DEG, 90],
					[47, CountMover.MOVE, 0.0, -1.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[95, CountMover.MOVE, -1.0, 0.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[63, CountMover.MOVE, 0.0, -1.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[256, CountMover.MOVE, -1.0, 0.0],
				]
				],
			[baseOffset+ 6090, enemyFighter.Fighter6, 37+256, 184-128,
				# 上から出てくる
				[
					[0, CountMover.SET_DEG, 270],
					[47, CountMover.MOVE, 0.0, 1.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[63, CountMover.MOVE, -1.0, 0.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[31, CountMover.MOVE, 0.0, 1.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[63, CountMover.MOVE, -1.0, 0.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[31, CountMover.MOVE, 0.0, -1.0],
				]
				],
			[baseOffset+ 6120, enemyFighter.Fighter6, 17+256, 212-128,
				# 下から出てくる
				[
					[0, CountMover.SET_DEG, 90],
					[47, CountMover.MOVE, 0.0, -1.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[31, CountMover.MOVE, 1.0, 0.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[63, CountMover.MOVE, 0.0, -1.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[256, CountMover.MOVE, -1.0, 0.0],
				]
				],
			[baseOffset+ 6180, enemyFighter.Fighter6, 37+256, 184-128,
				# 上から出てくる
				[
					[0, CountMover.SET_DEG, 270],
					[47, CountMover.MOVE, 0.0, 1.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[63, CountMover.MOVE, -1.0, 0.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[31, CountMover.MOVE, 0.0, 1.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[63, CountMover.MOVE, -1.0, 0.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[31, CountMover.MOVE, 0.0, -1.0],
				]
				],
			[baseOffset+ 6220, enemyFighter.Fighter6, 41+256, 212-128,
				# 下から出てくる
				[
					[0, CountMover.SET_DEG, 90],
					[47, CountMover.MOVE, 0.0, -1.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[256, CountMover.MOVE, -1.0, 0.0],
				]
				],
			[baseOffset+ 6300, enemyFighter.Fighter6, 41+256, 212-128,
				# 下から出てくる
				[
					[0, CountMover.SET_DEG, 90],
					[111, CountMover.MOVE, 0.0, -1.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[256, CountMover.MOVE, -1.0, 0.0],
				]
				],
			[baseOffset+ 6300, enemyFighter.Fighter6, 37+256, 184-128,
				# 上から出てくる
				[
					[0, CountMover.SET_DEG, 270],
					[47, CountMover.MOVE, 0.0, 1.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[31, CountMover.MOVE, 1.0, 0.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[63, CountMover.MOVE, 0.0, 1.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[95, CountMover.MOVE, -1.0, 0.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
				]
				],
			[baseOffset+ 6300, enemyFighter.Fighter6, 49+256, 184-128,
				# 上から出てくる
				[
					[0, CountMover.SET_DEG, 270],
					[175, CountMover.MOVE, 0.0, 1.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[256, CountMover.MOVE, -1.0, 0.0],
				]
				],
			[baseOffset+ 6450, enemyFighter.Fighter6, 41+256, 212-128,
				# 下から出てくる
				[
					[0, CountMover.SET_DEG, 90],
					[47, CountMover.MOVE, 0.0, -1.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[95, CountMover.MOVE, -1.0, 0.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[63, CountMover.MOVE, 0.0, -1.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[256, CountMover.MOVE, -1.0, 0.0],
				]
				],
			[baseOffset+ 6480, enemyFighter.Fighter6, 49+256, 184-128,
				# 上から出てくる
				[
					[0, CountMover.SET_DEG, 270],
					[175, CountMover.MOVE, 0.0, 1.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[256, CountMover.MOVE, -1.0, 0.0],
				]
				],
			[baseOffset+ 6800, enemyFighter.Fighter6, 57+256, 184-128,
				# 上から出てくる
				[
					[0, CountMover.SET_DEG, 270],
					[47, CountMover.MOVE, 0.0, 1.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[63, CountMover.MOVE, -1.0, 0.0],
					[19, CountMover.ROTATE_DEG2, 4.5, 0.0],
					[175, CountMover.MOVE, 0.0, 1.0],
					[19, CountMover.ROTATE_DEG2, -4.5, 0.0],
					[256, CountMover.MOVE, -1.0, 0.0],
				]
				],
			[baseOffset+ 7000, enemyArmored.CylinderCrab2],
		]
