import os
import re
import requests
from urllib.parse import urlparse
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
import frontmatter
import html2text
from slugify import slugify
from collections import Counter
from zhipuai import ZhipuAI
import mimetypes
import uuid

client = ZhipuAI(api_key="30e7f246c91c2bc062887ec8aab16ff3.YyZwIQuO1eIwV8gw") 

def html_to_markdown(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # 处理带有 class="code-snippet__fix" 的代码片段
    for code_snippet in soup.find_all(class_='code-snippet__fix'):
        code_text = code_snippet.get_text()
        # 将代码片段转换为 Markdown 格式
        code_markdown = f'\n```\n{code_text}\n```\n'
        code_snippet.replace_with(code_markdown)

    # 将处理后的 HTML 转换为 Markdown
    h = html2text.HTML2Text()
    h.ignore_links = False
    markdown_content = h.handle(str(soup))

    return markdown_content

def download_and_save_image(url, save_dir):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # 尝试从Content-Type获取文件扩展名
            content_type = response.headers.get('Content-Type')
            ext = mimetypes.guess_extension(content_type)
            
            if not ext:
                # 如果无法从Content-Type获取扩展名,尝试从URL获取
                ext = os.path.splitext(urlparse(url).path)[1]
            
            if not ext:
                # 如果仍然无法获取扩展名,使用默认扩展名
                ext = '.jpg'
            
            # 生成唯一的文件名
            filename = f"{uuid.uuid4().hex}{ext}"
            save_path = os.path.join(save_dir, filename)
            
            with open(save_path, 'wb') as f:
                f.write(response.content)
            
            return save_path
    except Exception as e:
        print(f"下载图片失败: {url}. 错误: {e}")
    return None

def clean_markdown(markdown_content, image_dir):
    # 创建图片保存目录
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)

    # 查找所有图片链接
    img_pattern = r'!\[.*?\]\((https?://[^\s\)]+)\)'
    def replace_image(match):
        img_url = match.group(1)
        if 'mmbiz.qpic.cn' in img_url:
            new_path = download_and_save_image(img_url, image_dir)
            if new_path:
                # 修改图片路径,使用相对路径
                return f'![](/assets/images/{os.path.basename(new_path)})'
        return match.group(0)  # 如果下载失败，保留原始链接

    markdown_content = re.sub(img_pattern, replace_image, markdown_content)

    markdown_content = re.sub(r'!\[图片\]\(https://mmbiz\.qpic\.cn/mmbiz_png/Oh47rXadcrfBHps94U5yNKia9FgvibicoeGLHzxTCNtuylSRqRiczzbA8AQVG0tonWMLOPIkYXcXP4v3ssK0rc1hrA/640\?wx_fmt=png&from=appmsg\)', '', markdown_content)
    
    # 删除"活水智能关注和星标下方账号用AI提升生产力"及以下内容
    patterns = [
        r"活水智能关注和星标下方账号用AI提升生产力",
        r"\*\*活水智能\*\*\*\*关注和星标下方账号\*\*\*\*用AI提升生产力\*\*"
    ]
    for pattern in patterns:
        split_content = re.split(pattern, markdown_content, flags=re.IGNORECASE)
        if len(split_content) > 1:
            markdown_content = split_content[0].strip()
            break

    return markdown_content

def analyze_content_for_tags(content):
    # 定义关键词和对应的标签
    keyword_tags = {
        'AI': ['人工智能', '机器学习', '深度学习', 'AI', '神经网络', '自然语言处理', 'NLP'],
        '知识图谱': ['知识图谱', '图数据库', '语义网络', '本体', '实体关系', 'RDF', 'SPARQL'],
        '教程': ['教程', '指南', '步骤', '学习', '入门', '实践', '操作方法']
    }

    # 计算关键词出的次数
    word_count = Counter()
    for tag, keywords in keyword_tags.items():
        for keyword in keywords:
            count = len(re.findall(keyword, content, re.IGNORECASE))
            word_count[tag] += count

    # 决定添加哪些标签
    threshold = 2  # 可以调整这个阈值
    tags = [tag for tag, count in word_count.items() if count >= threshold]

    return tags

def generate_filename(title, content):
    prompt = f"""
    请你根据以下文章内容,取英文标题,全小写,最多五个单词,方便被seo捕捉到。格式为每个单词使用"-"分隔:

    标题: {title}
    内容: {content[:4000]}  # 只取前4000个字符,避免超出token限制
    """
    
    response = client.chat.completions.create(
        model="glm-4-flash",
        messages=[{"role": "user", "content": prompt}]
    )
    
    filename = response.choices[0].message.content.strip()
    return filename

def convert_html_to_md(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # 修改图片保存目录
    image_dir = os.path.join('assets', 'images')
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
    
    for filename in os.listdir(input_folder):
        if filename.endswith('.html'):
            input_path = os.path.join(input_folder, filename)
            
            # 提取日期和标题
            match = re.match(r'(\d{4}-\d{2}-\d{2})_(.+)\.html', filename)
            if match:
                date = match.group(1)
                title = match.group(2).replace('_', ' ')
                
                # 读取内容并转换为 Markdown
                with open(input_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                post = frontmatter.loads(content)
                markdown_content = html_to_markdown(post.content)
                markdown_content = clean_markdown(markdown_content, image_dir)
                
                # 使用 generate_filename 生成文件名
                try:
                    generated_filename = generate_filename(title, markdown_content)
                    output_filename = f"{date}-{generated_filename}.md"
                except Exception as e:
                    print(f"生成文件名时出错: {e}. 使用默认文件名。")
                    output_filename = f"{date}-{slugify(title, max_length=50)}.md"
                
                output_path = os.path.join(output_folder, output_filename)
                
                # 分析内容并获取标签
                tags = analyze_content_for_tags(markdown_content)
                
                # 写入转换后的内容
                with open(output_path, 'w', encoding='utf-8') as file:
                    # 写入 frontmatter
                    file.write('---\n')
                    file.write('layout: post\n')  # 添加 layout: post
                    file.write(f'title: "{title}"\n')
                    file.write(f'date: {date}\n')
                    file.write(f'tags: {tags}\n')
                    file.write(f'style: huoshui\n')
                    file.write('---\n\n')
                    # 写入 markdown 内容
                    file.write(markdown_content)
                
                print(f'已转换: {filename} -> {output_filename}')
            else:
                print(f"警告: 文件名 {filename} 不符合预期格式,跳过处理。")
                continue

# 使用示例
input_folder = 'html'
output_folder = '_posts'
convert_html_to_md(input_folder, output_folder)