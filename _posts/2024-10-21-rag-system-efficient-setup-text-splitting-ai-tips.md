---
categories: articles
date: '2024-10-21'
layout: post
style: huoshui
tags:
- AI
title: RAG系统高效搭建：文本分割与AI应用技巧
---

![图片来源：Clark Tibbs on Unsplash](https://miro.medium.com/v2/resize:fit:1400/0*ALfK1LZ0nYnnYgrM)

RAG（检索增强生成）是一种创建基于大语言模型（LLM）应用的高效方式。它有助于生成对用户查询的准确回答。为了创建一个基于 RAG 的应用程序，我们需要执行一些操作，例如文档加载、将大文档拆分为多个小块、嵌入、嵌入索引，并将它们存储在向量数据库中。然后根据用户查询，系统从向量数据库中提取相关上下文并传递给提示词以及用户查询。然后 LLM 将用户查询和内容结合起来，生成适当的响应。这是 RAG 系统的整体流程。

_如果你想一步步学习生成式 AI，可以关注_ _这个 Medium 列表_，_成为这方面的专家。_

![来源：作者提供的图片](https://miro.medium.com/v2/resize:fit:1400/1*LqJpLwJ71KFV_wIdHwZIfQ.png)

**文本分割器** 在 LangChain 中有助于将大文档分解为较小的块。在大文档或文本中，很难根据用户查询找到相关的上下文。此外，我们无法将整个大文档传递给 LLM 模型。每个 LLM 模型能处理的 **Token** 是有限的，因此必须将大文本拆分为较小部分。这样我们就可以轻松地从这些小块中找到相关的上下文，并将其作为输入传递给 LLM，确保输入量低于模型的最大输入大小。因此，文本分割器的 **关键使用场景** 如下：

-   处理超过 LLM 模型 Token 限制的大文档，文本分割技术有助于将文档划分为较小的部分，以便模型处理。
-   在问答任务中，较小的文本块在查询、索引和检索方面更有效，而大文档则效率较低。
-   它通过在适当的点拆分段落或句子数量，帮助将上下文保留在较小的部分中。这样每个块都包含适当的知识。
-   LLM 在上下文窗口大小上有 Token 数量限制。即使上下文大小是无限的，更多的输入 Token 也会导致更高的成本，而金钱不是 **无限的**。

## LangChain 中的文本分割技术

LangChain 提供了许多文本分割技术来适应不同类型的数据。今天我们将探索不同的文本分割技术，例如字符文本分割器、递归字符文本分割器、Token 文本分割器、Markdown 标题文本分割器、Python 代码文本分割器、HTML 文本分割器、Spacy 文本分割器、Latex 文本分割器、递归 JSON 文本分割器。如果你有兴趣探索更多的分割技术，请访问这个 LangChain 页面。建议你在自己的系统上运行代码，深入理解这些概念。

首先，安装执行分割技术所需的库。打开命令提示符或终端并运行以下命令。

```
pip install langchain spacy langchain_text_splitter langchain_core
```

## 字符文本分割器

这是最基本的文本分割技术，它根据特定的字符数来划分文本。它适用于简单且统一的文本分割任务。参数 **separator** 表示文本将只在换行符处拆分，因为使用了 “\\n” 作为分隔符。它避免在段落中间拆分。我们可以使用其他分隔符，如空格。块大小表示每个块中的最大字符数，而块重叠表示从前一个块中取多少字符到下一个块中。_我们要注意，每个块应该包含有用的知识。_

```
from langchain.text_splitter import CharacterTextSplitter

text = "你的长文档文本在这里..."

splitter = CharacterTextSplitter(
    separator="\n\n",  
    chunk_size=10, 
    chunk_overlap=2 
)

chunks = splitter.split_text(text)
print(chunks)
```

## 递归字符文本分割器

它使用字符分隔符将大文档分解为较小的块。它递归地尝试使用分隔符层次结构（如段落 `\n\n`、句子 `\n` 和字符 `.`、`,`）来拆分文本。它优先进行较高级别的拆分（如段落），如果需要则向下移动层次结构。当你需要灵活且分层的方法时，可以尝试这种技术。

```
from langchain.text_splitter import RecursiveCharacterTextSplitter

text = "你的长文档文本在这里..."

splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", " ", ""],
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len
)

chunks = splitter.split_text(text)
print(chunks)
```

## Token 文本分割器

它根据 Token 而不是字符或单词来拆分文本。对于有 Token 限制的语言模型来说，这是必要的。它使用模型的 Token 化方法将大文档分割成块。这里我们使用了 OpenAI 的编码来对文档进行 Token 化。

```
from langchain.text_splitter import TokenTextSplitter

text = "你的长文档文本在这里..."

splitter = TokenTextSplitter(
    encoding_name="cl100k_base",  
    chunk_size=100,
    chunk_overlap=20
)

chunks = splitter.split_text(text)
print(chunks)
```

## Markdown 标题文本分割器

这种方法用于根据标题级别（如 #、##、### 等）拆分 Markdown 文档。它使用分层方法，例如将特定标题及其子标题下的文本分开。当你想组织 Markdown 文件中的内容（如技术文档）时，可以尝试这种分割方法。

```
from langchain.text_splitter import MarkdownHeaderTextSplitter

markdown_text = """
# 标题
## 部分 1
部分 1 的内容
## 部分 2
部分 2 的内容
### 子部分 2.1
子部分 2.1 的内容
"""

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]

splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
chunks = splitter.split_text(markdown_text)
print(chunks)
```

## Python 代码文本分割器

当你想将 Python 代码分解为较小的逻辑块时，这种技术非常有用。它基于 Python 特定的分隔符（如函数、类等）来拆分代码。

```
from langchain.text_splitter import PythonCodeTextSplitter

python_code = """
def function1():
    print("Hello, World!")

class MyClass:
    def __init__(self):
        self.value = 42

    def method1(self):
        return self.value
"""

splitter = PythonCodeTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

chunks = splitter.split_text(python_code)
print(chunks)
```

## HTML 文本分割器

当你处理网页时，想要基于 HTML 层次结构进行分割而不破坏文档结构。你可以使用这种技术，它根据文档的结构来拆分 HTML 内容。它识别常见的 HTML 标签，如 `<p>、<div>、<h1>`等，并根据文档结构拆分文本。

```
from langchain_text_splitters import HTMLSectionSplitter

html_text = """
<html>
<body>
<h1>主标题</h1>
<p>这是一个段落。</p>
<div>
    <h2>子部分</h2>
    <p>另一个段落。</p>
</div>
</body>
</html>
"""

headers_to_split_on = [("h1", "Header 1"), ("h2", "Header 2")]
splitter = HTMLSectionSplitter(
    headers_to_split_on=headers_to_split_on,
    chunk_size=100,
    chunk_overlap=20
)

chunks = splitter.split_text(html_text)
chunks
```

## Spacy 文本分割器

它使用 Spacy NLP 管道来分割文本，利用 Spacy 的 Token 化和句子分割能力，基于语言规则来拆分文本。当语言细微差别（如句子边界）很重要时，可以尝试这种方法。

```
from langchain.text_splitter import SpacyTextSplitter

text = "你的长文档文本在这里。它可以是多种语言的。SpaCy 将处理语言的细微差别。"

splitter = SpacyTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

chunks = splitter.split_text(text)
chunks
```

## Latex 文本分割器

当你处理科学论文、数学文档或任何 LaTex 格式的文本时，可以使用这种技术，它在保留其结构的同时拆分文本。它使用 latex 特定的分隔符，如 `\\documentclass{}`、`\\begin{}`等，将文本拆分为块。

```
from langchain.text_splitter import LatexTextSplitter

latex_text = r"""
\documentclass{article}
\begin{document}
\section{引言}
这是引言部分。
\section{方法}
这是方法部分。
\end{document}
"""

splitter = LatexTextSplitter(
    chunk_size=100,
    chunk_overlap=20
)

chunks = splitter.split_text(latex_text)
chunks
```

## 递归 JSON 文本分割器

你可以使用它将大型或嵌套的 JSON 对象分割为较小的可管理部分。它递归地拆分 JSON，并通过遍历键和值保持层次结构的顺序。

```
from langchain_text_splitters import RecursiveJsonSplitter

json_data = {
    "company": {
        "name": "TechCorp",
        "location": {
            "city": "Metropolis",
            "state": "NY"
        },
        "departments": [
            {
                "name": "Research",
                "employees": [
                    {"name": "Alice", "age": 30, "role": "Scientist"},
                    {"name": "Bob", "age": 25, "role": "Technician"}
                ]
            },
            {
                "name": "Development",
                "employees": [
                    {"name": "Charlie", "age": 35, "role": "Engineer"},
                    {"name": "David", "age": 28, "role": "Developer"}
                ]
            }
        ]
    },
    "financials": {
        "year": 2023,
        "revenue": 1000000,
        "expenses": 750000
    }
}

splitter = RecursiveJsonSplitter(max_chunk_size=200, min_chunk_size=20)

chunks = splitter.split_text(json_data, convert_lists=True)

for chunk in chunks:
    print(len(chunk))
    print(chunk)
```

## 选择合适的文本分割器

我们之前讨论过递归字符文本分割技术。你也可以使用这种技术递归地分割编程语言。编程语言的结构不同于纯文本，我们可以根据特定语言的语法来拆分代码。

```
from langchain_text_splitters import RecursiveCharacterTextSplitter, Language

PYTHON_CODE = """
def add(a, b):
    return a + b

class Calculator:
    def __init__(self):
        self.result = 0

    def add(self, value):
        self.result += value
        return self.result

    def subtract(self, value):
        self.result -= value
        return self.result

# 调用函数
def main():
    calc = Calculator()
    print(calc.add(5))
    print(calc.subtract(2))

if __name__ == "__main__":
    main()
"""

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON, chunk_size=100, chunk_overlap=0)

python_docs = python_splitter.create_documents([PYTHON_CODE])
python_docs
```

_如果你不确定哪种分割技术最适合你的 RAG 应用程序，可以选择递归字符文本分割器技术。它作为通用的默认选项，也可以执行专门的分割器，如 MarkdownHeaderTextSplitter、PythonCodeTextSplitter 等，它们为特定的文档格式提供解决方案。_