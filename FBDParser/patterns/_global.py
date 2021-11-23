# -*- coding: utf-8 -*-

import re


class _R:
    def __init__(self, kwargs):
        self.kwargs = kwargs

    def __getitem__(self, key):
        return re.sub(r'\(\?P\<.*?\>', '(?:', self.kwargs[key])


def _f(pat, **vars):
    args = dict(globals(), **vars)
    args['_r'] = _R(args)
    return pat.format(**args)


"=======================================公用参数========================================="

# 字号
size = r'''(?:
    (?P<p1>[0124567]["”]?|3|10["”]?|11|63|72|84|96)|  # 常用字号
    (?P<p2>\d+\.(?:\d\d?)?)|  # 磅字号
    (?P<p3>\d{1,4}j)  # 级字号
)'''

# 双向字号
bisize = _f(r'''(?:
    (?P<v>{_r[size]})  # 纵向字号
    (?:,(?P<h>{_r[size]}))?  # 横向字号
)''')

# 行距、字距
length = _f(r'''(?:
    (?P<p1>  # 以字号为单位
        (?:(?P<size>{_r[size]})\:)?  # 单位字号
        (?:\d+(?:\*\d+(?:/\d+)?)?|\*\d+(?:/\d+)?)
    )|
    (?P<p2>\d+(?:\.\d+)?mm)|  # 以毫米为单位
    (?P<p3>\d+(?:\.\d+)?p)|  # 以磅为单位
    (?P<p4>\d+x)  # 以线为单位
)''')

# 空行参数
lines = _f(r'''(?:
    (?P<p1>\d+)|  # 整数行
    (?P<p2>\d*\+{_r[length]})|  # 附加距离
    (?P<p3>\d*\*\d+(?:/\d+)?)  # 行占比
)''')

# 起点
anchor = _f(r'''(?:
    (?P<qd>  # 起点
        \((?:-?{_r[lines]})?,-?{_r[length]}\)|  # 绝对位置
        # 相对当前栏（页）的位置
        # K表示要排到下一栏（页）的初始位置
        ,K?(?:[ZY]|S|[ZY][SX])|,X|,K
    )?
    (?P<pf>,PZ|,PY|,BP)?  # 排法
    (?P<dy>,DY)?  # 在分栏或对照时，内容可跨栏
)''')

# 字体名
fontname = r'[A-Z][A-Z1-9]*'

# 字体集
fontset = _f(r'''
    (?P<zh>  # 字号
        {_r[bisize]})
    (?P<ht>{_r[fontname]})  # 汉字字体
    (?:&(?P<wt>{_r[fontname]}))?  # 外文字体
    (?:&(?P<st>{_r[fontname]}))?  # 数字字体
    (?:《H(?P<hw>.*?)》)?  # 汉字外挂字体名
    (?:《W(?P<ww>.*?)》)?  # 外文外挂字体名
''')

# 颜色
color = r'''@(?P<ys>%?(?:  # CMYK值/百分比
    \d{1,3},\d{1,3},\d{1,3},\d{1,3}|
    \(\d{1,3},\d{1,3},\d{1,3},\d{1,3}\))
)'''

# 花边线
lace = r'H(?:0\d\d|10\d|11[0-7])'
