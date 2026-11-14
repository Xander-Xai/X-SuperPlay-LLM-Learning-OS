# Ragas / Evals / Trace Grading｜RAG 与 Agent 的测试体系

**Ragas（框架）** != RAG（检索增强生成） != EleutherAI **lm-evaluation-harness（通用模型基准）** != Agent **Harness（运行环境）**。

**问题**：RAG 找到了文档，但回答是不是被证据支持？Agent 调用了工具，但整体目标有没有成功？**大白话**：图书管理员找书、写作者答题、工具操作员完成流程，是三场不同考试，不能合并一个“准确率”掩盖失败。

## 1. 官方 Ragas 指标：分类、测量目标与主要局限

| 官方指标/领域 | 测什么 | 依赖的标注/输入示例 | 防止误读 |
|---|---|---|---|
| Context Precision | 检索排在前面的上下文与问题/参考是否相关 | Query、Retrieved Contexts、相关性判据/Reference，依所选实现 | 高分不代表相关文档全找齐 |
| Context Recall | 回答所需证据有没有被覆盖 | Reference/Gold Context 与检索结果，按版本 | 高召回可能包含大量噪声 |
| Faithfulness | 生成回答的各 Claim 是否可由提供的 Context 推导 | Response、Retrieved Contexts，通常需要 Judge | 与给定 Context 一致 ≠ 当前真实世界正确 |
| Response Relevancy | 回答是否针对用户问题 | User Input、Response；可能用 LLM/Embeddings | 相关 ≠事实正确 |
| Noise Sensitivity | 引入无关或误导材料时输出质量是否退化 | 干扰文档与 Ground Truth | 不保证安全权限 |
| Tool Call Accuracy / F1 | Agent 选对工具/参数/顺序的程度 | 期望 Tool Call 与实际 Trace | JSON Validity 不代替任务完成 |
| Agent Goal Accuracy | 端到端目标是否达成 | 任务定义、结果或 Reference/Judge | 一次成功不代表稳定可靠 |

依据 [Ragas Metrics 最新目录](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) · [Faithfulness](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/) · [Tool Metrics](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/agents/)。**部分指标使用 LLM Judge，成本、重现性、评分偏差和版本都需要校准。**

## 本轮严格补验：冻结案例与可选真实 Ragas 接线

此前只有单条 recall_at_k 与少量函数负例，缺少逐案例报告及明确的拒答分母。现新增：

- [19 条固定用例](labs/benchmark_cases.json) · [离线评测程序](labs/evaluate_benchmark.py)：分别输出正例 Recall@k、无证据/无权限 Abstain、未授权文档违规、工具正确性与副作用，一次复跑可定位失败 ID 和类型；
- [Ragas Faithfulness 可选脚本](labs/ragas_live_optional.py)：参照当前官方 collections API，需要明确 --live、API Key 和实际可用模型，CI 仅执行无 Key Dry Run；
- [完整说明](labs/README.md)：独立检索分母、如何构建业务 Gold Set 与人工校准集、为何不能把代理指标当正式 Ragas。

专业公式：Recall@k = Top-k 中 Gold 证据个数 / 全部 Gold 证据个数。Gold 集为空的拒答案例**不计入**这个比率，而单独统计拒答正确率。该指标不等于 Ragas Context Recall/Precision 等可能依赖参考答案/LLM Judge 的指标。

**证据状态**：离线合成基准能够执行，但真实模型与正式 Ragas Judge 还未在用户环境执行；不可称正式 Ragas 评分已 PASS。

## 2. 最小 Eval 结构

~~~mermaid
flowchart LR
  Q["固定任务/真实授权或 SYNTHETIC"] --> B["版本化数据集: question/gold docs/expected tools"]
  B --> R["执行同一版本 RAG/Agent"]
  R --> T["保留原始 Retrieval/Tool/Output Trace"]
  T --> A["Deterministic Assertions：ACL、JSON、Doc ID、参数"]
  T --> J["Ragas LLM Judge：faithfulness/relevancy 等"]
  A --> G["独立 Task Success + 失败分桶"]
  J --> G
  G --> D["对照差异：质量/成本/P95/回归"]
~~~

运行 Ragas 应记录**精确版本与 API**；其 Quickstart、metrics/collections API 近年来有变化，直接复制早年 ragas.evaluate 导入方式可能失败。推荐先按 [Ragas 官方 Quickstart](https://docs.ragas.io/en/latest/getstarted/quickstart/) 生成可运行工程，再以自己的脱敏固定测试集替换示例。**不要在课程仓提交 API Key**。

## 3. 从没有 LLM 的最小实验到真正评测

- L0/L1：用本仓 [离线 Lab](labs/README.md) 计算真实可定义的 Recall@k/权限违规/Tool Accuracy/任务状态；这是**确定性代理指标**，不是 Ragas 的 Faithfulness。
- L2：在固定允许调用的模型环境，运行正式 Ragas metrics，保存数据集版本、评委模型/Prompt、输出和标注规则；使用固定人工标注集校准 Judge。
- L3：构造 3 类负例：检索文档缺关键证据、伪造引用/事实冲突、工具参数合法但业务失败。比较 Retrieval、Grounding、E2E，而不是单一 Score。
- L4：换一个新的任务/文档/权限模型，脱离教学样例自行诊断回归；如果真实上线，额外走 G0–G8。

## 4. 关键工程细节

- 将 **评测样本单位**固定为任务或文档族，重复请求/同源改写不能当独立测试样本；
- 置信区间按样本数、类别、聚类结构；评委分数不可当严格概率；
- 测试可能包含“应该拒绝”，不能把拒答样本从分母排除；
- Trace 存储可能包含敏感 Tool 参数/用户信息，必须脱敏并依数据留存政策；
- 生产指标需把质/安/钱/时分别报告：Task Success、Faithfulness、越权率、成本、TTFT/P95。

关联 [M10 评估](../modules/M10.md)、[Agent Harness](AGENT-HARNESS-ENGINEERING.md)、[已有 Task Eval Toy](../labs/task-evaluation/README.md)、[OpenAI Agent Trace Grading](https://developers.openai.com/api/docs/guides/trace-grading)。
