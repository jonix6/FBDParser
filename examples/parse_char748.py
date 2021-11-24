# -*- coding: utf-8 -*-

from FBDParser.parser import Parser
from FBDParser.charmaps import CMap748, FZ748Map, variants748

cmap = CMap748()


class TestParser(Parser):
    def __init__(self):
        self.text = ''

    def do_FJ(self, form, fj):
        FZ748Map.update(variants748[fj and fj == 'F'])

    def do_text(self, text, font=''):
        self.text += text

    def do_linefeed(self):
        self.text += u'\n\u3000\u3000'

    def do_gb748(self, nm):
        x = int(nm, 16)
        self.text += cmap.decode(x)

    def do_gbk(self, nm):
        x = int(nm, 16)
        self.text += bytearray([x >> 8, x & 0xff]).decode('gb18030')


if __name__ == '__main__':
    parser = TestParser()
    parser.fromfile('docs/cmap748-sample.fbd')
    print(parser.text)
