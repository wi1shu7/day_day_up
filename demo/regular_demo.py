import re
import traceback
from datetime import datetime

try:
    print("result".center(50, '-'))
    pattern = r'(Office|Word|Excel)2000'
    result = re.search(pattern, 'Office2000')
    print(result)
    print(result.group())
    print(result.group(1))
except Exception:
    print(traceback.format_exc())

try:
    print("result1".center(50, '-'))
    pattern1 = r'(?:Office|Word|Excel)2000'
    result1 = re.search(pattern1, 'Office2000')
    print(result1)
    print(result1.group())
    print(result1.group(1))
except Exception:
    print(traceback.format_exc())

try:
    print("result2".center(50, '-'))
    pattern2 = r'Office(?=95|98|NT|2000)'
    result2 = re.search(pattern2, 'Office2000')
    print(result2)
    print(result2.group())
    print(result2.group(1))
except Exception:
    print(traceback.format_exc())
"""
在正则表达式中，(?=...)是一个“正向先行断言”。
它的作用是查找后面跟着特定模式的内容，但是并不包含该模式。
也就是说，它期待后面的内容匹配其内部的模式，但是它并不会“消耗”或匹配该模式，只是确认它存在。

第一个例子pattern2 = r'Office(?=95|98|NT|2000)'中，(?=95|98|NT|2000)仍然是一个正向先行断言，
它期待后面的内容是"95"，"98"，"NT"或"2000"。
由于没有其他的字符要求紧跟在断言匹配的字符串后面，所以这个模式可以成功匹配到'Office2000'。

第二个例子pattern3 = r'Office(?=95|98|NT|2000)-a'中，(?=95|98|NT|2000)是一个正向先行断言，
它期待后面的内容是"95"，"98"，"NT"或"2000"。
然而，这个断言后面紧接着的是"-a"，所以它期待的实际上是"2000-a"这样的模式。
但是，在正向先行断言中，断言并不会“消耗”或匹配它内部的模式，所以"-a"实际上是在尝试匹配"Office"后面紧接着的内容，而并非"2000"后面的内容。
因此，在字符串'Office2000-a'中，"-a"并不能匹配到，所以整个模式匹配失败。
"""
try:
    print("result3".center(50, '-'))
    pattern3 = r'Office(?=95|98|NT|2000)-a'
    result3 = re.search(pattern3, 'Office2000-a')
    print(result3)
    print(result3.group())
except Exception:
    print(traceback.format_exc())

try:
    print("result4".center(50, '-'))
    pattern4 = r'(?#这是个注释罢了)Office(?!95|98|NT|2000)'
    result4 = re.search(pattern4, 'Office3.1')
    print(result4)
    print(result4.group())
except Exception:
    print(traceback.format_exc())

"""
正则表达式中的断言是一种特殊类型的非捕获组，用于确定某个模式是否在当前位置的前后存在，但并不消耗字符，
也就是说，它们不会影响到正则表达式的主要匹配结果。

1. `(?<=pattern)`: 零宽度正向回查（也称为正向零宽断言）。

这个断言会查找前面是`pattern`的地方。
例如，`(?<=a)b`会匹配所有前面是`a`的`b`。在字符串`abc`中，`b`会被匹配，因为它前面是`a`。
但是，这个断言并不会“消耗”或匹配`a`，所以如果你对整个字符串进行匹配，只有`b`会被返回，而不是`ab`。

注意，正向回查中的`pattern`必须是固定长度的。也就是说，你不能在`pattern`中使用`*`或`+`这样的量词。

2. `(?<!pattern)`: 零宽度负向回查（也称为负向零宽断言）。

这个断言会查找前面不是`pattern`的地方。例如，`(?<!a)b`会匹配所有前面不是`a`的`b`。
在字符串`abc`中，`b`不会被匹配，因为它前面是`a`。
但是，在字符串`dbc`中，`b`会被匹配，因为它前面是`d`，不是`a`。

同样，负向回查中的`pattern`必须是固定长度的。

这些断言非常有用，可以帮助你精确地控制你的正则表达式应该在哪里匹配，而不仅仅是基于被匹配的字符串的内容。
"""

try:
    print("result5".center(50, '-'))
    pattern5 = r'(?# 零宽度正向回查)(?:(?<=Office)|(?<=Word)|(?<=Excel))2000'
    result5 = re.search(pattern5, 'abc-Office2000')
    print(result5)
    print(result5.group())
except Exception:
    print(traceback.format_exc())

try:
    print("result6".center(50, '-'))
    pattern6 = r'(?# 零宽度负向回查)(?<!Office)2000'
    result6 = re.search(pattern6, 'abc-Office-abc-2000')
    print(result6)
    print(result6.group())
except Exception:
    print(traceback.format_exc())

try:
    print("result7".center(50, '-'))
    text = "I love apple pie and cherry pie."
    pattern7 = r"(?=.*apple)(?=.*pie)"
    result7 = re.search(pattern7, text)
    print(result7)
except Exception:
    print(traceback.format_exc())

try:
    print("result8".center(50, '-'))
    test_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(test_str)
    regex = r"(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})"
    subst = r"\1年\2月\3日 \4时\5分\6秒"
    result8 = re.sub(regex, subst, test_str)
    print(result8)
    print('day day up go go die')
except Exception:
    print(traceback.format_exc())