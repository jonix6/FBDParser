# -*- coding: utf-8 -*-

from ._global import _f

"========================================边栏类======================================"

# 栏间线
column_sep = _f(r'''(?P<xx>  # 栏线线型
    F|  # 反线
    S|  # 双线
    Z|  # 正线（缺省）
    D|  # 点线
    Q|  # 曲线
    =|  # 双曲线
    CW|  # 外粗内细文武线
    XW|  # 外细内粗文武线
    {lace}  # 花边线
)''')

class SideBarPatterns:
    # 边边注解（BB）
    BB_infix = _f(r'''
        {fontset}  # 字号、字体
        (?P<ys>{_r[color]})?  # 颜色
    ''')

    # 边栏注解（BL）
    BL_arg = _f(r'''
        。(?P<lk>,?{_r[length]}|{_r[length]},{_r[length]})  # 版心内外栏宽
        (?:!
            (?:{column_sep}  # 栏线线型
                (?P<xh>{_r[size]})?  # 栏线字号
            )?
            (?P<xs>{_r[color]})?  # 栏线颜色
        )?
        (?:K(?P<jj>{_r[length]}))?  # 主副栏间距
    ''', column_sep=column_sep)
    BL_prefix = _f(r'''
        (?:
            1(?P<l1>{_r[BL_arg]})  # 第一个副栏参数
            (?:;2(?P<l2>{_r[BL_arg]}))?  # 第二个副栏参数
            |2(?P<l3>{_r[BL_arg]})  # 第二个副栏参数（独立）
        )(?P<hl>,X)?  # 每次换页后副栏与主栏/另一副栏左右位置互换
    ''', BL_arg=BL_arg)

    # 边注注解（BZ）
    BZ_prefix = r'''
        (?P<lh>[12])?  # 边注排的副栏序号
        (?P<cy>\#)?  # 边注自动拆页
    '''
