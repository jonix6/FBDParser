# -*- coding: utf-8 -*-

from ._global import _f

"====================================化学结构式类====================================="


class ChemicalPatterns:
    # 反应注解（FY）
    FY_infix = FY_prefix = _f(r'''
        (?P<fh>  # 反应号
            JH\*?|  # 聚合
            KN\*?|  # 可逆
            =|  # 等号
            J  # 实心箭头（缺省）
        )?,?
        (?P<fx>[SXZY])?,?  # 反应方向（上下左右）
        (?P<cd>{_r[length]})?  # 长度
    ''')

    # 结构注解（JG）
    # 相联注解（XL）
    JG_prefix = XL_prefix = ''

    # 邻边注解（LB）
    LB_infix = r'(?P<bh>[1-6](?:,[1-6])*)'  # 边编号

    # 六角环注解（LJ）
    LJ_infix = LJ_prefix = _f(r'''
        (?P<gg>{_r[length]}(?:,{_r[length]})?)?  # 规格
        (?:(?:\A|,)(?P<fx>[HS]))?  # 六角方向（横向，竖向）
        (?:(?:\A|,)  # 各边形式
            (?P<gb>D|  # 单键边
                W\([1-6](?:,[1-6])*\)|  # 无键边
                S\([1-6](?:,[1-6])*\)  # 双键边
                (?:W\([1-6](?:,[1-6])*\))?
            )?
            (?:Y(?P<qy>[01])  # 嵌圆
                (?:\((?P<yj>{_r[length]})\))?  # 嵌圆距离
            )?
        )?
        (?:(?:\A|,)L(?P<lr>[1-6]))?  # 连入角
        (?:\#(?P<nf>\S))?  # 内嵌字符
    ''')

    # 相联始点注解（LS）
    # 线始注解（XS）
    # 线末注解（XM）
    LS_arg = XS_arg = XM_arg = r'''
        (?P<bh>[1-9]|1\d|20)  # 编号
        (?P<wz>[ZY][SX]?|[SX])  # 位置
    '''
    LS_infix = XS_infix = XM_infix = _f(r'(?P<gd>{_r[LS_arg]}(?:,{_r[LS_arg]})*)', LS_arg=LS_arg)

    # 相联终点注解（LZ）
    LZ_arg = LS_arg + r'''
        (?:,(?P<xx>XJ|KH))?  # 线选择
        (?:,(?P<xw>[SX]))?  # 线位置
        (?:,(?P<xf>F))?  # 反方向，箭头落在始点上
    '''
    LZ_infix = LZ_prefix = _f(r'(?P<gd>{_r[LZ_arg]}(?:,{_r[LZ_arg]})*)', LZ_arg=LZ_arg)

    # 竖排注解（SP）
    SP_prefix = _f(r'''
        (?P<xh>\d+)?  # 字符盒组序号
        (?:G(?P<gd>{_r[lines]}))?  # 竖排字所占的高度
    ''')

    # 连到注解（LD）
    LD_infix = r'''
        (?P<xh>\d+)  # 字符序号
        (?P<wz>[ZY][SX]?|[SX])?  # 位置
    '''

    # 角键注解（JJ）
    JJ_arg = _f(r'''
        (?P<bh>[1-6])  # 角编号
        (?:,(?P<jx>[LSXQD]X|SJ|JT|XS))?  # 键形
        (?:,(?P<fx>[ZY][SX]?|[SX]))?  # 方向
        (?:,(?P<cd>{_r[length]}))?  # 角键长度
    ''')
    JJ_infix = _f(r'(?P<jj>{_r[JJ_arg]}(?:;{_r[JJ_arg]})*)', JJ_arg=JJ_arg)

    # 字键注解（ZJ）
    ZJ_arg = _f(r'''
        (?:(?P<jx>[LSXQD]X|SJ|JT|XS),)?  # 键形
        (?:{LD_infix},)?  # 位置
        (?:(?P<fx>)[ZY][SX]?|[SX])  # 方向
        (?:,(?P<cd>{_r[length]}))?  # 字键长度
    ''', LD_infix=LD_infix)
    ZJ_infix = _f(r'(?P<zj>{_r[ZJ_arg]}(?:;{_r[ZJ_arg]})*)', ZJ_arg=ZJ_arg)
