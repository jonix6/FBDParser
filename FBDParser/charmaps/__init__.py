# -*- coding: utf-8 -*-

from .hanzi748 import hanzi748
from .symbol748 import symbol748
from .symbols import symbolsA, symbolsB
from .variant748 import variants748
from ..exceptions import FBDEncodingError


class CMap(dict):
    def __str__(self):
        return 'character map contains {0} codes'.format(len(self))


# 748编码映射集: 748编码 -> GBK编码
FZ748Map = CMap()
FZ748Map.update(hanzi748)
FZ748Map.update(symbol748)


# unicode映射集: AB库字符 -> 同义unicode
unicodeMap = CMap()
unicodeMap.update(symbolsA)
unicodeMap.update(symbolsB)


class CMap748:
    '''### 方正748编码映射集

    对748编码进行映射，返回相同语义的GBK编码，并可通过unicode映射集，将字符编码转为可打印的unicode字符。

    对于补字，可通过导入补字映射，对补字进行解码。
    '''

    def __init__(self, complements=None):
        self.complements = complements or {}

    def __assert(func):
        def wrapper(obj, x):
            try:
                assert 0x8080 <= x <= 0xFEFF
                a, b = x >> 8, x & 0xFF
                if 0x80 <= a <= 0xA0:
                    assert b >= 0x80
                elif a >= 0xA4:
                    assert b >= 0x21
            except AssertionError:
                raise FBDEncodingError(
                    'invaild 748 encoding: 0x{:x}'.format(x))
            return func(obj, x)
        return wrapper

    @__assert
    def register(self, code, char):
        self.complements[code] = char

    @__assert
    def normalize(self, x):
        return FZ748Map.get(x, x)

    @__assert
    def decode(self, x, translate=True):
        if x in self.complements:
            return self.complements[x]
        x = FZ748Map.get(x, x)
        char = bytearray([x >> 8, x & 0xFF]).decode('gb18030')
        if translate:
            char = char.translate(unicodeMap)
        return char
