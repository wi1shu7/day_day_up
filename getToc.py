import os
import subprocess


def replace_first_occurrence(string, old_substring, new_substring):
    index = string.find(old_substring)  # 查找子字符串的索引
    if index != -1:
        # 使用切片操作替换第一次出现的子字符串
        new_string = string[:index] + new_substring + string[index + len(old_substring):]
        return new_string
    else:
        return string


if __name__ == "__main__":
    toc: str = subprocess.run('gh-md-toc.exe daydayup.md', shell=True, capture_output=True, text=True, encoding='utf-8') \
        .stdout \
        .replace("Table of Contents\n=================", '') \
        .replace("Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc.go)", '') \
        .strip()

    with open('./daydayup.md', 'r', encoding='utf-8') as f:
        old_file = f.read()

    new_file = replace_first_occurrence(old_file, '[TOC]', toc)

    with open('./README.md', 'w', encoding='utf-8') as f:
        f.write(new_file)
