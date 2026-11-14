# RAG 专项课程交付与验收边界（2026-11-14）

状态：**CURRICULUM_READY / OFFLINE_LAB_CODE_ADDED / REAL_RAG_NOT_RUN / LEARNER_UNASSESSED**。

## 范围验收清单

- [x] 十大 R01–R10 技术主题有专业机制、白话边界/失败示例、学习产物与最小来源。
- [x] 参考六周路径，但不改变本仓需求驱动原则、M01–M12 或应用层 10 条 Track。
- [x] 论文、权威教科书、官方实现/官方模型卡可导航；动态链接按来源账本分级和版本复核。
- [x] 五组受控实验 E1–E5、120 道金标问题**设计规范**与正负样本独立分母。
- [x] 标准库 micro-lab 代码和对照测试被提交；真实 ES/Milvus、BGE、Ragas Judge 未由此证明。
- [x] 12 道面试问题附追问、证据模板，链接已有能力与生产门禁。

## 运行验收（以实际 CI 记录为准，不能自行勾“已经通过”）

- [ ] 在提交对应 Git SHA 上运行 Python 3.11 stdlib 单元测试。
- [ ] 运行本仓 check_repo 与现有应用层索引/实验验证器。
- [ ] 主分支合并后检查目标文件和相对链接、CI 状态。
- [ ] 将 E1–E5 用真实授权数据/固定模型分别实跑，记录原始日志和环境。
- [ ] 由学习者闭卷完成 L1–L4 题目；若实际要上线，再验证 G0–G8。

## 明确未验证的事项

真实中文分词、OCR、向量索引、ANN、BGE/CLIP/CrossEncoder、LLM 生成、正式 Ragas Judge、跨租户生产安全、长期数据更新、用户本人学习成绩、任何项目线上效益。教学合成结果不外推成这些项目的准确率或 P95。

## 回归路径

~~~bash
python LLM-Training/application-engineering/rag-deep-dive/lab/retrieval_eval.py
python -m unittest discover -s LLM-Training/application-engineering/rag-deep-dive/lab -p 'test_*.py' -v
python LLM-Training/tools/check_repo.py
python LLM-Training/application-engineering/tools/validate_application_engineering.py
~~~
