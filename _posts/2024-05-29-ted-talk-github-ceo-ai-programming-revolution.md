---
categories: articles
date: 2024-05-29
layout: post
style: huoshui
tags:
- AI
- 教程
title: TED最新演讲｜GithubCEO：AI让编程变得像聊天一样自然，人人都可
---

![](/assets/images/1191ff73b81747518025722d33155f2e.png)

作者：Thomas Dohmke

编译：活水智能

来源：TED

**编者按**

 _如今，编程不再是专业开发者的专利，而是像搭建乐高积木一样简单和有趣。AI的进步正让这一切成为现实。_

 _GitHub CEO 托马斯·多姆克（Thomas
Dohmke）最近在TED进行了演讲，他展示了如何借助AI助手Copilot，用自然语言指挥AI完成开发应用、设计游戏和创建网站。而这无需复杂的编程知识。_

_这意味着未来，编程将成为每个人都能掌握的技能。例如，我们发起的「活水AI黑客马拉松」，有很多编程新手在AI的协助下，42天内开发出了产品。借助AI，你可以像写作一样，直接把创意变成产品。_

 _本文你将了解AI如何彻底改变我们与技术互动的方式，并引领我们进入一个人人皆可编程的新时代。让我们一同探索这场技术革命带来的无限可能。_

_TED演讲视频见：https://www.ted.com/talks/thomas_dohmke_with_ai_anyone_can_be_a_coder_now/transcript_

  

以下是演讲全文文字版：

* * *

我是一个成年了还爱玩乐高的人。我从小在80年代的柏林长大，那时就喜欢乐高，现在依然如此。

现在，每个星期六的下午，我会和我的孩子们一起搭乐高。我对乐高的热爱一直保持不变的原因很简单：乐高是一种几乎没有门槛的创造力实现系统。

除了是个乐高迷，我还是GitHub的CEO。如果你不熟悉GitHub，可以把它想象成编码的家园。

这是所有软件开发者，社会上的顶尖技术达人们，共同协作的平台。我们的使命之一就是让每个开发者都能轻松地用代码实现大小创意。

然而，与乐高不同的是，软件开发的过程对于大多数人来说显得望而生畏。直到2022年末ChatGPT出现，一切才开始改变。

## 1

现在我们生活在一个智能机器能理解我们，我们也能理解它们的世界。而这一切都因为语言，这将永远改变我们创造软件的方式。

在此之前，要创建软件，你必须是一个专业的软件开发者，必须理解、掌握并解释一种高度复杂，有时甚至毫无逻辑的机器语言——代码。现代代码对大多数人来说仍然像象形文字一样。

这里有个例子，这是20世纪40年代初世界上第一个计算机编程语言，叫做Plankalkül。它为我们今天使用的现代代码奠定了基础。如你所见，这些只是一些数字、一些气泡和一些大括号。这里几乎没有人类的痕迹，对吧？

时间快进约20年，我们看到了编程语言COBOL的诞生。

COBOL诞生于艾森豪威尔时代，但至今仍是许多大型金融机构的重要语言。华尔街、你的储蓄账户、你的信用卡，今天都在使用它。我们在这里看到了一些熟悉的词汇，但从结构上看，我觉得大多数人还是看不懂。

![](/assets/images/87bd7b9f0a6f472ab51a7eeb8975b61d.png)

再快进30年，到1991年，Python诞生了，这是AI时代最受欢迎的编程语言之一。80年间，我们从气泡到括号，再到一些英语词汇，但仍未达到人类语言的直观性。

直到2020年6月，我们获得了OpenAI的大型语言模型——GPT-3的早期访问权限。当时是COVID封锁期，我记得我们在视频通话中，向这个模型输入了随机的编程练习，结果它在第一次尝试中就解决了93%的问题。

我们在GitHub意识到我们手中握有非凡的东西，于是迅速推出了一种新型开发者工具——GitHub Copilot：一个为软件开发者预测和完成代码的AI助手。

Copilot现在是全球最受欢迎的AI开发者工具，编程的时代重生了。

但这一突破的可能性不仅限于商业成果。因为支撑ChatGPT和Copilot的大型语言模型是基于大量的人类信息训练的，它们几乎能理解并解释每一种主要的人类语言。

它们似乎明白我们在说什么。我们在人类语言和机器语言之间找到了新的融合。有了Copilot，任何人现在都可以用任何人类语言，通过一个简单的书面提示来构建软件。

再见了，气泡和大括号。这是自软件开发诞生以来最深远的技术突破。今天，在GitHub上有超过1亿开发者，约占全球人口的1%。我认为这个数字将会爆炸式增长。

让我在我的MacBook上给你展示一下原因。

2

我们从原始的Copilot开始，或者说OG Copilot，它实际上只是预测和完成编辑器中的代码。

你可以把编辑器想象成开发者的Google Docs。当你打开一个文档时，你知道，那种空白页的感觉，我到底想做什么呢？

我提到了乐高，所以让我们在网页上构建一个3D乐高积木。开发者的做法是开始打字。我在JavaScript文件中输入“创建一个创建乐高积木的函数”。

你可以看到这里的灰色文本，我们称之为“幽灵文本”。这是来自大型语言模型的建议。现在我只需按Tab键和Enter键。

![](/assets/images/f45d7bc2fa3b49758d350c7640cdfb8d.png)

我得到另一个建议，创建一个乐高塔。也许我们稍后再做这个。或者我可以输入“绘制乐高积木的函数”。这里你再次看到来自Copilot的幽灵文本。如果我喜欢这里看到的内容，我可以接受它。

开发者喜欢这个功能，因为他们不用自己写十行代码或从网上复制粘贴，可以直接在编辑器中完成，保持工作流畅。然而，原始的Copilot没有提供互动的方式。我不能问问题，不能指示它做不同的事情。

去年我们推出了一个新功能，Copilot聊天，你可以把它看作是编辑器中的ChatGPT。我可以在侧边栏打开它，现在我可以告诉它为我创建一个包含3D乐高积木的完整网页。

和ChatGPT类似，它会流式生成响应，不仅提供一些代码，还会给出解释。它开始写代码，你可以看到注释解释代码的作用。

它使用了一个叫Three.js的开源库。你可以看到这种方法赋予了开发者和学习开发的人力量。最后，它还会给出另一个解释。我可以检查代码，然后按下按钮将其复制到我的文件中。

![](/assets/images/5308b8a749194096b7c93cf206425580.png)

但是我想给你们展示一些别的东西。你们可能已经看到这个小麦克风图标了。我可以用它来对Copilot讲话。我想用德语问它编辑器左侧的代码是做什么的。

（德语）你能解释一下这段代码是做什么的吗？

现在Copilot再次回应我，并且用德语回答。它大意是：“当然可以，这段JavaScript代码定义了一个名为‘drawLEGOBrick’的函数。”

这样你就明白了，一个在柏林、孟买或里约热内卢的六岁孩子，现在可以在没有父母或技术背景的情况下探索编程。我的意思是，你知道的。

但你也看到，仍然需要弄清楚如何把这一切整合在一起，对吧？这里有很多技术内容。

我有代码，需要在我的机器上迭代，还要搞清楚如何部署到云端以便和朋友分享。

3  

但现在我的乐高积木已经准备好了。

你可以看到，如果我完成了所有这些步骤，现在它是一个旋转的积木。我可以用鼠标旋转它。这里有反钉、正钉，还有不错的光效。我甚至可以放大和缩小查看它。

![](/assets/images/682ab19e457e4b35a1011ce6da6d7231.png)

现在我不想再做这些开发者的事情了，我只想直接将我的创意变为现实。所以，我将在舞台上首次展示我们称之为Copilot
Workspace的新产品。它正是为此而生。这里是我的工作空间，你可以看到已经没有编辑器了。

我只看到一个任务框，我可以在里面输入任务。现在我有了乐高积木，我想把它扩展成一个乐高房子。堆叠积木形成一个乐高房子。我可以用德语或其他语言来做，但现在我们用英语。

我保存了任务。然后，Copilot Workspace会分析我已有的内容，并向我描述它的建议。基本上，它把我的请求重新组织成一个计划或规范。

你可以看到这里全部是自然语言的描述，没有代码。这些描述是英文的。然后我可以编辑这些内容，如果觉得计划不完全符合我的预期，还可以添加新的条目。

我可以更进一步生成一个计划，一个代理会遍历我已有的所有文件，确定需要如何修改这些文件，或者是否需要向我的代码库添加文件。

所以它想添加一个“createLEGOHouse”函数，并在之后调用这个函数。看起来不错，让我们实现它吧。现在Copilot使用我的任务、规范和计划为我编写代码。

你可以看到两个文件在排队，public/legoBrick.js文件，砰，代码已经为我写好了，对吧？我不需要碰代码，甚至不需要知道代码是什么。现在我看到它导入了一些新内容，并写了很多实现这些更改的代码。

你想看看结果吗？我们有没有得到一个乐高房子？这里有一个按钮可以打开实时预览，我可以点击它。现在积木从天而降，我有了一个乐高房子。你知道的，这不是一张图片。

是的，谢谢。这一切都是实时的，这是代码的力量，这是用自然语言将我的创意转化为现实的力量。

最后一件事。谢谢你，Copilot，我们总是要对AI友好。（笑）

  

4  

你刚刚看到的是三年内的三次飞跃。

这三次飞跃对计算机编程的可及性带来的进步，比过去100年都要多。记得我说过世界上有百分之一的人是开发者吗？现在你可以看到这将如何改变。Copilot
Workspace可能现在还是一个开发者工具，但很快这些开发者工具会变得普及。

因为，未来，每个人无论说什么语言，都将具备与机器对话的能力。任何人类语言现在都是开始编程的唯一技能。这将引发一场全球化的软件开发者浪潮，并重塑全球经济的地理版图。

因此，我认为到2030年，甚至可能更早，GitHub上将有超过十亿的软件开发者。想象一下：全球10%的人口不仅能够控制计算机，还能够像骑自行车一样轻松地创建软件。这将带来一场人类创造力的新文艺复兴。

![](/assets/images/75b7152ea5524a5fb5755ad9addf23aa.png)

现在，在场的每一个人都可能立即产生一个绝妙的想法：一个网站、一个应用程序、一个酷炫的电脑游戏、一首惊人的歌曲，甚至可能是某种疾病的治疗方法。

举个例子，去年，我花了几周时间开发了一款应用，可以追踪我一生中所有的飞行记录。

我知道你们在想什么：这家伙真是个极客，对吧？是的，没错，我喜欢构建这样的东西。借助AI，现在我可以用英语或德语，在喝完一杯酒之前完成这些事情。不久后，这对在场的每个人来说都将成为现实。

极客的大门已经敞开。（笑声）

5

这并不意味着每个人都会成为专业的软件开发者，甚至也不意味着他们应该成为。专业软件开发者这个职业不会消失。世界上总会需要那些设计和维护最大型软件系统的人。

我们每天都在为越来越复杂的系统添加数百万行代码，并且我们几乎跟不上维护现有系统的速度。像世界上的任何基础设施一样，我们需要真正的专家来保护和更新它。

这里的重点不是“会”还是“应该”。而是任何人都可以做到。因为我们拥有的最强大的系统——任何一种人类语言，现在已经与机器语言融合。很快，构建软件将变得像堆叠乐高一样简单和愉快。

非常感谢。

### 问答环节

Bilawal
Sidhu：哇，我得说，十亿开发者让GitHub听起来更像是YouTube和TikTok，而不是今天的模样，太令人兴奋了。我得问你一个问题，也许是最关键的问题。精彩的演讲。你说开发者仍然掌控全局。

你还说：“我们在三年内实现了三次飞跃。”稍微快进一点，你认为未来人类还需要参与其中吗？还是这些AI系统将能够自主构建和维护软件？

Thomas
Dohmke：你知道，我一直以来的观点是，我们称它为Copilot是有原因的。我们需要一个飞行员。我们需要一个能够创造性地决定要做什么的飞行员。就像乐高套装一样。

你需要把这个大问题拆解成更小的问题，拆解成小的构建块。为此，你需要一个系统思考者。

你需要一个能够搞清楚自己是在构建一个销售点系统，还是一个iPhone应用程序，还是一个酷炫的电脑游戏，还是下一个Facebook的人。

这些是非常不同的系统。现在这些构建块将会越来越大。今天是几行代码，也许是一个完整的文件，将来可能是一个完整的子系统。

所以我的工作量会减少。但我仍然在掌控整个系统。正如我提到的，我们仍在运行60年代的COBOL系统。因此我们还有很多工作要做。

BS：完全同意。所以我们将在更高层次上协调这些系统。

感谢Thomas Dohmke。

  


## 推荐阅读*

  • [50+开源仓库！让你在本地轻松运行大模型](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247485623&idx=1&sn=e251c4efd77db66913df6a8ae6b09f55&chksm=c3546a24f423e332f05097850ffe7bb67b5fb1c2d2a7e7dcf2f7e89428970d67fe80fe092a7b&scene=21#wechat_redirect)

  • [最全盘点：人类历史上所有文本数据总量](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247485448&idx=1&sn=149c4683bd8d1d2f75b444b900503823&chksm=c3546a9bf423e38dcb031eabe5d3f9002714ac13eb29d741b47d3aecde4ae3a0a88a9ce8232e&scene=21#wechat_redirect)

  • [八款产品首次亮相！总有一款适合你](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247484890&idx=1&sn=d5b5c9e561ecc4b291b8bfb69dbfb02c&chksm=c3546749f423ee5ff1018e11939c2361a5f4ab0e7b1f3bc9789db9a11a2661d381c55367eddb&scene=21#wechat_redirect)