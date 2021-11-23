# -*- coding: utf-8 -*-

from ._global import _f
from ._frames import border, background

"========================================行内控制类=========================================="

class InlinePatterns:
    # 撑满注解（CM）
    CM_prefix = _f(r'''(?P<cd>  # 长度
        {_r[length]})''')
    CM_infix = _f(r'''
        {CM_prefix}
        -(?P<zs>\d+)  # 字/词数
    ''', CM_prefix=CM_prefix)

    # 对齐注解（DQ）
    DQ_prefix = CM_prefix + '?'

    # 段首注解（DS）
    DS_infix = DS_prefix = _f(r'''
        (?P<gd>  # 高度
            {_r[lines]})。
        (?P<kd>  # 宽度
            {_r[length]})
        {border}?  # 边框说明
        (?:{background})?  # 底纹说明
    ''', border=border, background=background)

    # 位标注解（WB）
    WB_infix = r'''(?P<yw>  # 右对位
        Y)?'''

    # 对位注解（DW）
    DW_infix = DW_prefix = r'''(?P<wb>  # 位标数
        \d{,2})'''

    # 行中注解（HZ）
    HZ_prefix = ''

    # 基线注解（JX）
    JX_infix = _f(r'''
        (?P<jl>  # 基线移动的距离，负数表示字符向上移动
            -?{_r[lines]})
        (?:。(?P<zs>\d+))?  # 移动的字数，缺省表示移动一行字符
    ''')

    # 空格注解（KG）
    KG_prefix = _f(r'''(?P<kg>  # 空格长度
        -?{_r[length]})''')
    KG_infix = _f(r'''
        {KG_prefix}
        (?P<zs>。\d*)?  # 空格数
    ''', KG_prefix=KG_prefix)

    # 连排注解（PX）
    PX_prefix = _f(r'''
        (?P<qz>  # 前一个盒子的字号（注意：先横向后纵向）
            {_r[bisize]})?
        (?:\#(?P<hz>  # 后一个盒子的字号
            {_r[bisize]}))?
        (?P<ys>  # 颜色
            {_r[color]})?
        (?:K(?P<jj>  # 两组盒子的间距
            {_r[length]}))?
        (?:G(?P<dj>  # 盒子内容之间的距离
            {_r[length]}))?
        (?P<pf>[SX])?  # 前后盒子排版顺序（后在上/后在下）
        (?P<dq>[LMR])?  # 盒子内容水平对齐（居左/居中/居右）
        (?P<hq>[UCD])?  # 盒子垂直对齐（上齐/居中/下齐）
        (?P<jx>Z)?  # 在一组上下内容之间加一正线
    ''')