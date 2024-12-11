---
categories: articles
date: 2024-10-23
layout: post
style: huoshui
tags:
- AI
- 知识图谱
- 教程
title: Graphiti：揭秘知识图谱构建挑战与高效解决方案
---

![扩展大语言模型数据提取：挑战、设计决策与解决方案](https://blog.getzep.com/content/images/size/w2000/2024/09/graphiti---graph-intro---short.gif)

Graphiti 是一个用于构建和查询动态、时间感知的知识图谱的 Python 库。它可以用于建模复杂、不断演变的数据集，并确保 AI 智能体能够访问它们完成非平凡任务所需的数据。它是一个强大的工具，可以作为许多复杂 RAG 项目的数据库和检索层。

构建 Graphiti 是一个充满挑战的过程。本文将讨论我们的设计决策、提示词工程的演变以及扩展基于大语言模型的信息提取的各种方法。这篇文章是我们探索构建 Graphiti 过程中遇到挑战的系列文章的开篇。阅读本文将加深您对 Graphiti 库的理解，并为未来的开发提供宝贵的见解。

Graphiti 是开源的，您可以在 GitHub 仓库中找到该项目的概述：**https://github.com/getzep/graphiti?ref=blog.getzep.com**

## 架构设计

Graphiti 的想法源于我们在使用简单事实三元组时遇到的局限性，尤其是在 Zep 中，Zep 是我们为大语言模型应用程序提供的长期记忆服务。我们意识到需要一个知识图谱来更复杂和结构化地处理事实和其他信息。这种方法使我们能够维护更全面的已摄取数据的上下文以及提取实体之间的关系。然而，我们仍然必须在图的结构和如何实现我们雄心勃勃的目标方面做出许多决定。

在研究基于大语言模型生成的知识图谱时，我们注意到了两篇论文：微软的 GraphRAG 本地到全球的论文（https://arxiv.org/pdf/2404.16130?ref=blog.getzep.com）和 AriGraph 论文（https://arxiv.org/pdf/2407.04363?ref=blog.getzep.com）。AriGraph 论文使用配备知识图谱的大语言模型来解决 TextWorld 问题——这些是基于文本的谜题，涉及房间导航、物品识别和物品使用。我们从 AriGraph 中获得的关键见解是其图谱的情节性记忆和语义记忆存储。

情节记忆存储了离散实例和事件的记忆，而语义节点则对实体及其关系进行建模，类似于微软的 GraphRAG 和传统的基于分类法的知识图谱。在 Graphiti 中，我们采用了这种方法，创建了两类不同的对象：情节节点与边，以及实体节点与边。

![](https://blog.getzep.com/content/images/2024/09/graphiti-blog-2-2024-09-11-231622.png)

在 Graphiti 中，情节节点包含情节的原始数据。情节是添加到图中的单个基于文本的事件——它可以是非结构化文本，如消息或文档段落，也可以是结构化的 JSON。情节节点保存来自该情节的内容，保留完整的上下文。

另一方面，实体节点代表从情节中提取的语义主体和客体。它们代表人、地点、事物和思想，并与它们的现实世界对应物一一对应。情节边表示情节节点和实体节点之间的关系：如果某个实体在特定情节中被提及，则这两个节点将有相应的情节边。最后，实体边表示两个实体节点之间的关系，并将相应的事实存储为属性。

举个例子：假设我们将情节“Preston: 我最喜欢的乐队是 Pink Floyd”添加到图中。我们会将“Preston”和“Pink Floyd”提取为实体节点，并在它们之间创建 `HAS_FAVORITE_BAND` 作为实体边。原始情节将作为情节节点的内容存储，并通过情节边将其连接到两个实体节点。`HAS_FAVORITE_BAND` 边还会将提取的事实“Preston 最喜欢的乐队是 Pink Floyd”作为属性存储。此外，实体节点存储了所有附加边的摘要，提供了预先计算的实体摘要。

![](https://blog.getzep.com/content/images/2024/09/Untitled-diagram-2024-09-11-215005.png)

这种知识图谱架构提供了一种灵活的方式来存储任意数据，同时尽可能多地保留上下文。然而，提取所有这些数据并不像看上去那么简单。使用大语言模型可靠且高效地提取这些信息是一个重大挑战。

## 大型提示词

在开发初期，我们使用了一个冗长的提示词来从情节中提取实体节点和边。这个提示词包括了先前情节和现有图数据库的额外上下文。（注意：系统提示词不包含在这些示例中。）先前的情节有助于确定实体名称（例如，解析代词），而现有的图架构则防止了实体或关系的重复。

简而言之，这个初始提示词：

- 提供了现有图的摘要作为输入
- 包含了当前情节和前 3 个情节的上下文
- 提供了时间戳作为参考
- 要求大语言模型以 JSON 格式提供新的节点和边
- 提供了 35 条关于设置字段和避免重复信息的指南

```text
Given the following graph summary, previous episodes, and new episode, extract new semantic nodes and edges that need to be added:
Current Graph Summary:

{graph_summary}

Previous Episodes Context (Last 3 episodes):

{context}

New Episode:

Text: {episode.text}

Reference Timestamp: {reference_time}

IMPORTANT: The reference timestamp provided above is the point in time from which all relative time expressions in the text should be interpreted. For example, if the text mentions "two years ago" and the reference timestamp is 2022-08-07, it means the event occurred in 2020-08-07.

IMPORTANT: When extracting new nodes and relationships, make sure to connect them to the existing graph structure whenever possible. Look for relationships between new elements and existing nodes. If a new node seems isolated, try to find a meaningful connection to at least one existing node.

Please provide your response in the following JSON format:

{
  "new_nodes": [
    {
      "name": "NodeName",
      "type": "SemanticNode",
      "properties": {
        "name": "NodeName",
        "region_summary": "Summary"
      }
    }
  ],
  "new_edges": [
    {
      "from": "SourceNodeName",
      "to": "TargetNodeName",
      "type": "RELATIONSHIP_TYPE",
      "properties": {
        "id": "UniqueID",
        "episodes": ["CurrentEpisodeName"],
        "fact": "Fact description",
        "valid_from": "YYYY-MM-DDTHH:MM:SSZ or null if not explicitly mentioned",
        "valid_to": "YYYY-MM-DDTHH:MM:SSZ or null if ongoing (meaning it is still truthy) or not explicitly mentioned"
      }
    }
  ]
}

Guidelines:

1. Use the previous episodes as context to better understand the current episode.
2. Extract new nodes and edges based on the content of the current episode, while considering context from previous episodes.
3. Identify and extract ALL key entities, concepts, or actors mentioned in the current episode, even if they seem implicit.
4. Ensure that any entity performing actions or being central to the current episode is represented as a node.
5. Create nodes for all important entities in the current episode, regardless of whether they already exist in the graph summary.
6. Focus on capturing the complete context of the current episode, including the subject of any actions or statements.
7. Create meaningful relationships between all relevant entities based on the current episode content.
8. Use descriptive and unique names for nodes that clearly represent the entity's role or nature.
9. Choose appropriate relationship types that accurately describe the interaction between nodes.
10. Ensure all required fields are filled for both nodes and edges.
11. For the "valid_from" field in edges, ONLY set a timestamp if a specific start time is explicitly mentioned in the text. If no start time is mentioned, use null. Do not infer or assume a start time.
12. For the "valid_to" field in edges, ONLY set a timestamp if an end time or duration is explicitly mentioned. Use null if the relationship is ongoing or no end time is specified.
13. Pay special attention to temporal expressions that indicate both the start and end of a relationship, such as "was married for 4 years and divorced 1 year ago".
14. Do not include transaction_from or transaction_to in your response. These will be handled separately.
15. Aim for clarity and completeness in your extractions while providing all necessary information.
16. If an actor (such as a user or system) is implied but not explicitly mentioned in the current episode, create a node for them as well.
17. Only create SemanticNode types. Do not create EpisodicNode types.
18. Prefer creating edges over nodes for representing actions, decisions, preferences, or any relational information.
19. When considering whether to create a node or an edge, ask yourself: "Can this concept exist independently, or is it primarily describing a relationship between other entities?" If it's the latter, create an edge instead of a node.
20. Capture implicit relationships by connecting specific instances to their general categories. For example, if a specific brand is mentioned, create a relationship between that brand and the general "Brand" concept.
21. Ensure important details about entities are captured either as properties of the relevant node or as separate nodes connected by appropriate edges.
22. Consider the context from previous episodes, but prioritize new or updated information from the current episode.
23. Pay special attention to hierarchical relationships. If an entity is a type or instance of a more general concept, make sure to create an edge representing this relationship.
24. When new entities are introduced, consider how they relate to existing entities and concepts in the graph. Create edges to represent these relationships.
25. IMPORTANT: Do not infer or assume any temporal information that is not explicitly stated in the text. If a start or end time is not mentioned, always use null for valid_from or valid_to respectively.
26. Ensure that new nodes are connected to at least one existing node whenever possible.
27. Look for implicit relationships between new and existing nodes based on context.
28. If a new node seems isolated, consider its relevance to the overall conversation and find a meaningful way to connect it to the existing structure.
29. If a new node truly represents a new concept with no clear connection to existing nodes, explain why it's important to add it as an isolated node.
30. Prefer creating direct relationships between entities over introducing intermediate nodes.
31. Keep the graph structure as simple as possible while accurately representing the information.
32. Avoid creating nodes for concepts that can be fully represented by relationships between existing entities.
33. When deciding between creating a node or an edge, choose the option that results in the most straightforward graph structure.
34. For events or status changes, focus on updating or creating relationships between involved entities rather than introducing new nodes.
35. Ensure each node represents a distinct entity or concept, not a relationship state or event.

IMPORTANT: Strive for a clean and efficient graph structure. Represent relationships and states through edges whenever possible, minimizing unnecessary nodes.
IMPORTANT: Do not recreate or duplicate existing relationships. Only add new information or update existing relationships when necessary.

Remember to capture all relevant information from the current episode while maintaining and strengthening connections to previously established concepts and entities.
```

这个提示词最初是作为原型创建的，因此我们从未期望它会进入 Graphiti 的发布版本。然而，这个提示词已经有许多积极的方面。最重要的是，它足够好地证明了我们在 Graphiti 上的想法是可行的，我们的愿景是可以实现的。

此外，这个提示词清楚地概述了将情节转化为相应图元素所需的步骤和上下文。提示词使用清晰的语言和详细的指南，尽量减少了响应中的歧义和混淆。最后，它使用了结构化的 JSON 输出，使我们能够更可靠地在代码中使用输出，而不会遇到格式错误。

然而，这个提示词有两个主要缺陷：1）它无法随着知识图谱的增长而扩展，2）它太长且令人困惑。扩展问题的出现是因为任何现实世界的数据库都将远远大于大语言模型的上下文窗口，因此需要找到一种方法来避免将整个图架构传递到提示词中。提示词的长度和复杂性导致了处理速度变慢，并且由于更频繁的幻觉和混淆，输出变得不太可预测。它也足够复杂，以至于像 GPT-4o-mini 和 Llama-3.1-70b 这样的中小型大语言模型难以提供高质量的结果。


## 关注点分离与提示词工程

在 Graphiti 中，大语言模型提供的输出用于构建我们的数据库，而不是为人类消费生成文本输出。这意味着结构和内容的一致性和可预测性至关重要。此外，我们在提示词中采用的关注点分离使我们能够同时运行多个提示词，大大减少了总的完成时间。

因此，我们应该像减少过长函数的复杂性一样，寻求减少代码库中提示词的复杂性。我们的策略类似：我们识别出所有要完成的任务，并将尽可能多的任务分离到各自的提示词或函数中。

考虑到这一点，我们可以将提示词分解为以下任务：

1. 从当前情节中提取实体
2. 与现有实体去重
3. 从情节中提取事实
4. 与现有事实（来自实体边）去重
5. 确定提取事实的时间
6. 使任何已失效的现有事实失效

![](https://blog.getzep.com/content/images/2024/09/Untitled-diagram-2024-09-11-232108.png)

在当前版本的 Graphiti 中，每个任务都有自己的独立提示词。这种分离不仅使我们的输出更快、更准确、更易于测试，还允许我们在任务之间没有直接依赖关系的情况下并行运行许多任务，从而显著加快了处理速度。我将介绍实体提取和去重提示词策略的演变过程。

实体提取提示词可能是我们所有提示词中最简单的。我们从最初的巨型提示词中得到的主要启示是，我们不再需要现有图的上下文：大语言模型已经非常擅长从任意文本中进行零样本实体提取。这意味着我们通过消除不必要的上下文进一步简化了提示词，只保留完成任务所需的内容：

```text
Given the following conversation, extract entity nodes from the CURRENT MESSAGE that are explicitly or implicitly mentioned:
Conversation:

{json.dumps([ep['content'] for ep in context['previous_episodes']], indent=2)}

<CURRENT MESSAGE>

{context["episode_content"]}

Guidelines:

1. ALWAYS extract the speaker/actor as the first node. The speaker is the part before the colon in each line of dialogue.

2. Extract other significant entities, concepts, or actors mentioned in the conversation.

3. Provide concise but informative summaries for each extracted node.

4. Avoid creating nodes for relationships or actions.

5. Avoid creating nodes for temporal information like dates, times or years (these will be added to edges later).

6. Be as explicit as possible in your node names, using full names and avoiding abbreviations.

Respond with a JSON object in the following format:

{
  "extracted_nodes": [
    {
      "name": "Unique identifier for the node (use the speaker's name for speaker nodes)",
      "labels": [
        "Entity",
        "Speaker for speaker nodes",
        "OptionalAdditionalLabel"
      ],
      "summary": "Brief summary of the node's role or significance"
    }
  ]
}
```

可以很快看出，这个提示词要简单得多，因此输出也更加可预测，使我们能够使用较小的大语言模型，并更容易针对特定任务进行提示词工程。

节点去重提示词的第一版也减少了其必要的上下文：既然我们已经从情节中提取了实体及其摘要，情节不再提供完成任务所需的必要上下文。此外，已经知道提取的节点是什么使我们能够解决图大小扩展问题：我们可以简单地从现有节点中提取与我们新提取节点最相似的节点，并让大语言模型找到任何重复项。我们通过混合搜索找到这些相似的节点，这意味着我们还可以将此提示词的最大上下文限制在相对较小的 Token 大小，因此该提示词不会随着图的大小无限线性扩展。提示词如下：

```text
Given the following context, deduplicate nodes from a list of new nodes given a list of existing nodes:
Existing Nodes:

{json.dumps(context['existing_nodes'], indent=2)}

New Nodes:

{json.dumps(context['extracted_nodes'], indent=2)}

Important:

If a node in the new nodes is describing the same entity as a node in the existing nodes, mark it as a duplicate!!!

Task:

If any node in New Nodes is a duplicate of a node in Existing Nodes, add their uuids to the output list

When finding duplicates nodes, synthesize their summaries into a short new summary that contains the

relevant information of the summaries of the new and existing nodes.

Guidelines:

1. Use both the name and summary of nodes to determine if they are duplicates,

duplicate nodes may have different names

2. In the output, uuid should always be the uuid of the New Node that is a duplicate. duplicate_of should be

the uuid of the Existing Node.

Respond with a JSON object in the following format:

{
  "duplicates": [
    {
      "uuid": "uuid of the new node like 5d643020624c42fa9de13f97b1b3fa39",
      "duplicate_of": "uuid of the existing node",
      "summary": "Brief summary of the node's role or significance. Takes information from the new and existing nodes"
    }
  ]
}
```

虽然这个提示词比我们的初始原型更简单，但任务和期望的输出仍然显得有些不直观。这可能会导致大语言模型的混淆和不一致的结果，这些结果可能是错误的，或者更为严重的是，如果大语言模型没有严格遵循所有提供的指南，可能会破坏我们的代码。为了进一步简化这个提示词，我决定写出我希望大语言模型执行的伪代码，然后倒推构建一个更好的提示词。以下是我起草的伪代码：

```python
for each node in extracted_nodes:
  for each existing_node in existing_nodes:
    if node is existing_node:
      return (existing_node.uuid, updated_summary)
```

当我检查这个伪代码时，我意识到第一个循环是完全确定的。通过为提取节点列表中的每个节点创建一个提示词来处理剩余任务，我们可以大大简化输出。这种方法进一步减少了提示词的上下文，因为我们只需要传递与要解析的新节点相似的现有节点。此外，我们可以并行运行每个去重提示词，从而加快结果的生成。这一见解引导我们创建了当前使用的节点去重提示词。

```text
Given the following context, determine whether the New Node represents any of the entities in the list of Existing Nodes.
Existing Nodes:

{json.dumps(context['existing_nodes'], indent=2)}

New Node:

{json.dumps(context['extracted_nodes'], indent=2)}

Task:

1. If the New Node represents the same entity as any node in Existing Nodes, return 'is_duplicate: true' in the

response. Otherwise, return 'is_duplicate: false'

2. If is_duplicate is true, also return the uuid of the existing node in the response

3. If is_duplicate is true, return a summary that synthesizes the information in the New Node summary and the

summary of the Existing Node it is a duplicate of.

Guidelines:

1. Use both the name and summary of nodes to determine if the entities are duplicates,

duplicate nodes may have different names

Respond with a JSON object in the following format:

{
  "is_duplicate": true,
  "uuid": "uuid of the existing node like 5d643020624c42fa9de13f97b1b3fa39 or null",
  "summary": "Brief summary of the node's role or significance. Takes information from the new and existing node"
}
```

这个提示词生成了更简单的输出，并且在实践中表现显著更好。边提取和去重提示词的演变过程类似，因此我在此不再详细介绍。然而，我鼓励感兴趣的读者在我们的 GitHub 代码库中探索它们。与我们的初始提示词相比，我们当前的架构提供了更准确且更易于测试的结果，并且速度更快。

## 结论

在本文中，我们初步探讨了在 Graphiti 开发过程中遇到的一些决策和挑战。我们探讨了在构建知识图谱时灵活和结构化架构的重要性、提示词工程的过程及其重要性，以及许多传统开发策略（如关注点分离）如何应用于提示词工程。我们还强调了速度和可扩展性在构建数据库的大语言模型项目中的关键作用。

在我们的下一篇文章中，我们将讨论 Graphiti 的一个关键差异化特性：它的一级时间架构，以及我们在实现它时遇到的挑战。希望您觉得本次讨论有所启发。如果这篇文章引起了您的兴趣，请查看我们的 GitHub。