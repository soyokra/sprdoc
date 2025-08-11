import os
import sys

import markdown
import shutil


def convert_md_to_html(src_dir, dest_dir, framework):
    """
    递归将源目录中的所有Markdown文件转换为HTML文件，并保持目录结构

    参数:
        src_dir: 源目录路径，包含.md文件
        dest_dir: 目标目录路径，用于存放转换后的.html文件
    """
    # 确保源目录存在
    if not os.path.exists(src_dir):
        print(f"错误: 源目录 '{src_dir}' 不存在")
        return

    # 确保目标目录存在
    os.makedirs(dest_dir, exist_ok=True)

    framework_path = os.path.join("", framework + ".html")
    with open(framework_path, 'r', encoding='utf-8') as framework_file:
        framework_content = framework_file.read()

    # 遍历源目录中的所有项
    for item in os.listdir(src_dir):
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        # 如果是目录，则递归处理
        if os.path.isdir(src_path):
            convert_md_to_html(src_path, dest_path, framework)
        # 如果是Markdown文件，则进行转换
        elif os.path.isfile(src_path) and item.endswith('.md'):
            # 生成目标HTML文件名
            html_filename = os.path.splitext(item)[0] + '.html'
            html_dest_path = os.path.join(dest_dir, html_filename)

            try:
                # 读取Markdown文件内容
                with open(src_path, 'r', encoding='utf-8') as md_file:
                    md_content = md_file.read()

                # 转换为HTML
                html_content = markdown.markdown(md_content, extensions=['fenced_code'])
                html_content = framework_content.replace('{content}', html_content)
                # 写入HTML文件
                with open(html_dest_path, 'w', encoding='utf-8') as html_file:
                    html_file.write(html_content)

                print(f"已转换: {src_path} -> {html_dest_path}")

            except Exception as e:
                print(f"转换失败 {src_path}: {str(e)}")
        elif os.path.isfile(src_path):
            shutil.copy(src_path, os.path.join(dest_dir, item))
        # 对于非Markdown文件，可以选择复制或忽略
        # 这里选择忽略，如果需要复制可以取消下面的注释
        # else:
        #     if os.path.isfile(src_path):
        #         shutil.copy2(src_path, dest_path)
        #         print(f"已复制: {src_path} -> {dest_path}")


if __name__ == "__main__":
    # 源目录和目标目录
    source_directory = "doc/blog"
    destination_directory = "view/blog"
    framework = "blog"

    print(f"开始转换Markdown文件，从 '{source_directory}' 到 '{destination_directory}'")
    convert_md_to_html(source_directory, destination_directory, framework)

    # 源目录和目标目录
    source_directory = "doc/sprival"
    destination_directory = "view/sprival"
    framework = "sprival"

    print(f"开始转换Markdown文件，从 '{source_directory}' 到 '{destination_directory}'")
    convert_md_to_html(source_directory, destination_directory, framework)

    print("转换完成!")
