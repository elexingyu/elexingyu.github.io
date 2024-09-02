---
layout: post
title: "AI生产力快报｜14"
date: 2024-01-11
tags: ['AI']
style: huoshui
---


![](/assets/images/5805a0c8490945d2b9ba9f8642a68c3d.gif)

编辑：晓霖

供稿：郑嘻嘻

**聪明生产力**

  

  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
**OpenAI如何设置GPTs指令**  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

还记得第一次制作 GPTs 时，帮你构建 GPT 的小助手「GPT Builder」吗？这个小助手本身也是一个 GPTs，没想到吧！

### GPT Builder

GPT Builder 配备了特定的指令和功能，能够直接编写和修改正在构建的 GPT 模型。最近，OpenAI 公开了 GPT Builder
的构建过程，以及具体的提示词。以此为示例，我们可以看到 OpenAI 如何使用 Prompt 创建功能强大的 GPT 模型。

    
    
    原文：https://help.openai.com/en/articles/8770868-gpt-builder  
    翻译：https://baoyu.io/translations/openai/gpt-builder

你发现了吗？当你在引导一个 GPT 制作新的 GPT 时，Prompt 的复杂度急剧上升，你要处理的是 GPT 和它所制作的 GPT
Builder，以及分别与它们对话的用户之间的关系。

### 指令构成

OpenAI 将这个 Prompt 分为「基本背景」和「操作步骤」两大部分，最终这两个部分都会整合到配置页面的「Instruction」中。

在「基本背景」部分，他们赋予 GPT 一个擅长创造和改进 GPT 的专家身份，然后指定了任务背景和操作原则。每一点都短小精悍、环环相扣，逻辑极其清晰。

在「操作步骤」部分，他们重新赋予 GPT 一个新的身份 —— 专门用于开发新的 GPT 模型的迭代式原型实验场（iterative prototype
playground），然后依次列出所需执行步骤，并在最后说明了一些操作过程中的注意事项。

### 指令迭代

这个 Prompt 穿插着许多「Don't」和「IF」指令，相信这些指令不仅来自于他们对 GPT
的了解，更来自于实际的测试和调试，在不断迭代中产生。作者在文中提到，这是 2023 年 1 月 3 日的 Prompt，意味着未来还会迭代更新的
Prompt。

正如他们为 GPT 设定的第二个身份时所用的「迭代」一词，这个 Prompt 是为「迭代新的 GPT」而生。也就是说，OpenAI 在迭代一个为迭代新的
GPT 而生的 Prompt。是的，这个 Prompt 里充满了这种嵌套关系。

### GPTs商店

GPT Store 已正式上线！如果你打算上架自己的 GPTs，需要提前做好以下准备：

  * • 查看使用政策和品牌指南

  * • 验证你的构建者配置文件

  * • 将 GPTs 设定为 Public（公开）

如果你还没想好要打造什么样的 GPTs，可以到 42master.io 寻找灵感，42 位 GPT 大师当中总有一款对你有所启发。

目前，GPTs 已在移动客户端支持使用语音对话，你可以随时去 42master.io 找哲学大师或心理学大师聊天。

    
    
    活水大师：https://42master.io

  

  

  

  

  

  

  

  

  

  

  

**大模型动态**

  

  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
**LangChain推出首个稳定版本**  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

Langchain 是一个为开发大语言模型应用而设计的开源库，允许开发者根据特定需求灵活地集成和替换不同的语言模型和组件。Langchain
支持多种大语言模型，提供了一套直观的接口，方便不太熟悉深度学习或自然语言处理的开发者快速调用，这对于快速原型设计和迭代尤其重要。

经过一年的迭代，官方推出了第一个稳定版本 LangChain
v0.1.0，提升集成的稳健性、稳定性、可扩展性以及一般开发者的体验。此外，新版本还提供了能够将语言智能体构建为图的
LangGraph，允许用户创建更多的自定义循环行为，目前支持 OpenGPTs。

    
    
    官网博客：https://blog.langchain.dev/langchain-v0-1-0  
    功能介绍：https://www.youtube.com/playlist?list=PLfaIDFEXuae0gBSJ9T0w7cu7iJZbH3T31

  

  

  

  

  

  

  

  

  

  

  

  

  

  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
**GitHub Copilot Chat对所有订阅用户开放**  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

GitHub Copilot Chat 是一个聊天界面，可让你用自然语言与 GitHub Copilot 交互，直接在受支持的 IDE
中询问编码相关问题并接收答案。借助它，你可以用自然语言完成各种编码相关任务，例如提供代码建议、解释代码片段的功能和用途、为代码生成单元测试，以及为代码中的
bug 建议修复。

GitHub Copilot 的订阅用户均可以在 Visual Studio Code 和 Visual Studio 中使用。JetBrains IDE
中的 GitHub Copilot Chat 目前为 beta 版，可能会有变动。

GitHub Copilot Chat
聊天界面提供了对编码信息和支持的访问，或许可以帮你节省一些浏览文档或搜索在线论坛的时间。但如果你在使用一些较新的工具或库，建议你以阅读官方文档为主，避免
GitHub Copilot 因训练资料未及时更新，提供了错误的编码信息。

    
    
    官方介绍：https://docs.github.com/zh/copilot/github-copilot-chat

  

  

  

  

  

  

  

  

  

  

  

**AI时代洞见**

  

  

  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
**处理 AI 时人们容易陷入的思维陷阱**  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  

FJ 是一位有着四年经验的机器学习工程师，曾在 AI 创业公司、FAANG 和财富 100 强公司任职。在与客户的互动中，他发现许多关于 AI
工作方式及其解读的错误和不良观点，于是撰写博客文章 _The AI Operator’s Handbook_ ，总结了一些在处理 AI
时人们容易陷入的思维陷阱。

    
    
    原文：https://medium.com/unintended-purposes/the-ai-operators-handbook-0fa3f4d387f8  
    翻译：https://baoyu.io/translations/ai/the-ai-operators-handbook

他的另一篇博客文章 _The future of Humans: Operators of AI_ 阐述了为什么劳动者要迅速转型成为 AI
操作员，以适应劳动力市场的变化。他认为关于 AI 系统的基本认识能帮助人们避免在使用 AI 时犯下代价高昂甚至危险的错误。

    
    
    原文：https://medium.com/unintended-purposes/the-future-of-humans-operators-of-ai-244359017575

