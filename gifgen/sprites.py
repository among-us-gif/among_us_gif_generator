class ReplaceColors:
    red_replace_color = {
        'red': (215, 30, 34),
        'blue': (29, 60, 233),
        'green': (27, 145, 62),
        'pink': (255, 99, 212),
        'orange': (255, 141, 28),
        'yellow': (255, 255, 103),
        'black': (74, 86, 94),
        'white': (233, 247, 255),
        'purple': (120, 61, 210),
        'brown': (128, 88, 45),
        'cyan': (68, 255, 247),
        'lime': (91, 255, 75),
        'maroon': (108, 43, 61),
        'rose': (255, 214, 236),
        'banana': (255, 255, 190),
        'gray': (131, 151, 167),
        'tan': (159, 153, 137),
        'coral': (236, 117, 120),
    }

    blue_replace_color = {
        'red': (122, 8, 56),
        'blue': (9, 21, 142),
        'green': (10, 77, 46),
        'pink': (172, 43, 174),
        'orange': (180, 62, 21),
        'yellow': (195, 136, 34),
        'black': (30, 31, 38),
        'white': (132, 149, 192),
        'purple': (59, 23, 124),
        'brown': (94, 38, 21),
        'cyan': (36, 169, 191),
        'lime': (21, 168, 66),
        'maroon': (65, 15, 26),
        'rose': (222, 146, 179),
        'banana': (210, 188, 137),
        'gray': (70, 86, 100),
        'tan': (81, 65, 62),
        'coral': (180, 67, 98),
    }

    def __init__(self, color='blue'):
        self.green = (149, 202, 220)
        self.blue = ReplaceColors.blue_replace_color[color]
        self.red = ReplaceColors.red_replace_color[color]


class Skins:
    skin_idle = {
        'archae': 'archae-idle.png',
        'astro': 'astro-main.png',
        'capt': 'capt-main.png',
        'hazmat': 'hazmat-idle.png',
        'mech': 'mech_main.png',
        'military': 'military_stand.png',
        'miner': 'Miner-idll.png',
        'police': 'pol_Main.png',
        'science': 'sci_main.png',
        'secguard': 'secguard_idle.png',
        'blacksuit': 'suitB-Main.png',
        'whitesuit': 'suitW-main.png',
        'tarmac': 'tarmac-idle.png',
        'wall': 'wall-main.png',
        'winter': 'winter-idle.png',
    }

    skin_eject = {
        'archae': 'archae-eject.png',
        'astro': 'astro-eject.png',
        'capt': 'captl-eject.png',
        'hazmat': 'hazmat-eject.png',
        'mech': 'mech-eject.png',
        'military': 'military_ejected.png',
        'miner': 'Miner-eject.png',
        'police': 'police_eject.png',
        'science': 'sci-eject.png',
        'secguard': 'secguard-eject.png',
        'blacksuit': 'suitBlack-eject.png',
        'whitesuit': 'suitW-eject.png',
        'tarmac': 'tarmac-eject.png',
        'wall': 'wall-eject.png',
        'winter': 'winter-eject.png',
    }

    idle_offset = {
        'archae': (13, 41),
        'astro': (13, 46),
        'capt': (14, 45),
        'hazmat': (12, 34),
        'mech': (13, 46),
        'military': (11, 45),
        'miner': (13, 40),
        'police': (10, 45),
        'science': (13, 42),
        'secguard': (14, 43),
        'blacksuit': (14, 44),
        'whitesuit': (14, 44),
        'tarmac': (14, 40),
        'wall': (10, 44),
        'winter': (9, 35),
    }

    eject_offset = {
        'archae': (12, 35),
        'astro': (12, 35),
        'capt': (12, 35),
        'hazmat': (13, 37),
        'mech': (13, 35),
        'military': (12, 35),
        'miner': (12, 36),
        'police': (12, 35),
        'science': (-10, 35),  # need to expand canvas (on both sides)
        'secguard': (13, 35),
        'blacksuit': (12, 35),
        'whitesuit': (11, 35),
        'tarmac': (14, 37),
        'wall': (12, 35),
        'winter': (5, 30),
    }

    def __init__(self, skin='capt'):
        self.idle = Skins.skin_idle[skin]
        self.eject = Skins.skin_eject[skin]
        self.idle_offset = Skins.idle_offset[skin]
        self.eject_offset = Skins.eject_offset[skin]
