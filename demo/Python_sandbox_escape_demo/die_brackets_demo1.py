def base1(a):
    print(f"base1 -> {a}")
    return a


def base2(cls):
    print(f"base2 -> {cls}")
    return "hello"

@base1
@base2
class MyClass:
    pass