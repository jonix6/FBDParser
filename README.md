# FBDParser

方正书版BD排版语言解析器，使用Python编写，通过辨析控制字符对方正书版小样内容进行解析，并提供对各种语义片段进行处理的通用接口，以便扩展现有解析器功能。

### 基本语义类型

| 名称        | 含义         |
| ----------- | ------------ |
| text        | 普通文本     |
| command     | 排版注解     |
| linefeed    | 换段符       |
| return      | 换行符       |
| endfeed     | 文件结束符   |
| comment     | 注释         |
| entity      | 盘外符       |
| math_sign   | 数学态切换符 |
| page_num    | 页码替换符   |
| font_switch | 转字体符     |
| superscript | 上标         |
| subscript   | 下标         |

