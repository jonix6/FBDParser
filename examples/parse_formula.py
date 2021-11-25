# -*- coding: utf-8 -*-

from FBDParser.lexer import operators
from FBDParser.parser import Parser

# update math operators
operators[u'±'] = 'pm'

class TestParser(Parser):
    def __init__(self):
        self.formula = ''

    def do_math_block(self):
        self.formula += '\n$$\n'

    def do_text(self, text, font=''):
        self.formula += text

    def do_run_open(self):
        self.formula += '{'

    def do_run_close(self):
        self.formula += '}'

    def do_superscript(self):
        self.formula += '^'

    def do_pm(self):
        self.formula += ' \\pm'

    def do_SX(self, form, **args):
        if form == 'prefix':
            self.formula += ' \\frac{'
        else:
            self.formula += '}'

    def do_KF(self, form, **args):
        if form == 'prefix':
            self.formula += ' \\sqrt{'
        else:
            self.formula += '}'
    
    def do_anonymous(self, cmd):
        self.formula += '}{'

if __name__ == '__main__':
    parser = TestParser()
    parser.fromfile('docs/formula-sample.fbd')
    print(parser.formula)

