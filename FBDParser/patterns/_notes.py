
from ._global import _r, length, size, fontset, color, lines
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
    GZ_prefix = rf'''
        {font}  # 字号、字体，缺省字号为正文字高的1/2
        (?:《(?P<hw>.+?)》)?  # 汉字外挂字体
        (?:;(?P<hj>{_r(length)}))?  # 割注文行距，缺省为0
    '''

    # 注文注解（ZW）
    ZW_prefix = rf'''
        (?P<tl>DY)?  # 分栏排时注文不是排在末栏而要通栏排
        (?P<zf>{list_style})?  # 注序号形式
        (?P<xx>\d+)?  # 序号
        (?P<wk>B)?  # 注序号与注文间不留空
        (?P<pf>  # 注文与上一注文是否连排
            P|  # 注文另行开始排
            L\#?{_r(length)}?  # 注文在上一注文末尾连排
        )?
        (?:J(?P<dj>{_r(length)}))?  # 注线与注文内容距离
        (?P<zq>Z)?  # 注序号与注文中线对齐
        (?:,(?P<zh>{_r(size)}))?  # 注序号的字号
        (?P<hy>  # 换页计算序号方式
            ;X|  # 其后的注文换页时按递增方式计算序号
            ;C  # 其后的注文换页时按重置方式计算序号
        )?
    '''

    # 注文说明注解（ZS）
    ZS_infix = rf'''
        {fontset}  # 字号、字体
        (?:(?P<ys>{_r(color)})Z)?  # 文字颜色
        (?:(?P<xs>{_r(color)})X)?  # 注线颜色
        (?:,(?:
            (?P<zf>(?:{list_style}){_r(size)}?)  # 注序号形式
            |(?P<xh>{_r(size)})  # 注序字号
        ))?
        (?:,X(?P<xc>1|\d+/\d+|\d+(?:\.\d+)?mm))?  # 注线长
        (?:,S(?P<sd>{_r(length)}))?  # 注线始点
        (?:,J(?P<dj>{_r(lines)}))?  # 注线与注文内容距离
        (?:,L{border})?  # 注线线型
        (?:,HK{ParagraphPatterns.HK_infix})?  # 注文行宽
        (?:,HJ{ParagraphPatterns.HJ_infix})?  # 注文行距
        (?:,SJ{LayoutPatterns.SJ_infix})?  # 注文缩进
        (?P<dg>,DG)?  # 每个注文悬挂缩进，首行注序号顶格排起
        (?P<qp>\#)?  # 注文竖排时，单双页都排注文
        (?P<lp>%)?  # 注文连排
        (?P<fy>!)?  # 使用多种脚注符形式混排时，保证注文中脚注符右端对齐
    '''
