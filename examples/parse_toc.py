# -*- coding: utf-8 -*-

from FBDParser.parser import Parser
from FBDParser.charmaps import symbolsA, symbolsB

from collections import deque
from unicodedata import east_asian_width

class TestParser(Parser):
    def __init__(self, fill=40):
        self.toc = []
        self.start_parsing = False

        self.label = u''
        self.pageno = 1
        self.pagenums = deque()

        self.pagenum_fenced = False
        self.fill = fill

    def do_text(self, text, font=''):
        if font == 'symbolA':
            text = text.translate(symbolsA)
        elif font == 'symbolB':
            text = text.translate(symbolsB)
        if self.start_parsing:
            self.label += text.replace(u'〓', u'　')

    def do_page_num(self):
        pageno = self.pagenums.popleft()
        if self.start_parsing:
            self.label += u'({})'.format(pageno) if self.pagenum_fenced else str(pageno)

    def do_linefeed(self):
        if self.start_parsing:
            self.toc.append(self.label)
            self.label = u'　　'

    def do_return(self):
        if self.start_parsing:
            self.toc.append(self.label)
            self.label = u''

    def do_JY(self, form, **args):
        if self.start_parsing:
            width = sum(east_asian_width(c) in 'FWA' for c in self.label)
            self.label = (self.label + u' ').ljust(self.fill - width, u'.') + u' '

    def do_LM(self, form, **args):
        self.pageno += 1

    def do_ML(self, form, kh=None, **args):
        if form == 'infix':
            if kh:
                self.pagenum_fenced = kh == '+'
            self.pagenums.append(self.pageno)
        else:
            self.start_parsing = form == 'prefix'

if __name__ == '__main__':
    parser = TestParser()
    parser.fromfile('docs/simple-toc.fbd')
    for line in parser.toc:
        print(line)
