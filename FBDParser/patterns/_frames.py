
from ._global import _r, lace, lines, length, anchor

"========================================版心区块类========================================"

background = r'''
    (?P<dw>B[0-8]\d\d\d)  # 底纹
    (?P<tw>D)?  # 本方框底纹代替外层底纹
    (?P<yw>H)?  # 底纹用阴图
    (?P<pw>\#)?  # 底纹不留余白
'''

border = rf'''(?P<kx>  # 边框说明
    F|  # 反线
    S|  # 双线
    D|  # 点线
    W|  # 不要线也不占位置
    K|  # 表示空边框(无线但占一字宽边框位置)
    Q|  # 曲线
    =|  # 双曲线
    CW|  # 外粗内细文武线
    XW|  # 外细内粗文武线
    {lace}  # 花边线
)'''


class FramePatterns:
    # 方框注解（FK）
    FK_infix = rf'''
        {border}?  # 边框说明
        (?:{background})?  # 底纹说明
        (?:TK(?P<sk>{_r(lines)}))?  # 上边空
        (?:JK(?P<xk>{_r(lines)}))?  # 下边空
        (?P<nk>!)?  # 边框线不占位
    '''
    FK_prefix = rf'''
        {border}?  # 边框说明
        (?:{background})?  # 底纹说明
        (?:
            (?P<gd>{_r(lines)})?  # 方框高度
            (?:。(?P<kd>{_r(length)}))?  # 方框宽度
            |(?:TK(?P<sk>{_r(lines)}))?  # 上边空
            (?:JK(?P<xk>{_r(lines)}))?  # 下边空
        )?
        (?:(?P<dq>  # 内容对齐
            ZQ|  # 左齐
            YQ|  # 右齐
            CM)  # 撑满
            (?P<sj>{_r(length)})?  # 内容缩进
        )?
        (?P<nk>!)?  # 边框线不占位
    '''

    # 分区注解（FQ）
    FQ_prefix = rf'''
        (?P<gd>{_r(lines)})  # 分区高度
        (?:。(?P<kd>{_r(length)}))?  # 分区宽度
        {anchor}  # 起点、排法
        (?:-{border})?  # 边框说明
        (?:{background})?  # 底纹说明
        (?P<jz>Z)?  # 分区内容横排时上下居中，竖排时左右居中
        (?P<fp>!)?  # 与外层横竖排法相反
    '''
