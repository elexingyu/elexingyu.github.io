---
categories: articles
date: '2024-10-24'
layout: post
style: huoshui
tags:
- AI
- 知识图谱
- 教程
title: LLM图建模挑战：大语言模型如何绘制数据图谱？
---

![图模型展示了 Tracks 与 Artists 之间的 PERFORMED_BY 关系。照片由作者提供。](https://cdn-images-1.medium.com/max/1000/0*sRaVx5ZOjvNZojLB.png)

**当大语言模型 (LLM) 尝试从平面 CSV 文件创建图时表现如何？**

我的工作中很大一部分是改善用户使用 Neo4j 的体验。通常，如何将数据导入 Neo4j 并有效建模是用户面临的主要挑战，尤其是在初期阶段。尽管初始的数据模型很重要并且需要深思熟虑，但随着数据规模或用户数量的增长，它可以轻松地重构以提高性能。

因此，作为对自己的挑战，我想看看 LLM 是否能够帮助进行初始数据模型的创建。即使不能，它至少可以展示事物之间的连接，并为用户提供一些可以快速展示给他人的结果。

直觉上，我知道数据建模是一个迭代的过程，某些 LLM 在处理大量数据时容易分心，因此这是一个使用 LangGraph 通过数据循环工作的好机会。

让我们深入了解使其实现的提示词。

## 图建模基础

GraphAcademy 上的图数据建模基础课程引导你了解如何在图中建模数据的基础知识，但作为初步尝试，我使用了以下经验法则：

- 名词变成标签——它们描述节点所代表的事物。
- 动词变成关系类型——它们描述事物之间的连接方式。
- 其他内容变成属性（尤其是副词）——你有一个名字，并且可能驾驶一辆灰色的车。

动词也可以是节点；你可能很高兴知道某个人订购了某个产品，但这个基本模型并不能让你知道产品是在哪里和什么时候订购的。在这种情况下，订单成为模型中的一个新节点。

我确信这可以被提炼成一个提示词，以创建一种零样本学习的图数据建模方法。

## 迭代方法

几个月前我简要尝试过这个方法，发现我使用的模型在处理较大模式时容易分心，提示词很快达到了 LLM 的 Token 限制。

这次我决定尝试一种迭代方法，一次只处理一个键。这应该有助于避免分心，因为 LLM 只需要一次考虑一项内容。

最终的方法使用了以下步骤：

1. 将 CSV 文件加载到 Pandas 数据框中。
2. 分析 CSV 中的每一列，并将其附加到一个基于 JSON Schema 的数据模型中。
3. 为每个实体识别并添加缺失的唯一 ID。
4. 审查数据模型的准确性。
5. 生成导入节点和关系的 Cypher 语句。
6. 生成支持导入语句的唯一约束。
7. 创建约束并运行导入。

## 数据

我在 Kaggle 上快速浏览了一下，寻找一个有趣的数据集。脱颖而出的是 Spotify 最多播放的歌曲数据集。

```
import pandas as pd

csv_file = '/Users/adam/projects/datamodeller/data/spotify/spotify-most-streamed-songs.csv'

df = pd.read_csv(csv_file)
df.head()


track_name artist(s)_name artist_count released_year released_month released_day in_spotify_playlists in_spotify_charts streams in_apple_playlists … key mode danceability_% valence_% energy_% acousticness_% instrumentalness_% liveness_% speechiness_% cover_url
0 Seven (feat. Latto) (Explicit Ver.) Latto, Jung Kook 2 2023 7 14 553 147 141381703 43 … B Major 80 89 83 31 0 8 4 Not Found
1 LALA Myke Towers 1 2023 3 23 1474 48 133716286 48 … C# Major 71 61 74 7 0 10 4 https://i.scdn.co/image/ab67616d0000b2730656d5…
2 vampire Olivia Rodrigo 1 2023 6 30 1397 113 140003974 94 … F Major 51 32 53 17 0 31 6 https://i.scdn.co/image/ab67616d0000b273e85259…
3 Cruel Summer Taylor Swift 1 2019 8 23 7858 100 800840817 116 … A Major 55 58 72 11 0 11 15 https://i.scdn.co/image/ab67616d0000b273e787cf…
4 WHERE SHE GOES Bad Bunny 1 2023 5 18 3133 50 303236322 84 … A Minor 65 23 80 14 63 11 6 https://i.scdn.co/image/ab67616d0000b273ab5c9c…
```

这个数据集相对简单，但我马上就能看出应该存在曲目和艺术家之间的关系。

同时，还需要克服数据清理方面的挑战，尤其是列名和艺术家名称列中的艺术家是以逗号分隔的值。

## 选择 LLM

我真的很想使用本地 LLM，但我很快发现 Llama 3 无法胜任。如果有疑问，退回到 OpenAI：

```
from langchain_core.prompts import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
from langchain_core.output_parsers import JsonOutputParser

from langchain_openai import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o")
```

## 创建数据模型

我使用了一组简化的建模说明来创建数据建模提示词。我不得不多次调整提示词以获得一致的输出。

零样本学习的例子效果相对较好，但我发现输出不一致。定义一个结构化的输出来保存 JSON 输出确实有帮助：

```
class JSONSchemaSpecification(BaseModel):
  notes: str = Field(description="Any notes or comments about the schema")
  jsonschema: str = Field(description="A JSON array of JSON schema specifications that describe the entities in the data model")
```

## 少样本学习示例输出

JSON 本身也不一致，所以我最终基于电影推荐数据集定义了一个模式。

示例输出：

```
example_output = [
   dict(
    title="Person",
    type="object",
    description="Node",
    properties=[
        dict(name="name", column_name="person_name", type="string", description="The name of the person", examples=["Tom Hanks"]),
        dict(name="date_of_birth", column_name="person_dob", type="date", description="The date of birth for the person", examples=["1987-06-05"]),
        dict(name="id", column_name="person_name, date_of_birth", type="string", description="The ID is a combination of name and date of birth to ensure uniqueness", examples=["tom-hanks-1987-06-05"]),
    ],
  ),
   dict(
    title="Director",
    type="object",
    description="Node",
    properties=[
        dict(name="name", column_name="director_names", type="string", description="The name of the directors. Split values in column by a comma", examples=["Francis Ford Coppola"]),
    ],
  ),
   dict(
    title="Movie",
    type="object",
    description="Node",
    properties=[
        dict(name="title", column_name="title", type="string", description="The title of the movie", examples=["Toy Story"]),
        dict(name="released", column_name="released", type="integer", description="The year the movie was released", examples=["1990"]),
    ],
  ),
   dict(
    title="ACTED_IN",
    type="object",
    description="Relationship",
    properties=[
        dict(name="_from", column_name="od", type="string", description="Person found by the `id`.  The ID is a combination of name and date of birth to ensure uniqueness", examples=["Person"]),
        dict(name="_to", column_name="title", type="string", description="The movie title", examples=["Movie"]),
        dict(name="roles", type="string", column_name="person_roles", description="The roles the person played in the movie", examples=["Woody"]),
    ],
  ),
   dict(
    title="DIRECTED",
    type="object",
    description="Relationship",
    properties=[
        dict(name="_from", type="string", column_name="director_names", description="Director names are comma separated", examples=["Director"]),
        dict(name="_to", type="string", column_name="title", description="The label of the node this relationship ends at", examples=["Movie"]),
    ],
  ),
]
```

我不得不偏离严格的 JSON Schema，并在输出中添加 column_name 字段，以帮助 LLM 生成导入脚本。提供描述的示例在这方面也有帮助，否则在 MATCH 子句中使用的属性会不一致。

## 链式操作

这是最终的提示词：

```
model_prompt = PromptTemplate.from_template("""
You are an expert Graph Database administrator.
Your task is to design a data model based on the information provided from an existing data source.

You must decide where the following column fits in with the existing data model.  Consider:
* Does the column represent an entity, for example a Person, Place, or Movie?  If so, this should be a node in its own right.
* Does the column represent a relationship between two entities?  If so, this should be a relationship between two nodes.
* Does the column represent an attribute of an entity or relationship?  If so, this should be a property of a node or relationship.
* Does the column represent a shared attribute that could be interesting to query through to find similar nodes, for example a Genre?  If so, this should be a node in its own right.


## Instructions for Nodes

* Node labels are generally nouns, for example Person, Place, or Movie
* Node titles should be in UpperCamelCase

## Instructions for Relationships

* Relationshops are generally verbs, for example ACTED_IN, DIRECTED, or PURCHASED
* Examples of good relationships are (:Person)-[:ACTED_IN]->(:Movie) or (:Person)-[:PURCHASED]->(:Product)
* Relationships should be in UPPER_SNAKE_CASE
* Provide any specific instructions for the field in the description.  For example, does the field contain a list of comma separated values or a single value?

## Instructions for Properties

* Relationships should be in lowerPascalCase
* Prefer the shorter name where possible, for example "person_id" and "personId" should simply be "id"
* If you are changing the property name from the original field name, mention the column name in the description
* Do not include examples for integer or date fields
* Always include instructions on data preparation for the field.  Does it need to be cast as a string or split into multiple fields on a delimiting value?
* Property keys should be letters only, no numbers or special characters.

## Important!

Consider the examples provided.  Does any data preparation need to be done to ensure the data is in the correct format?
You must include any information about data preparation in the description.

## Example Output

Here is an example of a good output:
'''
{example_output}
'''

## New Data:

Key: {key}
Data Type: {type}
Example Values: {examples}

## Existing Data Model

Here is the existing data model:
'''
{existing_model}
'''

## Keep Existing Data Model

Apply your changes to the existing data model but never remove any existing definitions.
""", partial_variables=dict(example_output=dumps(example_output)))

model_chain = model_prompt | llm.with_structured_output(JSONSchemaSpecification)
```

## 执行链式操作

为了迭代更新模型，我遍历数据框中的键，并将每个键、其数据类型及前五个唯一值传递给提示词：

```
from json_repair import dumps, loads

existing_model = {}

for i, key in enumerate(df):
  print("\n", i, key)
  print("----------------")
  try:
    res = try_chain(model_chain, dict(
      existing_model=dumps(existing_model),
      key=key,
      type=df[key].dtype,
      examples=dumps(df[key].unique()[:5].tolist())
    ))
    print(res.notes)
    existing_model = loads(res.jsonschema)

    print([n['title'] for n in existing_model])
  except Exception as e:
    print(e)
    pass

existing_model
```

控制台输出：

```
 0 track_name
----------------
Adding 'track_name' to an existing data model. This represents a music track entity.
['Track']

  1 artist(s)_name
----------------
Adding a new column 'artist(s)_name' to the existing data model. This column represents multiple artists associated with tracks and should be modeled as a new node 'Artist' and a relationship 'PERFORMED_BY' from 'Track' to 'Artist'.
['Track', 'Artist', 'PERFORMED_BY']

  2 artist_count
----------------
Added artist_count as a property of Track node. This property indicates the number of artists performing in the track.
['Track', 'Artist', 'PERFORMED_BY']

  3 released_year
----------------
Add the released_year column to the existing data model as a property of the Track node.
['Track', 'Artist', 'PERFORMED_BY']

  4 released_month
----------------
Adding the 'released_month' column to the existing data model, considering it as an attribute of the Track node.
['Track', 'Artist', 'PERFORMED_BY']

  5 released_day
----------------
Added a new property 'released_day' to the 'Track' node to capture the day of the month a track was released.
['Track', 'Artist', 'PERFORMED_BY']

  6 in_spotify_playlists
----------------
Adding the new column 'in_spotify_playlists' to the existing data model as a property of the 'Track' node.
['Track', 'Artist', 'PERFORMED_BY']

  7 in_spotify_charts
----------------
Adding the 'in_spotify_charts' column to the existing data model as a property of the Track node.
['Track', 'Artist', 'PERFORMED_BY']

  8 streams
----------------
Adding a new column 'streams' to the existing data model, representing the number of streams for a track.
['Track', 'Artist', 'PERFORMED_BY']

  9 in_apple_playlists
----------------
Adding new column 'in_apple_playlists' to the existing data model
['Track', 'Artist', 'PERFORMED_BY']

  10 in_apple_charts
----------------
Adding 'in_apple_charts' as a property to the 'Track' node, representing the number of times the track appeared in the Apple charts.
['Track', 'Artist', 'PERFORMED_BY']

  11 in_deezer_playlists
----------------
Add 'in_deezer_playlists' to the existing data model for a music track database.
['Track', 'Artist', 'PERFORMED_BY']

  12 in_deezer_charts
----------------
Adding a new property 'inDeezerCharts' to the existing 'Track' node to represent the number of times the track appeared in Deezer charts.
['Track', 'Artist', 'PERFORMED_BY']

  13 in_shazam_charts
----------------
Adding new data 'in_shazam_charts' to the existing data model. This appears to be an attribute of the 'Track' node, indicating the number of times a track appeared in the Shazam charts.
['Track', 'Artist', 'PERFORMED_BY']

  14 bpm
----------------
Added bpm column as a property to the Track node as it represents a characteristic of the track.
['Track', 'Artist', 'PERFORMED_BY']

  15 key
----------------
Adding the 'key' column to the existing data model. The 'key' represents the musical key of a track, which is a shared attribute that can be interesting to query through to find similar tracks.
['Track', 'Artist', 'PERFORMED_BY']

  16 mode
----------------
Adding 'mode' to the existing data model. It represents a musical characteristic of a track, which is best captured as an attribute of the Track node.
['Track', 'Artist', 'PERFORMED_BY']

  17 danceability_%
----------------
Added 'danceability_%' to the existing data model as a property of the Track node. The field represents the danceability percentage of the track.
['Track', 'Artist', 'PERFORMED_BY']

  18 valence_%
----------------
Adding the valence percentage column to the existing data model as a property of the Track node.
['Track', 'Artist', 'PERFORMED_BY']

  19 energy_%
----------------
Integration of the new column 'energy_%' into the existing data model. This column represents an attribute of the Track entity and should be added as a property of the Track node.
['Track', 'Artist', 'PERFORMED_BY']

  20 acousticness_%
----------------
Adding acousticness_% to the existing data model as a property of the Track node.
['Track', 'Artist', 'PERFORMED_BY']

  21 instrumentalness_%
----------------
Adding the new column 'instrumentalness_%' to the existing Track node as it represents an attribute of the Track entity.
['Track', 'Artist', 'PERFORMED_BY']

  22 liveness_%
----------------
Adding the new column 'liveness_%' to the existing data model as an attribute of the Track node
['Track', 'Artist', 'PERFORMED_BY']

  23 speechiness_%
----------------
Adding the new column 'speechiness_%' to the existing data model as a property of the 'Track' node.
['Track', 'Artist', 'PERFORMED_BY']

  24 cover_url
----------------
Adding a new property 'cover_url' to the existing 'Track' node. This property represents the URL of the track's cover image.
['Track', 'Artist', 'PERFORMED_BY']
```

在对提示词进行了一些调整以处理用例后，我得到了一个我相当满意的模型。LLM 成功确定了数据集由 Track、Artist 以及连接两者的 PERFORMED_BY 关系组成：

```
[
  {
    "title": "Track",
    "type": "object",
    "description": "Node",
    "properties": [
      {
        "name": "name",
        "column_name": "track_name",
        "type": "string",
        "description": "The name of the track",
        "examples": [
          "Seven (feat. Latto) (Explicit Ver.)",
          "LALA",
          "vampire",
          "Cruel Summer",
          "WHERE SHE GOES",
        ],
      },
      {
        "name": "artist_count",
        "column_name": "artist_count",
        "type": "integer",
        "description": "The number of artists performing in the track",
        "examples": [2, 1, 3, 8, 4],
      },
      {
        "name": "released_year",
        "column_name": "released_year",
        "type": "integer",
        "description": "The year the track was released",
        "examples": [2023, 2019, 2022, 2013, 2014],
      },
      {
        "name": "released_month",
        "column_name": "released_month",
        "type": "integer",
        "description": "The month the track was released",
        "examples": [7, 3, 6, 8, 5],
      },
      {
        "name": "released_day",
        "column_name": "released_day",
        "type": "integer",
        "description": "The day of the month the track was released",
        "examples": [14, 23, 30, 18, 1],
      },
      {
        "name": "inSpotifyPlaylists",
        "column_name": "in_spotify_playlists",
        "type": "integer",
        "description": "The number of Spotify playlists the track is in. Cast the value as an integer.",
        "examples": [553, 1474, 1397, 7858, 3133],
      },
      {
        "name": "inSpotifyCharts",
        "column_name": "in_spotify_charts",
        "type": "integer",
        "description": "The number of times the track appeared in the Spotify charts. Cast the value as an integer.",
        "examples": [147, 48, 113, 100, 50],
      },
      {
        "name": "streams",
        "column_name": "streams",
        "type": "array",
        "description": "The list of stream IDs for the track. Maintain the array format.",
        "examples": [
          "141381703",
          "133716286",
          "140003974",
          "800840817",
          "303236322",
        ],
      },
      {
        "name": "inApplePlaylists",
        "column_name": "in_apple_playlists",
        "type": "integer",
        "description": "The number of Apple playlists the track is in. Cast the value as an integer.",
        "examples": [43, 48, 94, 116, 84],
      },
      {
        "name": "inAppleCharts",
        "column_name": "in_apple_charts",
        "type": "integer",
        "description": "The number of times the track appeared in the Apple charts. Cast the value as an integer.",
        "examples": [263, 126, 207, 133, 213],
      },
      {
        "name": "inDeezerPlaylists",
        "column_name": "in_deezer_playlists",
        "type": "array",
        "description": "The list of Deezer playlist IDs the track is in. Maintain the array format.",
        "examples": ["45", "58", "91", "125", "87"],
      },
      {
        "name": "inDeezerCharts",
        "column_name": "in_deezer_charts",
        "type": "integer",
        "description": "The number of times the track appeared in the Deezer charts. Cast the value as an integer.",
        "examples": [10, 14, 12, 15, 17],
      },
      {
        "name": "inShazamCharts",
        "column_name": "in_shazam_charts",
        "type": "array",
        "description": "The list of Shazam chart IDs the track is in. Maintain the array format.",
        "examples": ["826", "382", "949", "548", "425"],
      },
      {
        "name": "bpm",
        "column_name": "bpm",
        "type": "integer",
        "description": "The beats per minute of the track. Cast the value as an integer.",
        "examples": [125, 92, 138, 170, 144],
      },
      {
        "name": "key",
        "column_name": "key",
        "type": "string",
        "description": "The musical key of the track. Cast the value as a string.",
        "examples": ["B", "C#", "F", "A", "D"],
      },
      {
        "name": "mode",
        "column_name": "mode",
        "type": "string",
        "description": "The mode of the track (e.g., Major, Minor). Cast the value as a string.",
        "examples": ["Major", "Minor"],
      },
      {
        "name": "danceability",
        "column_name": "danceability_%",
        "type": "integer",
        "description": "The danceability percentage of the track. Cast the value as an integer.",
        "examples": [80, 71, 51, 55, 65],
      },
      {
        "name": "valence",
        "column_name": "valence_%",
        "type": "integer",
        "description": "The valence percentage of the track. Cast the value as an integer.",
        "examples": [89, 61, 32, 58, 23],
      },
      {
        "name": "energy",
        "column_name": "energy_%",
        "type": "integer",
        "description": "The energy percentage of the track. Cast the value as an integer.",
        "examples": [83, 74, 53, 72, 80],
      },
      {
        "name": "acousticness",
        "column_name": "acousticness_%",
        "type": "integer",
        "description": "The acousticness percentage of the track. Cast the value as an integer.",
        "examples": [31, 7, 17, 11, 14],
      },
      {
        "name": "instrumentalness",
        "column_name": "instrumentalness_%",
        "type": "integer",
        "description": "The instrumentalness percentage of the track. Cast the value as an integer.",
        "examples": [0, 63, 17, 2, 19],
      },
      {
        "name": "liveness",
        "column_name": "liveness_%",
        "type": "integer",
        "description": "The liveness percentage of the track. Cast the value as an integer.",
        "examples": [8, 10, 31, 11, 28],
      },
      {
        "name": "speechiness",
        "column_name": "speechiness_%",
        "type": "integer",
        "description": "The speechiness percentage of the track. Cast the value as an integer.",
        "examples": [4, 6, 15, 24, 3],
      },
      {
        "name": "coverUrl",
        "column_name": "cover_url",
        "type": "string",
        "description": "The URL of the track's cover image. If the value is 'Not Found', it should be cast as an empty string.",
        "examples": [
          "https://i.scdn.co/image/ab67616d0000b2730656d5ce813ca3cc4b677e05",
          "https://i.scdn.co/image/ab67616d0000b273e85259a1cae29a8d91f2093d",
        ],
      },
    ],
  },
  {
    "title": "Artist",
    "type": "object",
    "description": "Node",
    "properties": [
      {
        "name": "name",
        "column_name": "artist(s)_name",
        "type": "string",
        "description": "The name of the artist. Split values in column by a comma",
        "examples": [
          "Latto",
          "Jung Kook",
          "Myke Towers",
          "Olivia Rodrigo",
          "Taylor Swift",
          "Bad Bunny",
        ],
      }
    ],
  },
  {
    "title": "PERFORMED_BY",
    "type": "object",
    "description": "Relationship",
    "properties": [
      {
        "name": "_from",
        "type": "string",
        "description": "The label of the node this relationship starts at",
        "examples": ["Track"],
      },
      {
        "name": "_to",
        "type": "string",
        "description": "The label of the node this relationship ends at",
        "examples": ["Artist"],
      },
    ],
  },
]

[
  {
    "title": "Track",
    "type": "object",
    "description": "Node",
    "properties": [
      {
        "name": "name",
        "column_name": "track_name",
        "type": "string",
        "description": "The name of the track",
        "examples": [
          "Seven (feat. Latto) (Explicit Ver.)",
          "LALA",
          "vampire",
          "Cruel Summer",
          "WHERE SHE GOES",
        ],
      },
      {
        "name": "artist_count",
        "column_name": "artist_count",
        "type": "integer",
        "description": "The number of artists performing in the track",
        "examples": [2, 1, 3, 8, 4],
      },
      {
        "name": "released_year",
        "column_name": "released_year",
        "type": "integer",
        "description": "The year the track was released",
        "examples": [2023, 2019, 2022, 2013, 2014],
      },
      {
        "name": "released_month",
        "column_name": "released_month",
        "type": "integer",
        "description": "The month the track was released",
        "examples": [7, 3, 6, 8, 5],
      },
      {
        "name": "released_day",
        "column_name": "released_day",
        "type": "integer",
        "description": "The day of the month the track was released",
        "examples": [14, 23, 30, 18, 1],
      },
      {
        "name": "inSpotifyPlaylists",
        "column_name": "in_spotify_playlists",
        "type": "integer",
        "description": "The number of Spotify playlists the track is in. Cast the value as an integer.",
        "examples": [553, 1474, 1397, 7858, 3133],
      },
      {
        "name": "inSpotifyCharts",
        "column_name": "in_spotify_charts",
        "type": "integer",
        "description": "The number of times the track appeared in the Spotify charts. Cast the value as an integer.",
        "examples": [147, 48, 113, 100, 50],
      },
      {
        "name": "streams",
        "column_name": "streams",
        "type": "array",
        "description": "The list of stream IDs for the track. Maintain the array format.",
        "examples": [
          "141381703",
          "133716286",
          "140003974",
          "800840817",
          "303236322",
        ],
      },
      {
        "name": "inApplePlaylists",
        "column_name": "in_apple_playlists",
        "type": "integer",
        "description": "The number of Apple playlists the track is in. Cast the value as an integer.",
        "examples": [43, 48, 94, 116, 84],
      },
      {
        "name": "inAppleCharts",
        "column_name": "in_apple_charts",
        "type": "integer",
        "description": "The number of times the track appeared in the Apple charts. Cast the value as an integer.",
        "examples": [263, 126, 207, 133, 213],
      },
      {
        "name": "inDeezerPlaylists",
        "column_name": "in_deezer_playlists",
        "type": "array",
        "description": "The list of Deezer playlist IDs the track is in. Maintain the array format.",
        "examples": ["45", "58", "91", "125", "87"],
      },
      {
        "name": "inDeezerCharts",
        "column_name": "in_deezer_charts",
        "type": "integer",
        "description": "The number of times the track appeared in the Deezer charts. Cast the value as an integer.",
        "examples": [10, 14, 12, 15, 17],
      },
      {
        "name": "inShazamCharts",
        "column_name": "in_shazam_charts",
        "type": "array",
        "description": "The list of Shazam chart IDs the track is in. Maintain the array format.",
        "examples": ["826", "382", "949", "548", "425"],
      },
      {
        "name": "bpm",
        "column_name": "bpm",
        "type": "integer",
        "description": "The beats per minute of the track. Cast the value as an integer.",
        "examples": [125, 92, 138, 170, 144],
      },
      {
        "name": "key",
        "column_name": "key",
        "type": "string",
        "description": "The musical key of the track. Cast the value as a string.",
        "examples": ["B", "C#", "F", "A", "D"],
      },
      {
        "name": "mode",
        "column_name": "mode",
        "type": "string",
        "description": "The mode of the track (e.g., Major, Minor). Cast the value as a string.",
        "examples": ["Major", "Minor"],
      },
      {
        "name": "danceability",
        "column_name": "danceability_%",
        "type": "integer",
        "description": "The danceability percentage of the track. Cast the value as an integer.",
        "examples": [80, 71, 51, 55, 65],
      },
      {
        "name": "valence",
        "column_name": "valence_%",
        "type": "integer",
        "description": "The valence percentage of the track. Cast the value as an integer.",
        "examples": [89, 61, 32, 58, 23],
      },
      {
        "name": "energy",
        "column_name": "energy_%",
        "type": "integer",
        "description": "The energy percentage of the track. Cast the value as an integer.",
        "examples": [83, 74, 53, 72, 80],
      },
      {
        "name": "acousticness",
        "column_name": "acousticness_%",
        "type": "integer",
        "description": "The acousticness percentage of the track. Cast the value as an integer.",
        "examples": [31, 7, 17, 11, 14],
      },
      {
        "name": "instrumentalness",
        "column_name": "instrumentalness_%",
        "type": "integer",
        "description": "The instrumentalness percentage of the track. Cast the value as an integer.",
        "examples": [0, 63, 17, 2, 19],
      },
      {
        "name": "liveness",
        "column_name": "liveness_%",
        "type": "integer",
        "description": "The liveness percentage of the track. Cast the value as an integer.",
        "examples": [8, 10, 31, 11, 28],
      },
      {
        "name": "speechiness",
        "column_name": "speechiness_%",
        "type": "integer",
        "description": "The speechiness percentage of the track. Cast the value as an integer.",
        "examples": [4, 6, 15, 24, 3],
      },
      {
        "name": "coverUrl",
        "column_name": "cover_url",
        "type": "string",
        "description": "The URL of the track's cover image. If the value is 'Not Found', it should be cast as an empty string.",
        "examples": [
          "https://i.scdn.co/image/ab67616d0000b2730656d5ce813ca3cc4b677e05",
          "https://i.scdn.co/image/ab67616d0000b273e85259a1cae29a8d91f2093d",
        ],
      },
    ],
  },
  {
    "title": "Artist",
    "type": "object",
    "description": "Node",
    "properties": [
      {
        "name": "name",
        "column_name": "artist(s)_name",
        "type": "string",
        "description": "The name of the artist. Split values in column by a comma",
        "examples": [
          "Latto",
          "Jung Kook",
          "Myke Towers",
          "Olivia Rodrigo",
          "Taylor Swift",
          "Bad Bunny",
        ],
      }
    ],
  },
  {
    "title": "PERFORMED_BY",
    "type": "object",
    "description": "Relationship",
    "properties": [
      {
        "name": "_from",
        "type": "string",
        "description": "The label of the node this relationship starts at",
        "examples": ["Track"],
      },
      {
        "name": "_to",
        "type": "string",
        "description": "The label of the node this relationship ends at",
        "examples": ["Artist"],
      },
    ],
  },
]
```

## 添加唯一标识符

我注意到模式中没有包含任何唯一标识符，这在导入关系时可能会成为问题。很显然，不同的艺术家可能发布同名歌曲，两个艺术家也可能拥有相同的名字。

因此，为曲目创建一个标识符，以便在更大的数据集中进行区分，这一点非常重要：

```
# Add primary key/unique identifiers
uid_prompt = PromptTemplate.from_template("""
You are a graph database expert reviewing a single entity from a data model generated by a colleague.
You want to ensure that all of the nodes imported into the database are unique.

## Example

A schema contains Actors with a number of properties including name, date of birth.

Two actors may have the same name then add a new compound property combining the name and date of birth.
If combining values, include the instruction to convert the value to slug case.  Call the new property 'id'.

If you have identified a new property, add it to the list of properties leaving the rest intact.
Include in the description the fields that are to be concatenated.


## Example Output

Here is an example of a good output:
'''
{example_output}
'''

## Current Entity Schema
'''
{entity}
'''

""", partial_variables=dict(example_output=dumps(example_output)))

uid_chain = uid_prompt | llm.with_structured_output(JSONSchemaSpecification)
```

这一步实际上只需要对节点执行，因此我从模式中提取了节点，为每个节点运行链式操作，然后将关系与更新后的定义结合起来：

```
# extract nodes and relationships
nodes = [n for n in existing_model if "node" in n["description"].lower()]
rels = [n for n in existing_model if "node" not in n["description"].lower()]

# generate a unique id for nodes
with_uids = []

for entity in nodes:
  res = uid_chain.invoke(dict(entity=dumps(entity)))
  json = loads(res.jsonschema)

  with_uids = with_uids + json if type(json) == list else with_uids + [json]

# combine nodes and relationships
with_uids = with_uids + rels
```

## 数据模型审查

为了确保模型的合理性，值得检查模型是否可以进行优化。model_prompt 在识别名词和动词方面做得很好，但在更复杂的模型中。

某次迭代将 *_playlists 和 _charts 列视为 ID，并尝试创建 Stream 节点和 IN_PLAYLIST 关系。我猜测这可能是因为超过 1000 的数字使用了逗号格式（例如 1,001）。

这是个不错的想法，但可能有点过于聪明了。不过这表明了让一个了解数据结构的人参与其中的重要性。

```
# Add primary key/unique identifiers
review_prompt = PromptTemplate.from_template("""
You are a graph database expert reviewing a data model generated by a colleague.

Your task is to review the data model and ensure that it is fit for purpose.
Check for:


## Check for nested objects

Remember that Neo4j cannot store arrays of objects or nested objects.
These must be converted into into separate nodes with relationships between them.
You must include the new node and a reference to the relationship to the output schema.

## Check for Entities in properties

If there is a property that represents an array of IDs, a new node should be created for that entity.
You must include the new node and a reference to the relationship to the output schema.

# Keep Instructions

Ensure that the instructions for the nodes, relationships, and properties are clear and concise.
You may improve them but the detail must not be removed in any circumstances.


## Current Entity Schema

'''
{entity}
'''
""")

review_chain = review_prompt | llm.with_structured_output(JSONSchemaSpecification)

review_nodes = [n for n in with_uids if "node" in n["description"].lower() ]
review_rels = [n for n in with_uids if "node" not in n["description"].lower() ]

reviewed = []

for entity in review_nodes:
  res = review_chain.invoke(dict(entity=dumps(entity)))
  json = loads(res.jsonschema)

  reviewed = reviewed + json

# add relationships back in
reviewed = reviewed + review_rels

len(reviewed)

reviewed = with_uids
```

在现实场景中，我会希望多次运行此过程，以迭代改进数据模型。我会设置一个最大限制，然后迭代到该点或数据模型对象不再变化为止。

## 生成导入语句

此时，模式应该足够健壮，并包含尽可能多的信息，以允许 LLM 生成一组导入脚本。

根据 Neo4j 数据导入建议，文件应多次处理，每次只导入一个节点或关系，以避免急切操作和锁定。

```
import_prompt = PromptTemplate.from_template("""
Based on the data model, write a Cypher statement to import the following data from a CSV file into Neo4j.

Do not use LOAD CSV as this data will be imported using the Neo4j Python Driver, use UNWIND on the $rows parameter instead.
You are writing a multi-pass import process, so concentrate on the entity mentioned.
When importing data, you must use the following guidelines:
* follow the instructions in the description when identifying primary keys.
* Use the instructions in the description to determine the format of properties when a finding.
* When combining fields into an ID, use the apoc.text.slug function to convert any text to slug case and toLower to convert the string to lowercase - apoc.text.slug(toLower(row.`name`))
* If you split a property, convert it to a string and use the trim function to remove any whitespace - trim(toString(row.`name`))
* When combining properties, wrap each property in the coalesce function so the property is not null if one of the values is not set - coalesce(row.`id`, '') + '--'+ coalsece(row.`title`)
* Use the `column_name` field to map the CSV column to the property in the data model.
* Wrap all column names from the CSV in backticks - for example row.`column_name`.
* When you merge nodes, merge on the unique identifier and nothing else.  All other properties should be set using `SET`.
* Do not use apoc.periodic.iterate, the files will be batched in the application.
Data Model:
'''
{data_model}
'''
Current Entity:
'''
{entity}
'''
""")
```

此链式操作需要与前几个步骤不同的输出对象。在这种情况下，cypher 成员最为重要，但我还想包括一个 chain_of_thought 键，以鼓励思维过程：

```
class CypherOutputSpecification(BaseModel):
  chain_of_thought: str = Field(description="Any reasoning used to write the Cypher statement")
  cypher: str = Field(description="The Cypher statement to import the data")
  notes: Optional[str] = Field(description="Any notes or closing remarks about the Cypher statement")

import_chain = import_prompt | llm.with_structured_output(CypherOutputSpecification)
```

然后同样的过程适用于遍历每个已审查的定义并生成 Cypher：

```
import_cypher = []
for n in reviewed:
  print('\n\n------', n['title'])
  res = import_chain.invoke(dict(
    data_model=dumps(reviewed),
    entity=n
  ))
  import_cypher.append((
    res.cypher
  ))
  print(res.cypher)

```

控制台输出：

```
------ Track
UNWIND $rows AS row
MERGE (t:Track {id: apoc.text.slug(toLower(coalesce(row.`track_name`, '') + '-' + coalesce(row.`released_year`, '')))})
SET t.name = trim(toString(row.`track_name`)),
    t.artist_count = toInteger(row.`artist_count`),
    t.released_year = toInteger(row.`released_year`),
    t.released_month = toInteger(row.`released_month`),
    t.released_day = toInteger(row.`released_day`),
    t.inSpotifyPlaylists = toInteger(row.`in_spotify_playlists`),
    t.inSpotifyCharts = toInteger(row.`in_spotify_charts`),
    t.streams = row.`streams`,
    t.inApplePlaylists = toInteger(row.`in_apple_playlists`),
    t.inAppleCharts = toInteger(row.`in_apple_charts`),
    t.inDeezerPlaylists = row.`in_deezer_playlists`,
    t.inDeezerCharts = toInteger(row.`in_deezer_charts`),
    t.inShazamCharts = row.`in_shazam_charts`,
    t.bpm = toInteger(row.`bpm`),
    t.key = trim(toString(row.`key`)),
    t.mode = trim(toString(row.`mode`)),
    t.danceability = toInteger(row.`danceability_%`),
    t.valence = toInteger(row.`valence_%`),
    t.energy = toInteger(row.`energy_%`),
    t.acousticness = toInteger(row.`acousticness_%`),
    t.instrumentalness = toInteger(row.`instrumentalness_%`),
    t.liveness = toInteger(row.`liveness_%`),
    t.speechiness = toInteger(row.`speechiness_%`),
    t.coverUrl = CASE row.`cover_url` WHEN 'Not Found' THEN '' ELSE trim(toString(row.`cover_url`)) END


------ Artist
UNWIND $rows AS row
WITH row, split(row.`artist(s)_name`, ',') AS artistNames
UNWIND artistNames AS artistName
MERGE (a:Artist {id: apoc.text.slug(toLower(trim(artistName)))})
SET a.name = trim(artistName)


------ PERFORMED_BY
UNWIND $rows AS row
UNWIND split(row.`artist(s)_name`, ',') AS artist_name
MERGE (t:Track {id: apoc.text.slug(toLower(row.`track_name`)) + '-' + trim(toString(row.`released_year`))})
MERGE (a:Artist {id: apoc.text.slug(toLower(trim(artist_name)))})
MERGE (t)-[:PERFORMED_BY]->(a)
```

这个提示词经过了一些工程调整才获得一致的结果：

- 有时 Cypher 会包含定义了多个字段的 MERGE 语句，这在最佳情况下也是次优的。如果任何列为空，整个导入将失败。
- 有时结果会包含 apoc.period.iterate，但我不再需要它，并且我希望能够使用 Python 驱动程序执行代码。
- 我不得不反复强调，在创建关系时应使用指定的列名。
- 当使用关系两端节点的唯一标识符时，LLM 就不会遵循指示，因此我多次尝试让它遵循描述中的指示。这个提示词和 model_prompt 之间有些往返。
- 对于包含特殊字符的列名（如 energy_%），需要使用反引号。

将此分为两个提示词——一个用于节点，一个用于关系——也会有所帮助。但这是留待另一天的任务。

## 创建唯一约束

接下来，导入脚本可以作为在数据库中创建唯一约束的基础：

```
constraint_prompt = PromptTemplate.from_template("""
You are an expert graph database administrator.
Use the following Cypher statement to write a Cypher statement to
create unique constraints on any properties used in a MERGE statement.

The correct syntax for a unique constraint is:
CREATE CONSTRAINT movie_title_id IF NOT EXISTS FOR (m:Movie) REQUIRE m.title IS UNIQUE;

Cypher:
'''
{cypher}
'''
""")

constraint_chain = constraint_prompt | llm.with_structured_output(CypherOutputSpecification)

constraint_queries = []

for statement in import_cypher:
  res = constraint_chain.invoke(dict(cypher=statement))

  statements = res.cypher.split(";")

  for cypher in statements:
    constraint_queries.append(cypher)
```

控制台输出：

```
CREATE CONSTRAINT track_id_unique IF NOT EXISTS FOR (t:Track) REQUIRE t.id IS UNIQUE

CREATE CONSTRAINT stream_id IF NOT EXISTS FOR (s:Stream) REQUIRE s.id IS UNIQUE

CREATE CONSTRAINT playlist_id IF NOT EXISTS FOR (p:Playlist) REQUIRE p.id IS UNIQUE

CREATE CONSTRAINT chart_id IF NOT EXISTS FOR (c:Chart) REQUIRE c.id IS UNIQUE

CREATE CONSTRAINT track_id_unique IF NOT EXISTS FOR (t:Track) REQUIRE t.id IS UNIQUE

CREATE CONSTRAINT stream_id_unique IF NOT EXISTS FOR (s:Stream) REQUIRE s.id IS UNIQUE

CREATE CONSTRAINT track_id_unique IF NOT EXISTS FOR (t:Track) REQUIRE t.id IS UNIQUE

CREATE CONSTRAINT playlist_id_unique IF NOT EXISTS FOR (p:Playlist) REQUIRE p.id IS UNIQUE

CREATE CONSTRAINT track_id_unique IF NOT EXISTS FOR (track:Track) REQUIRE track.id IS UNIQUE

CREATE CONSTRAINT chart_id_unique IF NOT EXISTS FOR (chart:Chart) REQUIRE chart.id IS UNIQUE
```

有时这个提示词会返回索引和约束的语句，因此需要用分号来分割。

## 运行导入

一切就绪后，便是执行 Cypher 语句的时间：

```
from os import getenv
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
  getenv("NEO4J_URI"),
  auth=(
    getenv("NEO4J_USERNAME"),
    getenv("NEO4J_PASSWORD")
  )
)

with driver.session() as session:
  # truncate the db
  session.run("MATCH (n) DETACH DELETE n")

  # create constraints
  for q in constraint_queries:
    if q.strip() != "":
      session.run(q)

  # import the data
  for q in import_cypher:
    if q.strip() != "":
        res = session.run(q, rows=rows).consume()
        print(q)
        print(res.counters)
```

## 数据集的质量保证

如果没有对数据集进行一些质量保证，这篇文章就不完整了，使用 GraphCypherQAChain：

```
from langchain.chains import GraphCypherQAChain
from langchain_community.graphs import Neo4jGraph

graph = Neo4jGraph(
  url=getenv("NEO4J_URI"),
  username=getenv("NEO4J_USERNAME"),
  password=getenv("NEO4J_PASSWORD"),
  enhanced_schema=True
)

qa = GraphCypherQAChain.from_llm(
  llm,
  graph=graph,
  allow_dangerous_requests=True,
  verbose=True
)

```

## 最受欢迎的艺术家

数据库中最受欢迎的艺术家是谁？

```
qa.invoke({"query": "Who are the most popular artists?"})

> Entering new GraphCypherQAChain chain...
Generated Cypher:
cypher
MATCH (:Track)-[:PERFORMED_BY]->(a:Artist)
RETURN a.name, COUNT(*) AS popularity
ORDER BY popularity DESC
LIMIT 10

Full Context:
[{'a.name': 'Bad Bunny', 'popularity': 40}, {'a.name': 'Taylor Swift', 'popularity': 38}, {'a.name': 'The Weeknd', 'popularity': 36}, {'a.name': 'SZA', 'popularity': 23}, {'a.name': 'Kendrick Lamar', 'popularity': 23}, {'a.name': 'Feid', 'popularity': 21}, {'a.name': 'Drake', 'popularity': 19}, {'a.name': 'Harry Styles', 'popularity': 17}, {'a.name': 'Peso Pluma', 'popularity': 16}, {'a.name': '21 Savage', 'popularity': 14}]

> Finished chain.

{
  "query": "Who are the most popular artists?",
  "result": "Bad Bunny, Taylor Swift, and The Weeknd are the most popular artists."
}
```

LLM 似乎是根据艺术家参与的曲目数量来判断受欢迎程度的，而不是根据他们的总播放量。

## 每分钟节拍数

哪首曲子的 BPM 最高？

```
qa.invoke({"query": "Which track has the highest BPM?"})

> Entering new GraphCypherQAChain chain...
Generated Cypher:
cypher
MATCH (t:Track)
RETURN t
ORDER BY t.bpm DESC
LIMIT 1

Full Context:
[{'t': {'id': 'seven-feat-latto-explicit-ver--2023'}}]

> Finished chain.

{
  "query": "Which track has the highest BPM?",
  "result": "I don't know the answer."
}
```

## 改进 Cypher 生成提示词

在这种情况下，Cypher 看起来不错，并且提示中包含了正确的结果，但 gpt-4o 无法解释答案。看来传递给 GraphCypherQAChain 的 CYPHER_GENERATION_PROMPT 需要添加额外的说明，以使列名更详细。

> 始终在 Cypher 语句中使用详细的列名，使用标签和属性名。例如，使用‘person_name’而不是‘name’。

带有自定义提示词的 GraphCypherQAChain：

```
CYPHER_GENERATION_TEMPLATE = """Task:Generate Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
Do not use any other relationship types or properties that are not provided.
Schema:
{schema}
Note: Do not include any explanations or apologies in your responses.
Do not respond to any questions that might ask anything else than for you to construct a Cypher statement.
Do not include any text except the generated Cypher statement.

Always use verbose column names in the Cypher statement using the label and property names. For example, use 'person_name' instead of 'name'.
Include data from the immediate network around the node in the result to provide extra context.  For example, include the Movie release year, a list of actors and their roles, or the director of a movie.
When ordering by a property, add an `IS NOT NULL` check to ensure that only nodes with that property are returned.

Examples: Here are a few examples of generated Cypher statements for particular questions:

# How many people acted in Top Gun?
MATCH (m:Movie {{name:"Top Gun"}})
RETURN COUNT { (m)<-[:ACTED_IN]-() } AS numberOfActors

The question is:
{question}"""

CYPHER_GENERATION_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], template=CYPHER_GENERATION_TEMPLATE
)

qa = GraphCypherQAChain.from_llm(
  llm,
  graph=graph,
  allow_dangerous_requests=True,
  verbose=True,
  cypher_prompt=CYPHER_GENERATION_PROMPT,
)
```

## 由最多艺术家表演的曲目

图在返回按类型和方向计数的关系时表现出色。

```
qa.invoke({"query": "Which tracks are performed by the most artists?"})

> Entering new GraphCypherQAChain chain...
Generated Cypher:
cypher
MATCH (t:Track)
    WITH t, COUNT { (t)-[:PERFORMED_BY]->(:Artist) }  as artist_count
WHERE artist_count IS NOT NULL
RETURN t.id AS track_id, t.name AS track_name, artist_count
ORDER BY artist_count DESC

Full Context:
[{'track_id': 'los-del-espacio-2023', 'track_name': 'Los del Espacio', 'artist_count': 8}, {'track_id': 'se-le-ve-2021', 'track_name': 'Se Le Ve', 'artist_count': 8}, {'track_id': 'we-don-t-talk-about-bruno-2021', 'track_name': "We Don't Talk About Bruno", 'artist_count': 7}, {'track_id': 'cayï-ï-la-noche-feat-cruz-cafunï-ï-abhir-hathi-bejo-el-ima--2022', 'track_name': None, 'artist_count': 6}, {'track_id': 'jhoome-jo-pathaan-2022', 'track_name': 'Jhoome Jo Pathaan', 'artist_count': 6}, {'track_id': 'besharam-rang-from-pathaan--2022', 'track_name': None, 'artist_count': 6}, {'track_id': 'nobody-like-u-from-turning-red--2022', 'track_name': None, 'artist_count': 6}, {'track_id': 'ultra-solo-remix-2022', 'track_name': 'ULTRA SOLO REMIX', 'artist_count': 5}, {'track_id': 'angel-pt-1-feat-jimin-of-bts-jvke-muni-long--2023', 'track_name': None, 'artist_count': 5}, {'track_id': 'link-up-metro-boomin-don-toliver-wizkid-feat-beam-toian-spider-verse-remix-spider-man-across-the-spider-verse--2023', 'track_name': None, 'artist_count': 5}]

> Finished chain.

{
  "query": "Which tracks are performed by the most artists?",
  "result": "The tracks \"Los del Espacio\" and \"Se Le Ve\" are performed by the most artists, with each track having 8 artists."
}
```

## 总结

CSV 分析和建模是最耗时的部分。生成可能需要超过五分钟。

成本本身相当便宜。在八小时的实验中，我必须发送了数百个请求，最终我花费了大约一美元左右。

在达到这个目标之前，我遇到了许多挑战：

- 提示词经过了多次迭代才正确。这一问题可以通过对模型进行微调或提供少样本示例来解决。
- GPT-4o 的 JSON 响应可能不一致。有人向我推荐了 json-repair (https://github.com/mangiucugna/json_repair)，它比让 LLM 自己验证 JSON 输出效果更好。

我可以看到这种方法在 LangGraph 实现中运行良好，在该实现中，操作按顺序执行，使大语言模型能够构建和精细化模型。随着新模型的不断发布，这些模型也可能受益于微调。