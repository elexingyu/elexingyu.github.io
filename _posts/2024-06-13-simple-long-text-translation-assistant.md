---
layout: post
title: "智能翻译助手：让长文本翻译、专业术语和方言翻译变得更简单！[附PDF翻译工具]"
date: 2024-06-13
tags: ['AI', '教程']
style: huoshui
---



![](/assets/images/abfe205af61c40c68e8b17797f5b6e5a.png)  

日常工作中，经常遇到要把国外的资料翻译为母语，用于学习和沟通。

但是，翻译长文本（比如书，很多PDF 文档），往往耗时耗力。如果夹杂着方言、专业术语，还要让翻译后的文本保持特定语言风格，更让人头疼不已。

好在有了大模型，一切变得简单了。

本文将介绍一种全新的翻译智能助手（translation-agent），可用于翻译长文本，并且让翻译后保持特定语言风格，更精准地翻译专业术语和地方方言。

项目地址：https://github.com/andrewyng/translation-agent

该智能翻译助手由AI领域大牛吴恩达博士开源。根据BLEU分数的评估，该翻译助手，有时翻译效果比头部的翻译产品更好。

![](/assets/images/04c2656e7cce44908ac03b0584904876.png)

这无疑是智能翻译的起点，是翻译领域一个很有有前景的方向。目前还处于早期，还有很大的改进空间。

**文章最后，我们会附上常用于翻译PDF等文档的工具。**

## **工作原理**

这个机器翻译智能助手通过以下三步实现：

  1. 1\. 使用大模型将文本从`源语言`翻译为`目标语言`；

  2.   

  3. 2\. 让大模型对翻译进行反思，提出改进建议；

  4.   

  5. 3\. 根据建议优化翻译。

有没有很熟悉的感觉？先翻译—>反思—>优化翻译。

## 有什么优势？

该智能翻译工作流使用大模型作为翻译的核心引擎，具备很强的灵活性和适应性。

比如，你可以通过更改提示词，比传统翻译更容易实现：

修改输出风格。如正式或非正式风格。

处理习惯性用语和术语。如名字、技术术语和缩写。例如，在提示词中放入术语表，确保特定术语（如“开源”、“H100”或“GPU”）能很好地翻译。

根据特定区域或方言进行调整。例如，拉丁美洲西班牙语与西班牙西班牙语不同；加拿大法语与法国法语不同。

## 怎么使用呢？

以下是使用`translation-agent`的步骤：

### 安装：

需要使用Poetry包管理器进行安装。Poetry安装 具体步骤如下：

需要一个包含OPENAI_API_KEY的.env文件才能运行工作流程。参见.env.sample文件作为示例。

    
    
    git clone https://github.com/andrewyng/translation-agent.git  
    cd translation-agent  
    poetry install  
    poetry shell # 激活虚拟环境

### 开始使用

    
    
    import translation_agent as ta  
    source_lang, target_lang, country = "English", "Spanish", "Mexico"  
    translation = ta.translate(source_lang, target_lang, source_text, country)

参见examples/example_script.py文件以获取示例脚本。

以上只是简单的介绍，感兴趣的可以尝试：

1）使用不同的大模型和超参数，特别是为了优化特定风格；2）探索如何高效地建立专业术语表、地方方言表；3）评估不同语言的表现，并寻找更合适的评估方法，特别是在专业领域或在特殊文本类型中的应用。  

  

下面介绍一些用来翻译PDF等文档的工具。

## 文档翻译工具

### 沉浸式翻译

非常推荐！

网址：https://immersivetranslate.com/

安装浏览器插件，选择右下角更多，可选择「制作双语BPUB电子书」、「翻译本地PDF文件」、「翻译THML / txt文件」、「翻译本地字幕文件」等。

![](/assets/images/35515f3564034141bf37310738aa3968.png)

免费使用，高级功能需会员。

沉浸式翻译还支持调用谷歌翻译、OpenAI、小牛翻译等 API 进行翻译，如想使用GPT-3.5/4 翻译，只需填入 API Key。

#### 小牛翻译

网址：https://niutrans.com/trans?type=doc

选择「文档翻译」上传文档即可翻译。每日可享20万字符流量+100页文档页数，免费翻译。

![](/assets/images/3eeb1f1a6105456a834896b8291b432a.png)

支持格式：PDF、DOCX、DOC、PPT、PPTX、XLS、XLSX

### 谷歌翻译

网页：https://translate.google.com/?hl=zh-CN&sl=en&tl=zh-CN&op=docs

上传文档即可翻译，排版一般。免费。

![](/assets/images/0bb7c25fd7ba488494764f28b1cf3e32.png)

### 彩云小译

网页：https://fanyi.caiyunapp.com/#/

支持文档翻译、网页翻译、视频字幕翻译。点击「文档翻译」，上传文档即可开始翻译。免费版限额3次。

![](/assets/images/c488147967a84c009b59298b6ad129ab.png)

 
