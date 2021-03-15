
from ._global import _r, size, color, length
from ._textstyles import font, TextPatterns

"========================================表格类========================================="

class TablePatterns:
    # 表格注解（BG）
    # 子表注解（ZB）
    BG_suffix = ZB_suffix = rf'''
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
            (?P<dz>{_r(size)})?  # 线字号
        )?
        (?P<ds>{_r(color)})?  # 底线颜色
    '''
    BG_prefix = rf'''
        (?:(?P<qd>\({_r(length)}\)|!))?  # 表格起点
        (?:(?P<bt>BT)|  # 表头
        SD{BG_suffix.replace('<d', '<s')})?  # 换页时上顶线型号、颜色
        (?:XD{BG_suffix.replace('<d', '<x')})?  # 换页时下底线型号、颜色
        (?P<xb>[;,]N)?  # 使用新的方式绘制表格线
        (?:[;,]HT{font.replace('<z', '<h')})?  # 汉字字号、字体
        (?:[;,]WT{TextPatterns.ST_infix.replace('<z', '<w').replace('<bt>', '<wb>')})?  # 外文字号、字体
        (?:[;,]ST{TextPatterns.ST_infix.replace('<z', '<s').replace('<bt>', '<sb>')})?  # 数字字号、字体
        (?:(?:;J|,HJ)(?P<hj>{_r(length)}))?  # 行距
    '''

    # 续表注解（XB）
    XB_infix = rf'''
        (?:,HT{font.replace('<z', '<h')})?  # 汉字字号、字体
        (?:,WT{TextPatterns.ST_infix.replace('<z', '<w').replace('<bt>', '<wb>')})?  # 外文字号、字体
        (?:,ST{TextPatterns.ST_infix.replace('<z', '<s').replace('<bt>', '<sb>')})?  # 数字字号、字体
        (?:,J{_r(length)})?  # 行距
        (?:;(?P<dw>  # 续表内容在表格顶线上位置
            M|(?:  # 居中
            Z|  # 左齐
            Y|  # 右齐
            D)  # 自动根据页码单右双左（缺省）
            -?{_r(length)})
        )?
        (?P<hs>\#)?  # 续表数字采用中文数字
        (?P<nr>.+)  # 续表内容
    '''

    # 表格跨项位标注解（GW）
    # 改排注解（GP）
    # 卧排表格注解（ZP）
    GW_infix = GP_infix = ZB_prefix = ZP_prefix = ''

    # 表行注解（BH）
    BH_arg = rf'''
        ,{BG_suffix.replace('<d', '<z')}  # 左线线型号、颜色
        (?:K(?P<kd>{_r(length)})?)?  # 栏宽
        (?:。(?P<ls>\d+))?  # 栏数
        (?P<dw>DW)?  # 各表行相应栏数的数字项对位(个位对齐)
        (?:(?P<pf>  # 内容排法
            CM|  # 撑满
            YQ|  # 右齐
            ZQ)  # 左齐
            (?P<sj>{_r(length)})?  # 对齐缩进
        )?
    '''
    BH_infix = rf'''
        (?:D{BG_suffix.replace('<d', '<s')})?  # 顶线型号、颜色
        (?:G?(?P<hg>{_r(length)})?|  # 行高
            (?:TK(?P<sk>{_r(length)}))?  # 顶线与内容之间的间距
            (?:JK(?P<xk>{_r(length)}))?  # 底线与内容之间的间距
        )?
        (?P<hq>  # 本行所有内容的整体排法
            JZ|  # 居中（缺省）
            SQ|  # 上齐
            XQ)?  # 下齐
        (?:B(?P<dw>[0-8]\d\d\d))?  # 底纹
        (?P<cs>(?:{_r(BH_arg)})*)  # 各栏参数
        (?:{BG_suffix.replace('<d', '<y')})?  # 右线型号、颜色
    '''

    # 表首注解（BS）
    BS_infix = rf'''
        (?P<qd>[ZY][SX])  # 起点（左/右+上/下）
        (?:X(?P<qx>{_r(length)}))?  # 起点X偏移
        (?:Y(?P<qy>{_r(length)}))?  # 起点Y偏移
    '''
    BS_prefix = rf'''
        {BS_infix}-  # 起点
        (?P<zd>[ZY][SX])  # 终点
        (?:X(?P<zx>{_r(length)}))?  # 终点X偏移
        (?:Y(?P<zy>{_r(length)}))?  # 终点Y偏移   
    '''

    # 表格跨项对位注解（GD）
    GD_infix = r'(?P<wb>\d{,2})'  # 位标数

    # 无线表注解（WX）
    WX_arg = rf'''
        (?P<kd>{_r(length)})  # 栏宽
        (?:KG(?P<jj>{_r(length)}))?  # 与后一栏间的栏间距
        (?:。(?P<ls>[1-9]\d?))?  # 栏数
        (?P<dw>DW)?  # 该栏的数字项对位(个位对齐)
        (?P<pf>CM|YQ|JZ)?  # 内容排法
    '''
    WX_prefix = rf'''
        (?:(?P<qd>\({_r(length)}\)|!))?  # 表格起点
        (?P<dw>DW)?  # 各表行相应栏数的数字项对位(个位对齐)
        (?P<kl>KL)?  # 允许跨栏
        (?P<pf>CM|YQ|JZ)?  # 内容排法
        (?P<cs>{_r(WX_arg)}(?:,{_r(WX_arg)})*)  # 栏说明
    '''
