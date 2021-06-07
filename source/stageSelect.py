
import pyxel
import stage
import gcommon
from audio import BGM
from drawing import Drawing

class StageSelect:
    nodeBaseX = 16
    nodeBaseY = 64
    # ステータスによって変える色のテーブル
    # 0 : 無効
    # 1 : まだ未達
    # 2 : クリア済み
    # 3 : 選択肢（選択中）
    # 4 : 選択肢（非選択）
    imageColorTable = [
        [[1, 0], [5, 1], [12, 5]],
        [[1, 0], [5, 1], [12, 5]],
        [],
        [[1, 1], [5, 8], [12, 14]],
        [[5, 2], [12, 2]],
    ]
    textColorTable = [
        [[7, 1]],
        [[7, 12]],
        [[5, 1]],
        [],
        [[7, 5],[5, 1]],
    ]

    @classmethod
    # node 描画するステージ(StateInfo)
    # currentStage 現在選択中のステージ(StateInfo)
    # selectableStageMap 選択可能なステージ(string, StateInfo)のマップ
    # cleaedMap クリアしたステージ文字列（stringのマップ）
    def drawNode(cls, node: stage.StageInfo, currentStage, selectableStageMap, clearedMap, highlight:bool):
        if node.drawFlag:
            return
        node.drawFlag = True
        # 0 : 無効
        # 1 : まだ未達
        # 2 : クリア済み
        # 3 : 選択肢（選択中）
        # 4 : 選択肢（非選択）
        status = 1
        # 状態種類
        #   無効（実装されてない）  enabled = False
        #   有効
        #     まだ未達
        #     クリア済
        #     選択肢  選択中／非選択
        if node == None or node.enabled == False:
            status = 0
        else:
            # 有効
            if node.stage in clearedMap:
                # クリア済みは色そのまま
                status = 2
                pass
            else:
                if node.stage in selectableStageMap:
                    if node.stage == currentStage.stage:
                        # 選択中
                        status = 3
                        if highlight == False:
                            status = 2
                    else:
                        # 非選択
                        status = 4
                else:
                    status = 1
        for t in __class__.imageColorTable[status]:
            pyxel.pal(t[0], t[1])
        pyxel.blt(node.x +__class__.nodeBaseX, node.y + __class__.nodeBaseY, 0, 0, 224, 32, 16)
        pyxel.pal()
        for t in __class__.textColorTable[status]:
            pyxel.pal(t[0], t[1])
        if node != None:
            Drawing.showText(node.x + 8 +__class__.nodeBaseX, node.y +4 + __class__.nodeBaseY, node.stage)
        pyxel.pal()
        if node != None and node.nextStageList != None:
            for childNode in node.nextStageList:
                StageSelect.drawNode(childNode, currentStage, selectableStageMap, clearedMap, highlight)


class NextStageSelectScene:
    def __init__(self, parent, currentStage, clearedMap):
        self.parent = parent
        self.currentStage = currentStage
        self.clearedMap = clearedMap
        if self.clearedMap == None:
            self.clearedMap = {}
        self.stageManager = stage.StageLinkManager()
        self.nextStageList = self.stageManager.findNextStageList(self.currentStage)
        self.nextStageMap = {}
        for stageInfo in self.nextStageList:
            self.nextStageMap[stageInfo.stage] = stageInfo
        
        self.currentStageInfo = None        # self.stageManager.findStage(self.currentStage)
        self.currentIndex = 0
        self.state = 0
        self.cnt = 0
        self.star_pos = 0

    def init(self):
        pyxel.image(1).load(0,0,"assets/stageList.png")

    def update(self):
        self.star_pos -= 0.25
        if self.star_pos<0:
            self.star_pos += 256

        if self.state == 0:
            if self.cnt == 20:
                BGM.play(BGM.STAGE_SELECT)
            if self.cnt > 20:
                if gcommon.checkUpP():
                    BGM.sound(gcommon.SOUND_MENUMOVE)
                    self.currentIndex -= 1
                    if self.currentIndex < 0:
                        self.currentIndex = len(self.nextStageList) -1
                if gcommon.checkDownP():
                    BGM.sound(gcommon.SOUND_MENUMOVE)
                    self.currentIndex += 1
                    if self.currentIndex >= len(self.nextStageList):
                        self.currentIndex = 0
                if gcommon.checkShotKeyP():
                    BGM.stop()
                    BGM.sound(gcommon.SOUND_GAMESTART)
                    self.state = 1
                    self.cnt = 0
        else:
            #print(str(self.cnt))
            if self.cnt > 40:
                gcommon.app.startNextStage(self.nextStageList[self.currentIndex].stage)
        self.currentStageInfo = self.nextStageList[self.currentIndex]
        self.cnt += 1


    def draw(self):
        pyxel.cls(0)
        #self.drawStar()
        gcommon.drawStar(self.star_pos)

        if len(self.nextStageList) == 1:
            # 選択できない
            Drawing.showTextHCenter(20, "GET READY FOR THE NEXT STAGE")
        else:
            Drawing.showTextHCenter(20, "SELECT NEXT STAGE")

        stageInfo = self.stageManager.stageRoot
        stageInfo.setDrawFlag(False)
        highlight = True
        if self.state == 0:
            if self.cnt & 16 == 0:
                highlight = False
        elif self.state == 1:
            if self.cnt & 2 == 0:
                highlight = False
        StageSelect.drawNode(stageInfo, self.currentStageInfo, self.nextStageMap, self.clearedMap, highlight)
        
        px = self.currentStageInfo.imageX  * 64
        py = self.currentStageInfo.imageY  * 56
        pyxel.blt(32, 108, 1, px, py, 64, 56)

        Drawing.showTextHCenter(180, "PUSH SHOT KEY")
  

class CustomStageSelectScene:
    nodeBaseX = 16
    nodeBaseY = 64
    # ステータスによって変える色のテーブル（次ステージ選択と色が違う）
    # 0 : 無効
    # 1 : まだ未達
    # 2 : クリア済み
    # 3 : 選択肢（選択中）
    # 4 : 選択肢（非選択）
    imageColorTable = [
        [[1, 0], [5, 1], [12, 5]],
        [[1, 0], [5, 1], [12, 5]],
        [],
        [[1, 1], [5, 8], [12, 14]],
        [],         #[[5, 2], [12, 2]],
    ]
    textColorTable = [
        [[7, 1]],
        [[7, 12]],
        [[5, 1]],
        [],
        [[5, 1]],       #[[7, 5],[5, 1]],
    ]
    def __init__(self, parent):
        self.parent = parent
        self.clearedMap = {}
        self.stageManager = stage.StageLinkManager()
        
        self.rootStageInfo = self.stageManager.getFirstStage()
        self.currentStageInfo = self.rootStageInfo
        self.currentIndex = 0
        self.state = 0
        self.cnt = 0
        self.star_pos = 0
        self.selectableStageMap = {}
        self.setSelectableStageMap(self.currentStageInfo)
        self.clearedMap = {}

    def init(self):
        pyxel.image(1).load(0,0,"assets/stageList.png")


    def setSelectableStageMap(self, stageInfo: stage.StageInfo):
        self.selectableStageMap[stageInfo.stage] = stageInfo
        if stageInfo.nextStageList != None:
            for child in stageInfo.nextStageList:
                self.setSelectableStageMap(child)

    def update(self):
        self.star_pos -= 0.25
        if self.star_pos<0:
            self.star_pos += 256

        if self.state == 0:
            if self.cnt == 20:
                BGM.play(BGM.STAGE_SELECT)
            if self.cnt > 20:
                if gcommon.checkUpP():
                    if self.currentStageInfo.parentList != None:
                        lst = self.currentStageInfo.parentList[0].nextStageList
                        if len(lst) > 1:
                            BGM.sound(gcommon.SOUND_MENUMOVE)
                            self.currentIndex -= 1
                            if self.currentIndex < 0:
                                self.currentIndex = len(lst) -1
                            self.currentStageInfo = lst[self.currentIndex]
                elif gcommon.checkDownP():
                    if self.currentStageInfo.parentList != None:
                        lst = self.currentStageInfo.parentList[0].nextStageList
                        if lst != None and len(lst) > 1:
                            BGM.sound(gcommon.SOUND_MENUMOVE)
                            self.currentIndex += 1
                            if self.currentIndex >= len(lst):
                                self.currentIndex = 0
                            self.currentStageInfo = lst[self.currentIndex]
                elif gcommon.checkRightP():
                    lst = self.currentStageInfo.nextStageList
                    if lst != None:
                        BGM.sound(gcommon.SOUND_MENUMOVE)
                        if self.currentIndex >= len(lst):
                            self.currentIndex = len(lst) -1
                        self.currentStageInfo = self.currentStageInfo.nextStageList[self.currentIndex]
                        #gcommon.debugPrint("index = " + str(self.currentIndex) + " " + self.currentStageInfo.stage)
                elif gcommon.checkLeftP():
                    if self.currentStageInfo.parentList != None:
                        BGM.sound(gcommon.SOUND_MENUMOVE)
                        self.currentStageInfo = self.currentStageInfo.parentList[0]
                        self.currentIndex = 0
                        #gcommon.debugPrint("index = " + str(self.currentIndex) + " " + self.currentStageInfo.stage)
                if gcommon.checkShotKeyP():
                    BGM.stop()
                    BGM.sound(gcommon.SOUND_GAMESTART)
                    self.state = 1
                    self.cnt = 0
        else:
            #print(str(self.cnt))
            if self.cnt > 40:
                gcommon.app.startNextStage(self.currentStageInfo.stage)
        self.cnt += 1


    def draw(self):
        pyxel.cls(0)
        #self.drawStar()
        gcommon.drawStar(self.star_pos)

        Drawing.showTextHCenter(20, "SELECT STAGE")

        stageInfo = self.stageManager.stageRoot
        stageInfo.setDrawFlag(False)
        highlight = True
        if self.state == 0:
            if self.cnt & 16 == 0:
                highlight = False
        elif self.state == 1:
            if self.cnt & 2 == 0:
                highlight = False
        self.drawNode(stageInfo, self.currentStageInfo, self.selectableStageMap, self.clearedMap, highlight)

        px = self.currentStageInfo.imageX  * 64
        py = self.currentStageInfo.imageY  * 56
        pyxel.blt(32, 108, 1, px, py, 64, 56)

        Drawing.showTextHCenter(180, "PUSH SHOT KEY")

    # node 描画するステージ(StateInfo)
    # currentStage 現在選択中のステージ(StateInfo)
    # selectableStageMap 選択可能なステージ(string, StateInfo)のマップ
    # cleaedMap クリアしたステージ文字列（stringのマップ）
    #
    def drawNode(self, node: stage.StageInfo, currentStage, selectableStageMap, clearedMap, highlight:bool):
        if node.drawFlag:
            return
        node.drawFlag = True
        # 0 : 無効
        # 1 : まだ未達
        # 2 : クリア済み
        # 3 : 選択肢（選択中）
        # 4 : 選択肢（非選択）
        status = 1
        # 状態種類
        #   無効（実装されてない）  enabled = False
        #   有効
        #     まだ未達
        #     クリア済
        #     選択肢  選択中／非選択
        if node == None or node.enabled == False:
            status = 0
        else:
            # 有効
            if node.stage in clearedMap:
                # クリア済みは色そのまま
                status = 2
                pass
            else:
                if node.stage in selectableStageMap:
                    if node.stage == currentStage.stage:
                        # 選択中
                        status = 3
                        if highlight == False:
                            status = 2
                    else:
                        # 非選択
                        status = 4
                else:
                    status = 1
        for t in __class__.imageColorTable[status]:
            pyxel.pal(t[0], t[1])
        pyxel.blt(node.x +__class__.nodeBaseX, node.y + __class__.nodeBaseY, 0, 0, 224, 32, 16)
        pyxel.pal()
        for t in __class__.textColorTable[status]:
            pyxel.pal(t[0], t[1])
        if node != None:
            Drawing.showText(node.x + 8 +__class__.nodeBaseX, node.y +4 + __class__.nodeBaseY, node.stage)
        pyxel.pal()
        if node != None and node.nextStageList != None:
            for childNode in node.nextStageList:
                self.drawNode(childNode, currentStage, selectableStageMap, clearedMap, highlight)
