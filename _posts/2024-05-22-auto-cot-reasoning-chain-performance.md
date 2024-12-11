---
categories: articles
date: 2024-05-22
layout: post
style: huoshui
tags:
- AI
- 教程
title: Auto-CoT：自动生成推理链，推理性能与人工介入设计思维链相当
---

![](/assets/images/aeb2cdeacc034c6eb3012cd3a8a03f81.png)

这篇论文提出一种自动化的思维链（CoT）提示方法，它通过生成多样化问题的推理链来展示解决问题的过程，这种方法的性能与传统需要人工介入设计思维链的方法相当，甚至可能更优。  

    
    
    论文标题：Automatic Chain of Thought Prompting in Large Language Models   
    作者：Zhuosheng Zhang，Aston Zhang、Mu Li、Alex Smola   
    论文全文：https://arxiv.org/abs/2210.03493   
    代码仓库：https://github.com/amazon-science/auto-cot  
    

论文主要探讨如何在使用大语言模型（LLMs）进行复杂推理任务时，自动生成推理思维链（chain-of-thought，CoT）。

CoT提示是一种促使LLMs生成中间推理步骤的技术，有两种主要范式：

一种是使用简单的提示词（如“Let’s think step by step”）来促进LLMs逐步推理。

另一种是手动为每个问题设计由问题和推理链组成的示例。

虽然手动设计的思维链示例（Manual-CoT）性能更好，但需要大量的人力，而且其性能依赖于精心设计的示例。

作者提出一种自动生成思维链提示的方法（Auto-CoT），通过提出多样化的问题并自动生成推理链来构建示例，不再依赖手动设计示例。

![](/assets/images/afe61c8b99ee42e684231f7731039748.png)

Auto-CoT方法包括两个主要步骤：

首先将给定数据集的问题划分为几个簇，然后从每个簇中选择一个代表性问题，并使用简单的启发式方法通过Zero-Shot-CoT生成其推理链。

Auto-CoT使用“Let’s think step by
step”提示来为每个问题生成推理链，但这种方法生成的链可能包含错误。好在增加问题的多样性可以减轻这些错误的影响。

![](/assets/images/eef08ef46a4e41f784ae7cafe4426967.png)

作者在十个公共基准推理任务上利用GPT-3评估了Auto-CoT，并发现其性能与传统需要人工介入设计思维链的方法相当，甚至可能更优。

实验证明，即使在示例中存在一定比例的错误推理链，多样性也可以帮助维持整体推理性能。

**这表明LLMs可以通过自动构建示例来执行CoT推理。**