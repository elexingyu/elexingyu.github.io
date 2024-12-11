---
categories: articles
date: '2024-10-04'
layout: post
style: huoshui
tags:
- AI
- 知识图谱
title: GraphRAG Agent：结合Neo4j与Milvus打造智能问答系统
---

这篇文章详细介绍了如何使用 Neo4j 图数据库和 Milvus(https://zilliz.com/what-is-milvus) 向量数据库构建一个 GraphRAG Agent。该智能体结合了 图数据库和向量搜索的强大功能，能够为用户查询提供准确和相关的答案。在这个示例中，我们将使用 LangGraph、Llama 3.1 8B 结合 Ollama 和 GPT-4o。

传统的检索增强生成（RAG）系统仅依赖向量数据库来检索相关文档。我们的方法更进一步，通过结合 Neo4j (https://neo4j.com/) 来捕捉实体和概念之间的关系，提供更细致的信息理解。通过结合这两种技术，我们希望创建一个更强大和信息丰富的 RAG 系统。

![向量 + GraphRAG 架构](https://dist.neo4j.com/wp-content/uploads/20240927080732/vector-graphrag-architecture.png)

构建 RAG 智能体
----------------------

我们的智能体遵循三个关键概念：路由、后备机制和自我校正。这些原则通过一系列 LangGraph 组件实现：

* **路由** – 一个专门的路由机制决定是使用向量数据库、知识图谱，还是两者的组合，具体取决于查询。
* **后备** – 在初次检索不足的情况下，智能体会使用 Tavily 进行网络搜索。
* **自我校正** – 智能体评估自身的回答并尝试纠正幻觉或不准确之处。

我们还有其他组件，例如：

* **检索** – 我们使用 Milvus，这是一款开源且高性能的向量数据库，根据与用户查询的语义相似度存储和检索文档块。
* **图增强** – 使用 Neo4j 从检索的文档中构建知识图，丰富包含关系和实体的上下文。
* **LLMs 集成** – 使用本地 LLM Llama 3.1 8B 生成答案并评估检索信息的相关性和准确性，而 GPT-4o 用于生成 Neo4j 使用的查询语言 Cypher。

GraphRAG 架构
----------------------

我们 GraphRAG Agent 的架构可以被视为一个包含多个互联节点的工作流：

* **问题路由** – 智能体首先分析问题，以确定最佳的检索策略（向量搜索、图搜索或两者）。
* **检索** – 根据路由决定，从 Milvus 中检索相关文档，或从 Neo4j 图中提取信息。
* **生成** – LLM 使用检索到的上下文生成答案。
* **评估** – 智能体评估生成的答案的相关性、准确性和潜在的幻觉。
* **改进**（如有必要）– 如果答案不令人满意，智能体可以改进其搜索或尝试纠正错误。

智能体示例
--------------------

为了展示我们的 LLM 智能体的能力，让我们看看两个不同的组件：`图生成`和`复合智能体`。

虽然完整代码在博文底部可用，但这些代码片段将提供更好的理解这些智能体在 LangChain 框架中如何工作。

### 图生成

该组件旨在通过利用 Neo4j 的能力来改善问答过程。它通过利用嵌入在 Neo4j 图数据库中的知识回答问题。其工作原理如下：

1. `GraphCypherQAChain` – 允许 LLM 与 Neo4j 图数据库交互。它以两种方式使用 LLM：

* `cypher_llm` – 该 LLM 实例负责生成 Cypher 查询，以根据用户的问题从图中提取相关信息。
* **验证** – 确保 Cypher 查询有效，以确保它们在语法上是正确的。

3. **上下文检索** – 验证后的查询在 Neo4j 图上执行，以检索必要的上下文。
4. **答案生成** – 语言模型使用检索到的上下文生成用户问题的答案。

### 生成 Cypher 查询
```python
llm = ChatOllama(model=local_llm, temperature=0)

# 链
graph_rag_chain = GraphCypherQAChain.from_llm(
        cypher_llm=llm,
        qa_llm=llm,
        validate_cypher=True,
        graph=graph,
        verbose=True,
        return_intermediate_steps=True,
        return_direct=True,
    )

# 运行
question = "agent memory"
generation = graph_rag_chain.invoke({"query": question})
```

该组件使 RAG 系统能够利用 Neo4j，从而提供更全面和准确的答案。

### 复合智能体、图与向量 🪄

魔法发生在这里：我们的智能体能够结合来自 Milvus 和 Neo4j 的结果，从而更好地理解信息，提供更准确和细致的答案。其工作原理如下：

1. **提示** – 我们定义一个提示，指示 LLM 使用来自 Milvus 和 Neo4j 的上下文回答问题。
2. **检索** – 智能体从 Milvus（使用向量搜索）和 Neo4j（使用图生成）中检索相关信息。
3. **答案生成** – Llama 3.1 8B 处理提示并生成简洁答案，利用来自向量和图数据库的综合知识。

### 复合向量 + 图生成
```python
cypher_prompt = PromptTemplate(
    template="""你是 Neo4j Cypher 查询生成的专家。
    使用以下架构生成一个 Cypher 查询，以回答给定问题。
    通过使用不区分大小写的匹配和适当的部分字符串匹配，使查询灵活。
    专注于搜索论文标题，因为它们包含最相关的信息。
    
    架构：
    {schema}
    
    问题：{question}
    
    Cypher 查询：""",
    input_variables=["schema", "question"],
)

# QA 提示
qa_prompt = PromptTemplate(
    template="""你是一个问答任务的助手。
    使用以下 Cypher 查询结果回答问题。如果你不知道答案，就说你不知道。
    最多使用三句话，保持答案简洁。如果没有主题信息可用，关注论文标题。
    
    问题：{question} 
    Cypher 查询：{query}
    查询结果：{context} 
    
    答案：""",
    input_variables=["question", "query", "context"],
)

llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 链
graph_rag_chain = GraphCypherQAChain.from

_llm(
    cypher_llm=llm,
    qa_llm=llm,
    validate_cypher=True,
    graph=graph,
    verbose=True,
    return_intermediate_steps=True,
    return_direct=True,
    cypher_prompt=cypher_prompt,
    qa_prompt=qa_prompt,
)
```

让我们看看我们的搜索结果，结合图和向量数据库的优势，以增强我们对研究论文的发现。

我们首先使用 Neo4j 进行图搜索：

### 示例输入数据
```python
question = "什么论文讨论多智能体？"
generation = graph_rag_chain.invoke({"query": question})
print(generation)
```

```
> 进入新的 GraphCypherQAChain 链...
生成的 Cypher：
cypher
MATCH (p:Paper)
WHERE toLower(p.title) CONTAINS toLower("多智能体")
RETURN p.title AS PaperTitle, p.summary AS Summary, p.url AS URL

```

```
>  Finished chain. 

{'query': '什么论文讨论多智能体？', 'result': [{'PaperTitle': '协作多智能体、多推理路径（CoMM）提示框架', 'Summary': '在这项工作中，我们旨在推动 LLM 的推理能力的上限，提出一个协作多智能体、多推理路径（CoMM）提示框架。具体来说，我们提示 LLM 在问题解决团队中扮演不同角色，并鼓励不同角色的代理协同解决目标任务。我们发现为不同角色应用不同的推理路径是一种有效策略，可以在多智能体场景中实现少样本提示方法。实证结果证明了所提方法在两个大学级科学问题上的有效性。我们的进一步分析显示提示 LLM 扮演不同角色或专家是必要的。', 'URL': 'https://github.com/amazon-science/comm-prompt'}]}

```


图搜索在查找关系和元数据方面表现出色。它可以快速识别基于标题、作者或预定义类别的论文，提供数据的结构化视图。

接下来，我们转向我们的向量搜索以获得不同的视角：

### 示例输入数据
```python
question = "什么论文讨论多智能体？"

# 获取向量 + 图答案
docs = retriever.invoke(question)
vector_context = rag_chain.invoke({"context": docs, "question": question})
```

```
> 该论文讨论了“适应性对话团队构建为语言模型代理”并讨论多智能体。它提出了一种新的适应性团队构建范例，为构建 LLM 代理团队以有效解决复杂任务提供灵活的解决方案。该方法称为 Captain Agent，动态形成和管理每个任务解决过程中的团队，利用嵌套的群体对话和反思，以确保多样化的专业知识并防止刻板输出。
```

向量搜索在理解上下文和语义相似度方面表现优异。它能够发现与查询在概念上相关的论文，即使它们没有明确包含搜索词。

最后，我们结合这两种搜索方法：

这是我们 RAG Agent 的重要部分，使得能够同时使用向量和图数据库。

```python
composite_chain = prompt | llm | StrOutputParser()
answer = composite_chain.invoke({"question": question, "context": vector_context, "graph_context": graph_context})
print(answer)
```

```
> 论文“协作多智能体、多推理路径（CoMM）提示框架”讨论了多智能体。它提出了一种框架，提示 LLM 在问题解决团队中扮演不同角色，并鼓励不同角色的代理协同解决目标任务。该论文呈现了在两个大学级科学问题上的实证结果，证明了所提方法的有效性。
```

通过集成图搜索和向量搜索，我们利用了两种方法的优势。图搜索提供精确度并导航结构化关系，而向量搜索通过语义理解增加深度。

这种组合方法提供了几个优势：

1. **提高召回率**：找到更多相关的答案和上下文信息。
2. **增强准确性**：通过图数据库确保检索的答案在结构上是正确的，提供可靠的信息源。
3. **丰富理解**：结合向量搜索的语义能力，能够更好地理解问题的含义和上下文，从而提供更相关的答案。

结论
---------------------

GraphRAG Agent 结合了 Neo4j 和 Milvus 的优势，为问答系统提供新颖强大的解决方案。通过集成图数据库和向量数据库，我们能够为用户提供更精确、全面和信息丰富的答案。未来，我们将继续探索这两种技术的结合，提升智能体的能力。