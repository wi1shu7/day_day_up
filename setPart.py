import os
import re

SAVA_PATH = r'.\芝士'

def get_files_in_directory(directory_path):
    # 获取目录下的所有文件名
    files = os.listdir(directory_path)
    return files

def delete_files_not_in_list(directory_path, subsections_keys):
    files = get_files_in_directory(directory_path)
    for file in files:
        if file not in subsections_keys:
            file_path = os.path.join(directory_path, file)
            # 删除不属于 subsections_keys 列表的文件
            print(f'remove -> {file}')
            os.remove(file_path)

def extract_subsections(md_content):
    pattern = r'^## (.+?)$([\s\S]*?)(?=(^## |\Z))'
    matches = re.findall(pattern, md_content, re.MULTILINE)
    return matches


def modify_image_urls(content):
    pattern = r'!\[.*?\]\((daydayup\.assets/.*?)\)'
    new_content = re.sub(pattern, r'![](../\1)', content)
    return new_content


def save_subsections_to_files(subsections):
    import subprocess
    global SAVA_PATH

    if not os.path.exists(SAVA_PATH):
        os.mkdir(SAVA_PATH)

    for title, content, _ in subsections:
        filename = os.path.join(SAVA_PATH, f"{title}.md")
        modified_content = '[TOC]' + modify_image_urls(content)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(modified_content.strip())

        print(f"<---{filename}--->")


def main():
    global SAVA_PATH
    with open('daydayup.md', 'r', encoding='utf-8') as file:
        md_content = file.read()

    subsections = extract_subsections(md_content)

    subsections_keys = []
    for i in subsections:
        subsections_keys.append(i[0] + '.md')

    save_subsections_to_files(subsections)
    delete_files_not_in_list(SAVA_PATH, subsections_keys)



if __name__ == "__main__":
    main()
