# Agent 三段项目、失败注入与任务级评测

> 下面是**实验设计，不是已全部实现的生产系统**。已有离线代码使用合成数据，真实 LLM、LangGraph、网络、事务必须在独立授权环境运行，并保存真实日志。个人技能按 [统一 L0–L4](../assessments/CAPABILITY-RUBRIC.md) 评分；真实上线使用 [G0–G8](../production/PRODUCTION-READINESS.md)。

## A｜Mini Agent：从零写执行循环（Week 1–2）

- 输入：合成身份/租户/订单、Scripted Model 的 Tool Call、审批和步数预算。
- 输出：Completed/ToolError/StepLimit/InvalidModel + Trace + 最终订单状态。
- 机制：ScriptedModel → Loop → Tool Gateway → in-memory Orders，无真实 LLM、网络和数据库。
- 对照：固定的订单查询 Workflow（无动态决策）与可调用工具的 Loop；比较执行步数、错误状态。
- 必测：未知 Tool、字段错误、跨 Tenant、未经审批的退款、重复幂等键、同键不同 Payload、无限循环。
- 入口：[可运行 Mini Loop](labs/MINI-AGENT-LOOP.md)；完成后尝试独立更换可支付 API 的真实 Model Adapter，锁版本、控制成本、保留工具 Trace。

## B｜客服工作流：LangGraph 复盘（Week 3–6）

**三条最小链路**：订单查询、知识问答、退款人工审批。不为学习堆砌 Agent 数量。先把一条事务做到能恢复、审计和评测。

| 阶段 | 机制 | 负例/故障注入 |
|---|---|---|
| API | 可信 Actor/Tenant/Role、限流、请求预算 | 伪造 admin 字段不得提权 |
| Router | 固定 Workflow 与 LLM Router 做对照 | 路由错不能造成越权 |
| Evidence | RAG 证据/ACL/时效与拒答 | 未授权资料、无有效证据 |
| Interrupt | HITL 审批绑定 actor/order/action | 审批撤销、重复恢复 |
| Mutation | 幂等作用域、参数指纹、业务状态校验 | 相同 Key 不同 Payload、超时后重复 |
| Durable | Checkpoint、Worker、业务 DB 独立设计 | 写入成功但回执丢失 |
| Delivery | SSE、可重查 Run Status | 断线时误报成功 |
| Evals | Trace + 最终响应 + DB 状态核对 | 回复成功但 DB 没改 |

**控制变量**：相同冻结任务/模型/权限/工具/预算，对比 ①固定 Workflow ②单 Agent ③Router/多 Agent。预先写判断阈值，不因 Agent 数量增加就默认质量提升。

## C｜长任务 Coding/Research Harness（Week 7–8）

定义一个需要多阶段搜索/文件修改的教学任务；需任务进度、上下文管理、允许的工具沙箱、失败恢复、终态验证。冻结输入连续执行三次，记录全部 Trace、成本、失败，不挑最好的一次。必测外部页面 Prompt Injection、越界文件读写、上下文溢出、取消/重启和重复副作用。

## 固定数据集格式

每条案例至少记录：

~~~json
{
  "case_id": "refund-replay-001",
  "scope": "SYNTHETIC",
  "task": "Refund a paid order after approval",
  "trusted_tenant": "A",
  "trusted_actor": "operator-1",
  "initial_business_state": "paid",
  "approval_state": "approved",
  "expected_tools": ["refund_order"],
  "expected_final_business_state": "refunded",
  "expected_response_class": "completed",
  "threat_category": "duplicate_delivery"
}
~~~

| 指标 | 分母/定义 | 注意事项 |
|---|---|---|
| Task Success | 应实际完成的任务数 | 要核对业务终态而不只看文案 |
| Correct Abstention | 规则要求拒绝的案例 | 正确拒绝另算，不混入成功操作分母 |
| Tool Accuracy | 需要工具的已标注案例 | 名称、参数、顺序、权限一起检查 |
| Recovery Rate | 实际注入故障的案例 | 单纯声称可恢复不计分 |
| Safety Violation | 安全威胁测试集 | 即使任务成功，越权依然失败 |
| P95 / Cost | 定义采样窗口和请求数 | 包含失败/超时，不选择性排除 |

## 必测失败类别

- [ ] 模型连续给工具但不终止；未知 Tool；参数缺字段/类型不合法。
- [ ] 合法 Schema 的跨租户订单；错误 Actor/Role；审批伪造或撤销。
- [ ] 同键同 Payload 重放；同键不同 Payload 冲突；工具响应丢失后重放。
- [ ] Worker 在执行前/写入后/回执前崩溃；Checkpoint 恢复重进节点。
- [ ] Retriever 引用未授权文档；Prompt Injection；工具结果夹带恶意指令。
- [ ] Handoff 循环/上下文泄漏；并行状态冲突。
- [ ] SSE 断线/取消；Final 说成功但 DB 显示失败。

## 统一实验记录模板

~~~text
Task ID / Status: NOT_RUN | RUNNING | PASS | FAIL | INCONCLUSIVE
Scope: SYNTHETIC | AUTHORIZED_REAL / Examiner
Question / Fixed baseline / Controlled variable
Code SHA / Model revision / SDK versions / Data hash / Exact command
Raw output and sanitized Trace / Final business state
Main metrics: numerator, denominator, cost, latency
Negative cases and failures / Assumptions and limitations
Level requested L0–L4 / Evidence links / Stop or next gap
If production: G0–G8 outcome
~~~

现有 [19 条合成评测](labs/README.md) 和 [Agent Mini Lab](labs/MINI-AGENT-LOOP.md) 只证明局部确定性契约，不代表真模型 Faithfulness、业务安全、恢复可靠性或 SLA。
