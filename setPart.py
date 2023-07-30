import os
import re


def extract_subsections(md_content):
    pattern = r'^## (.+?)$([\s\S]*?)(?=(^## |\Z))'
    matches = re.findall(pattern, md_content, re.MULTILINE)
    return matches


def modify_image_urls(content):
    pattern = r'!\[.*?\]\((daydayup\.assets/.*?)\)'
    new_content = re.sub(pattern, r'![](../\1)', content)
    return new_content


def save_subsections_to_files(subsections):
    if not os.path.exists('芝士'):
        os.mkdir('芝士')

    for title, content, _ in subsections:
        filename = os.path.join('芝士', f"{title}.md")
        modified_content = modify_image_urls(content)
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(modified_content.strip())


def main():
    with open('daydayup.md', 'r', encoding='utf-8') as file:
        md_content = file.read()

    subsections = extract_subsections(md_content)
    save_subsections_to_files(subsections)


if __name__ == "__main__":
    main()
