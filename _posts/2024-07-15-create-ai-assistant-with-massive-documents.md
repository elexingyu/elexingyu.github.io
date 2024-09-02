---
layout: post
title: "教程｜用大量文档创建AI助理，可用于快速提取关键信息，学习名人思想等"
date: 2024-07-15
tags: ['AI', '教程']
style: huoshui
---

![](/assets/images/9ecf21218b2149ef84b26a20588fcb07.png)  

随着AI大模型发展，从大量、结构复杂的文档中提取关键信息，编排工作流的需求变多。

比如上传某个领域知识，通过AI对话，找到关键信息；上传某个作者的所有书籍/演讲，学习其思想。

目前有很多工具（如下图），还有Coze。

![](/assets/images/af6e0a8231354c55a6026baa7982967f.png)

今天介绍一款关注度较高的开源工具——RAGFlow。

RAGFlow是一款基于深度文档理解技术的开源RAG（检索增强生成）引擎，能快速、准确地从各种复杂文档中提取信息，生成高质量的答案。广泛适用于企业和个人。

![](/assets/images/21b1ced2212c46cd8af9fae42bb00e43.png)

图 从文档中检索信息，返回引文

最近一个月，RAGFlow新增了从Docx文件中提取图片和表格、流程编排可视化等功能，功能变得更加强大了。

## RAGFlow 能做什么

### 轻松处理复杂文档

告别手动查找和整理！RAGFlow支持Word 文档、PPT、excel 表格、txt
文件、图片、PDF、影印件、复印件、结构化数据、网页等各种格式的文档。

可以自动识别并提取图片、表格等内容，让信息获取变得前所未有的简单。

### 提供精准答案

当你有问题需要解答时，RAGFlow能快速从相关文档中找到答案，并标明信息来源。

这样，你就可以轻松验证答案的准确性和可靠性，不必担心回答虚假信息了。

### 工作流编排

无论是企业内部知识管理、法律文档解析，还是学术研究资料整理，RAGFlow都能应对自如。

它的多模板分块功能可以适应不同的业务需求，灵活性极高。还提供易用的API，可以轻松集成到各类企业系统。

## 如何使用 RAGFlow

有两种方法，一种是自行部署使用，可以根据需求二次开发。这种方法适合有技术基础的同学。

这种方法的前提条件是要求：

  * • CPU：≥4核

  * • 内存：≥16GB

  * • 硬盘：≥50GB

  * • Docker：≥24.0.0 & Docker Compose：≥v2.26.1

具体操作见：https://github.com/infiniflow/ragflow

另外一种是使用官网，上手简单，适合没有技术基础的同学。

下面重点介绍这种使用。

## 操作流程

我们以硅谷创业教父保罗·格雷厄姆（Paul Graham）的为例。保罗是硅谷最具影响力的企业家、创业思想家和投资人之一。他的思想影响了无数年轻人。

假如你想学习他的思维方式，遇到问题想问问他，现在你可以使用 RAGFlow 打造一个保罗分身。

![](/assets/images/203769cdb949430fbac03da8c4c888be.png)

### 准备数据

首先，下载他博客上的所有文章。

![](/assets/images/188e171922f94ea6b29fc0b5e87c31e2.png)

### 数据解析

打开RAGFlow官网并登录：https://ragflow.io/

可以看到，页面上方有四个模块，点击相应模块，即可切换。

![](/assets/images/1386118094dc44cb90eaca9fa0ce47ca.png)

上传数据。支持上传各种格式（见上文）、多个文档。

数据上传后，等待数据解析。根据上传的数据量，解析时间有所不同。下面是我解析好的数据。

![](/assets/images/bf653698a6bd46cc88533a979bc9776d.png)

如果你想更新数据，可以选择左边的“配置”上传数据。

### 新建助理

现在建立一个保罗分身。点击新建助理，配置助理名字、设置开场白、选择知识库。

![](/assets/images/8085db6d276e4cb7b6bc1a2855488b7e.png)

在“提示引擎”处配置系统提示词，让其用保罗的思维方式、语气回答问题，只能从知识库中检索数据回答问题。

![](/assets/images/f9997dc2ccd54c87a20d09054c3a44f8.png)

这样保罗的分身就建好了。

### 测试效果

输入问题，测试效果。

下图问了保罗分身如何保持独立思考，回家效果只能说能看。

![](/assets/images/20e3fa722dcb4085a5a21899af2bb6ec.png)

如果测试效果不好，按下图更改数值。如提高“相似度阈值”，那么检索出的文本相似度会提高。

### API集成

可以生成API，集成到各类企业系统。比如对接到飞书、企业微信中。

![](/assets/images/f7372aa29c794d2389ed8a6d6036975a.png)

### 复杂流程编排

可以选择“图”进行复杂工作流编排。可根据需要，集成外部浏览器等。

比如，我可以集成保罗的博客官网，以便从博客官网搜索信息。

![](/assets/images/165c61a135154234a38c5c248a07c37a.png)

  

需要注意的是，RAGFlow官网提供默认模型只有一个deepseek-chat。如果想要更多功能，需要自行部署配置。

如果你想要学习更实用、更底层的操作，可以关注我们的[AI线下工作坊](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247484956&idx=1&sn=da84741808848eafafb9d4d97f47641e&chksm=c354648ff423ed992bb4995172650da7186a7e04f6f7d5442faa28911f15d0f001df2ece8d9a&scene=21#wechat_redirect)，【入群】享受报名优惠。  

  



  

## 推荐阅读

[5种](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247486313&idx=1&sn=d08f61ed0c59596515a257a5ed5bcf2b&chksm=c35469faf423e0ec2e6f328ae5209ff5a7047455fadf3166de9bdf6e563babe6663b03ca6b4c&scene=21#wechat_redirect)[使用AI大模型的正确姿势！接入知识库、微调，总有一种适合你](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247486313&idx=1&sn=d08f61ed0c59596515a257a5ed5bcf2b&chksm=c35469faf423e0ec2e6f328ae5209ff5a7047455fadf3166de9bdf6e563babe6663b03ca6b4c&scene=21#wechat_redirect)

[解读 Graph RAG：从大规模文档中发现规律，找到相互关系，速度更快，信息更全面！](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247486198&idx=1&sn=fe870f73635f7e97d576fb81c20befe2&chksm=c3546865f423e173293ec3697258a848a7dff22690a4b9cad0a91abdce7745760d98c5b16281&scene=21#wechat_redirect)  

[最具代表性的文本数据集：覆盖32个领域，444个数据集，774.5TB数据量](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247486148&idx=1&sn=6cf9d475da4efa7521cb08f2835b8ad8&chksm=c3546857f423e141806236ba0a96fdc5e5bd16c5ca735361a9f50dbffec57fbdc4a521f7c1b4&scene=21#wechat_redirect)****
