# -*- coding: utf-8 -*-

from ._global import _f
from ._frames import FramePatterns

"=======================================边文背景类========================================"

# 书眉线
running_head = r'''
    S|  # 双线
    F|  # 反线
    CW|  # 粗文武线
    XW|  # 细文武线
    B  # 不画线
'''

page_number = r'''
(?P<mx>  # 页码类型
    R|  # 罗马数字
    B|  # 阳圈码
    H|  # 阴圈码
    \(|  # 括号码
    \(S|  # 竖括号码
    F|  # 方框码
    FH|  # 阴方框码
    FL|  # 立体方框码
    S|  # 单字多位数码
    \.)?  # 点码
(?P<zm>Z\#?)?  # 中文数字页码；#：小于40的中文页码采用"十廿卅"方式
'''

class WhitespacePatterns:
    # 暗码注解（AM）
    # 边码注解（BM）
    # 无页码注解（WM）
    AM_infix = BM_infix = WM_infix = ''

    # 背景注解（BJ）
    BJ_prefix = _f(r'''
        (?P<zj>  # 左边距
            -?{_r[length]})?,
        (?P<sj>  # 上边距
            -?{_r[length]})?,
        (?P<yj>  # 右边距
            -?{_r[length]})?,
        (?P<xj>  # 下边距
            -?{_r[length]})?
        (?P<fp>\#)?  # 排法与正文排法相反
    ''')

    # 边文注解（BW）
    BW_prefix = _f(r'''(?:  # 初用参数
        (?P<py>  # 边文排在哪些页，缺省表示后续各页均排边文
            B|  # 边文只排在本页
            D|  # 边文排在后续各单页
            S  # 边文排在后续各双页
        )?
        (?:\(
            (?P<wz>[SXZY])?  # 边文位于版心的上/下/左/右面，缺省为上
            (?P<bj>  # 边文与版心之间的距离，缺省为一五号字
                -?{_r[length]})?
            ,(?P<sj>  # 左/上边距，缺省均为0
                -?{_r[length]})?
            ,(?P<zj>  # 右/下边距，缺省均为0
                -?{_r[length]})?
        \))?
        (?:G(?P<gd>  # 边文高
            {_r[length]}\#?))?
        (?:M(?P<qs>\d*)  # 页码的起始页号
            (?:  # 页码型号
                {page_number}|  # 单字页码
                D  # 多字页码
                    (?P<dz>Z)?  # 使用中文数字页码
                    (?P<mk>   # 多字页码宽度
                        {_r[length]})?
                    (?P<mq>[ZY]Q)?\#?  # 多字页码左/右对齐排
            )
        )?
        |  # 继承参数
        X(?P<ds>[DS])?  # 继承前面单/双页边文参数，缺省为各页边文
        (?P<jw>[SXZY])?  # 继承位于页面哪个位置的边文，缺省为上
    )?''', page_number=page_number)

    # 书眉说明注解（MS）
    MS_infix = _f(r'''
        (?P<tp>%)?  # 在蒙文排版中，要同时排竖排词条和横排词条
        (?P<px>X)?  # 表示书眉在下，缺省本参数表示书眉在上
        (?:C(?P<ct>  # 词条在书眉上的格式
            SM|  # 书眉左边排首词条，右边排末词条
            S\WM|  # 书眉上排首词条与末词条，中间用<间隔符>相连
            S|  # 单、双页都排首词条
            DM,SS|  # 单页排末词条，双页排首词条 
            DS,SM|  # 单页排首词条，双页排末词条
            M)  # 单、双页都排末词条
        )?
        (?:J(?P<qk>  # 词条切口距离
            {_r[length]}))?
        {fontset}  # 字号、字体
        (?P<pl>,L)?  # 书眉排在里口
        (?P<pw>,W)?  # 书眉排在外口
        (?:,(?P<mx>  # 书眉线
            {running_head}))?
        (?:(?P<ys>  # 字颜色
            {_r[color]})Z)?
        (?:(?P<xs>  # 线颜色
            {_r[color]})X)?
        (?:。(?P<xj>  # 书眉与眉线之间的距离
            {_r[length]}))?
        (?:,(?P<wj>  # 眉线与正文之间的距离
            {_r[length]}))?
        (?:  # 书眉线调整
            (?:;L(?P<nk>-?{_r[length]}))?  # 书眉线内扩
            (?:;W(?P<wk>-?{_r[length]})!?)?  # 书眉线外扩
            |(?:;K(?P<xk>{_r[length]}))?  # 书眉线宽度
        )?
    ''', running_head=running_head)

    # 单眉注解（DM）
    # 眉眉注解（MM）
    # 双眉注解（SM）
    DM_prefix = MM_prefix = SM_prefix = r'''(?P<lw>  # 书眉排在里/外口
        [LW])?'''

    # 空眉注解（KM）
    KM_infix = _f(r'''
        (?P<mx>  # 书眉线
            {running_head})?
        (?P<tk>T)?  # 能同时控制书眉、词条、边文显示
    ''', running_head=running_head)

    # 背景隐藏注解（BY）
    BY_infix = _f(r'''
        (?P<jy>J)?  # 本页的背景内容隐藏
        (?P<wy>W)?  # 本页的边文内容隐藏
        (?P<yy>YW?)?  # 本页的页码内容隐藏。参数W表示本页页码不占页号，不显示
        (?:(?P<my>M)  # 本页的书眉内容隐藏
            (?P<mx>  # 书眉内容隐藏时的书眉线类型
                Z|{running_head})?
        )?
        (?:(?P<ny>N)  # 本页的页号内容隐藏
            (?P<nf>(?:《.+?》)*)  )?  # 需要隐藏的页号标识符
        (?:(?P<qy>Q)  # 本页的多页分区内容隐藏
            (?P<qf>(?:《.+?》)*)  )?  # 需要隐藏的多页分区名称
    ''', running_head=running_head)

    # 词条注解（CT）
    CT_prefix = r'''(?P<yt>  # 词条为隐词条，不出现在正文
        \#)?'''
    CT_infix = _f(r'''{CT_prefix}
        (?P<kc>!)?  # 词条将被无条件添加到入到书眉中无论上一个词条是否与本词条相同
        (?:K(?P<kg>  # 后加设置的空格字距
            {_r[length]}))?
    ''', CT_prefix=CT_prefix)

    # 多页分区注解（MQ）
    MQ_prefix = _f(r'''
        (?:《(?P<qm>.+?)》)  # 分区名
        (?:
            (?P<cj>  # 分区所在层级
                1|  # 分区位于背景下面
                2|  # 分区位于背景上面，边文下面（缺省）
                3|  # 分区位于边文上面，版心下面
                4)?  # 分区位于版心上面
            (?P<qy>  # 分区出现的页
                D|  # 分区只在单页出现
                S|  # 分区只在双页出现
                M|  # 分区在每页都出现
                B|  # 分区只在本页出现
                X)  # 分区只在下页出现
            # 尺寸、起点、排法、边框说明、底纹说明、居中、反排
            {FramePatterns.FQ_prefix}
            (?P<sp>F)?  # 分区中的文字从右到左竖排
            (?P<dz>%)?  # 分区不在版心中挖空
        )?
    ''', FramePatterns=FramePatterns)
    MQ_infix = r'''
        (?:《(?P<qm>.+?)》)  # 分区名
        (?P<kg>[JH])  # 禁止/激活多页分区
        (?P<cj>[1-4])?  # 分区所在层级
        (?P<sx>[SX])?  # 将分区移到同层所有分区的上/下面
    '''

    # 页码注解（YM）
    YM_infix = YM_prefix = _f(r'''
        (?P<lm>  # 页码用罗马数字
            L|  # 页码用大写罗马数字，但要≤16
            R)?  # 页码用小写罗马数字，但要≤16
        (?P<zh>  # 页码字号
            {_r[size]})
        (?P<zt>{_r[fontname]})  # 页码字体
        (?P<ys>  # 页码颜色
            {_r[color]})?
        (?P<zs>  # 页码两边加装饰符，缺省为不加装饰符
            。|  # 页码两边加一实心圆点
            \-)?  # 页码两边加一条短线
        (?P<yq>  # 页码在页面的对齐方式
            !|\#-?{_r[length]})?
        (?:%(?P<jj>  # 页码与正文间的距离
            -?{_r[length]}))?
        (?:=(?P<qs>\d+))?  # 起始页码
        (?P<sm>,S)?  # 页码在上
        (?:《W(?P<ww>.*?)》)?  # 外文外挂字体名
        (?::(?P<dq>  # 页码对齐方式
            Z|  # 左边对齐
            M|  # 中间对齐（缺省）
            Y)  # 右边对齐
        )?
        (?:[;!](?P<ws>\d+))?  # 页码显示位数
        (?:[;!](?P<dw>  # 页码数字对位方式
            SZ|  # 里口边对齐
            SM|  # 中间对齐
            SY)  # 切口边对齐
        )?
    ''')

    # 页号注解（PN）
    PN_infix = PN_prefix = _f(r'''
        (?:《(?P<bz>.+?)》)?  # 标识符
        (?:-{page_number}  # 页号类型
            (?P<dz>\^)?  # 单字页号
        )?
        (?:Y(?P<cx>  # 页号出现方式
            0|  # 不出现
            1|  # 只在单页出现
            2|  # 只在双页出现
            3|  # 在每页都出现（缺省）
            -\d+)  # 指定出现的次数
        )?
        (?:  # 页号位置
            (?P<ds>[=!])  # 单双页页号的水平位置是一致/对称的
            (?:
                (?:@(?P<yw>0?\d|1[0-2]))  # 预设位置
                |(?P<py>  # 自定义纵向位置（!表示居中）
                    -?{_r[lines]}|!)。
                (?P<px>  # 自定义横向位置（!表示居中）
                    -?{_r[length]}|!)
            )
        )?
        (?:V(?P<fx>[!=]))?  # 与版心排版方向相反/相同
        (?:P(?P<yh>\d+))?  # 当前页号
        (?:\+(?P<jg>\d+))?  # 页号间隔
        (?:K(?P<ws>[2-5]))?  # 页号显示位数，如果页号位数小于要求的显示位数，则在前补0
        (?:,(?P<dw>  # 页号数字对位方式
            SZ|  # 里口边对齐
            SM|  # 中间对齐
            SY)  # 切口边对齐
        )?
    ''', page_number=page_number.replace('R|', '[LR]|'))