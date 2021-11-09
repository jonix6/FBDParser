# -*- coding: utf-8 -*-

from ._global import _f

"================================== 盘外符 ====================================="

entities = {}
entities['zstack'] = r'D(?P<zf>\S{2,5})'  # 单字宽的字
entities['ystack'] = r'''A(?P<zf>\S\S)  # 上下附加字符
    (?P<jx>X)?  # 表示<字符2>附加在<字符1>之下
    (?P<gd>[GDU])?  # 高低位置
    (?P<zy>[1-9])?  # 左右位置
'''
entities['xstack'] = r'''Y(?P<zf>\S\S)  # 附加单字符
    (?P<jz>Z)?  # 表示附加字符排在主字符的左边
    (?P<gd>[GDU])?  # 高低位置
'''
entities['supsub'] = _f(r'''J(?P<zz>\S)  # 附加多字符
    (?:
        (?P<sz>\S{{1,3}})  # 上角字符
        (?P<sg>[GDU])?  # 上角高低位置
    )?
    (?:;
        (?P<xz>\S{{1,3}})  # 下角字符
        (?P<xg>[GDU])?  # 下角高低位置
    )?
    (?:,
        (?:
        WT(?P<wh>{_r[bisize]})  # 外文字号
            (?P<wz>{_r[fontname]})  # 外文字体
        |HT(?P<hh>{_r[bisize]})  # 外文字号
            (?P<hz>{_r[fontname]})  # 外文字体
        )
    )?
''')
entities['gb748'] = r'N?(?P<nm>[0-9A-F]{4})'  # 748编码盘外符
entities['gbk'] = r'G(?P<nm>[0-9A-F]{4})'  # GBK编码盘外符
entities['num_c'] = r'B(?P<sz>\d{2,3})'  # 阳圈码
entities['num_c_n'] = r'H(?P<sz>\d{2,3})'  # 阴圈码
entities['num_p'] = r'\((?P<sz>\d{2,3})'  # 括号码
entities['num_s'] = r'F(?P<sz>\d{2,3})'  # 方框码
entities['num_s_n'] = r'FH(?P<sz>\d\d)'  # 阴方框码
entities['num_s_s'] = r'FL(?P<sz>\d{1,3})'  # 立体方框码
entities['num_d'] = r'\.(?P<sz>\d\d)'  # 点码
entities['num'] = r'(?P<sz>\d{2,3})'  # 一字宽
entities['znum_c'] = r'BZ(?P<dx>\#)?(?P<sz>\d{1,3})'  # 中文阳圈码
entities['znum_c_n'] = r'HZ(?P<dx>\#)?(?P<sz>\d\d)'  # 中文阴圈码
entities['znum_p'] = r'\(Z(?P<dx>\#)?(?P<sz>\d{1,3})'  # 中文横括号码
entities['znum_vp'] = r'\(SZ(?P<dx>\#)?(?P<sz>\d{1,3})'  # 中文竖括号码
entities['znum_s'] = r'FZ(?P<dx>\#)?(?P<sz>\d{1,3})'  # 中文方框码
entities['znum_s_n'] = r'FHZ(?P<dx>\#)?(?P<sz>\d\d)'  # 中文阴方框码
entities['znum_d'] = r'\.Z(?P<dx>\#)?(?P<sz>\d{1,3})'  # 中文点码
entities['znum_s_s'] = r'FHZ(?P<dx>\#)?(?P<sz>\d{1,3})'  # 立体中文方框码
entities['frac_d'] = r'(?P<fz>\d)/(?P<fm>\d\d?)'  # 斜分数
entities['frac_v'] = r'(?P<fz>\d)-(?P<fm>\d)'  # 正分数

entity = '|'.join(_f(r'(?P<{k}>{_r[v]})', k=k, v=v)
                  for k, v in entities.items())
