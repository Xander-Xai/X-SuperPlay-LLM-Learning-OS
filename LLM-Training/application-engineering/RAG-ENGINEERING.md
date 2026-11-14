# RAG 全链路工程｜从检索到证据支持，不只会建向量库

**定义**：Retrieval-Augmented Generation 在推理阶段检索外部证据，将可信、授权、相关且适当新鲜的材料提供给生成模型。通常不修改模型权重。**大白话**：员工不用背库存/法规，先从有权限的最新版资料里查，再基于证据回答。

## 1. 全链路与边界（P0）

~~~mermaid
flowchart LR
  D["文档/表格/图片→版本与权限"] --> X["解析/OCR→Chunk/Metadata→质量/去重"]
  X --> I["Embedding/Index/ES/Vector"]
  Q["用户问题+身份/租户/时间"] --> R["Rewrite/Query Routing"]
  R --> S["ACL过滤后: BM25/稠密/Hybrid召回"]
  I --> S
  S --> F["RRF / Cross-encoder Rerank / Parent-doc"]
  F --> G["证据门禁：相关性/可回答性/冲突/版本"]
  G --> C["Context预算/序列化/引用ID"]
  C --> L["LLM生成→Claim/Citation验证"]
  L --> E["任务评测/拒答/权限/耗时/反馈"]
~~~

**区别**：Recall/Rerank 决定“有没有找对材料”；Context Engineering 决定“哪些材料最终进模型”；Prompt 决定“如何回答”；Evidence/Answer Gate 决定“何时拒绝/如何验真”；数据授权和 ACL 在检索/服务端实现。RAG 不必使用向量数据库：SQL/FAQ/BM25/全文索引也可能是更好的基线。

## 2. 最小知识树

| 学习点 | 专业定义 | 白话类比 | 最小验证 |
|---|---|---|---|
| Chunking/Parsing/OCR | 文档边界、页码、布局、表格、来源和内容哈希决定可检索单元 | 书先正确分章节和页码 | 表格拆坏/图片文字丢失的负例 |
| Sparse/Dense/Hybrid | BM25 词项匹配 vs Embedding 语义召回，混合检索合并结果 | 按关键词找书与按意思找书 | 中文别名、配方编号、改写问题分别测 Recall@k |
| RRF/Rerank | RRF 按排序名次聚合；CrossEncoder 联合 Query/Doc 评分 | 先粗筛，再细看候选 | 固定候选比较 Recall/Precision/nDCG 与 CPU/延迟 |
| ACL/Time/Version | 每个检索文档带 tenant/role/source/version/validity；请求按用户权限过滤 | 可看的资料才能进会议室 | 跨租户诱饵文档 + 过期文档拒入 |
| Evidence Gate | 不满足可信证据/冲突过大时拒答或要求澄清 | 没证据不能写结论 | 同名产品冲突、检索为空、引用伪造负例 |
| Citation Support | 每条关键事实 Claim 要能被证据推导并标注来源 | 报告必须能找到原文 | 引用存在却不支持结论的反例 |
| Retrieval vs Generation Eval | Recall@k、MRR、nDCG 与 Faithfulness/E2E 分开 | 找对书和回答对问题是两门考试 | 固定题集分桶检索失败/生成失败 |

## 3. Ragas 是评测，不是 RAG 的另外一个算法

Ragas 官方列出 Context Precision、Context Recall、Response Relevancy、Faithfulness、Noise Sensitivity；Agent 用例含 Tool Call Accuracy 和 Agent Goal Accuracy。不同指标依赖不同输入字段、参考答案和/或 Judge 模型，**不能把“Faithfulness 高”当成事实绝对正确，也不能把 Context Precision 当成 Recall**。

操作/公式/版本详见 [Ragas 与 Task Eval](RAGAS-EVALUATION.md)。项目源码可参照 [HF RAG Course](https://huggingface.co/learn/cookbook/en/rag_zephyr_langchain) 和 [LangChain RAG 教程](https://docs.langchain.com/oss/python/langchain/retrieval)；具体版本在执行时核实。

## 4. 三个实战路由（按需选一条）

1. **引用编造**：建立含 gold evidence/doc ID 的固定测试集；先测关键证据 Recall@5，再测 Faithfulness/Claim Support，再单独测 Answer Gate 拒答。先检查 OCR/Chunk/Ranking，而不是盲目 SFT。
2. **新旧法规冲突**：索引添加版本/生效日期/来源优先级；在授权数据上测试仅允许最新有效版本；禁止让 LLM 自行决定能否访问私有资料。
3. **检索效果不稳定**：对比 BM25、Dense、Hybrid+RRF 与 CrossEncoder，在同题同权限/相同上下文预算下做消融，记录 P95/Cost/准确性和受控负例。

**最短路线**：[上游 RAG 专项](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/practice/rag/README.md) → [本仓 Tool Gateway](../labs/synthetic-tool-gateway/README.md) → [离线教学 RAG + Context Lab](labs/README.md) → [Ragas 评测](RAGAS-EVALUATION.md) → [G0–G8](../production/PRODUCTION-READINESS.md)。

**状态**：目前文档为学习体系；离线 Lab 无真实 Embedding/LLM/ES/Milvus。没有用户本人跑出的真实 RAG 模型实验/业务数据时标 **NOT RUN**。
