---
author: 晓霖
categories: articles
date: 2023-11-09
layout: post
style: huoshui
tags:
- AI
title: AI生产力快报｜05
---

![](/assets/images/459167ac2e224c43bce5d4392ebdbe8f.gif)

编辑：晓霖

**聪明生产力**

  

**01**

  
  
  
**为什么指定角色就能提高ChatGPT的回答质量？**  
  
  

你可能会好奇，在与 ChatGPT 交互时，为什么告诉它 “你是某某领域专家”， 就可以让它给出质量更高的答案？这与 GPT 的工作原理有关。

  

ChatGPT 与人脑的工作方式不同，它并不是真正 "知道"
答案的质量高低，它的回答质量是由概率权重、训练时的优化目标以及上下文相关性决定的。它基于训练过程中学到的大量文本数据来预测下一个最有可能的单词或字符（即
Token），预测过程基于算法计算概率分布。

  

当你指定了 ChatGPT 的角色，相当于设定了专业领域上下文，ChatGPT
会激活与该领域相关的词汇和知识库，从而提高了信息检索的相关性和准确性。ChatGPT
会模仿该领域专家的回答模式，不仅在专业术语的使用上，也在逻辑推理和知识整合上力求精确。专业上下文的设定能减少语义模糊，减少模型选择不相关信息的可能性，从而降低错误回答的概率。

  

但你不能给它过高的预期设定，它只是一个具有广泛知识的工具，并不具备超人的智慧。如果你告诉它 “你智商 200”，它可能会
“误入歧途”，生成一些看似深奥实则不切实际的内容。

  

就像你教一只鹦鹉说话，虽然它能模仿你的声音，但它并不理解这些词语的真正含义。当你告诉 ChatGPT 它是专家时，你其实是在引导这只 “高级鹦鹉” 选择它
“学过” 的最好的词句来回答你。

  

  

  

  

  

  

  

  

  

  

  

**大模型动态**

  

**02**

  
  
  
**OpenAI 首届开发者大会新品一览**  
  
  

OpenAI 首届开发者大会备受关注，推出了具有 128K 上下文和更低价格的 GPT-4 Turbo、具有多模态功能的 API、新的 Assistant
API，以及用自然语言就能创建个性化 GPT 的 GPTs。

  

**GPT-4 Turbo：更强更便宜**

  

支持 128k 上下文窗口，内部和外部知识库更新到了 2023 年 4 月，每分钟的速率限制翻倍，将来还会越来越快。

  

允许同时调用多个函数，并引入 seed parameter，可以根据需要重现输出。

  

提供了一个 JSON Mode，可以保证模型以特定 JSON 方式提供回答，调用 API 时也更加方便。

  

输入方面降至 GPT-4 的 1/3 ，即 0.01 美元 / 1000token；而输出方面降至一半，即为 0.03 美元 /
1000token。总体使用降价大概 2.75 倍。

  

目前付费开发者已经可以使用 gpt-4-1106-preview，稳定版将在未来几周内发布。此外，GPT-3.5 Turbo 16k
也降价了，同样支持微调。

  

**GPT-4 Turbo：集成多模态**

  

集成 GPT-4 Turbo with vision，能够接受并处理图像输入。价格取决于输入图像的大小，例如一张像素 1080×1080 的图像需要的成本为
0.00765 美元。

  

集成 DALL・E 3，能够生成图像。有不同的格式和质量选项，生成一张图像的起价为 0.04 美元。

  

集成 TTS，将文本转化为人类质量的语音。每输入 1000 字符的起价为 0.015 美元。

  

未来还将集成其刚刚开源的语音识别模型 Whisper V3。

  

此外，系统内置了版权保护措施：版权护盾。如果用户面临有关版权侵权的法律索赔，OpenAI 将介入，为客户辩护并支付由此产生的费用。版权护盾适用于
ChatGPT Enterprise 和开发者平台的一般可用功能。

  

**Assistant API：构建更强大的 AI 应用**

  

使用 Assistants API，用户可以构建一个具有特定指令、利用外部知识并可以调用 OpenAI 生成式 AI 模型和工具来执行任务的「助手」。

  

Assistants API 提供了四项功能，帮助你构建功能更强大的 AI 应用。

  

> 长线程（persistent threads）：用户再需要处理长对话历史，只需将每条新消息添加到现有线程中。
>
>  
>
>
> 代码解释器（Code Interpreter）：在沙盒执行环境中编写和运行 Python 代码，并生成图形和图表，处理包含各种数据和格式的文件。定价
> $0.03 /session (free until 11/17/2023)。
>
>  
>
>
> 知识库检索（Retrieval）：利用模型之外的知识（如专有领域数据、产品信息或用户提供的文档）增强 assistants。定价
> $0.20/GB/assistant/day (free until 11/17/2023)。据悉，每个 Assistants 最多可附加 20
> 个文件，每个文件不超过 512MB。
>
>  
>
>
> 函数调用（Function calling）：使助理能够调用用户定义的函数，并将响应合并到消息当中。

  

OpenAI 表示，与平台的其他部分一样，传给 OpenAI API 的数据和文件绝不会用于训练他们的模型，用户随时可以删除数据。

  

现在就可以前往 Assistants playground 试用 Assistants API
测试版：https://platform.openai.com/playground?mode=assistant

  

**GPTs 与 GPT 商店**

  

借助GPTs，用户无需写代码就能创建出自定义版本的 ChatGPT。

  

现场展示了如何通过一个名为 GPT Builder 的对话式 AI 模型，使用自然语言来构建定制化的
GPT。用户只需要定制指令（Prompt）、外设的知识库、动作（action），即可创建个性化的 GPT。

  

GPTs 不但可以调用内置功能，还可以通过外部 API 来调用定制化的 action，并且允许 GPTs 集成外部数据或与现实世界交互。目前，GPTs
提供给 ChatGPT Plus 和企业用户试用。

  

OpenAI 将在本月底上线 GPT Store，开发者们可以在商店分享和发布自己创建的 GPTs。GPT
发布后，应用可以选择私有，专属企业拥有和公开所有三种方式。

  

目前 GPTs 商店已经上架 16 个 GPTs，账号已经被推送 GPTs 的用户可以去试玩了。

  

  

  

  

  

  

  

  

  

  

  

  

**AI时代洞见**

  

**03**

  
  
  
**吴恩达《面向所有人的生成式AI》全新上线**  
  
  

人工智能专家吴恩达老师推出全新课程《面向所有人的生成式AI》，面向没有编码或人工智能经验的普通人群，讲解生成式人工智能的入门知识。

  

如果你对 ChatGPT 等大语言模型（LLM）的底层原理感兴趣，非常推荐你通过这个系列课程了解 GenAI。课程将会讲解生成式 Al
的工作原理、如何在工作或业务中使用生成式 AI，以及生成式 Al 的潜在风险和如何安全使用。

  

课程分三节，一共6小时。你可以选择免费旁听，或者花 49.99 美元参加小测验、获取Coursera的结业证明。

  

课程地址：https://www.coursera.org/learn/generative-ai-for-everyone

中文字幕：https://space.bilibili.com/589397373/channel/collectiondetail?sid=1844068

  

  

  

  

  

  

  

  

  

  

  

**Reference**

https://openai.com/blog/new-models-and-developer-products-announced-at-devday

https://openai.com/blog/introducing-gpts

https://mp.weixin.qq.com/s/7uowRd_V0Ze54VBbuMmynQ

![](/assets/images/6d2628d688b44bf5b0dc266077532c6b.png)

**活水智能**
是一家致力于通过人工智能提高知识工作者的生产力的公司，作为「AI时代的生产力专家」，活水智能的核心目标是为用户提供最先进的AI技术和工具，帮助他们更高效、更智能地完成工作。