# -*- coding: utf-8 -*-

from ._global import _f
from ._frames import border, background

"========================================行内控制类=========================================="

class InlinePatterns:
    # 撑满注解（CM）
    CM_prefix = _f(r'(?P<cd>{_r[length]})')  # 长度
    CM_infix = _f(r'{CM_prefix}-(?P<zs>\d+)', CM_prefix=CM_prefix)  # 字/词数

    # 对齐注解（DQ）
    DQ_prefix = CM_prefix + '?'

    # 段首注解（DS）
    DS_infix = DS_prefix = _f(r'''
        (?P<gd>{_r[lines]})。  # 高度
        (?P<kd>{_r[length]})  # 宽度
        {border}?  # 边框说明
        (?:{background})?  # 底纹说明
    ''', border=border, background=background)

    # 位标注解（WB）
    WB_infix = r'(?P<yw>Y)?'  # 右对位

    # 对位注解（DW）
    DW_infix = DW_prefix = r'(?P<wb>\d{,2})'  # 位标数

    # 行中注解（HZ）
    HZ_prefix = ''

    # 基线注解（JX）
    JX_infix = _f(r'''
        (?P<jl>-?{_r[lines]})  # 基线移动的距离，负数表示字符向上移动
        (?:。(?P<zs>\d+))?  # 移动的字数，缺省表示移动一行字符
    ''')

    # 空格注解（KG）
    KG_prefix = _f(r'(?P<kg>-?{_r[length]})')  # 空格长度
    KG_infix = _f(r'{KG_prefix}(?P<zs>。\d*)?', KG_prefix=KG_prefix)  # 空格数

    # 连排注解（PX）
    PX_prefix = _f(r'''
        (?P<qz>{_r[bisize]})?  # 前一个盒子的字号（注意：先横向后纵向）
        (?:\#(?P<hz>{_r[bisize]}))?  # 后一个盒子的字号
        (?P<ys>{_r[color]})?  # 颜色
        (?:K(?P<jj>{_r[length]}))?  # 两组盒子的间距
        (?:G(?P<dj>{_r[length]}))?  # 盒子内容之间的距离
        (?P<pf>[SX])?  # 前后盒子排版顺序（后在上/后在下）
        (?P<dq>[LMR])?  # 盒子内容水平对齐（居左/居中/居右）
        (?P<hq>[UCD])?  # 盒子垂直对齐（上齐/居中/下齐）
        (?P<jx>Z)?  # 在一组上下内容之间加一正线
    ''')