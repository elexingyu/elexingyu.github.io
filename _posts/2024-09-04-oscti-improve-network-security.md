---
categories: articles
date: '2024-09-04'
layout: post
style: huoshui
tags:
- AI
- 知识图谱
- 教程
title: 开源情报大揭秘：如何用OSCTI提升网络安全
---

为什么选择开源网络威胁情报？
-----------------------------------

开源网络威胁情报（OSCTI）因其可访问性、成本效益、灵活性、质量、透明性和创新性，已在安全专业人士和组织中广受欢迎。

OSCTI 旨在通过使组织更容易访问和使用威胁情报数据和工具，从而提升其整体安全态势。通过公开和协作方式分享数据和工具，各组织可以共同努力，更好地理解和应对不断演变的威胁形势。

开源情报（OSINT）随时可用，且能够被广大专家社区轻松获取，使信息共享和威胁情报协作变得更加容易。已有几个 OSINT 平台，如 AlienVault 的开源威胁交换(https://cybersecurity.att.com/open-threat-exchange) (OTX) 和 网络威胁联盟(https://www.cyberthreatalliance.org/) (CTA)，提供对 OSCTI 报告和威胁情报数据的访问。

OTX 向全球威胁研究人员和安全专业人员开放访问权限。目前已有超过 140 个国家的 100,000 多名参与者，每天贡献超过 1900 万个威胁指标。

是的——每天有 1900 万个威胁指标。没有任何人类能够每天追踪或调查其中的 1% 以上。安全专家通常需要从特定攻击或漏洞开始，通过各种深层关系导航相关的情报，以便全面了解网络威胁的全貌。

目前已有一些平台能够将数据整合到单一存储库中，提供搜索 UI 和类似仪表盘的视图，并允许用户通过页面链接浏览详细信息。

![AlienVault OTX 门户 的截图](https://cdn-images-1.medium.com/max/1024/1*Pu1EvOcOA57hfhM-pNv2nQ.png)


我将演示一种低代码的方法，结合使用 Neo4j AuraDB(https://neo4j.com/cloud/platform/aura-graph-database/) 的图形可视化工具 Bloom 与 OTX，以实现更强大的可视化威胁调查——无需数据集成/导入管道即可开始。

所需工具
--------

### 1. AlienVault OTX API

AlienVault OTX 已经为外部应用程序提供了 RESTful API 来查询其数据库。以下示例为按其 ID 搜索 CVE-2017–0144：

https://otx.alienvault.com/api/v1/indicator/cve/CVE-2017-0144

### 2. Neo4j AuraDB 和 Bloom

Neo4j AuraDB 是一种完全托管的云图数据库服务。AuraDB 利用数据中的关系，支持实时分析和洞察的高速查询。AuraDB 可靠、安全且全自动化，使您可以专注于构建图形应用程序，而无需担心数据库管理。

出于实验目的，我将使用 AuraDB 免费实例。它可以在 90 天内保留创建的数据库并存储一些数据。

Aura Free(https://neo4j.com/cloud/aura-free/)

一旦图数据库管理系统实例启动，我将访问 Bloom 可视化 UI 进行实际调查。Bloom 具有直观、无代码的搜索到可视化设计，是促进同行、管理者和高管之间沟通的理想界面，也适用于分享图形开发和分析团队的创新工作。

熟悉新可视化工具的 UI 和操作可能会有所帮助，以下是一个很好的参考来源：

Bloom 快速入门 – Neo4j Bloom(https://neo4j.com/docs/bloom-user-guide/current/bloom-quick-start/)



分步指南
--------

### 1. 创建数据库模式

一旦 AuraDB 实例启动，进入控制台页面，点击 **Query** 按钮启动 Neo4j 浏览器。

![Neo4j Aura 控制面板](https://cdn-images-1.medium.com/max/1024/1*HMpd3Igh0ZCaTHQaTKKKYA.png)


使用 “neo4j” 作为用户名和生成的密码登录数据库。将以下内容复制并粘贴到文本框中执行：

```
CREATE CONSTRAINT FOR (n:pulse) REQUIRE n.id IS UNIQUE;  
CREATE CONSTRAINT FOR (n:malware\\_family) REQUIRE n.id IS UNIQUE;  
CREATE CONSTRAINT FOR (n:reference) REQUIRE n.url IS UNIQUE;  
CREATE CONSTRAINT FOR (n:country) REQUIRE n.name IS UNIQUE;  
CREATE CONSTRAINT FOR (n:attack) REQUIRE n.id IS UNIQUE;  
CREATE CONSTRAINT FOR (n:tag) REQUIRE n.name IS UNIQUE;  
CREATE CONSTRAINT FOR (n:indicator) REQUIRE n.indicator IS UNIQUE;  
CREATE CONSTRAINT FOR (n:indicator) REQUIRE n.id IS UNIQUE;  
CREATE CONSTRAINT FOR (n:pulse\\_collection) REQUIRE n.indicator IS UNIQUE;  
CREATE CONSTRAINT FOR (n:type) REQUIRE n.name IS UNIQUE;  
CREATE CONSTRAINT FOR (n:indicator\\_collection) REQUIRE (n.pulse\\_id, n.type) IS UNIQUE;
```

![](https://cdn-images-1.medium.com/max/1024/1*wX3813Dd6rASE4X0oZgrJw.jpeg)

很容易看出，上述语句为数据库中某些标签的节点创建了多个唯一性约束。例如：

```
CREATE CONSTRAINT FOR (n:indicator) REQUIRE n.id IS UNIQUE;
```
这是创建一个约束，以确保每个威胁指标节点的 ID 属性始终唯一。_威胁指标_ 指的是威胁指标（IOC）。

作为一种轻模式的原生图数据库，实施了标签属性图（LPG），威胁指标是一个节点组的标签。有关 LPG 和图形建模的更多信息，请查看：

图数据库概念 – 入门指南(https://neo4j.com/docs/getting-started/current/appendix/graphdb-concepts/)

### 2. 启动 Bloom 并导入透视图

返回 Neo4j Aura 控制台并点击 **Explore** 按钮启动 Bloom。

![Neo4j Aura 控制面板](https://cdn-images-1.medium.com/max/1024/1*HMpd3Igh0ZCaTHQaTKKKYA.png)



完成后，前往我的 GitHub 仓库(https://github.com/Joshua-Yu/cyber/blob/main/Threat%20Intelligence%20Analysis.json) 下载用于网络情报调查的透视图。

在 Neo4j Bloom 中，_透视图_ 定义了目标 Neo4j 图中某个业务视图或领域。单个 Neo4j 图可以通过不同的透视图来查看，每个透视图都为不同的业务目标量身定制。透视图定义了：

*   业务实体的分类
*   属性可见性和值类型
*   关系可见性
*   样式（颜色、图标、标题）
*   自定义搜索短语和场景操作

按照以下步骤导入透视图：

检查默认透视图。

![](https://cdn-images-1.medium.com/max/1024/1*kO9zKSjYRRSNU7bu9OXEjA.jpeg)

导入新下载的透视图并选择使用。

![](https://cdn-images-1.medium.com/max/1024/1*dqjDOf2RiU6S4GHt7p4U3Q.jpeg)

### 3. 探索 WannaCry 勒索软件情报

现在我们准备开始！

WannaCry 是最著名、影响最深远的勒索软件攻击之一。WannaCry 首次发现于 2017 年 5 月，是一种勒索软件蠕虫，迅速传播到世界各地，感染了 150 多个国家的数十万台计算机。

WannaCry 攻击对企业、医疗机构和政府机构造成了重大影响，导致了广泛的破坏和巨大的经济损失。该攻击成为了组织优先考虑其网络安全措施的警钟，并强调了定期应用软件更新和补丁以解决已知漏洞的重要性。

WannaCry 利用 Microsoft Windows 操作系统中的一个漏洞（即 CVE-2017–0144）在同一网络的受感染计算机之间传播。安装后，恶意软件会加密受感染计算机上的文件，并要求支付赎金以换取解密密钥。所以我们从这个 CVE 开始。

在 Bloom 左上角的文本框中输入“Search”。下拉列表中会出现建议的搜索短语“Search for CVE-”。选择它并完成输入“Search for CVE-2017–0144”，然后按下 **Enter** 执行搜索。

![](https://cdn-images-1.medium.com/max/824/1*OJaDZvMP8-kK0T60cpIAGg.png)

这将触发后台 Cypher 查询以调用 OTX API。结果如下所示。

![](https://cdn-images-1.medium.com/max/1024/1*fS45pxr5Tn6zCmjF41ExjQ.png)

此 CVE 在 OTX 存储库中有 50 个脉冲。默认情况下，Bloom 应用基于力的样式规则来安排图形布局。它还支持分层布局，这对于更清楚地查看分层结构可能很有用。

![更改图形布局](https://cdn-images-1.medium.com/max/1024/1*tMbzNf3ZyGsxlBYXrSkcDw.png)


下面是切换到分层布局后的结果。

![](https://cdn-images-1.medium.com/max/1024/1*xMi75EV1VIN6pji9InWTZQ.png)

让我选择一个脉冲——LemonDuck 木马——进行深入挖掘。以下是步骤：

1. 在文本框中输入“LemonDuck Trojan”并按 **Enter**。这将搜索该文本并将匹配的节点/圆圈带到屏幕中央。

2. 双击代表 LemonDuck 木马的节点，以查看其属性显示在左侧的弹出面板中。

3. 左键单击节点，然后右键单击它以查看快捷菜单。由于数据库中还没有关于此脉冲的相关数据，我们看到菜单项“Expand”被禁用。

![](https://cdn-images-1.medium.com/max/1024/1*TLSul2bzD1m_HvR1TH_GKQ.png)

在这种情况下，我们选择菜单项 **Scene Action** > **Get pulse info**。这将触发另一个保存的 Cypher 查询，以调用 OTX API 以获取相关脉冲。

![](https://cdn-images-1.medium.com/max/1024/1*Rnv93CVkk1bQQfElsJGC0g.png)

4. 还有数百个其他相关威胁指标。让我们找到域名（共 12 个），并定位代表 ackng.com 的节点。从那里我们将选择场景操作以获取该域名的相关 IP。

![图片14](https://cdn-images-1.medium.com/max/1024/1*bDwjIdlSuwI9QUJKmMr4Bg.png)

这一发现过程可以一直继续下去，直到我们对威胁有了全面的了解。Bloom 透视图包含了针对威胁指标的条件样式，其中为每种威胁指标类型（如 FileHash-MD5、主机名、域名等）分配了唯一的颜色。

![彩色威胁指标节点表示不同类型](https://cdn-images-1.medium.com/max/1024/1*3eLoVkixCTmt_IzFfJOOBQ.png)


进一步讨论
------------------

在这个简短的教程中，我介绍了如何使用图形可视化工具进行网络威胁调查，使用空的（且免费的）Neo4j AuraDB、Bloom 几乎无需代码。

虽然开源网络威胁情报使安全专家能够更容易地访问许多有价值的信息，但它也很容易让用户感到不知所措。通过页面链接导航相关信息对高效和富有成效的调查帮助不大。通过图形可视化和按需情报检索，此方法提供了一种创新的方式，使安全专家能够选择需要深入研究的威胁情报，并帮助他们更轻松地了解网络威胁的范围、影响和关联性。

通过 Save Cypher 和 Scene Actions 等功能，使用 Cypher（一种 Neo4j 的图形查询语言）进行场景特定分析变得容易实现。此外，还可以很容易地提供一种全面而无缝的方式来访问来自不同网络威胁来源的信息，而无需手动切换它们。