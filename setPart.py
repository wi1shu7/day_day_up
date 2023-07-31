import os
import re


def replace_first_occurrence(string, old_substring, new_substring):
    index = string.find(old_substring)  # 查找子字符串的索引
    if index != -1:
        # 使用切片操作替换第一次出现的子字符串
        new_string = string[:index] + new_substring + string[index + len(old_substring):]
        return new_string
    else:
        return string


def extract_subsections(md_content):
    pattern = r'^## (.+?)$([\s\S]*?)(?=(^## |\Z))'
    matches = re.findall(pattern, md_content, re.MULTILINE)
    return matches


def modify_image_urls(content):
    pattern = r'!\[.*?\]\((daydayup\.assets/.*?)\)'
    new_content = re.sub(pattern, r'![](../\1)', content)
    return new_content


def save_subsections_to_files(subsections):
    import getToc
    import subprocess

    save_path = r'.\芝士'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    for title, content, _ in subsections:
        filename = os.path.join(save_path, f"{title}.md")
        modified_content = '[TOC]' + modify_image_urls(content)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(modified_content.strip())

        print(f"<---{filename}--->")


def main():
    with open('daydayup.md', 'r', encoding='utf-8') as file:
        md_content = file.read()

    subsections = extract_subsections(md_content)
    save_subsections_to_files(subsections)


if __name__ == "__main__":
    main()
