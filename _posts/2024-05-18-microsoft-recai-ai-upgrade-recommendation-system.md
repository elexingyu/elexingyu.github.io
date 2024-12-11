---
categories: articles
date: 2024-05-18
layout: post
style: huoshui
tags:
- AI
- 教程
title: 微软RecAI：用AI升级你的推荐系统
---

> 推荐系统无处不在，它就像我们的私人助理，帮助我们从海量的信息中筛选出感兴趣的内容。然而传统的推荐系统往往缺乏互动性、透明度和可控性。

微软研究院开源的 RecAI
结合大语言模型（LLMs）和传统推荐模型，创建一个更智能、更具交互性的推荐系统，不但提供精准的推荐，还能与用户互动，解释推荐原因，并根据反馈不断学习和进化。

## 组成部分

RecAI 采用模块化设计，由几个关键组件构成:

1\. **推荐系统AI代理（InteRecAgent）：**
是一个AI代理框架，将LLMs作为核心智能，负责用户交互和上下文推理，同时将传统推荐模型作为工具，结合了大型语言模型的智能交互能力和传统推荐系统的数据训练优势，将传统模型如矩阵分解转换为会话型、互动型和可解释的推荐系统。

2\. **选择性的知识插件（Selective Knowledge Plugin）：**
通过提示（prompt）向大型语言模型注入选择性的知识，以增强模型的领域特定能力。这种方法可在不修改模型参数的情况下，通过精心设计的提示（prompt），将大量持续更新的领域特定数据模式注入到LLMs中。

3\. **嵌入式和生成式语言模型（RecLM-emb和RecLM-gen）** ：RecLM-
emb是针对项目检索优化的文本嵌入模型，支持文本模态，如搜索查询、项目描述和用户指令，为项目检索提供嵌入支持。针对不同领域的数据模式差异对生成式语言模型进行微调，以提高推荐任务的表现。这包括监督式微调（SFT）和强化学习（RL）技术，潜在应用包括排名器、会话推荐器和用户模拟器。

4\. **模型解释器（RecExplainer）** ：为了提高基于深度学习的推荐系统的可解释性，RecAI项目提出了一种新的模型解释方法
RecExplainer，使用LLMs作为替代模型，学习模仿并理解目标推荐模型，从而提供更可靠和透明的推荐系统。

5\. **RecLM评估器（RecLM Evaluator）** :全方位评估语言模型在推荐系统中的表现，涵盖检索、排序、解释、对话等多个维度。

## 实现方式

RecAI 的实现方式可概括为"语言模型+推荐系统"，即利用大型语言模型强大的自然语言理解和生成能力，赋予推荐系统以类似人类的交互和认知能力。

同时，RecAI 继承了传统推荐系统在用户行为分析和个性化方面的优势，使得 RecAI 兼具智能和专业性。

## 小 结

RecAI 通过整合大型语言模型来增强推荐系统的交互性、解释性和控制性，让推荐系统从只会"喂养"用户，变成能够"理解"用户的智能助手。

未来，我们与推荐系统的互动，将更加自然、高效和愉悦，就像与一位了解我们的朋友交谈一样。

> 项目仓库：https://github.com/microsoft/RecAI
>
> 论文链接：https://arxiv.org/html/2403.06465v1


## 推荐阅读

  • [FineWeb：Hugging Face开源的15T超大数据集](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247485219&idx=1&sn=380bae26f5275370ddbc5b30f0778523&chksm=c35465b0f423eca609b24448b0a81fcd35bd098c13b7946416eb58cafef1bb422696b7d0ea6f&scene=21#wechat_redirect)[](https://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247485169&idx=1&sn=cd8f4d1be87702fdec14dfea200bd824&scene=21#wechat_redirect "开源大模型太多怎么选？一文读懂，5个最好的开源大模型！")

  • [最全盘点：人类历史上所有文本数据总量](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247485448&idx=1&sn=149c4683bd8d1d2f75b444b900503823&chksm=c3546a9bf423e38dcb031eabe5d3f9002714ac13eb29d741b47d3aecde4ae3a0a88a9ce8232e&scene=21#wechat_redirect)[](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247484977&idx=1&sn=e5e4bcc108c8cf6f01dcc305c84fd6ed&chksm=c35464a2f423edb46defe0a8340c82f945a29fbabe851f024a6b13e171ae41f6703f3c3a1a07&scene=21#wechat_redirect)

  • [用时42天，借助AI大模型，创作者们的产品亮相了](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247485306&idx=1&sn=11012a7414b0bc84ea8bf08ab7e122e9&chksm=c35465e9f423ecff178d790b5d45882085dc29aa952e663a81e109fddaca49fc284ae792a795&scene=21#wechat_redirect)