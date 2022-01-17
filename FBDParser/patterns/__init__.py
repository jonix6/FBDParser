# -*- coding: utf-8 -*-

from ._chemical import ChemicalPatterns
from ._columns import ColumnPatterns
from ._drawings import DrawingPatterns
from ._formulas import FormulaPatterns
from ._frames import FramePatterns
from ._images import ImagePatterns
from ._indexes import IndexPatterns
from ._inlines import InlinePatterns
from ._layout import LayoutPatterns
from ._marks import MarkPatterns
from ._mongol import MongolPatterns
from ._notes import NotePatterns
from ._others import OtherPatterns
from ._outlines import OutlinePatterns
from ._pagenavs import PagingPatterns
from ._paragraphs import ParagraphPatterns
from ._sidebars import SideBarPatterns
from ._tables import TablePatterns
from ._textstyles import TextPatterns
from ._whitespaces import WhitespacePatterns

from ._entities import entities, entity
from ..exceptions import FBDCommandError, FBDEntityError

import re, sys
_py2 = sys.version_info < (3, 0)

class CommandPatterns(
        ChemicalPatterns, ColumnPatterns, DrawingPatterns, FormulaPatterns,
        FramePatterns, ImagePatterns, IndexPatterns, InlinePatterns,
        LayoutPatterns, MarkPatterns, MongolPatterns, NotePatterns,
        OtherPatterns, OutlinePatterns, PagingPatterns, ParagraphPatterns,
        SideBarPatterns, TablePatterns, TextPatterns, WhitespacePatterns):
    '''### 书版排版注解解析器
    
    将注解按不同格式进行解析，以字典形式返回各注解参数。
    
    参数名称按语法规则标记为两个小写字母，可调用manual方法获取其含义。'''

    @classmethod
    def get(self, name, form):
        return hasattr(self, name + '_' + form)

    @classmethod
    def pattern(self, name, form):
        if self.get(name, form):
            pat = getattr(self, name + '_' + form)
            if _py2:
                pat = pat.decode('utf-8')
            return re.compile(r'\A(?:' + pat + r')\Z', re.X)

    @classmethod
    def match(self, name, form, cmd):
        pat = self.pattern(name, form)
        m = pat and pat.match(cmd)
        return m and m.groupdict()

    @classmethod
    def manual(self, name, form):
        '各注解参数的详细说明: 缩写 -> 含义'
        if self.get(name, form):
            info = {}
            pat = getattr(self, name + '_' + form)
            if _py2:
                pat = pat.decode('utf-8')
            for m in re.finditer(r'^.*?\(\?P\<(.*?)\>.*(?<!\\)#\s*(.*)$', pat, re.M):
                info[m.group(1)] = m.group(2)
            return info

class EntityPatterns:
    @staticmethod
    def match(cmd):
        match_any = re.match(r'\A(?:' + entity + r')\Z', cmd, re.X)
        if match_any:
            name = match_any.lastgroup
            m = re.match(r'\A(?:' + entities[name] + r')\Z', cmd, re.X)
            return m and (name, m.groupdict())


def get_form(c):
    if c == '(':
        return 'prefix'
    elif c == ')':
        return 'suffix'
    return 'infix'


def parse_command(cmd):
    if len(cmd) >= 2 and 'A' <= cmd[0] <= 'Z' and 'A' <= cmd[1] <= 'Z':
        name, c = cmd[:2], cmd[2:]
        form = c and get_form(c[0]) or 'infix'
        c = c[form != 'infix':]
        has_pattern = CommandPatterns.get(name, form)
        if not has_pattern and form != 'suffix':
            raise FBDCommandError('invalid command: ' + cmd)
        if not has_pattern:
            return name, form, {}
        args = CommandPatterns.match(name, form, c)
        if args is None:
            print(name, form, c, CommandPatterns.pattern(name, form).pattern)
            raise FBDCommandError('command argument error: ' + cmd)
        return name, form, args


def parse_entity(cmd):
    token = EntityPatterns.match(cmd)
    if not token:
        raise FBDEntityError('entity argument error: ' + cmd)
    return token
