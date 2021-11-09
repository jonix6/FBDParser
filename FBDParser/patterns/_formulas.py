# -*- coding: utf-8 -*-

from ._global import _f

"=====================================数学公式类======================================"


class FormulaPatterns:
    # 阿克生注解（AK）
    AK_infix = r'''
        (?P<zm>[a-zA-Z\u0391-\u0451])\s*  # 字母
        (?P<ak>[\:\-\=~→←。\*·¨ˇ\^\u0308])  # 阿克生符
        (?P<jd>D?)  # 指定附加字符需降低安排位置
        (?P<wz>[1-9]?)  # 调节阿克生符位置的左右
    '''

    # 除号注解（CH）
    # 方程号注解（FH）
    CH_prefix = FH_infix = ''

    # 顶底注解（DD）
    DD_arg = _f(r'''
        (?P<w>  # 位置，缺省时居中排
            Z|  # 左对齐
            Y|  # 右对齐
            M)?  # 撑满排
        (?P<j>-?{_r[length]})?  # 附加距离
    ''')
    DD_prefix = _f(
        r''' # 单项参数
        (?P<d0>X?  # 表示顶底内容加在下面
            {DD_arg_0})
        |  # 双项参数
        (?:{DD_arg_1}(?:;{DD_arg_2})?)
    ''', DD_arg_0=DD_arg.replace('<w>', '<w0>').replace('<j>', '<j0>'),
        DD_arg_1=DD_arg.replace('<w>', '<w1>').replace('<j>', '<j1>'),
        DD_arg_2=DD_arg.replace('<w>', '<w2>').replace('<j>', '<j2>'))

    # 方程注解（FC）
    FC_prefix = r'''
        (?P<kh>[\{{\}}\(\)])?  # 边括号
        (?P<zt>J)?  # 公式作为一个整体，禁止拆页
    '''

    # 行列注解（HL）
    HL_arg = _f(r'''
        (?P<lh>\d+),  # 列号
        (?:(?P<lj>{_r[length]}[ZY]?)|  # 列距（与左/右对齐）
        (?P<wz>[ZY]))  # 左/右对齐
    ''')
    HL_prefix = _f(r'''
        (?P<ls>\d+)  # 总列数
        (?P<xx>[FSZDQ=])?  # 分割线线型
        (?::
            (?P<lx>{_r[HL_arg]}(?:;{_r[HL_arg]})*)  # 列信息
        )?
    ''', HL_arg=HL_arg)

    # 界标注解（JB）
    _JB_open = r'[\(\{〔\[\|\/\\\=]'  # 开界标符
    _JB_close = r'[\)\}〕\]\|\/\\\=]'  # 闭界标符
    JB_prefix = _f(r'''
        (?P<kf>{_JB_open})?  # 开界标符
        (?P<jz>Z)?  # 界标符居中
    ''', _JB_open=_JB_open)
    JB_suffix = _f(r'(?P<bf>{_JB_close})?', _JB_close=_JB_close)  # 闭界标符
    JB_infix = _f(r'''
        (?:<  # 开界标
            (?P<kd>\d+\*?)  # 开界标大小
            (?P<kf>{_JB_open})  # 开界标符
        )|(?:>  # 闭界标
            (?P<bd>\d+\*?)  # 闭界标大小
            (?P<bf>{_JB_close})  # 闭界标符
        )
    ''', _JB_open=_JB_open, _JB_close=_JB_close)

    # 积分注解（JF）
    JF_prefix = r'(?P<fg>[DZ])?'  # 上、下限符号在积分符号的顶端/侧面

    # 开方注解（KF）
    KF_prefix = r'(?P<ks>S)?'  # 指定开方数

    # 添线注解（TX）
    TX_prefix = TX_suffix = _f(r'(?P<jj>-?{_r[length]})?')  # 添线与盒子的距离
    TX_infix = _f(r'''
        (?P<hx>X)?  # 在盒子下面添线
        (?P<bg>B)?  # 添线内容不占高度
        (?P<zk>Z)?  # 添线内容采用窄宽排版
        (?P<xx>[\-\=\~\(\)\{{\}}\[\]〔〕→←])  # 线类型
        {TX_prefix}
    ''', TX_prefix=TX_prefix)

    # 上下注解（SX）
    SX_prefix = _f(r'''
        (?P<cx>C)?  # 指定分数线加长
        (?P<wx>B)?  # 不要分数线
        (?P<dq>[ZY])?  # 上下盒子左/右对齐
        (?P<jj>-?{_r[length]})?  # 上下盒组间的距离
    ''')

    # 左齐注解（ZQ）
    ZQ_prefix = _f(r'(?P<zj>{_r[length]})?')  # 字间距
    ZQ_infix = _f(r'(?P<zs>\d+)(?:,{ZQ_prefix})?', ZQ_prefix=ZQ_prefix)  # 字数
