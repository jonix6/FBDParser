
from collections import deque
from .lexer import Lexer
from unicodedata import normalize

escaped_tokens = {
    ' ': '　',
    '!': '“',
    '"': '”',
    '#': '〕',
    '$': '\ue006',
    '%': '\ue00a',
    '&': '\ue007',
    "'": '’',
    '(': '\ue000',
    ')': '\ue002',
    '*': '〔',
    '+': '\ue00b',
    ',': '、',
    '-': '\ue00b',
    '.': '。',
    '/': '‘',
    '0': '〖HT',
    '1': '〖ST',
    '2': '〖WT',
    '3': '〖BH',
    '4': '〖BT',
    '5': '·',
    '6': '【',
    '7': '】',
    '8': '〈',
    '9': '〉',
    ':': '…',
    ';': '\ue004',
    '<': '《',
    '=': '\ue003',
    '>': '》',
    '?': '→',
    '@': '\ue005',
    'A': '〖BT(',
    'B': '〖BG(',
    'C': '〖CT(',
    'D': '〖DS(',
    'E': '〖FK(',
    'F': '〖FL(',
    'G': '〖FQ(',
    'H': '〖HS(',
    'I': '〖JY(',
    'J': '〖JZ(',
    'K': '〖KX(',
    'L': '〖LT(',
    'M': '〖ML(',
    'N': '〖BS(',
    'O': '〖ZB(',
    'P': '〖HZ(',
    'Q': '〖QX(',
    'R': '〖JB(',
    'S': '〖SX(',
    'T': '〖TS(',
    'U': '〖ZZ(',
    'V': '〖ZW(',
    'W': '〖WX(',
    'X': '〖XZ(',
    'Y': '〖YY(',
    'Z': '〖ZK(',
    '^': '\ue010',
    '-': '—',
    '`': 'ˈ',
    'a': '〖BT)〗',
    'b': '〖BG)',
    'c': '〖CT)〗',
    'd': '〖DS)〗',
    'e': '〖FK)〗',
    'f': '〖FL)',
    'g': '〖FQ)〗',
    'h': '〖HS)〗',
    'i': '〖JY)〗',
    'j': '〖JZ)〗',
    'k': '〖KX)〗',
    'l': '〖LT)〗',
    'm': '〖ML)〗',
    'n': '〖BS)〗',
    'o': '〖ZB)',
    'p': '〖HZ)〗',
    'q': '〖QX)〗',
    'r': '〖JB)',
    's': '〖SX)〗',
    't': '〖TS)〗',
    'u': '〖ZZ)〗',
    'v': '〖ZW)〗',
    'w': '〖WX)〗',
    'x': '〖XZ)〗',
    'y': '〖YY)〗',
    'z': '〖ZK)〗',
    '{': '\ue008',
    '|': '\ue011',
    '}': '\ue009',
    '~': '\ue001'
}


class Tokenizer:
    def __init__(self):
        self.state_stack = []
        self.current = ''

        self.stack = deque()
        self.escape = 0
        self.comment = []

    def reset(self):
        self.state_stack.clear()
        self.current = ''
        self.stack.clear()
        self.escape = 0
        self.comment.clear()

    def get_current_state(self):
        if self.state_stack:
            return self.state_stack[-1]
        return 'text'

    def new_object(self, new_state=''):
        state = self.state_stack.pop() if self.state_stack else 'text'
        if state != 'text' or self.current:
            self.stack.append((state, self.current))
        new_state and self.state_stack.append(new_state)
        self.current = ''

    def parse_token(self, token):
        if self.comment:
            self.comment_token(token)
        elif self.escape:
            self.escape_token(token)
        else:
            type, cate, char = token
            func = getattr(self, f'parse_{type}', None)
            func and func(cate, char)

    def parse_char(self, state, char):
        if state == 'text' and '\ue000' <= char <= '\ue814':
            self.new_object()
            self.stack.append(('text@symbolA', char))
        else:
            self.current += char

    def comment_token(self, token):
        if token[1] == 'command':
            if token[0] == 'open':
                self.comment[-1] += token[2]
                return self.comment.append('')
            elif normalize('NFC', self.comment[-1]) == 'BP)':
                self.stack.append(
                    ('comment', ''.join(self.comment) + token[2]))
                return self.comment.clear()
        self.comment[-1] += token[2]

    def escape_token(self, token):
        state = self.get_current_state()
        escape, self.escape = self.escape, 0
        if escape == 1:
            return self.parse_char(state, token[2])
        if ' ' <= token[2] <= '~':
            text = escaped_tokens.get(token[2], token[2])
            for token in Lexer(apply_ascii_operator=False).fromstring(text):
                self.parse_token(token)
        else:
            self.parse_char(state, '\\')
            self.parse_token(token)

    def parse_open(self, cate, char):
        state = self.get_current_state()
        if state == 'text':
            self.new_object(cate)
        else:
            assert state != cate != 'command', "open command operation error"
            self.current += char

    def parse_close(self, cate, char):
        state = self.get_current_state()
        if state != cate:
            self.parse_char(state, char)
        else:
            self.new_object()
            if cate == 'command' and normalize('NFC', self.stack[-1][1]) == 'BP(':
                self.comment.append(f'〖{self.stack.pop()[1]}〗')

    def parse_plain(self, cate, char):
        if self.get_current_state() == 'text' and cate != 'text':
            self.new_object()
            self.stack.append((f'text@{cate}', char))
        else:
            self.current += char

    def parse_symbol(self, font, char):
        if self.get_current_state() == 'text':
            self.new_object()
            self.stack.append((f'text@{font}', char))
        else:
            self.current += char

    def parse_operator(self, cate, char):
        if cate == 'escape':
            self.escape = 1
        elif cate == 'pattern':
            self.escape = 2
        elif cate != 'endfeed' and self.get_current_state() != 'text':
            self.current += char
        else:
            self.new_object()
            self.stack.append(('operator', cate))

    def parse_hidden(self, cate, char):
        pass

    def tokenize(self, tokens):
        for token in tokens:
            self.parse_token(token)
            while self.stack:
                yield self.stack.popleft()
        self.new_object()
        while self.stack:
            yield self.stack.popleft()

    def fromfile(self, filename, strict=True, apply_ascii_operator=True):
        device = Lexer(
            strict=strict, apply_ascii_operator=apply_ascii_operator)
        yield from self.tokenize(device.fromfile(filename))

    def frombytes(self, data, strict=True, apply_ascii_operator=True):
        device = Lexer(
            strict=strict, apply_ascii_operator=apply_ascii_operator)
        yield from self.tokenize(device.frombytes(data))

    def fromstring(self, text, apply_ascii_operator=True):
        yield from self.tokenize(Lexer(apply_ascii_operator=apply_ascii_operator).fromstring(text))
