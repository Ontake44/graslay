import pyxel
import pygame.mixer
import gcommon
from settings import Settings

class BGM:
    #                 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26
    sound_priority = [0,2,1,4,5,3,6,8,8,1, 0, 6, 6, 1, 6, 6, 6, 1, 0, 5, 0, 0, 0, 0, 0, 0, 0]

    bgmList = [
        # volume rate, filename
        [0.5, "Dream_Fantasy.mp3"],
        [1.0, "game_maoudamashii_6_dangeon22.mp3"],
        [1.0, "Spear.mp3"],
        [1.0, "game_maoudamashii_6_dangeon15.mp3"],
        [1.0, "Abstract.mp3"],
        [1.0, "Break_the_Wedge.mp3"],
        [1.0, "Fantasma.mp3"],
        [1.0, "In_Dark_Down.mp3"],
        [1.0, "Grenade.mp3"],
        [1.0, "Blaze.mp3"],
        [1.0, "game_maoudamashii_9_jingle02.mp3"],
        [1.0, "game_maoudamashii_9_jingle07.mp3"],
        [1.0, "idola_cell.mp3"],
        [0.6, "Fireworks.mp3"],
        [0.5, "Dream_Fantasy.mp3"],		#"Runners_High.mp3"
        [1.0, "with_silence.mp3"],
        [0.6, "Runners_High.mp3"],
        [1.0, "Zonky_Cyber.mp3"]
    ] 

    STAGE1 = 0		#"Dream_Fantasy.mp3"
    STAGE2 = 1		#"game_maoudamashii_6_dangeon22.mp3"
    STAGE3 = 2		#"Spear.mp3"
    STAGE4 = 3		#"game_maoudamashii_6_dangeon15.mp3"
    STAGE5 = 4		#"Abstract.mp3"
    STAGE6_1 = 5	#"Break_the_Wedge.mp3"
    STAGE6_2 = 6	#"Fantasma.mp3"
    STAGE6_3 = 7	#"In_Dark_Down.mp3"
    BOSS  = 8		#"Grenade.mp3"
    BOSS_LAST = 9	#"Blaze.mp3"
    STAGE_CLEAR = 10	#"game_maoudamashii_9_jingle02.mp3"
    GAME_OVER = 11		#"game_maoudamashii_9_jingle07.mp3"
    #TITLE = "Underground_Worship.mp3"
    TITLE = 12		#"idola_cell.mp3"
    ENDING = 13
    LAUNCH = 14
    RANKING = 15
    STAGE_SELECT = 16
    STAGE_FIRE = 17

    @classmethod
    def getBgm(cls, no):
        return BGM.bgmList[no]

    @classmethod
    def play(cls, no):
        bgm = BGM.getBgm(no)
        pygame.mixer.music.load(gcommon.resource_path("assets/music/" + bgm[1]))
        pygame.mixer.music.set_volume(0.5 * Settings.bgmVolume * bgm[0]/10.0)
        pygame.mixer.music.play(-1)
		
    @classmethod
    def playOnce(cls, no):
        bgm = BGM.getBgm(no)
        pygame.mixer.music.load(gcommon.resource_path("assets/music/" + bgm[1]))
        pygame.mixer.music.set_volume(0.5 * Settings.bgmVolume * bgm[0]/10.0)
        pygame.mixer.music.play(1)

    @classmethod
    def stop(cls):
        pygame.mixer.music.stop()

    @classmethod
    def sound(cls, snd,ch=0):
        if Settings.soundVolume > 0:
            n = pyxel.play_pos(ch)
            if n >=0:
                pass
                #print("snd=" + hex(n))
            if (n == -1):
                pyxel.play(ch, snd)
            else:
                sn = int(n/100)
                if sn < len(cls.sound_priority):
                    if cls.sound_priority[sn]<cls.sound_priority[snd]:
                        pyxel.stop(ch)
                        pyxel.play(ch, snd)
                else:
                    print("Illegal sound number! " + str(sn))


