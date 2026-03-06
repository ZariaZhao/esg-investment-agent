Phase 1: 高保真数据引擎 (1.5h)
目标：解决 ESG PDF 的解析乱码，为后续分析打下“干净”的数据基础。

核心任务：

PDF 解析选型：对比 PyMuPDF (fitz) 和 Unstructured。重点解决财报中的表格（Table）提取问题。

Markdown 转换：将提取的文本转为 Markdown 格式，保留标题层级（Header）。

你应该搜索的资料：

"PyMuPDF extract table to markdown"

"Unstructured.io hi_res strategy for PDF tables"

完成标准 (KPI)：

[ ] 成功将一份 ESG PDF 转为带表格结构的 Markdown 文件。

[ ] 能够手动通过正则或工具提取出“Environment”章节的起始位置。
























Phase 2: 语义分块与索引构建 (2.5h)
目标：拒绝一刀切，建立符合金融逻辑的搜索深度。

核心任务：

Recursive Chunking：实现基于字符和层级的递归切分。针对法律/金融文档，设置 chunk_size 在 800-1200 tokens 之间。

Metadata 注入：在向量库（Pinecone）中为每个块注入 {"company": "...", "year": 2025, "section": "Social"}。

你应该搜索的资料：

"LangChain RecursiveCharacterTextSplitter separators list"

"Pinecone metadata filtering best practices"

完成标准 (KPI)：

[ ] 成功将所有 Chunk 及其 Embedding 上传至 Pinecone。

[ ] 实现一个简单的 Metadata Filter 脚本（例如：只检索 2025 年的数据）。

Phase 3: 核心检索逻辑与 Agent 雏形 (2.5h)
目标：从“查数据”进化为“懂意图”，解决术语匹配失效问题。

核心任务：

Hybrid Search：结合词法搜索 (BM25) 和向量搜索。这是为了应对金融领域特定的法律条文代号检索。

Agent Logic (V1)：使用 FastAPI 封装接口，并加入初步的“查询规划”（例如：判断用户是问“单一事实”还是“跨年度对比”）。

你应该搜索的资料：

"Hybrid Search RRF algorithm python implementation"

"FastAPI async def vs def for OpenAI API calls"

完成标准 (KPI)：

[ ] 实现一个 hybrid_search 函数并返回合并排序后的 Top-5 结果。

[ ] 接口延迟在网络正常的 South Yarra 环境下控制在 3s 以内。

Phase 4: 系统评估与性能优化 (1.5h)
目标：用数据支撑你的简历，而不是靠“感觉”。

核心任务：

RAGAS 评估：计算 Faithfulness (忠实度) 和 Answer Relevancy (相关性)。

Embedding Cache：在内存或 Redis 中缓存 Query 的向量，减少重复请求的开销。

你应该搜索的资料：

"Ragas evaluation faithfulness formula"

"Semantic caching for LLM applications"

完成标准 (KPI)：

[ ] 生成一份包含 10 个问题的 RAGAS 评估报告（CSV/JSON）。

[ ] 能够量化说明：加入重排序（Re-rank）后，回答准确率提升了多少百分比。

Phase 5: 部署与工业级呈现 (1h)
目标：让你的项目在面试官面前“真实可触”。

核心任务：

Railway 部署：将 FastAPI 后端部署上线。

README 文档：撰写包含架构图、技术决策（Trade-offs）和效果演示的英文文档。

你应该搜索的资料：

"Railway.app deploy fastapi dockerfile"

"Best README for machine learning engineer projects github"

完成标准 (KPI)：

[ ] 一个可以在外网访问的 API 链接。

[ ] GitHub 项目首页有一张清晰的系统架构图。