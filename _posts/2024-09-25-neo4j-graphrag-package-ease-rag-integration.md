---
categories: articles
date: 2024-09-25
layout: post
style: huoshui
tags:
- AI
- 知识图谱
title: 轻松上手：Neo4j GraphRAG包简化RAG应用集成
---

介绍
------------

如果你已经探索过使用 Neo4j 来实现 GraphRAG，你可能已经了解它在提升生成模型输出质量方面的潜力。传统上，这需要深入掌握 Neo4j 和 Cypher（Neo4j 的查询语言）。在本文中，您可以了解到一种更简单的方式，简化 Neo4j 与检索增强生成（RAG）应用的集成，使开发者更容易使用，那就是：适用于 Python 的官方 Neo4j GraphRAG 包（neo4j-graphrag）！

**neo4j-graphrag：https://pypi.org/project/neo4j-graphrag/**

该 Python 包为您提供了管理 RAG 过程中的检索与生成任务的高效工具。本文将展示如何使用该包执行检索任务。接下来的文章将介绍其生成功能，帮助您构建完整的端到端 RAG 流程。

什么是 GraphRAG？
-----------------

neo4j-graphrag 包简化了图检索增强生成（GraphRAG）。在 Neo4j，我们相信将图数据库与向量搜索结合起来代表了 RAG 的下一步发展方向。

安装设置
-----

首先，连接到一个预配置的 Neo4j 演示数据库，该数据库模拟了一个电影推荐知识图谱。您可以使用用户名和密码 "recommendations" 访问 [https://demo.neo4jlabs.com:7473/browser/](https://demo.neo4jlabs.com:7473/browser/)。这一设置提供了一个现实场景，向量嵌入数据已作为 Neo4j 数据库的一部分。

使用 Cypher 命令可视化数据：
```cypher
MATCH (n) RETURN n LIMIT 25;
```

观察每个节点右侧详情中的 **plotEmbedding** 属性。我们将在演示中使用这些嵌入执行向量搜索。您可以通过以下 Cypher 命令检查是否存在 **moviePlotsEmbedding** 向量索引：
```cypher
SHOW INDEXES YIELD * WHERE type='VECTOR';
```

在您的 Python 环境中，安装 neo4j-graphrag 包及其他依赖包：
```bash
pip install neo4j-graphrag neo4j openai
```

接着，使用 Neo4j Python 驱动程序连接到数据库：
```python
from neo4j import GraphDatabase
# 演示数据库凭证
URI = "neo4j+s://demo.neo4jlabs.com"
AUTH = ("recommendations", "recommendations")
# 连接到 Neo4j 数据库
driver = GraphDatabase.driver(URI, auth=AUTH)
```

确保您已设置 OpenAI API 密钥：
```python
import os
os.environ["OPENAI_API_KEY"] = "sk-..."
```

检索操作
---------

我们的包提供了适用于不同检索策略的多种检索器类（参见文档：https://neo4j.com/docs/neo4j-graphrag-python/current/）。在这里，我们使用 `VectorRetriever` 类：
```python
from neo4j-graphrag.retrievers import VectorRetriever
from neo4j-graphrag.embeddings.openai import OpenAIEmbeddings
embedder = OpenAIEmbeddings(model="text-embedding-ada-002")
retriever = VectorRetriever(
    driver,
    index_name="moviePlotsEmbedding",
    embedder=embedder,
    return_properties=["title", "plot"],
)
```

我们使用 **text-embedding-ada-002** 模型，因为演示数据库中的电影情节嵌入是使用该模型生成的，从而使检索结果更加相关。您可以自定义返回的结果属性，这里我们指定了返回节点属性 `title` 和 `plot`。

使用检索器搜索与查询最相关的电影情节，执行近似最近邻搜索以识别最佳匹配的前三个电影情节：
```python
query_text = "A movie about the famous sinking of the Titanic"
retriever_result = retriever.search(query_text=query_text, top_k=3)
print(retriever_result)
```

结果可以进一步解析为：
```python
import re

for k, item in enumerate(retriever_result.items):
    plot = re.search(r"'plot':\s*'([^']*)'", item.content).group(1)
    title = re.search(r"'title':\s*'([^']*)'", item.content).group(1)
    score = item.metadata["score"]
    print(f"Result {k}: {title} - {score} - {plot}")
```

GraphRAG
--------

让我们看看检索器如何集成到简单的 GraphRAG 流程中。要使用 neo4j-graphrag 包执行 GraphRAG 查询，需要以下几个组件：
1.  一个 Neo4j 驱动——用于查询 Neo4j 数据库。
2.  一个检索器——neo4j-graphrag 包提供了一些实现，并允许您编写自己的检索器。
3.  一个 LLM——我们需要调用一个 LLM 来生成答案。neo4j-graphrag 包目前仅提供 OpenAI 的 LLM 实现，但其接口与 LangChain 的聊天模型兼容，并允许您编写自己的接口。

实际操作只需几行代码：
```python
from neo4j-graphrag.llm import OpenAILLM
from neo4j-graphrag.generation import GraphRAG

# LLM
llm = OpenAILLM(model_name="gpt-4", model_params={"temperature": 0})

# 初始化 RAG 流程
rag = GraphRAG(retriever=retriever, llm=llm)

# 查询图谱
query_text = "What movies are sad romances?"
response = rag.search(query_text=query_text, retriever_config={"top_k": 5})
print(response.answer)
```

总结
-------

我们展示了如何使用 neo4j-graphrag 包中的 `VectorRetriever` 类执行简单的检索查询。未来的文章将探讨其他检索策略以及如何在 GraphRAG 流程中使用不同的 LLM。敬请期待！

欢迎您将 `neo4j-graphrag` 包集成到您的项目中，并在公众号文章下方分享您的见解。

该包代码是开源的，您可以在 GitHub(**https://github.com/neo4j/neo4j-graphrag-python**) 上找到它，欢迎在上面提交问题。