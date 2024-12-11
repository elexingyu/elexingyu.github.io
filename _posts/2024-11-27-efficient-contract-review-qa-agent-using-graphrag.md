---
categories: articles
date: 2024-11-27
layout: post
style: huoshui
tags:
- AI
- 知识图谱
title: GraphRAG赋能合同审查：构建高效问答智能体指南
---

在这篇文章中，我们介绍了一种利用图检索增强生成（GraphRAG）方法的方案，以简化商业合同数据的处理过程，并构建一个问答智能体（Q&A Agent）。

这种方法与传统的检索增强生成（RAG）方法不同，其重点在于提高数据提取的效率，而不是像传统 RAG 那样不加区分地拆分和向量化整个文档。

在传统 RAG 方法中，每个文档都会被拆分成若干小块并向量化以供检索，这可能会导致大量不必要的数据被拆分、存储到向量索引中。然而，在这里，我们的重点是针对特定的用例（如商业合同审查）从每份合同中提取最相关的信息。这些数据随后被结构化为知识图谱，以组织关键实体和关系，从而通过 Cypher 查询（Neo4j 的查询语言）和向量搜索实现更精确的图数据检索。

通过减少向量化内容的数量并专注于提取高度相关的知识，这种方法提高了问答智能体的准确性和性能，使其适合处理复杂且特定领域的问题。

该方法包括四个阶段：通过目标信息提取（LLM + 提示词）创建知识图谱（LLM + Neo4j），再利用简单的图数据检索功能（Cypher、Text2Cypher、向量搜索），最终构建一个基于这些检索功能的问答智能体（Microsoft Semantic Kernel）。

下图展示了该方法的流程。

![四阶段GraphRAG方法](https://dist.neo4j.com/wp-content/uploads/20241125041920/graphrag-four-stage.png)

四阶段 GraphRAG 方法：从基于问题的提取 > 知识图谱模型 > GraphRAG 检索 > 问答智能体。图片由 Neo4j 的 Sebastian Nilsson 提供，经作者授权转载。

但在此之前，对于不熟悉商业法律的读者，让我们先简要介绍一下合同审查问题。

## 合同审查与大语言模型

商业合同审查是一项劳动密集型的工作，通常需要律师助理和初级律师仔细识别合同中的关键信息。

_“合同审查是指通过仔细阅读合同，了解签署方的权利和义务，并评估其相关影响的过程。”——Hendrycks, Burns 等，《NeurIPS 2021》，在_ _《CUAD：用于法律合同审查的专家注释 NLP 数据集》中。_

合同审查的第一阶段涉及审阅数百页的合同，以找到相关条款或义务。审查人员需要确定相关条款是否存在，如果存在，它们的内容是什么，并记录这些条款的位置。

_例如，他们需要判断合同是三年期还是一年期；确定合同的终止日期；判断某条款是否属于反转让条款或排他性条款等。”——Hendrycks, Burns 等，《NeurIPS 2021》，在_ _《CUAD：用于法律合同审查的专家注释 NLP 数据集》中。_

这是一项需要极大细致程度的任务，但往往效率低下，同时非常适合大语言模型的应用。

完成第一阶段后，高级法律从业者可以开始审查合同中的弱点和风险。这正是一个由大语言模型驱动、以知识图谱中的信息为基础的问答智能体可以成为法律专家得力助手的地方。

## 使用 LLM、函数调用和 GraphRAG 构建商业合同审查智能体的四步法

接下来的内容将描述这一过程的每一步。过程中，我将通过代码片段来说明主要思想。

四个步骤如下：

1. 从合同中提取相关信息（LLM + 合同）
2. 将提取的信息存储到知识图谱中（Neo4j）
3. 开发简单的知识图谱数据检索功能（Python）
4. 构建一个能够处理复杂问题的问答智能体（Semantic Kernel、LLM、Neo4j）

## 数据集

CUAD（Contract Understanding Atticus Dataset）是一个依据 CC BY 4.0 许可发布的公开数据集，包含 510 份法律合同中超过 13,000 条专家标注的条款，用于帮助构建用于合同审查的 AI 模型。它涵盖了许多重要的法律条款，如保密性、终止条款和赔偿条款，这些条款对于合同分析至关重要。

我们将使用该数据集中的三份合同，展示如何有效提取和分析关键法律信息，构建知识图谱并利用其进行精确的复杂问题回答。

这三份合同的总页数为 95 页。

## 第一步：从合同中提取相关信息

通过提示词让 LLM 从合同中提取精确信息并生成 JSON 输出，表示合同中的相关信息，这是一个相对简单的任务。

在商业审查中，可以设计提示词定位上述每个关键要素——当事方、日期、条款——并将它们整齐地总结为机器可读的 JSON 文件。

**提取提示词（简化版）**

> _仅使用此合同\[Contract.pdf\]中的信息回答以下问题：_
>
> _1）这是什么类型的合同？2）合同的当事方及其角色是什么？它们在哪注册成立？请列出州和国家（使用 ISO 3166 国家名称）。3）协议日期是什么？4）生效日期是什么？_
>
> _对于以下每种合同条款类型，提取两条信息：a）一个是/否，指示您是否认为该条款存在于合同中；b）一个列出指示该条款类型存在的摘录的列表。_
>
> _合同条款类型：竞争限制例外、竞业禁止条款、排他性条款、禁止招揽客户、禁止招揽员工、不得诋毁条款、方便终止条款、优先购买权条款、控制权变更条款、反转让条款、不设上限的责任条款、责任上限条款。_
>
> _请将最终答案以 JSON 文档的形式提供。_

请注意，上述部分展示的是提取提示词的简化版本。完整版本可以在此处查看。提示词的最后部分指定了 JSON 文档的格式，这对于确保一致的 JSON 模式输出非常有用。

在 Python 中，这项任务相对简单。以下`main()`函数旨在通过提取提示词（extraction_prompt），利用 OpenAI GPT-4o 从一组 PDF 合同文件中提取相关法律信息并将结果保存为 JSON 格式：

```
def main():
    pdf_files = [filename for filename in os.listdir('./data/input/') if filename.endswith('.pdf')]
    
    for pdf_filename in pdf_files:
        print('Processing ' + pdf_filename + '...')    
        # Extract content from PDF using the assistant
        complete_response = process_pdf('./data/input/' + pdf_filename)
        # Log the complete response to debug
        save_json_string_to_file(complete_response, './data/debug/complete_response_' + pdf_filename + '.json')

```

“_process_pdf_”函数使用 OpenAI GPT-4o，通过提取提示词从合同中提取知识：

```
 def process_pdf(pdf_filename):
    # Create OpenAI message thread
    thread = client.beta.threads.create()
    # Upload PDF file to the thread
    file = client.files.create(file=open(pdf_filename, "rb"), purpose="assistants")
    # Create message with contract as attachment and extraction_prompt
    client.beta.threads.messages.create(thread_id=thread.id,role="user",
        attachments=[
            Attachment(
                file_id=file.id, tools=[AttachmentToolFileSearch(type="file_search")])
        ],
        content=extraction_prompt,
    )
    # Run the message thread
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=pdf_assistant.id, timeout=1000)
    # Retrieve messages
    messages_cursor = client.beta.threads.messages.list(thread_id=thread.id)
    messages = [message for message in messages_cursor]
    # Return last message in Thread 
    return messages[0].content[0].text.value
```

对于每份合同，“process_pdf”返回的消息如下所示：

```
{
    "agreement": {
        "agreement_name": "Marketing Affiliate Agreement",
        "agreement_type": "Marketing Affiliate Agreement",
        "effective_date": "May 8, 2014",
        "expiration_date": "December 31, 2014",
        "renewal_term": "1 year",
        "Notice_period_to_Terminate_Renewal": "30 days",
        "parties": [
            {
                "role": "Company",
                "name": "Birch First Global Investments Inc.",
                "incorporation_country": "United States Virgin Islands",
                "incorporation_state": "N/A"
            },
            {
                "role": "Marketing Affiliate",
                "name": "Mount Knowledge Holdings Inc.",
                "incorporation_country": "United States",
                "incorporation_state": "Nevada"
            }
        ],
        "governing_law": {
            "country": "United States",
            "state": "Nevada",
            "most_favored_country": "United States"
        },
        "clauses": [
            {
                "clause_type": "Competitive Restriction Exception",
                "exists": false,
                "excerpts": []
            },
            {
                "clause_type": "Exclusivity",
                "exists": true,
                "excerpts": [
                    "Company hereby grants to MA the right to advertise, market and sell to corporate users, government agencies and educational facilities for their own internal purposes only, not for remarketing or redistribution."
                ]
            },
            {
                "clause_type": "Non-Disparagement",
                "exists": true,
                "excerpts": [
                    "MA agrees to conduct business in a manner that reflects favorably at all times on the Technology sold and the good name, goodwill and reputation of Company."
                ]
            },
            {
                "clause_type": "Termination For Convenience",
                "exists": true,
                "excerpts": [
                    "This Agreement may be terminated by either party at the expiration of its term or any renewal term upon thirty (30) days written notice to the other party."
                ]
            },
            {
                "clause_type": "Anti-Assignment",
                "exists": true,
                "excerpts": [
                    "MA may not assign, sell, lease or otherwise transfer in whole or in part any of the rights granted pursuant to this Agreement without prior written approval of Company."
                ]
            },
            
            {
                "clause_type": "Price Restrictions",
                "exists": true,
                "excerpts": [
                    "Company reserves the right to change its prices and/or fees, from time to time, in its sole and absolute discretion."
                ]
            },
            {
                "clause_type": "Minimum Commitment",
                "exists": true,
                "excerpts": [
                    "MA commits to purchase a minimum of 100 Units in aggregate within the Territory within the first six months of term of this Agreement."
                ]
            },
            
            {
                "clause_type": "IP Ownership Assignment",
                "exists": true,
                "excerpts": [
                    "Title to the Technology and all copyrights in Technology shall remain with Company and/or its Affiliates."
                ]
            },
            
            {
                "clause_type": "License grant",
                "exists": true,
                "excerpts": [
                    "Company hereby grants to MA the right to advertise, market and sell the Technology listed in Schedule A of this Agreement."
                ]
            },
            {
                "clause_type": "Non-Transferable License",
                "exists": true,
                "excerpts": [
                    "MA acknowledges that MA and its Clients receive no title to the Technology contained on the Technology."
                ]
            },
            {
                "clause_type": "Cap On Liability",
                "exists": true,
                "excerpts": [
                    "In no event shall Company be liable to MA, its Clients, or any third party for any tort or contract damages or indirect, special, general, incidental or consequential damages."
                ]
            },
            
            {
                "clause_type": "Warranty Duration",
                "exists": true,
                "excerpts": [
                    "Company's sole and exclusive liability for the warranty provided shall be to correct the Technology to operate in substantial accordance with its then current specifications."
                ]
            }
            
            
        ]
    }
}
```

## 第二步：创建知识图谱

现在，每份合同都已经转为 JSON 文件，下一步是将其创建为 Neo4j 中的知识图谱。

此时，花些时间设计数据模型是很有必要的。您需要考虑以下关键问题：

- 图谱中的节点和关系分别代表什么？
- 每个节点和关系的主要属性是什么？
- 是否需要对某些属性建立索引？
- 哪些属性需要向量嵌入以实现语义相似性搜索？

在我们的案例中，一个合适的设计（模式）包括以下主要实体：协议（合同）、其条款、作为协议方的组织以及它们之间的关系。

下图展示了该模式的可视化表示。

![模式的可视化表示](https://dist.neo4j.com/wp-content/uploads/20241125042042/commercial-contract-data-model.png)


```
Node properties:
Agreement {agreement_type: STRING, contract_id: INTEGER,
          effective_date: STRING, expiration_date: STRING,
          renewal_term: STRING, name: STRING}
ContractClause {name: STRING, type: STRING}
ClauseType {name: STRING}
Country {name: STRING}
Excerpt {text: STRING}
Organization {name: STRING}

Relationship properties:
IS_PARTY_TO {role: STRING}
GOVERNED_BY_LAW {state: STRING}
HAS_CLAUSE {type: STRING}
INCORPORATED_IN {state: STRING}
```

只有摘录——即在第一步中由 LLM 识别的短文本片段——需要文本嵌入。这种方法显著减少了表示每份合同所需的向量数量和向量索引的大小，使流程更高效、可扩展。

将每个 JSON 加载到具有上述模式的知识图谱中的 Python 脚本简化版本如下：

```
NEO4J_URI=os.getenv('NEO4J_URI', 'bolt://localhost:7687')
NEO4J_USER=os.getenv('NEO4J_USERNAME', 'neo4j')
NEO4J_PASSWORD=os.getenv('NEO4J_PASSWORD')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
JSON_CONTRACT_FOLDER = './data/output/'

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

contract_id = 1

json_contracts = [filename for filename in os.listdir(JSON_CONTRACT_FOLDER) if filename.endswith('.json')]
for json_contract in json_contracts:
  with open(JSON_CONTRACT_FOLDER + json_contract,'r') as file:
    json_string = file.read()
    json_data = json.loads(json_string)
    agreement = json_data['agreement']
    agreement['contract_id'] = contract_id
    driver.execute_query(CREATE_GRAPH_STATEMENT,  data=json_data)
    contract_id+=1

create_full_text_indices(driver)
driver.execute_query(CREATE_VECTOR_INDEX_STATEMENT)
print ("Generating Embeddings for Contract Excerpts...")
driver.execute_query(EMBEDDINGS_STATEMENT, token = OPENAI_API_KEY)
```

其中，唯一复杂的部分是“CREATE_GRAPH_STATEMENT”。这是一个 Cypher 语句，用于将合同 JSON 映射到知识图谱中的节点和关系。

完整的 Cypher 语句如下：

```
CREATE_GRAPH_STATEMENT = """
WITH $data AS data
WITH data.agreement as a

MERGE (agreement:Agreement {contract_id: a.contract_id})
ON CREATE SET 
  agreement.contract_id  = a.contract_id,
  agreement.name = a.agreement_name,
  agreement.effective_date = a.effective_date,
  agreement.expiration_date = a.expiration_date,
  agreement.agreement_type = a.agreement_type,
  agreement.renewal_term = a.renewal_term,
  agreement.most_favored_country = a.governing_law.most_favored_country
  //agreement.Notice_period_to_Terminate_Renewal = a.Notice_period_to_Terminate_Renewal

MERGE (gl_country:Country {name: a.governing_law.country})
MERGE (agreement)-[gbl:GOVERNED_BY_LAW]->(gl_country)
SET gbl.state = a.governing_law.state


FOREACH (party IN a.parties |
  // todo proper global id for the party
  MERGE (p:Organization {name: party.name})
  MERGE (p)-[ipt:IS_PARTY_TO]->(agreement)
  SET ipt.role = party.role
  MERGE (country_of_incorporation:Country {name: party.incorporation_country})
  MERGE (p)-[incorporated:INCORPORATED_IN]->(country_of_incorporation)
  SET incorporated.state = party.incorporation_state
)

WITH a, agreement, [clause IN a.clauses WHERE clause.exists = true] AS valid_clauses
FOREACH (clause IN valid_clauses |
  CREATE (cl:ContractClause {type: clause.clause_type})
  MERGE (agreement)-[clt:HAS_CLAUSE]->(cl)
  SET clt.type = clause.clause_type
  // ON CREATE SET c.excerpts = clause.excerpts
  FOREACH (excerpt IN clause.excerpts |
    MERGE (cl)-[:HAS_EXCERPT]->(e:Excerpt {text: excerpt})
  )
  //link clauses to a Clause Type label
  MERGE (clType:ClauseType{name: clause.clause_type})
  MERGE (cl)-[:HAS_TYPE]->(clType)
)"""
```

以下是该语句的分解。

### 数据绑定：

```
WITH $data AS data
WITH data.agreement as a
```

- `$data`是以 JSON 格式传递到查询中的输入数据，包含有关协议（合同）的信息。
- 第二行将`data.agreement`分配给别名`a`，以便在后续查询中引用合同详细信息。

### 插入或更新协议节点：

```
MERGE (agreement:Agreement {contract_id: a.contract_id})
ON CREATE SET 
  agreement.name = a.agreement_name,
  agreement.effective_date = a.effective_date,
  agreement.expiration_date = a.expiration_date,
  agreement.agreement_type = a.agreement_type,
  agreement.renewal_term = a.renewal_term,
  agreement.most_favored_country = a.governing_law.most_favored_country
```

- `MERGE`尝试查找具有指定 contract_id 的现有`Agreement`节点。如果不存在，则创建一个。
- ON CREATE SET 子句设置新创建的`Agreement`节点上的各种属性，例如`contract_id`、`agreement_name`、`effective_date`以及 JSON 输入中的其他协议相关字段。

### 创建适用法律关系：

```
MERGE (gl_country:Country {name: a.governing_law.country})
MERGE (agreement)-[gbl:GOVERNED_BY_LAW]->(gl_country)
SET gbl.state = a.governing_law.state
```

- 这会为与协议相关的适用法律国家创建或合并一个`Country`节点。
- 然后，在`Agreement`和`Country`之间创建或合并一个`GOVERNED_BY_LAW`关系。
- 它还设置了`GOVERNED_BY_LAW`关系的`state`属性。

### 创建当事方及注册地关系：

```
 FOREACH (party IN a.parties |
  MERGE (p:Organization {name: party.name})
  MERGE (p)-[ipt:IS_PARTY_TO]->(agreement)
  SET ipt.role = party.role
  MERGE (country_of_incorporation:Country {name: party.incorporation_country})
  MERGE (p)-[incorporated:INCORPORATED_IN]->(country_of_incorporation)
  SET incorporated.state = party.incorporation_state
)
```

对于合同中的每个当事方（`a.parties`）：

- 合并（或插入）一个代表当事方的`Organization`节点。
- 在`Organization`和`Agreement`之间创建一个`IS_PARTY_TO`关系，设置当事方的角色（例如：买方、卖方）。
- 为组织注册地的国家合并一个`Country`节点。
- 在组织和注册地国家之间创建一个`INCORPORATED_IN`关系，并设置注册地的州。

### 创建合同条款和摘录：

```
WITH a, agreement, [clause IN a.clauses WHERE clause.exists = true] AS valid_clauses
FOREACH (clause IN valid_clauses |
  CREATE (cl:ContractClause {type: clause.clause_type})
  MERGE (agreement)-[clt:HAS_CLAUSE]->(cl)
  SET clt.type = clause.clause_type
  FOREACH (excerpt IN clause.excerpts |
    MERGE (cl)-[:HAS_EXCERPT]->(e:Excerpt {text: excerpt})
  )
  MERGE (clType:ClauseType{name: clause.clause_type})
  MERGE (cl)-[:HAS_TYPE]->(clType)
)
```

- 此部分首先过滤条款列表（`a.clauses`），仅包括`clause.exists = true`的条款（即在第一步中由 LLM 识别出摘录的条款）。

对于每个条款：

- 创建一个`ContractClause`节点，其`name`和`type`分别对应于条款类型。
- 在`Agreement`和`ContractClause`之间建立一个`HAS_CLAUSE`关系。
- 对于与条款相关的每个`excerpt`，创建一个`Excerpt`节点，并通过`HAS_EXCERPT`关系将其链接到`ContractClause`。
- 最后，为条款类型创建（或合并）一个`ClauseType`节点，并通过`HAS_TYPE`关系将`ContractClause`链接到`ClauseType`。

运行导入脚本后，可以在 Neo4j 中将单个合同可视化为知识图谱。

![单个合同的知识图谱表示：绿色为当事方（组织），蓝色为合同条款，浅棕色为摘录，橙色为国家。图片由作者提供。](https://dist.neo4j.com/wp-content/uploads/20241125042101/knowledge-graph-representation-contract.png)



知识图谱中这三份合同仅需要一个小型图谱（少于 100 个节点和 200 个关系）。最重要的是，仅需要 40-50 个摘录的向量嵌入。这个带有少量向量的知识图谱现在可以用来支持一个功能强大的问答智能体。

## 第三步：为 GraphRAG 开发数据检索功能

合同现在已被结构化为知识图谱，下一步是创建一小组图数据检索功能。这些功能是开发问答智能体的核心构建块。

让我们定义一些基本的数据检索功能：

1. 检索合同的基本信息（通过合同 ID）。
2. 查找涉及特定组织的合同（通过组织名称的部分匹配）。
3. 查找不包含特定条款类型的合同。
4. 查找包含特定条款类型的合同。
5. 根据条款中的文本（摘录）与输入文本的语义相似性查找合同（例如：提到“禁止物品”的合同）。
6. 针对数据库中的所有合同运行自然语言查询——例如，统计“满足某些条件的合同数量”的聚合查询。

在第四步中，我们将使用 Microsoft Semantic Kernel 库构建一个问答智能体。该库简化了智能体的构建过程。开发者可以定义智能体可用的功能和工具，以便回答问题。

为了简化 Neo4j 与 Semantic Kernel 库之间的集成，我们定义了一个`ContractPlugin`，其中包含每个数据检索功能的“签名”。请注意每个功能的`@kernel_function`装饰器，以及为每个功能提供的类型信息和描述。

Semantic Kernel 使用“插件”类的概念来封装智能体可用的一组功能。它会使用这些装饰过的功能、类型信息和文档，向 LLM 函数调用功能提供智能体可用的功能信息：

```
from typing import List, Optional, Annotated
from AgreementSchema import Agreement, ClauseType
from semantic_kernel.functions import kernel_function
from ContractService import  ContractSearchService

class ContractPlugin:
    def __init__(self, contract_search_service: ContractSearchService ):
        self.contract_search_service = contract_search_service
    
    @kernel_function
    async def get_contract(self, contract_id: int) -> Annotated[Agreement, "A contract"]:
        """Gets details about a contract with the given id."""
        return await self.contract_search_service.get_contract(contract_id)

    @kernel_function
    async def get_contracts(self, organization_name: str) -> Annotated[List[Agreement], "A list of contracts"]:
        """Gets basic details about all contracts where one of the parties has a name similar to the given organization name."""
        return await self.contract_search_service.get_contracts(organization_name)
    
    @kernel_function
    async def get_contracts_without_clause(self, clause_type: ClauseType) -> Annotated[List[Agreement], "A list of contracts"]:
        """Gets basic details from contracts without a clause of the given type."""
        return await self.contract_search_service.get_contracts_without_clause(clause_type=clause_type)
    
    @kernel_function
    async def get_contracts_with_clause_type(self, clause_type: ClauseType) -> Annotated[List[Agreement], "A list of contracts"]:
        """Gets basic details from contracts with a clause of the given type."""
        return await self.contract_search_service.get_contracts_with_clause_type(clause_type=clause_type)

    @kernel_function
    async def get_contracts_similar_text(self, clause_text: str) -> Annotated[List[Agreement], "A list of contracts with similar text in one of their clauses"]:
        """Gets basic details from contracts having semantically similar text in one of their clauses to the to the 'clause_text' provided."""
        return await self.contract_search_service.get_contracts_similar_text(clause_text=clause_text)
    
    @kernel_function
    async def answer_aggregation_question(self, user_question: str) -> Annotated[str, "An answer to user_question"]:
        """Answer obtained by turning user_question into a CYPHER query"""
        return await self.contract_search_service.answer_aggregation_question(user_question=user_question)
```

建议探索包含上述功能实现的`ContractService`类。每个功能展示了不同的 GraphRAG 数据检索技术和模式。

让我们逐步了解这些功能的实现，因为它们展示了不同的 GraphRAG 数据检索技术和模式。

### 获取合同（通过合同 ID）——基于 Cypher 的检索功能

`get_contract(self, contract_id: int)`是一个异步方法，旨在使用 Cypher 查询从 Neo4j 数据库检索特定合同（`Agreement`）的详细信息。该功能返回一个`Agreement`对象，其中包含有关协议、条款、当事方及其关系的信息。

以下是该功能的实现：

```
async def get_contract(self, contract_id: int) -> Agreement:
        
        GET_CONTRACT_BY_ID_QUERY = """
            MATCH (a:Agreement {contract_id: $contract_id})-[:HAS_CLAUSE]->(clause:ContractClause)
            WITH a, collect(clause) as clauses
            MATCH (country:Country)-[i:INCORPORATED_IN]-(p:Organization)-[r:IS_PARTY_TO]-(a)
            WITH a, clauses, collect(p) as parties, collect(country) as countries, collect(r) as roles, collect(i) as states
            RETURN a as agreement, clauses, parties, countries, roles, states
        """
        
        agreement_node = {}
        
        records, _, _  = self._driver.execute_query(GET_CONTRACT_BY_ID_QUERY,{'contract_id':contract_id})

        if (len(records)==1):
            agreement_node =    records[0].get('agreement')
            party_list =        records[0].get('parties')
            role_list =         records[0].get('roles')
            country_list =      records[0].get('countries')
            state_list =        records[0].get('states')
            clause_list =       records[0].get('clauses')
        
        return await self._get_agreement(
            agreement_node, format="long",
            party_list=party_list, role_list=role_list,
            country_list=country_list,state_list=state_list,
            clause_list=clause_list
        )
```

最重要的组件是`**GET_CONTRACT_BY_ID_QUERY**`中的 Cypher 查询。此查询使用作为输入参数提供的 contract_id 执行。输出是匹配的协议及其条款和相关的当事方（每个当事方具有角色和注册地的国家/州）。

数据随后传递给`_get_agreement`实用函数，该函数将数据映射到“Agreement”。Agreement 是一个 TypedDict，定义如下：

```
class Agreement(TypedDict):  
    contract_id: int
    agreement_name: str
    agreement_type: str
    effective_date: str
    expiration_date: str
    renewal_term: str
    notice_period_to_terminate_Renewal: str
    parties: List[Party]
    clauses: List[ContractClause]
```

### 查找不包含特定条款类型的合同——另一个 Cypher 检索功能

此功能展示了知识图谱的一项强大功能，即测试关系的不存在。

`get_contracts_without_clause()`功能从 Neo4j 数据库中检索所有不包含特定类型条款的合同（`Agreements`）。该功能以`ClauseType`作为输入，并返回符合条件的`Agreement`对象列表。

此类数据检索信息无法通过向量搜索轻松实现。完整实现如下：

```
async def get_contracts_without_clause(self, clause_type: ClauseType) -> List[Agreement]:
        GET_CONTRACT_WITHOUT_CLAUSE_TYPE_QUERY = """
            MATCH (a:Agreement)
            OPTIONAL MATCH (a)-[:HAS_CLAUSE]->(cc:ContractClause {type: $clause_type})
            WITH a,cc
            WHERE cc is NULL
            WITH a
            MATCH (country:Country)-[i:INCORPORATED_IN]-(p:Organization)-[r:IS_PARTY_TO]-(a)
            RETURN a as agreement, collect(p) as parties, collect(r) as roles, collect(country) as countries, collect(i) as states
        """
       
        #run the Cypher query
        records, _ , _ = self._driver.execute_query(GET_CONTRACT_WITHOUT_CLAUSE_TYPE_QUERY,{'clause_type':clause_type.value})

        all_agreements = []
        for row in records:
            agreement_node =  row['agreement']
            party_list =  row['parties']
            role_list =  row['roles']
            country_list = row['countries']
            state_list = row['states']
            agreement : Agreement = await self._get_agreement(
                format="short",
                agreement_node=agreement_node,
                party_list=party_list,
                role_list=role_list,
                country_list=country_list,
                state_list=state_list
            )
            all_agreements.append(agreement)
        return all_agreements
```

格式与前一个功能类似。Cypher 查询`**GET_CONTRACTS_WITHOUT_CLAUSE_TYPE_QUERY**`定义了要匹配的节点和关系模式。它执行一个可选匹配，以过滤掉包含特定条款类型的合同，并收集有关协议的相关数据，例如涉及的当事方及其详细信息。

然后，该功能构建并返回一个`Agreement`对象列表，其中封装了每个匹配协议的所有相关信息。

### 查找具有语义相似文本的合同——向量搜索+图数据检索功能

`get_contracts_similar_text()`功能旨在查找包含与提供的`clause_text`文本相似条款的协议（合同）。它使用语义向量搜索来识别相关摘录，并遍历图谱以返回有关相应协议和条款的信息以及这些摘录的来源。

此功能利用定义在每个摘录“text”属性上的向量索引。它使用最近发布的 Neo4j GraphRAG 包来简化运行语义搜索+图遍历代码所需的 Cypher 代码：

```
async def get_contracts_similar_text(self, clause_text: str) -> List[Agreement]:

        #Cypher to traverse from the semantically similar excerpts back to the agreement
        EXCERPT_TO_AGREEMENT_TRAVERSAL_QUERY="""
            MATCH (a:Agreement)-[:HAS_CLAUSE]->(cc:ContractClause)-[:HAS_EXCERPT]-(node) 
            RETURN a.name as agreement_name, a.contract_id as contract_id, cc.type as clause_type, node.text as excerpt
        """
        
        #Set up vector Cypher retriever
        retriever = VectorCypherRetriever(
            driver= self._driver,  
            index_name="excerpt_embedding",
            embedder=self._openai_embedder, 
            retrieval_query=EXCERPT_TO_AGREEMENT_TRAVERSAL_QUERY,
            result_formatter=my_vector_search_excerpt_record_formatter
        )
        
        # run vector search query on excerpts and get results containing the relevant agreement and clause 
        retriever_result = retriever.search(query_text=clause_text, top_k=3)

        #set up List of Agreements (with partial data) to be returned
        agreements = []
        for item in retriever_result.items:
            //extract information from returned items and append agreement to results
            // full code not shown here but available on the Github repo
            

        return agreements
```

让我们了解此数据检索功能的主要组件：

- Neo4j GraphRAG VectorCypherRetriever 允许开发者在向量索引上执行语义相似性。在我们的案例中，对于每个通过语义相似性找到的“摘录”节点，使用额外的 Cypher 表达式来获取与该节点相关的其他节点。
- VectorCypherRetriever 的参数相对简单。`index_name`是运行语义相似性的向量索引。embedder 为文本生成向量嵌入。`driver`只是一个 Neo4j Python 驱动程序实例。`retrieval_query`指定了与每个“摘录”节点相关的其他节点和关系。
- `EXCERPT_TO_AGREEMENT_TRAVERSAL_QUERY`指定了要检索的其他节点。在这种情况下，对于每个摘录，我们检索其相关的合同条款及对应的协议。

```
 EXCERPT_TO_AGREEMENT_TRAVERSAL_QUERY="""
  MATCH (a:Agreement)-[:HAS_CLAUSE]->(cc:ContractClause)-[:HAS_EXCERPT]-(node) 
  RETURN a.name as agreement_name, a.contract_id as contract_id, cc.type as clause_type, node.text as excerpt
"""
```

### 运行自然语言查询——Text2Cypher 数据检索功能

`answer_aggregation_question()`功能利用 Neo4j GraphRAG 包的 Text2CypherRetriever 来回答自然语言中的问题。Text2CypherRetriever 使用 LLM 将用户问题转换为 Cypher 查询并在 Neo4j 数据库中运行。

该功能利用 GPT-4o 生成所需的 Cypher 查询。让我们逐步了解此数据检索功能的主要组件：

```
 async def answer_aggregation_question(self, user_question) -> str:
        answer = ""


        NEO4J_SCHEMA = """
            omitted for brevity (see below for the full value)
        """

        # Initialize the retriever
        retriever = Text2CypherRetriever(
            driver=self._driver,
            llm=self._llm,
            neo4j_schema=NEO4J_SCHEMA
        )

        # Generate a Cypher query using the LLM, send it to the Neo4j database, and return the results
        retriever_result = retriever.search(query_text=user_question)

        for item in retriever_result.items:
            content = str(item.content)
            if content:
                answer += content + '\n\n'

        return answer
```

此功能利用 Neo4j GraphRAG 包的 Text2CypherRetriever。它使用 LLM——在本例中是 OpenAI LLM——将用户问题（自然语言）转换为在数据库上执行的 Cypher 查询。查询结果将被返回。

确保 LLM 生成的查询使用数据库中定义的节点、关系和属性的关键要素是为 LLM 提供数据模型的文本描述。

在我们的案例中，使用以下数据模型表示法即可满足需求：

```
 NEO4J_SCHEMA = """
Node properties:
Agreement {agreement_type: STRING, contract_id: INTEGER,effective_date: STRING,renewal_term: STRING, name: STRING}
ContractClause {name: STRING, type: STRING}
ClauseType {name: STRING}
Country {name: STRING}
Excerpt {text: STRING}
Organization {name: STRING}

Relationship properties:
IS_PARTY_TO {role: STRING}
GOVERNED_BY_LAW {state: STRING}
HAS_CLAUSE {type: STRING}
INCORPORATED_IN {state: STRING}

The relationships:
(:Agreement)-[:HAS_CLAUSE]->(:ContractClause)
(:ContractClause)-[:HAS_EXCERPT]->(:Excerpt)
(:ContractClause)-[:HAS_TYPE]->(:ClauseType)
(:Agreement)-[:GOVERNED_BY_LAW]->(:Country)
(:Organization)-[:IS_PARTY_TO]->(:Agreement)
(:Organization)-[:INCORPORATED_IN]->(:Country)
  """
```

## 第四步：构建问答智能体

通过我们的知识图谱数据检索功能，我们已经准备好构建一个由 GraphRAG 支持的智能体。

让我们设置一个聊天机器人智能体，能够使用 GPT-4o、我们的数据检索功能以及 Neo4j 支持的知识图谱回答用户关于合同的问题。

我们将使用 Microsoft Semantic Kernel，一个允许开发者将 LLM 函数调用与现有 API 和数据检索功能集成的框架。

该框架使用“插件”概念来表示内核可以执行的特定功能。在我们的案例中，所有在“ContractPlugin”中定义的数据检索功能都可以被 LLM 用来回答问题。

该框架使用“内存”概念来存储用户和智能体之间的所有交互，以及执行的功能和检索到的数据。

一个极其简单的基于终端的智能体可以通过几行代码实现。以下代码片段展示了智能体的主要部分（省略了导入和环境变量）：

```
logging.basicConfig(level=logging.INFO)

# Initialize the kernel
kernel = Kernel()

# Add the Contract Search plugin to the kernel
contract_search_neo4j = ContractSearchService(NEO4J_URI,NEO4J_USER,NEO4J_PASSWORD)
kernel.add_plugin(ContractPlugin(contract_search_service=contract_search_neo4j),plugin_name="contract_search")

# Add the OpenAI chat completion service to the Kernel
kernel.add_service(OpenAIChatCompletion(ai_model_id="gpt-4o",api_key=OPENAI_KEY, service_id=service_id))

# Enable automatic function calling
settings: OpenAIChatPromptExecutionSettings = kernel.get_prompt_execution_settings_from_service_id(service_id=service_id)
settings.function_choice_behavior = FunctionChoiceBehavior.Auto(filters={"included_plugins": ["contract_search"]})

# Create a history of the conversation
history = ChatHistory()

async def basic_agent() :
    userInput = None
    while True:
        # Collect user input
        userInput = input("User > ")

        # Terminate the loop if the user says "exit"
        if userInput == "exit":
            break

        # Add user input to the history
        history.add_user_message(userInput)

        # 3. Get the response from the AI with automatic function calling
        chat_completion : OpenAIChatCompletion = kernel.get_service(type=ChatCompletionClientBase)
        result = (await chat_completion.get_chat_message_contents(
            chat_history=history,
            settings=settings,
            kernel=kernel,
            arguments=KernelArguments(),
        ))[0]

        # Print the results
        print("Assistant > " + str(result))

        # Add the message from the agent to the chat history
        history.add_message(result)

if __name__ == "__main__":
    asyncio.run(basic_agent())
```

让我们向智能体提出一些非平凡的问题。

**1\. 找到包含价格限制但没有保险条款的合同：**

```
Assistant > I found the following contract that contains a Price Restrictions clause but does not contain an Insurance clause:

- **Name:** Birch First Global Investments Inc. and Mount Knowledge Holdings Inc. MARKETING AFFILIATE AGREEMENT
- **Agreement Type:** MARKETING AFFILIATE AGREEMENT
- **Parties:**
  - **MOUNT KNOWLEDGE HOLDINGS INC.** (Marketing Affiliate), incorporated in Nevada, USA
  - **BIRCH FIRST GLOBAL INVESTMENTS INC.** (Company), incorporated in the Virgin Islands (VIR)

Would you like to know more details about this contract?
```

在这里，Semantic Agent 规划器审查了内核中可用的功能，并确定回答此问题需要调用两个功能，而单独一个功能无法提供完整答案。

首先，它执行“获取包含\[价格限制\]条款的合同”功能，然后执行“获取没有\[保险\]条款的合同”功能。规划器随后结合两个功能的结果以识别交集，最终得出正确答案。

如果查看调试信息，可以确认 LLM 执行的函数调用序列，以及每次调用消耗的 token 数量。注意两个数据检索功能的调用。

![调试信息](https://dist.neo4j.com/wp-content/uploads/20241125042150/debugging-information.png)

**2\. 是的，请提供更多细节：**

```
Assistant > Here are the detailed information about the contract:

### Contract Details:
- **Name:** Birch First Global Investments Inc. and Mount Knowledge Holdings Inc. MARKETING AFFILIATE AGREEMENT
- **Agreement Type:** MARKETING AFFILIATE AGREEMENT
- **Expiration Date:** December 31, 2014
- **Renewal Term:** One (1) year

### Parties Involved:
1. **MOUNT KNOWLEDGE HOLDINGS INC.** 
   - **Role:** Marketing Affiliate
   - **Incorporation Country:** USA
   - **Incorporation State:** Nevada
2. **BIRCH FIRST GLOBAL INVESTMENTS INC.**
   - **Role:** Company
   - **Incorporation Country:** Virgin Islands (VIR)

### Clauses Included:
- No-Solicit Of Employees
- Third Party Beneficiary
- Price Restrictions
- Affiliate License-Licensee
- Affiliate License-Licensor
- Cap On Liability
- Audit Rights
- Warranty Duration
- Post-Termination Services
- Non-Transferable License
- License grant
- IP Ownership Assignment
- Minimum Commitment
- Anti-Assignment
- Non-Disparagement

### Clauses Not Included:
- Insurance

Is there anything specific you would like to know or any particular clause details you are interested in?
```

在这种情况下，LLM 在后台使用了“通过 ID 查找合同”。您可能注意到，显示给用户的输出并未包括合同的 ID。然而，Semantic Kernel 在会话内存中存储了从先前调用的函数返回的所有信息！

这种智能体功能调用、内存使用以及用户查询自动映射到具有正确参数的函数调用的强大组合，解释了使用 Semantic Kernel 构建的智能体背后的“奥秘”。

**3\. 是否有任何合同提到可以不时更改价格的能力？**

```
Assistant > Yes, there is a contract that mentions 
the ability to make price changes from time to time. 
Here is the relevant excerpt:

1. **Birch First Global Investments Inc. and Mount Knowledge Holdings Inc. MARKETING AFFILIATE AGREEMENT**
   - **Contract ID:** 1
   - **Clause Type:** Price Restrictions
   - **Excerpt:**
     ```
     Company reserves the right to change its process and/or fees, from time to time, in its sole and absolute discretion. In the event of a price and/or fee change for Technology, Company shall notify MA in writing ninety (90) days prior to the effective date of any such change. All other prices and/or fees may be adjusted without prior notice to MA.
     ```

Would you like more information about this contract or any other details?
```

为了回答这个问题，Semantic Kernel 正在执行**get_contract_similar_text 数据**检索功能。

```
User > any contract mentions the ability to make price changes from time to time
INFO:semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion_base:processing 1 tool calls in parallel.

INFO:semantic_kernel.kernel:Calling contract_search-get_contracts_similar_text
 function with args: {"clause_text":"price changes from time to time"}


Assistant > Yes, there is a contract that mentions the ability to make price changes from time to time. Here is the relevant excerpt:

1. **Birch First Global Investments Inc. and Mount Knowledge Holdings Inc. MARKETING AFFILIATE AGREEMENT**
   - **Contract ID:** 1
   - **Clause Type:** Price Restrictions
   - **Excerpt:**
     ```
     Company reserves the right to change its process and/or fees, from time to time, in its sole and absolute discretion. In the event of a price and/or fee change for Technology, Company shall notify MA in writing ninety (90) days prior to the effective date of any such change. All other prices and/or fees may be adjusted without prior notice to MA.
     ```

```

如前所述，此功能使用向量搜索和 Cypher 查询，不仅检索语义相似的摘录，还检索包含这些摘录的相关合同和条款。

最后，让我们问数据库中有多少份合同。

**4\. 数据库中有多少份合同？**

此问题需要 LLM 使用 Text2Cypher 数据检索器：

```
Assistant > There are a total of 3 contracts in the database.
```

调试信息确认 Semantic Kernel 使用“user_question” = “数据库中有多少份合同？”运行了 Text2Cypher 数据检索功能。

```
User >  how many contracts are there on the database?
INFO:httpx:HTTP Request: POST https://api.openai.com/v1/chat/completions "HTTP/1.1 200 OK"
INFO:semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion_base:processing 1 tool calls in parallel.

INFO:semantic_kernel.kernel:Calling contract_search-answer_aggregation_question function 
with args: {"user_question":"How many contracts are there in the database?"}


INFO:semantic_kernel.functions.kernel_function:Function completed. Duration: 0.588805s

INFO:semantic_kernel.connectors.ai.open_ai.services.open_ai_handler:OpenAI usage: CompletionUsage(completion_tokens=13, prompt_tokens=3328, total_tokens=3341, completion_tokens_details={'reasoning_tokens': 0})

Assistant > There are a total of 3 contracts in the database.
```

## 自己试试

GitHub 仓库（https://github.com/neo4j-product-examples/graphrag-contract-review）包含一个提供更优雅智能体 UI 的 Streamlit 应用程序。鼓励您与智能体交互，并对 ContractPlugin 进行更改，以便您的智能体能够处理更多问题。

## 结论

在本篇博文中，我们探索了一种 GraphRAG 方法，将商业合同审查的劳动密集型任务转变为更高效的 AI 驱动流程。

通过专注于使用 LLM 和提示词进行目标信息提取，构建基于 Neo4j 的结构化知识图谱，实施简单的数据检索功能，最终开发问答智能体，我们创建了一个能够有效处理复杂问题的智能解决方案。

这种方法减少了传统基于向量搜索的 RAG 中存在的低效问题，而是专注于提取相关信息，降低了对不必要向量嵌入的需求，同时简化了整体流程。希望从合同数据处理到交互式问答智能体的这一旅程能够激发您利用 GraphRAG 实现更高效、更智能的 AI 驱动决策。

立即开始构建您自己的商业合同审查智能体，亲身体验 GraphRAG 的强大功能吧！