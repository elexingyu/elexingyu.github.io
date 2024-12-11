---
categories: articles
date: 2024-12-10
layout: post
style: huoshui
tags:
- AI
- 教程
title: GraphMuse库解密：音乐符号处理的图神经网络技巧
---

![图片由 Dall-E 3 生成](https://miro.medium.com/v2/resize:fit:1400/1*AUunhJf4xjHvGXVncwiUzA.png)

在这篇文章中，我们将探讨我最近的一篇论文以及开源软件：GraphMuse Python 库。  
但在深入之前，让我先为大家介绍一下符号音乐处理的一些基础知识。

> 故事是这样开始的……

符号音乐处理主要是指从乐谱中提取信息。“符号”一词指的是任何形式的乐谱或音乐记谱中存在的符号。乐谱中除了音符之外，还可能包含多种元素，例如拍号、调号、表情记号、力度记号等。乐谱可以以多种格式存在，比如 MIDI、MusicXML、MEI、Kern、ABC 等。

近年来，图神经网络（Graph Neural Networks, GNNs）在从生物网络到推荐系统再到音乐分析的众多领域中变得越来越流行，并取得了一定的成功。在音乐分析领域，GNNs 被用于解决诸如和声分析、乐句分割以及声部分离等任务。

其核心思想很简单：乐谱中的每个音符是图中的一个顶点，而边则由音符之间的时间关系定义，如下图所示。

![](https://miro.medium.com/v2/resize:fit:1400/1*PvEckgEwXWbe4zrM8TgDtw.png)

这些边被分为四类：

- 同时开始的音符通过“起始”边（蓝色）相连；
- 在某个音符结束后紧接着开始的音符通过“连续”边（红色）相连；
- 在某个音符开始和结束之间开始的音符通过“期间”边（绿色）相连；
- 最后，当出现休止时，所有最后结束的音符与接下来第一个开始的音符通过“静止”边（黄色）相连。

这种对图的最小化建模保证了乐谱从头到尾是连续连接的，不会有任何不连通的子图。

## 什么是 GraphMuse

GraphMuse 是一个用于训练和应用深度图模型进行乐谱音乐分析的 Python 库。

GraphMuse 提供了加载器、模型和工具，用于结合 GNNs 进行符号音乐处理。它基于 _PyTorch_ 和 _PyTorch Geometric_ 构建，具有更高的灵活性和互操作性。

PyTorch 是一个开源的机器学习库，可以高效地构建深度学习模型并支持 GPU 加速。而 _PyTorch Geometric_ 是一个基于 PyTorch 的库，能够轻松编写和训练图神经网络（GNNs），适用于广泛的应用场景。

最后，GraphMuse 提供了将乐谱转换为图的功能。图的创建采用了 C 代码实现，并通过 Python 绑定来加速图的构建，比之前基于 numpy 的实现快了多达 300 倍。

## 科学基础

图在音乐分析和表示中经常被使用。例如，Tonnetz、申克分析（Schenkerian analysis）以及树形结构分析（treelike form analysis）都值得一提。图的优势在于它能够通过边的设计同时捕捉音乐的层次性和序列性。

基于图的符号音乐处理结合 GNNs 起源于 2021 年，当时使用了一种从乐谱生成表演的模型。从那时起，许多图模型被引入，其中一些在音乐分析任务中达到了当前的最先进水平。

既然我们已经讨论了图的必要性，那么让我们来面对设计和训练符号音乐图模型的复杂性。

图和音乐的主要复杂性在于：音乐作品的长度并不总是相同，而由它们生成的图的大小也各不相同。例如，一首巴赫的合唱可能只有 200 个音符，而一首贝多芬的奏鸣曲可能会超过 5000 个音符。在我们的图中，音符的数量直接对应于每个乐谱图中的顶点数量。

在乐谱图上高效快速地训练并非易事，需要一种采样方法，能够在不降低模型性能的前提下，最大化计算资源的利用率（包括内存和时间），甚至有时还能提升模型性能。

在训练过程中，采样涉及将不同乐谱的图组合起来创建一个新的图，通常在计算机科学中称为“批次”。每个批次会被输入到 GNN 模型中，计算损失值。这个损失值用于反向传播并更新模型参数。这个单次迭代称为一个训练步骤。为了优化模型，这个过程会重复多次，直到训练收敛，理想情况下模型表现最佳。

听起来很复杂，但别担心，因为 GraphMuse 可以帮你处理这些部分！

## GraphMuse 的内部工作原理

GraphMuse 中符号音乐乐谱的通用图处理/训练流程包括以下步骤：

1.  预处理乐谱数据库以生成输入图，GraphMuse 可以快速轻松地完成这一步；
2.  对输入图进行采样以创建内存高效的批次，GraphMuse 也能搞定；
3.  将多个采样的输入图组合成一个新图，包含来自各个采样输入图的节点和边；对于每个图，选定一组节点，我们称之为 _目标节点_。目标节点的邻居也可以按需获取，这一过程称为节点采样（node-wise sampling）。
4.  通过图卷积更新目标节点的表示以生成节点嵌入。GraphMuse 提供了一些可以使用的模型，当然你也可以选择 PyTorch Geometric；
5.  将这些嵌入应用于特定任务。这个部分由你来完成，我相信你一定能做到！

请注意，根据采样策略，目标节点可以包括批次节点的全部或部分。

现在流程已经图示化，让我们更详细地看看 GraphMuse 如何处理每个乐谱中的音符采样。

![顶部：采样的音符及其邻居；中间：乐谱图及采样过程；底部：节拍和小节的采样过程。](https://miro.medium.com/v2/resize:fit:1400/1*ZTyNDmYsnjSk_Pya47pHHA.png)

**每个乐谱的采样过程**

1.  首先随机选取一个音符（黄色）进行采样；
2.  然后计算目标音符的边界，这里示例中预算为 15 个音符（粉色和黄色音符）；
3.  接着获取目标音符的 k 跳邻居（浅蓝色表示 1 跳，深蓝色表示 2 跳）。k 跳邻居根据输入图计算（图中用连接音符的彩色边表示）；
4.  我们还可以扩展采样过程以包括节拍和小节元素。注意，k 跳邻居不一定严格与时间窗口相关。

为了最大化计算资源（如内存）的利用，上述过程会对多个乐谱同时重复，以创建一个批次。通过这一过程，GraphMuse 确保每个采样片段的目标音符数量相同。每个采样片段可以组合成一个新图，其大小至多为 **乐谱数量** x **目标音符数量**。这个新图构成当前训练步骤的批次。

## GraphMuse 实操

在实操部分，我们尝试使用 GraphMuse 和一个模型来处理音高拼写任务。音高拼写任务是指在乐谱中缺少音符名称和变音符号时推断这些信息。例如，当我们有一个量化后的 MIDI 文件时，希望生成如下图所示的乐谱：

![MIDI 文件为输入（顶部），乐谱为目标输出（底部）。](https://miro.medium.com/v2/resize:fit:1400/1*AtwRLqbO7g4OYP5hHFNhqA.png)

在安装 GraphMuse 之前，你需要先安装 PyTorch 和 PyTorch Geometric。请查看适合你系统的版本 **这里** （https://pytorch.org/get-started/locally/） 和 **这里**（https://pytorch-geometric.readthedocs.io/en/latest/install/installation.html）。

完成这一步后，在你的终端中输入以下命令来安装 GraphMuse：

```
pip install graphmuse
```

安装完成后，让我们从 URL 读取一个 MIDI 文件，并使用 GraphMuse 创建乐谱图。

```
import graphmuse as gm

midi_url_raw = "https://github.com/CPJKU/partitura/raw/refs/heads/main/tests/data/midi/bach_midi_score.mid"
graph = gm.load_midi_to_graph(midi_url_raw)

```

底层过程会使用 Partitura 读取文件，然后通过 GraphMuse 处理。

为了训练我们的模型以处理音高拼写，我们首先需要一个已经标注了音高拼写的乐谱数据集。为此，我们将使用 ASAP 数据集（根据 CC BY-NC-SA 4.0 许可），它将作为模型学习的基础。你可以通过 git 或直接从 GitHub 下载 ASAP 数据集（https://github.com/cpjku/asap-dataset）：

```
git clone https://github.com/cpjku/asap-dataset.git
```

ASAP 数据集包含了各种古典钢琴作品的乐谱和表演数据。对于我们的用例，我们只使用以 `.musicxml` 结尾的乐谱。

加载该数据集时，我们需要两个关键工具：一个用于编码音高拼写，另一个用于处理调号信息，它们都会被转换成数值标签。幸运的是，这些工具在 GraphMuse 的预构建音高拼写模型中已经提供。让我们开始导入所有必要的包并加载第一个乐谱来入门。

```
import graphmuse as gm
import partitura as pt
import os
import torch
import numpy as np

# Directory containing the dataset, change this to the location of your dataset
dataset_dir = "/your/path/to/the/asap-dataset"

# Find all the score files in the dataset (they are all named 'xml_score.musicxml')
score_files = [os.path.join(dp, f) for dp, dn, filenames in os.walk(dataset_dir) for f in filenames if f == 'xml_score.musicxml']

# Use the first 30 scores, change this number to use more or less scores
score_files = score_files[:30]

# probe the first score file
score = pt.load_score(score_files[0])
# Extract features and note array
features, f_names = gm.utils.get_score_features(score)
na = score.note_array(include_pitch_spelling=True, include_key_signature=True)
# Create a graph from the score features
graph = gm.create_score_graph(features, score.note_array())

# Get input feature size and metadata from the first graph
in_feats = graph["note"].x.shape[1]
metadata = graph.metadata()

# Create a model for pitch spelling prediction
model = gm.nn.models.PitchSpellingGNN(
    in_feats=in_feats, n_hidden=128, out_feats_enc=64, n_layers=2, metadata=metadata, add_seq=True
)

# Create encoders for pitch and key signature labels
pe = model.pitch_label_encoder
ke = model.key_label_encoder
```

接下来，我们将加载数据集中剩余的乐谱文件，继续为模型训练准备数据。

```
# Initialize lists to store graphs and encoders
graphs = []

# Process each score file
for score_file in score_files:
    # Load the score
    score = pt.load_score(score_file)

    # Extract features and note array
    features, f_names = gm.utils.get_score_features(score)
    na = score.note_array(include_pitch_spelling=True, include_key_signature=True)

    # Encode pitch and key signature labels
    labels_pitch = pe.encode(na)
    labels_key = ke.encode(na)

    # Create a graph from the score features
    graph = gm.create_score_graph(features, score.note_array())

    # Add encoded labels to the graph
    graph["note"].y_pitch = torch.from_numpy(labels_pitch).long()
    graph["note"].y_key = torch.from_numpy(labels_key).long()

    # Append the graph to the list
    graphs.append(graph)
```

一旦图结构准备好，我们可以继续创建数据加载器，这一过程由 GraphMuse 提供。在此阶段，我们还将定义标准训练组件，例如损失函数和优化器，以指导学习过程。

```
# Create a DataLoader to sample subgraphs from the graphs
loader = gm.loader.MuseNeighborLoader(graphs, subgraph_size=100, batch_size=16, num_neighbors=[3, 3])

# Define loss functions for pitch and key prediction
loss_pitch = torch.nn.CrossEntropyLoss()
loss_key = torch.nn.CrossEntropyLoss()

# Define the optimizer
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
```

让我稍微解释一下 _gm.loader.MuseNeighborLoader_。  
这是 GraphMuse 中的核心数据加载器，包含了之前部分中解释的采样过程。_subgraph_size_ 指每个输入图的目标节点数量，_batch_size_ 是每批次采样的图数量，最后 _num_neighbors_ 是指在每层中每个采样节点的邻居数量。

一切准备就绪后，我们终于可以开始训练模型了。让我们深入其中，开始训练过程吧！

```
# Train the model for 5 epochs
for epoch in range(5):
    loss = 0
    i = 0
    for batch in loader:
        # Zero the gradients
        optimizer.zero_grad()

        # Get neighbor masks for nodes and edges for more efficient training
        neighbor_mask_node = {k: batch[k].neighbor_mask for k in batch.node_types}
        neighbor_mask_edge = {k: batch[k].neighbor_mask for k in batch.edge_types}

        # Forward pass through the model
        pred_pitch, pred_key = model(
            batch.x_dict, batch.edge_index_dict, neighbor_mask_node, neighbor_mask_edge,
            batch["note"].batch[batch["note"].neighbor_mask == 0]
        )

        # Compute loss for pitch and key prediction
        loss_pitch_val = loss_pitch(pred_pitch, batch["note"].y_pitch[batch["note"].neighbor_mask == 0])
        loss_key_val = loss_key(pred_key, batch["note"].y_key[batch["note"].neighbor_mask == 0])

        # Total loss
        loss_val = loss_pitch_val + loss_key_val

        # Backward pass and optimization
        loss_val.backward()
        optimizer.step()

        # Accumulate loss
        loss += loss_val.item()
        i += 1

    # Print average loss for the epoch
    print(f"Epoch {epoch} Loss {loss / i}")
```

希望很快我们就能看到损失函数下降，这表明我们的模型正在有效学习如何执行音高拼写。祝一切顺利！

![](https://miro.medium.com/v2/resize:fit:1024/1*-7vH_uBVk1jWhvhrIx3-5w.png)

## 为什么选择 GraphMuse？

GraphMuse 是一个框架，旨在让基于图的符号音乐处理模型的训练和部署变得更简单。

对于那些希望重新训练、部署或微调之前最先进的符号音乐分析模型的人，GraphMuse 包含了一些必要的组件，可以更快、更高效地重建和重新训练你的模型。

对于那些希望原型设计、创新和设计新模型的人，GraphMuse 通过其简单性保留了灵活性。它旨在提供一组简单的工具，而不是包含复杂的链式管道，这些管道可能会阻碍创新过程。

对于那些希望学习、可视化并亲身体验的人，GraphMuse 是一个很好的起点。它通过几行代码就能轻松引入基本功能和流程。GraphMuse 还与 MusGViz 相关联，可以轻松地将图和乐谱一起可视化。

## 局限性与未来计划

我们在谈论任何项目的积极方面时，也不能忽略其消极方面。

GraphMuse 是一个新生项目，目前的状态还相当简单。它专注于涵盖图学习的基本部分，而不是成为一个涵盖所有可能性的全面框架。因此，它在上述流程的许多部分仍然高度依赖用户的实现。

和每个正在开发的开源项目一样，GraphMuse 需要帮助才能成长。因此，如果你发现了 bug 或希望添加更多功能，请不要犹豫，在 GraphMuse 的 GitHub 项目中报告、请求或贡献。

最后但同样重要的是，GraphMuse 使用了如 torch-sparse 和 torch-scatter 等 C 库，并有其自己的 C 绑定来加速图创建，因此安装并不总是那么简单。根据我们的用户测试和用户交互报告，Windows 的安装更具挑战性，尽管并非不可能（我自己就在 Windows 上运行它）。

未来计划包括：

- 使安装更简单；
- 增加对精确任务的模型和数据加载器的支持；
- 发展围绕 GraphMuse 的开源社区，以继续推动音乐的图形编码发展。

## 结论

GraphMuse 是一个使音乐图处理更简单的 Python 库。它专注于基于图的音乐模型的训练，但在研究型项目需要时保留了灵活性。

如果你想支持 GraphMuse 的开发和未来成长，请在此处为仓库加星（https://github.com/manoskary/graphmuse）。

祝你图形编码愉快！！！