# Agent 24 道闭卷题｜含判分要点与实践指向

> 面试题仅用于知识验收，不代表通过仓库 [L0–L4 Rubric](../assessments/CAPABILITY-RUBRIC.md)。每题须闭卷解释边界，L2+ 必须能独立提供代码或真实运行证据。对应 [学习主线](AGENT-LEARNING-PATH.md)。

| 编号 | 问题 | 回答要点 |
|---|---|---|
| 01 | Agent、Workflow、普通聊天应用如何区别？ | 固定路径 vs 模型动态决定步骤；优先简单架构 |
| 02 | Function Calling 是模型执行函数吗？ | 不是，模型提议，宿主校验/执行，结果回传 |
| 03 | Agent Loop 为什么必须有停止条件？ | 步数/时间/Token预算、超限/转人工 |
| 04 | JSON Schema 合法为什么仍可能不能调用工具？ | 业务语义、Actor/Tenant ACL 与审批独立校验 |
| 05 | 工具超时能否立刻重试退款？ | 超时不证明没成功，需查询状态或受保护幂等 |
| 06 | ReAct 与 Plan-and-Execute 有何区别？ | 交替行动观察 vs 显式任务分解，需按任务选 |
| 07 | State、Node、Edge、Reducer 如何配合？ | 图的共享状态、计算步骤、跳转、并行合并 |
| 08 | Checkpoint 是否就是长期记忆？ | Thread 执行快照 vs 跨线程 Store/Memory |
| 09 | Interrupt 恢复为何容易重复副作用？ | 重新执行边界与任务恢复，写操作需额外保护 |
| 10 | 何时用 Router，何时用 Supervisor？ | 相对确定的业务分派 vs 动态反复协调 |
| 11 | 多 Agent 有哪些常见系统失败？ | 交接循环、上下文污染、冲突、成本与路由误差 |
| 12 | Agentic RAG 与传统 RAG 有何不同？ | 模型动态选择检索步骤，不保证检索更好 |
| 13 | SSE 断开意味着后台任务停止了吗？ | 不一定，传输与 Durable Task 是两层 |
| 14 | 幂等键如何避免跨用户污染？ | 可信 tenant/actor/操作作用域+payload 指纹 |
| 15 | 写入成功但回执丢失如何恢复？ | 业务状态核对、外部幂等协议、必要补偿 |
| 16 | Tool Success 为何不能等于 Task Success？ | 选错工具/规划/业务终态仍可失败 |
| 17 | Trace、Metric、Log 各用于什么？ | 单次路径、聚合趋势、详细事件与错误 |
| 18 | 怎样公平比较单 Agent 与多 Agent？ | 同数据、模型、工具、权限和预算；报告失败与成本 |
| 19 | Prompt Injection 如何越过信任边界？ | 低可信外部内容冒充高优先级指令 |
| 20 | Prompt 可以代替后端鉴权吗？ | 不能，执行层必须有 ACL/HITL/沙箱 |
| 21 | 拒答是成功还是失败？ | Gold Policy 正确拒绝单列，不能混淆分母 |
| 22 | MCP、Skills、Function Call 各是什么？ | 接入协议、任务资源封装、模型动作提议 |
| 23 | A2A 与本地多 Agent Handoff 区别？ | 跨系统互操作协议 vs 单系统编排 |
| 24 | 如何证明 Agent 能投产？ | 真实任务/故障/安全/成本/监控/回滚+G0–G8 |

## 两道系统设计追问

**企业客服**：设计订单查询、RAG 知识问答、退款 HITL。说明 API 身份、LangGraph Checkpoint/业务 DB、SSE/Worker、幂等键、Trace 和 P95，并诊断「退款已执行但 HTTP 响应丢失」。

**长任务研究 Agent**：规划、外部网页低信任、工具沙箱、上下文压缩、Checkpoint、恢复和终态验证。如何防止网页中的指令获得读写用户其他文件的权限？

## 三种 Trace 口述

- 正常：用户 → LLM ToolCall → Gateway → ToolResult → Final。
- 失败：越权 ToolCall → Forbidden → 明确失败/转人工，不能直接显示成功。
- 恢复：外部副作用已发生 → 响应丢失 → 查询事实/幂等重入 → 不重复操作。

闭卷问题先尝试不查文档回答；不确定时复现 [Mini Loop](labs/MINI-AGENT-LOOP.md)，再看 [官方资料](AGENT-OFFICIAL-RESOURCES.md) 和 [项目评测](AGENT-PRACTICE-AND-EVAL.md)。
