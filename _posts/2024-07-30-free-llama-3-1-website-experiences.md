---

layout: post  
title: "5个免费使用Llama 3.1的网站，还可在电脑桌面运行"  
date: 2024-07-30  
tags: ['AI']  
style: huoshui  

---

![](/assets/images/563bcde5dc7b4e96a15834fd3d04c5b3.png)

Meta最近发布了Llama 3.1，这款模型在某些基准测试中已经超越了最好的闭源语言模型，如GPT-4o、Gemma 2和Claude 3.5 Sonnet。

Llama 3.1系列支持多语言模型，包括法语、德语、印地语、意大利语、葡萄牙语、西班牙语和泰语，提供80亿、700亿和4050亿参数规模的版本。尤其是4050亿参数模型，使用超过16,000个Nvidia H100 GPU进行训练，并拥有高达128K的上下文窗口。

![](/assets/images/a27c9b4e48d247ceae0a051d4aa9c3bf.png)

接下来，我将分享五种免费体验Llama 3.1的方法，最后还有一个小彩蛋哦！

## 1. Ollama

Ollama是一个先进的AI工具，允许用户轻松地在本地机器上设置和运行大模型。

### 步骤：

1. **下载并安装Ollama**：访问Ollama的官网并下载安装包。安装成功后，在终端运行`ollama -v`查看版本信息。

   ![](/assets/images/6d1ff4582ac04385a4abcbbee3f335b4.jpg)

   官网：[Ollama](https://ollama.com/)

2. **下载Llama 3.1模型**：根据你的电脑性能选择合适的版本。由于运行4050亿参数模型的硬件要求较高，建议先尝试80亿参数模型。

   ![](/assets/images/91ff3ff1babe418099dd7dde26f8e5da.png)

3. **开始使用**：运行以下命令即可开始体验Llama 3.1。

   ```bash
   ollama run llama3.1:8b
   ```

   ![](/assets/images/e4cc33dd4ce44ef8a36223d0b1ccbd49.png)

如果你已经参加过AI生产力工作坊二期，那么你应该对这些操作非常熟悉，可以结合课程中的技巧进行更多尝试，欢迎在群内分享你的经验。

## 2. HuggingChat

HuggingChat是由Hugging Face开发的开源AI聊天机器人，托管了多个生成式AI模型。

### 步骤：

1. **访问HuggingChat**：前往Hugging Face的官网并创建账户。

   网址：[HuggingChat](https://huggingface.co/chat/)

2. **激活Llama 3.1模型**：在设置页面中选择`meta-llama/Meta-Llama-3.1–405B-Instruct-FP8`模型。

   ![](/assets/images/b9b0c7f5088c4347bfd8ca8a5449f896.png)

3. **开始使用**：关闭设置窗口后，你就可以开始与Llama 3.1互动了。

   ![](/assets/images/4790d977d56d4691bcc60e7bfde49345.png)

HuggingChat还提供了增强功能的附加工具，如网页搜索和PDF解析，甚至可以生成图像。启用图像生成工具后，你可以让Llama 3.1生成图片，例如：

![](/assets/images/57d4885b9545455a85841997d14335d9.png)

## 3. Groq

Groq因其专门设计用于加速AI推理工作负载的硬件和软件而闻名，Llama 3.1目前已经在Groq Playground上托管。

### 步骤：

1. **访问Groq Playground**：前往Groq的官网并登录。

   官网：[Groq Playground](https://console.groq.com/playground)

2. **使用Groq Chat**：虽然目前在Playground上无法使用4050亿参数模型，但你可以使用Groq Chat，它的速度非常快。

   ![](/assets/images/01bfca39f8c343ad9bbc296a54d7f74c.png)

   Groq Chat官网：[Groq Chat](https://groq.com/)

Groq的LPU（学习处理单元）可以实现领先的推理速度，例如在700亿参数模型上每秒250个token，在80亿参数模型上每秒超过1200个token。

## 4. Fireworks AI

Fireworks是一个构建和部署生成式AI API的平台，支持Llama 3.1的所有模型。

### 步骤：

1. **访问Fireworks AI**：前往Fireworks AI的官网并登录。

   页面：[Fireworks AI](https://fireworks.ai/models/fireworks/llama-v3p1-405b-instruct)

2. **调整参数并调用API**：在右侧部分调整参数设置，并使用你的配置调用API。

   ![](/assets/images/cb4165dd24794860a43a571bdbc8767d.png)

请注意，你需要一个API密钥才可以使用更多功能，适合开发者。

## 5. Cloudflare Playground

Cloudflare是互联网上最大的网络平台之一，最近他们推出了一个AI运用，允许用户探索不同的文本生成模型。

### 步骤：

1. **访问Cloudflare Playground**：前往Cloudflare的官网并登录。

   地址：[Cloudflare Playground](https://playground.ai.cloudflare.com/)

2. **选择模型并开始聊天**：无需创建账户即可免费使用。

   ![](/assets/images/23f1d9347b194d628afe5862be5cc4cc.png)

## 彩蛋：Poe.com

Poe是免费体验Llama 3.1的最佳方式之一。

### 步骤：

1. **访问Poe官网并创建账户**：每天赠送3,000个免费积分，可发送6条免费消息。

   官网：[Poe](https://poe.com)

2. **找到Llama-3.1–405B-T机器人**：在官方机器人部分找到并打开它，然后开始与Llama 3.1聊天。该机器人由Together.ai托管。

   ![](/assets/images/562d3f143e5b4c3faadbe5246be5383b.png)

Poe还支持下载到手机或Mac上使用，功能强大，推荐大家试试！

## 推荐阅读

- [Triplex：用于创建知识图谱的开源模型，成本比GPT-4o低10倍！](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247486546&idx=1&sn=98139129e78b457e2f1885495f3c58b3&chksm=c3546ec1f423e7d7df329e883ab39c79eaf61e6bc38cc801a318c7f95a229a670b161ca445af&scene=21#wechat_redirect)

- [五分钟内将文本转为图谱，可用于发现实体之间关系和规律，与文本对话](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247486457&idx=1&sn=e801511901e60a9058b443819eaaaf60&chksm=c354696af423e07cf55e3fdc59375b352e493f6ab3cf282d199f74ca9b2556cb797671cb2418&scene=21#wechat_redirect)

- [从大规模文档中发现规律，找到相互关系，速度更快，信息更全面！](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247486198&idx=1&sn=fe870f73635f7e97d576fb81c20befe2&chksm=c3546865f423e173293ec3697258a848a7dff22690a4b9cad0a91abdce7745760d98c5b16281&scene=21#wechat_redirect)
