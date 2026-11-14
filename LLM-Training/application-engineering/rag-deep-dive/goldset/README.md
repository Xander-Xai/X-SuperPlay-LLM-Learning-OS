# 120 题可运行合成 Gold Set（课程验收，不是业务基准）

状态：**80 份虚构文本 + 120 个模板生成的标注问题**，不是人工评审的业务真值。示例产品、数字与用量都是虚构内容，不能用于配方、健康、法规或商业判断。全部问题的 split 都是 toy_dev，不能称为盲测/验证泛化。

从仓库根目录运行：

~~~bash
python LLM-Training/application-engineering/rag-deep-dive/goldset/evaluate.py
python LLM-Training/application-engineering/rag-deep-dive/goldset/evaluate.py --mode rewrite_bm25 --k 5
python LLM-Training/application-engineering/rag-deep-dive/goldset/evaluate.py --mode multiquery_rrf --k 5
python -m unittest discover -s LLM-Training/application-engineering/rag-deep-dive/goldset -p 'test_*.py' -v
~~~

| 桶 | 数量 | 当前模拟 | 后续真实考核 |
|---|---:|---|---|
| direct 单文档 | 25 | 含唯一来源的事实句 | 源 PDF 原始段落 |
| exact 编号 | 20 | 预分词 BM25 | 中文分词器 / ES |
| paraphrase 同义 | 20 | 改写语言但带代码 | 真实 Dense 的语义召回 |
| multi_hop 多证据 | 15 | 两个独立 Gold 文档 | 多源引用与生成准确率 |
| table_ocr_proxy | 15 | 文字表格 | 真 OCR / 行列解析 |
| multi_turn | 10 | 冻结的人工改写 | LLM Rewrite 与指代错误 |
| no_answer | 10 | 不存在的编码 | Evidence Gate / 拒答 |
| acl | 5 | 过期/跨租户隐藏文档 | 服务端 ACL 与缓存撤权 |
| **共计** | **120** | **105 正例 + 15 拒答样例** | **需要独立人工审校** |

模拟 gold_source_spans 包含 source_id、page 与原文 quote；校验程序会拒绝不存在的 Gold、引用不支持的 quote、权限不合法的金标、伪造人工审校标签与错误分母。离线代码会分开报告 Recall/Hit/MRR/nDCG 正例均值和应拒答样例的空检索代理，绝不以它们替代真实生成 Faithfulness。

**实践**：固定 goldset SHA，执行三种模式，记录每个桶的结果；选择至少 3 条失败案例（尤其 multi_turn 和 multi_hop），提出单变量改动及预期。然后按照 [真实模型本地入口](../lab/real_embedding_eval.py) 使用已经下载的模型比对，确保不将 Top-K 有结果误当证据充分。

继续：[RAG 实验协议](../LABS.md)、[24 步周计划](../WEEKLY-EXECUTION.md)、[Rubric](../../../assessments/CAPABILITY-RUBRIC.md)。
