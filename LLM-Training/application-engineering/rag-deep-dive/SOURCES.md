# RAG 权威资料账本（课程使用版）

目的：优先使用论文原文、研究者教材、官方实现与可复核文档；二手视频用来启发，不作为未经核对的正确性依据。与 [全仓来源分级](../../resources/AUTHORITATIVE-INDEX.md) 一致：P0 原始论文/官方规范与实现，P1 作者授课/工程实践，P2 社区讨论仅作线索。

**核查说明**：2026-11-14 对标“直接来源”的候选做网页检索与页面内容抽样核对；下表“抽查”仅指页面身份和主题可核实，**不是每条深层链接、每个 API 版本、所有资源完整性/可安装性已实测**。动态文档用于学习时再固定 release/tag/commit 与环境版本。上游本仓 RAG 来源保留 [固定 SHA](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/practice/rag/README.md)，不复制其教学代码。

| 来源 ID | 学习主题 | 一手/官方参考 | 重点读什么 | 审计说明 |
|---|---|---|---|---|
| S01 | R01 | [RAG 2020 原论文](https://arxiv.org/abs/2005.11401) | 参数记忆/外部检索与原始架构 | 论文页面抽查 |
| S02 | R01 | [LangChain Retrieval](https://docs.langchain.com/oss/python/langchain/retrieval) | 当前工程划分与 API 边界 | 官方，动态 API 按版本复核 |
| S03 | R02 | [Docling 官方代码](https://github.com/docling-project/docling) | 版面、表格、OCR、结构输出 | 仓库抽查，运行版本待固定 |
| S04 | R02 | [Anthropic Contextual Retrieval](https://www.anthropic.com/research/contextual-retrieval) | Chunk 上下文与成本/效果 | 原厂研究页抽查 |
| S05 | R03 | [BGE-M3 模型卡](https://huggingface.co/BAAI/bge-m3) | Dense/Sparse/ColBERT 与长度维度 | 模型卡抽查，revision 待固定 |
| S06 | R03/R05 | [Sentence Transformers Retrieve & Re-Rank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) | BiEncoder vs CrossEncoder | 官方教程抽查 |
| S07 | R04 | [Stanford IR 教科书](https://www-nlp.stanford.edu/IR-book/) | 倒排索引、打分与评测第 1/6/7/8 章 | 作者教材抽查，经典基础而非新 API |
| S08 | R04 | [Milvus Index Explained](https://milvus.io/docs/index-explained.md) | ANN 的时间-空间-召回权衡 | 官方文档抽查 |
| S09 | R04 | [Milvus HNSW](https://milvus.io/docs/hnsw.md) | M/efConstruction/ef 参数 | 官方文档抽查 |
| S10 | R04/R05 | [Elastic Hybrid Search](https://www.elastic.co/docs/solutions/search/hybrid-search) | BM25+Dense、RRF | 官方文档抽查 |
| S11 | R05 | [Elastic RRF 参考](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion) | RRF 公式、名次、k | 官方文档抽查 |
| S12 | R07/R08 | [Ragas Faithfulness](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/) | Claim Support 计算 | 官方文档抽查，执行需要版本 |
| S13 | R08 | [Ragas Metrics](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) | 各分项输入和局限 | 官方文档抽查 |
| S14 | R08 | [Ragas Context Precision](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/context_precision/) | 与 Recall/Hit 的区别 | 官方文档抽查 |
| S15 | R08 | [BEIR](https://github.com/beir-cellar/beir) | 检索统一基准及 nDCG/MRR | 社区/论文配套项目；本轮未运行 |
| S16 | R09 | [OWASP RAG 安全指南](https://cheatsheetseries.owasp.org/cheatsheets/RAG_Security_Cheat_Sheet.html) | 文档注入、租户隔离、完整流水线威胁 | 权威安全指导抽查 |
| S17 | R10 | [Microsoft GraphRAG](https://github.com/microsoft/graphrag) | 图索引/社区摘要/成本及维护状态 | 官方研究仓库抽查，偏维护模式 |
| S18 | R10 | [Hugging Face Agentic RAG](https://huggingface.co/learn/agents-course/en/unit3/agentic-rag/agentic-rag) | 工具选择与动态检索 | 官方教学页抽查 |
| S19 | R02/R06 | [LangChain RAG From Scratch](https://github.com/langchain-ai/rag-from-scratch) | 分步 Notebook 与优化思路 | 官方示例仓库，运行版本待核 |
| S20 | R03 | [BGE 官方仓库](https://github.com/FlagOpen/FlagEmbedding) | 实际编码/重排实现 | 源码入口，使用前锁 commit |
| S21 | R07–R08 | [本仓 Ragas](../RAGAS-EVALUATION.md) | 现有 19 案例与可选 Judge API | 本仓既有课程，不是第三方证据 |
| S22 | R01–R10 | [本仓既有应用工程 Lab](../labs/README.md) | Synthetic pipeline、拒答/权限/工具 | 仅离线合成，不是生产验证 |


| S23 | R01–R09 | [DeepLearning.AI RAG 系统课程](https://www.deeplearning.ai/courses/retrieval-augmented-generation) | 以课程作骨架、动手比较 BM25/RRF/向量与评测 | 作者课程 P1，课程页面抽查，权益/内容可能变 |
| S24 | R02/R05/R08 | [Building and Evaluating Advanced RAG](https://www.deeplearning.ai/courses/building-evaluating-advanced-rag) | Sentence-window、Auto-merging、RAG Triad | 作者课程 P1，课程页面抽查 |
| S25 | R05/R06 | [Advanced Retrieval for AI with Chroma](https://www.deeplearning.ai/courses/advanced-retrieval-for-ai) | Query Expansion、CrossEncoder、Embedding Adapter | 作者课程 P1，课程页面抽查 |
| S26 | R01/R02 | [LlamaIndex Introduction to RAG](https://developers.llamaindex.ai/python/framework/understanding/rag/) | Loading、Indexing、Storing、Querying、Evaluation | 官方手册抽查，当前 API 依版本复核 |
| S27 | R02/R10 | [PaddleOCR 官方仓库](https://github.com/PaddlePaddle/PaddleOCR) | OCR/结构化解析质量与版本 | 官方源码抽查，实际 OCR 未运行 |
| S28 | R03/R10 | [OpenAI CLIP 官方仓库](https://github.com/openai/CLIP) | 图文对比学习/相容向量空间 | 官方源码抽查，实际 CLIP 未运行 |


| S29 | R05 | [RRF 原始 SIGIR 论文 DOI](https://doi.org/10.1145/1571941.1572114) | 排名融合原理 | 一手论文，2026-11-15 页面核对 |
| S30 | R04 | [HNSW 原论文](https://arxiv.org/abs/1603.09320) | 图结构、ef/M、召回-效率权衡 | 一手论文，2026-11-15 论文核对 |
| S31 | R06 | [HyDE 原论文](https://arxiv.org/abs/2212.10496) | 生成假设文本作为检索表示，不是事实证据 | 一手论文，版本/实施待核 |
| S32 | R10 | [Corrective RAG 论文](https://arxiv.org/abs/2401.15884) | 检索纠错与补检 | 一手论文，2026-11-15 论文核对 |
| S33 | R10 | [Adaptive RAG 论文](https://arxiv.org/abs/2403.14403) | 按查询复杂度选择检索策略 | 一手论文，2026-11-15 论文核对 |
| S34 | R07/R08 | [Ragas 稳定版 RAG 教程](https://docs.ragas.io/en/stable/tutorials/rag/) | 逐步评估 RAG 与数据录入 | 官方 stable 页面，2026-11-15 核对；使用时仍固定包版本 |

## 资料取用策略

- 第一次：先看本专项对应 Rxx 讲义，选该行 1 个 P0 原文/官方手册，回答“它为什么有效/何时失效”。
- 第二次：对照官方源码/实验 API，只实现最小版本；固定环境 pip freeze、模型 revision、源文档 hash。
- 第三次：加入一个难负例与基线消融，记录数值/Trace、可能的混杂因素；无法得出结论就标 INCONCLUSIVE。
- 第四次：脱离资料讲出来并换一个未训练场景独立复核；按 [Rubric](../../assessments/CAPABILITY-RUBRIC.md) 而不是观看量验收。

**稳定性策略**：优先 DOI/arXiv、官方仓库固定 tag/commit、官方文档入口；网页可能迁移，修复 URL 时维护本账本和 checked_on。公开模型/文档不意味着允许重新分发其中全文、训练数据或商业使用；保留来源版权与许可要求。
