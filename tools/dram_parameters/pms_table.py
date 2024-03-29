#!/usr/bin/env python3
from argparse import ArgumentParser
from collections import namedtuple
from math import ceil, floor
from operator import itemgetter

# Fixed PLL register setting value.
ICP=1
LOCK_EN=1
BYPASS=0
SRC=0
RESETB=0

# MAX LPDDR4X PHY SPEED
MAX_SPEED=4264

# PMS_TABLE_UNIT
unit=8

Phypms = namedtuple('Phypms','freq p m s pll_value')
phypmss = []

def get_phy_pms(phypmss, speed):
    for phypms in phypmss:
        if phypms.freq == speed:
            return phypms
    raise Exception('invalid target frequency: %d' % speed)

def search_phypmss(phypmss, speed):
    ret=0
    for phypms in phypmss:
        if phypms.freq == speed:
            ret=1
    return ret

def lpddr4_pll_check(reg):
    p = (reg & 0x3F) >> 0
    m = (reg & 0xFFC0) >> 6
    s = (reg & 0x70000) >> 16
    ref_freq=float(24.0)/(float)(p)
    speed=(m*24*2)
    ret = 0

    ##### REF CLOCK SPEC CHECK ######
    if float(ref_freq) < float(4):
        ret=1
    elif float(ref_freq) > float(12):
        ret=1
        
    ##### FVCO SPEC CHECK ######
    FVCO=float(speed)/float(p)

    if float(FVCO) < float(2150):
        ret=1
    elif float(FVCO) > float(4300):
        ret=1

    ##### FOUT CHECK ######
    FOUT=float(FVCO)/float(1<<s)

    if float(FOUT) < float(34):
        ret=1
    elif float(FOUT) > float(4300):
        ret=1

    #### LPDDR4X phy speed CHECK ####
    if FOUT > 4266:
        ret=1

    return ret

def generate_pms_table():
        for s in range(0,7):
                for p in range(1,64):
                        for m in range(64, 1024):
                                reg=0
                                reg |= (p<<0)|(m<<6)|(s<<16)|(ICP<<24)|(LOCK_EN<<26)|(BYPASS<<21)|(SRC<<19)|(RESETB<<31)

                                if lpddr4_pll_check(reg) != 0:
                                    continue
                                else:
                                    speed=((m*24*2)/p)/(1<<s)
                    
                                    if (MAX_SPEED - speed)%unit == 0:
                                        if search_phypmss(phypmss, speed) == 0:
                                            phypmss.append(Phypms(speed, p, m, s, reg))

        phypmss.sort(key=lambda t:t[0])
        for i, data in enumerate(phypmss):
            print("phypmss.append(Phypms(%d, %d, %d, %d, %d))" % (phypmss[i].freq, phypmss[i].p, phypmss[i].m,
                                    phypmss[i].s, phypmss[i].pll_value))


######################
# uncomment generate_pms_table() function to generate table.
# 
# generate_pms_table() 
# 
######################

phypmss.append(Phypms(40, 3, 160, 6, 84289539))
phypmss.append(Phypms(48, 2, 128, 6, 84287490))
phypmss.append(Phypms(56, 3, 224, 6, 84293635))
phypmss.append(Phypms(64, 3, 256, 6, 84295683))
phypmss.append(Phypms(72, 2, 96, 5, 84219906))
phypmss.append(Phypms(80, 3, 160, 5, 84224003))
phypmss.append(Phypms(88, 3, 176, 5, 84225027))
phypmss.append(Phypms(96, 2, 128, 5, 84221954))
phypmss.append(Phypms(104, 3, 208, 5, 84227075))
phypmss.append(Phypms(112, 3, 224, 5, 84228099))
phypmss.append(Phypms(120, 2, 160, 5, 84224002))
phypmss.append(Phypms(128, 3, 256, 5, 84230147))
phypmss.append(Phypms(136, 3, 136, 4, 84156931))
phypmss.append(Phypms(144, 2, 96, 4, 84154370))
phypmss.append(Phypms(152, 3, 152, 4, 84157955))
phypmss.append(Phypms(160, 3, 160, 4, 84158467))
phypmss.append(Phypms(168, 2, 112, 4, 84155394))
phypmss.append(Phypms(176, 3, 176, 4, 84159491))
phypmss.append(Phypms(184, 3, 184, 4, 84160003))
phypmss.append(Phypms(192, 2, 128, 4, 84156418))
phypmss.append(Phypms(200, 3, 200, 4, 84161027))
phypmss.append(Phypms(208, 3, 208, 4, 84161539))
phypmss.append(Phypms(216, 2, 144, 4, 84157442))
phypmss.append(Phypms(224, 3, 224, 4, 84162563))
phypmss.append(Phypms(232, 3, 232, 4, 84163075))
phypmss.append(Phypms(240, 2, 160, 4, 84158466))
phypmss.append(Phypms(248, 3, 248, 4, 84164099))
phypmss.append(Phypms(256, 3, 256, 4, 84164611))
phypmss.append(Phypms(264, 2, 176, 4, 84159490))
phypmss.append(Phypms(272, 3, 136, 3, 84091395))
phypmss.append(Phypms(280, 3, 140, 3, 84091651))
phypmss.append(Phypms(288, 2, 96, 3, 84088834))
phypmss.append(Phypms(296, 3, 148, 3, 84092163))
phypmss.append(Phypms(304, 3, 152, 3, 84092419))
phypmss.append(Phypms(312, 2, 104, 3, 84089346))
phypmss.append(Phypms(320, 3, 160, 3, 84092931))
phypmss.append(Phypms(328, 3, 164, 3, 84093187))
phypmss.append(Phypms(336, 2, 112, 3, 84089858))
phypmss.append(Phypms(344, 3, 172, 3, 84093699))
phypmss.append(Phypms(352, 3, 176, 3, 84093955))
phypmss.append(Phypms(360, 2, 120, 3, 84090370))
phypmss.append(Phypms(368, 3, 184, 3, 84094467))
phypmss.append(Phypms(376, 3, 188, 3, 84094723))
phypmss.append(Phypms(384, 2, 128, 3, 84090882))
phypmss.append(Phypms(392, 3, 196, 3, 84095235))
phypmss.append(Phypms(400, 3, 200, 3, 84095491))
phypmss.append(Phypms(408, 2, 136, 3, 84091394))
phypmss.append(Phypms(416, 3, 208, 3, 84096003))
phypmss.append(Phypms(424, 3, 212, 3, 84096259))
phypmss.append(Phypms(432, 2, 144, 3, 84091906))
phypmss.append(Phypms(440, 3, 220, 3, 84096771))
phypmss.append(Phypms(448, 3, 224, 3, 84097027))
phypmss.append(Phypms(456, 2, 152, 3, 84092418))
phypmss.append(Phypms(464, 3, 232, 3, 84097539))
phypmss.append(Phypms(472, 3, 236, 3, 84097795))
phypmss.append(Phypms(480, 2, 160, 3, 84092930))
phypmss.append(Phypms(488, 3, 244, 3, 84098307))
phypmss.append(Phypms(496, 3, 248, 3, 84098563))
phypmss.append(Phypms(504, 2, 168, 3, 84093442))
phypmss.append(Phypms(512, 3, 256, 3, 84099075))
phypmss.append(Phypms(520, 3, 260, 3, 84099331))
phypmss.append(Phypms(528, 2, 176, 3, 84093954))
phypmss.append(Phypms(536, 3, 268, 3, 84099843))
phypmss.append(Phypms(544, 3, 136, 2, 84025859))
phypmss.append(Phypms(552, 2, 92, 2, 84023042))
phypmss.append(Phypms(560, 3, 140, 2, 84026115))
phypmss.append(Phypms(568, 3, 142, 2, 84026243))
phypmss.append(Phypms(576, 2, 96, 2, 84023298))
phypmss.append(Phypms(584, 3, 146, 2, 84026499))
phypmss.append(Phypms(592, 3, 148, 2, 84026627))
phypmss.append(Phypms(600, 2, 100, 2, 84023554))
phypmss.append(Phypms(608, 3, 152, 2, 84026883))
phypmss.append(Phypms(616, 3, 154, 2, 84027011))
phypmss.append(Phypms(624, 2, 104, 2, 84023810))
phypmss.append(Phypms(632, 3, 158, 2, 84027267))
phypmss.append(Phypms(640, 3, 160, 2, 84027395))
phypmss.append(Phypms(648, 2, 108, 2, 84024066))
phypmss.append(Phypms(656, 3, 164, 2, 84027651))
phypmss.append(Phypms(664, 3, 166, 2, 84027779))
phypmss.append(Phypms(672, 2, 112, 2, 84024322))
phypmss.append(Phypms(680, 3, 170, 2, 84028035))
phypmss.append(Phypms(688, 3, 172, 2, 84028163))
phypmss.append(Phypms(696, 2, 116, 2, 84024578))
phypmss.append(Phypms(704, 3, 176, 2, 84028419))
phypmss.append(Phypms(712, 3, 178, 2, 84028547))
phypmss.append(Phypms(720, 2, 120, 2, 84024834))
phypmss.append(Phypms(728, 3, 182, 2, 84028803))
phypmss.append(Phypms(736, 3, 184, 2, 84028931))
phypmss.append(Phypms(744, 2, 124, 2, 84025090))
phypmss.append(Phypms(752, 3, 188, 2, 84029187))
phypmss.append(Phypms(760, 3, 190, 2, 84029315))
phypmss.append(Phypms(768, 2, 128, 2, 84025346))
phypmss.append(Phypms(776, 3, 194, 2, 84029571))
phypmss.append(Phypms(784, 3, 196, 2, 84029699))
phypmss.append(Phypms(792, 2, 132, 2, 84025602))
phypmss.append(Phypms(800, 3, 200, 2, 84029955))
phypmss.append(Phypms(808, 3, 202, 2, 84030083))
phypmss.append(Phypms(816, 2, 136, 2, 84025858))
phypmss.append(Phypms(824, 3, 206, 2, 84030339))
phypmss.append(Phypms(832, 3, 208, 2, 84030467))
phypmss.append(Phypms(840, 2, 140, 2, 84026114))
phypmss.append(Phypms(848, 3, 212, 2, 84030723))
phypmss.append(Phypms(856, 3, 214, 2, 84030851))
phypmss.append(Phypms(864, 2, 144, 2, 84026370))
phypmss.append(Phypms(872, 3, 218, 2, 84031107))
phypmss.append(Phypms(880, 3, 220, 2, 84031235))
phypmss.append(Phypms(888, 2, 148, 2, 84026626))
phypmss.append(Phypms(896, 3, 224, 2, 84031491))
phypmss.append(Phypms(904, 3, 226, 2, 84031619))
phypmss.append(Phypms(912, 2, 152, 2, 84026882))
phypmss.append(Phypms(920, 3, 230, 2, 84031875))
phypmss.append(Phypms(928, 3, 232, 2, 84032003))
phypmss.append(Phypms(936, 2, 156, 2, 84027138))
phypmss.append(Phypms(944, 3, 236, 2, 84032259))
phypmss.append(Phypms(952, 3, 238, 2, 84032387))
phypmss.append(Phypms(960, 2, 160, 2, 84027394))
phypmss.append(Phypms(968, 3, 242, 2, 84032643))
phypmss.append(Phypms(976, 3, 244, 2, 84032771))
phypmss.append(Phypms(984, 2, 164, 2, 84027650))
phypmss.append(Phypms(992, 3, 248, 2, 84033027))
phypmss.append(Phypms(1000, 3, 250, 2, 84033155))
phypmss.append(Phypms(1008, 2, 168, 2, 84027906))
phypmss.append(Phypms(1016, 3, 254, 2, 84033411))
phypmss.append(Phypms(1024, 3, 256, 2, 84033539))
phypmss.append(Phypms(1032, 2, 172, 2, 84028162))
phypmss.append(Phypms(1040, 3, 260, 2, 84033795))
phypmss.append(Phypms(1048, 3, 262, 2, 84033923))
phypmss.append(Phypms(1056, 2, 176, 2, 84028418))
phypmss.append(Phypms(1064, 3, 266, 2, 84034179))
phypmss.append(Phypms(1072, 3, 268, 2, 84034307))
phypmss.append(Phypms(1080, 2, 90, 1, 83957378))
phypmss.append(Phypms(1088, 3, 136, 1, 83960323))
phypmss.append(Phypms(1096, 3, 137, 1, 83960387))
phypmss.append(Phypms(1104, 2, 92, 1, 83957506))
phypmss.append(Phypms(1112, 3, 139, 1, 83960515))
phypmss.append(Phypms(1120, 3, 140, 1, 83960579))
phypmss.append(Phypms(1128, 2, 94, 1, 83957634))
phypmss.append(Phypms(1136, 3, 142, 1, 83960707))
phypmss.append(Phypms(1144, 3, 143, 1, 83960771))
phypmss.append(Phypms(1152, 2, 96, 1, 83957762))
phypmss.append(Phypms(1160, 3, 145, 1, 83960899))
phypmss.append(Phypms(1168, 3, 146, 1, 83960963))
phypmss.append(Phypms(1176, 2, 98, 1, 83957890))
phypmss.append(Phypms(1184, 3, 148, 1, 83961091))
phypmss.append(Phypms(1192, 3, 149, 1, 83961155))
phypmss.append(Phypms(1200, 2, 100, 1, 83958018))
phypmss.append(Phypms(1208, 3, 151, 1, 83961283))
phypmss.append(Phypms(1216, 3, 152, 1, 83961347))
phypmss.append(Phypms(1224, 2, 102, 1, 83958146))
phypmss.append(Phypms(1232, 3, 154, 1, 83961475))
phypmss.append(Phypms(1240, 3, 155, 1, 83961539))
phypmss.append(Phypms(1248, 2, 104, 1, 83958274))
phypmss.append(Phypms(1256, 3, 157, 1, 83961667))
phypmss.append(Phypms(1264, 3, 158, 1, 83961731))
phypmss.append(Phypms(1272, 2, 106, 1, 83958402))
phypmss.append(Phypms(1280, 3, 160, 1, 83961859))
phypmss.append(Phypms(1288, 3, 161, 1, 83961923))
phypmss.append(Phypms(1296, 2, 108, 1, 83958530))
phypmss.append(Phypms(1304, 3, 163, 1, 83962051))
phypmss.append(Phypms(1312, 3, 164, 1, 83962115))
phypmss.append(Phypms(1320, 2, 110, 1, 83958658))
phypmss.append(Phypms(1328, 3, 166, 1, 83962243))
phypmss.append(Phypms(1336, 3, 167, 1, 83962307))
phypmss.append(Phypms(1344, 2, 112, 1, 83958786))
phypmss.append(Phypms(1352, 3, 169, 1, 83962435))
phypmss.append(Phypms(1360, 3, 170, 1, 83962499))
phypmss.append(Phypms(1368, 2, 114, 1, 83958914))
phypmss.append(Phypms(1376, 3, 172, 1, 83962627))
phypmss.append(Phypms(1384, 3, 173, 1, 83962691))
phypmss.append(Phypms(1392, 2, 116, 1, 83959042))
phypmss.append(Phypms(1400, 3, 175, 1, 83962819))
phypmss.append(Phypms(1408, 3, 176, 1, 83962883))
phypmss.append(Phypms(1416, 2, 118, 1, 83959170))
phypmss.append(Phypms(1424, 3, 178, 1, 83963011))
phypmss.append(Phypms(1432, 3, 179, 1, 83963075))
phypmss.append(Phypms(1440, 2, 120, 1, 83959298))
phypmss.append(Phypms(1448, 3, 181, 1, 83963203))
phypmss.append(Phypms(1456, 3, 182, 1, 83963267))
phypmss.append(Phypms(1464, 2, 122, 1, 83959426))
phypmss.append(Phypms(1472, 3, 184, 1, 83963395))
phypmss.append(Phypms(1480, 3, 185, 1, 83963459))
phypmss.append(Phypms(1488, 2, 124, 1, 83959554))
phypmss.append(Phypms(1496, 3, 187, 1, 83963587))
phypmss.append(Phypms(1504, 3, 188, 1, 83963651))
phypmss.append(Phypms(1512, 2, 126, 1, 83959682))
phypmss.append(Phypms(1520, 3, 190, 1, 83963779))
phypmss.append(Phypms(1528, 3, 191, 1, 83963843))
phypmss.append(Phypms(1536, 2, 128, 1, 83959810))
phypmss.append(Phypms(1544, 3, 193, 1, 83963971))
phypmss.append(Phypms(1552, 3, 194, 1, 83964035))
phypmss.append(Phypms(1560, 2, 130, 1, 83959938))
phypmss.append(Phypms(1568, 3, 196, 1, 83964163))
phypmss.append(Phypms(1576, 3, 197, 1, 83964227))
phypmss.append(Phypms(1584, 2, 132, 1, 83960066))
phypmss.append(Phypms(1592, 3, 199, 1, 83964355))
phypmss.append(Phypms(1600, 3, 200, 1, 83964419))
phypmss.append(Phypms(1608, 2, 134, 1, 83960194))
phypmss.append(Phypms(1616, 3, 202, 1, 83964547))
phypmss.append(Phypms(1624, 3, 203, 1, 83964611))
phypmss.append(Phypms(1632, 2, 136, 1, 83960322))
phypmss.append(Phypms(1640, 3, 205, 1, 83964739))
phypmss.append(Phypms(1648, 3, 206, 1, 83964803))
phypmss.append(Phypms(1656, 2, 138, 1, 83960450))
phypmss.append(Phypms(1664, 3, 208, 1, 83964931))
phypmss.append(Phypms(1672, 3, 209, 1, 83964995))
phypmss.append(Phypms(1680, 2, 140, 1, 83960578))
phypmss.append(Phypms(1688, 3, 211, 1, 83965123))
phypmss.append(Phypms(1696, 3, 212, 1, 83965187))
phypmss.append(Phypms(1704, 2, 142, 1, 83960706))
phypmss.append(Phypms(1712, 3, 214, 1, 83965315))
phypmss.append(Phypms(1720, 3, 215, 1, 83965379))
phypmss.append(Phypms(1728, 2, 144, 1, 83960834))
phypmss.append(Phypms(1736, 3, 217, 1, 83965507))
phypmss.append(Phypms(1744, 3, 218, 1, 83965571))
phypmss.append(Phypms(1752, 2, 146, 1, 83960962))
phypmss.append(Phypms(1760, 3, 220, 1, 83965699))
phypmss.append(Phypms(1768, 3, 221, 1, 83965763))
phypmss.append(Phypms(1776, 2, 148, 1, 83961090))
phypmss.append(Phypms(1784, 3, 223, 1, 83965891))
phypmss.append(Phypms(1792, 3, 224, 1, 83965955))
phypmss.append(Phypms(1800, 2, 150, 1, 83961218))
phypmss.append(Phypms(1808, 3, 226, 1, 83966083))
phypmss.append(Phypms(1816, 3, 227, 1, 83966147))
phypmss.append(Phypms(1824, 2, 152, 1, 83961346))
phypmss.append(Phypms(1832, 3, 229, 1, 83966275))
phypmss.append(Phypms(1840, 3, 230, 1, 83966339))
phypmss.append(Phypms(1848, 2, 154, 1, 83961474))
phypmss.append(Phypms(1856, 3, 232, 1, 83966467))
phypmss.append(Phypms(1864, 3, 233, 1, 83966531))
phypmss.append(Phypms(1872, 2, 156, 1, 83961602))
phypmss.append(Phypms(1880, 3, 235, 1, 83966659))
phypmss.append(Phypms(1888, 3, 236, 1, 83966723))
phypmss.append(Phypms(1896, 2, 158, 1, 83961730))
phypmss.append(Phypms(1904, 3, 238, 1, 83966851))
phypmss.append(Phypms(1912, 3, 239, 1, 83966915))
phypmss.append(Phypms(1920, 2, 160, 1, 83961858))
phypmss.append(Phypms(1928, 3, 241, 1, 83967043))
phypmss.append(Phypms(1936, 3, 242, 1, 83967107))
phypmss.append(Phypms(1944, 2, 162, 1, 83961986))
phypmss.append(Phypms(1952, 3, 244, 1, 83967235))
phypmss.append(Phypms(1960, 3, 245, 1, 83967299))
phypmss.append(Phypms(1968, 2, 164, 1, 83962114))
phypmss.append(Phypms(1976, 3, 247, 1, 83967427))
phypmss.append(Phypms(1984, 3, 248, 1, 83967491))
phypmss.append(Phypms(1992, 2, 166, 1, 83962242))
phypmss.append(Phypms(2000, 3, 250, 1, 83967619))
phypmss.append(Phypms(2008, 3, 251, 1, 83967683))
phypmss.append(Phypms(2016, 2, 168, 1, 83962370))
phypmss.append(Phypms(2024, 3, 253, 1, 83967811))
phypmss.append(Phypms(2032, 3, 254, 1, 83967875))
phypmss.append(Phypms(2040, 2, 170, 1, 83962498))
phypmss.append(Phypms(2048, 3, 256, 1, 83968003))
phypmss.append(Phypms(2056, 3, 257, 1, 83968067))
phypmss.append(Phypms(2064, 2, 172, 1, 83962626))
phypmss.append(Phypms(2072, 3, 259, 1, 83968195))
phypmss.append(Phypms(2080, 3, 260, 1, 83968259))
phypmss.append(Phypms(2088, 2, 174, 1, 83962754))
phypmss.append(Phypms(2096, 3, 262, 1, 83968387))
phypmss.append(Phypms(2104, 3, 263, 1, 83968451))
phypmss.append(Phypms(2112, 2, 176, 1, 83962882))
phypmss.append(Phypms(2120, 3, 265, 1, 83968579))
phypmss.append(Phypms(2128, 3, 266, 1, 83968643))
phypmss.append(Phypms(2136, 2, 178, 1, 83963010))
phypmss.append(Phypms(2144, 3, 268, 1, 83968771))
phypmss.append(Phypms(2152, 6, 269, 0, 83903302))
phypmss.append(Phypms(2160, 2, 90, 0, 83891842))
phypmss.append(Phypms(2168, 6, 271, 0, 83903430))
phypmss.append(Phypms(2176, 3, 136, 0, 83894787))
phypmss.append(Phypms(2184, 2, 91, 0, 83891906))
phypmss.append(Phypms(2192, 3, 137, 0, 83894851))
phypmss.append(Phypms(2200, 6, 275, 0, 83903686))
phypmss.append(Phypms(2208, 2, 92, 0, 83891970))
phypmss.append(Phypms(2216, 6, 277, 0, 83903814))
phypmss.append(Phypms(2224, 3, 139, 0, 83894979))
phypmss.append(Phypms(2232, 2, 93, 0, 83892034))
phypmss.append(Phypms(2240, 3, 140, 0, 83895043))
phypmss.append(Phypms(2248, 6, 281, 0, 83904070))
phypmss.append(Phypms(2256, 2, 94, 0, 83892098))
phypmss.append(Phypms(2264, 6, 283, 0, 83904198))
phypmss.append(Phypms(2272, 3, 142, 0, 83895171))
phypmss.append(Phypms(2280, 2, 95, 0, 83892162))
phypmss.append(Phypms(2288, 3, 143, 0, 83895235))
phypmss.append(Phypms(2296, 6, 287, 0, 83904454))
phypmss.append(Phypms(2304, 2, 96, 0, 83892226))
phypmss.append(Phypms(2312, 6, 289, 0, 83904582))
phypmss.append(Phypms(2320, 3, 145, 0, 83895363))
phypmss.append(Phypms(2328, 2, 97, 0, 83892290))
phypmss.append(Phypms(2336, 3, 146, 0, 83895427))
phypmss.append(Phypms(2344, 6, 293, 0, 83904838))
phypmss.append(Phypms(2352, 2, 98, 0, 83892354))
phypmss.append(Phypms(2360, 6, 295, 0, 83904966))
phypmss.append(Phypms(2368, 3, 148, 0, 83895555))
phypmss.append(Phypms(2376, 2, 99, 0, 83892418))
phypmss.append(Phypms(2384, 3, 149, 0, 83895619))
phypmss.append(Phypms(2392, 6, 299, 0, 83905222))
phypmss.append(Phypms(2400, 2, 100, 0, 83892482))
phypmss.append(Phypms(2408, 6, 301, 0, 83905350))
phypmss.append(Phypms(2416, 3, 151, 0, 83895747))
phypmss.append(Phypms(2424, 2, 101, 0, 83892546))
phypmss.append(Phypms(2432, 3, 152, 0, 83895811))
phypmss.append(Phypms(2440, 6, 305, 0, 83905606))
phypmss.append(Phypms(2448, 2, 102, 0, 83892610))
phypmss.append(Phypms(2456, 6, 307, 0, 83905734))
phypmss.append(Phypms(2464, 3, 154, 0, 83895939))
phypmss.append(Phypms(2472, 2, 103, 0, 83892674))
phypmss.append(Phypms(2480, 3, 155, 0, 83896003))
phypmss.append(Phypms(2488, 6, 311, 0, 83905990))
phypmss.append(Phypms(2496, 2, 104, 0, 83892738))
phypmss.append(Phypms(2504, 6, 313, 0, 83906118))
phypmss.append(Phypms(2512, 3, 157, 0, 83896131))
phypmss.append(Phypms(2520, 2, 105, 0, 83892802))
phypmss.append(Phypms(2528, 3, 158, 0, 83896195))
phypmss.append(Phypms(2536, 6, 317, 0, 83906374))
phypmss.append(Phypms(2544, 2, 106, 0, 83892866))
phypmss.append(Phypms(2552, 6, 319, 0, 83906502))
phypmss.append(Phypms(2560, 3, 160, 0, 83896323))
phypmss.append(Phypms(2568, 2, 107, 0, 83892930))
phypmss.append(Phypms(2576, 3, 161, 0, 83896387))
phypmss.append(Phypms(2584, 6, 323, 0, 83906758))
phypmss.append(Phypms(2592, 2, 108, 0, 83892994))
phypmss.append(Phypms(2600, 6, 325, 0, 83906886))
phypmss.append(Phypms(2608, 3, 163, 0, 83896515))
phypmss.append(Phypms(2616, 2, 109, 0, 83893058))
phypmss.append(Phypms(2624, 3, 164, 0, 83896579))
phypmss.append(Phypms(2632, 6, 329, 0, 83907142))
phypmss.append(Phypms(2640, 2, 110, 0, 83893122))
phypmss.append(Phypms(2648, 6, 331, 0, 83907270))
phypmss.append(Phypms(2656, 3, 166, 0, 83896707))
phypmss.append(Phypms(2664, 2, 111, 0, 83893186))
phypmss.append(Phypms(2672, 3, 167, 0, 83896771))
phypmss.append(Phypms(2680, 6, 335, 0, 83907526))
phypmss.append(Phypms(2688, 2, 112, 0, 83893250))
phypmss.append(Phypms(2696, 6, 337, 0, 83907654))
phypmss.append(Phypms(2704, 3, 169, 0, 83896899))
phypmss.append(Phypms(2712, 2, 113, 0, 83893314))
phypmss.append(Phypms(2720, 3, 170, 0, 83896963))
phypmss.append(Phypms(2728, 6, 341, 0, 83907910))
phypmss.append(Phypms(2736, 2, 114, 0, 83893378))
phypmss.append(Phypms(2744, 6, 343, 0, 83908038))
phypmss.append(Phypms(2752, 3, 172, 0, 83897091))
phypmss.append(Phypms(2760, 2, 115, 0, 83893442))
phypmss.append(Phypms(2768, 3, 173, 0, 83897155))
phypmss.append(Phypms(2776, 6, 347, 0, 83908294))
phypmss.append(Phypms(2784, 2, 116, 0, 83893506))
phypmss.append(Phypms(2792, 6, 349, 0, 83908422))
phypmss.append(Phypms(2800, 3, 175, 0, 83897283))
phypmss.append(Phypms(2808, 2, 117, 0, 83893570))
phypmss.append(Phypms(2816, 3, 176, 0, 83897347))
phypmss.append(Phypms(2824, 6, 353, 0, 83908678))
phypmss.append(Phypms(2832, 2, 118, 0, 83893634))
phypmss.append(Phypms(2840, 6, 355, 0, 83908806))
phypmss.append(Phypms(2848, 3, 178, 0, 83897475))
phypmss.append(Phypms(2856, 2, 119, 0, 83893698))
phypmss.append(Phypms(2864, 3, 179, 0, 83897539))
phypmss.append(Phypms(2872, 6, 359, 0, 83909062))
phypmss.append(Phypms(2880, 2, 120, 0, 83893762))
phypmss.append(Phypms(2888, 6, 361, 0, 83909190))
phypmss.append(Phypms(2896, 3, 181, 0, 83897667))
phypmss.append(Phypms(2904, 2, 121, 0, 83893826))
phypmss.append(Phypms(2912, 3, 182, 0, 83897731))
phypmss.append(Phypms(2920, 6, 365, 0, 83909446))
phypmss.append(Phypms(2928, 2, 122, 0, 83893890))
phypmss.append(Phypms(2936, 6, 367, 0, 83909574))
phypmss.append(Phypms(2944, 3, 184, 0, 83897859))
phypmss.append(Phypms(2952, 2, 123, 0, 83893954))
phypmss.append(Phypms(2960, 3, 185, 0, 83897923))
phypmss.append(Phypms(2968, 6, 371, 0, 83909830))
phypmss.append(Phypms(2976, 2, 124, 0, 83894018))
phypmss.append(Phypms(2984, 6, 373, 0, 83909958))
phypmss.append(Phypms(2992, 3, 187, 0, 83898051))
phypmss.append(Phypms(3000, 2, 125, 0, 83894082))
phypmss.append(Phypms(3008, 3, 188, 0, 83898115))
phypmss.append(Phypms(3016, 6, 377, 0, 83910214))
phypmss.append(Phypms(3024, 2, 126, 0, 83894146))
phypmss.append(Phypms(3032, 6, 379, 0, 83910342))
phypmss.append(Phypms(3040, 3, 190, 0, 83898243))
phypmss.append(Phypms(3048, 2, 127, 0, 83894210))
phypmss.append(Phypms(3056, 3, 191, 0, 83898307))
phypmss.append(Phypms(3064, 6, 383, 0, 83910598))
phypmss.append(Phypms(3072, 2, 128, 0, 83894274))
phypmss.append(Phypms(3080, 6, 385, 0, 83910726))
phypmss.append(Phypms(3088, 3, 193, 0, 83898435))
phypmss.append(Phypms(3096, 2, 129, 0, 83894338))
phypmss.append(Phypms(3104, 3, 194, 0, 83898499))
phypmss.append(Phypms(3112, 6, 389, 0, 83910982))
phypmss.append(Phypms(3120, 2, 130, 0, 83894402))
phypmss.append(Phypms(3128, 6, 391, 0, 83911110))
phypmss.append(Phypms(3136, 3, 196, 0, 83898627))
phypmss.append(Phypms(3144, 2, 131, 0, 83894466))
phypmss.append(Phypms(3152, 3, 197, 0, 83898691))
phypmss.append(Phypms(3160, 6, 395, 0, 83911366))
phypmss.append(Phypms(3168, 2, 132, 0, 83894530))
phypmss.append(Phypms(3176, 6, 397, 0, 83911494))
phypmss.append(Phypms(3184, 3, 199, 0, 83898819))
phypmss.append(Phypms(3192, 2, 133, 0, 83894594))
phypmss.append(Phypms(3200, 3, 200, 0, 83898883))
phypmss.append(Phypms(3208, 6, 401, 0, 83911750))
phypmss.append(Phypms(3216, 2, 134, 0, 83894658))
phypmss.append(Phypms(3224, 6, 403, 0, 83911878))
phypmss.append(Phypms(3232, 3, 202, 0, 83899011))
phypmss.append(Phypms(3240, 2, 135, 0, 83894722))
phypmss.append(Phypms(3248, 3, 203, 0, 83899075))
phypmss.append(Phypms(3256, 6, 407, 0, 83912134))
phypmss.append(Phypms(3264, 2, 136, 0, 83894786))
phypmss.append(Phypms(3272, 6, 409, 0, 83912262))
phypmss.append(Phypms(3280, 3, 205, 0, 83899203))
phypmss.append(Phypms(3288, 2, 137, 0, 83894850))
phypmss.append(Phypms(3296, 3, 206, 0, 83899267))
phypmss.append(Phypms(3304, 6, 413, 0, 83912518))
phypmss.append(Phypms(3312, 2, 138, 0, 83894914))
phypmss.append(Phypms(3320, 6, 415, 0, 83912646))
phypmss.append(Phypms(3328, 3, 208, 0, 83899395))
phypmss.append(Phypms(3336, 2, 139, 0, 83894978))
phypmss.append(Phypms(3344, 3, 209, 0, 83899459))
phypmss.append(Phypms(3352, 6, 419, 0, 83912902))
phypmss.append(Phypms(3360, 2, 140, 0, 83895042))
phypmss.append(Phypms(3368, 6, 421, 0, 83913030))
phypmss.append(Phypms(3376, 3, 211, 0, 83899587))
phypmss.append(Phypms(3384, 2, 141, 0, 83895106))
phypmss.append(Phypms(3392, 3, 212, 0, 83899651))
phypmss.append(Phypms(3400, 6, 425, 0, 83913286))
phypmss.append(Phypms(3408, 2, 142, 0, 83895170))
phypmss.append(Phypms(3416, 6, 427, 0, 83913414))
phypmss.append(Phypms(3424, 3, 214, 0, 83899779))
phypmss.append(Phypms(3432, 2, 143, 0, 83895234))
phypmss.append(Phypms(3440, 3, 215, 0, 83899843))
phypmss.append(Phypms(3448, 6, 431, 0, 83913670))
phypmss.append(Phypms(3456, 2, 144, 0, 83895298))
phypmss.append(Phypms(3464, 6, 433, 0, 83913798))
phypmss.append(Phypms(3472, 3, 217, 0, 83899971))
phypmss.append(Phypms(3480, 2, 145, 0, 83895362))
phypmss.append(Phypms(3488, 3, 218, 0, 83900035))
phypmss.append(Phypms(3496, 6, 437, 0, 83914054))
phypmss.append(Phypms(3504, 2, 146, 0, 83895426))
phypmss.append(Phypms(3512, 6, 439, 0, 83914182))
phypmss.append(Phypms(3520, 3, 220, 0, 83900163))
phypmss.append(Phypms(3528, 2, 147, 0, 83895490))
phypmss.append(Phypms(3536, 3, 221, 0, 83900227))
phypmss.append(Phypms(3544, 6, 443, 0, 83914438))
phypmss.append(Phypms(3552, 2, 148, 0, 83895554))
phypmss.append(Phypms(3560, 6, 445, 0, 83914566))
phypmss.append(Phypms(3568, 3, 223, 0, 83900355))
phypmss.append(Phypms(3576, 2, 149, 0, 83895618))
phypmss.append(Phypms(3584, 3, 224, 0, 83900419))
phypmss.append(Phypms(3592, 6, 449, 0, 83914822))
phypmss.append(Phypms(3600, 2, 150, 0, 83895682))
phypmss.append(Phypms(3608, 6, 451, 0, 83914950))
phypmss.append(Phypms(3616, 3, 226, 0, 83900547))
phypmss.append(Phypms(3624, 2, 151, 0, 83895746))
phypmss.append(Phypms(3632, 3, 227, 0, 83900611))
phypmss.append(Phypms(3640, 6, 455, 0, 83915206))
phypmss.append(Phypms(3648, 2, 152, 0, 83895810))
phypmss.append(Phypms(3656, 6, 457, 0, 83915334))
phypmss.append(Phypms(3664, 3, 229, 0, 83900739))
phypmss.append(Phypms(3672, 2, 153, 0, 83895874))
phypmss.append(Phypms(3680, 3, 230, 0, 83900803))
phypmss.append(Phypms(3688, 6, 461, 0, 83915590))
phypmss.append(Phypms(3696, 2, 154, 0, 83895938))
phypmss.append(Phypms(3704, 6, 463, 0, 83915718))
phypmss.append(Phypms(3712, 3, 232, 0, 83900931))
phypmss.append(Phypms(3720, 2, 155, 0, 83896002))
phypmss.append(Phypms(3728, 3, 233, 0, 83900995))
phypmss.append(Phypms(3736, 6, 467, 0, 83915974))
phypmss.append(Phypms(3744, 2, 156, 0, 83896066))
phypmss.append(Phypms(3752, 6, 469, 0, 83916102))
phypmss.append(Phypms(3760, 3, 235, 0, 83901123))
phypmss.append(Phypms(3768, 2, 157, 0, 83896130))
phypmss.append(Phypms(3776, 3, 236, 0, 83901187))
phypmss.append(Phypms(3784, 6, 473, 0, 83916358))
phypmss.append(Phypms(3792, 2, 158, 0, 83896194))
phypmss.append(Phypms(3800, 6, 475, 0, 83916486))
phypmss.append(Phypms(3808, 3, 238, 0, 83901315))
phypmss.append(Phypms(3816, 2, 159, 0, 83896258))
phypmss.append(Phypms(3824, 3, 239, 0, 83901379))
phypmss.append(Phypms(3832, 6, 479, 0, 83916742))
phypmss.append(Phypms(3840, 2, 160, 0, 83896322))
phypmss.append(Phypms(3848, 6, 481, 0, 83916870))
phypmss.append(Phypms(3856, 3, 241, 0, 83901507))
phypmss.append(Phypms(3864, 2, 161, 0, 83896386))
phypmss.append(Phypms(3872, 3, 242, 0, 83901571))
phypmss.append(Phypms(3880, 6, 485, 0, 83917126))
phypmss.append(Phypms(3888, 2, 162, 0, 83896450))
phypmss.append(Phypms(3896, 6, 487, 0, 83917254))
phypmss.append(Phypms(3904, 3, 244, 0, 83901699))
phypmss.append(Phypms(3912, 2, 163, 0, 83896514))
phypmss.append(Phypms(3920, 3, 245, 0, 83901763))
phypmss.append(Phypms(3928, 6, 491, 0, 83917510))
phypmss.append(Phypms(3936, 2, 164, 0, 83896578))
phypmss.append(Phypms(3944, 6, 493, 0, 83917638))
phypmss.append(Phypms(3952, 3, 247, 0, 83901891))
phypmss.append(Phypms(3960, 2, 165, 0, 83896642))
phypmss.append(Phypms(3968, 3, 248, 0, 83901955))
phypmss.append(Phypms(3976, 6, 497, 0, 83917894))
phypmss.append(Phypms(3984, 2, 166, 0, 83896706))
phypmss.append(Phypms(3992, 6, 499, 0, 83918022))
phypmss.append(Phypms(4000, 3, 250, 0, 83902083))
phypmss.append(Phypms(4008, 2, 167, 0, 83896770))
phypmss.append(Phypms(4016, 3, 251, 0, 83902147))
phypmss.append(Phypms(4024, 6, 503, 0, 83918278))
phypmss.append(Phypms(4032, 2, 168, 0, 83896834))
phypmss.append(Phypms(4040, 6, 505, 0, 83918406))
phypmss.append(Phypms(4048, 3, 253, 0, 83902275))
phypmss.append(Phypms(4056, 2, 169, 0, 83896898))
phypmss.append(Phypms(4064, 3, 254, 0, 83902339))
phypmss.append(Phypms(4072, 6, 509, 0, 83918662))
phypmss.append(Phypms(4080, 2, 170, 0, 83896962))
phypmss.append(Phypms(4088, 6, 511, 0, 83918790))
phypmss.append(Phypms(4096, 3, 256, 0, 83902467))
phypmss.append(Phypms(4104, 2, 171, 0, 83897026))
phypmss.append(Phypms(4112, 3, 257, 0, 83902531))
phypmss.append(Phypms(4120, 6, 515, 0, 83919046))
phypmss.append(Phypms(4128, 2, 172, 0, 83897090))
phypmss.append(Phypms(4136, 6, 517, 0, 83919174))
phypmss.append(Phypms(4144, 3, 259, 0, 83902659))
phypmss.append(Phypms(4152, 2, 173, 0, 83897154))
phypmss.append(Phypms(4160, 3, 260, 0, 83902723))
phypmss.append(Phypms(4168, 6, 521, 0, 83919430))
phypmss.append(Phypms(4176, 2, 174, 0, 83897218))
phypmss.append(Phypms(4184, 6, 523, 0, 83919558))
phypmss.append(Phypms(4192, 3, 262, 0, 83902851))
phypmss.append(Phypms(4200, 2, 175, 0, 83897282))
phypmss.append(Phypms(4208, 3, 263, 0, 83902915))
phypmss.append(Phypms(4216, 6, 527, 0, 83919814))
phypmss.append(Phypms(4224, 2, 176, 0, 83897346))
phypmss.append(Phypms(4232, 6, 529, 0, 83919942))
phypmss.append(Phypms(4240, 3, 265, 0, 83903043))
phypmss.append(Phypms(4248, 2, 177, 0, 83897410))
phypmss.append(Phypms(4256, 3, 266, 0, 83903107))
phypmss.append(Phypms(4264, 6, 533, 0, 83920198))
