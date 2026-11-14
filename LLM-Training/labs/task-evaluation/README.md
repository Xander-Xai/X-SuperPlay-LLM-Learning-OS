# Agent/LLM 任务级评估 Lab｜正确分母、失败分类和置信限制

> **SYNTHETIC LABELS / NO MODEL / NOT A LATENCY BENCHMARK。** 此工具使用 16 条事先标注的虚构输出，不联网，也不调用 Qwen、RAG 或工具 API；它仅验证“如何定义可解释的任务级指标”。JSON 中的 `latency_ms` 是教学占位值，绝不能作为真实推理延迟宣传。

## 运行

```bash
python LLM-Training/labs/task-evaluation/evaluate.py
python -m unittest discover -s LLM-Training/labs/task-evaluation -p 'test_*.py' -v
```

## 关键知识与公式

同一 Agent 的结果要分别验证：
- `Tool Selection Accuracy`：所有任务中正确选择工具或拒答的比例，分母全部任务；
- `Schema Valid Rate`：全部输出的结构合法比例，不能只统计成功调用；
- `Argument Accuracy`：需要工具的任务中，工具类型、schema 和目标 ID 均正确的比例，分母包含预测错误；
- `Tool Execution Success`：需要工具任务中成功执行的比例；
- `Citation Support`：需要引用的任务中，外部标注判断来源支持的比例（本 Lab 只读取预标注结果，**不自行核验引用事实**）；
- `Refusal Accuracy`：要求拒答的任务中，真正拒绝且没有工具执行的比例；
- `E2E Success`：满足任务要求所有环节的比例，不能用单个 JSON valid 代替。

`Wilson 95% interval` 是对独立伯努利样本的统计近似；小样本、簇相关、标注误差会破坏解释，**16 条样本仅用来练算法和分母，不用于生产 SLO 保证**。

## 练习（适合边做边学）

1. 将 T09 的 `citation_supported` 从 false 改为 true，解释为什么只改善 Citation 和 E2E 而非 Tool Selection。
2. 将 T15 改为正确拒答，验证独立拒答率和任务成功率的变化；若工具已执行仍不应 PASS。
3. 删除一个失败样本与保留它分别计算：解释选择性排除如何虚高指标。
4. 为某个测试族新增 8 个真正不同的虚构任务，观察 Wilson 区间并说明不能把同模板改写当独立样本。
5. 迁移到真实项目时用**真实授权的脱敏审计数据**替换 fixture，明确定义标签负责人、held-out 划分、抽检、时间窗、工具调用权限与 P95 压测方法。真实数据/商业事实仍留项目仓。

参考：[M10 评估](../../modules/M10.md) · [生产门禁](../../production/PRODUCTION-READINESS.md) · [上游 RAG 评估实验](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/tree/main/docs/labs/llm-market-rag-eval-20261029) · [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)。学习结果记录在 [需求卡](../../demand-driven/DEMAND-CARD-TEMPLATE.md)。

