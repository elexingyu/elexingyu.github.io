---
categories: articles
date: 2023-08-24
layout: post
style: huoshui
tags:
- AI
title: AIGC每周观察[0814-0820]
---

![](/assets/images/67ec4e3341584a9ca1a6c116ec20debc.png)

## 热点回顾

#### OpenAI 官宣第一笔收购，全资收购了 Global Illumination 整个团队

OpenAI 收购了 Global Illumination (https://ill.inc/)
团队，一家利用人工智能构建创意工具、基础设施和数字体验的公司。该团队之前曾在 Instagram 和 Facebook 早期设计和构建产品，并且还在
YouTube、Google、Pixar、Riot Games 和其他知名公司做出贡献。他们的最新作品
Biomes，是一款基于网络的开源多人在线角色扮演游戏（https://github.com/ill-inc/biomes-
game‍）‍类似于我的世界，但可以用浏览器运行。这次收购的背后，有人认为 OpenAI 可能是看重了 Global Illumination
团队的产品能力，也有人猜测 OpenAI 可能是看上了这个高自由度的游戏。有业内人士猜测 OpenAI 可能正为 ChatGPT
拓展更多的图像/视频类功能，或者是为了构建 Dall-E 2 图像生成服务，又或是推出一个’文本-视频’产品。

ref. https://openai.com/blog/openai-acquires-global-illumination

**探索之问:**

1\. OpenAI 为何选择收购 Global Illumination，而不是其他 AI 初创公司？  
2\. 「我的世界」的开源版「Biomes」与 OpenAI 的未来策略有何关联？  
3\. Global Illumination 团队在 Instagram 和 Facebook 的早期阶段设计并构建了哪些产品，使其成为 OpenAI
的收购目标？

#### OpenAI 宣布将 GPT-4 引入内容审核系统，用 API 就能创建自己的 AI 辅助审核系统

OpenAI 在其最新博客中介绍了如何使用 GPT-4
进行内容策略制定和内容审核决策。这种方法使得标签更加一致，策略调整的反馈循环更快，减少了人工审核员的参与。内容审核在维持数字平台健康中起到关键作用。使用
GPT-4 的内容审核系统可以更快地对策略变更进行迭代，将周期从几个月缩短到几小时。GPT-4
还能够解读长篇的内容策略文档中的规则和细微之处，并即时适应策略更新，从而实现更一致的标签。OpenAI 相信这为数字平台的未来提供了一个更积极的愿景，即
AI 可以根据特定平台的策略帮助在线流量进行审核，减轻大量人工审核员的精神负担。任何拥有 OpenAI API 访问权限的人都可以用这种方法，创建自己的
AI 辅助审核系统。

ref. https://openai.com/blog/using-gpt-4-for-content-moderation

**探索之问:**

1\. GPT-4 如何帮助缩短内容策略变更的迭代周期？  
2\. 如何利用 GPT-4 实现更一致的内容标签？  
3\. AI 在数字平台的未来中将扮演怎样的角色？

#### 爆料称 Google 或将于秋季上线 Gemini，相当于 GPT-4 和 Midjourney/Stable Diffusion 的合体版

今年 4 月，谷歌将 Google Brain 与 DeepMind 合并。6 月，在开发者大会上公布了一系列 AI 新项目，包括首次亮相的
Gemini。近日，有媒体爆料称 Gemini 将具有类似 Midjourney/Stable Diffusion
的「文生图」能力。根据此前的报导，Gemini 一开始就以多模式、高效的工具和 API
集成为目标而创建，旨在支持未来的创新，例如内存和规划。经过微调和严格的安全测试后，Gemini 将像 PaLM 2
一样提供不同尺寸和功能的模型版本。值得注意的是，Google Brain 与 DeepMind 合并后，将类似 GPT-4 的文本处理能力与 AlphaGo
的强化学习以及 “树搜索” 方法相结合，赋予了 Gemini 巨大的潜力。

拓展阅读：《把 AI 变成你的 “人生导师”？谷歌被曝正在 “密谋” 几十项震撼更新》
https://www.8btc.com/article/6829922

#### Open LLM 榜单再次刷新，比 Llama 2 更强的「鸭嘴兽」登上榜首

为了挑战 OpenAI 的 GPT-3.5 和 GPT-4 等闭源模型，一系列的开源模型如 LLaMa、Falcon 等正在崛起，Meta AI 发布的
LLaMa-2 模型被视为开源领域的强大模型。最近，Open LLM 榜单的排行发生了变化，一个名为
Platypus（鸭嘴兽）的模型成为了新的领头羊。Platypus 是基于 LLama 2 微调的，由波士顿大学的研究者使用 PEFT、LoRA 和
Open-Platypus 数据集进行优化。Open-Platypus 数据集是一个小规模的数据集，旨在提高 LLM 的 STEM
和逻辑知识。此外，文章还详细描述了数据集的优化过程、微调与合并的方法以及 Platypus 的性能和局限性。

ref.
[https://mp.weixin.qq.com/s/OPVhwXmHUWHzGesELOtgMg](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2650887575&idx=5&sn=dca3e98e1c41fc03b65dc037016e56ad&scene=21#wechat_redirect)

**探索之问:**

1\. Platypus 模型为何能在 Open LLM 榜单中脱颖而出，超越其他竞争对手？  
2\. Open-Platypus 数据集有何独特之处，使其能够有效提高 LLM 的 STEM 和逻辑知识？  
3\. Platypus 模型在实际应用中可能遇到哪些挑战和局限性？

#### UC 伯克利发布 Vicuna v1.5，一款受欢迎的 GPT-4 本地平替

UC 伯克利近期发布了 Vicuna v1.5，这是基于 Llama 2 微调的新版本，支持 4K 和 16K 上下文，并在多数基准测试中取得了
SOTA。Vicuna 主要在 ShareGPT 收集的用户共享对话上进行了微调。自今年 4 月发布以来，Vicuna 已经成为了最受欢迎的聊天 LLM
之一，其在多模态、AI 安全和评估方面的研究都具有开创性。仅在 7 月，Vicuna 模型在 Hugging Face 上的下载量已经超过了 200 万次。

ref.
[https://mp.weixin.qq.com/s/OWPQtFaww1vAqLoQuTxI6Q](https://mp.weixin.qq.com/s?__biz=MzI3MTA0MTk1MA==&mid=2652366117&idx=3&sn=2471f919dad24bb587925167e786bfee&scene=21#wechat_redirect)

试用 Demo: https://chat.lmsys.org/?continueFlag=16ed0766e4a2ffa353c9d070a982323d

#### 字节跳动上线测试版「豆包」，一款基于云雀模型开发的 AI 聊天机器人

「豆包」是字节跳动公司基于云雀模型开发的 AI 工具，就是此前内部代号为「Grace」的 AI
项目，提供聊天机器人、写作助手以及英语学习助手等功能，可以回答各种问题并进行对话，支持网页 Web 平台 iOS 以及安卓平台，但 iOS 需要使用
TestFlight 安装。据「豆包」项目组人士消息，「豆包」是一款聊天机器人产品，还处于早期开发验证阶段，这次上架仍是小范围的邀请制测试。

ref. [https://mp.weixin.qq.com/s/MFbs-
Ss68cn-Y2K1dnvIRg](https://mp.weixin.qq.com/s?__biz=MzIzNjc1NzUzMw==&mid=2247692038&idx=1&sn=cdb8590d5e01f59005c6bf30f5698279&scene=21#wechat_redirect)

#### 小米 AI 大模型 MiLM-6B 在 GitHub 上曝光，C-Eval 总榜排名第 10

小米表示早在今年 4 月组建了自己的 Al 大模型团队，主力突破方向是轻量化本地部署。几天前，小米的 64 亿参数大模型在 GitHub 上曝光，其在
C-Eval 和 CMMLU 基准上均取得了同体量最好的性能。根据 C-Eval 给出的信息，MiLM-6B 模型在
STEM（科学、技术、工程和数学教育）全部 20
个科目中，计量师、物理、化学、生物等多个项目获得了较高的准确率。未来该模型可能会被用于小米旗下「小爱同学」等虚拟助理服务中。

ref. https://www.jiqizhixin.com/articles/2023-08-15-15

**探索之问:**

1\. 小米的大语言模型如何在手机上实现本地运行，与云端运行有何不同？  
2\. 面对激烈的科技竞争，小米如何通过技术创新确保其在市场中的领先地位？

#### 「快手 AI 对话」功能在安卓版本开放内测，一个基于自研大语言模型的应用

快手近期公布了其基于自研大语言模型的最新应用进展，即「快手 AI 对话」功能，该功能已在快手 APP 的安卓版本中开放内测。用户只需在最新版本的 APP
上点击搜索首页右上角的 AI
图标，即可进入产品首页并开始对话。此功能主要依赖于快手站内丰富多样的社区内容生态，可以帮助用户快速查找短视频、达人、百科等内容，为用户提供全新的信息获取方式。此外，「快手
AI
对话」还能打破站内内容的生态壁垒，有望为用户提供全网检索服务。与通用大模型相比，这是一个针对搜索新场景的新探索，不仅提高了回答的准确性，还满足了用户多样化的需求。此功能不仅涵盖了生活常识和服务查询等内容，用户还可以进行追问，以获得更个性化的搜索结果。据悉，这是短视频直播行业首个基于大语言模型的应用产品。

ref.
[https://mp.weixin.qq.com/s/SrtfTVMhVoPuubeOdZTpSw](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2650887911&idx=3&sn=a23e0f681d84fad6649e431ddd8c88b1&scene=21#wechat_redirect)

## 本周精选

#### Transformer 速查宝典，涵盖模型、架构、训练方法的论文

这篇 Transformer 的综述文章，涵盖了 22 个模型、11 个架构变化、7 种预训练后技术和 3 种训练技术（以及以上都不是的 5
种技术），供大家了解 Transformer 的来龙去脉及相关技术。文章按重要性和独特性的松散顺序列出了各种技术，其中 GPT-3 和 GPT-4 是
OpenAI 发布的大型语言模型，Gopher 和 AlphaCode 是 DeepMind
的大型语言模型。此外，文章还介绍了各种架构变化，如多查询注意力、稀疏注意力和混合专家等。文章还探讨了后预训练技术，如使用 PPO 的 RLHF 和
Constitutional。最后，还提到了一些训练技术和其他相关技术。  
源头：https://kipp.ly/transformer-
taxonomy/?continueFlag=a897a8d0eb16dcae5398f1b58cc5e06f中文编译：[https://mp.weixin.qq.com/s/uBv8t2hd0WS4aAqUuAyBhw](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2650887276&idx=3&sn=68a3517cadd5e42d4b48a863ed402c43&scene=21#wechat_redirect)**探索之问:**
1\. GPT-4 与 GPT-3 相比，有哪些显著的改进和特点？  
2\. 为什么 DeepMind 的 Gopher 模型在 2020 年底训练，但直到 2021 年才发布？  
3\. 在所有列出的模型和技术中，哪些被认为是未来 AI 发展的关键？

#### 谷歌：大模型不仅有涌现能力，训练时间长了还有「领悟」能力

谷歌的研究显示，当模型达到一定规模时，除了涌现现象外，还存在另一种被称为「领悟」的现象。这种现象在 2021 年被发现，当模型经过长时间的训练后，它会从仅仅
“记忆训练数据”
转变为对未见过的数据展现出强大的泛化能力。这种「领悟」现象在微型模型中被观察到，但研究者们也探讨了大型语言模型是否也会在长时间训练后突然泛化。文章通过微型模型的实验，如模加法任务和
01
序列问题，来探索模型如何从记忆转变为泛化。研究还指出，「领悟」是一个偶然的现象，与模型大小、权重衰减、数据大小和其他超参数有关。最后，文章提出了关于记忆和泛化之间的开放性问题，以及如何更好地理解大型模型的可能方法。源头：https://pair.withgoogle.com/explorables/grokking/中文：[https://mp.weixin.qq.com/s/1iWUVNpHZGcIxt9mv-
Wv1w](https://mp.weixin.qq.com/s?__biz=MzA3MzI4MjgzMw==&mid=2650887337&idx=2&sn=d56074c06587c18c6e63471ba136bfb3&scene=21#wechat_redirect)**探索之问:**
1\. 什么是模型的「领悟」现象，它与涌现现象有何不同？  
2\. 在模型训练中，为什么会出现从记忆数据模式转变为泛化数据模式的情况？  
3\. 如何更好地理解和解释大型模型的工作机制？

#### 硅谷大佬们都在追的 “e/acc”，是个什么新玩意？

近期，硅谷科技圈出现了一个新词 “e/acc”，即 “有效加速”（Effective
Accelerationism）。这是一种整合生物、物理、经济和社会理论的哲学思想，强调适应性、进化、智能和加速为宇宙中的普遍原则。其核心理念是技术创新对社会的推动和变革。这个概念起初源于英国哲学家尼克・兰德在
2018 年提出的理论，但现在更多地与人工智能技术的进步联系在一起。硅谷的许多大佬，如 A16Z 的创始人 Marc Andreessen 和 YC
孵化器的 CEO Garry Tan，都公开支持这一思潮。此外，旧金山被视为 e/acc 思潮的中心，有观点认为 e/acc 将改变旧金山，使其成为 AI
研究和创新的焦点。ref. https://www.8btc.com/article/6829264**探索之问:** 1\. “e/acc”
为何能在短时间内在硅谷引起如此大的关注？  
2\. 如何看待 “有效加速” 与人工智能技术之间的关系？  
3\. 旧金山如何通过 “e/acc” 思潮迎来其历史上的黄金时代？

## 活水创意 Flow

本期「活水创意Flow」带来的是活水社群成员冰瓜王同学关于如何用 GPT 学习理财规划的分享：

学习一个领域的技能最重要的学会这个领域的思考方法。同样，学习理财规划的最好方式也是观察理财规划师是如何思考的。GPT无疑为我们创造了一个很好的条件，它既可以扮演一名咨询者，也可以扮演理财规划师。在观察GPT如何为咨询者进行理财规划的过程中，我们可以掌握理财规划的基本思路。具体步骤如下：

1\. 让GPT扮演理财客户提供具体的财务信息 2\. 让GPT扮演理财规划师用专业的框架整理客户财务信息 3\. 让GPT补充客户还没有提供的信息 4\.
让GPT提供理财规划方案

完整对话：https://42share.com/gpt/3072926004

  

![](/assets/images/521134bb442c499bb10cb973e9b29098.png)

欢迎加入阳志平老师创办的「玩转 GPT」知识星球，了解更多前沿论文、使用技巧、原创产品，与 2100+
成员一起碰撞无限创意。还有各种有趣有料的活动等你来参与！

**👇 加入知识星球，一起玩转GPT！**

![](/assets/images/4de5381f6f3e45cd97db8b7479a3f619.jpg)