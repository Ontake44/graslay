import gcommon
import pygame.mixer
from settings import Defaults
from settings import Settings
from audio import BGM

class GameSession:
	difficulty = gcommon.DIFFICULTY_NORMAL
	difficutlyRate = 1.0
	playerStock = 0
	stage = 0
	score = 0
	scoreCheck = 0
	weaponType = gcommon.WeaponType.TYPE_A
	scoreFirstExtend = False
	credits = 0
	gameMode = gcommon.GAMEMODE_NORMAL
	weaponSave = gcommon.WEAPON_STRAIGHT
	enemy_shot_rate = gcommon.ENEMY_SHOT_RATE_NORMAL
	powerRate = gcommon.POWER_RATE_NORMAL
	multipleCount = Defaults.INIT_MULTIPLE_COUNT

	@classmethod
	def initNormal(cls, difficulty):
		__class__.init(difficulty, Defaults.INIT_PLAYER_STOCK, gcommon.GAMEMODE_NORMAL, "1A", Settings.credits)

	@classmethod
	def init(cls, difficulty, playerStock, gameMode, stage, credits):
		cls.difficulty = difficulty
		__class__.playerStock = playerStock
		__class__.score = 0
		__class__.scoreCheck = 0
		__class__.scoreFirstExtend = False
		__class__.stage = stage

		__class__.gameMode = gameMode
		__class__.credits = credits
		__class__.weaponSave = gcommon.WEAPON_STRAIGHT
		if __class__.difficulty == gcommon.DIFFICULTY_EASY:
			# Easy
			__class__.powerRate = gcommon.POWER_RATE_EASY
			__class__.enemy_shot_rate = gcommon.ENEMY_SHOT_RATE_EASY
			__class__.difficutlyRate = gcommon.DIFFICULTY_RATE_EASY
		elif __class__.difficulty == gcommon.DIFFICULTY_NORMAL:
			# Normal
			__class__.powerRate = gcommon.POWER_RATE_NORMAL
			__class__.enemy_shot_rate = gcommon.ENEMY_SHOT_RATE_NORMAL
			__class__.difficutlyRate = gcommon.DIFFICULTY_RATE_NORMAL
		else:
			# Hard
			__class__.powerRate = gcommon.POWER_RATE_HARD
			__class__.enemy_shot_rate = gcommon.ENEMY_SHOT_RATE_HARD
			__class__.difficutlyRate = gcommon.DIFFICULTY_RATE_HARD

	@classmethod
	def isEasy(cls):
		return __class__.difficulty == gcommon.DIFFICULTY_EASY

	@classmethod
	def isNormal(cls):
		return __class__.difficulty == gcommon.DIFFICULTY_NORMAL

	@classmethod
	def isNormalOrMore(cls):
		return __class__.difficulty >= gcommon.DIFFICULTY_NORMAL

	# ノーマル以下
	@classmethod
	def isNormalOrLess(cls):
		return __class__.difficulty <= gcommon.DIFFICULTY_NORMAL

	@classmethod
	def isHard(cls):
		return __class__.difficulty == gcommon.DIFFICULTY_HARD
	
	@classmethod
	def addScore(cls, score):
		__class__.score += score
		__class__.scoreCheck += score
		if __class__.scoreFirstExtend == False and __class__.scoreCheck >= 20000:
			__class__.playerStock += 1
			__class__.scoreFirstExtend = True
			BGM.sound(gcommon.SOUND_EXTENDED, gcommon.SOUND_CH1)
			gcommon.debugPrint("First Extended")
		elif __class__.scoreCheck >= 50000:
			__class__.playerStock += 1
			__class__.scoreCheck = 0
			BGM.sound(gcommon.SOUND_EXTENDED, gcommon.SOUND_CH1)
			gcommon.debugPrint("Extended by 50000")

	@classmethod
	def addPlayerStock(cls):
		__class__.playerStock += 1
		BGM.sound(gcommon.SOUND_EXTENDED, gcommon.SOUND_CH1)

	# 
	@classmethod
	def execContinue(cls):
		__class__.credits -= 1
		__class__.playerStock = Defaults.INIT_PLAYER_STOCK -1
		__class__.score = 0
		__class__.scoreCheck = 0
		__class__.scoreFirstExtend = False

