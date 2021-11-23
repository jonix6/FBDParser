# -*- coding: utf-8 -*-

from ._global import _f
from ._sidebars import column_sep

"========================================分栏类======================================"

class ColumnPatterns:
    # 分栏注解（FL）
    FL_prefix = _f(r'''
        (?:
            (?P<lk>  # 栏宽
                {_r[length]}(?:,{_r[length]}){{1,7}})
            |(?P<ls>[2-8])  # 均分成几栏
        )?
        (?P<hx>!)?  # 栏间画一条以五号字为准的正线
        (?:H(?P<xh>  # 栏线的粗细
            {_r[size]}))?
        (?:-{column_sep})?  # 栏线线型
        (?P<ys>  # 栏线颜色
            {_r[color]})?
        (?:K(?P<jj>  # 栏间距
            {_r[length]}))?
    ''', column_sep=column_sep)
    FL_suffix = r'''(?:
        (?P<xp>X)|  # 后边分栏注解中的内容与前面的内容接排
        (?P<lp>\d+)  # 拉平栏数
    )?'''

    # 对照注解（DZ）
    DZ_prefix = _f(r'''(?:
        (?P<zy>Y)|  # 中英文对照排法，即中文排一页，英文排一页
        {FL_prefix}  # 与分栏注解相同
    )?''', FL_prefix=FL_prefix)

    # 另栏注解（LL）
    LL_infix = ''
