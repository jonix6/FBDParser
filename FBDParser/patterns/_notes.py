# -*- coding: utf-8 -*-

from ._global import _f
from ._textstyles import font
from ._frames import border
from ._paragraphs import ParagraphPatterns
from ._layout import LayoutPatterns

"=========================================注文类========================================="

# 注序号形式
list_style = r'''
    F|  # 方括号
    Y|  # 阴圈码
    O|  # 阳圈码
    \*|  # “*”号
    K|  # 圆括号
    W|  # 数字码
    N|  # 无码状态下，脚注符不占位也不显示
    G|  # 中括号码［］
    I|  # 中括号码【】
    A|  # 中括号码〖〗
    T|  # ▲
    U|  # ★
    M|  # 阳方框码
    E  # 阴方框码
'''

class NotePatterns:
    # 割注注解（GZ）
    GZ_prefix = _f(r'''
        {font}  # 字号、字体，缺省字号为正文字高的1/2
        (?:《(?P<hw>.+?)》)?  # 汉字外挂字体
        (?:;(?P<hj>  # 割注文行距，缺省为0
            {_r[length]}))?
    ''', font=font)

    # 注文注解（ZW）
    ZW_prefix = _f(r'''
        (?P<tl>DY)?  # 分栏排时注文不是排在末栏而要通栏排
        (?P<zf>  # 注序号形式
            {list_style})?
        (?P<xx>\d+)?  # 序号
        (?P<wk>B)?  # 注序号与注文间不留空
        (?P<pf>  # 注文与上一注文是否连排
            P|  # 注文另行开始排
            L\#?{_r[length]}?  # 注文在上一注文末尾连排
        )?
        (?:J(?P<dj>  # 注线与注文内容距离
            {_r[length]}))?
        (?P<zq>Z)?  # 注序号与注文中线对齐
        (?:,(?P<zh>  # 注序号的字号
            {_r[size]}))?
        (?P<hy>  # 换页计算序号方式
            ;X|  # 其后的注文换页时按递增方式计算序号
            ;C  # 其后的注文换页时按重置方式计算序号
        )?
    ''', list_style=list_style)

    # 注文说明注解（ZS）
    ZS_infix = _f(r'''
        {fontset}  # 字号、字体
        (?:(?P<ys>  # 文字颜色
            {_r[color]})Z)?
        (?:(?P<xs>  # 注线颜色
            {_r[color]})X)?
        (?:,(?:
            (?P<zf>  # 注序号形式
                (?:{list_style}){_r[size]}?)
            |(?P<xh>  # 注序字号
                {_r[size]})
        ))?
        (?:,X(?P<xc>1|\d+/\d+|\d+(?:\.\d+)?mm))?  # 注线长
        (?:,S(?P<sd>  # 注线始点
            {_r[length]}))?
        (?:,J(?P<dj>  # 注线与注文内容距离
            {_r[lines]}))?
        (?:,L{border})?
        (?:,HK{ParagraphPatterns.HK_infix})?  # 注文行宽
        (?:,HJ{ParagraphPatterns.HJ_infix})?  # 注文行距
        (?:,SJ{LayoutPatterns.SJ_infix})?  # 注文缩进
        (?P<dg>,DG)?  # 每个注文悬挂缩进，首行注序号顶格排起
        (?P<qp>\#)?  # 注文竖排时，单双页都排注文
        (?P<lp>%)?  # 注文连排
        (?P<fy>!)?  # 使用多种脚注符形式混排时，保证注文中脚注符右端对齐
    ''', list_style=list_style, border=border.replace('框线', '注线线型'), 
    ParagraphPatterns=ParagraphPatterns, LayoutPatterns=LayoutPatterns)
