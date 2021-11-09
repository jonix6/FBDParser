# -*- coding: utf-8 -*-

from collections import deque

from .exceptions import FBDCommandError, FBDNestingError, FBDTemplateError, FBDSyntaxError
from .lexer import Lexer
from unicodedata import normalize

escaped_tokens = {
    u' ': u'　',
    u'!': u'“',
    u'"': u'”',
    u'#': u'〕',
    u'$': u'\ue006',
    u'%': u'\ue00a',
    u'&': u'\ue007',
    u"'": u'’',
    u'(': u'\ue000',
    u')': u'\ue002',
    u'*': u'〔',
    u'+': u'\ue00b',
    u',': u'、',
    u'-': u'\ue00b',
    u'.': u'。',
    u'/': u'‘',
    u'0': u'〖HT',
    u'1': u'〖ST',
    u'2': u'〖WT',
    u'3': u'〖BH',
    u'4': u'〖BT',
    u'5': u'·',
    u'6': u'【',
    u'7': u'】',
    u'8': u'〈',
    u'9': u'〉',
    u':': u'…',
    u';': u'\ue004',
    u'<': u'《',
    u'=': u'\ue003',
    u'>': u'》',
    u'?': u'→',
    u'@': u'\ue005',
    u'A': u'〖BT(',
    u'B': u'〖BG(',
    u'C': u'〖CT(',
    u'D': u'〖DS(',
    u'E': u'〖FK(',
    u'F': u'〖FL(',
    u'G': u'〖FQ(',
    u'H': u'〖HS(',
    u'I': u'〖JY(',
    u'J': u'〖JZ(',
    u'K': u'〖KX(',
    u'L': u'〖LT(',
    u'M': u'〖ML(',
    u'N': u'〖BS(',
    u'O': u'〖ZB(',
    u'P': u'〖HZ(',
    u'Q': u'〖QX(',
    u'R': u'〖JB(',
    u'S': u'〖SX(',
    u'T': u'〖TS(',
    u'U': u'〖ZZ(',
    u'V': u'〖ZW(',
    u'W': u'〖WX(',
    u'X': u'〖XZ(',
    u'Y': u'〖YY(',
    u'Z': u'〖ZK(',
    u'^': u'\ue010',
    u'-': u'—',
    u'`': u'ˈ',
    u'a': u'〖BT)〗',
    u'b': u'〖BG)',
    u'c': u'〖CT)〗',
    u'd': u'〖DS)〗',
    u'e': u'〖FK)〗',
    u'f': u'〖FL)',
    u'g': u'〖FQ)〗',
    u'h': u'〖HS)〗',
    u'i': u'〖JY)〗',
    u'j': u'〖JZ)〗',
    u'k': u'〖KX)〗',
    u'l': u'〖LT)〗',
    u'm': u'〖ML)〗',
    u'n': u'〖BS)〗',
    u'o': u'〖ZB)',
    u'p': u'〖HZ)〗',
    u'q': u'〖QX)〗',
    u'r': u'〖JB)',
    u's': u'〖SX)〗',
    u't': u'〖TS)〗',
    u'u': u'〖ZZ)〗',
    u'v': u'〖ZW)〗',
    u'w': u'〖WX)〗',
    u'x': u'〖XZ)〗',
    u'y': u'〖YY)〗',
    u'z': u'〖ZK)〗',
    u'{': u'\ue008',
    u'|': u'\ue011',
    u'}': u'\ue009',
    u'~': u'\ue001'
}


class Tokenizer:
    def __init__(self):
        self.state_stack = []
        self.current = u''

        self.stack = deque()
        self.escape = 0
        self.comment = []

        self.templates = {}
        self.temp_stack = []

    def reset(self):
        del self.state_stack[:]
        self.current = u''
        del self.stack[:]
        self.escape = 0
        del self.comment[:]
        self.templates.clear()
        del self.temp_stack[:]

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
        self.current = u''

    def parse_token(self, token):
        if self.comment:
            self.comment_token(token)
        elif self.escape:
            self.escape_token(token)
        else:
            type, cate, char = token
            func = getattr(self, 'parse_' + type, None)
            func and func(cate, char)

    def parse_char(self, state, char):
        if state == 'text' and u'\ue000' <= char <= u'\ue814':
            self.new_object('text@symbolA')
        self.current += char

    def comment_token(self, token):
        if token[1] == 'command':
            if token[0] == 'open':
                self.comment[-1] += token[2]
                return self.comment.append(u'')
            elif normalize('NFC', self.comment[-1]) == u'BP)':
                self.comment.pop()
                self.curstack().append(('comment', u''.join(self.comment)))
                del self.comment[:]
                return
        self.comment[-1] += token[2]

    def escape_token(self, token):
        state = self.get_current_state()
        escape, self.escape = self.escape, 0
        if escape == 1:
            return self.parse_char(state, token[2])
        elif escape == 3:
            self._assert('1' <= token[2] <= '9', FBDSyntaxError(
                'invalid argument index: ' + token[2] + ' for template ' + self.temp_stack[0][0]))
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
        self._assert(cmd == u'BP(', FBDCommandError(
            'command argument error: ' + cmd))
        self.comment.append(u'')

    def do_setter(self, cmd):
        if cmd == u'ZD)':
            self._assert(self.temp_stack and self.temp_stack[0][1] >= 0, FBDNestingError(
                'invalid command nesting: ' + cmd))
            name, args = self.temp_stack[0]
            arglength = len(self.temp_stack)-2
            if args > 0:
                self._assert(not args & args + 1, FBDTemplateError(
                    'use template with wrong length of arguments: ' + name))
                arglength = args.bit_length()-1
            self.templates[name] = [arglength] + self.temp_stack[1:]
            del self.temp_stack[:]
            return
        elif '(' in cmd:
            name, _, arg = cmd[2:].partition(u'(')
            if name.isalnum() and arg in (u'', u'D'):
                self._assert(not self.temp_stack, FBDNestingError(
                    'invalid command nesting: ' + cmd))
                return self.temp_stack.extend([[name, +(arg == u'D')], []])
        raise Exception('command argument error: ' + cmd)

    def do_getter(self, cmd):
        if cmd == u'=':
            self._assert(self.temp_stack and self.temp_stack[0][1] == -1, FBDNestingError(
                'invalid command nesting: ' + cmd))
            name = self.temp_stack[0][0]
            setter = self.templates[name]
            self._assert(setter[0] == len(self.temp_stack)-1, FBDTemplateError(
                'use template with wrong length of arguments: ' + name))
            for i in range(1, len(setter)-1):
                stack = setter[i][:]
                if stack and stack[-1][0] == 'argindex':
                    i = stack.pop()[1]
                self.stack.extend(stack)
                self.stack.extend(self.temp_stack[i])
            self.stack.extend(setter[-1])
            del self.temp_stack[:]
            return
        self._assert(not self.temp_stack, FBDNestingError(
            'invalid command nesting: ' + cmd))
        name = cmd[1:len(cmd)-(cmd[-1] == '(')]
        self._assert(name in self.templates, FBDTemplateError(
            'template not found: ' + name))
        setter = self.templates[name]
        if cmd[-1] != u'(':
            self._assert(not setter[0], FBDTemplateError(
                'use template with wrong length of arguments: ' + name))
            self.stack.extend(setter[1])
        else:
            self.temp_stack.extend([[name, -1], []])

    def parse_plain(self, cate, char):
        cur = self.get_current_state()
        if cur.startswith('text'):
            state = 'text@' + cate if cate != 'text' else 'text'
            cur != state and self.new_object(state)
        self.current += char

    def parse_symbol(self, font, char):
        return self.parse_plain('text@' + font, char)

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
        return self.tokenize(device.fromfile(filename))

    def frombytes(self, data, strict=True, apply_ascii_operator=True):
        device = Lexer(
            strict=strict, apply_ascii_operator=apply_ascii_operator)
        return self.tokenize(device.frombytes(data))

    def fromstring(self, text, apply_ascii_operator=True):
        return self.tokenize(Lexer(apply_ascii_operator=apply_ascii_operator).fromstring(text))
