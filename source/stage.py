import pyxel
import gcommon
from mapDraw import MapData
from gameSession import GameSession
from audio import BGM

class StageInfo:

    def __init__(self, stage, stageNo, enabled, nextStageList):
        self.stage = stage
        self.stageNo = stageNo
        self.enabled = enabled
        self.nextStageList = nextStageList
        self.x = 0
        self.y = 0
        self.imageX = 0
        self.imageY = 0
        self.drawFlag = False
        self.parentList = None
        if self.nextStageList != None:
            for child in self.nextStageList:
                child.appendParent(self)

    def appendParent(self, parent):
        if self.parentList == None:
            self.parentList = []
        self.parentList.append(parent)

    def setDrawFlag(self, flag):
        self.drawFlag = flag
        if self.nextStageList != None:
            for childNode in self.nextStageList:
                if childNode != None:
                    childNode.setDrawFlag(flag)

    def setImage(self, x, y):
        self.imageX = x
        self.imageY = y


# 各ステージ間の関係を管理するクラス
class StageLinkManager:
    def __init__(self):
        stage6A = StageInfo("6A", 6, True, None)
        stage6A.setImage(1, 1)
        # stage6B = StageInfo("6B", 6, False, None)
        # stage6C = StageInfo("6C", 6, False, None)
        # stage6D = StageInfo("6D", 6, False, None)
        # stage6E = StageInfo("6E", 6, False, None)
        # stage6F = StageInfo("6F", 6, False, None)

        stage5A = StageInfo("5A", 5, True, [stage6A])
        stage5A.setImage(0, 1)
        stage5B = StageInfo("5B", 5, True, [stage6A])
        stage5B.setImage(0, 3)
        # stage5B = StageInfo("5B", 5, False, [stage6B, stage6C])
        # stage5C = StageInfo("5C", 5, False, [stage6C, stage6D])
        # stage5D = StageInfo("5D", 5, False, [stage6D, stage6E])
        # stage5E = StageInfo("5E", 5, False, [stage6E, stage6F])

        stage4A = StageInfo("4A", 4, True, [stage5A, stage5B])
        stage4A.setImage(3, 0)
        # stage4B = StageInfo("4B", 4, True, [stage5B, stage5C])
        # stage4C = StageInfo("4C", 4, False, [stage5C, stage5D])
        # stage4D = StageInfo("4D", 4, False, [stage5D, stage5E])

        stage3A = StageInfo("3A", 3, True, [stage4A])
        stage3A.setImage(2, 0)
        stage3B = StageInfo("3B", 3, True, [stage4A])
        stage3B.setImage(2, 2)

        stage2A = StageInfo("2A", 2, True, [stage3A, stage3B])
        stage2A.setImage(1, 0)
        stage2B = StageInfo("2B", 2, True, [stage3A, stage3B])
        stage2B.setImage(1, 2)

        self.stageRoot = StageInfo("1A", 1, True, [stage2A, stage2B])
        self.stageRoot.setImage(0, 0)
        self.stageRoot.x = 0
        self.stageRoot.y = 0
        dx = 40
        stage2A.x = self.stageRoot.x +dx 
        stage2A.y = self.stageRoot.y -12
        stage2B.x = self.stageRoot.x +dx 
        stage2B.y = self.stageRoot.y +12
        stage3A.x = stage2A.x +dx
        stage3A.y = stage2A.y
        stage3B.x = stage2B.x +dx
        stage3B.y = stage2B.y
        stage4A.x = stage3A.x +dx 
        stage4A.y = self.stageRoot.y
        stage5A.x = stage4A.x +dx 
        stage5A.y = self.stageRoot.y -12
        stage5B.x = stage4A.x +dx 
        stage5B.y = self.stageRoot.y +12
        stage6A.x = stage5A.x +dx 
        stage6A.y = self.stageRoot.y

    def getFirstStage(self):
        return self.stageRoot

    def findNextStageList(self, stage: str):
        return self.nextStageList(self.stageRoot, stage)

    def findStage(self, stage: str) -> StageInfo:
        return self.findStageRecursive(self.stageRoot, stage)

    def findStageRecursive(self, node: StageInfo, stage: str) -> StageInfo:
        if node.stage == stage:
            return node
        else:
            for childNode in node.nextStageList:
                if childNode != None and childNode.stage == stage:
                    return childNode
            for childNode in node.nextStageList:
                if childNode != None:
                    return self.findStageRecursive(childNode, stage)
            return None


    def nextStageList(self, node, stage: str):
        if node.stage == stage:
            return node.nextStageList
        elif node.nextStageList == None:
            return None
        else:
            for childNode in node.nextStageList:
                if childNode != None:
                    if childNode.stage == stage:
                        return childNode.nextStageList
            for childNode in node.nextStageList:
                if childNode != None:
                    return self.nextStageList(childNode, stage)


class Stage:
    @classmethod
    def initStage(cls, stage, restart):
        gcommon.breakableMapData = False
        pyxel.tilemap(0).refimg = 1
        gcommon.waterSurface_y = 256 * 8.0

        if stage == "1A":
            #pyxel.load("assets/graslay_vehicle01.pyxres", False, False, True, True)
            pyxel.image(1).load(0,0,"assets/graslay1.png")
            gcommon.sync_map_y = 0
            gcommon.long_map = False
            gcommon.draw_star = True
            gcommon.eshot_sync_scroll = False
            MapData.loadMapData(0, "assets/graslay1.pyxmap")
            MapData.loadMapData(1, "assets/graslay1b.pyxmap")
            MapData.loadMapAttribute("assets/graslay1.mapatr")
            pyxel.tilemap(1).refimg = 1
            if restart or GameSession.gameMode == gcommon.GAMEMODE_CUSTOM:
                # 初期スタートは発艦時にBGM開始されているので、BGM流すのはリスタート・カスタム時だけ
                BGM.play(BGM.STAGE1)
        elif stage == "2A":
            # 生物
            #pyxel.load("assets/graslay_dangeon22.pyxres", False, False, True, True)
            pyxel.image(1).load(0,0,"assets/graslay2.png")
            gcommon.sync_map_y = 0
            gcommon.long_map = False
            gcommon.draw_star = False
            gcommon.eshot_sync_scroll = False
            MapData.loadMapData(0, "assets/graslay2.pyxmap")
            MapData.loadMapAttribute("assets/graslay2.mapatr")
        elif stage == "2B":
            # 洞窟
            pyxel.image(1).load(0,0,"assets/stage_cave.png")
            pyxel.image(2).load(0,0,"assets/stage_cave-2.png")
            gcommon.sync_map_y = 2
            gcommon.long_map = True
            gcommon.draw_star = False
            gcommon.eshot_sync_scroll = True
            MapData.loadMapData(0, "assets/stage_cave.pyxmap")
            MapData.loadMapData(1, "assets/stage_caveb.pyxmap")
            MapData.loadMapAttribute("assets/stage_cave.mapatr")
            pyxel.tilemap(1).refimg = 1
        elif stage == "3B":
            # 倉庫
            pyxel.image(1).load(0,0,"assets/stage_warehouse.png")
            pyxel.image(2).load(0,0,"assets/stage_warehouse-2.png")
            gcommon.sync_map_y = 0
            gcommon.long_map = True
            gcommon.draw_star = False
            gcommon.eshot_sync_scroll = False
            MapData.loadMapData(0, "assets/stage_warehouse0.pyxmap")    # 手前に見えるマップ
            MapData.loadMapData(2, "assets/stage_warehouse1.pyxmap")    # 奥に見えるマップ
            MapData.loadMapData(5, "assets/stage_warehousei.pyxmap")    # アイテム用マップ
            MapData.loadMapData(7, "assets/stage_warehouseb.pyxmap")    # 遠景
            pyxel.tilemap(0).refimg = 1
            pyxel.tilemap(2).refimg = 1
            pyxel.tilemap(7).refimg = 1  # background
            MapData.loadMapAttribute("assets/stage_warehouse.mapatr")
        elif stage == "3A":
            # 高速スクロール
            pyxel.image(1).load(0,0,"assets/graslay3.png")
            gcommon.sync_map_y = 1
            gcommon.long_map = True
            gcommon.draw_star = True
            gcommon.eshot_sync_scroll = False
            gcommon.breakableMapData = True
            MapData.loadMapData(0, "assets/graslay3-0.pyxmap")
            MapData.loadMapData(1, "assets/graslay3-1.pyxmap")
            MapData.loadMapData(2, "assets/graslay3b.pyxmap")
            MapData.loadMapAttribute("assets/graslay3.mapatr")
            pyxel.tilemap(1).refimg = 1
            pyxel.tilemap(2).refimg = 1
        elif stage == "4A":
            # 遺跡
            pyxel.image(1).load(0,0,"assets/graslay4.png")
            gcommon.sync_map_y = 0
            gcommon.long_map = True
            gcommon.draw_star = True
            gcommon.eshot_sync_scroll = False
            MapData.loadMapData(0, "assets/graslay4.pyxmap")
            MapData.loadMapData(1, "assets/graslay4b.pyxmap")
            MapData.loadMapAttribute("assets/graslay4.mapatr")
            pyxel.tilemap(1).refimg = 1
        elif stage == "5A":
            # ファクトリー
            pyxel.image(1).load(0,0,"assets/graslay_factory.png")
            pyxel.image(2).load(0,0,"assets/graslay_factory-2.png")
            gcommon.sync_map_y = 0
            gcommon.long_map = True
            gcommon.draw_star = True
            gcommon.eshot_sync_scroll = False
            MapData.loadMapData(0, "assets/graslay_factory.pyxmap")
            MapData.loadMapData(1, "assets/graslay_factoryb.pyxmap")
            MapData.loadMapAttribute("assets/graslay_factory.mapatr")
            pyxel.tilemap(1).refimg = 1
        elif stage == "5B":
            # 火
            pyxel.image(1).load(0,0,"assets/stage_fire.png")
            pyxel.image(2).load(0,0,"assets/stage_fire2.png")
            gcommon.sync_map_y = 0
            gcommon.long_map = True
            gcommon.draw_star = True
            gcommon.eshot_sync_scroll = False
            MapData.loadMapData(0, "assets/stage_fire0.pyxmap")    # 基地
            MapData.loadMapData(2, "assets/stage_fire1.pyxmap")    # 火
            MapData.loadMapData(7, "assets/stage_fireb.pyxmap")    # 遠景？
            MapData.loadMapAttribute("assets/stage_fire.mapatr")
            pyxel.tilemap(0).refimg = 1
            pyxel.tilemap(2).refimg = 1
        elif stage == "6A":
            # 最終ステージ
            pyxel.image(1).load(0,0,"assets/graslay_last.png")
            pyxel.image(2).load(0,0,"assets/graslay_last-1.png")
            #pyxel.image(2).load(0,0,"assets/graslay_last-2.png")
            gcommon.sync_map_y = 0
            gcommon.long_map = True
            gcommon.draw_star = True
            gcommon.eshot_sync_scroll = False
            MapData.loadMapData(0, "assets/graslay_last.pyxmap")
            MapData.loadMapData(1, "assets/graslay_lastb.pyxmap")
            MapData.loadMapAttribute("assets/graslay_last.mapatr")
            pyxel.tilemap(1).refimg = 1
        #elif self.stage == 3:
        #	pyxel.image(1).load(0,0,"assets\gra-den3a.png")
        #	pyxel.image(2).load(0,0,"assets\gra-den3b.png")
        #	gcommon.draw_star = True
