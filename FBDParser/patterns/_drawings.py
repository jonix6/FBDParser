# -*- coding: utf-8 -*-

from ._global import _f
from ._tables import TablePatterns

"=======================================框线底纹类========================================"

line_styles = _f(r'''(?P<xx>  # 线型
    \{{|  # 开花括弧
    \}}|  # 闭花括弧
    \[|  # 开正方括弧
    \]|  # 闭正方括弧
    〔|  # 开斜方括弧
    〕|  # 闭斜方括弧
    F|  # 反线
    S|  # 双线
    D|  # 点线
    Q|  # 曲线
    CW|  # 粗文武线
    XW|  # 细文武线
    =|  # 双曲线
    {lace}  # 花边线
)?''')


class DrawingPatterns:
    # 长度注解（CD）
    CD_infix = _f(r'''
        (?P<wz>  # 画线位置，缺省时表示在当前行的中线上画线
            \#|  # 在当前行的基线上画线
            %)?  # 在当前行的顶线上画线
        {line_styles}
        (?P<cd>  # 长度/高度
            -?{_r[length]}|!-?{_r[lines]})
        (?P<ch>Z)?  # 可拆行
    ''', line_styles=line_styles)

    # 画线注解（HX）
    HX_prefix = _f(r'''
        (?P<wz>  # 画线位置
            {_r[lines]},{_r[length]})\)
        {line_styles}
        (?P<cd>  # 长度/高度
            -?{_r[length]}|!-?{_r[lines]})
        (?P<ch>Z)?  # 可拆行
    ''', line_styles=line_styles)

    # 加底注解（JD）
    JD_infix = _f(r'''
        (?P<dw>[0-8]\d\d\d)  # 底纹编号
        (?:
            (?:\((?P<wz>  # 位置
                {_r[lines]},{_r[length]})\))?
            (?P<gd>  # 高度
                {_r[lines]})
            。(?P<kd>  # 宽度
                {_r[length]})
        )?
        (?P<tw>D)?  # 本方框底纹代替外层底纹
        (?P<yw>H)?  # 底纹用阴图
    ''')

    # 线字号注解（XH）
    XH_infix = _f(r'''(?P<xh>  # 线字号
    {_r[size]})?''')

    # 斜线注解（XX）
    XX_infix = _f(r'''
        (?P<xx>F|S|D|Q|H\d\d\d)?  # 斜线线型
        {TablePatterns.BS_prefix}  # 起止点
    ''', TablePatterns=TablePatterns)
