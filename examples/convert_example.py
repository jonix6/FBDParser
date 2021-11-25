# -*- coding: utf-8 -*-

import codecs
from FBDParser.parser import Parser
from FBDParser.charmaps import symbolsA, symbolsB


class TestConverter(Parser):
    def __init__(self, filename):
        self.fp = codecs.open(filename, 'w', encoding='utf-8')
        self.parsing = ''

    def close(self):
        self.fp.close()

    # 解析正文
    def do_text(self, text, font=''):
        if font == 'symbolA':
            text = text.translate(symbolsA)
        elif font == 'symbolB':
            text = text.translate(symbolsB)
        self.fp.write(text)

    # 解析换行符
    def do_return(self):
        self.fp.write('  \n')

    # 解析换段符
    def do_linefeed(self):
        self.fp.write('\n\n')

    # 解析标题
    def do_BT(self, form, jh, **args):
        self.fp.write('\n' + '#' * int(jh) + ' ')

    def do_anonymous(self, cmd):
        if self.parsing.startswith('table-'):
            self.fp.write('|')
        else:
            self.fp.write('}{')

    # 解析表格
    def do_BG(self, form, **args):
        if form == 'prefix':
            self.parsing = 'table-start'
            self.fp.write('\n|')
        else:
            self.parsing = ''
            self.fp.write('|\n')

    def do_BH(self, form, cs, **args):
        if self.parsing == 'table-start':
            self.parsing = 'table-head-' + str(cs.count('K'))
        else:
            self.fp.write('|\n')
            if self.parsing.startswith('table-head-'):
                numcols = int(self.parsing.rpartition('-')[-1])
                self.fp.write('|--' * numcols + '|\n')
                self.parsing = 'table-row'

    # 解析公式
    def do_math_block(self):
        self.fp.write('\n$$\n')

    def do_SX(self, form, **args):
        self.fp.write(' \\frac{' if form == 'prefix' else '}')

    def do_superscript(self):
        self.fp.write('^')

    def do_subscript(self):
        self.fp.write('_')

    # 解析化学式
    def do_font_switch(self):
        if not self.parsing:
            self.fp.write('\\ce{ ')
            self.parsing = 'chemical'
        else:
            self.fp.write(' }')
            self.parsing = ''

    def do_FY(self, form, **args):
        self.fp.write(' ->[' if form == 'prefix' else '] ')


if __name__ == '__main__':
    parser = TestConverter('test.md')
    parser.fromfile('docs/basic-convert.fbd')
    parser.close()
