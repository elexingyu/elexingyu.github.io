## 深入剖析 LangChain 中基于大语言模型（LLM）的图构建实现

![](https://static.openmindclub.com/42md/1733794746503-9a9039c2-a05e-4fad-9db6-5d45a7eebfaf.png)

从文本中创建图谱是一项令人兴奋但极具挑战性的任务。本质上，这是一种将非结构化文本转化为结构化数据的过程。尽管这种方法已经存在了一段时间，但随着大语言模型（LLM）的出现，它逐渐进入主流并受到更多关注。

![](https://static.openmindclub.com/42md/1733794758628-eaafd40e-db34-4532-982c-f63862f1aa70.png)

从文本中提取实体和关系以构建知识图谱。图片由作者提供。

在上图中可以看到，信息提取如何将原始文本转化为知识图谱。在左侧，多个文档展示了关于个人及其与公司的关系的非结构化句子；而在右侧，这些信息被表示为实体及其连接关系的图谱，清晰地展示了谁在某个公司工作或创立了某些组织。

### 为什么要将文本转化为图谱？

从文本中提取结构化信息并将其表示为图谱的一个关键原因是支持**基于检索增强生成（RAG）**的应用程序。虽然在非结构化文本上使用文本嵌入模型（text embedding models）是一种有效的方法，但在回答复杂的多跳问题时，它可能显得不足。这类问题需要理解多个实体之间的连接，或者需要执行诸如过滤、排序和聚合等结构化操作。

通过从文本中提取结构化信息并构建知识图谱，不仅可以更有效地组织数据，还可以创建一个强大的框架来理解实体之间的复杂关系。这种结构化方法使得检索和利用特定信息变得更加容易，扩展了可回答问题的范围，同时提高了回答的准确性。

---

大约一年前，我开始尝试使用 LLM 构建图谱。由于越来越多的人对此感兴趣，我们决定将这一能力集成到 LangChain 中，作为**LLM 图谱转换器（LLM Graph Transformer）**。在过去的一年里，我们收获了许多宝贵的经验，并引入了一些新功能，这些功能将在本文中展示。

代码已发布在 GitHub(https://github.com/) 上。

---

## 设置 Neo4j 环境

我们将使用 Neo4j 作为底层图存储，它自带图形可视化功能。最简单的开始方式是使用免费的 Neo4j Aura 实例，它提供了 Neo4j 数据库的云实例。或者，你也可以通过下载 Neo4j Desktop 应用程序并创建本地数据库实例来设置本地环境。

```python
from langchain_community.graphs import Neo4jGraph

graph = Neo4jGraph(
    url="bolt://54.87.130.140:7687",
    username="neo4j",
    password="cables-anchors-directories",
    refresh_schema=False
)
```

---

## LLM 图谱转换器

LLM 图谱转换器旨在提供一个灵活的框架，用于使用任何 LLM 构建图谱。由于目前有许多不同的提供商和模型，这项任务并不简单。幸运的是，LangChain 处理了许多标准化流程。至于 LLM 图谱转换器本身，它就像两种不同能力的工具结合在一起——能够在两种完全独立的模式下运行。

![LLM 图谱转换器包含两种从文本中提取图谱的独立模式。图片由用户提供。](https://static.openmindclub.com/42md/1733794772047-5ef1b97f-9b7d-48e3-8cb6-85a9f8bdea03.png)

LLM 图谱转换器有两种模式，每种模式都旨在使用 LLM 在不同场景下从文档中生成图谱：

1. **基于工具的模式（默认）**  
   当 LLM 支持结构化输出或函数调用时，该模式利用 LLM 内置的 `with_structured_output` 方法来使用工具。工具规范定义了输出格式，确保以结构化、预定义的方式提取实体和关系。这在图的左侧显示了 Node 和 Relationship 类的代码。

2. **基于提示的模式（后备）**  
   在 LLM 不支持工具或函数调用的情况下，LLM 图谱转换器会退回到纯粹基于提示的方式。此模式使用少样本提示（few-shot prompting）来定义输出格式，引导 LLM 以文本为基础的方式提取实体和关系。然后通过自定义函数解析结果，将 LLM 的输出转换为 JSON 格式。此 JSON 用于填充节点和关系，与基于工具的模式类似，但这里完全由提示而非结构化工具引导。这在图的右侧显示了一个示例提示和结果 JSON 输出。

这两种模式确保了 LLM 图谱转换器能够适应不同的 LLM，无论是直接使用工具还是通过解析基于文本的提示输出来构建图谱。

_注意：即使是支持工具或函数的模型，也可以通过设置属性 `_ignore_tools_usage=True` 来使用基于提示的提取模式。_

---

## 基于工具的提取

我们最初选择了基于工具的提取方法，因为它减少了对大量提示工程和自定义解析函数的需求。在 LangChain 中，`with_structured_output` 方法允许你使用工具或函数提取信息，输出通过 JSON 结构或 Pydantic 对象定义。我个人认为 Pydantic 对象更清晰，因此我们选择了它。

### 定义节点（Node）

首先，我们定义一个 `Node` 类：

```python
class Node(BaseNode):
    id: str = Field(..., description="Name or human-readable unique identifier")
    label: str = Field(..., description=f"Available options are {enum_values}")
    properties: Optional[List[Property]]
```

每个节点都有一个 `id`（唯一标识符）、一个 `label`（标签）和可选的 `properties`（属性）。为了简洁，这里没有包括完整的描述。将 id 描述为人类可读的唯一标识符非常重要，因为一些 LLM 倾向于以更传统的方式理解 ID 属性，比如随机字符串或递增整数。而我们希望将实体名称用作 id 属性。我们还通过在 `label` 描述中列出可用标签类型来限制标签类型。此外，像 OpenAI 的模型一样，LLM 支持一个 `enum` 参数，我们也使用了它。

### 定义关系（Relationship）

接下来，我们定义 `Relationship` 类：

```python
class Relationship(BaseRelationship):
    source_node_id: str
    source_node_label: str = Field(..., description=f"Available options are {enum_values}")
    target_node_id: str
    target_node_label: str = Field(..., description=f"Available options are {enum_values}")
    type: str = Field(..., description=f"Available options are {enum_values}")
    properties: Optional[List[Property]]
```

这是 `Relationship` 类的第二个版本。最初，我们为源节点和目标节点使用了嵌套的 `Node` 对象，但我们很快发现嵌套对象降低了提取过程的准确性和质量。因此，我们决定将源节点和目标节点展平为单独的字段，例如 `source_node_id` 和 `source_node_label`，以及 `target_node_id` 和 `target_node_label`。此外，我们在节点标签和关系类型的描述中定义了允许的值，以确保 LLM 遵循指定的图谱模式。

基于工具的提取方法使我们能够为节点和关系定义属性。以下是我们用于定义它们的类。

```
class Property(BaseModel):
    """A single property consisting of key and value"""
    key: str = Field(..., description=f"Available options are {enum_values}")
    value: str
```

每个 `Property` 都被定义为一个键值对。虽然这种方法很灵活，但也有其局限性。例如，我们无法为每个属性提供唯一的描述，也无法指定某些属性为必填而其他为可选，因此所有属性都被定义为可选。此外，属性并未为每种节点或关系类型单独定义，而是被所有类型共享。

我们还实现了一个详细的系统提示词，帮助指导提取过程。不过，根据我的经验，函数和参数的描述比系统消息对提取结果的影响更大。

目前，LLM Graph Transformer 中尚无简单方法来自定义函数或参数描述。

## 基于提示词的提取

由于仅有少数商业化的 LLM 和 LLaMA 3 支持原生工具，我们为不支持工具的模型实现了一个备用方案。即使使用支持工具的模型，也可以通过设置 `ignore_tool_usage=True` 来切换到基于提示词的方法。

大部分基于提示词的提示工程和示例由 Geraldus Wilsen 提供。

在基于提示词的方法中，我们必须直接在提示词中定义输出结构。完整的提示词可以在这里找到。在本文中，我们只进行高层概述。我们首先定义系统提示词。

```
You are a top-tier algorithm designed for extracting information in structured formats to build a knowledge graph. Your task is to identify the entities and relations specified in the user prompt from a given text and produce the output in JSON format. This output should be a list of JSON objects, with each object containing the following keys:

- **"head"**: The text of the extracted entity, which must match one of the types specified in the user prompt.
- **"head_type"**: The type of the extracted head entity, selected from the specified list of types.
- **"relation"**: The type of relation between the "head" and the "tail," chosen from the list of allowed relations.
- **"tail"**: The text of the entity representing the tail of the relation.
- **"tail_type"**: The type of the tail entity, also selected from the provided list of types.

Extract as many entities and relationships as possible.

**Entity Consistency**: Ensure consistency in entity representation. If an entity, like "John Doe," appears multiple times in the text under different names or pronouns (e.g., "Joe," "he"), use the most complete identifier consistently. This consistency is essential for creating a coherent and easily understandable knowledge graph.

**Important Notes**:
- Do not add any extra explanations or text.
```

在基于提示词的方法中，一个关键区别在于我们要求 LLM 仅提取关系，而不是单独的节点。这意味着我们不会有孤立节点，而工具方法中可能会有。此外，由于缺乏原生工具支持的模型通常表现较差，我们不允许提取任何属性（无论是节点还是关系的属性），以简化提取输出。

接下来，我们为模型添加了一些少样本学习示例。

```
examples = [
    {
        "text": (
            "Adam is a software engineer in Microsoft since 2009, "
            "and last year he got an award as the Best Talent"
        ),
        "head": "Adam",
        "head_type": "Person",
        "relation": "WORKS_FOR",
        "tail": "Microsoft",
        "tail_type": "Company",
    },
    {
        "text": (
            "Adam is a software engineer in Microsoft since 2009, "
            "and last year he got an award as the Best Talent"
        ),
        "head": "Adam",
        "head_type": "Person",
        "relation": "HAS_AWARD",
        "tail": "Best Talent",
        "tail_type": "Award",
    },
...
]
```

在这种方法中，目前不支持添加自定义的少样本学习示例或额外指令。唯一的自定义方式是通过 `prompt` 属性修改整个提示词。扩展自定义选项是我们正在积极考虑的方向。

接下来，我们将研究如何定义图谱模式。

## 定义图谱模式

在使用 LLM Graph Transformer 进行信息提取时，定义一个图谱模式对于指导模型构建有意义的结构化知识表示至关重要。一个定义良好的图谱模式会指定要提取的节点和关系类型，以及每个类型相关的属性。这种模式充当蓝图，确保 LLM 按照所需的知识图谱结构一致地提取相关信息。

在本文中，我们将使用玛丽·居里（Marie Curie）维基百科页面的开头段落进行测试，并在结尾添加一段关于罗宾·威廉姆斯（Robin Williams）的句子。

```
from langchain_core.documents import Document

text = """
Marie Curie, 7 November 1867 – 4 July 1934, was a Polish and naturalised-French physicist and chemist who conducted pioneering research on radioactivity.
She was the first woman to win a Nobel Prize, the first person to win a Nobel Prize twice, and the only person to win a Nobel Prize in two scientific fields.
Her husband, Pierre Curie, was a co-winner of her first Nobel Prize, making them the first-ever married couple to win the Nobel Prize and launching the Curie family legacy of five Nobel Prizes.
She was, in 1906, the first woman to become a professor at the University of Paris.
Also, Robin Williams.
"""
documents = [Document(page_content=text)]
```

我们将在所有示例中使用 GPT-4o。

```
from langchain_openai import ChatOpenAI
import getpass
import os

os.environ["OPENAI_API_KEY"] = getpass.getpass("OpenAI api key")

llm = ChatOpenAI(model='gpt-4o')
```

首先，让我们看看在没有定义任何图谱模式的情况下，提取过程是如何进行的。

```
from langchain_experimental.graph_transformers import LLMGraphTransformer

no_schema = LLMGraphTransformer(llm=llm)
```

现在，我们可以使用异步的 `aconvert_to_graph_documents` 函数处理文档。推荐使用异步方式进行 LLM 提取，因为它允许并行处理多个文档。这种方法可以显著减少等待时间，并提高处理多个文档时的吞吐量。

```
data = await no_schema.aconvert_to_graph_documents(documents)
```

LLM Graph Transformer 的响应将是一个图谱文档，其结构如下：

```
[
    GraphDocument(
        nodes=[
            Node(id="Marie Curie", type="Person", properties={}),
            Node(id="Pierre Curie", type="Person", properties={}),
            Node(id="Nobel Prize", type="Award", properties={}),
            Node(id="University Of Paris", type="Organization", properties={}),
            Node(id="Robin Williams", type="Person", properties={}),
        ],
        relationships=[
            Relationship(
                source=Node(id="Marie Curie", type="Person", properties={}),
                target=Node(id="Nobel Prize", type="Award", properties={}),
                type="WON",
                properties={},
            ),
            Relationship(
                source=Node(id="Marie Curie", type="Person", properties={}),
                target=Node(id="Nobel Prize", type="Award", properties={}),
                type="WON",
                properties={},
            ),
            Relationship(
                source=Node(id="Marie Curie", type="Person", properties={}),
                target=Node(
                    id="University Of Paris", type="Organization", properties={}
                ),
                type="PROFESSOR",
                properties={},
            ),
            Relationship(
                source=Node(id="Pierre Curie", type="Person", properties={}),
                target=Node(id="Nobel Prize", type="Award", properties={}),
                type="WON",
                properties={},
            ),
        ],
        source=Document(
            metadata={"id": "de3c93515e135ac0e47ca82a4f9b82d8"},
            page_content="\nMarie Curie, 7 November 1867 – 4 July 1934, was a Polish and naturalised-French physicist and chemist who conducted pioneering research on radioactivity.\nShe was the first woman to win a Nobel Prize, the first person to win a Nobel Prize twice, and the only person to win a Nobel Prize in two scientific fields.\nHer husband, Pierre Curie, was a co-winner of her first Nobel Prize, making them the first-ever married couple to win the Nobel Prize and launching the Curie family legacy of five Nobel Prizes.\nShe was, in 1906, the first woman to become a professor at the University of Paris.\nAlso, Robin Williams!\n",
        ),
    )
]
```

该图谱文档描述了提取的 `nodes` 和 `relationships`。此外，提取的源文档被添加到了 `source` 键下。

我们可以使用 Neo4j 浏览器可视化输出，从而更清晰直观地理解数据。

![](https://static.openmindclub.com/42md/1733794804552-85053585-80c0-428d-ab66-d18d8ebccfdc.png)

_上图展示了两次提取玛丽·居里段落的结果。在这种情况下，我们使用了带有工具提取的 GPT-4，它也允许孤立节点，如图所示。由于未定义图谱模式，LLM 在运行时决定提取哪些信息，这可能导致即使是同一段落的输出也有所不同。因此，一些提取结果比其他结果更详细，结构可能有所不同。例如，在左侧，玛丽被表示为诺贝尔奖的 `WINNER`，而在右侧，她 `WON` 诺贝尔奖。_

接下来，让我们尝试使用基于提示词的方法进行相同的提取。对于支持工具的模型，可以通过设置 `ignore_tool_usage` 参数启用基于提示词的提取。

```
no_schema_prompt = LLMGraphTransformer(llm=llm, ignore_tool_usage=True)
data = await no_schema.aconvert_to_graph_documents(documents)
```

同样，我们可以在 Neo4j 浏览器中可视化两次单独的执行结果。

![使用基于提示词的方法提取同一数据集时未定义图谱模式的可视化结果。图片由作者提供。](https://static.openmindclub.com/42md/1733794862445-82fedf4e-3fa6-4a26-b7d0-669d9ccb5546.png)


使用基于提示词的方法，我们不会看到任何孤立节点。然而，与之前的提取一样，模式可能因运行而异，导致相同输入的输出有所不同。

接下来，让我们看看如何通过定义图谱模式来帮助生成更一致的输出。

## 定义允许的节点

约束提取的图谱结构可以极大地提高一致性，因为它指导模型专注于特定的相关实体和关系。通过定义清晰的模式，可以提高提取的一致性，使输出更可预测并与实际需求对齐。这减少了运行之间的变化，并确保提取的数据遵循标准化结构，捕获预期的信息。通过一个定义良好的模式，模型不太可能忽略关键细节或引入意外元素，从而生成更简洁、更可用的图谱。

我们将从使用 `allowed_nodes` 参数定义要提取的节点类型开始。

```
allowed_nodes = ["Person", "Organization", "Location", "Award", "ResearchField"]
nodes_defined = LLMGraphTransformer(llm=llm, allowed_nodes=allowed_nodes)
data = await allowed_nodes.aconvert_to_graph_documents(documents)
```

在这里，我们定义了 LLM 应提取的五种节点类型，例如 _Person_、_Organization_、_Location_ 等。我们在 Neo4j 浏览器中可视化两次单独的执行结果以进行比较。

![定义预期节点类型后的两次提取可视化结果。图片由作者提供](https://static.openmindclub.com/42md/1733794900130-164f5655-451a-4ef3-8d9c-702167e7c5a2.png)


通过指定预期的节点类型，我们实现了更一致的节点提取。然而，仍可能发生一些变化。例如，在第一次运行中，“放射性”被提取为研究领域，而在第二次运行中则没有。

由于我们尚未定义关系，它们的类型在运行之间也可能有所不同。此外，一些提取可能捕获的信息比其他提取更多。例如，玛丽和皮埃尔之间的 `MARRIED_TO` 关系并未在两次提取中都出现。

接下来，让我们探讨如何通过定义关系类型进一步提高一致性。

## 定义允许的关系

如前所述，仅定义节点类型仍允许关系提取的变化。为了解决这个问题，让我们探讨如何定义关系。第一种方法是使用可用类型的列表来指定允许的关系。

```
allowed_nodes = ["Person", "Organization", "Location", "Award", "ResearchField"]
allowed_relationships = ["SPOUSE", "AWARD", "FIELD_OF_RESEARCH", "WORKS_AT", "IN_LOCATION"]
rels_defined = LLMGraphTransformer(
  llm=llm,
  allowed_nodes=allowed_nodes,
  allowed_relationships=allowed_relationships
)
data = await rels_defined.aconvert_to_graph_documents(documents)
```

再次检查两次单独提取的结果。

![定义了节点和关系类型后的两次提取可视化结果。图片由作者提供。](https://static.openmindclub.com/42md/1733794914049-22505b6d-8ae6-4523-9d19-fc8c58daef66.png)


通过同时定义节点和关系类型，我们的输出变得显著更一致。例如，玛丽始终被显示为获奖者、皮埃尔的配偶以及巴黎大学的教授。然而，由于关系被定义为通用列表，而没有限制它们可以连接的节点类型，因此仍可能发生一些变化。例如，`FIELD_OF_RESEARCH` 关系有时可能出现在 `Person` 和 `ResearchField` 之间，而有时可能连接 `Award` 和 `ResearchField`。此外，由于未定义关系方向，方向的一致性可能会有所不同。

为了解决无法指定关系连接的节点类型以及强制关系方向的问题，我们最近引入了一种新的关系定义选项，如下所示。

```
allowed_nodes = ["Person", "Organization", "Location", "Award", "ResearchField"]
allowed_relationships = [
    ("Person", "SPOUSE", "Person"),
    ("Person", "AWARD", "Award"),
    ("Person", "WORKS_AT", "Organization"),
    ("Organization", "IN_LOCATION", "Location"),
    ("Person", "FIELD_OF_RESEARCH", "ResearchField")
]
rels_defined = LLMGraphTransformer(
  llm=llm,
  allowed_nodes=allowed_nodes,
  allowed_relationships=allowed_relationships
)
data = await rels_defined.aconvert_to_graph_documents(documents)
```

与将关系定义为简单的字符串列表不同，我们现在使用三元组格式，其中元素分别表示源节点、关系类型和目标节点。

让我们再次可视化结果。

![使用三元组格式定义关系后的两次提取可视化结果。图片由作者提供。](https://static.openmindclub.com/42md/1733794925038-aaad15c9-a503-47a6-a9a5-f8ec84bbd707.png)


使用三元组方法为提取的图谱提供了更一致的模式。然而，鉴于 LLM 的特性，提取的细节级别可能仍会有所变化。例如，在右侧，皮埃尔被显示为诺贝尔奖的获奖者，而在左侧，这一信息缺失。

## 定义属性

对图谱模式的最终增强是为节点和关系定义属性。我们有两种选择。第一种是将 `node_properties` 或 `relationship_properties` 设置为 `true`，允许 LLM 自主决定提取哪些属性。

```
allowed_nodes = ["Person", "Organization", "Location", "Award", "ResearchField"]
allowed_relationships = [
    ("Person", "SPOUSE", "Person"),
    ("Person", "AWARD", "Award"),
    ("Person", "WORKS_AT", "Organization"),
    ("Organization", "IN_LOCATION", "Location"),
    ("Person", "FIELD_OF_RESEARCH", "ResearchField")
]
node_properties=True
relationship_properties=True
props_defined = LLMGraphTransformer(
  llm=llm,
  allowed_nodes=allowed_nodes,
  allowed_relationships=allowed_relationships,
  node_properties=node_properties,
  relationship_properties=relationship_properties
)
data = await props_defined.aconvert_to_graph_documents(documents)
graph.add_graph_documents(data)
```

让我们检查结果。

![提取的节点和关系属性。图片由作者提供。](https://static.openmindclub.com/42md/1733794931800-04bf5ac5-bf78-415a-95c7-e2082e694081.png)


我们允许 LLM 添加其认为相关的任何节点或关系属性。例如，它选择包括玛丽·居里的出生和死亡日期、她在巴黎大学的教授职位以及她两次获得诺贝尔奖的事实。这些额外的属性显著丰富了提取的信息。

第二种选择是定义我们希望提取的节点和关系属性。

```
allowed_nodes = ["Person", "Organization", "Location", "Award", "ResearchField"]
allowed_relationships = [
    ("Person", "SPOUSE", "Person"),
    ("Person", "AWARD", "Award"),
    ("Person", "WORKS_AT", "Organization"),
    ("Organization", "IN_LOCATION", "Location"),
    ("Person", "FIELD_OF_RESEARCH", "ResearchField")
]
node_properties=["birth_date", "death_date"]
relationship_properties=["start_date"]
props_defined = LLMGraphTransformer(
  llm=llm,
  allowed_nodes=allowed_nodes,
  allowed_relationships=allowed_relationships,
  node_properties=node_properties,
  relationship_properties=relationship_properties
)
data = await props_defined.aconvert_to_graph_documents(documents)
graph.add_graph_documents(data)
```

属性被简单地定义为两个列表。让我们看看 LLM 提取了什么。

![提取的预定义节点和关系属性。图片由作者提供。](https://static.openmindclub.com/42md/1733794939191-b699c0f8-004a-46f0-bfa6-3581704fa37b.png)


出生和死亡日期与之前的提取一致。然而，这次，LLM 还提取了玛丽在巴黎大学教授职位的开始日期。

属性确实为提取的信息增加了有价值的深度，但当前的实现存在一些限制：

- 属性只能通过基于工具的方法提取。
- 所有属性都被提取为字符串。
- 属性只能全局定义，无法为每个节点标签或关系类型单独定义。
- 没有选项来自定义属性描述，以指导 LLM 进行更精确的提取。

## 严格模式

如果你认为我们已经找到了一种让 LLM 完美遵循定义模式的方法，我必须澄清事实。尽管我们在提示工程方面投入了大量努力，但让 LLM，尤其是性能较差的模型，完全准确地遵循指令仍然具有挑战性。为了解决这个问题，我们引入了一个后处理步骤，称为 `strict_mode`，它会删除任何不符合定义图谱模式的信息，确保输出更干净和更一致。

默认情况下，`strict_mode` 设置为 `True`，但你可以通过以下代码禁用它：

```
LLMGraphTransformer(
  llm=llm,
  allowed_nodes=allowed_nodes,
  allowed_relationships=allowed_relationships,
  strict_mode=False
)
```

在禁用严格模式的情况下，你可能会得到超出定义图谱模式的节点或关系类型，因为 LLM 有时会对输出结构进行创造性发挥。

## 将图谱文档导入图数据库

从 LLM Graph Transformer 提取的图谱文档可以通过 `add_graph_documents` 方法导入到 Neo4j 等图数据库中，以便进一步分析和应用。我们将探索适合不同用例的多种数据导入选项。

## 默认导入

可以使用以下代码将节点和关系导入到 Neo4j。

```
graph.add_graph_documents(graph_documents)
```

这种方法直接导入提供的图谱文档中的所有节点和关系。我们在整个博客文章中使用了这种方法来查看不同 LLM 和模式配置的结果。

![默认导入设置。图片由作者提供。](https://static.openmindclub.com/42md/1733794952568-6e68822e-d5fa-4b89-8633-23851e07892b.png)


## 基础实体标签

大多数图数据库支持索引以优化数据导入和检索。在 Neo4j 中，索引只能为特定节点标签设置。由于我们可能无法提前知道所有节点标签，可以通过使用 `baseEntityLabel` 参数为每个节点添加一个次要基础标签来解决此问题。这样，我们仍然可以利用索引进行高效导入和检索，而无需为图谱中的每个可能节点标签设置索引。

```
graph.add_graph_documents(graph_documents, baseEntityLabel=True)
```

如前所述，使用 `baseEntityLabel` 参数会导致每个节点都有一个额外的 `__Entity__` 标签。

![每个节点通过 `baseEntityLabel`  参数获得一个次要标签。图片由作者提供。](https://static.openmindclub.com/42md/1733794962200-1fd3ccbd-e3f0-483a-ae3a-b778723934da.png)


## 包括源文档

最后一个选项是导入提取的节点和关系的源文档。这种方法使我们能够跟踪每个实体出现在哪些文档中。可以通过 `include_source` 参数导入源文档。

```
graph.add_graph_documents(graph_documents, include_source=True)
```

检查导入的图谱后，我们应该看到类似的结果。

![导入的源文档。图片由作者提供](https://static.openmindclub.com/42md/1733794981647-055c02e6-d2b8-4d76-93eb-985462642888.png)


在此可视化中，源文档以蓝色突出显示，所有从中提取的实体通过 `MENTIONS` 关系连接。这种模式允许构建同时利用结构化和非结构化搜索方法的检索器。

## 总结

在本文中，我们探讨了 LangChain 的 LLM Graph Transformer 及其构建知识图谱的双重模式。工具模式是我们的主要方法，它利用结构化输出和函数调用，减少提示工程并支持属性提取。而基于提示词的方法在工具不可用时非常有用，它依赖于少样本学习示例来指导 LLM。然而，基于提示词的提取不支持属性提取，也不会生成孤立节点。

我们观察到，定义清晰的图谱模式（包括允许的节点和关系类型）可以提高提取的一致性和性能。受约束的模式有助于确保输出符合所需结构，使其更可预测、可靠和适用。无论是使用工具还是提示词，LLM Graph Transformer 都能更有组织地将非结构化数据转化为结构化表示，从而支持更好的 RAG 应用和多跳查询处理。

代码已在 GitHub （https://github.com/tomasonjo/blogs/blob/master/llm/llm_graph_transformer_in_depth.ipynb）上提供。你还可以通过 Neo4j 的托管 **LLM Graph Builder** 应用程序在无代码环境中试用 LLM Graph Transformer。
