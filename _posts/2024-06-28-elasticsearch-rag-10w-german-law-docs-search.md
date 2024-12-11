---
categories: articles
date: 2024-06-28
layout: post
style: huoshui
tags:
- AI
title: 从10万份文档中更快、更准确地找到信息，还能理解语义！试试ElasticSear
---

![](/assets/images/ed56fb68d66c43f0b09662c70462f0e5.png)

作者：Diptanshu Gautam

编译：活水智能

目前，高效搜索和分析大量文档仍然是一项非常耗时的任务。

法律文件更是如此，因为精确性和全面性至关重要。

本文将探讨如何使用 ElasticSearch 和大模型相关技术检索增强生成（RAG）处理和检索超过10万份德语法律文档的信息。

（编者注：Elasticsearch 是一个开源的全文搜索引擎，其每个字段均可被索引，可以在极短的时间内存储、搜索和分析TB级数据）

## 处理海量文本的挑战

法律文件非常复杂，包含复杂的细节和特定术语。主要难点在于创建一个高效的系统，能够处理庞大的法律文档库，并快速提供准确、相关的结果。

这个问题以前也有解决方法。然而问题主要出在分块策略上。

之前使用的是langchain的递归分块策略。这是一种不错的策略，但在巨量文档面前，它无法保持语义完整性。

让我们来看一个使用句子转换器进行文本分割的示例代码。

from langchain.text_splitter import SentenceTransformersTokenTextSplitter  
text_splitter = SentenceTransformersTokenTextSplitter(  
tokens_per_chunk = 480,  
chunk_overlap = 50,  
model_name = "intfloat/multilingual-e5-large-instruct"  
)  
texts = text_splitter.split_documents(data)  

虽然分块重叠是一种有效的保持上下文的方法，但它也存在一些缺点和潜在的问题需要考虑：

需要更多储存空间。重叠的分块意味着某些文本部分会在多个分块中重复。这种冗余增加了对储存空间的需求，特别是在处理非常大的文档库时。

增加处理时间。更多的数据需要处理会导致计算开销增加。每个分块都需要处理和索引，这可能会减慢整个系统的速度。

上下文碎片化。虽然重叠有助于保持上下文，但对于上下文逻辑严密或复杂的文本来说，这可能还不够。重要信息可能仍然会在分块之间碎片化，导致理解或检索不完整。

由于我们有超过10万份文档，每份文档多达1000多页，这种策略并不适用。

## 解决方案

由于数据存储在云端的不同文件夹中，每个文件夹中有大量文件。

一个一个下载将耗费大量时间。因此，我选择了并发下载（concurrent futures），可以同时下载多个文件。

from concurrent import futures  
from concurrent.futures import ProcessPoolExecutor  
  
def download_parallel_multiprocessing():  
with ProcessPoolExecutor() as executor:  
future_to_key = {executor.submit(download_one_file, key): key for key in
list_key_to_download}  
  
for future in futures.as_completed(future_to_key):  
key = future_to_key[future]  
exception = future.exception()  
  
if not exception:  
yield key, future.result()  
else:  
yield key, exception  
  
for key, result in download_parallel_multiprocessing():  
# print(f"{key}: {result}")  
pass

这些文件下载后存储在临时文件夹中以供使用。接下来，我们定义了用于嵌入的模型。

由于这里使用的是德语，需要选择一个多语言编码器模型。因此，我们选择了intfloat/multilingual-e5-large。

from langchain_community.llms import WatsonxLLM  
# from dotenv import load_dotenv  
import os  
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as
GenParams  
  
# Model Declaration  
  
api_key = "Your Key Here"  
ibm_cloud_url = "Write your URL"  
project_id = "The project id"  
  
# Params Declaration  
params = {  
GenParams.DECODING_METHOD: "sample",  
GenParams.MIN_NEW_TOKENS: 50,  
GenParams.MAX_NEW_TOKENS: 430,  
GenParams.RANDOM_SEED: 42,  
GenParams.TEMPERATURE: 0,  
GenParams.TOP_K: 20,  
GenParams.TOP_P:1  
}  
# Model Configuration  
llm = WatsonxLLM(  
model_id='intfloat/multilingual-e5-large',  
url=ibm_cloud_url,  
apikey=api_key,  
project_id=project_id,  
params=params,  
)

### 过滤异常文件和去重

以下代码过滤了用户不需要的异常文件。它会在文件名中查找特定模式，然后在移除该模式后存储调整后的文件名。如果文件存在，则放入，表明存在重复文件。

import re  
  
def matching_files_with_names(file_names):  
matching_files = []  
for file_name in file_names:  
# Check if the file name contains a pattern  
pattern_match = re.search(r'\\[\d+\\]', file_name)  
if pattern_match:  
# Remove the pattern and check if the resulting name exists in the list  
pattern_removed_name = re.sub(r'\\[\d+\\].', '', file_name)  
if pattern_removed_name in file_names and pattern_removed_name != file_name:  
matching_files.append([file_name, pattern_removed_name])  
return matching_files  
  
matching_files = matching_files_with_names(matching_pairs)

在此之后，剩下超过102,000个文件需要处理。

提取元数据

下一步是预处理文件并将其分解成较小的块，以便后续处理。

由于文件内容是xml格式，实际的文本内容是html格式。

我们可以根据标题将文档分块。这样每个标题和文本都保持完整，从而保持块的语义含义。

第一步是加载和读取xml文件，并提取所有元数据。我们使用for循环遍历所有文件。

import lxml  
import pickle  
from lxml import etree  
from langchain.docstore.document import Document  
  
dir_list_pre = os.listdir("temp_pre/")  
# destination_path = "temp_post/"  
full_doc = []  
  
for file in tqdm(list(matching_pairs_og.keys())):  
file_path = "temp_pre/" \+ file  
with open(file_path, "r") as f:  
xml_content = f.read()  
  
# Parse the XML  
try:  
with open(file_path, "rb") as f:  
xml_content_tag_reader = f.read()  
parser = etree.XMLParser(recover=True)  
root = etree.fromstring(xml_content_tag_reader, parser)  
# Get the ElementTree object  
tree = root.getroottree()  
#Extracting metadata except that of text  
meta_tags = {tree.getpath(d): d.text for d in root.iterdescendants() if '/txt'
not in tree.getpath(d)}  
  
soup = BeautifulSoup(xml_content, "xml")  
  
text_tags = soup.find_all('txt')  
html_content = ''.join([' ' \+ tag.get_text() for tag in text_tags])  
  
if len(html_content)>0:  
  
html_soup = BeautifulSoup(html_content, "html.parser")  
  
# Find all <p> tags containing <strong> tags  
paragraphs_with_strong = html_soup.find_all(lambda tag: tag.name == 'p' and
tag.strong)  
  
# Iterate through each <p> tag containing <strong> tags  
for p_tag in paragraphs_with_strong:  
strong_tag = p_tag.strong  
if strong_tag:  
strong_text = strong_tag.text.strip()  
# Check if the text starts with a digit followed by a period and a space  
if re.match(r'^\d+\\. ', strong_text):  
# Find the previous sibling header tag  
previous_header = p_tag.find_previous_sibling(lambda tag:
tag.name.startswith('h') and len(tag.name) == 2)  
if previous_header:  
# Determine the level of the next header  
next_header_level = 'h6'  
# Replace the <p> tag with the next level header  
new_header_tag = html_soup.new_tag(next_header_level)  
new_header_tag.string = strong_text # Retain the text content within <strong>  
p_tag.replace_with(new_header_tag)  
  
# Get the modified HTML  
modified_html = str(html_soup)  
  
headers_to_split_on = [  
("h1", "Header 1"),  
("h2", "Header 2"),  
("h3", "Header 3"),  
("h4", "Header 4"),  
("h5", "Header 5"),  
("h6", "Header 6")  
]  
  
html_splitter =
HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)  
html_header_splits = html_splitter.split_text(modified_html)  
for i, split in enumerate(html_header_splits):  
tokens = llm.get_num_tokens(split.page_content)  
# html_header_splits[i].metadata.update(meta_tags)  
html_header_splits[i].metadata["token_count"] = tokens  
html_header_splits[i].metadata["source"] = file  
html_header_splits[i].metadata["index"] = i  
  
full_doc.append(html_header_splits)  
  
else:  
  
# Getting text from the file  
soup = BeautifulSoup(xml_content, "xml")  
text_tags = soup.find_all('txtascii')  
html_content = ''.join([' ' \+ tag.get_text() for tag in text_tags])  
  
lc_doc = Document(page_content=html_content)  
tokens = llm.get_num_tokens(html_content)  
# lc_doc.metadata["tags"] = meta_tags  
lc_doc.metadata["token_count"] = tokens  
lc_doc.metadata["source"] = file  
lc_doc.metadata["index"] = 1  
full_doc.append(lc_doc)  
  
except lxml.etree.XSLTApplyError as e:  
continue  
  
# Save the list to a file  
with open('full_xml.pkl', 'wb') as file:  
pickle.dump(full_doc, file)  
  
#Upload the file to COS  
cos_client.upload_file('./full_xml.pkl', bucket_name, 'full_xml.pkl')  
# cos_client.Object(bucket_name, item_name).put(Body=filelike_object)

一旦完成第一步后，使用lxml中的etree调用解析器函数，提取所有元数据。

with open(file_path, "rb") as f:  
xml_content_tag_reader = f.read()  
parser = etree.XMLParser(recover=True)  
root = etree.fromstring(xml_content_tag_reader, parser)  
# Get the ElementTree object  
tree = root.getroottree()  
#Extracting metadata except that of text  
meta_tags = {tree.getpath(d): d.text for d in root.iterdescendants() if '/txt'
not in tree.getpath(d)}

提取txt标签

下一步是读取内容并从xml内容中提取所有txt标签。对于每一页，有两个xml文件，一个包含html标签，一个包含高级元数据。

因此，检查是否有html_content可用，在这种情况下，使用Langchain的HTMLHeaderTextSplitter。

该模块根据提供的分块定义（在本例中为header_to_split_on），将文档分成较小的块。

from langchain_text_splitters import HTMLHeaderTextSplitter  
headers_to_split_on = [  
("h1", "Header 1"),  
("h2", "Header 2"),  
("h3", "Header 3"),  
("h4", "Header 4"),  
("h5", "Header 5"),  
("h6", "Header 6")  
]  
  
html_splitter =
HTMLHeaderTextSplitter(headers_to_split_on=headers_to_split_on)  
html_header_splits = html_splitter.split_text(modified_html)

然而，我注意到即使分块后，块的大小仍然太大。深入研究后，我发现<p>下的子标题标记在下，但可以用作子标题。

因此，下一步的自适应策略是进入数据中查找这种模式，并将标签更改为标题，从而定义新的标题，并将块分成更小的部分，同时保持语义。

# Find all <p> tags containing <strong> tags  
paragraphs_with_strong = html_soup.find_all(lambda tag: tag.name == 'p' and
tag.strong)  
  
# Iterate through each <p> tag containing <strong> tags  
for p_tag in paragraphs_with_strong:  
strong_tag = p_tag.strong  
if strong_tag:  
strong_text = strong_tag.text.strip()  
# Check if the text starts with a digit followed by a period and a space  
if re.match(r'^\d+\\. ', strong_text):  
# Find the previous sibling header tag  
previous_header = p_tag.find_previous_sibling(lambda tag:
tag.name.startswith('h') and len(tag.name) == 2)  
if previous_header:  
# Determine the level of the next header  
next_header_level = 'h6'  
# Replace the <p> tag with the next level header  
new_header_tag = html_soup.new_tag(next_header_level)  
new_header_tag.string = strong_text # Retain the text content within <strong>  
p_tag.replace_with(new_header_tag)

一旦完成（由于文件数量庞大，这花费了一个多小时），我添加了几个属性，如文件名、令牌大小和指示文件第n个块的索引。

我的目标是追溯到文件，以便我可以提取RAG模型选择的块的文件名和其他元数据。

一旦这些处理完成，就将其存储为pickle文件，因为这些文件存储在临时文件夹中，一旦内核关闭，这些文件将被删除。

将文本分成块

预处理完成后，我注意到有些文件没有分割成标签，因为langchain工具无法识别它们为标题。

因此，下一步是通过编写代码将页面分成不同的块。

def extract_headers_and_content(html):  
html_soup = BeautifulSoup(html, 'html.parser')  
headers = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']  
result = []  
current_metadata = {}  
  
for tag in html_soup.find_all(headers):  
# Update the current metadata hierarchy based on the current tag  
level = headers.index(tag.name)  
current_metadata = {h: current_metadata[h] for h in headers[:level] if h in
current_metadata}  
current_metadata[tag.name] = tag.get_text(strip=True)  
  
# Collect the content under the current header  
content = tag.find_next_sibling()  
content_text = ""  
while content and content.name not in headers:  
content_text += content.get_text(strip=True) + " "  
content = content.find_next_sibling()  
  
if content_text.strip():  
result.append({'page_content': content_text.strip(), 'metadata':
current_metadata.copy()})  
  
return result  
  
exception_file_chunking = []  
for key, value in tqdm(full_doc_v2.items()):  
extracted_data = extract_headers_and_content(value)  
extracted_data_v2 = [i for i in extracted_data if i['page_content'] != '']  
for idx, i in enumerate(extracted_data_v2):  
i['metadata']['source'] = key  
tokens = llm.get_num_tokens(i['page_content'])  
i['metadata']['token_count'] = tokens  
i['metadata']['index'] = idx  
exception_file_chunking.append(extracted_data_v2)

上述代码手动提取元数据，查找标题，并根据下一个兄弟节点（相同的下一个标题），仅提取该特定标签的信息。

这样，总块数超过了200万个。****

将标签命名为字符串

下一步是将标签重命名为字符串。

#Renaming the keys in the dictionary  
  
for k, v in tqdm(tags.items()):  
new_dict = {}  
for key, value in v.items():  
if key == '/Segmente/Segment':  
continue  
parts = key.rsplit('/', 2)  
text = '_'.join([part.lower() for part in parts[-2:]])  
new_dict[text] = value  
tags[k] = new_dict

文本向量化  

最后一步调用Hugging Face的嵌入模型进行向量化。具体操作如下：

from langchain.embeddings import HuggingFaceEmbeddings  
  
model_name = "intfloat/multilingual-e5-large"  
model_kwargs = {'device': 'cuda'}  
encode_kwargs = {'normalize_embeddings': False}  
hf = HuggingFaceEmbeddings(  
model_name=model_name,  
model_kwargs=model_kwargs,  
encode_kwargs=encode_kwargs  
)

创建客户端

接下来是创建一个Elastic Search客户端，用于与 Elastic Search 服务进行交互。

from elasticsearch import Elasticsearch  
from langchain_elasticsearch import ElasticsearchStore  
  
# Create a custom Elasticsearch client  
es_client = Elasticsearch(  
es_url,  
basic_auth=(es_user, es_password),  
verify_certs=False,  
request_timeout = 1200  
)  
  
elastic_vector_search = ElasticsearchStore(  
index_name="index_e5_multiprocessing_htmlsplitter_gpu_test_v2",  
es_connection=es_client,  
embedding=hf,  
)  
  
db = ElasticsearchStore.from_documents(  
documents=texts,  
embedding=hf,  
index_name="index_e5_multiprocessing-v6",  
strategy=ElasticsearchStore.ApproxRetrievalStrategy(  
hybrid = True  
),  
es_connection=es_client,  
)

至此，最终处理和分块完成。

我们使用BERT Score和余弦相似度来获取评估指标。

结果显示，平均BERT F1得分接近0.75，而余弦相似度接近0.9。表明语义准确性和相关性都很高。

## 结 论

为超过10万份文件构建RAG模型是一项具有挑战性但回报丰厚的工作。

在整个项目中，我们发现单一的分块方法并不适用。这促使我们开发了定制的分块策略，以高效处理文件。

通过提取元数据、自动删除重复文件以及从各种标签中细致地提取文本，我们确保了处理数据的质量。

结果令人鼓舞，BERT得分为0.75，余弦相似度为0.9。语义准确性和相关性都很高。

这些文件通过弹性混合搜索，从而有效地检索并提升了RAG模型的性能。

  

整个过程表明处理大规模数据时适应性和创新的重要性。

类似项目可以参考，释放庞大且多样的数据集的潜力，从而获得有意义的洞察。

  

参考资料：https://github.com/elastic/elasticsearch

  

推荐阅读

[Graph RAG：从大规模文档中发现规律，找到相互关系，速度更快，信息更全面！](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247486198&idx=1&sn=fe870f73635f7e97d576fb81c20befe2&chksm=c3546865f423e173293ec3697258a848a7dff22690a4b9cad0a91abdce7745760d98c5b16281&scene=21#wechat_redirect)

[最具代表性的文本数据集：覆盖32个领域，444个数据集，774.5TB数据量](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247486148&idx=1&sn=6cf9d475da4efa7521cb08f2835b8ad8&chksm=c3546857f423e141806236ba0a96fdc5e5bd16c5ca735361a9f50dbffec57fbdc4a521f7c1b4&scene=21#wechat_redirect)  

[心理学正在探究 AI 的心智理论](http://mp.weixin.qq.com/s?__biz=Mzk0OTY0NzM1Ng==&mid=2247486205&idx=1&sn=5aab2ad89e7657952688ac76ae6ef255&chksm=c354686ef423e178cd54716335e2d0e8d0cf1628561b3d46e497ac9b2ad6f576a4ca489029bc&scene=21#wechat_redirect)