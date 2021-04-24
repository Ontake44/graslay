
import pyxel
import stage
import gcommon
from audio import BGM
from drawing import Drawing

class StageSelectScene:
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
    def __init__(self, parent, currentStage, clearedMap):
        self.parent = parent
        self.currentStage = currentStage
        self.clearedMap = clearedMap
        if self.clearedMap == None:
            self.clearedMap = {}
        self.stageManager = stage.StageLinkManager()
        self.nextStageList = self.stageManager.findNextStageList(self.currentStage)
        self.currentStageInfo = self.stageManager.findStage(self.currentStage)
        self.currentIndex = 0
        self.state = 0
        self.cnt = 0
        self.star_pos = 0

    def init(self):
        pass

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
        self.cnt += 1


    def draw(self):
        pyxel.cls(0)
        #self.drawStar()
        gcommon.drawStar(self.star_pos)
        stageInfo = self.stageManager.stageRoot
        stageInfo.setDrawFlag(False)
        self.drawNode(stageInfo)

    # def drawStar(self):
    #     for i in range(0,96):
    #         pyxel.pset(gcommon.star_ary[i][0], int(i*2 +self.star_pos) % 200, gcommon.star_ary[i][1])

    def drawNode(self, node: stage.StageInfo):
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
            if node.stage in self.clearedMap:
                # クリア済みは色そのまま
                status = 2
                pass
            else:
                find = False
                for i, stageInfo in enumerate(self.nextStageList):
                    if stageInfo.stage == node.stage:
                        find = True
                        if i == self.currentIndex:
                            # 選択中
                            status = 3
                            if self.state == 0:
                                if self.cnt & 16 == 0:
                                    status = 2
                            elif self.state == 1:
                                if self.cnt & 2 == 0:
                                    status = 2
                        else:
                            # 非選択
                            status = 4
                            if self.state == 1:
                                status = 1
                        break
                if find == False:
                    status = 1
        # if self.state == 1:
        #     if status == 3:
        #         if self.cnt & 2 == 0:
        #             status = 2
        for t in __class__.imageColorTable[status]:
            pyxel.pal(t[0], t[1])
        pyxel.blt(node.x, node.y, 0, 0, 224, 32, 16)
        pyxel.pal()
        for t in __class__.textColorTable[status]:
            pyxel.pal(t[0], t[1])
        if node != None:
            Drawing.showText(node.x + 8, node.y +4, node.stage)
        pyxel.pal()
        if node != None and node.nextStageList != None:
            for childNode in node.nextStageList:
                self.drawNode(childNode)

