# FBDParser

方正书版 BD 排版语言解析器，使用 Python 编写，通过辨析控制字符对方正书版小样内容进行解析，并提供对各种语义片段进行处理的通用接口，以便扩展现有解析器功能。

### 支持功能

+ 全部书版注解、公用参数、盘外符辨析；
+ 方正 748 字库、书版 AB 库字符映射表，并提供部分字符的同义 Unicode 字符映射；
+ 兼容书版 6 / 7 / 9 / 10 / 2008 / 11 版本的语法规则。

### 使用示例

将参考文档（[basic-convert.fbd](https://github.com/jonix6/FBDParser/blob/main/examples/docs/basic-convert.fbd)）转换为Markdown

```Python
import codecs

# 基础解析器
from FBDParser.parser import Parser

# A、B库符号
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
    parser.fromfile('basic-convert.fbd')
    parser.close()
```



### 基本语义类型

| 名称        | 含义       |
| ----------- | ---------- |
| text        | 普通文本   |
| space       | 空白字符   |
| command     | 排版注解   |
| linefeed    | 换段符     |
| return      | 换行符     |
| endfeed     | 文件结束符 |
| comment     | 注释       |
| entity      | 盘外符     |
| math_inline | 正文数学态 |
| math_block  | 独立数学态 |
| page_num    | 页码替换符 |
| font_switch | 转字体符   |
| superscript | 上标       |
| subscript   | 下标       |
| hyphen      | 连字符     |

