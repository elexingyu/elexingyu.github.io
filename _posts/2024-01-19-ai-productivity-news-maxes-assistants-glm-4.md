---
layout: post
title: "AI生产力快报｜15"
date: 2024-01-19
tags: ['AI']
style: huoshui
---


![](/assets/images/fe8d805430f8410c9220a7bbc55123dd.gif)

编辑：晓霖

供稿：妙生

**聪明生产力**

  

  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
**调用 MiniMax Assistants API 创建智能助手**  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

MiniMax Assistants API 是基于大语言模型构建的、支持多种工具链能力的有状态 API。与 Chat completion API
相比，最大的区别是交互的维度从单轮对话，变成了更完整的一个事件、一次行为。目前 Assistants API 支持以下四种工具：

  * • Code Interpreter（代码解释器）

  * • Retrieval（知识库检索）

  * • Function Calling（函数调用）

  * • Web Search（网络搜索）

### 举个例子：智能客服

> **场景：** 某用户在直播间下单后，发现购买的食品已过期。客户向客服反应，并要求退货 / 退款。
>
>  
>
>
> **传统客服应用：** 通常需要额外开发一套流程管理工具，设计复杂的处理流程，要求用户填写和选择各种选项来解决问题。
>
>  
>
>
> **基于 Assistants API 的智能助手：** 在理解用户意图后，agent 自主引导用户提供订单号码，并自动调用 function
> calling 核验订单细节，生成客诉单号和链接，向用户发送退款 / 退货链接。

### 构建步骤

  * • 通过 Assistants API 创建一个 assistant id 并选择模型，如有需要可考虑关联上传好的 file 并开启 Code Interpreter、Retrieval 和 Function calling、Web Search 等工具。注意，只有关联 file 并开启 retrieval 时，retrieval 才会生效。

  * • 用户发送请求时，通过 Thread API 创建一个 thread id，并通过 Message 向 thread id 创建并添加一条 message id。

  * • 使用 thread id 关联 assistant id 创建 run，运行以得到请求回复，有需要时该 Assistant 会自动使用 file 调用此前启用的相关工具。

  * • 通过 retrieve run 检索 run 的完成状态，如已完成，可以通过 list message 查看回复

    
    
    操作指南：https://api.minimax.chat/document/guides/Assistants/operate  
    官方文档：https://api.minimax.chat/document/guides/Assistants/document  
    

  

  

  

  

  

  

  

  

  

  

  

**大模型动态**

  

  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
**幻方开源 MoE 大模型 DeepSeekMoE**  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

幻方开源自研 MoE 大模型 DeepSeekMoE，全新架构，支持中英文，免费商用。

### 两大创新

> **细粒度专家划分：** 不同于传统 MoE 直接从与标准 FFN 大小相同的 N 个专家里选择激活 K 个专家（如 Mistral 7B*8 为 8
> 选 2），幻方把 N 个专家粒度划分更细，在保证激活参数量不变的情况下，从 mN 个专家中选择激活 mK 个专家（如 DeepSeekMoE 16B 为
> 64 选 8），可以更加灵活地组合多个专家。
>
>  
>
>
> **共享专家分离：** 把激活专家区分为共享专家（Shared Expert）和独立路由专家（Routed
> Expert），将共享和通用的知识压缩进公共参数，减少独立路由专家参数之间的知识冗余。

### 模型表现

> 在相同语料下训练 2 万亿 token，DeepSeekMoE 16B 模型（实际激活参数量为 2.8B）性能匹敌 DeepSeek 7B Dense
> 模型，同时节省了 60% 的计算量。
>
>  
>
>
> 与目前 Dense 模型的开源代表 LLaMA2 相比，DeepSeekMoE 16B 在大部分数据集上性能领先 LLaMA2 7B，且仅用了 40%
> 计算量。
    
    
    官方介绍：https://mp.weixin.qq.com/s/T9-EGxYuHcGQgXArLXGbgg  
    模型下载：https://huggingface.co/deepseek-ai  
    微调代码：https://github.com/deepseek-ai/DeepSeek-MoE  
    技术报告：https://github.com/deepseek-ai/DeepSeek-MoE/blob/main/DeepSeekMoE.pdf

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
**智谱AI 发布新一代基座大模型 GLM-4**  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

智谱 AI 技术开放日 (Zhipu DevDay)」当天，GLM 技术团队推出新一代基座大模型 GLM-4，包括对标 OpenAI 的 All
Tools、GLMs、Assistant API 等等。目前，GLM-4 已经上线官方网站和手机 App「智谱清言」(需要更新到最新版本)。

### GLM-4

作为新一代基座大模型，GLM-4 整体性能相比 GLM3 提升 60%，支持 128k
上下文、更强的多模态，支持更快推理速度、更多并发，大大降低推理成本，同时增强了智能体能力。

### ALL Tools

只需一个指令，GLM-4 可根据用户意图自动分析指令，结合上下文选择决定调用合适的工具。可调用的工具包括 WebGLM 搜索增强、代码解释器（Code
Interpreter）、Function Call 和多模态文生图大模型（CogView3）。

### MaaS API

MaaS 平台也将全网开放 GLM-4、GLM-4V、CogView3 等模型 API，并邀请内测 GLM-4 Assistant API。

### GLMs 智能体

你可以下载（更新）智谱清言 APP，进行体验 GLMs，快速创建和分享自己的「智能体」。

    
    
    智谱官网：https://www.chatglm.cn  
    创建GLMs：https://chatglm.cn/glms  
    

  

  

  

  

  

  

  

  

  

  

  

**AI时代洞见**

  

  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
**AIGC 为广告制作模式带来了哪些改变？**  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

四位信息流广告领域的专业人士分享了在过去一年 AIGC 对广告行业带来的深刻变革，让我们看到 AIGC
在提高广告素材生成效率、加速审核流程、以及提供创意灵感等方面展现出的强大潜力。

伴随 AIGC
对广告行业的深入渗透，未来，人机协同或将成为广告创意生成的新范式。广告从业者的核心价值，不再局限于一篇文案、一张图片，而是将更加专注于战略规划、行业深耕以及与
AIGC 技术的深度融合。

    
    
    深度对话：https://mp.weixin.qq.com/s/RoJoCF_wpnaKsbbSLwieag

