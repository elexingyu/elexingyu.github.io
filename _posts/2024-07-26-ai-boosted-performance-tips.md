---
categories: articles
date: 2024-07-26
layout: post
style: huoshui
tags:
- AI
- 教程
title: 我是如何用AI提升业绩和工作效率的分享4个技巧！
---

![](/assets/images/7e701c2ac5f447ec942e29e44c759bc6.png)  

编者按：本文分享一位开发者在运营网站时，是如何使用AI的。希望他的使用技巧对你有所启发。国外工具大家可以换成国内的。全文略有删减。以下以第一人称叙述。  

* * *

我看到过很多帖子或评论，提到AI如何帮助他们编程、学习或自动化某些工作，但在当今的技术环境下，很难分辨出哪些是真实的、哪些是夸大的。

我很好奇大家用AI来干什么，比如：节省时间、实现以前不可能完成的任务、开发网站、教学、管理知识、学习技能或爱好、几乎任何有用的事情。

因此，我决定写一篇关于我在运营Unwrangle（网址：https://www.unwrangle.com/） 时如何使用AI的文章。

## 编写代码

一开始，ChatGPT刚发布时，我会将代码粘贴进去，然后手动将其响应添加到我的代码中。

不久后我在Hacker News上发现了一个项目——将API与任何代码库一起使用，我使用了一段时间，然后转而使用Cursor。

Cursor省去了我复制粘贴GPT或其他模型修改代码的时间。它的界面设计让AI辅助编程变得更加容易，尤其适合像我这样的中级程序员。

![](/assets/images/00ee7b7eff514e73b44fae52fc0f6351.png)

Cursor可以使用多个模型，现在可以在Claude、OpenAI和众多模型中进行选择。

起初，我几乎所有请求都使用GPT-4，但自从Claude发布Opus 3后，我会把Cursor每天提供的10个免费的Opus 3请求留给更长、更复杂的任务。

我发现，Opus不会让我自己编写剩余的代码，并且错误较少。这使得它在处理需要更细致逻辑应用的任务时更具优势。

我会根据不同问题选择不同的模型。

  * • GPT-4o：处理模式匹配任务（如用户输入异常处理、正则表达式、模板代码）时表现出色。

  * • Claude Opus 3：处理复杂或不明显的情况时依然是我的首选，因为它不会偷懒。

  * • Claude Sonnet 3：构建用户界面方面表现最佳。它们的Artefacts应用在使用图像参考构建UI时比Cursor更出色。

  * • 使用Sonnet 200k或Google的Gemini进行长对话任务时非常有用，特别是处理静态文件的任务。

![](/assets/images/e03fd3709b5d4c509aeadf54acf452ad.png)

根据我提供的图像，Claude Sonnet 通过Artefacts 为我创建的目录

这是我主要使用AI的地方，我对此非常满意。

**注：** 国内可以使用豆包MarsCode，简单任务可以使用任一大模型。

## 搜索资料

第二个我经常使用AI的用途是搜索。

在此之前，我习惯在HN、Reddit、LinkedIn（公司相关）、播客等平台上搜索信息，然后再尝试Google。

现在，这些网站对我也很有帮助：

**Devv.ai：** 我使用它的Github模式来询问开源项目相关问题。这帮助我在熟悉开源库时节省了时间。

![](/assets/images/ba59a38c79d04a91b3dfe911d00101fb.png)

网址：https://devv.ai/

**Exa：** 我用这个神经搜索引擎在Github上查找库和寻找我使用的工具的替代品。  

![](/assets/images/019c25ce1da04c82bb4177ca8bbea1e9.png)

网址：https://exa.ai/

**自托管的Perplexica：** 我一直将Perplexica作为主要搜索引擎，用于技术话题相关的网页搜索，效果出奇地好。

例如，我用它询问“Cursor是否为Sonnet使用GPT-4请求配额”，得到的答案比Google或Perplexity更好，而且它是开源的！

它使用SearXNG聚合超过70个搜索服务的结果。Perplexica还可以通过Ollama和Groq与其他聊天模型提供者一起使用。

网址：https://github.com/ItzCrazyKns/Perplexica

**注：** 国内可以使用秘塔搜索、天工AI搜索，kimi、混元等大模型自带的搜索功能。

## 编写文档

我需要在不同服务器上管理很多服务，以支持我的产品Unwrangle。我在Notion上维护一个Wiki，记录所有不同技术的设置和维护说明。

AI在这方面也帮我节省了时间！

现在，每当我完成需要记录的操作时，我会将.bash_history（记录Linux CLI命令的文件）保存为一个txt文件。

然后将其上传到Google的AI Studio，让它为我写一份类似Confluence风格的说明文档，方便我以后重复操作。

编写技术文档很重要，但也耗时且枯燥。所以这是我最喜欢用AI自动化的任务！

## 写营销邮件

我的写作能力并算太差。但撰写销售文案和邮件却是另一回事。我在找到合适的用语时常常感到困难，我既不想显得高冷，也不想显得过于热情或矫情。

Claude在这方面很有帮助。我给它一些定制指令后，生成的内容质量显著提升。

之前我从未使用AI写邮件，因为我觉得生成的内容太过通用、推销感太强，让人反感。

但Claude真的很有用。我提供一些上下文、邮件初稿，有时还附上对话记录，它提供修改意见，这帮助我大大提高了销售业绩。

以上是我使用AI提高效率的方式。我对AI能所带来的各种可能性感到无比兴奋，同时也警惕炒作。

如果你读到这里，我希望这篇文章对你有所帮助。你可以在这里联系作者：raunaq@unwrangle.com。

注：国内可以使用kimi，在中文写作上效果不错。

  

如果你也好奇人们在不同领域是如何使用AI自动化工作的，请投稿给我们！

  

## 推荐阅读

[分析了TED上AI相关的550个视频，我得出了这些结论…](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247486528&idx=1&sn=501b5c2c5cc34bf6636997962f42f872&chksm=c3546ed3f423e7c5a634e67aea3e6e2eeff94d2ef9a9c026f64ce7fd0ba56be76899c22cb9f9&scene=21#wechat_redirect)  

[Triplex：用于创建知识图谱的开源模型，成本比GPT-4o低10倍！](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247486546&idx=1&sn=98139129e78b457e2f1885495f3c58b3&chksm=c3546ec1f423e7d7df329e883ab39c79eaf61e6bc38cc801a318c7f95a229a670b161ca445af&scene=21#wechat_redirect)  

[使用AI大模型的正确姿势！接入知识库、微调，5种方法，总有一种适合你](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247486313&idx=1&sn=d08f61ed0c59596515a257a5ed5bcf2b&chksm=c35469faf423e0ec2e6f328ae5209ff5a7047455fadf3166de9bdf6e563babe6663b03ca6b4c&scene=21#wechat_redirect)