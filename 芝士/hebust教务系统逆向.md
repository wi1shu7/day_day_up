```python
https://github.com/wi1shu7/fuck_hebust_login
    
    
class InformationHandler:
    def __init__(self):
        self.modules = {}

    def register_module(self, module_name, module_function):
        self.modules[module_name] = module_function

    def process_information(self, information):
        # 假设信息格式为：-[模块] [参数1] [参数2] ...
        info_list = information.split()
        if len(info_list) < 2:
            raise ValueError("信息格式不正确！")
        
        module_name = info_list[0][2:]  # 去掉前面的“-”
        module_function = self.modules.get(module_name)
        if module_function is None:
            raise ValueError(f"找不到对应的模块：{module_name}")

        arguments = info_list[1:]
        return module_function(*arguments)

# 示例模块函数
def module_function_example(param1, param2):
    return f"模块函数示例：参数1={param1}，参数2={param2}"

if __name__ == "__main__":
    handler = InformationHandler()
    handler.register_module("模块名示例", module_function_example)

    information1 = "-模块名示例 参数1 参数2"
    result1 = handler.process_information(information1)
    print(result1)  # 输出：模块函数示例：参数1=参数1，参数2=参数2

```