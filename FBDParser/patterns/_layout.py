
from ._global import _r, length, color, lines, size, fontset

"=========================================版面控制类=========================================="

class LayoutPatterns:
    # 版心注解（BX）
    BX_infix = rf'''
        {fontset}  # 字号、字体
        (?P<ys>{_r(color)})?,  # 颜色
        (?P<bg>{_r(length)})。  # 版心高
        (?P<bk>{_r(length)}),  # 版心宽
        (?P<hj>{_r(length)})  # 行距
        (?P<sp>!?)  # 竖排
        (?P<bj>B?)  # 指定不拉行距
        (?P<db>D?)  # 表明页码和书眉相互独立，互不影响
        (?:C
            (?P<cg>\d+(?:\.\d+)?mm)。  # 成品尺寸高
            (?P<ck>\d+(?:\.\d+)?mm)  # 成品尺寸宽
            ,(?P<jz>A)?  # 版心居中排
            (?P<cy>S?\d+(?:\.\d+)?mm)  # 上空或下空尺寸
            ,(?P<cx>Z?\d+(?:\.\d+)?mm)  # 订口或切口尺寸
            ,(?P<cc>\d+(?:\.\d+)?mm)  # 出血尺寸
            ,(?P<qf>Q)?  # 区分左右页
            (?P<qd>F)?  # 起始页为单页
        )?
    '''

    # 彩色注解（CS）
    CS_infix = color.replace('@', r'''
        (?P<ss>  # 设置颜色对象，缺省表示设置字符颜色
            X|  # 设置框线颜色
            D)?  # 设置底纹颜色
    ''') + r'?'

    # 始点注解（SD）
    SD_infix = rf'''(?:
        (?P<xp>X)|  # 将本注解前所排的内容先写入磁盘文件中，然后从当前位置继续排
        (?P<dy>{_r(lines)})?  # 始点垂直位置
        (?:,(?P<dx>{_r(length)}))?  # 始点水平位置
        (?P<xf>;N)?  # 按新方法计算排版的位置
    )?'''

    # 段首缩进注解（SJ）
    SJ_infix = rf'''(?:
        (?P<zk>{_r(size)})  # 缩进单位字号
        (?:。(?P<zs>[1-9]|10))?  # 缩进字数
        |(?:J(?P<sk>{_r(length)}))  # 缩进距离值
    )?'''

    # 上齐注解（SQ）
    # 整体注解（ZT）
    SQ_infix = ZT_prefix = rf'''
        (?P<hj>{_r(lines)})?
    '''

    # 数字注解（SZ）
    SZ_infix = r'''(?P<sp>  # 竖排时数字排法
        H|  # 数字横向连排，但数字不能多于3位
        DB?  # 数字单个单个直立排，B：数字不能拆行
    )?'''

    # 外文竖排（WP）
    WP_infix = r'(?P<dp>D)?'  # 外文字母单个单个直立排

    # 消除单字行注解（XD）
    XD_infix = r'(?P<cx>!)?'  # 后面的文字不消除单字行
