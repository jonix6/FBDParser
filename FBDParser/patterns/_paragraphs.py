# -*- coding: utf-8 -*-

from ._global import _f

"=========================================行控制类=========================================="

class ParagraphPatterns:
    # 标题定义注解（BD）
    BD_infix = _f(r'''
        (?P<jh>[1-8]),  # 级号
        {fontset}  # 字号、字体
        (?P<ys>{_r[color]})?  # 颜色
        (?P<hs>{_r[lines]})  # 标题行数
        (?:S(?P<sk>{_r[lines]}))?  # 上空行数
        (?:Q(?P<qk>{_r[length]}))?  # 行前距
    ''')

    # 标题注解（BT）
    BT_infix = _f(r'''
        (?P<jh>[1-8])  # 级号
        (?P<hk>[\+\-]{_r[lines]})?  # 附加行空
        (?P<gt>\#?)  # 允许孤题
    ''')
    BT_prefix = BT_infix.replace(r'[1-8]', r'[1-8]+')  # 多级连排

    # 改宽注解（GK）
    # 前后注解（QH）
    GK_infix = QH_infix = QH_prefix = _f(r'''(?:
        (?P<zy>-?{_r[length]}!?)  # 左右缩进
        |(?P<zs>-?{_r[length]})?  # 左缩进
        !(?P<ys>-?{_r[length]})  # 右缩进
    )''')

    # 行距注解（HJ）
    HJ_infix = _f(r'(?P<hj>{_r[length]})?')

    # 行宽注解（HK）
    HK_infix = _f(r'''
        (?P<hk>{_r[length]})?  # 行宽
        (?:,(?P<bk>!?{_r[length]}))?  # 内边空，有!时表示左边空
    ''')

    # 行齐注解（HQ）
    HQ_infix = r'''(?P<hq>
        B|  # 行末不对齐，外文字不自动加连字符
        K  # 行末对齐，但外文字不自动加连字符，用字间拉空实现齐行
    )?'''  # 无参数表示注解后内容行末对齐，且外文字自动加连字符

    # 行数注解（HS）
    HS_infix = _f(r'''
        (?:
            (?P<hg>{_r[lines]})  # 行数内容高
            |(?:TK(?P<sk>{_r[lines]}))?  # 内容上空
            (?:JK(?P<xk>{_r[lines]}))?  # 内容下空
        )?
        (?P<jz>Z)?  # 内容居中排
        (?P<gt>\#)?  # 允许孤题，在标题和行数后不自动带一行文字
    ''')
    HS_prefix = HS_infix.replace(r'(?P<jz>Z)', r'(?P<jz>[ZQ])')  # Q：内容整体居中排

    # 行移注解（HY）
    HY_infix = _f(r'(?P<hy>D|{_r[length]})?')  # 行移参数：D行移距离取缺省距离，即：字高+行距

    # 居右注解（JY）
    JY_infix = _f(r'''
        (?:  # 居右内容前用字符充满
            (?:(?P<ld>。)|  # 用点线充满
                D(?P<lf>[^\s〖〗]))  # 自定义字符充满
            (?P<qk>{_r[length]})?  # 前空字距
        )?
        (?:,(?P<hk>{_r[length]}))? # 后空字距
    ''')
    JY_prefix = r'''
        (?P<zy>Z  # 整体居右
        (?P<cy>\#)?)?  # 可拆页
    '''

    # 居中注解（JZ）
    JZ_infix = _f(r'(?P<zj>{_r[length]})?')  # 字间距
    JZ_prefix = _f(r'(?:{JZ_infix}|{JY_prefix})?'
        , JZ_infix=JZ_infix, JY_prefix=JY_prefix)

    # 空行注解（KH）
    KH_infix = _f(r'''
        (?P<kh>-?{_r[lines]})  # 空行高度
        (?P<xp>[XD])?  # 空行后字符的起始位置（继续/顶格）
    ''')

    # 自换注解（ZH）
    ZH_prefix = ''

    # 自控注解（ZK）
    ZK_prefix = _f(r'''
        (?P<sj>{_r[length]})?  # 缩进
        (?P<wy>\#)?  # 只有在自动换行时缩进去排，而强迫换行时自控不起作用
    ''')