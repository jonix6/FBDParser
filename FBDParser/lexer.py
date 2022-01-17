# -*- coding: utf-8 -*-

import codecs
from io import BytesIO

TILDE_AS_HYPHEN = False  # 将"~"处理为软连字符

# 注解括弧对
enclosing = {
    u'〖': ('open', 'command'),
    u'〗': ('close', 'command'),
    u'\ue000': ('open', 'entity'),
    u'\ue002': ('close', 'entity')
}

# 操作符
operators = {
    u'\ue001': 'escape',
    u'\ue003': 'return',
    u'\ue004': 'linefeed',
    u'\ue005': 'endfeed',
    u'\ue006': 'math_sign',
    u'\ue007': 'page_num',
    u'\ue008': 'run_open',
    u'\ue009': 'run_close',
    u'\ue00a': 'font_switch',
    u'\ue00b': 'superscript',
    u'\ue00c': 'subscript',
    u'\ue5e6': 'nbsp',
    u'\ue5e7': 'ensp',
    u'\ue5e8': 'thinsp',
    u'\ue5e9': 'verythinsp'
}

# ascii操作符，按设置控制是否识别
ascii_operators = {
    '[': ('open', 'command'),
    ']': ('close', 'command'),
    '\\': ('operator', 'pattern')
}


class Lexer:
    '''### 字符类型识别器

    #### 主要功能

    逐字符读取数据流，按语法判断其语义类型，控制分词（tokenize）结果

    #### 传入参数

    + strict (bool): 若为true，当出现解码错误时报告异常，否则跳过继续读取
    + apply_ascii_operator (bool): 将"[, ], \\\\" 处理为转义字符'''

    def __init__(self, strict=False, apply_ascii_operator=True):
        self.strict = strict
        self.apply_ascii_operator = apply_ascii_operator

    def readbyte(self, fp, n):
        '读取n个字节数据'
        try:
            val = fp.read(n).encode('gb18030')
        except UnicodeError as e:
            val = e.args[1]
        if len(val) > n:
            fp.seek(n - len(val), 1)
            val = val[:n]
        return val

    def parse_char(self, char):
        '判断字符类型'
        cate1, cate2 = 'plain', 'text'
        if char in enclosing:
            cate1, cate2 = enclosing[char]
        elif char in operators:
            cate1, cate2 = 'operator', operators[char]
        elif self.apply_ascii_operator and char in ascii_operators:
            cate1, cate2 = ascii_operators[char]
        elif char == '~' and TILDE_AS_HYPHEN:
            cate1, cate2 = 'operator', 'hyphen'
        elif u'\ue000' <= char <= u'\ue814':
            cate2 = 'symbolA'
        elif char < ' ':
            cate1 = 'control'
        elif char.isspace():
            cate1 = 'space'
        return cate1, cate2, char

    def parse_gbk(self, fp):
        '''获取GB18030四字节字符或B库字符编码，并进行解码。

        解码方式: 

        + B库字符: 0e ff f0 | fe ** [aa bb] | 0f -> [aa bb]
        + GB18030四字节字符: 0e ff f0 | ff [ab cd ef] | 0f -> [aa 3e cd 3e]'''
        b = self.readbyte(fp, 2)
        c = self.readbyte(fp, 2)
        d = self.readbyte(fp, 1)
        if d == b'\x0f' and len(b) == len(c) == 2:
            if b[0] == 0xfe and b[1] < 0x80:
                return 'plain', 'symbolB', c.decode('gb18030')
            elif b[0] == 0xff:
                return 'plain', 'text', bytearray([b[1]-1, 48+c[1]//16, c[0], 47+c[1] % 16]).decode('gb18030')
        fp.seek(-len(b + c + d)-1, 1)

    def parse_symbol(self, fp, n):
        '''获取使用外挂字体的字符和所用字体。

        解码方式: 0e fe | 86 (S y m b o l) [4a d2 f1] | 0f -> charcode=0xca, font=Symbol

        |4a          |d2          |f1          |
        |------------|------------|------------|
        |01[001010]  |110100[10]  |111100[01]  |
        |00[001010]  |[10]000000  |[01]000000  |

        -> 11001010 -> 0xca'''
        fontname = self.readbyte(fp, n)
        x = self.readbyte(fp, 4)
        if len(x) == 4 and x[3] == 0xf:
            code = x[0] & 0x3f | ((x[1] | x[2]) & 3 << 6)
            return 'symbol', fontname.decode('gb18030'), chr(code)
        fp.seek(-len(fontname + x)-1, 1)

    def lex(self, fp):
        '迭代解析每个有语义的字符，生成三元组（大类、子类、字符）。'
        token = None
        while 1:
            try:
                c = fp.read(1)
                if not c:
                    break
                if c == '\x0e':
                    b = self.readbyte(fp, 2)
                    if not b:
                        break
                    if b == b'\xff\xf0':
                        token = self.parse_gbk(fp)
                    elif b[0] == 0xfe:
                        token = self.parse_symbol(fp, b[1] - 0x80)
                    else:
                        fp.seek(-2, 1)
                elif c > '\x0f' or c.isspace():
                    token = self.parse_char(c)
                if token:
                    yield token
                    token = None
            except UnicodeError as e:
                if self.strict:
                    raise e
                fp.seek(1-len(e.args[1]), 1)

    def fromstream(self, fp):
        '从文本流进行识别'
        try:
            for token in self.lex(fp):
                yield token
        finally:
            fp.close()

    def fromfile(self, filename):
        '从本地文件进行识别'
        return self.fromstream(codecs.open(filename, 'r', encoding='gb18030'))

    def frombytes(self, data):
        '从二进制字符串进行识别'
        info = codecs.lookup('gb18030')
        fp = codecs.StreamReaderWriter(
            BytesIO(data), info.streamreader, info.streamwriter)
        return self.fromstream(fp)

    def fromstring(self, text):
        '从字符串进行识别'
        for c in text:
            yield self.parse_char(c)
