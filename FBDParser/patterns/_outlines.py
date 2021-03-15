
"=========================================目录类========================================="

class OutlinePatterns:
    # 自动目录定义注解（MD）
    MD_prefix = r'(?P<jh>[1-8])'  # 级号

    # 目录注解（ML）
    ML_infix = r'(?P<kh>\+)?'  # 排目录时页码两端加括号

    # 自动目录登记注解（MZ）
    MZ_prefix = rf'''(?:
        {MD_prefix}  # 级号
        {ML_infix}  # 排目录时页码两端加括号
        (?P<hh>H)?  # 目录行后换行
    )?'''
    ML_prefix = MZ_infix = ''