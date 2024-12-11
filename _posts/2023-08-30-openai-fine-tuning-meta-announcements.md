---
categories: articles
date: 2023-08-30
layout: post
style: huoshui
tags:
- AI
title: OpenAI推出微调服务，Meta疯狂输出…｜微调特刊
---

![](/assets/images/956e6d9643184ff4a98a92defb62e51f.jpg)


**热点回顾**  

**1**

**OpenAI 发布 GPT-3.5 Turbo 微调和 API 更新，提升模型性能**

  
  
  
  
  

OpenAI 最近发布了关于其 GPT-3.5 Turbo 模型的微调（fine-tuning）和 API
更新的信息。这次更新允许开发者自定义模型，以更好地适应各种用例，并能在大规模下运行这些定制模型。早期测试显示，经过微调的 GPT-3.5 Turbo
在某些特定任务上甚至能超过基础版的
GPT-4。该更新还强调了微调的多种用例，包括改善模型的可控制性、输出格式的一致性以及定制输出的语气。此外，微调还可以缩短提示长度，同时保持相似的性能表现。微调与其他技术（如提示工程、信息检索和函数调用）结合使用时效果最佳。OpenAI
还计划在今年秋季推出支持函数调用和 gpt-3.5-turbo-16k 的微调。为了确保微调的安全性，所有微调训练数据都会通过 OpenAI 的审查 API
和基于 GPT-4 的审查系统进行筛查。

ref. https://openai.com/blog/gpt-3-5-turbo-fine-tuning-and-api-updates

  
  

  

**2**

**Meta 推出 SeamlessM4T：一站式多语言、多任务翻译模型**

  
  
  
  
  

Meta 公司推出了一款名为 SeamlessM4T 的多语言、多任务模型，该模型能够在语音和文本之间无缝地进行翻译和转录。SeamlessM4T 支持近
100
种输入和输出语言的自动语音识别、语音到文本翻译、语音到语音翻译、文本到文本翻译以及文本到语音翻译。该模型是在开放科学的原则下公开发布的，允许研究人员和开发者在此基础上进行进一步的开发。SeamlessM4T
还发布了一个名为 SeamlessAlign 的大型开放多模态翻译数据集，该数据集包含了 270,000
小时的语音和文本对齐数据。该模型不仅提高了对低资源和中等资源语言的性能，还在高资源语言（如英语、西班牙语和德语）上保持了强劲的性能。Meta
公司表示，这一工作是向创建通用翻译器迈出的重要一步，该翻译器将使使用不同语言的人能够更有效地进行沟通。

ref. https://ai.meta.com/blog/seamless-m4t/

  
  

  

**3**

**Meta 发布 Code Llama：一款多功能的编程专用大型语言模型**

  
  
  
  
  

Meta 公司发布了一款名为 Code Llama 的大型语言模型（LLM），专门用于编程任务。Code Llama 基于 Llama 2
构建，具有生成代码和自然语言描述代码的能力。该模型有三个版本：基础版 Code Llama、专门用于 Python 的 Codel
Llama，以及针对自然语言指令进行微调的 Code Llama - Instruct。Code Llama
在编程任务方面表现出色，不仅可以提高开发者的工作效率，还可以降低编程入门门槛。该模型支持多种流行编程语言，包括 Python、C++、Java
等，并提供了不同大小的模型以满足不同的性能和延迟需求。此外，Code Llama 还经过了严格的性能和安全性评估，其开源许可证允许研究和商业用途。

ref. https://ai.meta.com/blog/code-llama-large-language-model-coding/

论文地址：https://ai.meta.com/research/publications/code-llama-open-foundation-
models-for-code/

GitHub 地址：https://github.com/facebookresearch/codellama

  
  

  

**4**

**在 Excel 中无缝集成 Python：数据分析的新里程碑**

  
  
  
  
  

Microsoft 近日发布了 Excel 中的 Python 公开预览版，实现了 Python 和 Excel 分析在同一 Excel
网格中的无缝集成。这一新功能允许用户在熟悉的 Excel 环境中进行高级数据分析，无需额外设置或安装。用户可以直接从 Excel 的功能区访问
Python，通过 Excel 的内置连接器和 Power Query 轻松将外部数据导入 Python 在 Excel
中的工作流程。此外，Microsoft 与 Anaconda 合作，利用运行在 Azure 中的 Anaconda 发行版为 Python
提供支持，包括流行的 Python 库如 pandas、statsmodels、Matplotlib 和 seaborn 等。用户还可以在
Microsoft Teams 和 Microsoft Outlook 等工具中分享工作簿和 Python 分析，实现无缝协作。Python 在 Excel
中的运行得到了企业级的安全保障，作为 M365 连接体验的一部分。

ref. https://techcommunity.microsoft.com/t5/microsoft-365-blog/introducing-
python-in-excel-the-best-of-both-worlds-for-data/ba-p/3905482

  
  

  

**5**

**IJCAI2023 奖项公布：揭晓 AI 顶级论文与创新技术**

  
  
  
  
  

该文章报道了 2023 年国际人工智能联合会议（IJCAI）的奖项公布情况。IJCAI 是 AI 领域的顶级学术会议，今年在澳门举行。会议共接收了 4566
篇完整论文，最终接收了 643 篇，接收率约为 14%。在杰出论文奖方面，获奖机构包括 Google
DeepMind、阿尔伯塔大学、阿姆斯特丹大学和莱比锡大学等。其中一篇论文展示了神经网络可以被替换为更优的上下文模型，在多个基准测试中表现出色。另一篇论文则是关于基于
SAT 的知识获取方法，该方法在多个数据集上的运行时间明显低于现有方法。还有一篇论文关注了安全强化学习，提出了一种新的安全 RL 技术。此外，AIJ
突出论文奖和 AIJ 经典论文奖也在会议上公布。

ref. https://www.thepaper.cn/newsDetail_forward_24349964

  
  

  

**2**  
** 本周精选  **  

  

**DeepLearning AI 推出**

**微调 LLM 的新课程**

**1**

  

Lamini 首席执行官 @realSharonZhou 和吴恩达（Andrew Ng）在课程中讲解微调大型语言模型 (LLM)
的基础知识，以及如何使用自己的数据训练开源 LLM。

课程地址：https://www.deeplearning.ai/short-courses/finetuning-large-language-
models/

  

**AI 开发：使用提示、微调**

**​和****搜索引擎的对比与权衡**

**2**

  

本文探讨了 AI 开发中三种主要方法：提示（Prompting）、微调（Fine-Tuning）和搜索引擎嵌入（Search Engine
Embeddings）的优缺点。「提示」方法具有快速迭代、低成本和灵活性的优点，几乎消除了数据收集、模型训练和基础设施方面的开销。「微调」在处理复杂任务、提供高精度和稳定性方面具有优势，尤其是当有大量高质量的域内训练数据可用时。「搜索引擎」嵌入则提供了一种简单、灵活和可解释的方法，特别适用于需要快速访问不断增长的数据的应用。文章最后指出，这三种方法各有所长，可以结合使用以构建更强大和健壮的
AI 产品。

文章地址：https://medium.com/intuitionmachine/ai-development-tradeoffs-using-
prompting-fine-tuning-and-search-engine-embeddings-91ff75beb7e2

  

**一个简单的 LLM 微调 UI**

**3**

  

AutoTrain Advanced 是一个由 Hugging Face 公司开发的开源项目，专注于机器学习模型的快速和简便的训练与部署。该项目支持
Python 3.8 以上版本，并可通过 PIP 进行安装。项目提供了多种预训练模型和 Fine Tuning 的教程，如 LLM Fine Tuning
和 DreamBooth Training。

项目地址：https://huggingface.co/autotrain

代码：https://github.com/huggingface/autotrain-advanced

  

![](/assets/images/a3ad3ab05464409395101ca599bacc98.png)

欢迎加入阳志平老师创办的「玩转GPT」知识星球，了解更多前沿论文、使用技巧、原创产品，与 2100+ 成员一起碰撞无限创意！

**👇 加入知识星球，一起玩转GPT！**

![](/assets/images/2375836909bb40ebbcad675347f146d8.jpg)