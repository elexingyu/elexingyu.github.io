---
categories: articles
date: '2024-09-26'
layout: post
style: huoshui
tags:
- AI
- 知识图谱
- 教程
title: GraphRAG进阶：Cypher查询提升电影推荐
---

![](https://miro.medium.com/v2/resize:fit:1400/1*RDkVlyxp_kJHNWDB1323ug.png)

在我们上一篇关于 Neo4j GraphRAG Python 包的博文中，我们介绍了如何使用该包构建一个基本的 GraphRAG 应用程序。在本篇及后续的文章中，我们将深入探讨该包的功能，并展示如何通过使用其他包含的检索器来进一步自定义和改进您的应用程序。在这里，我们将演示如何使用 Cypher 查询扩展上一篇文章中使用的向量搜索方法，通过添加图遍历作为额外的步骤。

## 设置

我们将使用与上一篇公号文章中相同的预配置 Neo4j 演示数据库。该数据库模拟了一个电影推荐知识图谱。（有关数据库的更多详细信息，请参阅上一篇公号文章的“设置”部分。）

您可以通过浏览器访问数据库，网址为 https://demo.neo4jlabs.com:7473/browser/，用户名和密码均为“recommendations”。使用以下代码片段连接到您的应用程序中的数据库：

```
from neo4j import GraphDatabase

URI = "neo4j+s://demo.neo4jlabs.com"
AUTH = ("recommendations", "recommendations")

driver = GraphDatabase.driver(URI, auth=AUTH)
```

另外，请确保导出您的 OpenAI 密钥：

```
import os

os.environ["OPENAI_API_KEY"] = "sk-…"
```

## 图中的其他节点

在 Neo4j 网页界面中运行以下命令，以可视化电影 “Tom and Huck” 及其与其他节点的直接关系：

```
MATCH (m:Movie {title: 'Tom and Huck'})-[r]-(n) RETURN *;
```

![电影 “Tom and Huck” 节点及其直接连接的节点](https://miro.medium.com/v2/resize:fit:1400/0*EoKfakeoTgiNfnzn)


请注意，我们现在可以看到电影的类型、出演的演员以及其他未包含在 Movie 节点中的有用信息。

在上一篇文章中，我们使用了电影情节嵌入和向量检索器来检索与用户查询最相似的电影节点。这些电影节点作为大语言模型（LLM）生成答案的上下文。然而，在这种设置中，只有电影节点本身包含的信息可以作为上下文，连接到未使用的电影节点的其他节点中的附加信息没有被利用。因此，如果用户询问有关电影类型或主演演员的问题，LLM 将无法获得适当的上下文来回答这些问题。

## 检索

幸运的是，我们可以使用 `VectorCypherRetriever` 类来检索这些附加信息。该检索器首先使用向量搜索从知识图谱中检索初始一系列节点，然后使用 Cypher 查询从这些初始节点遍历图谱，收集与它们连接的节点中的附加信息。

要使用此检索器，我们首先需要编写 Cypher 查询，以指定与通过向量搜索检索到的节点一起获取的确切附加信息。例如，要与电影节点一起检索演员信息，我们可以使用以下查询：

```
retrieval_query = """
MATCH
(actor:Actor)-[:ACTED_IN]->(node)
RETURN
node.title AS movie_title,
node.plot AS movie_plot, 
collect(actor.name) AS actors;
"""
```

此查询中的 `node` 变量是对通过初始向量搜索步骤检索到的节点的引用，这里是电影节点。此查询查找出演每部电影的所有演员，并返回他们的名字以及电影的标题和情节。

然后，我们将此查询传递给 `VectorCypherRetriever`，并传递与上一篇文章中传递给 `VectorRetriever` 的相同信息，例如向量索引的名称和嵌入：

```
from neo4j import GraphDatabase
from neo4j_graphrag.embeddings.openai import OpenAIEmbeddings
from neo4j_graphrag.retrievers import VectorCypherRetriever

driver = GraphDatabase.driver(URI, auth=AUTH)
embedder = OpenAIEmbeddings(model="text-embedding-ada-002")
vc_retriever = VectorCypherRetriever(
    driver,
    index_name="moviePlotsEmbedding",
    embedder=embedder,
    retrieval_query=retrieval_query,
)
```

同样，我们使用 `text-embedding-ada-002` 模型作为演示数据库中的电影情节嵌入，该嵌入最初是使用该模型生成的。

现在我们可以使用我们的检索器来搜索数据库中的电影及其主演演员的信息：

```
query_text = "Who were the actors in the movie about the magic jungle board game?"
retriever_result = retriever.search(query_text=query_text, top_k=3)
```

```
items=[
  RetrieverResultItem(content="<Record
    movie_title='Jumanji'
    movie_plot='When two kids find and play a magical board game, they release a man trapped for decades in it and a host of dangers that can only be stopped by finishing the game.'
    actors=['Robin Williams', 'Bradley Pierce', 'Kirsten Dunst', 'Jonathan Hyde']",
    metadata=None),
  RetrieverResultItem(content="<Record
    movie_title='Welcome to the Jungle'
    movie_plot='A company retreat on a tropical island goes terribly awry.'
    actors=['Jean-Claude Van Damme', 'Adam Brody', 'Rob Huebel', 'Kristen Schaal']",
    metadata=None),
  RetrieverResultItem(content='<Record
    movie_title=\'Last Mimzy, The\'
    movie_plot=\'Two siblings begin to develop special talents after they find a mysterious box of toys. Soon the kids, their parents, and even their teacher are drawn into a strange new world and find a task ahead of them that is far more important than any of them could imagine!\'
    actors=[\'Joely Richardson\', \'Rhiannon Leigh Wryn\', \'Timothy Hutton\', "Chris O\'Neil"]',
    metadata=None)
]
metadata={'__retriever': 'VectorCypherRetriever'}
```

请注意，我们已经检索到了每部电影的演员以及其标题和情节。使用 `VectorRetriever`，我们只能检索到标题和情节，而演员信息存储在连接到每个电影节点的演员节点中，因此无法检索到。

## GraphRAG

要构建一个完整的 GraphRAG 管道，我们只需将上一篇文章中使用的 `VectorRetriever` 替换为我们的 `VectorCypherRetriever`：

```
from neo4j_graphrag.llm import OpenAILLM
from neo4j_graphrag.generation import GraphRAG

llm = OpenAILLM(model_name="gpt-4o", model_params={"temperature": 0})

rag = GraphRAG(retriever=vc_retriever, llm=llm)

query_text = "Who were the actors in the movie about the magic jungle board game?"
response = rag.search(query=query_text, retriever_config={"top_k": 3})
print(response.answer)
```

这将返回以下响应：

```
电影 “Jumanji”，关于一个神奇的棋盘游戏，主演演员包括 Robin Williams、Bradley Pierce、Kirsten Dunst 和 Jonathan Hyde。
```

## 总结

在本篇文章中，我们演示了如何使用 Neo4j GraphRAG Python 包中的 `VectorCypherRetriever` 类构建一个简单的 GraphRAG 应用程序。我们展示了该强大的类如何在初始向量检索步骤之外，结合图遍历步骤，从图中获取无法通过向量检索获取的信息。随后我们展示了如何使 LLM 回答关于我们电影数据库的某些问题，而这些问题使用 `VectorRetriever` 类是无法回答的。

我们邀请您在项目中使用 neo4j-graphrag-python 包，并通过评论或在我们的 GraphRAG Discord 频道分享您的见解。

该包的代码是开源的，您可以在 GitHub 上找到它。欢迎在那里提交问题。
