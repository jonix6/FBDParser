

symbol748 = {}


def _update(code_748, code_gbk, numchars):
    for i in range(numchars):
        symbol748[code_748 + i] = code_gbk + i


_update(0x8EFF, 0x8E8F, 1)  # 8EFF -> 8E8F
_update(0x94FF, 0x94DA, 1)  # 94FF -> 94DA
_update(0x95FF, 0x95F1, 1)  # 95FF -> 95F1
_update(0x9680, 0xB17E, 1)  # 9680 -> B17E
_update(0x9681, 0xB47E, 1)  # 9681 -> B47E
_update(0x9682, 0xB57E, 1)  # 9682 -> B57E
_update(0x9683, 0xB261, 1)  # 9683 -> B261
_update(0xA081, 0x8940, 3)  # A081-A083 -> 8940-8942
_update(0xA089, 0xA2A0, 1)  # A089 -> A2A0
_update(0xA08A, 0x8943, 4)  # A08A-A08D -> 8943-8946
_update(0xA0A1, 0xA1A0, 1)  # A0A1 -> A1A0
_update(0xA0A2, 0xA3A2, 2)  # A0A2-A0A3 -> A3A2-A3A3
_update(0xA0A4, 0xA1E7, 1)  # A0A4 -> A1E7
_update(0xA0A5, 0xA3A5, 3)  # A0A5-A0A7 -> A3A5-A3A7
_update(0xA0A8, 0xA39F, 2)  # A0A8-A0A9 -> A39F-A3A0
_update(0xA0AA, 0xAAB3, 1)  # A0AA -> AAB3
_update(0xA0AB, 0xA3AB, 1)  # A0AB -> A3AB
_update(0xA0AC, 0xA29F, 1)  # A0AC -> A29F
_update(0xA0AD, 0xA3AD, 13)  # A0AD-A0B9 -> A3AD-A3B9
_update(0xA0BA, 0xA69F, 2)  # A0BA-A0BB -> A69F-A6A0
_update(0xA0BC, 0xA3BC, 31)  # A0BC-A0DA -> A3BC-A3DA
_update(0xA0DB, 0xA49F, 1)  # A0DB -> A49F
_update(0xA0DC, 0xA3DC, 1)  # A0DC -> A3DC
_update(0xA0DD, 0xA4A0, 1)  # A0DD -> A4A0
_update(0xA0DE, 0xA3DE, 29)  # A0DE-A0FA -> A3DE-A3FA
_update(0xA0FB, 0xA59F, 1)  # A0FB -> A59F
_update(0xA0FC, 0xA3FC, 1)  # A0FC -> A3FC
_update(0xA0FD, 0xA5A0, 1)  # A0FD -> A5A0
_update(0xA0FE, 0xA3FE, 1)  # A0FE -> A3FE
_update(0xA100, 0x8240, 11)  # A100-A10A -> 8240-824E
_update(0xA10B, 0xB14B, 22)  # A10B-A120 -> B14B-B160
_update(0xA121, 0xA140, 32)  # A121-A15F -> A140-A17E
_update(0xA160, 0xA180, 31)  # A160-A17E -> A180-A19E
_update(0xA180, 0xB180, 23)  # A180-A196 -> B180-B196
_update(0xA200, 0xB240, 33)  # A200-A220 -> B240-B260
_update(0xA221, 0xA240, 63)  # A221-A25F -> A240-A27E
_update(0xA260, 0xA280, 31)  # A260-A27E -> A280-A29E
_update(0xA280, 0xB280, 33)  # A280-A2A0 -> B280-B2A0
_update(0xA2FF, 0xA2EF, 1)  # A2FF -> A2EF
_update(0xA300, 0xB340, 31)  # A300-A31E -> B340-B35E
_update(0xA321, 0xA340, 63)  # A321-A35F -> A340-A37E
_update(0xA360, 0xA380, 31)  # A360-A37E -> A380-A39E
_update(0xA380, 0xB380, 19)  # A380-A392 -> B380-B392
_update(0xA393, 0xA1AD, 1)  # A393 -> A1AD
_update(0xA394, 0xB394, 13)  # A394-A3A0 -> B394-B3A0
_update(0xA421, 0xA440, 63)  # A421-A45F -> A440-A47E
_update(0xA460, 0xA480, 31)  # A460-A47E -> A480-A49E
_update(0xA480, 0xB480, 33)  # A480-A4A0 -> B480-B4A0
_update(0xA521, 0xA540, 63)  # A521-A55F -> A540-A57E
_update(0xA560, 0x97F2, 2)  # A560-A561 -> 97F2-97F3
_update(0xA56F, 0xA58F, 5)  # A56F-A573 -> A58F-A593
_update(0xA578, 0xA598, 7)  # A578-A57E -> A598-A59E
_update(0xA580, 0xB580, 33)  # A580-A5A0 -> B580-B5A0
_update(0xA621, 0xA640, 56)  # A621-A658 -> A640-A677
_update(0xA660, 0xA680, 14)  # A660-A66D -> A680-A68D
_update(0xA680, 0xB680, 31)  # A680-A69E -> B680-B69E
_update(0xA780, 0xB780, 32)  # A780-A79F -> B780-B79F
# A7A0 (no matches)
_update(0xA7FF, 0xB7A0, 1)  # A7FF -> B7A0
_update(0xA880, 0xB880, 30)  # A880-A89D -> B880-B89D
_update(0xA89F, 0xB89F, 2)  # A89F-A8A0 -> B89F-B8A0
_update(0xA980, 0xB980, 30)  # A980-A99D -> B980-B99D
_update(0xA9FF, 0xB9A0, 1)  # A9FF -> B9A0
_update(0xAA80, 0xBA80, 2)  # AA80-AA81 -> BA80-BA81
