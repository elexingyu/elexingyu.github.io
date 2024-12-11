---
categories: ['articles']
date: 2024-04-24
layout: post
style: huoshui
tags:
- AI
- 教程
title: 微软推出Phi-3Mini！性能超过两倍大小的模型
---

![](/assets/images/6aa4367c77224bc79e780a53cf260ec5.png)  

最近，微软刚推出了其轻量级AI模型Phi-3 Mini，这是微软计划发布的三个小型语言模型中的第一个。

Phi-3 Mini拥有38亿个参数，与GPT-4等大型语言模型相比，其在一个较小的数据集上训练而来。它现已在Azure、Hugging
Face和Ollama上推出。

微软计划发布Phi-3 Small(70亿参数)和Phi-3 Medium(140亿参数)。参数指的是模型可以理解的复杂指令的数量。  

![](/assets/images/9447a918f5254ac789551d8453b99543.jpg)

_上图直观地展示了Phi-3模型的性能。通过在大规模多任务语言理解(MMLU)基准测试中的对比,可以看出其相较于其他同等规模的模型有着怎样的优势。(图片由微软提供)_

微软在去年12月发布了Phi-2，其性能与Llama
2等更大的模型一样出色。微软表示，Phi-3的性能优于上一版本，可以提供接近于比它大10倍的模型的响应。

微软Azure AI平台的公司副总裁Eric Boyd告诉The Verge，Phi-3
Mini的能力与GPT-3.5等大型语言模型相当，"只是以更小的形式呈现"。

与大型模型相比，小型语言模型通常运行成本更低，在手机和笔记本电脑等个人设备上表现更好。

The Information 今年早些时候报道称，微软正在组建一个专门研究轻量级语言模型的团队。除了Phi，该公司还开发了专注于解决数学问题的 Orca-
Math 模型。

微软的竞争对手也有自己的小型语言模型，其中大多数针对文档摘要或编码辅助等更简单的任务。谷歌的Gemma 2B和7B适用于简单的聊天机器人和语言相关工作。

Anthropic的Claude 3 Haiku可以快速阅读带有图表的密集研究论文并进行总结，而Meta最近发布的Llama 3
8B可用于某些聊天机器人和编码辅助。

Boyd表示，开发人员使用"课程"训练Phi-3。他们的灵感来自于儿童如何从睡前故事、使用简单词汇和句子结构谈论更大主题的书籍中学习。

"没有足够的儿童读物，所以我们列出了3000多个单词，并要求一个大型语言模型制作'儿童读物'来教Phi，"Boyd说。

他补充说，Phi-3只是在之前版本学到的基础上进行了构建。Phi-1专注于编码，Phi-2开始学习推理，而Phi-3在编码和推理方面表现更好。

虽然Phi-3系列模型掌握了一些通用知识，但在广度上无法超越GPT-4或其他大型语言模型——在整个互联网上训练的大型语言模型与Phi-3等较小模型可以给出的答案之间存在很大差异。

![](/assets/images/65dd973bb47e4286930b23d1f94574f1.png)

Boyd表示，像Phi-3这样的小型语言模型更适合其定制应用程序，因为对于许多公司来说，其内部数据集无论如何都会比较小。

而且由于这些模型使用的计算能力更少，因此通常更加经济实惠。

**相关链接**

- https://news.microsoft.com/source/features/ai/the-phi-3-small-language-models-with-big-potential/
- https://azure.microsoft.com/en-us/blog/introducing-phi-3-redefining-whats-possible-with-slms/
- https://www.theverge.com/2024/4/23/24137534/microsoft-phi-3-launch-small-ai-language-model
- Phi-3技术报告：https://export.arxiv.org/abs/2404.14219