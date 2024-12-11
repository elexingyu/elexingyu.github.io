---
categories: articles
date: 2024-01-04
layout: post
style: huoshui
tags:
- AI
title: AI生产力快报｜13
---

![](/assets/images/40a1c3ee174d4fd7b83f8d1159d5c5b1.gif)

编辑：晓霖

供稿：妙生

**聪明生产力**

  

  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
**用Action打造更强GPTs**  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

大家去 42Master.io 体验 GPTs 了吗？哪款大师最深得你心呢？你想亲手打造一个 GPTs 吗？下面，我们来认识 GPTs
的必杀技之一：Actions。

### 基础方法

如果你是 ChatGPT Plus 用户，在 ChatGPT 页面点击左下角的用户名，选择「My GPTs」，点击「Creat a GPT」即可进入
NewGPT 创建页面。点击「Configure」进入配置页面，Capabilities 部分是 GPTs 提供的三个内置功能「Web
Browsing」「DALL・E Image Generation」「Code
Interpreter」，分别是联网功能、生成图片、代码解释器。如果你不满足于这三个功能，接下来的 Actions 可以连接外部 API，为你的 GPT
添加更多第三方功能。与插件一样，Actions 允许 GPT 集成外部数据，甚至与现实世界交互。一个 GPT 可以添加多个 Action 功能，例如将
GPT 连接到数据库，集成邮件发送功能，让它帮你发邮件。

    
    
    官方介绍：https://platform.openai.com/docs/actions

Actions 的使用方法是点击「Creat new action」，填写 Authentication、Schema、Privacy policy
三个部分。Authentication 填写授权的 API Key 或者 OAuth，没有的话可以选择 None。Privacy policy
填写隐私政策链接。最关键的部分是中间的 Schema，需要遵循 OpenAPI 规范。第一次接触 OpenAPI 的读者可以先了解 OpenAPI
规范，搭配 GPT 官方提供的三个模板作为示范，尝试跑通。

（请注意区分 OpenAPI 与 OpenAI。）  

    
    
    OpenAPI规范：https://swagger.io/specification  
    GPT官方文档：https://platform.openai.com/docs/plugins/getting-started/openapi-definition

### 从外部调用 Schema

如果你不想动手写 Schema，可以点击「Import from URL」，由托管地址导入 Schema 配置。GPT 提供的插件功能实际上也是基于
OpenAPI 规范开发，有部分插件作者会公开自己的 Schema，例如 WebPilot 公开了 Schema
链接，以及对应的隐私政策链接。有了这两个链接，再填写 Configure 页面中 Instructions 部分的提示词，你也可以创建一个带有
WebPilot 功能的 GPT。需要注意的是，这个 GPT 要取消勾选「Web Browsing」，避免产生冲突。

    
    
    Schema URL：https://gpts.webpilot.ai/gpts-openapi.yaml  
    Privacy policy：https://gpts.webpilot.ai/privacy_policy.html

### 在提问中创建 Actions

如果你已经习惯于通过自然语言对话来获取帮助，ChatGPT 还贴心地准备了一个 ActionsGPT，利用文档、代码示例、cURL 命令、介绍等方式帮你创建
Actions。

    
    
    ActionsGPT：https://chat.openai.com/g/g-TYEliDU6A-actionsgpt

  

  

  

  

  

  

  

  

  

  

  

**大模型动态**

  

  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
**2024 AAAI Fellows 名单出炉**  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

AAAI（Association for the Advancement of Artificial
Intelligence）是国际人工智能领域最权威的学术组织之一，每年都会表彰一批通过其研究员计划在人工智能领域持续做出重大贡献的个人。Fellow 是
AAAI 给予会员的最高荣誉，AAAI 每年严格限制入选人数，被誉为「AI 名人堂」。

2024 年度的 AAAI Fellows 评选结果共有 12 位学者入选，其中包括清华大学教授朱军，理由是为机器学习的理论和实践做出了重大贡献。

    
    
    历年评选结果：https://aaai.org/about-aaai/aaai-awards/the-aaai-fellows-program/elected-aaai-fellows

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
**Huggingface：2023 年开源社区发展**  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

在 2023 年，大型语言模型（Large Language Models，简称
LLMs）受到了广泛关注，许多人开始对这些模型的本质和功能有基本了解。是否开源的话题也引起了广泛讨论。开源模型的优势在于，促进了研究的可复制性，鼓励社区参与到人工智能模型的开发中来，帮助他们审视模型中可能存在的偏差和局限性。

Hugging Face 的研究员 Clémentine Fourrier 撰文回顾开源 LLMs
在过去一年的发展历程。从大型企业到初创公司，再到研究实验室，各种主体纷纷发布开源模型，这极大地赋能了社区，使得开源社区以前所未有的速度进行实验和探索。模型的公开出现起伏变化，从年初的公开发布（数据集组合、权重、架构）到年末对训练数据守口如瓶，导致无法复现研究。开源模型出现在包括中国在内许多新的地方，有几个新的参与者将自己定位为语言模型竞争中的强劲竞争者。个性化定制的可能性达到了前所未有的高度，强化学习优化的微调、适配器、合并技术等新策略的出现仅仅是个开始。更小的模型尺寸和量化升级使得大型语言模型对更多人来说真正变得唾手可得！新的架构也随之出现
—— 它们是否最终会取代 Transformer 架构，仍是一个值得关注的问题。

    
    
    中文原文：https://huggingface.co/blog/zh/2023-in-llms

  

  

  

  

  

  

  

  

  

  

  

**AI时代洞见**

  

  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
**吴恩达：未来十年 AI 领域不会改变的事情**  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

在高速发展的 AI
领域，哪些事情在未来十年仍不会改变呢？吴恩达在新年来信中分享了他的观点：我们需要建立一个社区，有朋友和盟友的人通常比孤单一人更能成功；掌握 AI
工具的使用者将更加高效，随着 AI 的持续发展，这一点将更加显著；AI 的高效运作需要优质数据。

这意味着我们要共同努力，继续构建 AI 社区，分享所学，相互激励，寻找合作伙伴；要不断学习，最好让学习成为一种习惯；继续培养以数据为中心的 AI
实践方法，掌控自己的数据是最重要的实践之一。

    
    
    原文：https://www.deeplearning.ai/the-batch/issue-229