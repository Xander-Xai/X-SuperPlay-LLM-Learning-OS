# RAG 深入学习专项：完整链路、实验与独立能力验收

> 定位：本目录是 [APP-RAG](../RAG-ENGINEERING.md) 的深入教学支线。不是新建 M13、不是替代 [上游已存在的 RAG 练习](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/practice/rag/README.md)，不把教学文档当成实际项目业绩。状态：CURRICULUM_READY / SYNTHETIC_LAB / REAL_RAG_NOT_RUN / LEARNER_UNASSESSED。

## 目标与使用方式

针对已有 ES、Milvus、BGE、CLIP、OCR、RRF、CrossEncoder、Evidence Gate 项目经验，但基础概念与全链路解释尚不够连贯的学习者：从原理、失败模式、可测对照，走向可复现工程设计和独立讲解。核心是 **解释为什么这样做、何时不用、怎样测它确实更好**。

最小导航：
1. [01–05 基础与检索](CORE-01-05.md)：适用边界→解析/Chunk→Embedding→BM25/ANN/Hybrid→RRF/Rerank。
2. [06–10 生成、评测、工程与高级](CORE-06-10.md)：Query→Grounding→评测→生产→多模态/Graph/Agentic。
3. [权威来源证据账本](SOURCES.md)：论文/教科书/官方文档，按任务精读；区分已抽查与待版本复核。
4. [实验设计与验收](LABS.md)：按需选择对照，不虚构跑分。附 [纯标准库检索微型实验](lab/README.md)。
5. [面试答辩题卡](INTERVIEW.md)：12 个核心问法、追问和证据模板。
6. [本轮交付与状态](ACCEPTANCE.md)：静态、自动化与真实模型的证据边界。

## 两条管道，先画对

~~~mermaid
flowchart LR
 A["离线：文档/图片/表格+许可/版本/ACL"] --> B["解析/OCR/表格结构/去重"]
 B --> C["Chunk+父子关系+页码+来源"]
 C --> D["Embedding+BM25倒排/ANN索引+原文"]
 U["在线：Query+Principal+会话上下文"] --> Q["Rewrite/路由/过滤条件"]
 Q --> R["服务端权限与版本过滤→BM25+Dense"]
 D --> R
 R --> F["融合/Rerank→证据充分性"]
 F --> G["Context预算与引用定位→LLM"]
 G --> V["逐主张核查/拒答/输出"]
 V --> M["Gold Set+Trace+P95/成本+回归"]
~~~

注意：精确库存/订单金额应查业务 API/SQL；法规变更应查有时效和授权的来源。RAG 不是必须包含向量库，长上下文直读、BM25、SQL 都是有效对照基线。

## 十个主题与独立产物（不是另起 10 个训练模块）

| ID | 能力 | 必交的最小证据 | 等级优先 |
|---|---|---|---|
| R01 | RAG 适用边界与全流程 | 离线/在线两图 + 3 个不应使用向量检索的反例 | P0 |
| R02 | 解析、OCR、Chunk、元数据 | 同文档 3 策略的错切例、页码/表格证据 | P0 |
| R03 | Embedding 原理与选型 | tokenizer/pooling/归一化、同题检索消融 | P0 |
| R04 | BM25、Dense、ANN、Hybrid | BM25 公式、ANN 参数与 Recall/延迟对照 | P0 |
| R05 | RRF 与 Bi-/CrossEncoder | 排名融合手算、重排成本与反例 | P0 |
| R06 | Rewrite/HyDE/多轮路由 | 保留原问题、前后 Recall 与错改反例 | P0 |
| R07 | Evidence/Answer Gate/引用 | 无证据、冲突、过期、注入的拒答与核查 | P0 |
| R08 | 检索/生成/系统分层评测 | Gold Set、分母、指标和故障归因报告 | P0 |
| R09 | ACL、版本、部署和性能 | 无权限泄漏、撤权、缓存隔离、Trace | P0 |
| R10 | 多模态/GraphRAG/Agentic | 复杂度-收益-成本的技术选型说明 | P1 |

完整细目见 [01–05](CORE-01-05.md) 和 [06–10](CORE-06-10.md)。

## 六周参考排期（可中断的需求驱动路径，不是必修课表）

| 参考周 | 聚焦 | 退出产物 |
|---|---|---|
| W1 | R01–R02：地图、解析、Chunk | baseline 与坏解析负例 |
| W2 | R03–R04：Embedding、BM25、ANN | 同题检索消融报告 |
| W3 | R05–R06：混合召回、RRF、Query | top-k 与 Rewrite 回归 |
| W4 | R07–R08：生成可信性、评测 | 120 题标注方案、误答/误拒分开 |
| W5 | R09：版本、ACL、P95 和成本 | Trace + 越权/更新负例 |
| W6 | R10 + 面试：OCR/VLM/Graph/Agentic | 模型选型证据 + 12 问闭卷口述 |

每天参考 2–3 小时：原理 25%、动手 35%、评测 25%、闭卷复述 15%。**重要：当下需求若只卡在 ACL 或 Recall，可直接跳 R09 / R08；不可用“打卡六周”代替 [L0–L4 能力评分](../../assessments/CAPABILITY-RUBRIC.md)。**

## 学习动作闭环

选择真实或脱敏问题 → 记录无训练 baseline → 查 P0/P1 资料与必要前置 → 运行一项单变量实验与至少两种负例 → 给出专业定义/白话/失败边界 → 保存数据版本、代码 SHA、配置、日志、成本与未知项 → 独立解一道新题 → 达标即停。

**今日最小任务**：先运行 [离线教学微实验](lab/README.md)，解释 BM25、RRF、ACL 和 Recall@K 的真实代码行为，再去替换真实 ES/Milvus/BGE。不要把这里的预制排名叫作向量语义召回。
