


class StageInfo:
    def __init__(self, stage, stageNo, enabled, nextStageList):
        self.stage = stage
        self.stageNo = stageNo
        self.enabled = enabled
        self.nextStageList = nextStageList
        self.x = 0
        self.y = 0
        self.drawFlag = False

    def setDrawFlag(self, flag):
        self.drawFlag = flag
        if self.nextStageList != None:
            for childNode in self.nextStageList:
                if childNode != None:
                    childNode.setDrawFlag(flag)

class StageManager:
    def __init__(self):
        stage6A = StageInfo("6A", 6, True, None)
        # stage6B = StageInfo("6B", 6, False, None)
        # stage6C = StageInfo("6C", 6, False, None)
        # stage6D = StageInfo("6D", 6, False, None)
        # stage6E = StageInfo("6E", 6, False, None)
        # stage6F = StageInfo("6F", 6, False, None)

        stage5A = StageInfo("5A", 5, True, [stage6A])
        # stage5B = StageInfo("5B", 5, False, [stage6B, stage6C])
        # stage5C = StageInfo("5C", 5, False, [stage6C, stage6D])
        # stage5D = StageInfo("5D", 5, False, [stage6D, stage6E])
        # stage5E = StageInfo("5E", 5, False, [stage6E, stage6F])

        stage4A = StageInfo("4A", 4, True, [stage5A])
        # stage4B = StageInfo("4B", 4, True, [stage5B, stage5C])
        # stage4C = StageInfo("4C", 4, False, [stage5C, stage5D])
        # stage4D = StageInfo("4D", 4, False, [stage5D, stage5E])

        stage3A = StageInfo("3A", 3, True, [stage4A])
        stage3B = StageInfo("3B", 3, True, [stage4A])

        stage2A = StageInfo("2A", 2, True, [stage3A, stage3B])

        self.stageRoot = StageInfo("1", 1, True, [stage2A])
        self.stageRoot.x = 16
        self.stageRoot.y = 100
        dx = 40
        stage2A.x = self.stageRoot.x +dx 
        stage2A.y = self.stageRoot.y
        stage3A.x = stage2A.x +dx
        stage3A.y = stage2A.y -12
        stage3B.x = stage2A.x +dx
        stage3B.y = stage2A.y +12
        stage4A.x = stage3A.x +dx 
        stage4A.y = self.stageRoot.y
        stage5A.x = stage4A.x +dx 
        stage5A.y = self.stageRoot.y
        stage6A.x = stage5A.x +dx 
        stage6A.y = self.stageRoot.y

    def firstStage(self):
        return self.stageRoot

    def findNextStageList(self, stage: str) -> []:
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


    def nextStageList(self, node, stage: str) -> []:
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
