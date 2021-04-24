


class ObjMgr:
	myShip = None
	# 自機弾
	shots = []
	shotGroups = []
	missleGroups = []
	# マルチプル用
	mshotGroupsList = []
	mmissileGroupsList = []

	# 敵
	objs = []

	nextDrawMap = None
	drawMap = None


	@classmethod
	def init(cls, multipleCount):
		cls.myShip = None
		cls.shots.clear()
		cls.shotGroups.clear()
		cls.missleGroups.clear()
		cls.mshotGroupsList.clear()
		cls.mmissileGroupsList.clear()
		for dummy in range(multipleCount):
			cls.mshotGroupsList.append([])
			cls.mmissileGroupsList.append([])
		
		cls.objs.clear()
		cls.nextDrawMap = None
		cls.drawMap = None

	@classmethod
	def addObj(cls, obj):
		cls.objs.append(obj)
		return obj

	@classmethod
	def setDrawMap(cls, obj):
		cls.nextDrawMap = obj

	@classmethod
	def removeDrawMap(cls):
		cls.drawMap = None

	@classmethod
	def updateDrawMap0(cls, skip):
		if cls.nextDrawMap != None:
			cls.nextDrawMap.init()
			cls.drawMap = cls.nextDrawMap
			cls.nextDrawMap = None
		if cls.drawMap != None:
			cls.drawMap.update0(skip)

	@classmethod
	def updateDrawMap(cls, skip):
		if cls.drawMap != None:
			cls.drawMap.update(skip)

	@classmethod
	def drawDrawMapBackground(cls):
		if cls.drawMap != None:
			cls.drawMap.drawBackground()

	@classmethod
	def drawDrawMap(cls):
		if cls.drawMap != None:
			cls.drawMap.draw()

	@classmethod
	def drawDrawMap2(cls):
		if cls.drawMap != None:
			cls.drawMap.draw2()

	@classmethod
	def debugListObj(cls):
		for obj in cls.objs:
			print(obj)
