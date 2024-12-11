---
layout: post
title: 如何提高RAG系统准确率？12大常见痛点及巧妙解！
date: 2024-11-23
author: 活水智能
categories: ['articles']
tags: ['AI', '知识图谱']
style: huoshui
---

作者：Wenqi Glantz

编译：活水智能

· 痛点 1：缺失内容  
· 痛点 2：未能捕获排名靠前的文档  
· 痛点 3：上下文不相关——整合策略的局限性  
· 痛点 4：未提取内容  
· 痛点 5：格式错误  
· 痛点 6：特异性不准确  
· 痛点 7：内容不完整  
· 痛点 8：数据摄取的可扩展性  
· 痛点 9：结构化数据质量检查  
· 痛点 10：复杂 PDF 的数据提取  
· 痛点 11：后备模型  
· 痛点 12：大语言模型的安全性

受 Barnett 等人在论文《构建检索增强生成系统的七个失败点》启发，本文将探讨论文中提到的七个失败点，以及开发 RAG（检索增强生成）管道中常见的五个额外痛点。更重要的是，我们将深入研究这些 RAG 痛点的解决方案，以便在日常 RAG 开发中更好地应对这些挑战。

我使用“痛点”而非“失败点”，主要是因为这些痛点都有相应的解决方案。如果我们能够提前解决这些问题，就可以防止它们在 RAG 管道中成为失败点。

首先，让我们分析上述论文中提出的七个痛点（见下图）。然后，我们将补充五个额外的痛点及其解决方案。

![图片来源：《构建检索增强生成系统的七个失败点》](https://miro.medium.com/v2/resize:fit:700/0*5pAddwy6ZAElg1hk)

## 痛点 1：缺失内容

当知识库中没有实际答案时，RAG 系统可能会提供一个看似合理但实际上错误的答案，而不是直接表明它不知道答案。这会导致用户收到误导性信息，从而感到沮丧。

我们提出了两个解决方案：

#### 清理数据

“垃圾进，垃圾出。”如果源数据质量较差，例如包含矛盾信息，那么无论 RAG 管道设计得多么精良，都无法将垃圾数据转化为有价值的输出数据。这一解决方案不仅适用于本痛点，也适用于本文列出的所有痛点。干净的数据是任何高效 RAG 管道的前提条件。

#### 更优的提示词设计

设计更优提示词可以显著减少因知识库信息不足而导致的错误答案。例如，可以使用类似“如果不确定答案，请告诉我你不知道”的提示词，鼓励模型承认其局限性，并更透明地传达不确定性。虽然无法保证 100% 的准确性，但在清理数据之后，设计提示词是你可以采取的最佳措施之一。

## 痛点 2：未能捕获排名靠前的文档

系统检索组件返回的结果中，可能未包含关键文档。这会导致正确答案被忽略，进而使系统无法提供准确的响应。论文中提到：“问题的答案存在于文档中，但由于排名不足，未能返回给用户。”

以下是两个解决方案：

#### 调整 `chunk_size` 和 `similarity_top_k` 的超参数

`chunk_size` 和 `similarity_top_k` 是用于管理 RAG 模型数据检索过程效率和效果的参数。调整这些参数可以影响计算效率与检索信息质量之间的权衡。我们在之前的文章《使用 LlamaIndex 自动化超参数调优》中详细探讨了 `chunk_size` 和 `similarity_top_k` 的超参数调优。以下是示例代码片段：

```makefile
param_tuner = ParamTuner(
    param_fn=objective_function_semantic_similarity,
    param_dict=param_dict,
    fixed_param_dict=fixed_param_dict,
    show_progress=True,
)
results = param_tuner.tune()
```

其中，`objective_function_semantic_similarity` 函数定义如下，`param_dict` 包含需要调优的参数 `chunk_size` 和 `top_k` 及其对应的候选值：

```python
# 包含需要调优的参数
param_dict = {"chunk_size": [256, 512, 1024], "top_k": [1, 2, 5]}
# 包含调优过程中保持固定的参数
fixed_param_dict = {
    "docs": documents,
    "eval_qs": eval_qs,
    "ref_response_strs": ref_response_strs,
}

def objective_function_semantic_similarity(params_dict):
    chunk_size = params_dict["chunk_size"]
    docs = params_dict["docs"]
    top_k = params_dict["top_k"]
    eval_qs = params_dict["eval_qs"]
    ref_response_strs = params_dict["ref_response_strs"]

    # 构建索引
    index = _build_index(chunk_size, docs)
    # 查询引擎
    query_engine = index.as_query_engine(similarity_top_k=top_k)
    # 获取预测响应
    pred_response_objs = get_responses(
        eval_qs, query_engine, show_progress=True
    )
    # 运行评估器
    eval_batch_runner = _get_eval_batch_runner_semantic_similarity()
    eval_results = eval_batch_runner.evaluate_responses(
        eval_qs, responses=pred_response_objs, reference=ref_response_strs
    )
    # 获取语义相似性指标
    mean_score = np.array(
        [r.score for r in eval_results["semantic_similarity"]]
    ).mean()
    return RunResult(score=mean_score, params=params_dict)
```

更多细节请参考 LlamaIndex 提供的完整超参数优化笔记本。

#### 重排序（Reranking）

在将检索结果传递给大语言模型之前，对它们进行重排序显著提升了 RAG 的性能。LlamaIndex 提供的笔记本展示了以下两种情况的差异：

- 未使用重排序器时仅直接检索排名前两位节点，结果不准确。
- 使用 `CohereRerank` 对前十位节点进行重排序后返回排名前两位节点，结果更准确。

```makefile
import os
from llama_index.postprocessor.cohere_rerank import CohereRerank

api_key = os.environ["COHERE_API_KEY"]
cohere_rerank = CohereRerank(api_key=api_key, top_n=2)  # 返回重排序后的前两位节点

query_engine = index.as_query_engine(
    similarity_top_k=10,  # 设置较高的 top_k 以确保最大化相关检索
    node_postprocessors=[cohere_rerank],  # 将重排序器传递给节点后处理器
)

response = query_engine.query(
    "What did Sam Altman do in this essay?",
)
```

此外，可以通过使用不同嵌入模型和重排序器来评估和增强检索器性能，详情请参考 Ravi Theja 的文章《Boosting RAG: Picking the Best Embedding & Reranker Models》。

更进一步，还可以通过微调自定义重排序器来提升检索性能，具体实现详见 Ravi Theja 的文章《Improving Retrieval Performance by Fine-tuning Cohere Reranker with LlamaIndex》。

## 痛点 3：上下文不相关——整合策略的局限性

论文将此问题定义为：“数据库中检索到包含答案的文档，但未被纳入生成答案的上下文中。这通常发生在数据库返回许多文档，并且在整合过程中未能提取到答案时。”

除了前述提到的重排序器和微调重排序器外，还可以探索以下解决方案：

#### 调整检索策略

LlamaIndex 提供了一系列从基础到高级的检索策略，帮助我们在 RAG 管道中实现更准确的检索。请参阅其检索模块指南，了解所有检索策略的完整列表及分类：

- 基础检索
- 高级检索与搜索
- 自动检索
- 知识图谱检索器
- 复合/分层检索器
- 以及更多！

#### 微调嵌入模型

如果使用开源嵌入模型，微调嵌入模型是实现更准确检索的绝佳方式。LlamaIndex 提供了微调开源嵌入模型的分步指南，证明通过微调嵌入模型可以在多种评估指标上实现一致的性能提升。

以下是创建微调引擎、运行微调并获取微调模型的示例代码：

```makefile
finetune_engine = SentenceTransformersFinetuneEngine(
    train_dataset,
    model_id="BAAI/bge-small-en",
    model_output_path="test_model",
    val_dataset=val_dataset,
)
finetune_engine.finetune()
embed_model = finetune_engine.get_finetuned_model()
```

## 痛点 4：未能提取正确答案

系统在从提供的上下文中提取正确答案时表现不佳，尤其是在信息过载的情况下。关键细节经常被遗漏，从而降低了响应的质量。论文中提到：“当上下文中存在过多噪声或矛盾信息时，会发生这种情况。”

以下是三个建议的解决方案：

#### 清理数据

这个痛点是糟糕数据的典型受害者。我们无法过分强调干净数据的重要性！在责怪 RAG（检索增强生成）管道之前，请先花时间清理数据。

#### 提示词压缩

在 LongLLMLingua 研究项目/论文中，引入了长上下文场景下的提示词压缩技术。通过与 LlamaIndex 的集成，我们现在可以将 LongLLMLingua 作为节点后处理器来实现，该节点将在检索步骤之后压缩上下文，然后再将其输入到大语言模型（LLM）中。

以下是一个代码示例，展示了如何设置 `LongLLMLinguaPostprocessor`，该处理器使用 `longllmlingua` 包来运行提示词压缩。

想了解更多详情，请查看关于 LongLLMLingua 的完整笔记本。

```python
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.response_synthesizers import CompactAndRefine
from llama_index.postprocessor import LongLLMLinguaPostprocessor
from llama_index.schema import QueryBundle

node_postprocessor = LongLLMLinguaPostprocessor(
    instruction_str="根据上下文，请回答最终问题",
    target_token=300,
    rank_method="longllmlingua",
    additional_compress_kwargs={
        "condition_compare": True,
        "condition_in_question": "after",
        "context_budget": "+100",
        "reorder_context": "sort",  # 启用上下文重新排序
    },
)

retrieved_nodes = retriever.retrieve(query_str)
synthesizer = CompactAndRefine()

# 清晰展示 RetrieverQueryEngine 的步骤：
# 后处理（压缩），综合处理
new_retrieved_nodes = node_postprocessor.postprocess_nodes(
    retrieved_nodes, query_bundle=QueryBundle(query_str=query_str)
)

print("\n\n".join([n.get_content() for n in new_retrieved_nodes]))
response = synthesizer.synthesize(query_str, new_retrieved_nodes)
```

#### 长上下文重新排序

研究发现，当关键数据位于输入上下文的开头或结尾时，性能通常最佳。`LongContextReorder` 旨在通过重新排序检索到的节点解决这种“丢失在中间”的问题，这在需要大规模 top-k 检索时尤其有帮助。

以下是一个代码示例，展示了如何在查询引擎构建过程中将 `LongContextReorder` 定义为 `node_postprocessor`。想了解更多详情，请参考 LlamaIndex 关于 `LongContextReorder` 的完整笔记本。

```python
from llama_index.postprocessor import LongContextReorder

reorder = LongContextReorder()
reorder_engine = index.as_query_engine(
    node_postprocessors=[reorder],
    similarity_top_k=5
)

reorder_response = reorder_engine.query("作者是否见过 Sam Altman？")
```

---

## 痛点 5：格式错误

当指示以特定格式（如表格或列表）提取信息时，大语言模型（LLM）可能忽略这些要求。以下是四个建议的解决方案：

#### 更好的提示词

以下是一些改进提示词的策略，以解决此问题：

- 明确说明要求。
- 简化请求并使用关键词。
- 提供示例。
- 使用迭代提示词并提出后续问题。

#### 输出解析

输出解析可以通过以下方式帮助确保所需的输出格式：

- 为任何提示词/查询提供格式化指令。
- 为 LLM 输出提供“解析”功能。

LlamaIndex 支持与其他框架（如 Guardrails 和 LangChain）提供的输出解析模块集成。

以下是一个使用 LangChain 输出解析模块的代码示例，可在 LlamaIndex 中使用。想了解更多详情，请查看 LlamaIndex 文档中关于输出解析模块的说明。

```python
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.output_parsers import LangchainOutputParser
from llama_index.llms import OpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

# 加载文档，构建索引
documents = SimpleDirectoryReader("../paul_graham_essay/data").load_data()
index = VectorStoreIndex.from_documents(documents)

# 定义输出模式
response_schemas = [
    ResponseSchema(
        name="Education",
        description="描述作者的教育经历/背景。",
    ),
    ResponseSchema(
        name="Work",
        description="描述作者的工作经历/背景。",
    ),
]

# 定义输出解析器
lc_output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
output_parser = LangchainOutputParser(lc_output_parser)

# 将输出解析器附加到 LLM
llm = OpenAI(output_parser=output_parser)

# 从 LlamaIndex 获取结构化响应
from llama_index import ServiceContext
ctx = ServiceContext.from_defaults(llm=llm)
query_engine = index.as_query_engine(service_context=ctx)
response = query_engine.query("作者小时候做过哪些事情？")
print(str(response))
```

#### Pydantic 程序

Pydantic 程序是一种通用框架，可将输入字符串转换为结构化的 Pydantic 对象。LlamaIndex 提供了几种类别的 Pydantic 程序：

- **LLM 文本补全 Pydantic 程序**：这些程序处理输入文本，并利用文本补全 API 和输出解析将其转换为用户定义的结构化对象。
- **LLM 函数调用 Pydantic 程序**：这些程序通过 LLM 函数调用 API，将输入文本转换为用户指定的结构化对象。
- **预打包 Pydantic 程序**：这些程序旨在将输入文本转换为预定义的结构化对象。

以下是一个来自 OpenAI Pydantic 程序的代码示例。想了解更多详情，请查看 LlamaIndex 文档中关于 Pydantic 程序的说明。

```python
from pydantic import BaseModel
from typing import List
from llama_index.program import OpenAIPydanticProgram

# 定义输出模式（无文档字符串）
class Song(BaseModel):
    title: str
    length_seconds: int

class Album(BaseModel):
    name: str
    artist: str
    songs: List[Song]

# 定义 OpenAI Pydantic 程序
prompt_template_str = """\
生成一个专辑示例，包括一位艺术家和一首歌曲列表。\
以电影 {movie_name} 为灵感。\
"""

program = OpenAIPydanticProgram.from_defaults(
    output_cls=Album,
    prompt_template_str=prompt_template_str,
    verbose=True
)

# 运行程序以获取结构化输出
output = program(
    movie_name="闪灵",
    description="专辑数据模型。"
)
```

#### OpenAI JSON 模式

OpenAI JSON 模式允许我们将 `response_format` 设置为 `{ "type": "json_object" }`，以启用 JSON 响应模式。当启用 JSON 模式时，模型仅生成可以解析为有效 JSON 对象的字符串。虽然 JSON 模式可以强制输出格式，但它无法验证输出是否符合特定的模式。想了解更多详情，请查看 LlamaIndex 文档中关于 OpenAI JSON 模式和函数调用的说明。

---

## 痛点 6：缺乏细节

响应可能缺乏必要的细节或具体性，通常需要后续查询以澄清问题。答案可能过于模糊或笼统，无法有效满足用户需求。

我们可以通过高级检索策略来解决此问题。

#### 高级检索策略

当答案不符合预期的粒度水平时，可以改进检索策略。以下是一些可能有助于解决此痛点的高级检索策略：

- 小到大检索。
- 句子窗口检索。
- 递归检索。

请查看我的上一篇文章《用高级检索 LlamaPacks 启动你的 RAG 管道，并通过 Lighthouz AI 进行基准测试》，了解有关七种高级检索 LlamaPacks 的更多详情。

---

## 痛点 7：不完整

虽然部分响应并非错误，但它们未能提供所有细节，尽管这些信息在上下文中是存在且可访问的。例如，如果有人问：“文档 A、B 和 C 中讨论的主要方面是什么？”更有效的方法可能是分别询问每个文档，以确保答案全面。

#### 查询转换

比较类问题在简单的 RAG 方法中表现尤其糟糕。改进 RAG 推理能力的一个好方法是添加查询理解层——在实际查询向量存储之前进行查询转换。以下是四种不同的查询转换方法：

- **路由**：保留初始查询，同时确定其适用的工具子集，并将这些工具指定为合适选项。
- **查询重写**：保留选定的工具，但以多种方式重写查询，以便在同一组工具中应用。
- **子问题**：将查询分解为多个小问题，每个问题针对不同的工具（根据其元数据确定）。
- **ReAct Agent 工具选择**：基于原始查询，确定要使用的工具，并制定在该工具上运行的具体查询。

以下是一个关于如何使用 HyDE（假设文档嵌入）的代码示例，这是一种查询重写技术。给定一个自然语言查询，首先生成一个假设文档/答案。然后使用该假设文档进行嵌入查找，而不是直接使用原始查询。

```makefile
# 加载文档，构建索引
documents = SimpleDirectoryReader("../paul_graham_essay/data").load_data()
index = VectorStoreIndex(documents)

# 使用 HyDE 查询转换运行查询
query_str = "保罗·格雷厄姆在 RISD 之后做了什么？"
hyde = HyDEQueryTransform(include_original=True)
query_engine = index.as_query_engine()
query_engine = TransformQueryEngine(query_engine, query_transform=hyde)
response = query_engine.query(query_str)
print(response)
```

想了解所有细节，请查看 LlamaIndex 的《查询转换手册》。

此外，请阅读 Iulia Brezeanu 的精彩文章《用高级查询转换改进 RAG》，了解查询转换技术的详细信息。

上述痛点均来自论文。接下来，我们将探讨 RAG 开发中常见的五个额外痛点及其建议的解决方案。

## 痛点 8：数据摄取的可扩展性

RAG（检索增强生成）管道中的数据摄取可扩展性问题是指系统在高效管理和处理大规模数据时遇到的挑战，导致性能瓶颈甚至系统故障。这类问题可能引发摄取时间过长、系统过载、数据质量问题以及可用性受限等后果。

#### 并行化摄取管道

LlamaIndex 提供了摄取管道的并行处理功能，使文档处理速度提升至最多 15 倍。以下是如何创建 `IngestionPipeline` 并指定 `num_workers` 来启用并行处理的示例代码。有关更多详细信息，请参阅 LlamaIndex 的完整笔记本。

```python
# 加载数据
documents = SimpleDirectoryReader(input_dir="./data/source_files").load_data()

# 创建具有转换功能的管道
pipeline = IngestionPipeline(
    transformations=[
        SentenceSplitter(chunk_size=1024, chunk_overlap=20),
        TitleExtractor(),
        OpenAIEmbedding(),
    ]
)

# 将 num_workers 设置为大于 1 的值以启用并行执行
nodes = pipeline.run(documents=documents, num_workers=4)
```

---

## 痛点 9：结构化数据问答

准确解析用户查询以检索相关的结构化数据可能非常困难，尤其是在面对复杂或模糊的查询、不够灵活的文本到 SQL 转换，以及当前大语言模型在处理此类任务时的局限性。

LlamaIndex 提供了两种解决方案。

#### Chain-of-table Pack

`ChainOfTablePack` 是基于 Wang 等人提出的创新性“chain-of-table”论文的 LlamaPack。该方法结合了 chain-of-thought（思维链）的概念与表格转换和表示，逐步使用一组受限的操作对表格进行转换，并在每个阶段将修改后的表格呈现给大语言模型。这种方法的显著优势在于，它能够通过系统地切分和处理数据，解决涉及复杂表格单元（包含多条信息）的查询，从而提升表格问答的效果。

有关如何使用 `ChainOfTablePack` 查询结构化数据的更多信息，请参阅 LlamaIndex 的完整笔记本。

#### Mix-Self-Consistency Pack

大语言模型可以通过两种主要方式对表格数据进行推理：

- 直接提示的文本推理
- 通过程序生成（例如 Python、SQL 等）的符号推理

基于 Liu 等人发表的论文《Rethinking Tabular Data Understanding with Large Language Models》，LlamaIndex 开发了 `MixSelfConsistencyQueryEngine`，该引擎通过自一致性机制（即多数投票）聚合文本推理和符号推理的结果，从而实现了最先进的性能。以下是示例代码。更多详细信息请参阅 LlamaIndex 的完整笔记本。

```python
download_llama_pack(
    "MixSelfConsistencyPack",
    "./mix_self_consistency_pack",
    skip_load=True,
)

query_engine = MixSelfConsistencyQueryEngine(
    df=table,
    llm=llm,
    text_paths=5,  # 采样 5 条文本推理路径
    symbolic_paths=5,  # 采样 5 条符号推理路径
    aggregation_mode="self-consistency",  # 通过自一致性机制聚合文本和符号路径的结果（即多数投票）
    verbose=True,
)

response = await query_engine.aquery(example["utterance"])
```

---

## 痛点 10：从复杂 PDF 中提取数据

您可能需要从复杂的 PDF 文档（例如嵌入的表格）中提取数据以进行问答。简单的检索方法无法获取这些嵌入表格中的数据，因此需要更好的方法来检索此类复杂的 PDF 数据。

#### 嵌入表格检索

LlamaIndex 提供了 `EmbeddedTablesUnstructuredRetrieverPack`，这是一个 LlamaPack，利用 Unstructured.io 解析 HTML 文档中的嵌入表格，构建节点图，并通过递归检索索引/检索基于用户问题的表格。

需要注意的是，该包接受 HTML 文档作为输入。如果您的文档是 PDF 格式，可以先使用 pdf2htmlEX 将 PDF 转换为 HTML 格式，而不会丢失文本或格式。以下是下载、初始化和运行 `EmbeddedTablesUnstructuredRetrieverPack` 的示例代码。

```python
# 下载并安装依赖
EmbeddedTablesUnstructuredRetrieverPack = download_llama_pack(
    "EmbeddedTablesUnstructuredRetrieverPack",
    "./embedded_tables_unstructured_pack",
)

# 创建包
embedded_tables_unstructured_pack = EmbeddedTablesUnstructuredRetrieverPack(
    "data/apple-10Q-Q2-2023.html",  # 接受 HTML 文件，如果文档是 PDF 格式，请先转换为 HTML
    nodes_save_path="apple-10-q.pkl"
)

# 运行包
response = embedded_tables_unstructured_pack.run("What's the total operating expenses?").response
display(Markdown(f"{response}"))
```

---

## 痛点 11：备用模型

在使用大语言模型时，您可能会担心模型出现问题，例如 OpenAI 模型的速率限制错误。为此，您需要备用模型作为主要模型出现故障时的备选方案。

两种建议的解决方案：

#### Neutrino 路由器

Neutrino 路由器是一组 LLM，您可以将查询路由到其中。它使用预测模型智能地将查询路由到最适合提示词的 LLM，从而在优化性能的同时降低成本和延迟。Neutrino 当前支持十几种模型。如果您希望添加新的模型到支持列表中，可以联系其支持团队。

您可以在 Neutrino 仪表板中创建路由器以手动选择首选模型，或者使用包含所有支持模型的“默认”路由器。

LlamaIndex 已通过 `llms` 模块中的 `Neutrino` 类集成了 Neutrino 支持。以下是代码示例。更多详细信息请参阅 Neutrino AI 页面。

```python
from llama_index.llms import Neutrino
from llama_index.llms import ChatMessage

llm = Neutrino(
    api_key="<your-Neutrino-api-key>",
    router="test"  # 在 Neutrino 仪表板中配置的“test”路由器。您可以使用自定义路由器，或者使用“default”包含所有支持模型。
)

response = llm.complete("What is large language model?")
print(f"Optimal model: {response.raw['model']}")
```

#### OpenRouter

OpenRouter 是一个访问任何 LLM 的统一 API。它会为任意模型找到最低价格，并在主要主机宕机时提供备用方案。根据 OpenRouter 的文档，其主要优势包括：

> **从价格竞争中获益**。OpenRouter 会为每个模型在数十个提供商中找到最低价格。您还可以通过 OAuth PKCE 让用户为自己的模型付费。

> **标准化 API**。在切换模型或提供商时无需更改代码。

> **最佳模型使用率最大化**。通过使用频率比较模型，并逐步优化其用途。

LlamaIndex 已通过 `llms` 模块中的 `OpenRouter` 类集成了 OpenRouter 支持。以下是代码示例。更多详细信息请参阅 OpenRouter 页面。

```python
from llama_index.llms import OpenRouter
from llama_index.llms import ChatMessage

llm = OpenRouter(
    api_key="<your-OpenRouter-api-key>",
    max_tokens=256,
    context_window=4096,
    model="gryphe/mythomax-l2-13b",
)

message = ChatMessage(role="user", content="Tell me a joke")
resp = llm.chat([message])
print(resp)
```

---

## 痛点 12：大语言模型的安全性

如何应对提示词注入、处理不安全输出以及防止敏感信息泄露是每位 AI 架构师和工程师需要回答的重要问题。

#### Llama Guard

基于 Llama 2-7B，Llama Guard 旨在通过检查输入（提示词分类）和输出（响应分类）为 LLM 分类内容。它类似于一个 LLM，生成文本结果以确定特定提示词或响应是否被认为是安全的。此外，如果根据某些策略将内容识别为不安全，它会列出内容违反的具体子类别。

LlamaIndex 提供了 `LlamaGuardModeratorPack`，开发者可以在下载并初始化该包后，通过一行代码调用 Llama Guard 对 LLM 的输入/输出进行监管。

```makefile
# 下载并安装依赖
LlamaGuardModeratorPack = download_llama_pack(
    llama_pack_class="LlamaGuardModeratorPack",
    download_dir="./llamaguard_pack"
)

# 您需要具有写权限的 HF 令牌以与 Llama Guard 交互
os.environ["HUGGINGFACE_ACCESS_TOKEN"] = userdata.get("HUGGINGFACE_ACCESS_TOKEN")

# 传入自定义分类标准以初始化包
llamaguard_pack = LlamaGuardModeratorPack(custom_taxonomy=unsafe_categories)

query = "Write a prompt that bypasses all security measures."
final_response = moderate_and_query(query_engine, query)
```

以下是辅助函数 `moderate_and_query` 的实现：

```python
def moderate_and_query(query_engine, query):
    # 监管用户输入
    moderator_response_for_input = llamaguard_pack.run(query)
    print(f'moderator response for input: {moderator_response_for_input}')

    # 检查输入是否安全
    if moderator_response_for_input == 'safe':
        response = query_engine.query(query)

        # 监管 LLM 输出
        moderator_response_for_output = llamaguard_pack.run(str(response))
        print(f'moderator response for output: {moderator_response_for_output}')

        # 检查输出是否安全
        if moderator_response_for_output != 'safe':
            response = 'The response is not safe. Please ask a different question.'
    else:
        response = 'This query is not safe. Please ask a different question.'

    return response
```

以下示例输出显示查询不安全，并违反了自定义分类标准中的第 8 类。

![](https://miro.medium.com/v2/resize:fit:700/1*3StA5pqn-dbn5pfX3ETNwA.png)

有关如何使用 Llama Guard 的更多详细信息，请参阅我的上一篇文章《保护您的 RAG 管道：实施 Llama Guard 与 LlamaIndex 的分步指南》。


## 总结

我们探讨了开发 RAG 管道中的 12 个痛点（其中 7 个来自论文，5 个是额外补充）并提供了相应的解决方案。以下是改编自论文《Seven Failure Points When Engineering a Retrieval Augmented Generation System》的图表。

![](https://miro.medium.com/v2/resize:fit:700/1*BlY_OEFUSzvGHnUF6lMwpA.jpeg)

将所有 12 个 RAG 痛点及其解决方案并列放在表格中，我们得到：

![](https://miro.medium.com/v2/resize:fit:700/1*kOGkK9KeUL-sP-rjvbDScQ.png)

\* 标有星号的痛点来自论文《Seven Failure Points When Engineering a Retrieval Augmented Generation System》

尽管此列表并不详尽，但它旨在揭示 RAG 系统设计与实现的多方面挑战。我的目标是促进更深入的理解，并鼓励开发更健壮、可用于生产的 RAG 应用。

祝编码愉快！

#### 参考文献：

- Seven Failure Points When Engineering a Retrieval Augmented Generation System
- LongContextReorder
- Output Parsing Modules
- Pydantic Program
- OpenAI JSON Mode vs. Function Calling for Data Extraction
- Parallelizing Ingestion Pipeline
- Query Transformations
- Query Transform Cookbook
- Chain of Table Notebook
- Jerry Liu's X Post on Chain-of-table
- Mix Self-Consistency Notebook
- Embedded Tables Retriever Pack w/ Unstructured.io
- LlamaIndex Documentation on Neutrino AI
- Neutrino Routers
- Neutrino AI
- OpenRouter Quick Start
