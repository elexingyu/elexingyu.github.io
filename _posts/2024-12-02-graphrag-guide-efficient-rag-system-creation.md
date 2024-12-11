---
categories: articles
date: 2024-12-02
layout: post
style: huoshui
tags:
- AI
- 知识图谱
title: GraphRAG解析：高效RAG系统构建全攻略
---

我经常在Reddit上看到关于GraphRAG的帖子，但直到大约一个月前，我才决定尝试一下。在花了一些时间进行实验后，我可以说它的表现令人印象深刻，但如果你使用的是OpenAI API，成本也相当高。在文档中运行他们提供的示例书籍测试花费了我大约7美元，所以虽然它的性能和组织能力非常出色，但它并不算经济实惠。

如果你是RAG系统的新手，我建议先阅读一些入门文章：

1、Anthropic 的新 RAG 方法(https://pub.towardsai.net/anthropics-new-rag-approach-e0c24a68893b)

2、RAG 从头开始(https://pub.towardsai.net/rag-from-scratch-66c5eff02482)

无论如何，这里是传统RAG系统的工作原理概述：

![](https://miro.medium.com/v2/resize:fit:1400/1*aBKnYfX6VPWxtGvw5vVXIw.png)



对于已经熟悉RAG的人来说，你可能遇到过和我一样的头疼问题：

-   文本块之间的上下文容易丢失
-   随着文档集合的增长，性能急剧下降
-   集成外部知识就像蒙着眼睛解魔方一样困难（比喻意指操作复杂且缺乏清晰方向）

## GraphRAG的工作原理

![](https://miro.medium.com/v2/resize:fit:1400/1*1r3_zcQg9ypH68E9uHkTPw.png)



GraphRAG是传统RAG的增强版本，主要分为两个阶段：

## 索引阶段

-   从源文档开始，将其**拆分**为更小的子文档（与传统RAG类似）
-   执行两个并行的提取过程：

1.  **实体提取**：识别出诸如人物、地点、公司等实体  
2.  **关系提取**：发现跨不同文本块的实体之间的联系  

-   创建一个**知识图谱**，其中节点代表实体，边代表它们之间的关系  
-   通过识别紧密相关的实体来建立**社区**  
-   在不同的社区层级生成**分层摘要**（共三级）  
-   使用归约-映射方法，通过逐步合并文本块生成整体摘要  

## 查询阶段

-   接收用户的**查询**  
-   根据所需的细节选择适当的**社区层级**  
-   在**社区层级**（而不是传统RAG的文本块层级）上执行**检索**  
-   检查社区摘要以**生成局部响应**  
-   将多个相关社区的**局部响应**组合成最终的综合答案  

GraphRAG的核心创新在于它将信息结构化为图形格式，并利用社区检测来生成更具上下文意识的响应。然而，**传统RAG系统仍然有其用武之地，特别是在考虑运行GraphRAG的计算成本时**。

## 设置GraphRAG

> ⚠️ 提醒：这个实验运行在GPT-4 API上，成本较高。我的一次测试成本约为7美元（基于GPT-4模型）。

**如果你更喜欢在本地LLM上使用ollama进行测试，请查看这个视频：**

接下来让我们一步步完成设置过程：

## 环境设置

首先，创建一个虚拟环境：

```
conda create -n GraphRAG
conda activate GraphRAG
```

安装GraphRAG包：

```
pip install graphrag
```

## 目录结构

GraphRAG需要特定的目录结构以实现最佳运行效果：  
\- 创建一个工作目录  
\- 在其中创建_ragtest/input_文件夹结构  
\- 将源文档放入input文件夹中  

在本文中，我们将使用提供的书籍作为示例。通过以下命令下载到input文件夹中：

```
curl https://www.gutenberg.org/cache/epub/24022/pg24022.txt > ./ragtest/input/book.txt
```

## 配置

使用以下命令初始化工作区：

```
python -m graphrag.index --init --root ./target
```

此操作会创建必要的配置文件，包括**settings.yml**，你需要在其中：  
\- 设置你的OpenAI API密钥  
\- 配置模型设置（默认使用GPT-4进行处理和OpenAI嵌入）  
\- 根据需要调整文本块大小（默认：300个token）和重叠部分（默认：100个token）  

## 构建知识图谱

运行索引过程：

```
python -m graphrag.index --init --root ./target
```

## 查询你的图谱

GraphRAG提供了两种主要的查询方式：

**全局查询**

```
python -m graphrag.query --root ./target --method global "what are the top themes in this story"
```

适用于关于主题和整体内容理解的广泛问题。

**局部查询**

```
python -m graphrag.query --root ./target --method local "what are the top themes in this story"
```

适用于关于文档内实体或关系的具体问题。

## 成本因素：值得吗？

让我们谈谈数字。在我用示例书籍进行测试时，GraphRAG调用了：

-   ~570次GPT-4 API请求  
-   大约25次嵌入请求  
-   处理了超过100万个token  

总成本：每本书大约7美元。

## 资源

https://www.microsoft.com/en-us/research/blog/graphrag-new-tool-for-complex-data-discovery-now-on-github/