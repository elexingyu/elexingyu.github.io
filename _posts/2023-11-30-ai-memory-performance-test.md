---
layout: post
title: "AI生产力快报｜08"
date: 2023-11-30
tags: ['AI']
style: huoshui
author: 晓霖
---


![](/assets/images/495d4aed99ec4a0ba7b804fd3d790648.gif)

编辑：晓霖

**聪明生产力**

  

  
  
  
**实测大模型在长上下文中的记忆表现**  
  
  

Greg Kamradt 用「大海捞针」的方式测试了 GPT-4-128K 和 Claude2.1 (200K Tokens)
对长上下文的回忆能力。他发现，尽管大模型支持更长的上下文窗口，一旦上下文长度超过一定的阀值，大模型对上下文内容的回忆能力就会明显降低，提供的答案更容易出错。

  

**测试方法**

  

以 Paul Graham 的 218 篇文章作为背景材料，在文档不同深度插入随机陈述：“在阳光明媚的日子里，在多洛雷斯公园吃三明治是在旧金山最佳活动。”
让大模型只使用所提供的上下文来回答指定问题，然后使用搭载 GPT-4 的 LangChain 评估工具来评估大模型生成的答案。

  

Greg 先测试了 GPT-4-128，用 15 种文档深度（均匀分布在文档开头的 0% 到结尾的 100%之间）和 15 种上下文长度（从 1K 到
128K Token）进行重复测试。测试 Claude2.1 时，为了在文档开头和结尾部分发现更多细节，他对文档深度采用了 Sigmoid
分布方式来进行测试，并将文档深度和上下文长度都增加到 35 种。

  

**测试结果**

  

当上下文长度超过 73K Token 时，GPT-4 的记忆表现开始下降。无论上下文有多长，GPT-4
都能记住文档开头的内容，但文档开头比文档结尾的记忆效果差一些。当内容位于文档深度的 7%-50% 区间时，GPT-4 的记忆表现较差。

  

与 GPT-4 类似，文档开头和结尾的事实几乎能被 Claude2.1 完美记住，而且开头比结尾的记忆效果稍差一些。当文档长达 20k Token
时，Claude 2.1 能够回忆起位于文档特定深度的事实。当文档长度大于 90k Token
时，文档结尾的记忆效果开始下降，但即使文档长度较短，也不能保证记忆效果。

  

**结 论**

  

提示工程很关键，但不要指望你发送的上下文信息总是能够被大模型检索到。尽管大模型支持的上下文长度不断增加，缩减上下文长度可以提高大模型记忆的准确性。与人类记忆类似，放在文档开头和后半部分的内容更容易被大模型记住。

  

**花 絮**

  

Greg
认为，使用大语言模型时，非常有必要理解模型的工作方式、优势和局限性。这类测试并不完全严谨和可靠，却可以通过真实案例，让大家感受大模型的工作原理，并将这些知识应用到实际使用场景中。

  

为了调用 API 测试 GPT-4-128K 和 Claude2.1在不同上下文长度的记忆表现，Greg 分别花费了约 200 美元和约 1016
美元。Claude2.1 的上下文长度更长，测试次数更多，花费也更多。测试 Claude2.1 时，Anthropic
团队提供了测试信用，并给出了最大化性能的提示建议。Greg 强调，Anthropic
团队的参与仅限于提供后勤支持。这项测试保持了独立性和完整性，确保他的发现没有偏见，并且未受到 Anthropic 团队支持的影响。

  

Greg 提醒大家，更改提示词、问题、待检索的事实和背景上下文都会影响性能，当大模型被要求同时回忆多个事实或进行合成推理时，性能可能会降低。

  

  

  

  

  

  

  

  

  

  

  

  

**大模型动态**

  

  
  
  
**Hugging Face 社区最受欢迎的 15 家 AI 机构**  
  
  

**Stability AI：** Stable Diffusion 背后的公司之一。

  

**Meta AI：** 开源了 Llama 模型，开发了 Emu、Wav2Vec、AudioCraft、SeamlessM4T
等多项增强现实和虚拟现实领域的 AI 技术。

  

**Runway：** 开发的视频生成工具 Gen-2，是生成式 AI 视频领域的标杆。

  

**CompVis：** 慕尼黑路德维希・马克西米利安大学计算机视觉与学习研究小组（前身为海德堡大学计算机视觉小组），与 Runway 的研究人员共同开发了
Stable Diffusion 模型。

  

**清华 KEG 实验室：** 开发了 ChatGLM2-6B 开源大模型，专注于知识图谱、自然语言处理等领域。

  

**BigScience：** 由 HuggingFace、GENCI 和 IDRIS 发起的开放式协作组织，汇聚了全球 1000 多名研究人员，开发了拥有
1760 亿参数的大模型 BLOOM。

  

**TIIuae：** 阿联酋技术创新研究所，开发了 Falcon 180B 开源大模型。

  

**Microsoft：** 推出了 Azure 云平台、Bing 和 Copilot 等流行的 AI 产品。

  

**GoogleAI：** 从 AI 基础研究到 AI 产品，再到 AI 行业的基础设计建设，都以领先的 AI 技术而闻名，例如
TensorFlow、Google Brain、BERT、Bard、Palm 等等，在开源社区亦有诸多贡献。旗下的 DeepMind 在 AI
领域不断取得令人瞩目的突破。

  

**OpenAI：** 开发了 GPT 系列大模型和 DALL・E 图像生成模型，开源了语音识别模型 Whisper。

  

**BigCode Project：** 一个开放的科学合作项目，开发的 StarCoder 是一个 160 亿参数的代码模型，还发布了
OctoPack（用于指令调优大型代码模型的工件）、The Stack（最大的可用预训练数据集）、SantaCoder (1.1B 参数的代码模型)。

  

**MosaicML：** 专注于优化和加速机器学习模型的训练过程，开源了可商用的 MPT-7B 和 MPT-30B 模型。

  

**UKP Lab：** 德国达姆施塔特技术大学的 UKP 实验室，专注于自然语言处理和机器学习的研究，重点关注大型语言模型、对话式人工智能、问答、跨文档
NLP 以及新颖的数据集和问题定义。

  

**EleutherAI：** 一个开源的社区人工智能项目，发布了 The Pile（多样化文本数据集）、GPT-J、GPT-NeoX 以及 Pythia
系列大模型。

  

**Salesforce：** 创始人是提出云计算和 SaaS 理念的 Marc Benioff，致力于将 AI 整合到办公即时通讯软件，并为销售人员推出了
Einstein GPT。

  

  

  

  

  

  

  

  

  

  

  

  

  
  
  
**当今 LLM 应用程序的体系结构**  
  
  

本文介绍了构建自己第一个 LLM 应用程序的五个主要步骤、LLM 应用的新兴架构，以及你可以立即开始探索的问题领域。

  

构建大语言模型应用的五个主要步骤是专注解决一个问题、选择合适的大语言模型（许可、规模、性能）、定制大语言模型（上下文学习、RLHF
或者微调）、构建应用的架构（用户输入、输入增强和提示构建工具、高效且负责任的 AI 工具）、对你的应用进行在线评估。

  

在 LLM 应用的新兴架构部分，本文以 Dave 利用一个基于大语言模型 (LLM) 的智能助手帮助他及时修复断线 Wi-Fi
的经历为例，逐步解析大语言模型应用的用户操作流程，以及搭建这样一个应用所需要的各种工具。

  

如果你正在寻找创新灵感或探索的新问题领域，可以通过 NASA 和 IBM 最近开源的地理空间 AI 模型、约翰霍普金斯应用物理实验室设计的对话型 AI
代理、Duolingo 和 Mercado Libre 等公司利用 GitHub Copilot 帮助更多人免费学习外语这 3 个项目，了解 LLM
应用和模型如何在真实世界中发挥作用。

  

如果你正在构建自己的 LLM 应用，不妨参考文章所列的步骤、架构、工具和实例。

  

    
    
    原文地址：https://github.blog/2023-10-30-the-architecture-of-todays-llm-applications  
    中文翻译：https://baoyu.io/translations/llm/the-architecture-of-todays-llm-applications

  

  

  

  

  

  

  

  

  

  

  

  

  

**AI时代洞见**

  

  
  
OpenAI 首席科学家 **Andrej Karpathy 的大模型科普演讲**  
  
  

如果你知道 Andrej Karpathy，相信你必然不会错过这个视频。

> Andrej Karpathy 是 OpenAI 创始成员，特斯拉前 AI 总监，目前回到 OpenAI。他曾被评为《麻省理工学院技术评论》2020
> 年度 35 岁以下创新者之一，是自然语言处理、计算机视觉、深度学习等领域专家。他主讲的斯坦福大学第一门深度学习课程「CS
> 231n：视觉识别的卷积神经网络」从 2015 年的 150 名学生增长到 2017 年的 750 名，成为斯坦福大学最大的班级之一。

在这个最新演讲视频中，Andrej Karpathy 类比如今的操作系统，为普通大众科普了 ChatGPT、Claude 和 Bard
等大语言模型的背景知识和基础原理，包括这些技术的现状与未来，以及这种新计算范式面临的安全挑战。

  

顶级大牛用通俗易懂的方式为你讲解前沿领域的专业知识，而且这些知识全部更新到 2023 年 11 月，这些在发展迅猛的 LLM
领域显得尤为珍贵。无论你是机器学习行家，还是 AI 领域新手，这个演讲都很值得一听。

  

    
    
    视频地址：https://youtu.be/zjkBMFhNj_g  
    中文字幕：https://www.bilibili.com/video/BV1Hj41177fb

  

如果你想深入探索大语言模型，可以参考 _Reading List For Andrej Karpathy’s “Intro to Large
Language Models” Video_ 这篇文章整理的阅读清单，进一步了解视频中提及的资源、学术论文和重要概念。

  

    
    
    文章地址：https://blog.oxen.ai/reading-list-for-andrej-karpathys-intro-to-large-language-models-video  
    中文翻译：https://baoyu.io/translations/llm/reading-list-for-andrej-karpathys-intro-to-large-language-models-video

  

  

  

  

  

  

  

  

  

  

  

  

**Referenc e**

    
    
    https://x.com/GregKamradt/status/1722386725635580292  
    https://x.com/GregKamradt/status/1727018183608193393  
    https://mp.weixin.qq.com/s/t2C5SeXuT1pNmdblMsLN0g  
    https://en.wikipedia.org/wiki/Andrej_Karpathy

**![](/assets/images/55f9b2199d7d41138cf31060394353e6.png)**

  
**活水智能**
致力于通过人工智能提高知识工作者的生产力，作为「AI时代的生产力专家」，我们的核心目标是为用户提供最先进的AI技术和工具，帮助用户更高效、更智能地完成工作。

