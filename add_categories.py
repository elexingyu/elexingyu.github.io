import os
import frontmatter
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="30e7f246c91c2bc062887ec8aab16ff3.YyZwIQuO1eIwV8gw")

def analyze_content_for_category(title, content):
    prompt = f"""
    请分析以下文章的标题和内容,判断它属于哪个栏目。
    只返回一个栏目名称: news 或 articles
    
    判断标准:
    1. news: 新闻报道、行业动态、产品发布等时效性较强的内容
    2. articles: 教程、经验分享、技术原理等经验性知识内容
    
    标题: {title}
    内容: {content[:2000]}  # 只取前2000字符避免超token
    """
    
    try:
        response = client.chat.completions.create(
            model="glm-4-flash",
            messages=[{"role": "user", "content": prompt}]
        )
        category = response.choices[0].message.content.strip().lower()
        return category if category in ['news', 'articles'] else 'articles'
    except Exception as e:
        print(f"分析文章类别时出错: {e}")
        return 'articles'  # 默认归类为articles

def add_categories_to_posts(posts_dir):
    for filename in os.listdir(posts_dir):
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(posts_dir, filename)
        
        try:
            # 读取文章
            post = frontmatter.load(filepath)
            
            # 如果已经有categories,跳过
            if 'categories' in post.metadata:
                print(f"跳过 {filename}: 已有categories")
                continue
                
            # 分析文章类别
            category = analyze_content_for_category(
                post.metadata.get('title', ''),
                post.content
            )
            
            # 添加category到metadata
            post.metadata['categories'] = category
            
            # 写回文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(frontmatter.dumps(post))
            
            print(f"已处理 {filename}: 分类为 {category}")
            
        except Exception as e:
            print(f"处理文件 {filename} 时出错: {e}")
            continue

if __name__ == "__main__":
    posts_dir = '_posts'
    add_categories_to_posts(posts_dir) 