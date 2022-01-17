# -*- coding: utf-8 -*-

from collections import deque

from .exceptions import FBDCommandError, FBDNestingError, FBDTemplateError, FBDSyntaxError
from .lexer import Lexer
from unicodedata import normalize

# 旧版可转义字符
escaped_tokens = {
    u' ': u'\u3000',
    u'!': u'“',
    u'"': u'”',
    u'#': u'\u3015',
    u'$': u'\ue006',
    u'%': u'\ue00a',
    u'&': u'\ue007',
    u"'": u'\u2019',
    u'(': u'\ue000',
    u')': u'\ue002',
    u'*': u'\u3014',
    u'+': u'\ue00b',
    u',': u'、',
    u'-': u'\ue00b',
    u'.': u'。',
    u'/': u'\u2018',
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
    u'`': u'\u02c8',
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
    '''### 语义片段分割器

    #### 主要功能

    根据从识别器（lexer）返回的字符及其语义类型，对原文本流进行片段分割并传递到解析器（parser）。'''

    def __init__(self):
        self.state_stack = []
        self.current = u''

        self.stack = deque()
        self.escape = ''
        self.comment = []

        self.templates = {}
        self.temp_stack = []

    def reset(self):
        del self.state_stack[:]
        self.current = u''
        del self.stack[:]
        self.escape = ''
        del self.comment[:]
        self.templates.clear()
        del self.temp_stack[:]

    def __assert(self, flag, err):
        if not flag:
            raise err

    def get_current_state(self):
        '获取当前写入的片段类型，默认为文本（text）'
        return self.state_stack[-1] if self.state_stack else 'text'

    def curstack(self):
        '返回当前收集的片段栈'
        return self.temp_stack[-1] if self.temp_stack else self.stack

    def new_object(self, new_state=''):
        '结束写入当前片段，并将此片段存入栈，new_state指定下个片段的类型'
        state = self.state_stack.pop() if self.state_stack else 'text'
        self.curstack().append((state, self.current))
        new_state and self.state_stack.append(new_state)
        self.current = u''

    def parse_token(self, token):
        '处理识别语义类型后的字符'
        if self.comment:  # 正在写入注释
            self.comment_token(token)
        elif self.escape:  # 字符需转义
            self.escape_token(token)
        else:
            type, cate, char = token
            func = getattr(self, 'parse_' + type, None)
            func and func(cate, char)

    def parse_char(self, state, char):
        '处理无语义字符'
        if state == 'text' and u'\ue000' <= char <= u'\ue814':
            # A库符号
            self.new_object('text@symbolA')
        self.current += char

    def comment_token(self, token):
        '将字符写入注释'
        if token[1] == 'command':
            if token[0] == 'open':
                # 若写入的是注解开弧，为避免出现语法错误，
                # 注释需写入一个新片段，以便判断当前注释片段是否是一个注解
                self.comment[-1] += token[2]
                return self.comment.append(u'')
            elif normalize('NFC', self.comment[-1]) == u'BP)':
                # 若写入的是注解闭弧，且当前注释片段为BP)，
                # 则视为注释结束注解〖BP)〗，结束写入注释
                self.comment.pop()
                self.curstack().append(('comment', u'〖'.join(self.comment)))
                del self.comment[:]
                return
        self.comment[-1] += token[2]

    def escape_token(self, token):
        '对字符进行转义，或保留原语义'
        state = self.get_current_state()
        escape, self.escape = self.escape, ''
        if escape == 'raw':  # 字符处理为一般字符
            self.parse_char(state, token[2])
        elif escape == 'shortcut':  # 转义字符
            if ' ' <= token[2] <= '~':
                text = escaped_tokens.get(token[2], token[2])
                for token in Lexer(apply_ascii_operator=False).fromstring(text):
                    self.parse_token(token)
            else:
                self.parse_char(state, '\\')
                self.parse_token(token)
        elif escape == 'math':  # 判断数学态
            if token[0] == 'operator' and token[1] == 'math_sign':
                self.curstack().append(('operator', 'math_block'))
            else:
                self.curstack().append(('operator', 'math_inline'))
                self.parse_token(token)
        elif escape == 'argument':  # 判断有序号形式的模板参数定义
            self.__assert('1' <= token[2] <= '9', FBDSyntaxError(
                'invalid argument index: ' + token[2] + ' for template ' + self.temp_stack[0][0]))
            i = int(token[2])
            # 记录参数插入位置
            self.temp_stack[-1].append(('argindex', i))
            # 参数索引记录到临时栈顶部，模板定义结束时要判断各参数是否连续
            self.temp_stack[0][1] |= 1 << i
            self.temp_stack.append([])

    def parse_open(self, cate, char):
        '处理注解开弧'
        state = self.get_current_state()
        if state.startswith('text'):
            self.new_object(cate)
        else:
            # 若当前写入的是排版注解，会出现语法错误
            self.__assert(state != cate != 'command', FBDSyntaxError(
                "open command operation error"))
            self.current += char

    def parse_close(self, cate, char):
        '处理注解闭弧'
        state = self.get_current_state()
        if state != cate:
            self.parse_char(state, char)
        else:
            self.new_object()
            if cate == 'command':
                # 由于注解和模板注解会影响语法判断，因此要对这些注解进行简单解析
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
        '解析注释开始注解〖BP(〗'
        self.__assert(cmd == u'BP(', FBDCommandError(
            'command argument error: ' + cmd))
        self.comment.append(u'')

    def do_setter(self, cmd):
        '''解析模板定义注解〖ZD(〗〖ZD)〗

        模板定义栈结构: [[模板名称, 参数记录], 片段栈]

        模板存储格式: 模板名称 -> [传参个数，语义片段+]'''
        if cmd == u'ZD)':
            # 判断当前栈是否为模板定义栈
            self.__assert(self.temp_stack and self.temp_stack[0][1] >= 0, FBDNestingError(
                'invalid command nesting: ' + cmd))
            name, args = self.temp_stack[0]
            arglength = len(self.temp_stack)-2
            if args > 0:
                # 模板为有序参数形式，各参数序号需连续
                self.__assert(not args & args + 1, FBDTemplateError(
                    'use template with wrong length of arguments: ' + name))
                arglength = args.bit_length()-1
            self.templates[name] = [arglength] + self.temp_stack[1:]
            del self.temp_stack[:]
            return
        elif '(' in cmd:
            name, _, arg = cmd[2:].partition(u'(')
            if name.isalnum() and arg in (u'', u'D'):
                # 当前不能写入其他模板或模板调用
                self.__assert(not self.temp_stack, FBDNestingError(
                    'invalid command nesting: ' + cmd))
                # 若模板为有序参数形式，参数记录为1
                return self.temp_stack.extend([[name, +(arg == u'D')], []])
        raise Exception('command argument error: ' + cmd)

    def do_getter(self, cmd):
        '''解析模板调用注解〖=X(〗〖=〗

        模板调用栈结构: [[模板名称, -1], 片段栈]'''
        if cmd == u'=':
            # 判断当前栈是否为模板调用栈
            self.__assert(self.temp_stack and self.temp_stack[0][1] == -1, FBDNestingError(
                'invalid command nesting: ' + cmd))
            name = self.temp_stack[0][0]
            setter = self.templates[name]
            # 判断调用的模板传参个数是否正确
            self.__assert(setter[0] == len(self.temp_stack)-1, FBDTemplateError(
                'use template with wrong length of arguments: ' + name))
            # 模板与调用栈拼接，写入工作栈
            for i in range(1, len(setter)-1):
                stack = setter[i][:]
                if stack and stack[-1][0] == 'argindex':
                    i = stack.pop()[1]
                self.stack.extend(stack)
                self.stack.extend(self.temp_stack[i])
            self.stack.extend(setter[-1])
            del self.temp_stack[:]
            return
        # 当前不能写入其他模板或模板调用
        self.__assert(not self.temp_stack, FBDNestingError(
            'invalid command nesting: ' + cmd))
        name = cmd[1:len(cmd)-(cmd[-1] == '(')]
        self.__assert(name in self.templates, FBDTemplateError(
            'template not found: ' + name))
        setter = self.templates[name]
        if cmd[-1] != u'(':
            # 无参数模板调用不能加括号
            self.__assert(not setter[0], FBDTemplateError(
                'use template with wrong length of arguments: ' + name))
            # 无参数模板直接写入工作栈则可
            self.stack.extend(setter[1])
        else:
            self.temp_stack.extend([[name, -1], []])

    def parse_plain(self, cate, char):
        '处理一般字符'
        cur = self.get_current_state()
        if cur.startswith('text'):
            # 若字体类型与当前的不同，结束写入当前片段
            state = 'text@' + cate if cate != 'text' else 'text'
            cur != state and self.new_object(state)
        self.current += char

    def parse_space(self, cate, char):
        '处理空白字符，连续空格只视为一个'
        if not self.current or self.current[-1] != ' ':
            self.current += u' '

    def parse_symbol(self, font, char):
        '处理用外挂字体的字符'
        return self.parse_plain('text@' + font, char)

    def parse_operator(self, cate, char):
        '处理控制字符'
        if cate == 'pattern':
            # 转义控制符
            self.escape = 'shortcut'
        elif not self.get_current_state().startswith('text'):
            # 不在写入正文，视为一般字符
            self.current += char
        elif cate == 'escape':
            # 清除语义控制符
            self.escape = 'raw'
        else:
            self.new_object()
            if cate == 'math_sign':
                # 数学态控制符，要判断下一个字符是否与其相同
                self.escape = 'math'
            elif cate == 'page_num' and self.temp_stack and self.temp_stack[0][1] >= 0:
                # 页码替换符，模板定义时为传参标记
                if self.temp_stack[0][1]:
                    # 模板定义含序号，下一个字符需为序号
                    self.escape = 'argument'
                else:
                    self.temp_stack.append([])
            elif cate == 'endfeed' and self.temp_stack and self.temp_stack[0][1] == -1:
                # 文件结束符，模板调用时为模板调用标记
                self.temp_stack.append([])
            else:
                self.curstack().append(('operator', cate))

    def parse_control(self, cate, char):
        pass

    def tokenize(self, tokens):
        '分割语义片段'
        for token in tokens:
            self.parse_token(token)
            while self.stack:
                yield self.stack.popleft()
        self.new_object()
        while self.stack:
            yield self.stack.popleft()

    def fromfile(self, filename, strict=True, apply_ascii_operator=True):
        '从本地文件进行分词'
        device = Lexer(
            strict=strict, apply_ascii_operator=apply_ascii_operator)
        return self.tokenize(device.fromfile(filename))

    def frombytes(self, data, strict=True, apply_ascii_operator=True):
        '从二进制字符串进行分词'
        device = Lexer(
            strict=strict, apply_ascii_operator=apply_ascii_operator)
        return self.tokenize(device.frombytes(data))

    def fromstring(self, text, apply_ascii_operator=True):
        '从字符串进行分词'
        return self.tokenize(Lexer(apply_ascii_operator=apply_ascii_operator).fromstring(text))
