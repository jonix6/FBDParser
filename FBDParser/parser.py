# -*- coding: utf-8 -*-

from .tokenizer import Tokenizer
from .patterns import parse_command, parse_entity
from .exceptions import FBDEOF

# full width -> ascii
trans = dict(zip(range(0xff01, 0xff5f), range(0x21, 0x7f)))
trans.update({0xe010: 0x2e, 0xe011: 0x2d, 0xe012: 0x2a})  # ".", "-", "*"


def normalize(s):
    '全角转半角'
    return s.translate(trans)


class Parser:
    '''### 书版小样基础解析器

    #### 主要功能

    按照分词（tokenize）结果解析正文、注解、控制符等不同类型片段。

    基础解析器只提供基本类型片段的常规处理接口，具体解析方法请自行扩展。'''

    def do_anonymous(self, cmd):
        '匿名注解（无名称的排版注解，如表格、盒组间隔）解析接口'
        pass

    def do_endfeed(self):
        '文件结束符解析接口，指示解析结束'
        raise FBDEOF('end of feed')

    def do_command(self, cmd):
        '排版注解解析接口'
        cmd = normalize(cmd)
        token = parse_command(cmd)
        if not token:
            self.do_anonymous(cmd)
        else:
            name, form, args = token
            func = getattr(self, 'do_' + name, None)
            func and func(form, **args)

    def do_operator(self, op):
        '控制符解析接口'
        func = getattr(self, 'do_' + op, None)
        func and func()

    def do_text(self, text, font=''):
        '文本解析接口'
        pass

    def do_comment(self, comment):
        '注释解析接口'
        pass

    def do_entity(self, cmd):
        '盘外符解析接口'
        cmd = normalize(cmd)
        name, args = parse_entity(cmd)
        func = getattr(self, 'do_' + name, None)
        func and func(**args)

    def parse(self, objects):
        '解析主程序'
        for obj in objects:
            if obj[0].startswith('text'):
                font = obj[0].partition('@')[-1]
                self.do_text(obj[1], font)
            else:
                try:
                    getattr(self, 'do_' + obj[0])(obj[1])
                except FBDEOF:
                    break

    def fromfile(self, filename, strict=True, apply_ascii_operator=True):
        '从本地文件进行解析'
        self.parse(Tokenizer().fromfile(
            filename, strict=strict, apply_ascii_operator=apply_ascii_operator))

    def frombytes(self, data, strict=True, apply_ascii_operator=True):
        '从二进制字符串进行解析'
        self.parse(Tokenizer().frombytes(
            data, strict=strict, apply_ascii_operator=apply_ascii_operator))

    def fromstring(self, text, apply_ascii_operator=True):
        '从字符串进行解析'
        self.parse(Tokenizer().fromstring(
            text, apply_ascii_operator=apply_ascii_operator))
