---
categories: articles
date: 2024-04-27
layout: post
style: huoshui
tags:
- AI
title: FineWeb：HuggingFace开源的15T超大数据集
---

在人工智能时代，数据如同新石油，为语言模型这个强大引擎提供动能。Hugging Face 发布的FineWeb就是一个超大规模的英文网页数据集。

## 核心价值：规模和质量

FineWeb数据集拥有超过15万亿个英文标记，不仅覆盖从2013年夏季至2024年3月长达十年的时间跨度，而且经过了严格的清洗和去重处理。在实际应用中，能够显著提升文本生成模型性能，使得生成的文本更加流畅、准确和多样化。

FineWeb数据集中的文本均为英文，结构井然有序，数据实例包含文本内容、唯一标识符、转储信息、原始网页URL、抓取日期、文件路径、语言和语言分数、标记计数等字段，为研究者提供了丰富的上下文信息。

    
    
    {  
       "text": "This is basically a peanut flavoured cream thickened with egg yolks and then set into a ramekin on top of some jam. Tony, one of the Wedgwood chefs, suggested sprinkling on some toasted crushed peanuts at the end to create extra crunch, which I thought was a great idea. The result is excellent.",  
       "id": "<urn:uuid:e5a3e79a-13d4-4147-a26e-167536fcac5d>",  
       "dump": "CC-MAIN-2021-43",  
       "url": "<http://allrecipes.co.uk/recipe/24758/peanut-butter-and-jam-creme-brulee.aspx?o_is=SimilarRecipes&o_ln=SimRecipes_Photo_7>",  
       "date": "2021-10-15T21:20:12Z",  
       "file_path": "s3://commoncrawl/crawl-data/CC-MAIN-2021-43/segments/1634323583083.92/warc/CC-MAIN-20211015192439-20211015222439-00600.warc.gz",  
       "language": "en",  
       "language_score": 0.948729,  
       "token_count": 69  
    }

## 数据来源和性能评估

数据来源于CommonCrawl基金会在2013-2024年间抓取的网页数据，使用Hugging Face的datatrove
库进行清洗、过滤和去重，主要用于在大型语言模型的预训练数据集的背景下作为公共数据的研究工件。

FineWeb在27亿个标记上训练的1.8B参数模型展示了不错的效果，与RefinedWeb、C4、DolmaV1.6、The Pile 和
SlimPajama等数据集相比，在多个维度上都表现出不俗的竞争力。

## 如何使用数据集

FineWeb数据集的使用门槛低，感兴趣的研究者和开发者可以通过datatrove库、huggingface_hub或datasets库来加载和使用这个数据集。

### 使用datatrove

    
    
    from datatrove.pipeline.readers import ParquetReader  
      
    # limit determines how many documents will be streamed (remove for all)  
    # to fetch a specific dump: hf://datasets/HuggingFaceFW/fineweb/data/CC-MAIN-2024-10  
    data_reader = ParquetReader("hf://datasets/HuggingFaceFW/fineweb/data", limit=1000)   
    for document in data_reader():  
        # do something with document  
        print(document)  
      
    ###############################      
    # OR for a processing pipeline:  
    ###############################  
      
    from datatrove.executor import LocalPipelineExecutor  
    from datatrove.pipeline.readers import ParquetReader  
    from datatrove.pipeline.filters import LambdaFilter  
    from datatrove.pipeline.writers import JsonlWriter  
      
    pipeline_exec = LocalPipelineExecutor(  
        pipeline=[  
            ParquetReader("hf://datasets/HuggingFaceFW/fineweb/data/CC-MAIN-2024-10", limit=1000),  
            LambdaFilter(lambda doc: "hugging" in doc.text),  
            JsonlWriter("some-output-path")  
        ],  
        tasks=10  
    )  
    pipeline_exec.run()

### 使用huggingface_hub

    
    
    from huggingface_hub import snapshot_download  
    folder = snapshot_download(  
                    "HuggingFaceFW/fineweb",   
                    repo_type="dataset",  
                    local_dir="./fineweb/",  
                    allow_patterns="data/CC-MAIN-2023-50/*")

### 使用dataset

    
    
    from datasets import load_dataset  
    fw = load_dataset("HuggingFaceFW/fineweb", name="CC-MAIN-2024-10", split="train", streaming=True)

## 偏差与不足

Hugging Face在减少NSFW和有害内容方面做了大量工作，但无法完全避免这些内容。此外，为避免特定方言中内容被不成比例地删除，Hugging
Face刻意避免使用基于与“黄金”来源（例如维基百科或毒性分类器）的相似性来定义文本质量的机器学习过滤方法。

  

项目地址：https://huggingface.co/datasets/HuggingFaceFW/fineweb