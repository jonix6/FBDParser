
from .tokenizer import Tokenizer
from .patterns import parse_command, parse_entity
from .exceptions import FBDEOF

# full width -> ascii
trans = dict(zip(range(0xff01, 0xff5f), range(0x21, 0x7f)))
trans.update({0xe010: 0x2e, 0xe011: 0x2d, 0xe012: 0x2a})  # ".", "-", "*"


def normalize(s):
    return s.translate(trans)


class Parser:
    def __init__(self):
        self.compilers = {}

    def do_anonymous(self, cmd):
        pass

    def do_endfeed(self):
        raise FBDEOF('end of feed')

    def do_command(self, cmd):
        cmd = normalize(cmd)
        token = parse_command(cmd)
        if not token:
            self.do_anonymous(cmd)
        else:
            name, form, args = token
            func = getattr(self, 'do_' + name, None)
            func and func(form, **args)

    def do_operator(self, op):
        func = getattr(self, 'do_' + op, None)
        func and func()

    def do_text(self, text, font=''):
        pass

    def do_comment(self, comment):
        pass

    def do_entity(self, cmd):
        cmd = normalize(cmd)
        name, args = parse_entity(cmd)
        func = getattr(self, 'do_' + name, None)
        func and func(**args)

    def parse(self, objects):
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
        self.parse(Tokenizer().fromfile(
            filename, strict=strict, apply_ascii_operator=apply_ascii_operator))

    def frombytes(self, data, strict=True, apply_ascii_operator=True):
        self.parse(Tokenizer().frombytes(
            data, strict=strict, apply_ascii_operator=apply_ascii_operator))

    def fromstring(self, text, apply_ascii_operator=True):
        self.parse(Tokenizer().fromstring(
            text, apply_ascii_operator=apply_ascii_operator))
