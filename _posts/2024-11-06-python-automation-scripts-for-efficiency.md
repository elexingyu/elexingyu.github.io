---
categories: articles
date: '2024-11-06'
layout: post
style: huoshui
tags:
- AI
- 教程
title: Python自动化利器：17个高效脚本提升效率
---

我已经使用 Python 近 5 年了，Python 的自动化能力依然吸引我，并激励我进行更多的研究。在过去的一年里，我一直在探索 Python 的自动化领域，并发现了一些令人惊叹的 Python 包、事实和有趣的脚本。在这篇博客中，我将分享一些我每天使用的自动化脚本，它们极大地提高了我的生产力和工作效率。

## 1\. Speakify

我喜欢书籍，但不喜欢自己读书，我更喜欢听书。这个自动化脚本对我来说是一个救命稻草，我经常用它来听 PDF 并将其转换为有声书，以便以后收听。


```python
import PyPDF2
import pyttsx3

# 打开 PDF 文件（输入你的 PDF 文件路径）
file = open('story.pdf', 'rb')
readpdf = PyPDF2.PdfReader(file)

# 初始化文本转语音引擎
speaker = pyttsx3.init()
rate = speaker.getProperty('rate')  # 获取当前的语速
speaker.setProperty('rate', 200)
volume = speaker.getProperty('volume')
speaker.setProperty('volume', 1)  # 设置音量级别（0.0 到 1.0）

# 获取并设置不同的声音
voices = speaker.getProperty('voices')
for voice in voices:
    if "english" in voice.name.lower() and "us" in voice.name.lower():
        speaker.setProperty('voice', voice.id)
        break

# 遍历 PDF 中的每一页
for pagenumber in range(len(readpdf.pages)):
    # 从页面中提取文本
    page = readpdf.pages[pagenumber]
    text = page.extract_text()

    # 使用 speaker 朗读文本
    # speaker.say(text)
    # speaker.runAndWait()

    # 将提取的文本保存为音频文件（如果需要）
    speaker.save_to_file(text, 'story.mp3')
    speaker.runAndWait()

# 停止 speaker
speaker.stop()

# 关闭 PDF 文件
file.close()
```

#### 应用场景

- **帮助视力障碍者**：提供书面内容的音频版本，帮助视力障碍者轻松获取信息。
- **随时随地学习**：允许用户在通勤或锻炼时收听文章或教材。
- **语言学习**：帮助语言学习者通过提供文本的音频版本来提高听力技能。
- **教育**：为学生提供他们阅读材料的音频版本，以便更灵活地学习。

## 2\. TabTornado

在编写这个脚本之前，我习惯通过书签保存我第二天想阅读的内容，但几周后我意识到我的书签栏越来越大，每天都很难找到新的书签。所以我想出了一个 Python 方法来解决这个问题。通过这个自动化脚本，我只需复制粘贴所有链接，并点击一次即可打开它们。

只需点击一次！

```python
import webbrowser

with open('links.txt') as file:
    links = file.readlines()

for link in links:
    webbrowser.open('link')
```

#### 应用场景

**提高工作效率**：需要检查多个工作相关网站的专业人士可以简化他们的日常工作，专注于内容而不是打开链接的过程。
**学习与发展**：在线学习者可以一次性打开所有课程材料、文章和资源，使他们的学习过程更加高效。

### 3\. PicFetcher

在计算机视觉项目中，收集大量图像数据是一个关键挑战。正如 Andrew Ng 所指出的，拥有一个大数据集可能比使用特定算法更重要。高质量的数据对于提高机器学习模型的性能和准确性至关重要。这个自动化脚本使得这个过程更加简单，只需几分钟就能下载指定数量的图片，代码量极少。

```python
# 导入必要的模块和函数
from simple_image_download import simple_image_download as simp

# 创建响应对象
response = simp.simple_image_download

## 关键词
keyword = "Dog"

# 下载图片
try:
    response().download(keyword, 20)
    print("图片下载成功。")
except Exception as e:
    print("发生错误：", e)
```

![脚本输出](https://miro.medium.com/v2/resize:fit:700/1*6bsf-Y1bpkr_ULqoLCB4-Q.png)

#### **应用场景**

- 构建计算机视觉数据集、横幅图像内容创建、营销活动、学术研究等。

## 4\. PyInspector

每个开发者都知道在 Python 代码中追踪 bug 的挫败感，经常被一堆错误困住。编写干净且高效的代码至关重要，但手动分析代码质量可能是个艰巨的任务。这个自动化脚本使用 Pylint 和 Flake8 包来彻底检查你的代码，将其与编码标准进行对比，并指出逻辑错误。它确保你的代码遵循行业最佳实践，并保持无错误状态。

```python
import os
import subprocess

def analyze_code(directory):
    # 列出目录中的 Python 文件
    python_files = [file for file in os.listdir(directory) if file.endswith('.py')]
    if not python_files:
        print("在指定目录中未找到 Python 文件。")
        return

    # 使用 pylint 和 flake8 分析每个 Python 文件
    for file in python_files:
        print(f"分析文件: {file}")
        file_path = os.path.join(directory, file)

        # 运行 pylint
        print("\n运行 pylint...")
        pylint_command = f"pylint {file_path}"
        subprocess.run(pylint_command, shell=True)

        # 运行 flake8
        print("\n运行 flake8...")
        flake8_command = f"flake8 {file_path}"
        subprocess.run(flake8_command, shell=True)

if __name__ == "__main__":
    directory = r"C:\Users\abhay\OneDrive\Desktop\Part7"
    analyze_code(directory)
```

![脚本输出 — 分析我的一个旧脚本的质量](https://miro.medium.com/v2/resize:fit:700/1*DEllOJcCGGaDJah3YKYRKQ.png)


## 5\. DataDummy

无论你是数据科学家需要样本数据来测试模型，还是只是想在不必要的表单中填写随机信息，这个 Python 自动化脚本都非常有用。它生成看似真实但完全虚构的数据集，非常适合测试、开发和模拟用途。该工具可以快速生成姓名、电子邮件、电话号码等，提供了一个多功能的数据生成解决方案。

```python
import pandas as pd
from faker import Faker
import random

fake = Faker()

def generate_fake_data(num_entries=10):
    data = []
    for _ in range(num_entries):
        entry = {
            "Name": fake.name(),
            "Address": fake.address(),
            "Email": fake.email(),
            "Phone Number": fake.phone_number(),
            "Date of Birth": fake.date_of_birth(minimum_age=18, maximum_age=65).strftime("%Y-%m-%d"),
            "Random Number": random.randint(1, 100),
            "Job Title": fake.job(),
            "Company": fake.company(),
            "Lorem Ipsum Text": fake.text(),
        }
        data.append(entry)
    return pd.DataFrame(data)

if __name__ == "__main__":
    num_entries = 10  # 你可以调整生成的条目数
    fake_data_df = generate_fake_data(num_entries)

    ## 假数据 Dataframe
    fake_data_df
```

## 6\. BgBuster

这个自动化脚本已经成为我日常工具包中的重要组成部分。作为一名作家，我经常处理图片，并且经常需要没有背景的图片。虽然有许多在线工具可以完成这项任务，但我对将我的图片上传到互联网上的隐私和安全性有所担忧。这个 Python 脚本利用 rembg 包在本地去除图片背景，确保我的图片保持安全和私密。


```python
from rembg import remove
from PIL import Image

## 输入和输出图片的路径
input_img = 'monkey.jpg'
output_img = 'monkey_rmbg.png'

## 加载并去除背景
inp = Image.open(input_img)
output = remove(inp)

## 将去除背景后的图片保存到与输入图片相同的位置
output.save(output_img)
```

![去除背景前](https://miro.medium.com/v2/resize:fit:700/1*NkZwFtWrMM-PCWZU-otcCQ.png)

![去除背景后](https://miro.medium.com/v2/resize:fit:700/1*Y6oM9C8yQVaRukAENhIXmg.png)

## 7\. MemoryMate

我经常在工作中需要记住重要的任务。为了解决这个问题并提高我的生产力，我使用 Python 开发了 MemoryMate，它作为我的数字记忆助手。它会在指定时间后发送带有自定义消息的提醒，确保我按时完成任务。MemoryMate 显著提高了我的工作效率，帮助我始终如期完成任务。最棒的是，它简单易用，且非常实用。

```python
from win10toast import ToastNotifier
import time

toaster = ToastNotifier()

def set_reminder():
    reminder_header = input("你想让我记住什么？\n")
    related_message = input("相关消息：\n")
    time_minutes = float(input("多少分钟后提醒？\n"))
    time_seconds = time_minutes * 60
    print("正在设置提醒...")
    time.sleep(2)
    print("设置完成！")
    time.sleep(time_seconds)
    toaster.show_toast(
        title=f"{reminder_header}",
        msg=f"{related_message}",
        duration=10,
        threaded=True
    )
    while toaster.notification_active():
        time.sleep(0.005)

if __name__ == "__main__":
    set_reminder()
```

![脚本输出](https://miro.medium.com/v2/resize:fit:700/1*Y26Y-hrhZ-ktfIroAuVpdQ.png)


> 你知道吗？在 Python 中，你可以使用类似 `999**999` 的极大整数进行计算而不会出现溢出错误，因为 Python 会自动使用“大整数”类型处理大数。

## 8\. MonitorMax 😎

系统资源监控对于显示各种系统资源的实时使用情况至关重要。它是用户、系统管理员和开发人员跟踪系统性能、识别瓶颈并确保高效资源管理的宝贵工具。这个 Python 自动化脚本帮助监控 CPU、GPU、电池和内存使用情况，并在任何资源使用超过安全阈值时生成警报。

```python
import psutil
import time
from win10toast import ToastNotifier

# 初始化 ToastNotifier 对象
toaster = ToastNotifier()

# 设置 CPU 使用率、内存使用率、GPU 使用率和电池电量的阈值
cpu_threshold = 40  # 百分比
memory_threshold = 40  # 百分比
gpu_threshold = 40  # 百分比
battery_threshold = 100  # 百分比

# 无限循环，持续监控系统资源
while True:
    try:
        # 获取系统资源信息
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        gpu_usage = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()

        # 检查 CPU 使用率
        if cpu_usage >= cpu_threshold:
            message = f"CPU 使用率过高: {cpu_usage}%"
            toaster.show_toast("资源警报", message, duration=10)

        # 检查内存使用率
        if memory_usage >= memory_threshold:
            message = f"内存使用率过高: {memory_usage}%"
            toaster.show_toast("资源警报", message, duration=10)

        # 检查 GPU 使用率
        if gpu_usage >= gpu_threshold:
            message = f"GPU 使用率过高: {gpu_usage}%"
            toaster.show_toast("资源警报", message, duration=10)

        # 检查电池电量
        if battery is not None and battery.percent <= battery_threshold and not battery.power_plugged:
            message = f"电池电量过低: {battery.percent}%"
            toaster.show_toast("电池警报", message, duration=10)

        # 等待 5 分钟后再次检查资源
        time.sleep(300)

    except Exception as e:
        print("发生错误：", str(e))
        break
```

![输出 — 资源警报](https://miro.medium.com/v2/resize:fit:700/1*uidReqDy7KG5EJi09yLU0g.png)


#### 应用场景：

这个脚本可以用于日常场景，如玩游戏、运行本地服务器、在本地训练深度学习模型等。通过跟踪所有资源，你可以确保脚本或任务使用了最优内存，如果没有，你可以相应地优化它。资源监控仪表板（你可以使用 Tkinter 创建一个仪表板，获取类似任务栏的实时资源图表，并添加通知和高内存使用声音警报）。

## 9\. EmailBlitz

处理大量电子邮件通信可能是一项挑战，无论是营销活动、新闻通讯还是组织更新。这个 Python 自动化脚本使任务变得更轻松，能够轻松发送批量电子邮件。它简化了通信流程，使你能够同时覆盖大量收件人，确保及时高效的消息传递。对于营销人员、管理员或任何需要发送大量电子邮件的人来说，这个脚本提高了生产力，节省了时间，并帮助保持沟通中的个人关怀。

```python
import smtplib
from email.message import EmailMessage
import pandas as pd

def send_email(remail, rsubject, rcontent):
    email = EmailMessage()  ## 创建 EmailMessage 对象
    email['from'] = 'The Pythoneer Here'  ## 发送人
    email['to'] = remail  ## 收件人
    email['subject'] = rsubject  ## 邮件主题
    email.set_content(rcontent)  ## 邮件内容

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()  ## 服务器对象
        smtp.starttls()  ## 用于在服务器和客户端之间发送数据
        smtp.login(SENDER_EMAIL, SENDER_PSWRD)  ## Gmail 的登录 ID 和密码
        smtp.send_message(email)  ## 发送邮件
        print("邮件发送到 ", remail)  ## 打印成功消息

if __name__ == '__main__':
    df = pd.read_excel('list.xlsx')
    length = len(df) + 1
    for index, item in df.iterrows():
        email = item[0]
        subject = item[1]
        content = item[2]
        send_email(email, subject, content)
```

## 10\. ClipSaver

你是否曾发现自己在处理多个文本片段时，结果却忘记了你复制了什么？想象一下，有一个工具可以跟踪你一天中复制的所有内容。这个 Python 自动化脚本正是这样做的。它监控你复制的所有内容，并将每个文本片段无缝地存储在一个简洁的图形界面中。不再需要在无数的标签页中搜索，也不用担心丢失有价值的信息——这个脚本让一切井然有序，易于访问。

```python
import tkinter as tk
from tkinter import ttk
import pyperclip

def update_listbox():
    new_item = pyperclip.paste()
    if new_item not in X:
        X.append(new_item)
        listbox.insert(tk.END, new_item)
        listbox.insert(tk.END, "----------------------")
        listbox.yview(tk.END)
    root.after(1000, update_listbox)

def copy_to_clipboard(event):
    selected_item = listbox.get(listbox.curselection())
    if selected_item:
        pyperclip.copy(selected_item)

X = []

root = tk.Tk()
root.title("剪贴板管理器")
root.geometry("500x500")
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(padx=10, pady=10)

label = tk.Label(frame, text="剪贴板内容:", bg="#f0f0f0")
label.grid(row=0, column=0)

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(root, width=150, height=150, yscrollcommand=scrollbar.set)
listbox.pack(pady=10)

scrollbar.config(command=listbox.yview)

update_listbox()

listbox.bind("<Double-Button-1>", copy_to_clipboard)

root.mainloop()
```


> 你知道吗，`.py` 扩展名在保存代码文件时并不重要？
> 你可以使用任何类型的扩展名来保存 Python 文件，无论是 `.cow`、`.cat` 还是 `.mango`，如果你的脚本是有效的，它将运行并给出你期望的输出。

## 11\. BriefBot

我喜欢每天阅读文章、研究论文和新闻出版物，我知道很多人也有这个习惯。然而，找到时间阅读完整的文章可能是个挑战。这个 Python 自动化脚本通过使用神经网络生成快速摘要来解决这个问题。它利用网络爬虫提取文章内容，并将其输入到一个预训练模型中，生成摘要，节省时间，使你更容易保持信息更新。

```python
from transformers import BartForConditionalGeneration, BartTokenizer
import requests
from bs4 import BeautifulSoup

## 总结文章的函数
def summarize_article(article_text, max_length=150):
    model_name = "facebook/bart-large-cnn"
    tokenizer = BartTokenizer.from_pretrained(model_name)
    model = BartForConditionalGeneration.from_pretrained(model_name)

    inputs = tokenizer.encode("summarize: " + article_text, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=max_length, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

## 爬取文章内容的函数
def scrape_webpage(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        all_text = soup.get_text(separator='\n', strip=True)
        return all_text
    except requests.exceptions.RequestException as e:
        print(f"错误: {e}")
        return None

if __name__ == "__main__":
    webpage_url = "https://www.bleepingcomputer.com/news/security/meet-brain-cipher-the-new-ransomware-behind-indonesia-data-center-attack/"  ## 测试脚本的示例 URL
    webpage_text = scrape_webpage(webpage_url)

    if webpage_text:
        summary = summarize_article(webpage_text)
        print("\n文章摘要:")
        print(summary)
    else:
        print("网页爬取失败。")
```

## 12\. SpellGuard

不论我们英文多么熟练，在写长篇报告、文章或研究论文时，我们都会犯拼写和语法错误。在 AI 时代，许多强大的 Python 包可以帮助纠正这些错误并对你的作品进行润色校对。这个 Python 脚本利用 AI 检测并纠正拼写和语法错误，确保你的写作清晰、准确且专业。

```python
## 安装库
!pip install lmproof

## 导入库
import lmproof as lm

## 校对函数
def Proofread(text):
    proof = lm.load("en")
    error_free_text = proof.proofread(text)
    return error_free_text

## 示例文本
TEXT = ''  ## 在此处放置示例文本

## 调用函数
Print(Proofread(TEXT))
```

![脚本输出](https://miro.medium.com/v2/resize:fit:700/1*imcSxGXsiMUjzWLQ56Ailw.png)


## 13\. LinkStatus

拥有一个博客网站仍然是许多作家的梦想。确保所有链接正常工作对于维护一个专业且用户友好的博客至关重要。损坏的链接会让读者感到沮丧，并损害你网站的信誉。这个 Python 自动化脚本允许你轻松检查多个 URL 的网络连接性。通过定期监控你的 URL，这个脚本确保你的链接始终处于活动状态，提升你网站的可靠性和用户体验。

```python
import csv
import requests
import pprint

def get_status(website):
    try:
        status = requests.get(website).status_code
        return "正常" if status == 200 else "错误 404"
    except:
        return "连接失败！"

def main():
    with open("sites.txt", "r") as fr:
        websites = [line.strip() for line in fr]

    web_status_dict = {website: get_status(website) for website in websites}
    pprint.pprint(web_status_dict)

    # 将结果写入 CSV 文件
    with open("web_status.csv", "w", newline='') as csvfile:
        fieldnames = ["网站", "状态"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for website, status in web_status_dict.items():
            writer.writerow({"网站": website, "状态": status})

    print("数据已上传到 CSV 文件！")

if __name__ == "__main__":
    main()
```

![脚本输出](https://miro.medium.com/v2/resize:fit:700/1*ePZLmHZIrfAnpdLEe1Xggw.png)


> 你可以在 Python 中使用中文字符串作为变量名。
> 例如：`金竹戈女日 = "Hello World"`

## 14\. DailyDigest

保持对你所在城市、州、国家或世界最新动态的了解很重要，但繁忙的日程常常让我们无法花时间阅读新闻。这个自动化脚本通过从 Google News 抓取流行新闻并大声朗读给你，解决了这个问题。无论你是刚开始一天还是在路上，这个脚本都能确保你轻松获取最新的新闻故事。

```python
import pyttsx3
import requests

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def trndnews():
    url = "http://newsapi.org/v2/top-headlines?country=us&apiKey=GET_YOUR_OWN"
    page = requests.get(url).json()
    article = page["articles"]
    results = []
    for ar in article:
        results.append(ar["title"])

    for i in range(len(results)):
        print(i + 1, results[i])
        speak(results)

trndnews()

'''运行脚本以获取来自美国的头条新闻'''
```

### 15\. QRGenie

自从人们开始使用二维码进行支付后，二维码的流行度迅速上升。如今，它们被用于分享社交链接、秘密消息、优惠券代码等。这个 Python 自动化脚本帮助你创建自定义二维码，包含你选择的数据，让你轻松分享信息并给观众留下深刻印象。

```python
import qrcode

def generate_qr_code(link, filename):
    """为给定的链接生成二维码并保存为文件名。"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("profile.png")

if __name__ == "__main__":
    generate_qr_code("https://huoshuiai.com/", "Profile.png")
    print(f"二维码保存成功！")
```



## 16\. ShrinkLink

我每天处理大量链接，有些我会保存，有些我会分享给我的读者。我最不喜欢的部分就是 URL 的长度，它们可能令人烦恼且难以阅读。这个自动化脚本通过使用外部 API 将长 URL 转换为简短的、易于管理的链接，极大地解决了这个问题。

```python
import pyshorteners

def generate_short_url(long_url):
    s = pyshorteners.Shortener()
    return s.tinyurl.short(long_url)

long_url = input('粘贴长 URL \n')
short_url = generate_short_url(long_url)
print(short_url)
```

![](https://miro.medium.com/v2/resize:fit:700/1*I4th9xrFEvc_3ajfkM3I8Q.png)

## 17\. CaptureIt

无论你是游戏玩家、影响者、艺术家还是开发者，屏幕录制软件对于捕捉你的活动至关重要。然而，许多现有的解决方案价格昂贵，或者有诸如水印和时间限制等限制。这个 Python 自动化脚本提供了一个简单的解决方案，没有水印、没有时间限制，并且可以自定义屏幕窗口选项。

```python
import cv2
import numpy as np
import pyautogui

SCREEN_SIZE = tuple(pyautogui.size())
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
fps = 12.0
record_seconds = 20
out = cv2.VideoWriter("video.mp4", fourcc, fps, SCREEN_SIZE)

for _ in range(int(record_seconds * fps)):
    img = pyautogui.screenshot(region=(0, 0, 500, 900))
    frame = np.array(img)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    out.write(frame)

    cv2.imshow("视频帧", frame)
    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
out.release()
```

## 额外福利

### H2OReminder

这个自动化脚本是一个简单而强大的程序，旨在通过定期提醒用户喝水来保持水分摄入。对于那些长时间坐在电脑前或日程繁忙的人来说，这是一款非常有用的工具，它可以帮助你保持健康的习惯，鼓励你定期喝水，保持整体健康和福祉。

```python
import time
from plyer import notification

if __name__ == "__main__":
    while True:
        notification.notify(
            title="请喝水",
            message="美国国家科学院、工程院和医学院建议：男性每天摄入约 15.5 杯（3.7 升）液体，女性约 11.5 杯（2.7 升）。保持喝水习惯！！！",
            app_icon="./Desktop-drinkWater-Notification/icon.ico",
            timeout=12
        )
        time.sleep(1800)  ## 根据你的喝水间隔调整时间！
```