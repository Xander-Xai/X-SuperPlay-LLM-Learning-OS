# RAG 六周执行手册｜24 个学习任务

> 这是参考日程，每周四个可验收任务；实际学习采用需求驱动原则，遇到工作/面试问题可跳转，不把打卡等同能力证明。各任务必须交“原理+实现+实验+结论”的证据卡，做到有日志和失败分析。每天约 2–3 小时，建议理论25% / 实作35% / 评测25% / 复述15%。

## 第 1 周：R01–R02（基础与数据处理）

- [ ] **W1-D1 全链路白板**：读 [R01](CORE-01-05.md)、[RAG 论文](https://arxiv.org/abs/2005.11401)，画离线/在线两图；分别解释 RAG、SFT、SQL、长上下文何时更合适。验收：3 个反例和成本/风险边界。
- [ ] **W1-D2 PDF/扫描与表格解析**：按 [Docling](https://github.com/docling-project/docling) 与 [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) 文档准备 3 份公开或自造的 PDF/表格，逐行核查页码、表格单元与 OCR 错行。验收：解析原文与错误清单（尚未运行须写 NOT RUN）。
- [ ] **W1-D3 Chunk 消融设计**：用同一原文设计固定 256/512/1024 Token、标题切分与 Parent–Child；保存独立 Gold 源片段和 context token 预算。验收：错切“否定/表格/跨段”各一例，实验未执行不得造 Recall。
- [ ] **W1-D4 最小 Pipeline**：运行 [小型离线实验](lab/README.md) 和 [120 题数据](goldset/README.md)；画出检索到引用映射的最短链路。验收：实际退出码 + 一份误检分析。

## 第 2 周：R03–R04（向量与索引）

- [ ] **W2-D1 Embedding 计算链**：手算两个归一化向量的 Cosine/Dot/L2，解释 pooling、对比损失、Hard Negative。验收：说明哪些条件下 Dot 与 Cosine 等价。
- [ ] **W2-D2 真实模型准备**：根据 [BGE 官方模型卡](https://huggingface.co/BAAI/bge-m3) 固定 revision、模型卡和许可；使用 [本地 Embedding 实验入口](lab/real_embedding_eval.py) 的 dry run。验收：若模型缺失标 NOT RUN，不自动下载。
- [ ] **W2-D3 BM25 vs Dense**：运行 Gold Set BM25 并在合法环境中运行本地 BGE 对照；比较多义、编号及同义问题。验收：分桶 Recall/MRR、模型名与运行日志；禁止把合成 BM25 叫真实 ES 结果。
- [ ] **W2-D4 HNSW/IVF 理论与参数**：读 [HNSW 原论文](https://arxiv.org/abs/1603.09320)，设计 M/efSearch 与 IVF nprobe 的 FLAT 真值对照。验收：Recall–延迟–内存三维取舍；没有 ANN 环境时保持未运行。

## 第 3 周：R05–R06（混检与 Query）

- [ ] **W3-D1 两路召回**：在相同权限和版本过滤下跑 BM25 与真实 Dense（无模型则用 toy 的词法双路演示）。验收：每路 Top-N、重合率与漏召回原因。
- [ ] **W3-D2 排名融合**：手算 RRF，运行 Gold Set multiquery_rrf，定位仅一路高价值文档排名下降的反例。验收：解释 RRF k 与 Top-K 不同。
- [ ] **W3-D3 CrossEncoder 精排**：读 [官方 Retrieve & Re-Rank](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html)，基于同一候选设计有/无精排消融。验收：NDCG、P95、成本、是否真的运行。
- [ ] **W3-D4 Rewrite/HyDE**：运行多轮 bucket 的 original 与 rewrite，对“在欧盟呢？”补前文并构造意图漂移负例。验收：原 Query 与 Rewrite 双保存；解释 HyDE 的假设文本不是证据。

## 第 4 周：R07–R08（证据与评测）

- [ ] **W4-D1 标注数据**：检查 [120 题模板](goldset/README.md)，把最少 10 条换成公开文档的人工校对源片段；评测集和训练/调参集必须按来源文档族拆分。验收：标注者、Gold、许可与数据版本。
- [ ] **W4-D2 Retrieval Metrics**：手算 1 组多 Gold 的 Recall@K/Hit/MRR/nDCG，执行合成评测。验收：105 正例与 15 负例分母独立、指标含义不混淆。
- [ ] **W4-D3 证据门控与引用**：定义 Evidence Gate 与 Answer Gate，设计“证据缺失/过期/冲突/注入”四类负例。验收：未授权文档不可进入生成 Context；不以相似度替代证据充分。
- [ ] **W4-D4 Ragas 与人工校准**：按 [Ragas 官方教程](https://docs.ragas.io/en/stable/tutorials/rag/) 实际版本选择 Faithfulness、Correctness、引用准确性；没有 Judge/人工标注则写 NOT RUN。验收：独立记录 Judge 版本、误答和误拒。

## 第 5 周：R09（生产工程与性能）

- [ ] **W5-D1 文档增量与版本**：设计原文/Chunk/ES/向量索引一致版本与蓝绿切换，模拟删除和更新失效。验收：索引版本错误与回滚动作。
- [ ] **W5-D2 权限边界**：模拟跨租户、权限撤销后缓存、过期文档和引用二次读取。验收：服务端过滤设计；教学 ACL=0 泄漏不代表生产安全。
- [ ] **W5-D3 观测与故障恢复**：给 Rewrite、检索、Rerank、LLM、Answer Gate 添加 Trace 字段模板，列超时/重试/熔断/降级策略。验收：P95 分阶段归因而非猜测。
- [ ] **W5-D4 性能/成本评测**：固定负载/并发/模型/Token 长度，设计 P50/P95、QPS、缓存命中、每问成本的对照。验收：无实际压测不可写实测数字。

## 第 6 周：R10（高级与面试）

- [ ] **W6-D1 多模态区别**：比较 OCR 文本、CLIP 图像召回、VLM 视觉理解；设计一份表格/包装图证据案例。验收：说明 BGE 与 CLIP 为什么不直接混算向量。
- [ ] **W6-D2 GraphRAG/Agentic RAG**：读 [GraphRAG](https://github.com/microsoft/graphrag) 与 [Agentic RAG](https://huggingface.co/learn/agents-course/en/unit3/agentic-rag/agentic-rag)；比较静态/动态/图检索。验收：成本和何时不值得上这些框架。
- [ ] **W6-D3 技术决策与失败复盘**：选 3 个此前失败案例，写“基线→根因→受控实验→改进/退化→边界”。验收：包含 NOT RUN / PASS / FAIL / INCONCLUSIVE 状态。
- [ ] **W6-D4 面试闭卷**：完成 [12 个问题](INTERVIEW.md)，至少口述完整链路、RRF、HNSW、Recall 与 ACL。验收：用 [L0–L4](../../assessments/CAPABILITY-RUBRIC.md) 的独立证据而非复述打分。

## 统一证据卡模板

~~~text
Task ID / Current demand / Status (NOT RUN | RUNNING | PASS | FAIL | INCONCLUSIVE)
Why / Professional mechanism / Plain language / Two failure modes
Source URL, checked-on, version/commit / Query and Gold / Dataset hash
Run command / Exit code / Log path / Baseline & single changed variable
Retrieval metrics and denominator / Citation & abstain denominators / Latency & cost
Independent explanation / Blind example / Next smallest gap / Stop decision
~~~

已有离线材料与真实模型之间存在明确边界；“完成学习计划”必须由个人独立讲解、运行、对照和排障证据证明。
