---
layout: post
title: "AI生产力快报｜11"
date: 2023-12-21
tags: ['AI']
style: huoshui
---


![](/assets/images/b192cd858f0b452f8db9b2a0b00f2fc8.gif)

编辑：晓霖

**聪明生产力**

  

  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
**OpenAI Prompt Engineering**  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

OpenAI 发布官方的 Prompt engineering 文档，分享了利用 GPT 获取更优结果的六个策略。

**一、撰写清晰的指令：** 模型对你想要的东西猜测得越少，输出好答案的可能性就越大。

**二、提供参考文本：** 提供参考文本可以减少捏造的答案。

**三、将复杂任务拆分为简单的子任务：**
复杂的任务往往比简单的任务更容易出错；将复杂任务重新定义为更简单任务的工作流后，早期任务的输出可作为后期任务的输入。

**四、给模型“思考”时间：** 模型在试图立即回答推理问题时更容易犯错，“思维链”可以帮助模型更可靠地推理出正确答案。

**五、使用外部工具：** 通过向模型提供其他工具的输出来弥补模型的弱点，例如文本检索系统（RAG）、代码解释器、模型特定功能等。

**六、系统地测试和调整：** 在某些情况下，对提示的修改会在一些孤立的示例上获得更好的性能，但在更具代表性的示例集上会导致更差的整体性能。

每个策略下都列出了具体技巧以及示例，你还可以组合使用这些策略获得更好的回答效果。一般来说，如果一个任务在某个模型上处理失败，通常值得用更强的模型再试一次。

    
    
    文档地址：https://platform.openai.com/docs/guides/prompt-engineering  
    更多案例：https://platform.openai.com/examples

  

  

  

  

  

  

  

  

  

  

  

  

**大模型动态**

  

  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
**Mistral AI 开源首个 MoE 大模型**  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

近期，Mistral AI 开源了基于 MoE（Mixture-of-Experts，混合专家）架构的 Mixtral 8x7B 模型，性能达到 Llama
2 70B 和 GPT-3.5 的水平，处理输入和生成输出的速度和成本则相当于 12.9B 的模型。

### MoE 的优点

Mixture-of-Experts (MoE) 是一种深度学习架构，在1991年的论文《Adaptive Mixture of Local
Experts》首次被提出，核心思想是将一个大型问题分解为许多较小的子问题，并由一组“专家”网络各自解决这些子问题。每个“专家”是一个较小的模型，专门处理特定类型的输入数据或任务。MoE的一个重要组件是门控网络（Gating
Network），负责决定哪个专家应该处理当前的输入数据。这个决策基于输入数据的特性，目的是将数据发送到最能有效处理该任务的专家。

通常，模型规模的拓展会显著增加训练成本。MoE
模型具有优异的可扩展性，可以根据任务需求灵活地调整专家的数量和类型，使其适应不同的应用场景。由于各个专家可以独立操作，MoE
模型特别适合并行处理，大大加快训练和推理速度。即使增加专家数量扩展成更大的模型，在处理更大的数据集和更复杂的任务时，MoE
模型不会显著增加每个输入的处理时间。更重要的是，并非所有专家都需要参与处理每个输入，MoE
模型在处理大规模和复杂问题时可以更有效地利用资源，达到节省计算资源的效果。

若想进一步了解MoE的构建模块、训练方式、推理权衡等内容，Hugging Face 的博客文章《Mixture of Experts
Explained》不容错过！

### Mixtral 8x7B 模型

Mixtral 8x7B 模型是具有开放权重的高质量稀疏专家混合模型（SMoE），是一个 decoder-only 的模型，由8组“专家”组成，在每个
token 的推理过程中只使用2个“专家”，并将其输出累加组合。模型总参数量为 46.7B，但每个 token 只使用其中 12.9B
参数，即实际执行速度和所需的成本相当于一个 12.9B 的模型。模型上下文窗口为
32k，可处理英语、法语、意大利语、德语和西班牙语等多种语言，在代码生成方面表现优异。Mixtral 使用公开数据进行预训练。

Mixtral 8x7B 模型遵循 Apache 2.0 许可，可免费商用。API 分为三个版本：Mistral-tiny 对应模型是 Mistral 7B
Instruct；Mistral-small 对应模型是 Mixtral 8×7B；Mistral-medium 对应的模型尚未公布，官方透露其在 MT-
Bench 上的得分为 8.3 分。

    
    
    Mistral AI官网介绍：https://mistral.ai/news/mixtral-of-experts  
    Hugging Face的博客文章：https://huggingface.co/blog/moe

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
**NeurIPS 2023 获奖论文出炉型**  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

NeurIPS（Neural Information Processing Systems，神经信息处理系统大会）是全球最著名的 AI
学术会议之一，通常在每年 12
月举办，讨论深度学习、计算机视觉、大规模机器学习、学习理论、优化、稀疏理论等众多细分领域。NeurIPS与ICML、ICLR并称机器学习领域国际三大顶会，代表人工智能领域研究最高水平。

NeurIPS 官方公布了 2023
年度的获奖论文，包括时间检验奖、两篇杰出论文、两篇杰出论文（亚军）、一个杰出数据集和一个杰出基准，其中大部分论文都是围绕大型语言模型（LLM）展开的工作。

### 时间检验奖

#### Distributed Representations of Words and Phrases and their
Compositionality

这篇十年前的论文引入了开创性的词嵌入技术 word2vec，展示了从大量非结构化文本中学习的能力，推动了自然语言处理新时代的到来。论文作者是当时仍在谷歌的
Tomas Mikolov、Ilya Sutskever、Kai Chen、Greg Corrado、Jeffrey Dean，论文被引量超过 4 万次。

    
    
    https://arxiv.org/abs/1310.4546

### 杰出论文奖

#### Privacy Auditing with One (1) Training Run（谷歌）

    
    
    https://arxiv.org/abs/2305.08846

#### Are Emergent Abilities of Large Language Models a Mirage?（斯坦福大学）

    
    
    https://arxiv.org/abs/2304.15004

### 杰出论文（亚军）

#### Scaling Data-Constrained Language Models（Hugging Face、哈佛大学、图尔库大学）

    
    
    https://arxiv.org/abs/2305.16264

#### Direct Preference Optimization: Your Language Model is Secretly a Reward
Model（斯坦福大学、 CZ Biohub）

    
    
    https://arxiv.org/abs/2305.18290  
    

### 杰出数据集论文

#### ClimSim: A large Multi-scale Dataset for Hybrid Physics-ML Climate
Emulation

    
    
    https://arxiv.org/abs/2306.08754  
    项目地址：https://leap-stc.github.io/ClimSim/README.html  
    

### 杰出基准论文

#### DECODINGTRUST: A Comprehensive Assessment of Trustworthiness in GPT
Models

    
    
    论文：https://arxiv.org/abs/2306.11698  
    基准测试：https://decodingtrust.github.io

  

  

  

  

  

  

  

  

  

  

  

**AI时代洞见**

  

  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
**对话：AI如何成为促进个人发展的强大工具**  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

领英（LinkedIn）创始人雷德· 霍夫曼（Reid
Hoffman）对话多位人工智能领域专家，深入探讨了人工智能可以如何成为促进个人发展的强大工具，为人们提供独特视角、提升协作、增进人际关系和实现远大目标。

    
    
    https://www.36kr.com/p/2523219973449217

