from logging import exception
import pyxel
import pygame.mixer
import gcommon
from settings import Settings

class BGM:
    #                 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26
    sound_priority = [0,2,1,4,5,3,6,8,8,1, 0, 6, 6, 1, 6, 6, 6, 1, 0, 5, 0, 5, 5, 3, 0, 0, 0]

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
        [1.0, "Zonky_Cyber.mp3"],
        [1.0, "Nervousness.mp3"],
        [1.0, "In_Chase.mp3"],
        [1.0, "R246_Midnight.mp3"],
        [1.0 ,"Pleasure_In_Survival.mp3"],
        [1.0 ,"DANGAN.mp3"],
        [1.0 ,"otoko_no_steaktime.mp3"],
        [1.0 ,"Fill_It_In_Black.mp3"],
        [1.0 ,"SAMURAI_PUNK.mp3"],
        [1.0 ,"The_BEAST.mp3"],
        [1.0 ,"Dominator.mp3"],
    ] 
    #
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
    ENDING = 13     #"Fireworks.mp3"
    LAUNCH = 14     #"Dream_Fantasy.mp3"
    RANKING = 15        # "with_silence.mp3"
    STAGE_SELECT = 16   # "Runners_High.mp3"
    STAGE_FIRE = 17     # "Zonky_Cyber.mp3"
    STAGE_CAVE = 18         # "Nervousness.mp3"
    STAGE_WAREHOUSE = 19    # "In_Chase.mp3"
    STAGE_LABYRINTH = 20    # "R246_Midnight.mp3"
    STAGE_BATTLESHIP = 21   # "Pleasure_In_Survival.mp3"
    BOSSRUSH_1 = 22         # DANGAN.mp3
    BOSSRUSH_2 = 23         # 漢のステーキタイム.mp3
    BOSSRUSH_4 = 25         # SAMURAI_PUNK.mp3
    BOSSRUSH_5 = 26         # The_BEAST.mp3
    BOSSRUSH_6 = 27         # Dominator.mp3

    @classmethod
    def getBgm(cls, no):
        return BGM.bgmList[no]

    @classmethod
    def play(cls, no):
        try:
            bgm = BGM.getBgm(no)
            #print("BGM " + gcommon.resource_path("assets/music/" + bgm[1]))
            pygame.mixer.music.load(gcommon.resource_path("assets/music/" + bgm[1]))
            pygame.mixer.music.set_volume(0.5 * Settings.bgmVolume * bgm[0]/10.0)
            pygame.mixer.music.play(-1)
        except Exception: 
            pass

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
            if n is None:
                pyxel.play(ch, snd)
                return
            sn = n[0]
            if sn < len(cls.sound_priority):
                if cls.sound_priority[sn]<cls.sound_priority[snd]:
                    pyxel.stop(ch)
                    pyxel.play(ch, snd)


