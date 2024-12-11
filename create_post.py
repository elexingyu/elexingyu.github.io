import os
import re
import frontmatter
from datetime import datetime
from zhipuai import ZhipuAI
from slugify import slugify

client = ZhipuAI(api_key="30e7f246c91c2bc062887ec8aab16ff3.YyZwIQuO1eIwV8gw")

def clean_title(title):
    """清理标题中的不需要的符号"""
    # 移除《》
    title = re.sub(r'[《》]', '', title)
    # 移除可能的其他多余符号(根据需要添加)
    title = re.sub(r'[「」『』【】]', '', title)
    return title.strip()

def generate_title(content):
    prompt = f"""
    请根据以下文章内容,生成一个吸引人的中文标题。要求:
    1. 标题要简洁有力,20字以内
    2. 要包含文章的核心内容和价值
    3. 如果是教程类文章,建议用"如何..."或"X个技巧..."的形式
    4. 如果是新闻类文章,要突出新闻性和时效性
    5. 不要加任何书名号
    
    文章内容:
    {content[:2000]}
    """
    
    try:
        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[{"role": "user", "content": prompt}]
        )
        title = response.choices[0].message.content.strip()
        # 清理标题
        title = clean_title(title)
        return title
    except Exception as e:
        print(f"生成标题失败: {e}")
        return "未命名文章"

def generate_seo_filename(title, content):
    prompt = f"""
    请你根据以下文章内容,取英文标题,全小写,最多五个单词,方便被seo捕捉到。格式为每个单词使用"-"分隔:

    标题: {title}
    内容: {content}
    """
    
    try:
        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[{"role": "user", "content": prompt}]
        )
        filename = response.choices[0].message.content.strip()
        return filename
    except Exception as e:
        print(f"生成SEO文件名失败: {e}")
        return slugify(title)

def analyze_content_for_category(title, content):
    prompt = f"""
    请分析以下文章的标题和内容,判断它属于哪个栏目。
    只返回一个栏目名称: news 或 articles
    
    判断标准:
    1. news: 新闻报道、行业动态、产品发布等时效性较强的内容
    2. articles: 教程、经验分享、技术原理等经验性知识内容
    
    标题: {title}
    内容: {content[:2000]}
    """
    
    try:
        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[{"role": "user", "content": prompt}]
        )
        category = response.choices[0].message.content.strip().lower()
        return category if category in ['news', 'articles'] else 'articles'
    except Exception as e:
        print(f"分析文章类别失败: {e}")
        return 'articles'

def analyze_content_for_tags(content):
    keyword_tags = {
        'AI': ['人工智能', '机器学习', '深度学习', 'AI', '神经网络', '自然语言处理', 'NLP'],
        '知识图谱': ['知识图谱', '图数据库', '语义网络', '本体', '实体关系', 'RDF', 'SPARQL', 'neo4j'],
        '教程': ['教程', '指南', '步骤', '学习', '入门', '实践', '操作方法']
    }

    word_count = {}
    for tag, keywords in keyword_tags.items():
        count = 0
        for keyword in keywords:
            count += len(re.findall(keyword, content, re.IGNORECASE))
        word_count[tag] = count

    threshold = 2
    return [tag for tag, count in word_count.items() if count >= threshold]

def create_post(input_file, publish_date=None):
    # 如果没有提供发布日期，使用今天的日期
    if publish_date is None:
        publish_date = datetime.now().strftime('%Y-%m-%d')
    
    # 读取输入文件
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 如果输入文件已经有front matter，则提取它
    if content.startswith('---'):
        post = frontmatter.loads(content)
        body = post.content
    else:
        # 移除可能的标题行
        lines = content.split('\n')
        if lines[0].startswith('#'):
            body = '\n'.join(lines[1:]).strip()
        else:
            body = content.strip()
    
    # 使用AI生成标题
    title = generate_title(body)
    print(f"生成的标题: {title}")
    
    # 生成SEO友好的文件名
    seo_filename = generate_seo_filename(title, body)
    
    # 分析文章类别和标签
    category = 'articles'
    tags = analyze_content_for_tags(body)
    
    # 构建新的front matter
    metadata = {
        'layout': 'post',
        'title': title,
        'date': publish_date,
        'categories': category,
        'tags': tags,
        'style': 'huoshui'
    }
    
    # 创建新的post对象
    new_post = frontmatter.Post(body, **metadata)
    
    # 构建输出文件路径
    output_filename = f"{publish_date}-{seo_filename}.md"
    output_path = os.path.join('_posts', output_filename)
    
    # 确保_posts目录存在
    os.makedirs('_posts', exist_ok=True)
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(frontmatter.dumps(new_post))
    
    print(f"文章已创建: {output_path}")
    print(f"标题: {title}")
    print(f"类别: {category}")
    print(f"标签: {tags}")

if __name__ == "__main__":
    # 使用示例
    input_file = "input.md"  # 你的输入文件
    publish_date = "2024-10-28"  # 指定发布日期
    create_post(input_file, publish_date) 