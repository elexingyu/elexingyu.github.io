---
layout: post
title: "50+开源仓库！让你在本地轻松运行大模型"
date: 2024-03-14
tags: ['AI']
style: huoshui
---

> 作者：Vince Lam 编译：Gavin



在之前的文章中，我讨论了使用本地托管的开源大模型（LLM）的好处，包括数据隐私和成本节约。通过主要使用免费模型，偶尔切换到GPT-4，我的月度支出从20美元降到了0.50美元。对于移动访问，设置一个端口转发到你的本地LLM服务器是一个免费的解决方案。

有许多开源工具可以在本地托管开源大模型进行推理：从命令行（CLI）工具到完整的GUI桌面应用程序。在这里，我将概述一些流行的开源仓库，并推荐我自己使用。我将这篇文章分为以下几个部分：

  1. 1\. 一站式桌面解决方案

  2. 2\. 通过CLI和后端API服务器进行大模型操作

  3. 3\. 用于连接大模型后端的前端用户界面（UI）

每个部分都包括一个相关的开源大模型 GitHub仓库的表格，以及用于衡量其受欢迎程度和活跃度的信息。（注：文末附表格下载方式）

这些项目在范围上可能会有所重叠，并且会分为后端服务器和用户界面的不同组成部分。这一领域发展迅速，因此细节可能很快就会过时。

![](/assets/images/97fa76d2ce7148f29bfe49aa2b5da2b6.png)

## 1\. 桌面解决方案

一站式桌面解决方案提供了易于使用和快速部署的环境，用户可以轻松地运行大模型的推理任务。

用户仅需下载并打开`.exe`或`.dmg`文件，即可迅速上手。这些工具非常适合技术背景不强、寻求即用型ChatGPT替代方案的用户，也适合任何希望在转向更复杂、更技术化的替代品之前探索AI的人。

### 最受欢迎的：GPT4All

GPT4All是一个一站式应用程序，它模仿了ChatGPT的界面，可以快速运行本地大模型来处理常见任务和检索增强生成（RAG，Retrieval
Augmented Generation, RAG）。所提供的模型即开即用，终端用户使用起来很方便。

下图是GPT4All 实时演示界面在 M1 MacOS 设备上的展示：

![](/assets/images/24f3c0c5f018460cb89d167ec6f2b5d0.gif)

### 开源替代方案：Lobe Chat 和 Jan

LM Studio 因设置简单和界面对用户友好，经常受到 YouTubers
和博主好评。它提供了模型卡片浏览、模型下载和系统兼容性检查等功能，使得模型选择对初学者来说变得易于上手。

它提供了模型卡片浏览、模型下载和系统兼容性检查等功能，使得模型选择对于初学者来说变得易于上手。

尽管 LM Studio
有诸多优点，但由于其开源许可协议，这会让其在商业环境中使用受到限制，我在使用它时还是有所犹豫，产品不可避免的商业化也是值得关注的一个问题。我更倾向于选择开源方案。

Lobe Chat 和 Jan 是 LM Studio 的开源替代品，它们都拥有较为优秀的用户界面。

Lobe Chat 是一个开源的高性能聊天机器人框架，支持语音合成、多模态和可扩展的插件系统，还支持一键免费部署私人 ChatGPT/LLM 网页应用程序。

![](/assets/images/5d99ff84002f460b9fec8408b8ca0c9c.png)

而 Jan 则是一款支持 Mac、Windows 和 Linux 系统的本地 AI 桌面应用，它除了支持本地模型外，还可以连接 OpenAI
API，为用户提供了更多的灵活性和选择。

下图是Jan UI在配备16GB Sonoma 14的Mac M1上运行情况：

![](/assets/images/9e9c16efc28948f99c79404dc712b6bb.gif)

### 功能齐全：h2oGPT

H2O.ai 是一家人工智能公司，通过其自动机器学习（AutoML）产品以及现在的生成式 AI 产品，为开源社区做出了巨大贡献。h2oGPT
提供了广泛的功能和定制选项，非常适合有 英伟达 GPU 的用户：

  * • 支持多种文件格式，适用于离线 RAG（Retrieval-Augmented Generation，检索增强生成）

  * • 使用奖励模型评估模型性能

  * • 适用于搜索、文档问答、Python 代码、CSV 文件的代理

  * • 通过数千个单元和集成测试进行的稳健测试

在正式安装前，你可以访问 gpt.h2o.ai
体验演示版。如果该界面满足你的需求，并且你对更多功能感兴趣，可以下载该应用的基础版本，该版本提供有限的文档查询功能。有关安装的问题，请参考设置说明。

![](/assets/images/d38953499a5f42c69c86ab18a5878327.jpg)

h2oGPT 可在 https://gpt.h2o.ai/ 获取。

### 其他桌面解决方案

最受欢迎的五大免费开源软件（FOSS）大模型桌面运用如下：

![](/assets/images/d0f1b3f07dd645c39b2c84e047592231.jpg)

## 2\. 通过CLI和后端API服务器进行大模型操作

CLI（命令行界面）工具能够通过远程 API 搭建本地推理服务器，并与前端用户界面（见第3节）集成，以提供定制化体验。它们通常提供与OpenAI
API兼容的端点，这让替换模型仅需最小的代码。

虽然聊天机器人是最常见的用例，但你也可以使用这些工具来驱动代理，使用如CrewAI和微软的AutoGen等框架。

### 高度优化：llama.cpp

llama.cpp 为跨设备的大模型推理提供了极简的设置。该项目是 Llama2 的 C++ 移植版本，支持 GGUF 格式的模型，包括多模态模型，如
LLava。其效率适合消费级硬件和边缘设备。

![](/assets/images/7c39aeb886534994aabedd6a01b64b5c.jpg)

llama.cpp

有许多基于llama.cpp的开源仓库，例如llama-cpp-
python（更多相关信息可以在README文件的描述部分找到）。这意味着，有很多工具和用户界面都是构建在llama.cpp之上的，它们为用户提供了更加直观和易用的交互方式。

如果你想开始使用，可以按照指引操作（网址：https://github.com/ggerganov/llama.cpp?tab=readme-ov-
file#usage)。你需要从HuggingFace下载GGUF格式的模型。

llama.cpp还包含了一个内置的HTTP服务器功能，你只需要在命令行中输入`./server`就能够启动。

    
    
    # Unix-based example  
    ./server -m models/7B/ggml-model.gguf -c 2048

因此，你可以轻松地将它与其他网页聊天界面（UI）连接起来，这些界面在第2部分中有列出。

对于那些熟悉CLI、喜欢编写自定义脚本以及在终端中查看输出的用户来说，llama.cpp是最佳选择。

### 直观的CLI：Ollama

Ollama是另一个基于llama.cpp构建的LLM推理命令行工具，它将脚本抽象成简单命令。受到Docker的启发，Ollama提供了简单直观的模型管理功能，这让更换模型变得容易。你可以在https://ollama.ai/library
查看可用模型的列表。你还可以根据这些指示运行HuggingFace上的任何GGUF模型。

![](/assets/images/f52eae691c8e4540af77d7ad73dc7307.jpg)

当你按照说明下载了Ollama应用程序之后，可以在终端运行以下命令，执行简单的推理：

    
    
    ollama run llama2

Ollama的README中提供了一个有用的通用启发式规则，用于选择模型大小：

> 你应该至少有8GB的可用内存来运行7B（70亿参数）模型，16GB来运行13B（130亿参数）模型，以及32GB来运行33B（330亿参数）模型。
>
>
> 默认情况下，Ollama使用4位量化。如果你想尝试其他量化级别，可以尝试其他标签。q后面的数字代表用于量化的位数（例如，q4表示4位量化）。数字越高，模型的准确性越好，但运行速度会越慢，同时需要的内存也越多。

使用`ollama
serve`时，Ollama会将自己设置为本地服务器，端口号为11434，这个服务器可以与其他服务进行连接。更多信息可以查看常见问题解答（FAQ）。

Ollama因其强大的社区支持和活跃的开发而脱颖而出，频繁的更新是根据Discord上用户的反馈驱动的。Ollama拥有许多集成，并且人们已经开发出了移动设备兼容性。

### 其他可选择的大模型后端

前5名的大模型推理仓库表：

![](/assets/images/d739663c4e5a4aa4aec1f32a884a772a.jpg)

## 3\. 连接到大模型后端的前端用户界面

上一节讨论的工具能够利用预训练的大模型来处理基本查询。然而，通过网络搜索和检索增强生成（RAG）集成外部信息后，这些工具的能力显著提升。使用利用现有LLM框架的用户界面，如LangChain和LlamaIndex，简化了将数据块嵌入向量数据库的过程。

这部分提到的用户界面，可以与第1节「工具」中的后端服务器无缝对接。它们兼容多种API，包括OpenAI的API，便于与专有和开放权重模型轻松集成。

### 在视觉和功能上最类似于ChatGPT：Open WebUI

Open WebUI是一个网页界面，提供了本地RAG集成、网络浏览、支持语音输入、多模态（如果模型支持的话）、支持OpenAI
API作为后端，以及更多功能。这个项目之前被称为ollama-webui，由Ollama团队开发。

![](/assets/images/0817061c2a7b4eabb7d4480f22a787bf.gif)

要连接 Open WebUI 与 Ollama，你只需要安装 Docker，然后简单地运行以下命令：

    
    
    docker run -d -p 3000:8080 --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:main

接着，你可以轻松地通过 http://localhost:3000 访问 Open WebUI。

### 支持多后端的用户界面：text-generation-webui

text-generation-webui 由 Oogabooga 开发，是一个功能齐全的 Gradio
网页界面，专为大模型（LLMs）设计，并支持多种后端加载器，如
transformers、GPTQ、autoawq（AWQ）、exllama（EXL2）、llama.cpp（GGUF）以及 Llama 模型——这些都是对
transformers 代码库进行重构并加入额外调整的版本。

![](/assets/images/eaaa2b27603a401ab2e7ce7f3f3864d0.jpg)

text-generation-webui 可自由配置，甚至由于其 transformers 后端，还提供了使用 QLoRA
的微调功能。这使您能够根据自己的数据增强模型的能力和定制模型。他们的 wiki 上有详尽的文档。我发现这个选项对于快速测试模型非常有用，因为它开箱即用。

### 其他用户界面选项

前五名开源大模型前端界面：

![](/assets/images/e20b596f3b8d4493ad8da215f79c5f27.jpg)

### 结论：我使用和推荐的工具

我一直在使用**Ollama**
，因为它的多功能性、易于管理的模型以及强大的支持，特别是它与OpenAI模型的无缝集成。在编程方面，Ollama的API可以连接到continue.dev的VS
Code插件，这让它取代了GitHub Copilot成为我的首选。

在众多用户界面中，我偏爱**Open WebUI**
，因为它拥有专业的、类似ChatGPT的界面。对于那些寻找类似ChatGPT的用户友好桌面应用的人来说，Lobe
Chat和Jan是我的首选推荐，具体取决于你需要哪些功能。

### 参考资料

https://github.com/janhq/awesome-local-ai

https://www.reddit.com/r/LocalLLaMA/

  

* 本文由活水智能编译，转载请注明出处

微信公众号后台回复「大模型」，即可获取50+本地轻量级运行大模型的完整列表。

  

