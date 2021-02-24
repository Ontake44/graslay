
import pyxel
import math
import random
import gcommon
import os
import json
import ranking

class RankingDispScene:
	LEFT_MARKER_X = 128 -8*4 -2
	RIGHT_MARKER_X = 128 +8*3 + 2
	MARKER_Y = 24
	EXIT_Y = 184
	colXList = [8, 56, 128, 208]
	colNameList = ["RANK", "NAME", "SCORE", "STAGE"]
	rankList = [" 1ST", " 2ND", " 3RD", " 4TH", " 5TH", " 6TH", " 7TH", " 8TH", " 9TH", "10TH"]
	def __init__(self):
		self.star_pos = 0
		self.menuPos = 0
		self.difficulty = gcommon.DIFFICULTY_NORMAL
		self.mouseManager = gcommon.MouseManager()
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
			gcommon.sound(gcommon.SOUND_MENUMOVE)
			self.menuPos = 0
		if gcommon.checkDownP():
			gcommon.sound(gcommon.SOUND_MENUMOVE)
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
				gcommon.sound(gcommon.SOUND_MENUMOVE)
				self.difficulty = gcommon.DIFFICULTY_EASY
			elif gcommon.checkRightP() or (gcommon.checkShotKeyP() and n == 1):
				gcommon.sound(gcommon.SOUND_MENUMOVE)
				self.difficulty = gcommon.DIFFICULTY_NORMAL

		elif self.menuPos == 1:
			if gcommon.checkShotKeyRectP(self.menuRects[1]):
				gcommon.sound(gcommon.SOUND_MENUMOVE)
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
		
		leftMarker = (self.difficulty == gcommon.DIFFICULTY_NORMAL)
		gcommon.drawLeftMarker(__class__.LEFT_MARKER_X, __class__.MARKER_Y, leftMarker)
		gcommon.drawRightMarker(__class__.RIGHT_MARKER_X, __class__.MARKER_Y, not leftMarker)

		# カラムヘッダー
		pyxel.pal(7, 12)
		for i, x in enumerate(__class__.colXList):
			gcommon.showText(x, 40, __class__.colNameList[i])
		pyxel.pal()

		cols = __class__.colXList
		if self.difficulty == gcommon.DIFFICULTY_EASY:
			rankingList = self.rakingManager.easyRanking
		else:
			rankingList = self.rakingManager.normalRanking
		if rankingList == None:
			rankingList = []
		sy = 56
		dy = 12
		for i in range(10):
			name = "---"
			score = "--------"
			stage = "-"
			if i < len(rankingList):
				name = rankingList[i].name
				score = str(rankingList[i].score).rjust(8)
				stage = str(rankingList[i].stage)
			gcommon.showText(cols[0], sy + i* dy, __class__.rankList[i])
			gcommon.showText(cols[1]+8, sy + i* dy, name)
			gcommon.showText(cols[2], sy + i* dy, score)
			gcommon.showText(cols[3]+16, sy + i* dy, stage)

		gcommon.setBrightness1()
		rect = self.menuRects[self.menuPos]
		pyxel.blt(rect.left, rect.top, 4, rect.left, rect.top, rect.getWidth(), rect.getHeight())
		pyxel.pal()

		# マウスカーソル
		if self.mouseManager.visible:
			gcommon.drawMenuCursor()

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


class RankingItem:
	def __init__(self):
		self.rank = 0
		self.name = ""
		self.score = 0
		self.stage = 0		# クリアすると-1

class RankingManager:
	RECORD_FILE = ".graslay_ranking"
	def __init__(self):
		self.normalRanking = []
		self.easyRanking = []

	def load(self):
		jsonFile = None
		try:
			recordsPath = os.path.join(os.path.expanduser("~"), RankingManager.RECORD_FILE)
			jsonFile = open(recordsPath, "r")
			jsonData = json.load(jsonFile)

			if "normal" in jsonData:
				print("find normal")
				self.normalRanking = self.getRanking(jsonData["normal"])

				for rec in self.normalRanking:
					print("rank :" + rec.name)
			if "easy" in jsonData:
				print("find normal")
				self.easyRanking = self.getRanking(jsonData["easy"])
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
		#json_data["ranking"] = ranking


	def getRankingJsonList(self, rankingList):
		jsonList = []
		for item in rankingList:
			dic = {"rank": item.rank, "name": item.name, "score": item.score, "stage": item.stage}
			jsonList.append(dic)
		return jsonList

	# ranking : jsonデータ
	def getRanking(self, ranking):
		rankingList = []
		for r in ranking:
			item = RankingItem()
			if "rank" in r:
				item.rank = r["rank"]
			if "name" in r:
				item.name = r["name"]
			if "score" in r:
				item.score = r["score"]
			if "stage" in r:
				item.stage = r["stage"]
			print("rank : " + str(item.rank))
			print("name : " + item.name)
			rankingList.append(item)
		return rankingList

