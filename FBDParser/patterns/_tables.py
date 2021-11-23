# -*- coding: utf-8 -*-

from ._global import _f
from ._textstyles import font, TextPatterns

"========================================表格类========================================="


class TablePatterns:
    # 表格注解（BG）
    # 子表注解（ZB）
    BG_suffix = ZB_suffix = _f(r'''
        (?:
            (?P<dx>  # 底线线型号
                F|  # 反线
                S|  # 双线
                W|  # 无线
                Z|  # 正线（缺省）
                D|  # 点线
                Q|  # 曲线
                =  # 双曲线
            )
            (?P<dz>  # 底线字号
                {_r[size]})?
        )?
        (?P<ds>  # 底线颜色
            {_r[color]})?
    ''')
    BG_prefix = _f(
        r'''(?:(?P<qd>  # 表格起点
            \({_r[length]}\)|!))?
        (?:(?P<bt>BT)|  # 表头
        SD{SD})?  # 换页时上顶线型号、颜色
        (?:XD{XD})?  # 换页时下底线型号、颜色
        (?P<xb>[;,]N)?  # 使用新的方式绘制表格线
        (?:[;,]HT{HT})?  # 汉字字号、字体
        (?:[;,]WT{WT})?  # 外文字号、字体
        (?:[;,]ST{ST})?  # 数字字号、字体
        (?:(?:;J|,HJ)(?P<hj>  # 行距
            {_r[length]}))?
    ''', SD=BG_suffix.replace('<d', '<s').replace('底线', '顶线'),
        XD=BG_suffix.replace('<d', '<x'),
        HT=font.replace('<z', '<h').replace('字', '汉字字'),
        WT=TextPatterns.ST_infix.replace('<z', '<w')
        .replace('<bt>', '<wb>').replace('字', '外文字'),
        ST=TextPatterns.ST_infix.replace('<z', '<s')
        .replace('<bt>', '<sb>').replace('字', '数字字'))

    # 续表注解（XB）
    XB_infix = _f(
        r'''(?:,HT{HT})?  # 汉字字号、字体
        (?:,WT{WT})?  # 外文字号、字体
        (?:,ST{ST})?  # 数字字号、字体
        (?:J(?P<hj>  # 行距
            {_r[length]}))?
        (?:;(?P<dw>  # 续表内容在表格顶线上位置
            M|(?:  # 居中
            Z|  # 左齐
            Y|  # 右齐
            D)  # 自动根据页码单右双左（缺省）
            -?{_r[length]})
        )?
        (?P<hs>\#)?  # 续表数字采用中文数字
        (?P<nr>.+)  # 续表内容
    ''',
        HT=font.replace('<z', '<h').replace('字', '汉字字'),
        WT=TextPatterns.ST_infix.replace('<z', '<w')
        .replace('<bt>', '<wb>').replace('字', '外文字'),
        ST=TextPatterns.ST_infix.replace('<z', '<s')
        .replace('<bt>', '<sb>').replace('字', '数字字'))

    # 表格跨项位标注解（GW）
    # 改排注解（GP）
    # 卧排表格注解（ZP）
    GW_infix = GP_infix = ZB_prefix = ZP_prefix = ''

    # 表行注解（BH）
    BH_arg = _f(r'''
        ,{BG_suffix}  # 左线线型号、颜色
        (?:K(?P<kd>{_r[length]})?)?  # 栏宽
        (?:。(?P<ls>\d+))?  # 栏数
        (?P<dw>DW)?  # 各表行相应栏数的数字项对位(个位对齐)
        (?:(?P<pf>  # 内容排法
            CM|  # 撑满
            YQ|  # 右齐
            ZQ)  # 左齐
            (?P<sj>{_r[length]})?  # 对齐缩进
        )?
    ''', BG_suffix=BG_suffix.replace('<d', '<z').replace('底线', '左线'))
    BH_infix = _f(
        r'''(?:D{BG_suffix_s})?  # 顶线型号、颜色
        (?:G?(?P<hg>  # 行高
            {_r[length]})?|
            (?:TK(?P<sk>  # 顶线与内容之间的间距
                {_r[length]}))?
            (?:JK(?P<xk>  # 底线与内容之间的间距
                {_r[length]}))?
        )?
        (?P<hq>  # 本行所有内容的整体排法
            JZ|  # 居中（缺省）
            SQ|  # 上齐
            XQ)?  # 下齐
        (?:B(?P<dw>[0-8]\d\d\d))?  # 底纹
        (?P<cs>  # 各栏参数
            (?:{_r[BH_arg]})*)
        (?:{BG_suffix_y})?  # 右线型号、颜色
    ''', BG_suffix_s=BG_suffix.replace('<d', '<s').replace('底线', '顶线'),
        BG_suffix_y=BG_suffix.replace('<d', '<y').replace('底线', '右线'),
        BH_arg=BH_arg)

    # 表首注解（BS）
    BS_infix = _f(r'''
        (?P<qd>[ZY][SX])  # 起点（左/右+上/下）
        (?:X(?P<qx>  # 起点X偏移
            {_r[length]}))?
        (?:Y(?P<qy>  # 起点Y偏移
            {_r[length]}))?
    ''')
    BS_prefix = _f(r'''
        {BS_infix}-  # 起点
        (?P<zd>[ZY][SX])  # 终点
        (?:X(?P<zx>  # 终点X偏移
            {_r[length]}))?
        (?:Y(?P<zy>  # 终点Y偏移
            {_r[length]}))?
    ''', BS_infix=BS_infix)

    # 表格跨项对位注解（GD）
    GD_infix = r'''(?P<wb>\d{,2})  # 位标数
    '''

    # 无线表注解（WX）
    WX_arg = _f(r'''
        (?P<kd>{_r[length]})  # 栏宽
        (?:KG(?P<jj>{_r[length]}))?  # 与后一栏间的栏间距
        (?:。(?P<ls>[1-9]\d?))?  # 栏数
        (?P<dw>DW)?  # 该栏的数字项对位(个位对齐)
        (?P<pf>CM|YQ|JZ)?  # 内容排法
    ''')
    WX_prefix = _f(r'''
        (?:(?P<qd>  # 表格起点
            \({_r[length]}\)|!))?
        (?P<dw>DW)?  # 各表行相应栏数的数字项对位(个位对齐)
        (?P<kl>KL)?  # 允许跨栏
        (?P<pf>CM|YQ|JZ)?  # 内容排法
        (?P<cs>  # 栏说明
            {_r[WX_arg]}(?:,{_r[WX_arg]})*)
    ''', WX_arg=WX_arg)
