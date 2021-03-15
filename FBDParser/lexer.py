
import codecs
from io import BytesIO

TILDE_AS_HYPHEN = False

enclosing = {
    '〖': ('open', 'command'), 
    '〗': ('close', 'command'), 
    '\ue000': ('open', 'entity'), 
    '\ue002': ('close', 'entity')
}

operators = {
    '\ue001': 'escape', 
    '\ue003': 'return', 
    '\ue004': 'linefeed', 
    '\ue005': 'endfeed', 
    '\ue006': 'math_sign', 
    '\ue007': 'page_num', 
    '\ue008': 'run_open', 
    '\ue009': 'run_close',   
    '\ue00a': 'font_switch', 
    '\ue00b': 'superscript', 
    '\ue00c': 'subscript', 
    '\ue5e6': 'nbsp', 
    '\ue5e7': 'ensp', 
    '\ue5e8': 'thinsp', 
    '\ue5e9': 'verythinsp'
}

ascii_operators = {
    '[': ('open', 'command'), 
    ']': ('close', 'command'), 
    '\\': ('operator', 'pattern')
}

class Lexer:
    def __init__(self, strict=False, apply_ascii_operator=True):
        self.strict = strict
        self.apply_ascii_operator = apply_ascii_operator

    def readbyte(self, fp, n):
        try:
            val = fp.read(n).encode('gb18030')
        except UnicodeError as e:
            val = e.args[1]
        if len(val) > n:
            fp.seek(n - len(val), 1)
            val = val[:n]
        return val

    def parse_char(self, char):
        cate1, cate2 = 'plain', 'text'
        if char in enclosing:
            cate1, cate2 = enclosing[char]
        elif char in operators:
            cate1, cate2 = 'operator', operators[char]
        elif self.apply_ascii_operator and char in ascii_operators:
            cate1, cate2 = ascii_operators[char]
        elif char == '~' and TILDE_AS_HYPHEN:
            cate1, cate2 = 'operator', 'hyphen'
        elif '\ue000' <= char <= '\ue814':
            cate2 = 'complement'
        elif char < ' ':
            cate1 = 'control'
        return cate1, cate2, char

    def parse_gbk(self, fp):
        b = self.readbyte(fp, 2)
        c = self.readbyte(fp, 2)
        d = self.readbyte(fp, 1)
        if d == b'\x0f' and len(b) == len(c) == 2:
            if b == b'\xfe\x01':
                return 'plain', 'complement', c.decode('gb18030')
            elif b[0] == 0xff:
                return 'plain', 'text', bytearray([b[1]-1, 48+c[1]//16, c[0], 48+c[1]%16-1]).decode('gb18030')
        fp.seek(-len(b + c + d), 1)

    def parse_symbol(self, fp, n):
        fontname = self.readbyte(fp, n)
        x = self.readbyte(fp, 4)
        if len(x) == 4 and x[3] == 0xf:
            return 'symbol', fontname.decode('gb18030'), chr((x[1] - 0x40) * 0x40 + x[0] - 0x40)
        fp.seek(-len(fontname + x), 1)

    def lex(self, fp):
        try:
            token = None
            while True:
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
                elif c > '\x0f' or c.isspace():
                    token = self.parse_char(c)
                if token:
                    yield token
                    token = None
        except UnicodeError as e:
            if self.strict:
                raise e
            fp.seek(fp.tell() + 1, 1)
            yield from self.lex(fp)

    def fromfile(self, filename):
        fp = codecs.open(filename, 'r', encoding='gb18030')
        try:
            yield from self.lex(fp)
        finally:
            fp.close()

    def frombytes(self, data):
        info = codecs.lookup('gb18030')
        fp = codecs.StreamReaderWriter(BytesIO(data), info.streamreader, info.streamwriter)
        try:
            yield from self.lex(fp)
        finally:
            fp.close()
            
    def fromstring(self, text):
        for c in text:
            yield self.parse_char(c)