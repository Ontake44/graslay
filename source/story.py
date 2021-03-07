
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

class Story:
	@classmethod
	def getStory1(cls):
		return [
			[150, enemy.Fan1Group, 8, 10, 6],	
			[270, enemy.Fan1Group, 170, 10, 6],	
			#[360, enemy.Fan1Group, 8, 10, 6],	
			[360, enemy.Fan1aGroup, 12],
			#[450, enemy.Fan1Group, 170, 10, 6],
			[450, enemy.Fan1aGroup, 12],
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
			[4160, enemy.WhereAppear, gcommon.GameSession.isNormalOrMore(), enemy.Jumper1, [-16, 50, 0.1]],
			[4190, enemy.WhereAppear, gcommon.GameSession.isNormalOrMore(), enemy.Jumper1, [-16, 50, 0.1]],
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
			[260, enemy.WhereAppear, gcommon.GameSession.isNormalOrMore(), enemy.Cell1Group1, [-16, 60, 0]],		\
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
			[5000, enemy.WhereAppear, gcommon.GameSession.isNormalOrMore(), enemy.Cell1Group1, [-256, 20, 0]],

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
			[6850, bossFactory.BossFactory, 0, 0],		\
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
			[6520 +baseOffset, enemy.Tank1, -24, 152, 0, 2],	\
			[6600 +baseOffset, enemy.Tank1, -24, 16, 1, 2],	\
			[6700 +baseOffset, enemy.Tank1, 256, 152, 0, 0],	\
			[6750 +baseOffset, enemy.Tank1, -24, 16, 1, 3],	\
			[6800 +baseOffset, enemy.Tank1, -24, 16, 1, 2],	\
			[7000 +baseOffset, enemy.Tank1, 256, 16, 1, 0],	\
			[7200 +baseOffset, enemy.Tank1, -24, 152, 0, 2],	\
			[7300 +baseOffset, enemy.Tank1, -24, 16, 1, 3],	\
			[7400 +baseOffset, enemy.Tank1, 256, 16, 1, 0],	\
			[7500 +baseOffset, enemy.Tank1, -24, 16, 1, 3],	\
			[8400 +baseOffset, bossLast.BossLast1],	\
		]
