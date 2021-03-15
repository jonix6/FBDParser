
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

import re


class CommandPatterns(
        ChemicalPatterns, ColumnPatterns, DrawingPatterns, FormulaPatterns,
        FramePatterns, ImagePatterns, IndexPatterns, InlinePatterns,
        LayoutPatterns, MarkPatterns, MongolPatterns, NotePatterns,
        OtherPatterns, OutlinePatterns, PagingPatterns, ParagraphPatterns,
        SideBarPatterns, TablePatterns, TextPatterns, WhitespacePatterns):

    @classmethod
    def get(self, name, form):
        return hasattr(self, f'{name}_{form}')

    @classmethod
    def match(self, name, form, cmd):
        if self.get(name, form):
            m = re.fullmatch(getattr(self, f'{name}_{form}'), cmd, re.X)
            return m and m.groupdict()


class EntityPatterns:
    @staticmethod
    def match(cmd):
        match_any = re.fullmatch(entity, cmd, re.X)
        if match_any:
            name = match_any.lastgroup
            m = re.fullmatch(entities[name], cmd, re.X)
            return m and (name, m.groupdict())
