
import pyxel
import math
import random
import gcommon
import os
import json
import ranking
from operator import itemgetter
from gameSession import GameSession
from audio import BGM
from mouseManager import MouseManager

# ランキング表示
class RankingDispScene:
	LEFT_MARKER_X = 128 -8*4 -2
	RIGHT_MARKER_X = 128 +8*3 + 2
	MARKER_Y = 24
	EXIT_Y = 184
	colXList = [8, 56, 128, 208]
	colNameList = ["RANK", "NAME", "SCORE", "STAGE"]
	rankList = [" 1ST", " 2ND", " 3RD", " 4TH", " 5TH", " 6TH", " 7TH", " 8TH", " 9TH", "10TH"]
	def __init__(self, exitTo):
		self.exitTo	= exitTo	# 0:タイトル 1:option
		self.star_pos = 0
		self.menuPos = 0
		self.difficulty = GameSession.difficulty
		self.mouseManager = MouseManager()
		self.markerRects = [
			gcommon.Rect.createWH(__class__.LEFT_MARKER_X, __class__.MARKER_Y, 8, 8),
			gcommon.Rect.createWH(__class__.RIGHT_MARKER_X, __class__.MARKER_Y, 8, 8)
		]
		self.exitRect = [
			gcommon.Rect.createWH(128 -8*2, __class__.EXIT_Y, 8*4, 8),
		]
		self.menuYList = (__class__.MARKER_Y, __class__.EXIT_Y)
		self.menuRects = [
			gcommon.Rect.create(64, __class__.MARKER_Y-2, 255 -64, __class__.MARKER_Y +10-1),
			gcommon.Rect.create(64, __class__.EXIT_Y-2, 255 -64, __class__.EXIT_Y +10-1)
		]

	def init(self):
		self.rakingManager = ranking.RankingManager()
		self.rakingManager.load()

	def update(self):
		self.star_pos -= 0.25
		if self.star_pos<0:
			self.star_pos += 200
		self.mouseManager.update()

		if gcommon.checkUpP():
			BGM.sound(gcommon.SOUND_MENUMOVE)
			self.menuPos = 0
		if gcommon.checkDownP():
			BGM.sound(gcommon.SOUND_MENUMOVE)
			self.menuPos = 1
		
		if self.mouseManager.visible:
			n = gcommon.checkMouseMenuPos(self.menuRects)
			if n != -1:
				self.menuPos = n
		if self.menuPos == 0:
			n = -1
			if self.mouseManager.visible:
				n = gcommon.checkMouseMenuPos(self.markerRects)
			if gcommon.checkLeftP() or (gcommon.checkShotKeyP() and n == 0):
				if self.difficulty > 0:
					BGM.sound(gcommon.SOUND_MENUMOVE)
					self.difficulty -= 1
			elif gcommon.checkRightP() or (gcommon.checkShotKeyP() and n == 1):
				if self.difficulty < 2:
					BGM.sound(gcommon.SOUND_MENUMOVE)
					self.difficulty += 1

		elif self.menuPos == 1:	# EXIT
			if gcommon.checkShotKeyRectP(self.menuRects[1]):
				BGM.sound(gcommon.SOUND_MENUMOVE)
				if self.exitTo == 0:
					gcommon.app.startTitle()
				else:
					gcommon.app.startOption()

	def draw(self):
		pyxel.cls(0)
		self.drawStar()

		gcommon.showTextHCenter(8, "SCORE RANKING")
		self.setOptionColor(0)
		gcommon.showTextHCenter(__class__.MARKER_Y, gcommon.difficultyText[self.difficulty])
		
		self.setOptionColor(1)
		gcommon.showTextHCenter(__class__.EXIT_Y, "EXIT")
		pyxel.pal()
		
		gcommon.drawLeftMarker(__class__.LEFT_MARKER_X, __class__.MARKER_Y, self.difficulty > 0)
		gcommon.drawRightMarker(__class__.RIGHT_MARKER_X, __class__.MARKER_Y, self.difficulty < 2)

		# カラムヘッダー
		pyxel.pal(7, 12)
		for i, x in enumerate(__class__.colXList):
			gcommon.showText(x, 40, __class__.colNameList[i])
		pyxel.pal()

		cols = __class__.colXList
		if self.difficulty == gcommon.DIFFICULTY_EASY:
			rankingList = self.rakingManager.easyRanking
		elif self.difficulty == gcommon.DIFFICULTY_NORMAL:
			rankingList = self.rakingManager.normalRanking
		else:
			rankingList = self.rakingManager.hardRanking
		if rankingList == None:
			rankingList = []
		sy = 56
		dy = 12
		for i in range(10):
			name = "---"
			score = "--------"
			stage = "  -"
			if i < len(rankingList):
				name = rankingList[i].name
				score = str(rankingList[i].score).rjust(8)
				if rankingList[i].stage == -1:
					stage = "CLEAR"
				else:
					stage = "  " + str(rankingList[i].stage)
			gcommon.showText(cols[0], sy + i* dy, __class__.rankList[i])
			gcommon.showText(cols[1]+8, sy + i* dy, name)
			gcommon.showText(cols[2], sy + i* dy, score)
			gcommon.showText(cols[3], sy + i* dy, stage)

		gcommon.setBrightness1()
		rect = self.menuRects[self.menuPos]
		pyxel.blt(rect.left, rect.top, 4, rect.left, rect.top, rect.getWidth(), rect.getHeight())
		pyxel.pal()

		# マウスカーソル
		if self.mouseManager.visible:
			self.mouseManager.drawMenuCursor()

	def setOptionColor(self, index):
		if index == self.menuPos:
			pyxel.pal()
		else:
			pyxel.pal(7, 12)

	def drawStar(self):
		for i in range(0,96):
			pyxel.pset(gcommon.star_ary[i][0], int(i*2 +self.star_pos) % 200, gcommon.star_ary[i][1])

	# ランキングに載るかどうかをチェック
	def checkRanking(self):
		return True

	def loadRanking(self):
		return False

# ネームエントリー
class EnterPlayerNameScene:
	allCharsList = ("ABCDEFGHIJKLM", "NOPQRSTUVWXYZ", "0123456789", " .-?!")
	allChars = allCharsList[0] + allCharsList[1] + allCharsList[2] + allCharsList[3]
	ALPHA_X = 16
	ALPHA_Y = 112
	def __init__(self):
		self.bgStarV = gcommon.BGStarV()
		self.mouseManager = MouseManager()
		self.markerRects = []
		for y, chars in enumerate(__class__.allCharsList):
			for i in range(len(chars)):
				rx = __class__.ALPHA_X -4 + i * 18
				ry = __class__.ALPHA_Y -4 + y * 18
				self.markerRects.append(gcommon.Rect.createWH(rx, ry, 16, 16))
		self.markerRects.append(gcommon.Rect.createWH(rx +18, ry, 16, 16))		# Back Space
		self.backSpaceIndex = len(self.markerRects) -1
		self.markerRects.append(gcommon.Rect.createWH(rx +18*2, ry, 24, 16))		# End
		self.endIndex = len(self.markerRects) -1
		self.rectIndex = 0
		self.cursorPos = 0
		self.name = ""

	def init(self):
		BGM.playOnce(BGM.RANKING)

	def update(self):
		self.bgStarV.update()
		self.mouseManager.update()
		if self.mouseManager.visible:
			n = gcommon.checkMouseMenuPos(self.markerRects)
			if n != -1:
				self.rectIndex = n
		else:
			if gcommon.checkLeftP():
				BGM.sound(gcommon.SOUND_MENUMOVE)
				self.rectIndex -= 1
				if self.rectIndex < 0:
					self.rectIndex = self.endIndex
			elif gcommon.checkRightP():
				BGM.sound(gcommon.SOUND_MENUMOVE)
				self.rectIndex += 1
				if self.rectIndex > self.endIndex:
					self.rectIndex = 0
			elif gcommon.checkUpP():
				BGM.sound(gcommon.SOUND_MENUMOVE)
				if self.rectIndex < 7:
					self.rectIndex = 26 + 10 + self.rectIndex
				elif self.rectIndex >= 7 and self.rectIndex < 13:
					self.rectIndex = self.endIndex
				elif self.rectIndex >= 13 and self.rectIndex < (26+10):		# アルファベット+数字
					self.rectIndex -= 13
				elif self.rectIndex >= (26+10) and self.rectIndex < (26+10+7):	# 記号+BS+End
					self.rectIndex -= 10
			elif gcommon.checkDownP():
				BGM.sound(gcommon.SOUND_MENUMOVE)
				if self.rectIndex >= 0 and self.rectIndex < 13:		# アルファベット１段目
					self.rectIndex += 13
				elif self.rectIndex >= 13 and self.rectIndex < (13+10):	# アルファベット２段目の途中
					self.rectIndex += 13
				elif self.rectIndex >= (13+10) and self.rectIndex < 26:	# アルファベット２段目の途中から２段目最後まで
					self.rectIndex = 26 + 10 -1
				elif self.rectIndex >= 26 and self.rectIndex < (26+7):
					self.rectIndex += 10
				elif self.rectIndex >= (26+7) and self.rectIndex < (26+10):
					self.rectIndex = 26 + 10 +7 -1
				else:
					self.rectIndex -= 26 + 10
			
		if gcommon.checkShotKeyP():
			BGM.sound(gcommon.SOUND_MENUMOVE)
			if self.cursorPos < 3 and self.rectIndex < self.backSpaceIndex:
				self.name += self.allChars[self.rectIndex]
				self.cursorPos += 1
			elif self.cursorPos > 0 and self.rectIndex == self.backSpaceIndex:
				self.name = self.name[:-1]
				self.cursorPos -= 1
			elif self.rectIndex == self.endIndex:
				self.addRecord()
				gcommon.app.startScoreRanking(0)
	

	def addRecord(self):
		rakingManager = ranking.RankingManager()
		rakingManager.load()
		rakingManager.addRecord(GameSession.difficulty, self.name, GameSession.score, GameSession.stage)
		rakingManager.save()

	def setOptionColor(self, index):
		if index == self.rectIndex:
			pyxel.pal()
		else:
			pyxel.pal(7, 12)
	
	def draw(self):
		pyxel.cls(0)
		self.bgStarV.draw()

		ty = 16
		gcommon.showTextHCenter(ty, "ENTER YOUR NAME")
		ty += 16

		gcommon.showTextHCenter(ty, "= " + gcommon.difficultyText[GameSession.difficulty] + " =")

		x0 = 32
		x1 = 128
		ty += 24
		gcommon.showText(x0, ty, "SCORE")
		gcommon.showText(x1, ty, str(GameSession.score).rjust(8, "0"))
		ty += 16

		gcommon.showText(x0, ty, "STAGE")
		stage = ""
		if GameSession.stage == -1:
			stage = "CLEAR"
		else:
			stage = "  " + str(GameSession.stage)
		gcommon.showText(x1, ty, stage)
		ty += 16

		gcommon.showText(x0, ty, "YOUR NAME")
		gcommon.showText(x1, ty, self.name)
		pyxel.rectb(x1 -4, ty-4, 8*3 + 8, 16, 5)

		pyxel.pal(7, 12)
		index = 0
		x0 = __class__.ALPHA_X = 16
		ty = __class__.ALPHA_Y
		for y, chars in enumerate(__class__.allCharsList):
			for i, c in enumerate(chars):
				self.setOptionColor(index)
				gcommon.showText(x0 + i*18, ty, str(c))
				index += 1
			ty += 18
		
		ty -= 18
		# BackSpace
		self.setOptionColor(index)
		pyxel.blt(x0 + 5 * 18, ty, 0, 208, 136, 8, 8, gcommon.TP_COLOR)
		index += 1
		
		# End
		self.setOptionColor(index)
		pyxel.blt(x0 + 6 * 18, ty, 0, 216, 136, 16, 8, gcommon.TP_COLOR)
		index += 1
		
		pyxel.pal()

		rect = self.markerRects[self.rectIndex]
		gcommon.setBrightness1()
		pyxel.blt(rect.left, rect.top, 4, rect.left, rect.top, rect.getWidth(), rect.getHeight())
		pyxel.pal()

		self.mouseManager.draw()

class RankingItem:
	def __init__(self):
		self.name = ""
		self.score = 0
		self.stage = 0		# クリアすると-1

class RankingManager:
	RECORD_FILE = ".graslay_ranking"
	def __init__(self):
		self.normalRanking = []
		self.easyRanking = []
		self.hardRanking = []

	def load(self):
		jsonFile = None
		try:
			recordsPath = os.path.join(os.path.expanduser("~"), RankingManager.RECORD_FILE)
			jsonFile = open(recordsPath, "r")
			jsonData = json.load(jsonFile)

			if "normal" in jsonData:
				self.normalRanking = self.getRanking(jsonData["normal"])
			if "easy" in jsonData:
				self.easyRanking = self.getRanking(jsonData["easy"])
			if "hard" in jsonData:
				self.hardRanking = self.getRanking(jsonData["hard"])
		except:
			pass
		finally:
			if jsonFile != None:
				try:
					jsonFile.close()
				except:
					pass
	
	def save(self):
		ranking = {}
		if self.normalRanking != None:
			ranking["normal"] = self.getRankingJsonList(self.normalRanking)
		if self.easyRanking != None:
			ranking["easy"] = self.getRankingJsonList(self.easyRanking)
		if self.hardRanking != None:
			ranking["hard"] = self.getRankingJsonList(self.hardRanking)
		#json_data["ranking"] = ranking
		try:
			settingsPath = os.path.join(os.path.expanduser("~"), RankingManager.RECORD_FILE)

			jsonFile = open(settingsPath, "w")
			json.dump(ranking, jsonFile)
			jsonFile.close()

		except:
			pass

	def inTop10(self, difficulty, score):
		ranking = None
		if difficulty == gcommon.DIFFICULTY_EASY:
			ranking = self.easyRanking
		elif difficulty == gcommon.DIFFICULTY_NORMAL:
			ranking = self.normalRanking
		else:
			ranking = self.hardRanking
		if ranking != None:
			if len(ranking) < 10:
				return True
			for item in ranking:
				if item.score < score:
					return True
			return False
		else:
			return True

	def addContinueRecord(self):
		self.load()
		self.addRecord(GameSession.difficulty, "=C=", GameSession.score, GameSession.stage)
		self.save()

	def addRecord(self, difficulty, name, score, stage):
		item = RankingItem()
		item.name = name
		item.score = score
		item.stage = stage
		if difficulty == gcommon.DIFFICULTY_EASY:
			ranking = self.easyRanking
		elif difficulty == gcommon.DIFFICULTY_NORMAL:
			ranking = self.normalRanking
		else:
			ranking = self.hardRanking
		ranking.append(item)
		ranking.sort(key=lambda i: i.score, reverse=True)
		if len(ranking) > 10:
			ranking.pop()

	def getRankingJsonList(self, rankingList):
		jsonList = []
		for item in rankingList:
			dic = {"name": item.name, "score": item.score, "stage": item.stage}
			jsonList.append(dic)
		return jsonList

	# ranking : jsonデータ
	def getRanking(self, ranking):
		rankingList = []
		for r in ranking:
			item = RankingItem()
			#if "rank" in r:
			#	item.rank = r["rank"]
			if "name" in r:
				item.name = r["name"]
			if "score" in r:
				item.score = r["score"]
			if "stage" in r:
				item.stage = r["stage"]
			#print("rank : " + str(item.rank))
			#print("name : " + item.name)
			rankingList.append(item)
		return rankingList

