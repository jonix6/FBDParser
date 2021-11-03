
from collections import deque

from .exceptions import FBDCommandError, FBDNestingError, FBDTemplateError, FBDSyntaxError
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

        self.templates = {}
        self.temp_stack = []

    def reset(self):
        self.state_stack.clear()
        self.current = ''
        self.stack.clear()
        self.escape = 0
        self.comment.clear()
        self.templates.clear()
        self.temp_stack.clear()

    def _assert(self, flag, err):
        if not flag:
            raise err

    def get_current_state(self):
        return self.state_stack[-1] if self.state_stack else 'text'

    def curstack(self):
        return self.temp_stack[-1] if self.temp_stack else self.stack

    def new_object(self, new_state=''):
        state = self.state_stack.pop() if self.state_stack else 'text'
        self.curstack().append((state, self.current))
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
            self.new_object('text@symbolA')
        self.current += char

    def comment_token(self, token):
        if token[1] == 'command':
            if token[0] == 'open':
                self.comment[-1] += token[2]
                return self.comment.append('')
            elif normalize('NFC', self.comment[-1]) == 'BP)':
                self.comment.pop()
                self.curstack().append(('comment', ''.join(self.comment)))
                return self.comment.clear()
        self.comment[-1] += token[2]

    def escape_token(self, token):
        state = self.get_current_state()
        escape, self.escape = self.escape, 0
        if escape == 1:
            return self.parse_char(state, token[2])
        elif escape == 3:
            self._assert('1' <= token[2] <= '9', FBDSyntaxError(
                f'invalid argument index: {token[2]} for template {self.temp_stack[0][0]}'))
            i = int(token[2])
            self.temp_stack[-1].append(('argindex', i))
            self.temp_stack[0][1] |= 1 << i
            return self.temp_stack.append([])
        if ' ' <= token[2] <= '~':
            text = escaped_tokens.get(token[2], token[2])
            for token in Lexer(apply_ascii_operator=False).fromstring(text):
                self.parse_token(token)
        else:
            self.parse_char(state, '\\')
            self.parse_token(token)

    def parse_open(self, cate, char):
        state = self.get_current_state()
        if state.startswith('text'):
            self.new_object(cate)
        else:
            self._assert(state != cate != 'command', FBDSyntaxError(
                "open command operation error"))
            self.current += char

    def parse_close(self, cate, char):
        state = self.get_current_state()
        if state != cate:
            self.parse_char(state, char)
        else:
            self.new_object()
            if cate == 'command':
                cmd = normalize('NFKC', self.curstack()[-1][1])
                if cmd[:2] == 'BP':
                    self.do_comment(cmd)
                elif cmd[:2] == 'ZD':
                    self.curstack().pop()
                    self.do_setter(cmd)
                elif cmd[:1] == '=':
                    self.curstack().pop()
                    self.do_getter(cmd)

    def do_comment(self, cmd):
        self._assert(cmd == 'BP(', FBDCommandError(
            f'command argument error: {cmd}'))
        self.comment.append('')

    def do_setter(self, cmd):
        if cmd == 'ZD)':
            self._assert(self.temp_stack and self.temp_stack[0][1] >= 0, FBDNestingError(
                f'invalid command nesting: {cmd}'))
            name, args = self.temp_stack[0]
            arglength = len(self.temp_stack)-2
            if args > 0:
                self._assert(not args & args + 1, FBDTemplateError(
                    f'use template with wrong length of arguments: {name}'))
                arglength = args.bit_length()-1
            self.templates[name] = [arglength, *self.temp_stack[1:]]
            return self.temp_stack.clear()
        elif '(' in cmd:
            name, _, arg = cmd[2:].partition('(')
            if name.isalnum() and arg in ('', 'D'):
                self._assert(not self.temp_stack, FBDNestingError(
                    f'invalid command nesting: {cmd}'))
                return self.temp_stack.extend([[name, +(arg == 'D')], []])
        raise Exception(f'command argument error: {cmd}')

    def do_getter(self, cmd):
        if cmd == '=':
            self._assert(self.temp_stack and self.temp_stack[0][1] == -1, FBDNestingError(
                f'invalid command nesting: {cmd}'))
            name = self.temp_stack[0][0]
            setter = self.templates[name]
            self._assert(setter[0] == len(self.temp_stack)-1, FBDTemplateError(
                f'use template with wrong length of arguments: {name}'))
            for i in range(1, len(setter)-1):
                stack = setter[i][:]
                if stack and stack[-1][0] == 'argindex':
                    i = stack.pop()[1]
                self.stack.extend(stack)
                self.stack.extend(self.temp_stack[i])
            self.stack.extend(setter[-1])
            return self.temp_stack.clear()
        self._assert(not self.temp_stack, FBDNestingError(
            f'invalid command nesting: {cmd}'))
        name = cmd[1:len(cmd)-(cmd[-1] == '(')]
        self._assert(name in self.templates, FBDTemplateError(
            f'template not found: {name}'))
        setter = self.templates[name]
        if cmd[-1] != '(':
            self._assert(not setter[0], FBDTemplateError(
                f'use template with wrong length of arguments: {name}'))
            self.stack.extend(setter[1])
        else:
            self.temp_stack.extend([[name, -1], []])

    def parse_plain(self, cate, char):
        cur = self.get_current_state()
        if cur.startswith('text'):
            state = f'text@{cate}' if cate != 'text' else 'text'
            cur != state and self.new_object(state)
        self.current += char

    def parse_symbol(self, font, char):
        return self.parse_plain(f'text@{font}', char)

    def parse_operator(self, cate, char):
        if cate == 'escape':
            self.escape = 1
        elif cate == 'pattern':
            self.escape = 2
        elif cate != 'endfeed' and not self.get_current_state().startswith('text'):
            self.current += char
        else:
            self.new_object()
            if cate == 'page_num' and self.temp_stack and self.temp_stack[0][1] >= 0:
                if self.temp_stack[0][1]:
                    self.escape = 3
                else:
                    self.temp_stack.append([])
            elif cate == 'endfeed' and self.temp_stack and self.temp_stack[0][1] == -1:
                self.temp_stack.append([])
            else:
                self.curstack().append(('operator', cate))

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
