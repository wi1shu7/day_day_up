import os
import subprocess
import argparse


def replace_first_occurrence(string, old_substring, new_substring):
    index = string.find(old_substring)# 查找子字符串的索引
    if index != -1:
        # 使用切片操作替换第一次出现的子字符串
        new_string = string[:index] + new_substring + string[index + len(old_substring):]
        return new_string
    else:
        return string

def get_toc(preFile, endFile, ifPrint):
    toc: str = subprocess.run(f'gh-md-toc.exe {preFile}', shell=True, capture_output=True, text=True, encoding='utf-8') \
        .stdout \
        .replace("Table of Contents\n=================", '') \
        .replace("Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc.go)", '') \
        .strip()

    with open(preFile, 'r', encoding='utf-8') as f:
        old_file = f.read()

    new_file = replace_first_occurrence(old_file, '[TOC]', toc)

    with open(endFile, 'w', encoding='utf-8') as f:
        f.write(new_file)

    print(toc if ifPrint else "")

if __name__ == "__main__":
    # 创建 ArgumentParser 对象
    parser = argparse.ArgumentParser(description="替换[TOC]为目录")

    # 添加需要接受的命令行参数
    parser.add_argument('-f1', type=str, default='./daydayup.md', help='需要修改的文件')
    parser.add_argument('-f2', type=str, default='./README.md', help='修改后文件的保存')
    parser.add_argument('--print', action='store_true', help='是否输出toc')

    # 解析命令行参数
    args = parser.parse_args()

    # 获取参数值，进行操作
    get_toc(args.f1, args.f2, args.print)

