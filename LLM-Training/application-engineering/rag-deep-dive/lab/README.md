# RAG Retrieval Offline Micro-Lab（标准库教学实验）

**SYNTHETIC ONLY：** 无 API Key、无网络、无第三方包、无 GPU；合成中文已经预分词。真实运行需 Python 3.11+。这不是 Elasticsearch/Milvus/BGE/LLM/正式 Ragas，也**不**验证 Prompt Injection 防护。

~~~bash
python LLM-Training/application-engineering/rag-deep-dive/lab/retrieval_eval.py
python -m unittest discover -s LLM-Training/application-engineering/rag-deep-dive/lab -p 'test_*.py' -v
~~~

## 可复核内容

- BM25 公式在一套确定性预分词样本上执行，含文档长度归一和正 IDF。
- 第二路 dense_stub 是 frozen ranking fixture：**不是**算出来的 Dense Embedding；用来单测 RRF 与评测接口。
- ACL/tenant/active 过滤在召回前执行；对外发出结果后还检查泄漏。
- 正例 Recall@3、Hit@3、MRR@3、二值 nDCG@3 与预期拒答案例各自有独立分母；Gold 为空不进入 Recall。
- 包括跨租户、角色、失效版本和含恶意指令文档的样例。只有检索/排序层，没有模型遵循文档指令的行为。
- 自动测试用负例证明：RRF 不同排序、授权过滤、生效状态、错误预测分母、返回非授权文档、Gold 缺失格式都会被检查。

## 教学边界与下一步

BM25 的输入是手工 term list，不是中文语言学分词或 ES analyzer；dense_stub 是人工名单，不能证明语义检索实际质量；空结果的拒答 proxy 不构成 Evidence Gate；文档标记的角色列表仅教学策略，不是真实后端安全实现。不同 baseline 结果仅适用于这些合成数据。

现实替换计划见 [实验手册](../LABS.md)；完成后一并记录模型/数据版本、正例与拒答分母、失败来源和算力成本。已经存在的 19 条跨 RAG/Agent 合成基准仍由 [原有评测](../../labs/README.md)维护，本实验不更名、不覆盖那些用例。
