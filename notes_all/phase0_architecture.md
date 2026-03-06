# Phase 0: Architecture Design

**Goal**: 理解RAG系统全貌，设计架构  
**Duration**: 1 hour  
**Status**: 🟡 In Progress

---

## Task 0.1 - System Architecture Diagram (30min)

### Instructions
用纸笔画出数据流：
```
offline pipeline
raw docs
-chunk(assign chunk_id)
-embedding(API call)
-vector store(chunk_id-vector)
同时chunk_id-chunk_text 存入docstore

online pipeline
query
-embedding(API call, cahche)
-Vector Search(retrive Top-K chunk_ids, cache)
-rerank (cross encoder, cache)
-fetch (chunk text from Doc Store)
-crate promot (question +context)
-llm (API call)
-Final answer
```

### Questions to Answer While Drawing
- [x] 需要几个主要组件？raw docs,chunks,embedding,vectorstore. query,retrieve,rerank,fetch,llm. promot
- [x] 数据在哪里存储？ vector store, doc store
- [x] 哪些步骤需要调用外部API？ embedding,llm
- [x] 哪些步骤可以cache？ embedding(query部分的),retrieve,rerank

### Resources
- Google: "RAG architecture diagram" (看图片找灵感)
- Pinecone blog: RAG system design

### My Diagram Description
```
Component 1: For the part of offline, it firstly chunk raw documents to some chunks,and then embedding them and upsert them to vectore store, so that docstore is build up successfully specificialy during chunk_id to chunk_text. 

Component 2: Then is the part of online query which happens many times. After users query, their query would be retrieved with pinecone and store in cache for 30 mins after being embedding in cache for 1 hour, and the be reranked and store in cache for 30 mins ,too. We would fetch these rerank results in doc store

Data Flow: 
offline:
Raw Docs → Chunking → Embedding → Vector Index
             ↓
         Doc Store

online:
Query → Embedding → Retrieve → Rerank → Fetch → Create Prompt → LLM

```

### Completion Criteria
- [x] 至少5个主要组件
- [x] 清晰的数据流向
- [x] 标注关键技术栈

---

## Task 0.2 - Core Questions (30min)

### Q1: 为什么需要Vector Database？

**我的思考：**
```
- 传统数据库（MySQL）能不能存embedding？
      可以，例如PostgreSQL + pgvector；MySQL 存 JSON array
- 如果能，为什么还要专门的Vector DB？
      传统数据库不适合高维近似最近邻搜索。
      在大规模数据下：全量扫描太慢，不支持高效 ANN 索引结构
- Vector DB解决了什么问题？
      高效 ANN 搜索（用更快的方法找到“足够近”的邻居，牺牲一点精度，换取巨大的速度提升。）
      支持 HNSW / IVF 等索引(Hierarchical Navigable Small World不再扫描所有向量，而是沿着图跳跃搜索。所以复杂度近似：O(log N))
      支持向量 + metadata 混合查询
      可扩展到百万 / 亿级向量
```

**查的资料：**
- [ ] Google: "vector database vs traditional database"
- [ ] Pinecone docs: https://docs.pinecone.io/docs/overview

**我的答案：**
```
Traditional databases can store embeddings, but they are not optimized for high-dimensional approximate nearest neighbor search. Vector databases implement ANN indexing structures like HNSW or IVF to enable scalable and efficient similarity search.
```

---

### Q2: Embedding vs Keyword Search的本质区别？
embedding是将文本映射到高维语义空间，使语义相似的文本在向量空间距离更近。
**我的思考：**
```
- Google搜索是keyword匹配
- Embedding搜索是什么原理？
- 举例说明两者区别
```

**查的资料：**
- [ ] OpenAI Embeddings Guide
- [ ] 试试看：写两个意思相同但用词不同的句子

**我的答案：**
```
[Google search like find what and where website conclude key word in a sentence. And Embedding is understand the meaning of sentence and the model infers the user’s implicit intent from the query. ]

Example:
Sentence A: "Tesla reduced emissions by 40%"
Sentence B: "Tesla cut CO2 output by 40 percent"

Keyword search会认为：key words are different they would return different results
Embedding search会认为：meaning are similar,results would similar
```

---

### Q3: 为什么要Chunk文档？
1 上下文窗口有限，token限制不能塞进整本书
### Q3.1 token限制？
Transformer 上下文窗口大小限制。      例如： 8k tokens 32k tokens超过就截断。
在 RAG 中： Question + Context + System prompt ≤ token limit
这决定：你能放多少 chunk  是否需要摘要


2 提高检索精度：精准到某个片段而不是查询匹配整篇语义
3 向量语义稀释问题：长文本embedding会变成“平均语义”导致向量表达不清晰

**我的思考：**
```
- 整篇PDF直接embedding不行吗？ 原因1：上下文窗口有限。LLM 有 token 限制，不能塞整本书。
- Chunk太小/太大会怎样？ 
- 金融文档的chunking策略？
```

**查的资料：**
- [ ] Google: "document chunking strategies RAG"
- [ ] LangChain text splitters

**我的答案：**
```
Firstly, embedding entiire document collapses mutiple semantic intents into a single vector.leading to semantic dilution and coarse retrieve granularity which significantly degrades retrieval precision and recall.
If chunk is too big to get exact meaning nor over the limit of the model, it is too small to get enough information nor lack of logic between the text.
For financial chunking, structure is the first important.第二，不要纯字符切也就是一刀割固定token，根据条款什么的超过限度再分割字符。表格易乱码要hi_res转markdown单独chunk。overloap是必要的，20到30%的overloap或50-150tokens。法规/10-K专门策略：明确点名10-K/财报pdf。测试不同 chunk_size：500 / 3000 的 trade-off。原则层面：
金融文档理想 chunk ≈ 600–1200 tokens
LangChain 实现层面：
chunk_size=1500–3000 characters（大致）

```

---

### Q4: Async vs Sync什么时候必须用async？

**我的思考：**
```
- 什么是阻塞？:做一件事是否需要等待，需要等待（当前线程什么都没有激活）就是阻塞。
- API调用为什么适合async？:API 调用是 I/O-bound，等待时间远大于计算时间。
- 数学计算需要async吗？不需要，因为async 解决的是：等待 I/O（网络、数据库、文件），而数学计算是：CPU / GPU 在持续运算，不存在“等待”
```

**查的资料：**
- [ ] FastAPI async: https://fastapi.tiangolo.com/async/

**我的答案：**
```
[在这里写你的理解]

应该用async的场景：
1.Web API 高并发 + 频繁外部 I/O（LLM API、Embedding API、Vector DB、SQL DB）
2.一个请求里要并发多个独立 I/O 调用（例如同时查多数据源、多向量库、多接口）
3.流式输出（streaming）或长连接场景

不需要async的场景：
1.单用户/离线脚本/Notebook（顺序执行即可）
2.CPU-bound 计算（NumPy、训练/推理、本地 heavy compute）；应考虑多进程/线程/GPU，而不是 async
3.请求链严格串行依赖、且并发量很低（async收益很小）
```

---

### Q5: 应该Cache什么？

**候选方案：**
A. Query的embedding
B. Pinecone搜索结果（TopK chunk_ids / chunks）
C. GPT生成的最终答案

**我的分析：**
方案A（Cache Query Embedding）:
- 成本：中（如果用外部Embedding API：有费用+网络延迟；本地embedding则成本低）
- 命中率：中（同样问题/相近问法会重复；可用normalize提升，如lowercase、去空格）
- 优缺点：
  - ✅ 优：安全、稳定；不依赖知识库更新；实现简单；能减少embedding API调用
  - ❌ 缺：问法稍变就miss；更换embedding模型版本需整体失效

方案B（Cache Pinecone 搜索结果）:
- 成本：中（减少向量检索的网络I/O和计算；也可连带减少后续rerank开销）
- 命中率：中（知识库/FAQ类问题重复率较高时命中更明显）
- 优缺点：
  - ✅ 优：显著降低检索延迟与成本；对高并发更有价值
  - ❌ 缺：有“过期风险”（知识库更新后TopK可能变化）；需要TTL或版本号（index_version/last_updated）做失效
  - ✅ 实践建议：cache key = hash(query + index_version)

方案C（Cache GPT最终答案）:
- 成本：高（LLM最贵、最慢，命中时省钱最大）
- 命中率：低~中（取决于是否FAQ/固定问题；问法变化会miss）
- 优缺点：
  - ✅ 优：命中后节省最大、延迟最低
  - ❌ 缺：风险最高（过期答案、错误固化/幻觉被缓存、多用户权限/个性化差异导致答案不适配）
  - ✅ 适用场景：静态FAQ、知识库低更新、同权限用户、答案可版本化；否则通常不缓存
  - ✅ 实践建议：cache key 必须包含 knowledge_version + user_scope（若多用户）

```

**我的选择：**
```
- 默认优先缓存：A（embedding）+ B（retrieval/rerank结果），TTL可设为：embedding 1h~24h；retrieval 10~30min（视知识库更新频率）
- C（最终答案）只在“高重复+低更新+同权限+版本控制”的FAQ场景启用
```
### Q6: Agent vs 普通RAG的区别？
```
普通 RAG
固定检索一次
无决策层
延迟低
成本低
适合单跳问题

Agent RAG
LLM 作为 Planner
可多次检索
可调用工具
延迟高
成本高
适合多跳复杂问题

我的思考：
- 普通RAG是"直接查数据"
- Agent是"先思考要不要查，怎么查"
- 这个思考过程值得吗？（考虑成本和latency）

场景分析：
Query 1: "What is Tesla's carbon emission?"
→ 普通RAG：直接查
→ Agent：也是直接查
→ 结论：这个case没必要用Agent

Query 2: "Compare Tesla vs Apple on emissions, who is better?"
→ 普通RAG：可能只查一个公司
→ Agent：会分两步查，然后对比
→ 结论：这个case Agent有优势
```

**去哪里查：**
- LangChain Agent概念：https://python.langchain.com/docs/modules/agents/
- 只看"Agent概念"部分，不要看具体实现

---

 ### Q7：为什么prompt 在 LLM 前
 将检索知识注入上下文实现grouded generation
 LLM 只读取输入的 token。检索到的知识必须通过 Prompt 拼接进输入，模型才能“看到”它。


 ### Q8：为什么会 hallucination？
 1 目标函数不等于事实验证
 2 信息不足
 3 噪声过多

## Token Budget 怎么分配？

模型 token 主要分为：
System Prompt
+ Retrieved Context
+ User Question
+ Response

---

### 分配原则

1️⃣ 优先保证 Response 空间  
避免输出被截断。

2️⃣ Context 质量 > 数量  
不要塞满 token，应提高 rerank 精度和证据密度。

3️⃣ 留出“推理空间”  
复杂问题需保留 20~40% token 给生成。

---
### 示例（8k 上限）

- 500~800：System + Instruction
- 4000~5000：Retrieved Context
- 2000~3000：Response

核心原则：
> 不要让 context 吃光 token 预算。


## Cache 放在哪里？

### Offline Pipeline
raw → chunk → embedding → vectorstore

### Online Pipeline
query → embedding → retrieve → rerank → fetch → prompt → LLM

---

### ✅ 1️⃣ Cache Query Embedding
位置：
query → [cache] → embedding

优点：
- 减少 embedding API 调用
- 风险低

---

### ✅ 2️⃣ Cache Retrieval / Rerank 结果
位置：
retrieve → [cache]
rerank → [cache]

优点：
- 降低向量搜索成本
- 降低 rerank 计算

注意：
- 需要 index_version 或 TTL 做失效控制

---

### ⚠ 3️⃣ Cache 最终答案（谨慎）
位置：
LLM → [cache]

优点：
- 节省最大成本

风险：
- 过期答案
- 错误固化（hallucination freeze）
- 多用户权限问题

适用：
- 静态 FAQ
- 低更新知识库
- 单用户场景


###极限降低 hallucination 的工程手段（不靠继续调 prompt）
Beyond prompt constraints, hallucination can be reduced by adding verification layers: citation-based grounding, abstention when evidence is insufficient, post-generation factuality checks, extract-then-generate pipelines, and hybrid retrieval to improve recall.

(1) 引用约束与可追溯输出（Citations / Attribution）

要求模型输出每个关键结论对应的 chunk_id 或引用编号
没有引用就不允许输出该结论（或降级为“不确定”）
这能强制模型“贴证据说话”，减少凭空补全

(2) 置信度与拒答策略（Abstain / “Insufficient info” Gate）

在生成前或生成后加一个判定：
检索到的证据是否覆盖问题要点？
覆盖不足 → 直接拒答/要求澄清/返回“资料不足”
这比“强行回答”更能避免幻觉。

(3) 事实一致性校验（Post-check / Verification）

生成后做检查，而不是只靠生成时约束：
Self-check：让另一个 LLM 只基于 context 判断答案中的每条事实“是否被支持”
Rule-based check：数值、年份、单位、比较关系是否一致（正则/解析）
不通过 → 让模型改写或删掉不支持的句子
这一步在工程里非常常见：先生成，再审计。

(4) 结构化提取 + 再生成（Extract-then-Generate）

不要直接让LLM写长段落：
先从 context 抽取结构化事实（表格/JSON）：公司、指标、年份、数值、单位
再根据结构化事实生成对比结论
这样能明显降低“编数字/编年份”。

(5) 混合检索（Hybrid Search: BM25 + Vector）

很多幻觉来自“检索错了/漏了”：
用 BM25（关键词精确）补向量检索的漏召回
合并候选再 rerank
尤其对：数字、专有名词、年份、型号 更稳。

(6) 上下文压缩（Contextual Compression）

不是“更多 chunk”，而是：
对候选 chunk 做摘要/关键句抽取
去噪、去重复
把证据浓缩到更小 token 里
减少 attention 稀释，提高证据密度。
。

🟢 第3阶段（15分钟）阅读材料

你查这三样：

“Bi-encoder vs Cross-encoder”

“LLM hallucination causes”

“Attention dilution in long context”

不需要论文，只要博客级别。







---

## Task 0.3 - Tech Stack Decisions (20min)

### Decision Matrix

| 需求 | 候选方案 | 我的选择 | 理由 |
|------|---------|---------|------|
| **Web框架** | Flask / FastAPI / Django | FastAPI| FastAPI 原生支持 async、类型提示、自动 OpenAPI 文档，适合 RAG API 服务化。|
| **Vector DB** | Pinecone / ChromaDB / Weaviate | romaDB| 无需账号/计费/网络；调试快，如果目标是“用 Pinecone 做亮点”且你已经在用 Pinecone：Pinecone|
| **LLM** | OpenAI / Claude / 开源 | Claude| 同一家同时提供 embeddings + LLM，接口统一；工程集成简单、文档充足|
| **部署** | AWS / Railway / Render | Railway |Railway/Render 部署体验更贴近“Demo 交付”，更符合求职展示需求。AWS 适合后续 Phase 5：确定要做生产化时再上。 |
| **前端** | React / Streamlit / HTML | Streamlit | Streamlit 把精力留在 RAG 质量和展示逻辑（contexts、citations、latency）。React 只有在追求“产品级 UI”时才值得；Phase 0 不需要。|

### My Final Stack
```
Backend: [FastAPI]
Vector DB: [Pinecone]
LLM: [OpenAI]
Deployment: [Railway]
Frontend: [Streamlit]

Overall Architecture:
离线 ingest：chunk→embedding→upsert Pinecone（存 vector+metadata）；docstore 存 chunk_text；在线 query：embedding→Pinecone topK→rerank→fetch→prompt→LLM；Streamlit 展示答案+引用。
```

---

## Failure Points

### 1️⃣ Retrieval Recall 不足
Problem:
Retrieve 没找到真正相关的 chunk。

Cause:
- chunk 太大
- embedding 模型不匹配
- ANN 近似误差

Impact:
LLM 被迫补全 → hallucination

Mitigation:
- 减小 chunk size
- hybrid search (BM25 + vector)
- 增加 topK
2️⃣ Rerank Precision 不足
Problem:
Rerank 排序错误。

Cause:
- topK 太少
- rerank 模型弱
- query 太复杂

Mitigation:
- 增加候选数
- 更强 cross-encoder
3️⃣ Attention 稀释
Problem:
塞入过多 chunk，重要信息被淹没。

Cause:
- token 过多
- 未排序

Mitigation:
- relevance sorting
- summary compression
4️⃣ Token Budget 超限
Problem:
上下文被截断。

Cause:
- 没计算 token
- prompt 过长

Mitigation:
- 预估 token
- dynamic truncation
5️⃣ Hallucination
Problem:
模型编造信息。

Cause:
- context 不足
- 未加 grounded 指令

Mitigation:
- 强约束 prompt
- 引用编号
- 不足则拒答
在每个 Failure Point 后面加一句：

Design Trade-off:

例如：

增加 topK 提高 recall，但会增加 rerank 计算量。
强约束 prompt 降低 hallucination，但可能降低生成灵活性。


## Phase 0 Completion Checklist

- [x] 架构图已完成（纸笔）
- [x] 5个核心问题已回答（8个）
- [x] 技术选型已完成
- [x] 所有决策都有明确理由
- [x] 知道去哪里查文档

**Completed at**: 24/02/2026 
**Total time**: 5:16 PM

---

## Key Learnings
```
1. RAG = Retrieval → Rerank → Generation
2. 最大风险：Recall不足 + Attention稀释
3. 选型原则：最小复杂度 + 可演示 + 可替换

今天学到的Top 3点：
1. RAG 的核心不在“模型大小”，而在检索质量与证据组织。
2. Retrieval 与 Rerank 的调优必须基于评估集，而不是主观感觉。
3. Hallucination 多数源于证据缺失或过载，而不是模型能力不足。


面试可以说的：
- 
```
- 我把 RAG 拆成 Retrieval、Rerank、Generation 三层，并分别分析了各自的失败模式。
- 我理解 Recall 与 Precision 的区别，并知道如何通过离线评估来调优 chunk 和 topK。
- 在架构设计阶段，我优先考虑最小复杂度与可替换性，而不是过早优化。
---

## Questions for Claude
```
完成后我不确定的点：
1. 在多用户场景下 cache 如何做版本控制？
2. 什么时候应该引入 rerank，而不是只调 topK？
3. 在实际项目中，如何设计一个最小但有效的评估集？
```