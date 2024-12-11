---
author: 晓霖
categories: articles
date: 2023-11-23
layout: post
style: huoshui
tags:
- AI
title: AI生产力快报｜07
---

![](/assets/images/8c274b9537b346fabf1660f9df883357.gif)

​编辑：晓霖

**聪明生产力**

  

  
  
  
**Langchain：一个学习和开发AI应用的工具选择**  
  
  

Langchain 是一个为大语言模型应用开发而设计的开源库，旨在简化开发者在软件开发中对 GPT
等大型语言模型的集成和使用。其设计哲学是模块化和灵活性，允许开发者根据特定需求，灵活地集成和替换不同的语言模型和组件。Langchain
支持多种大语言模型，且特别强调易用性，提供了一套直观的接口，方便不太熟悉深度学习或自然语言处理的开发者快速调用，这对于快速原型设计和迭代尤其重要。

  

在 OpenAI 开发者大会之后，LangChain 立即开源了 OpenGPTs，提供与 OpenAI GPTs 类似体验。OpenGPTs 在
LangChain、LangServe 和 LangSmith 的基础上开发，提供 60+ 种 LLM 选择，以及 100+
个工具选择。除此之外，你还可调用自己编写的工具。与直接使用 OpenAI 的 GPTs 相比，OpenGPTs 具有更高的可定制性。

（详见 _https://github.com/langchain-ai/opengpts_ ）

  

如果你关注提示词管理，他们最近推出的 LangChain Hub 是一个集浏览社区提示和管理个人提示于一体的平台。Langchain Blog
还撰文分析了自该平台上线以来，提示工程领域的几个主要趋势，还分享了不少精彩案例。如果你想深入学习大模型相关技术和开发知识，不要错过他们的 Blog。

  

**官方文档：** _https://python.langchain.com/docs/get_started/introduction_

**博客文章：** _https://blog.langchain.dev/the-prompt-landscape/_

  

  

  

  

  

  

  

  

  

  

  

  

**大模型动态**

  

  
  
  
**Github：Octoverse 2023 开源报告**  
  
  

随着2023年 Github 上生成式人工智能项目总数同比增长 248%，「生成式 AI 技术」成为 Octoverse 2023
的关键词。今年报告主题为「AI、云和 Git
的开源活动如何改变开发者体验」，针对软件开发领域提出了三大趋势：开发者正在大量使用生成式人工智能、开发者正在大规模运行云原生应用程序、2023
年的首次开源贡献者人数最多。除此之外，报告还统计和预测了各地开发者社区情况，以及 Github 上最流行的编程语言趋势。

  

正如 Git 已成为开发者体验的基础，GitHub 上有越来越多数据表明，不管是开发者使用的编码工具，还是他们开发的项目，AI 已逐步成为主流。过去一年，有
92% 的开发者使用过基于 AI 的编码工具来处理工作或工作以外的任务。与此同时，生成式 AI 在开源和公共项目中发展迅猛，langchain 和
stable-diffusion-webui 等基于生成式 AI 的开源软件项目是 2023 年 GitHub
上贡献者数量最多的项目。越来越多开发者正在利用预训练好的 AI 模型构建 LLM 应用程序，根据用户需求定 AI 应用程序。

  

如果你也想在编程的世界体验 AI 编码工具，这些近期比较热门的 AI 编码工具可供参考：

  

**GitHub：GitHub Copilot**

> 内嵌基于 GPT-4 的聊天窗口，聊天功能支持与代码进行自然语言交互。
>
> 可以识别代码和报错信息、分析代码用途、生成单元测试、提出 debug 建议。
>
> 集成在 VS Code 和 Visual Studio。

**Meta：Code Llama**

> 基础模型是 Code Llama，专注于生成和讨论代码。
>
> 支持最高 10 万 token 上下文。
>
> 开源，对研究和商业使用免费。****

**DeepSeek AI：DeepSeek Coder**

> 在 2T 令牌上用 87% 代码和 13% 中英文自然语言重头训练，对代码的语义和结构有较好理解。
>
> 可选择从 1B 到 33B 多种尺寸的模型。
>
> 支持自动化编程、代码补全、代码翻译等功能。

**智谱 AI：CodeGeeX**

> 基于 ChatGLM2-6B 基座语言模型。
>
> 支持代码生成 / 补全、注释生成、代码翻译等功能。
>
> 提供 VS Code, Jetbrains 插件。
>
> 开源，可公开用于研究目的，商用需填写登记表。

  

  

  

  

  

  

  

  

  

  

  

  
  
  
**天气预测大模型 GraphCas：表现优于现有天气预报系统**  
  
  

谷歌 DeepMind 实验室发布的天气预测大模型 GraphCas，具有 0.25 度经度 / 纬度的高分辨率，相当于把地球表面分割成超过 100
万个网格，产生总计上亿条预测数据。在 1380 个准确度测试指标中，有 90% 的预测结果优于目前最准确的天气预测系统
HRES。如果把预测范围限制在对流层，这个比例将高达 99.7%。不仅如此，在 Google TPU v4 机器上，GraphCast
只需不到一分钟就可以完成 10 天的预测，远快于 HRES 等传统方法。今年 9 月，GraphCast 提前 9 天预测了北大西洋的飓风
Lee，比使用传统预测系统提前 3 天。

  

与传统预测方式不同，GraphCast 依靠寻找数据中的规律进行预测，而不是使用人类建立的物理方程。通过输入此前 6 小时的气象数据，GraphCast
可以预测未来 6 小时的天气，并可将预测结果作为新的「当前」状态，继续迭代预测。

  

目前该模型已经开源，相关论文 _Learning skillful medium-range global weather forecasting_
已发布在 Science 上。接下来，除了提高天气预报的准确度，DeepMind
希望通过开发新工具和加速研究，进一步了解气候的更广泛模式，提高全球应对环境挑战的能力。

  

**开源模型：** _https://github.com/google-deepmind/graphcast_

**Science 论文：** _https://www.science.org/doi/10.1126/science.adi2336_

  

  

  

  

  

  

  

  

  

  

  

  

  

**AI时代洞见**

  

  
  
OpenAI 首席科学家 **OpenAI 首席科学家 Ilya Sutskever 深度访谈**  
  
  

OpenAI 首席科学家 Ilya Sutskever 在最近一次访谈中，分享了 OpenAI
的目标与战术演变，以及对人工智能未来的展望。这些见解折射出一位顶尖科学家的深邃思考。

  

OpenAI 自成立之初，目标就是「通用人工智能 ——
能够胜任人类大部分工作、活动和任务的人工智能，并确保这些进步造福全人类」。尽管随着时间的流逝，他们的战术有所演变，但这一终极目标始终未变。OpenAI
结合「自上而下的想法」与「自下而上的探索」，用好的想法指导实践，再通过实践来验证和调整这些想法。这样的实践表明，模型的可靠性在不断提升，即当面对的新问题难度不超过之前成功解决过的问题时，模型能够持续成功。

  

Ilya 坦言，随着对大型神经网络，尤其是 Transformer 模型的研究深入，人们逐渐意识到其在文本预测方面的惊人潜力。当从 GPT-2 向
GPT-3
过渡时，他感受到模型功能和能力的显著提升，这种跃升让他深感震撼。更加让他惊讶的是，在与这些模型交互时，他能感觉到被理解，这无疑是对人工智能领域的重要肯定。

  

7B、13B
等规模的模型研究并非浪费，更大的模型确实往往比小模型更优秀，但在实际应用中，大模型的成本并不在所有情景下都合理。对于是否应该开源那些能够完成复杂任务的大型模型，Ilya
认为这会带来难以预测的后果，尤其是当模型具备自主进行科学研究甚至构建、交付大型科学项目的能力时，是否开源的问题变得更加复杂。

  

在人工智能越来越接近生物智能的今天，我们从什么时候开始可以将这些系统视为数字生命？Ilya
认为，当这些系统变得可靠且高度自治时，这样的时刻就会到来。他还预测，未来我们将拥有比人类更聪明的计算机和数据中心，这种 "更聪明"
并不仅仅是记忆力或知识量的堆砌，而是对研究主题有更深入的理解，意味着学习速度更快。

  

**访谈视频：** _https://youtu.be/Ft0gTO2K85A_

**中文字幕视频：** _https://www.bilibili.com/video/BV1Kz4y1K7zR_

**中文全文：** _https://mp.weixin.qq.com/s/7uowRd_V0Ze54VBbuMmynQ_

  

  

  

  

  

  

  

  

  

  

  

  

**Reference**

https://github.com/langchain-ai/opengpts

https://github.blog/2023-11-08-the-state-of-open-source-and-ai/

https://deepmind.google/discover/blog/graphcast-ai-model-for-faster-and-more-
accurate-global-weather-forecasting/