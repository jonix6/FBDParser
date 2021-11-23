# -*- coding: utf-8 -*-

"=========================================目录类========================================="

class OutlinePatterns:
    # 自动目录定义注解（MD）
    MD_prefix = r'''(?P<jh>  # 级号
        [1-8])'''

    # 目录注解（ML）
    ML_infix = r'''(?P<kh>  # 排目录时页码两端加括号
        \+)?'''

    # 自动目录登记注解（MZ）
    MZ_prefix = r'''(?:
        {MD_prefix}
        {ML_infix}
        (?P<hh>H)?  # 目录行后换行
    )?'''.format(MD_prefix=MD_prefix, ML_infix=ML_infix)
    ML_prefix = MZ_infix = ''