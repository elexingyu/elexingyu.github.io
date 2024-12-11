---
categories: articles
date: '2024-09-30'
layout: post
style: huoshui
tags:
- AI
- 知识图谱
title: GraphRAG全索引结合，提升电影推荐检索效能
---

引言
------------
在我们关于 **Neo4j GraphRAG Python** 包系列的第三篇文章中，我们将探讨如何使用全文索引来增强 GraphRAG 应用。我们将展示如何将全文索引与向量索引结合使用，以通过检索仅靠向量检索可能遗漏的信息来提高这些应用程序的检索性能。

此外，我们将逐步讲解如何构建一个利用 Neo4j GraphRAG Python 库中的全文索引和向量索引的 GraphRAG 应用。

设置
-----
首先，确保你已经安装了 Neo4j GraphRAG 包、Neo4j Python 驱动程序和 OpenAI Python 包：
```bash
pip install neo4j neo4j-graphrag openai
```
我们将使用与前几篇文章中相同的预配置 Neo4j 演示数据库（参见《》和《》）。该数据库模拟了一个电影推荐知识图谱。有关数据库的更多信息，请阅读 《》 的设置部分。

你可以通过浏览器访问数据库 **https://demo.neo4jlabs.com:7473/browser/** ，用户名和密码均为“recommendations”。使用以下代码片段在应用程序中连接数据库：
```python
from neo4j import GraphDatabase

# 演示数据库凭据
URI = "neo4j+s://demo.neo4jlabs.com"
AUTH = ("recommendations", "recommendations")
# 连接到 Neo4j 数据库
driver = GraphDatabase.driver(URI, auth=AUTH)
```
此外，请确保导出你的 OpenAI 密钥：
```python
import os

os.environ["OPENAI_API_KEY"] = "sk-…"
```

向量搜索的局限性
-----------------
向量搜索通常是 RAG 应用的重要组成部分。它使应用能够在数据库中查找与用户查询语义上相似的信息，并将这些信息作为大语言模型生成响应的相关上下文。在本系列的前几篇博客中，我们在 GraphRAG 应用中使用了向量搜索来返回与用户查询含义相近的电影情节，从而回答他们关于电影的问题。例如，当用户问“那个关于恐龙主题公园的电影叫什么？”时，向量搜索将检索出电影《侏罗纪公园》。这是因为该电影的情节“在一次预览游览期间，主题公园遭遇了重大断电，导致克隆恐龙展品失控”在意义上与用户的查询相似。

然而，语义相似性并不总是检索最相关信息的最佳度量标准。例如，在搜索缺乏广泛语义含义或在更广泛的上下文中具有不同含义的领域特定术语时，向量搜索可能无法检索到相关信息，或可能返回不相关的信息。这是因为这些术语在用于向量搜索的嵌入模型的训练数据中可能没有得到很好的表示。此外，当用户查询包含需要精确匹配的特定字符串（如姓名或日期）时，语义相似性也不是一个可靠的度量。例如，使用 VectorRetriever 来查询一部在1375年帝国中国背景下的电影时：
```python
from neo4j import GraphDatabase
from neo4j-graphrag.embeddings.openai import OpenAIEmbeddings
from neo4j-graphrag.retrievers import VectorRetriever

driver = GraphDatabase.driver(URI, auth=AUTH)
embedder = OpenAIEmbeddings(model="text-embedding-ada-002")
retriever = VectorRetriever(
    driver,
    index_name="moviePlotsEmbedding",
    embedder=embedder,
    return_properties=["title", "plot"],
)

query_text = "What is the name of the movie set in 1375 in Imperial China?"
retriever_result = retriever.search(query_text=query_text, top_k=3)
print(retriever_result)
```
为了准确匹配此查询，VectorRetriever 的匹配算法需要在电影情节描述中找到1375年的确切日期引用，而它无法做到。因此，VectorRetriever 无法为此查询返回正确的电影（《武士》）。相反，它检索出与中国相关的电影，但没有一部具体设定在1375年。

全文索引
--------
幸运的是，有一种解决方案：全文索引。与根据语义相似性匹配字符串的向量索引不同，全文索引基于词汇相似性匹配文本片段，即比较文本的确切措辞或结构。例如，考虑句子“The bat flew”和“The bat broke”。这些句子在词汇上相似，因为它们仅相差一个词，但它们在语义上是不同的：第一个描述动物飞翔，而第二个描述物体破裂。全文索引使我们能够精确匹配字符串，如日期和名称。

混合检索器
------------
我们可以通过使用 Neo4j GraphRAG Python 库中的 HybridRetriever 类为我们的 GraphRAG 应用使用全文索引。该检索器在一种称为混合搜索的过程中结合了向量索引和全文索引。它使用用户查询同时搜索这两种索引，检索节点及其相应的得分。在对每组结果的得分进行标准化后，它将它们合并，并按得分对组合结果进行排序，返回最匹配的结果。
```python
from neo4j import GraphDatabase
from neo4j-graphrag.embeddings.openai import OpenAIEmbeddings
from neo4j-graphrag.retrievers import HybridRetriever

driver = GraphDatabase.driver(URI, auth=AUTH)
embedder = OpenAIEmbeddings(model="text-embedding-ada-002")
retriever = HybridRetriever(
    driver=driver,
    vector_index_name="moviePlotsEmbedding",
    fulltext_index_name="movieFulltext",
    embedder=embedder,
    return_properties=["title", "plot"],
)
query_text = "What is the name of the movie set in 1375 in Imperial China?"

retriever_result = retriever.search(query_text=query_text, top_k=3)
print(retriever_result)
```
此处，我们再次使用电影情节的向量索引（moviePlotsEmbedding），以及每部电影的标题和情节的全文索引（movieFulltext）。使用此检索器返回了正确的电影：
```python
items = [
    RetrieverResultItem(
        content="{'title': 'Musa the Warrior (Musa)', 'plot': '1375年，九位高丽武士，作为帝国中国流放的使节，保护中国明朝公主免受蒙古军队的袭击。'}",
        metadata={"score": 1.0},
    ),
]
```

总结
-------
我们展示了如何使用 neo4j-graphrag 包中的 HybridRetriever 类来构建一个 GraphRAG 应用。我们展示了该类如何结合向量和全文搜索来检索用户查询的正确上下文，而这些信息可能无法通过向量搜索单独获取。


该包代码是开源的，你可以在 GitHub(https://github.com/neo4j/neo4j-graphrag-python) 上找到。欢迎在那里提交问题。