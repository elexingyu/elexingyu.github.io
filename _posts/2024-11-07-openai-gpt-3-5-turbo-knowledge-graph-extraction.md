---
categories: articles
date: 2024-11-07
layout: post
style: huoshui
tags:
- AI
- 知识图谱
- 教程
title: 构建知识图谱新突破：OpenAI GPT-3.5-turbo高效提取实体关系
---

本文将探讨如何使用 OpenAI 的 gpt-3.5-turbo 从原始文本数据构建知识图谱。大语言模型（LLM）在文本生成和问答任务中表现优异。检索增强生成（RAG）进一步提升了它们的性能，使其能够访问最新的领域特定知识。本文的目标是利用大语言模型作为信息提取工具，将原始文本转换为可查询的事实，从而获取有用的见解。但在此之前，我们需要定义一些关键概念。

## 什么是知识图谱？

知识图谱是一个语义网络，它表示并关联现实世界中的实体。这些实体通常对应于人物、组织、物体、事件和概念。知识图谱由以下结构的三元组组成：

**头实体 → 关系 → 尾实体**

或者在语义网的术语中：

**主语 → 谓语 → 宾语**

这种网络表示法使我们能够提取并分析这些实体之间存在的复杂关系。

知识图谱通常伴随概念、关系及其属性的定义——即**本体**。本体是一种正式规范，它在目标领域中定义了概念及其关系，从而为网络提供了语义。

搜索引擎和其他网络上的自动化智能体使用本体来理解特定网页的内容，以便对其进行索引并正确显示。

## 案例描述

在这个用例中，我们将使用 OpenAI 的 gpt-3.5-turbo 从 Amazon 产品数据集中提取的产品描述创建一个知识图谱。

在网络上有许多用于描述产品的本体，其中最流行的是 Good Relations 本体和 Product Types 本体。这两个本体都扩展了 Schema.org 本体。

Schema.org 是一个协作的社区活动，旨在创建、维护和推广用于互联网结构化数据的模式。Schema.org 的词汇可以与多种不同的编码一起使用，包括 RDFa、Microdata 和 JSON-LD。

在当前任务中，我们将使用 Schema.org 中关于产品及相关概念的定义，包括它们的关系，从产品描述中提取三元组。

## 实现

我们将使用 Python 来实现该解决方案。首先，我们需要安装并导入所需的库。

## 导入库并读取数据

```
!pip install pandas openai sentence-transformers networkx
```

```
import json
import logging
import matplotlib.pyplot as plt
import networkx as nx
from networkx import connected_components
from openai import OpenAI
import pandas as pd
from sentence_transformers import SentenceTransformer, util
```

现在，我们将 Amazon 产品数据集读取为 pandas 数据框。

```
data = pd.read_csv("amazon_products.csv")
```

我们可以在下图中看到数据集的内容。数据集包含以下列：“PRODUCT_ID”、“TITLE”、“BULLET_POINTS”、“DESCRIPTION”、“PRODUCT_TYPE_ID”和“PRODUCT_LENGTH”。我们将把“TITLE”、“BULLET_POINTS”和“DESCRIPTION”列组合成一个名为“text”的列，该列将代表我们将提示 ChatGPT 从中提取实体和关系的产品规格。

![图 1. 数据集内容](https://miro.medium.com/v2/resize:fit:1400/1*yf1SjWjsBb1VexzETOt0EA.png)


```
data['text'] = data['TITLE'] + data['BULLET_POINTS'] + data['DESCRIPTION']
```

## 信息提取

我们将指示 ChatGPT 从提供的产品规格中提取实体和关系，并将结果返回为 JSON 对象数组。JSON 对象必须包含以下键：“head”、“head_type”、“relation”、“tail”和“tail_type”。

“head”键必须包含从用户提示词提供的列表中提取的实体文本。“head_type”键必须包含提取的头实体的类型，该类型必须是用户列表中的一种。“relation”键必须包含头实体和尾实体之间关系的类型，“tail”键必须表示三元组中的宾语实体的文本，而“tail_type”键必须包含尾实体的类型。

我们将使用以下列出的实体类型和关系类型提示 ChatGPT 进行实体关系提取。我们会将这些实体和关系映射到 Schema.org 本体中的对应实体和关系。映射中的键表示提供给 ChatGPT 的实体和关系类型，值表示 Schema.org 中对象和属性的 URL。

```
# ENTITY TYPES:
entity_types = {
  "product": "https://schema.org/Product", 
  "rating": "https://schema.org/AggregateRating",
  "price": "https://schema.org/Offer", 
  "characteristic": "https://schema.org/PropertyValue", 
  "material": "https://schema.org/Text",
  "manufacturer": "https://schema.org/Organization", 
  "brand": "https://schema.org/Brand", 
  "measurement": "https://schema.org/QuantitativeValue", 
  "organization": "https://schema.org/Organization",  
  "color": "https://schema.org/Text",
}

# RELATION TYPES:
relation_types = {
  "hasCharacteristic": "https://schema.org/additionalProperty",
  "hasColor": "https://schema.org/color", 
  "hasBrand": "https://schema.org/brand", 
  "isProducedBy": "https://schema.org/manufacturer", 
  "hasColor": "https://schema.org/color",
  "hasMeasurement": "https://schema.org/hasMeasurement", 
  "isSimilarTo": "https://schema.org/isSimilarTo", 
  "madeOfMaterial": "https://schema.org/material", 
  "hasPrice": "https://schema.org/offers", 
  "hasRating": "https://schema.org/aggregateRating", 
  "relatedTo": "https://schema.org/isRelatedTo"
 }
```

为了使用 ChatGPT 进行信息提取，我们创建了一个 OpenAI 客户端，并使用聊天完成 API 为每个从原始产品规格中识别的关系生成 JSON 对象数组。默认模型选择 gpt-3.5-turbo，因为它的性能足以用于此简单演示。

```
client = OpenAI(api_key="<YOUR_API_KEY>")
```

```
def extract_information(text, model="gpt-3.5-turbo"):
   completion = client.chat.completions.create(
        model=model,
        temperature=0,
        messages=[
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt.format(
              entity_types=entity_types,
              relation_types=relation_types,
              specification=text
            )
        }
        ]
    )

   return completion.choices[0].message.content
```

## 提示词设计

system_prompt 变量包含指导 ChatGPT 从原始文本中提取实体和关系的指令，并以 JSON 对象数组的形式返回结果，每个对象包含以下键：“head”、“head_type”、“relation”、“tail”和“tail_type”。

```
system_prompt = """You are an expert agent specialized in analyzing product specifications in an online retail store.
Your task is to identify the entities and relations requested with the user prompt, from a given product specification.
You must generate the output in a JSON containing a list with JOSN objects having the following keys: "head", "head_type", "relation", "tail", and "tail_type".
The "head" key must contain the text of the extracted entity with one of the types from the provided list in the user prompt, the "head_type"
key must contain the type of the extracted head entity which must be one of the types from the provided user list,
the "relation" key must contain the type of relation between the "head" and the "tail", the "tail" key must represent the text of an
extracted entity which is the tail of the relation, and the "tail_type" key must contain the type of the tail entity. Attempt to extract as
many entities and relations as you can.
"""
```

user_prompt 变量包含数据集中单个规格的示例输出，并提示 ChatGPT 以相同方式从提供的规格中提取实体和关系。这是 ChatGPT 单样本学习的一个示例。

```
user_prompt = """Based on the following example, extract entities and relations from the provided text.
Use the following entity types:

# ENTITY TYPES:
{entity_types}

Use the following relation types:
{relation_types}

--> Beginning of example

# Specification
"YUVORA 3D Brick Wall Stickers | PE Foam Fancy Wallpaper for Walls,
 Waterproof & Self Adhesive, White Color 3D Latest Unique Design Wallpaper for Home (70*70 CMT) -40 Tiles
 [Made of soft PE foam,Anti Children's Collision,take care of your family.Waterproof, moist-proof and sound insulated. Easy clean and maintenance with wet cloth,economic wall covering material.,Self adhesive peel and stick wallpaper,Easy paste And removement .Easy To cut DIY the shape according to your room area,The embossed 3d wall sticker offers stunning visual impact. the tiles are light, water proof, anti-collision, they can be installed in minutes over a clean and sleek surface without any mess or specialized tools, and never crack with time.,Peel and stick 3d wallpaper is also an economic wall covering material, they will remain on your walls for as long as you wish them to be. The tiles can also be easily installed directly over existing panels or smooth surface.,Usage range: Featured walls,Kitchen,bedroom,living room, dinning room,TV walls,sofa background,office wall decoration,etc. Don't use in shower and rugged wall surface]
Provide high quality foam 3D wall panels self adhesive peel and stick wallpaper, made of soft PE foam,children's collision, waterproof, moist-proof and sound insulated,easy cleaning and maintenance with wet cloth,economic wall covering material, the material of 3D foam wallpaper is SAFE, easy to paste and remove . Easy to cut DIY the shape according to your decor area. Offers best quality products. This wallpaper we are is a real wallpaper with factory done self adhesive backing. You would be glad that you it. Product features High-density foaming technology Total Three production processes Can be use of up to 10 years Surface Treatment: 3D Deep Embossing Damask Pattern."

################

# Output
[
  {{
    "head": "YUVORA 3D Brick Wall Stickers",
    "head_type": "product",
    "relation": "isProducedBy",
    "tail": "YUVORA",
    "tail_type": "manufacturer"
  }},
  {{
    "head": "YUVORA 3D Brick Wall Stickers",
    "head_type": "product",
    "relation": "hasCharacteristic",
    "tail": "Waterproof",
    "tail_type": "characteristic"
  }},
  {{
    "head": "YUVORA 3D Brick Wall Stickers",
    "head_type": "product",
    "relation": "hasCharacteristic",
    "tail": "Self Adhesive",
    "tail_type": "characteristic"
  }},
  {{
    "head": "YUVORA 3D Brick Wall Stickers",
    "head_type": "product",
    "relation": "hasColor",
    "tail": "White",
    "tail_type": "color"
  }},
  {{
    "head": "YUVORA 3D Brick Wall Stickers",
    "head_type": "product",
    "relation": "hasMeasurement",
    "tail": "70*70 CMT",
    "tail_type": "measurement"
  }},
  {{
    "head": "YUVORA 3D Brick Wall Stickers",
    "head_type": "product",
    "relation": "hasMeasurement",
    "tail": "40 tiles",
    "tail_type": "measurement"
  }},
  {{
    "head": "YUVORA 3D Brick Wall Stickers",
    "head_type": "product",
    "relation": "hasMeasurement",
    "tail": "40 tiles",
    "tail_type": "measurement"
  }}
]

--> End of example

For the following specification, generate extract entitites and relations as in the provided example.

# Specification
{specification}
################

# Output

"""
```

现在，我们为数据集中的每个规格调用 extract_information 函数，并创建所有提取的三元组的列表，这些三元组将代表我们的知识图谱。为了演示，我们将使用 100 个产品规格的子集生成知识图谱。

```
kg = []
for content in data['text'].values[:100]:
  try:
    extracted_relations = extract_information(content)
    extracted_relations = json.loads(extracted_relations)
    kg.extend(extracted_relations)
  except Exception as e:
    logging.error(e)

kg_relations = pd.DataFrame(kg)
```

信息提取的结果显示在下图中。

![图 2. ChatGPT 信息提取结果](https://miro.medium.com/v2/resize:fit:1400/1*nWqw6rBA0KRfkgt-_Pojlg.png)



## 实体解析

实体解析（ER）是消除与现实世界概念相对应的实体歧义的过程。在本例中，我们将尝试对数据集中的头实体和尾实体进行基础的实体解析。这样做的原因是为了更简洁地表示文本中的事实。

我们将使用 NLP 技术进行实体解析，具体来说，我们将使用 sentence-transformers 库为每个头实体创建嵌入，并计算头实体之间的余弦相似度。

我们将使用“all-MiniLM-L6-v2”句子转换器创建嵌入，因为它是一个快速且相对准确的模型，适合此用例。对于每对头实体，如果相似度大于 0.95，我们将认为这些实体是相同的，并将它们的文本值标准化为相同。尾实体也适用相同的逻辑。

通过这种方式，如果我们有两个实体，一个是“Microsoft”，另一个是“Microsoft Inc.”，那么这两个实体将被合并为一个。

我们以如下方式加载并使用嵌入模型来计算第一个和第二个头实体之间的相似度。

```
heads = kg_relations['head'].values
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = embedding_model.encode(heads)
similarity = util.cos_sim(embeddings[0], embeddings[1])
```

为了在实体解析后可视化提取的知识图谱，我们使用了 Python 的 networkx 库。首先，我们创建一个空图，并将每个提取的关系添加到图中。

```
G = nx.Graph()
for _, row in kg_relations.iterrows():
  G.add_edge(row['head'], row['tail'], label=row['relation'])
```

要绘制图形，我们可以使用以下代码：

```
pos = nx.spring_layout(G, seed=47, k=0.9)
labels = nx.get_edge_attributes(G, 'label')
plt.figure(figsize=(15, 15))
nx.draw(G, pos, with_labels=True, font_size=10, node_size=700, node_color='lightblue', edge_color='gray', alpha=0.6)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8, label_pos=0.3, verticalalignment='baseline')
plt.title('Product Knowledge Graph')
plt.show()
```

生成的知识图谱的子图显示在下图中：

![图 3. 产品知识图谱示例](https://miro.medium.com/v2/resize:fit:1100/format:webp/1*Z71iLSSBFE-q3c8t2auXxg.png)


我们可以看到，通过这种方式，我们可以根据产品共享的特征连接多个不同的产品。这对于学习产品之间的共同属性、规范化产品规格、使用 Schema.org 等通用模式描述网络资源，甚至基于产品规格进行产品推荐非常有用。

## 结论

大多数公司都有大量未使用的非结构化数据存储在数据湖中。通过创建知识图谱从这些未使用的数据中提取见解的做法，将有助于获取那些被困在未处理和非结构化文本语料库中的信息，并利用这些信息做出更明智的决策。

到目前为止，我们已经看到，LLM 可以用于从原始文本数据中提取实体和关系三元组，并自动构建知识图谱。在下一篇文章中，我们将尝试基于提取的知识图谱创建一个产品推荐系统。