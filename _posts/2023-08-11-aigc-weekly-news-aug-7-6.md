---
layout: post
title: "AIGC每周观察[0731-0806]"
date: 2023-08-11
tags: ['AI']
style: huoshui
---


![](/assets/images/33fb7b35841c431f9d9843442ba54a5f.jpg)
​

## 热点回顾  

#### Meta 开源 AudioCraft，可根据文本生成声音和音乐

Meta公司开源了AudioCraft，能够从文本输入生成音频和音乐，简化了音频生成模型的整体设计，使用户能够更容易地与Meta过去几年开发的现有模型互动。AudioCraft包括三个模型：MusicGen、AudioGen和EnCodec。MusicGen从文本输入生成音乐，AudioGen从文本输入生成音效，EnCodec解码器的新版本支持更高质量的音乐生成，减少了对人工的依赖。这三个模型现在可供研究目的使用，以便用户进一步了解这项技术。![](/assets/images/588665d9e58947b181f194761eb7cf4e.jpg)

**探索之问:** AudioCraft 如何改变音乐和音效的生成方式？EnCodec 解码器的新版本如何提高音乐生成的质量？AudioCraft
如何为研究者和实践者提供更多的机会来训练和理解这种技术？

Ref. https://ai.meta.com/blog/audiocraft-musicgen-audiogen-encodec-generative-
ai-audio/

#### 阿里开源「通义千问」通用模型Qwen-7B和对话模型Qwen-7B-Chat

通义千问70亿参数通用模型Qwen-7B和对话模型Qwen-7B-Chat上架魔搭，两款模型均开源、免费、可商用。Qwen-7B是支持中、英等多种语言的基座模型，在超过2万亿token数据集上训练，上下文窗口长度达到8k。Qwen-7B-Chat是基于基座模型的中英文对话模型，已实现与人类认知对齐。这两款模型都可以在魔搭社区下载，用户可以在本地部署或在阿里云机器学习平台PAI上进行训练、部署和推理。

**探索之问:**
通义千问在中英文能力上与其他同类模型相比有何优势？开源大模型对于推动中国AI开源生态的建设有何重要性？阿里云如何计划进一步支持和推动大模型的研究和应用？

Ref.
[https://mp.weixin.qq.com/s/c4qvn0xTChq9xxvdrNa4pQ](https://mp.weixin.qq.com/s?__biz=MzA4NjI4MzM4MQ==&mid=2660237077&idx=1&sn=94bfb7a12a8df58db1ca390a8ab2d215&scene=21#wechat_redirect)

#### OpenAI 7月18日向美国专利商标局 (USPTO) 提交了“GPT-5”的商标申请

OpenAI 已经为 “GPT-5”
提交了一个新的商标申请，该文件于7月18日提交给美国专利和商标局(USPTO)。![](/assets/images/34f6eb8d3b484a3996a204c818da6dc5.jpg)

**探索之问:** GPT-5 会有什么新功能或改进？OpenAI 如何继续在其 GPT 系列中进行创新？GPT-5 的发布可能对 AI 领域产生什么影响？

Ref. https://twitter.com/JoshGerben/status/1686010094373232646?s=20

#### ChatGPT更新了prompt推荐、快捷键等一系列新功能

8月4日，OpenAI 宣布将在接下来的一周内推出一系列小更新，以改进 ChatGPT 的体验：

**提示示例** ：为了帮助用户开始新的聊天，聊天框附近会显示示例。

**建议的回复** ：根据上下文提供对话建议的回复。

**默认使用 GPT-4** ：Plus 用户开始新聊天时，默认选择上次的模型。

**上传多个文件** ：Plus 用户在要求 ChatGPT 分析数据时，支持上传多个文件。

**保持登录状态** ：不再每2周被注销一次。

**键盘快捷键** ：如 ⌘ (Ctrl) + Shift + 复制最后一个代码块，⌘ (Ctrl) + / 查看完整列表。

**探索之问:** ChatGPT 如何进一步增强用户体验？OpenAI 如何根据用户反馈和需求持续优化其产品？

Ref. https://twitter.com/OpenAI/status/1687159114047291392?s=20

#### Jupyter 发布开源的 Jupyter AI —支持多个大模型的 Jupyter Notebook 助手

#### Jupyter 发布免费开源的 Jupyter AI，将生成式人工智能引入 Jupyter
Notebook，为用户提供解释和生成代码、修复错误、总结内容、询问关于本地文件的问题以及从自然语言提示生成整个笔记本的能力。通过强大的命令和聊天界面，Jupyter
AI 可以与来自 AI21、Anthropic、AWS、Cohere 和 OpenAI 等提供商的大型语言模型 (LLM) 进行连接。

![](/assets/images/2a6d375dfdb04e7e81294ddd60919e5a.jpg)

**探索之问:** Jupyter AI 如何改变数据科学家和研究者与 Jupyter 笔记本的互动方式？与其他 AI 工具相比，Jupyter AI
提供了哪些独特的功能？Jupyter AI 如何确保用户数据的隐私和安全？

Ref. https://blog.jupyter.org/generative-ai-in-jupyter-3f7174824862

#### 多个 AIGC 应用在苹果应用商店下架

8月1日凌晨，包括讯飞星火App在内的多个AIGC应用，在苹果商店被集中下架。接近监管部门的人士表示，主要原因是即将于8月15日实施的《生成式人工智能服务管理暂行办法》。这些下架的App在数据采集和使用环节存在不规范之处，比如非法采集，并不是所有信息数据都可以无限制采集；采集到的信息数据二次开发利用，这里的伦理和法律问题还未规范，甚至还有二次开发被用于诈骗等，有些App还涉及数据出境。已经下架的App预计需要很长时间才能再次上架。

**探索之问:**
《生成式人工智能服务管理暂行办法》对于国内AI应用的发展有何影响？数据采集和使用的规范对于AI应用的长期健康发展有何重要性？如何平衡AI技术的快速发展与数据隐私和安全的需求？

Ref. https://36kr.com/p/2370292995368713

## 本周精选

#### What Is ChatGPT Doing … and Why Does It Work?

本文深入浅出地解释了ChatGPT在做什么，以及内部工作原理、其有效性背后的原因。与其他大型语言模型(LLMs)一样，ChatGPT旨在生成与人类书写内容高度相似的文本，基于从数十亿网页中观察到的模式，为任何给定的文本产生一个”合理的延续”。ChatGPT不仅仅是基于最高概率预测下一个单词，它还引入了随机性，以生成多样化和吸引人的内容。文章还谈及神经网络的概念，并将这些计算模型与人类大脑的神经结构进行类比。神经网络，特别是其识别模式和进行区分的能力，在像ChatGPT这样的模型中起到了关键作用。全文阅读：https://writings.stephenwolfram.com/2023/02/what-
is-chatgpt-doing-and-why-does-it-work/**探索之问:** 1\.
在预测中引入随机性是如何导致ChatGPT生成更具吸引力和多样化的内容的？2\.
神经网络在哪些方面模仿了人类大脑的功能，这种相似性如何有助于它们在图像识别等任务中的成功？

3\. 考虑到语言的广泛性和复杂性，ChatGPT是如何管理生成连贯和与上下文相关的内容的？

#### The Transformer Blueprint: A Holistic Guide to the Transformer Neural
Network Architecture

本文深入探讨了Transformer，这个在2017年的著名论文“attention is all you
need”中引入的神经网络架构。文章详细讨论了Transformer的应用、影响、挑战和未来方向。Transformer最初是作为神经机器翻译的工具而诞生的，但它的应用远远超出了自然语言处理(NLP)的范围，成为了一个多功能和通用的神经网络架构。文章还详细探讨了Transformer模型的每一个关键组件，从其注意力机制到其编码器-
解码器结构。全文阅读：https://deeprevision.github.io/posts/001-transformer/**探索之问:** 1\.
Transformer如何改变了人们对神经网络架构的看法？2\. 除了NLP，Transformer还可以应用在哪些领域？

3\. 未来Transformer架构可以有哪些变化和改进？

#### Open Problems and Fundamental Limitations of Reinforcement Learning from
Human Feedback

本文探讨了人类反馈强化学习（RLHF）的开放问题和基本限制。RLHF 是一种训练 AI
系统与人类目标对齐的技术，已成为微调最先进的大型语言模型（LLMs）的核心方法。尽管 RLHF 很受欢迎，但对其缺陷的公开研究相对较少。文章包括 (1)
调查 RLHF 及相关方法的开放问题和基本限制；(2) 概述理解、改进和补充 RLHF 的技术；(3) 提议审计和披露标准以提高 RLHF
系统的社会监督。文章强调了 RLHF 的局限性，并突出了开发更安全的 AI
系统多方面方法的重要性。全文阅读：https://arxiv.org/pdf/2307.15217.pdf**探索之问:** 1\.
在RLHF中，如何有效地获得人类的高质量反馈，并处理人类反馈的不完美？2\. 在RLHF中，如何获取有代表性和有助于使用者的数据？

3\. 在RLHF中，如何平衡反馈的丰富性与效率之间的矛盾？

#### Agent：OpenAI的下一步，亚马逊云科技站在第5层

OpenAI的创始成员Andrej
Karpathy在黑客马拉松上表示，相比大模型训练，OpenAI更关注Agent领域。Agent可以理解为能自主理解、规划、执行复杂任务的系统。Agent正在酝酿第二轮爆发，将与应用和场景结合得更紧密。例如，开源项目Sweep与GitHub整合，自动处理bug报告和功能请求。初创公司Seednapse
AI提出了构建AI应用的五层基石理论，包括Models、Prompt Templates、Chains、Agent和Multi-
Agent。亚马逊云科技也在Agent领域发力，推出了Amazon Bedrock
Agents新功能，这类服务从第五层开始，降低了开发门槛。全文阅读：[https://mp.weixin.qq.com/s/5N5H2yqiCKWtM34ngjk6Hw](https://mp.weixin.qq.com/s?__biz=MzIzNjc1NzUzMw==&mid=2247689266&idx=1&sn=0446f069305593b4698eebb92827837d&scene=21#wechat_redirect)**探索之问:**
1\. 如何定义Agent，并将其应用于实际业务中？2\. 如何在实际应用中实践五层基石理论？3\.
在Agent领域，亚马逊云科技如何利用其技术和资源优势持续发力？

![](/assets/images/ac7d51bbd6314aecb1830260557e7324.png)


