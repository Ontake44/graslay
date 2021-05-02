import json
import os.path
import sys
import os
import gcommon

class Defaults:
	INIT_START_STAGE = "1"
	INIT_WEAPON_TYPE = gcommon.WeaponType.TYPE_A
	# 残機
	INIT_PLAYER_STOCK = 3
	INIT_BGM_VOL = 7
	INIT_SOUND_VOL = 10
	INIT_DIFFICULTY = gcommon.DIFFICULTY_NORMAL
	INIT_CREDITS = 3
	INIT_MULTIPLE_COUNT = 4
	INIT_MOUSE_ENABLED = True


class Settings:
    SETTINGS_FILE = ".graslay"
    playerStock = Defaults.INIT_PLAYER_STOCK
    weaponType = Defaults.INIT_WEAPON_TYPE
    multipleCount = Defaults.INIT_MULTIPLE_COUNT
    startStage = Defaults.INIT_START_STAGE
    bgmVolume = Defaults.INIT_BGM_VOL
    soundVolume = Defaults.INIT_SOUND_VOL
    difficulty = Defaults.INIT_DIFFICULTY
    credits = Defaults.INIT_CREDITS
    normalRanking = None
    easyRanking = None
    mouseEnabled = Defaults.INIT_MOUSE_ENABLED

    @classmethod
    def loadSettings(cls):
        json_file = None
        try:
            settingsPath = os.path.join(os.path.expanduser("~"), cls.SETTINGS_FILE)

            playerStock = 3
            startStage = "1"
            bgmVol = 6
            soundVol = 10
            mouseEnabled = "1"
            difficulty = Defaults.INIT_DIFFICULTY
            credits = Defaults.INIT_CREDITS
            weaponType = Defaults.INIT_WEAPON_TYPE
            multipleCount = Defaults.INIT_MULTIPLE_COUNT
            json_file = open(settingsPath, "r")
            json_data = json.load(json_file)
            if "playerStock" in json_data:
                playerStock = int(json_data["playerStock"])
            if "startStage" in json_data:
                startStage = str(json_data["startStage"])
            if "bgmVol" in json_data:
                bgmVol = int(json_data["bgmVol"])
            if "soundVol" in json_data:
                soundVol = int(json_data["soundVol"])
            if "mouseEnabled" in json_data:
                mouseEnabled = int(json_data["mouseEnabled"])
            if "difficulty" in json_data:
                difficulty = int(json_data["difficulty"])
            if "credits" in json_data:
                credits = int(json_data["credits"])
            if "weaponType" in json_data:
                weaponType = int(json_data["weaponType"])
            if "multipleCount" in json_data:
                multipleCount = int(json_data["multipleCount"])

            if playerStock >= 1 and playerStock <= 99:
                Settings.playerStock = playerStock
            if startStage in gcommon.stageList:
                Settings.startStage = startStage
            if bgmVol >= 0 and bgmVol <= 10:
                Settings.bgmVolume = bgmVol
            if soundVol >= 0 and soundVol <= 10:
                Settings.soundVolume = soundVol
            Settings.mouseEnabled = True if mouseEnabled == "1" else False
            if difficulty in (gcommon.DIFFICULTY_EASY, gcommon.DIFFICULTY_NORMAL, gcommon.DIFFICULTY_HARD):
                Settings.difficulty = difficulty
            if credits > 0 and credits < 100:
                Settings.credits = credits
            if weaponType == gcommon.WeaponType.TYPE_A or weaponType == gcommon.WeaponType.TYPE_B:
                Settings.weaponType = weaponType
            if multipleCount >= 0 and multipleCount <= 20:
                Settings.multipleCount = multipleCount
        except:
            pass
        finally:
            if json_file != None:
                try:
                    json_file.close()
                except:
                    pass

    @classmethod
    def saveSettings(cls):
        json_data = { "playerStock": Settings.playerStock, \
            "startStage": Settings.startStage, \
            "bgmVol": Settings.bgmVolume, \
            "soundVol" : Settings.soundVolume, \
            "mouseEnabled" : "1" if Settings.mouseEnabled else "0",	\
            "difficulty" : 	Settings.difficulty,	\
            "credits" : Settings.credits,	\
            "weaponType" : Settings.weaponType,		\
            "multipleCount" : Settings.multipleCount		\
        }

        try:
            settingsPath = os.path.join(os.path.expanduser("~"), cls.SETTINGS_FILE)

            json_file = open(settingsPath, "w")
            json.dump(json_data, json_file)
            json_file.close()

        except:
            pass
