# RAG 实验任务与验收协议

[目录](README.md) / [离线微实验](lab/README.md) / [学习者等级](../../assessments/CAPABILITY-RUBRIC.md) / [既有 Ragas](../RAGAS-EVALUATION.md)。

## 0. 先跑不需要 GPU/Key 的最小对照

~~~bash
python LLM-Training/application-engineering/rag-deep-dive/lab/retrieval_eval.py
python -m unittest discover -s LLM-Training/application-engineering/rag-deep-dive/lab -p 'test_*.py' -v
~~~

这个微实验自包含，演示 BM25（预分词合成语料）、给定排名模拟的第二路召回、RRF、ACL、Recall/Hit/MRR/nDCG、无证据/无权限拒答分母。不含真实 Embedding/ANN/Tokenizer/LLM，不可将结果写成 BGE/ES/Milvus/Ragas 实测。

## 已有的 120 题可运行样本（合成，不是业务真值）

[goldset 入口](goldset/README.md) 已提交 80 份虚构资料与 120 条模板生成的分桶标注（105 正例/15 拒答）。可以用下列命令对照 BM25、预定义 Rewrite 和两条词法排名 RRF，但不涉及真正的 OCR/Embedding/LLM：

~~~bash
python LLM-Training/application-engineering/rag-deep-dive/goldset/evaluate.py --mode bm25 --k 5
python LLM-Training/application-engineering/rag-deep-dive/goldset/evaluate.py --mode rewrite_bm25 --k 5
python LLM-Training/application-engineering/rag-deep-dive/goldset/evaluate.py --mode multiquery_rrf --k 5
python LLM-Training/application-engineering/rag-deep-dive/lab/real_embedding_eval.py
~~~

最后一条是无联网 Dry Run；真正使用本地已下载 SentenceTransformer 路径需手工选择 --model-path 并自行安装适配的 sentence-transformers，CI 不下载模型。输出正例检索指标，不会伪装成 Ragas 或答案正确率。

## 1. 真正进阶实验（规划，NOT RUN）

| 编号 | 独立变量 | 固定控制项 | 结果指标 | 最少负例 |
|---|---|---|---|---|
| E1 Parsing/Chunk | 固定512 vs 结构化 vs Parent–Child | 文档、问题、生成模型、来源金标 | Recall@5/10、引用定位、Token、OCR/表格准确 | 跨段否定、表格错列 |
| E2 Embedding | BGE-base-zh-v1.5 vs BGE-M3（向量维度各自新索引） | Chunk、Query、ACL、候选数 | Recall@K、MRR、index size、延迟 | 精确代码、术语同义 |
| E3 Retrieval | BM25 / Dense / Hybrid+RRF / +CrossEncoder | E2 最优配置、金标、统一 Token 预算 | Recall、nDCG、P95、成本 | 一路漏召回、重复段 |
| E4 Rewrite/Grounding | 原始 vs Rewrite/MultiQuery；无/有 evidence gate | 检索底座与模型固定 | 正确率、引用支持、误拒/误答 | 多轮指代错、旧法规、恶意指令 |
| E5 Production | ACL撤权/索引切换/缓存/并发参数 | 完全同一授权用例集与监控 | 越权率、P95、QPS、版本错误、成本 | 跨租户、缓存撤权、回滚 |

**实验报告至少包括**：目的、数据许可与脱敏、baseline、预注册假设、唯一改变变量、代码/数据 SHA、模型/索引版本、原始 Query/Gold、K/score 定义、重复试验次数、错误样例、结果是否可推广、NOT RUN/PASS/FAIL/INCONCLUSIVE。

## 2. 120 条 Gold Set 分类（合成模板已落盘，真实业务标注仍待执行）

| 类型 | 条数 | 需要单独衡量 |
|---|---:|---|
| 单文档事实 | 25 | 正例答案/span Recall |
| 精确编码/数值 | 20 | 严格准确、单位和版本 |
| 同义词改写 | 20 | 语义检索对词项匹配 |
| 跨文档多跳 | 15 | 是否覆盖全部必要证据 |
| OCR/表格 | 15 | 解析与答案两阶段错误 |
| 多轮追问 | 10 | Rewrite 不改变原意 |
| 无答案 | 10 | 正确拒答与误答 |
| 权限/隔离 | 5 | 未授权泄漏为零 |

本仓合成数据实际满足以上数量，但数据由模板生成，非人工审核、非真实表格 OCR，也不是真正的独立测试集。真实项目需要重新采集 50–100 份授权或公开文档并人工核对，不得把合成指标作为业务性能。

每条最少字段：case_id、query、query_type、source_family、gold_source_spans、answer_reference、expected_abstain、tenant、role、valid_on、annotation_review。禁止使用个人/客户敏感信息，固定 Gold 版本；重复问法按 source_family 聚类划分，防止泄漏。同一问题可以有多个相关证据；Gold 为空时不计算 Recall，而统计 Abstain。

## 3. 指标口径，防止“系统好看但业务没用”

~~~text
Recall@K = |topK ∩ relevant_gold| / |relevant_gold|（仅 gold 非空）
Hit@K = 1[TopK 至少一个相关结果]（仅 gold 非空）
MRR@K = 1 / 第一个相关结果排名（没有则0）
DCG@K = Σ ((2^relevance_i - 1) / log2(i+1))
nDCG@K = DCG@K / IDCG@K（按 gold 相关性等级）
Abstain accuracy = 正确拒答的负例数 / 应拒答负例数
ACL leak count = 返回的未授权文档数（必须为0）
~~~

注意：Recall@K 按标注单元（文档或片段）与去重规则严格对齐；nDCG 可以是二值或分级相关性，需写清。Faithfulness 是回答被给定上下文支持的比例，不等于真实法律正确或 Answer Correctness。NLI/Ragas Judge 一定要有人审校集。各类请求 P95 与 QPS 要报负载、模型实例、缓存和输入输出长度。

## 4. 真实模型实验替换路线

1. 将本仓合成文档换成公开许可或脱敏真实文档；保存 content_hash、源 ID、许可证、版本和撤销机制。
2. 用真正中文分词或 ES Analyzer 替换预分词 BM25 的 token 生成，并与 ES 的词法检索结果对照。
3. 使用实际 BGE embedding + Milvus/FAISS（固定模型 revision、索引参数），以 FLAT 精确向量搜索对照 ANN Recall。
4. 把静态第二路排名替换真实 Dense 检索结果；将合成案例扩展成上述 Gold Set，分桶跑 E1–E5。
5. 将 LLM 的输出与引用通过正式 Ragas/人工标注评估，保留评委及模型版本；不能写 API Key 到本仓。
6. 最后执行 ACL/更新/性能/成本压测与 [生产门禁](../../production/PRODUCTION-READINESS.md)；无证据不宣称通过。

## 5. 停止/验收

- L1：闭卷说清 BM25、RRF、Recall/Hit/MRR/nDCG 的公式与两个陷阱。
- L2：能独立改一个 Gold Case、恢复一项失败单测，并在真实受许可数据上跑自己的可复现检索。
- L3：单变量实验至少一个改善和一个退化，能指出因果限制、展示错误日志。
- L4：新领域盲测，从失败追踪到修复，不借助预设答案；如要求上线则另验 G0–G8。
- 没有真实运行证据时维持 NOT RUN；CI 通过仅说明**离线课程程序**通过。
