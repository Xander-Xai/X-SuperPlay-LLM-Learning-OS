# CORE｜Agent Loop 与 Loop Engineering 的机制、时序、边界

## 1. 五种 Loop 不要混淆

| 名称 | 由谁控制循环 | 成功判据 | 例子 |
|---|---|---|---|
| Agent Loop | Runtime 根据模型工具调用/终止输出 | 本轮任务完成、拒答或超限 | 查询订单后再检索 |
| Evaluator–Optimizer | 预设工作流/评审器 | 达到生成质量要求 | 写报告→评估→修改 |
| Loop Engineering 外层任务循环 | Trigger/Orchestrator/Verifier Policy | **独立环境验收**与预算规则 | Issue→Agent 修复→CI→反馈重跑 |
| 业务运营闭环 | 业务 KPI 与流程 | 工单 SLA、客户确认等 | 工单处理→跟进 |
| 训练优化循环 | Optimizer/Trainer | Loss/Reward 等训练指标 | SFT、GRPO；与 Agent 运行不是一回事 |

### Agent Loop 最小完整时序

1. Host 收到受信用户身份、目标、可用工具与预算。
2. Runtime 构造 messages、tool schemas、context；调用 LLM。
3. 模型返回 Final 或一个/多个 ToolCall（名称、参数、Tool Call ID）。
4. **宿主**校验 JSON/Schema、业务权限/租户、审批与幂等约束，真正执行工具。
5. 将每个结果与准确 Tool Call ID 关联回填，记录状态与 Trace；错误要分桶。
6. 检查步数/工具数/时间/Token/费用上限；未完成则返回步骤 2，终态则停止。

~~~mermaid
sequenceDiagram
 participant User
 participant Host as Agent Runtime
 participant Model as LLM
 participant Tool as Tool Gateway
 User->>Host: Task + Trusted Identity
 loop Within limits
   Host->>Model: Messages and Tool Schemas
   Model-->>Host: Final or ToolCall(id,name,args)
   alt ToolCall
     Host->>Tool: Validate and Execute under ACL
     Tool-->>Host: ToolResult(id, status, data)
   end
   Host->>Host: Append Observation / Trace / State
 end
 Host-->>User: Completed / Failed / Rejected / Escalated
~~~

**细节**：Function Calling 不是 GPU 自动运行 Python；工具返回属于低信任内容；Chat Completions 的 tool_call_id 与 Responses 的 function_call_output 协议不可随意混用。模型的 Final 文本不保证外部业务已成功。

### Agent 的最终输出为什么还不够？

Coding Agent 输出「修好了」，但代码不一定能通过测试；客服 Agent 输出「退款成功」，业务 DB 不一定已经退款。**独立 Verifier** 要拿环境事实，而不是以模型自评替代验收。

## 2. Loop Engineering 设计的是完整任务生命周期

任务的基本链：

**Trigger → Intake/Handoff → Policy/Budget → Agent Run → Independent Verify → Persist Feedback → Retry/Stop/Escalate**。

| 组件 | 输入与输出 | 工程难点 | 典型负例 |
|---|---|---|---|
| Trigger | Webhook/cron/manual→稳定 task_id | 事件去重、调度可靠性 | GitHub webhook 至少一次投递 |
| Task Contract | 受信目标、scope、验收项、身份与资源限额 | 验收标准先冻结 | Agent 自己修改测试让它通过 |
| Runner / Harness | Agent run_id、工具、上下文、沙箱 | 权限、工具执行、超时/计费 | 不受限工具一直循环 |
| Independent Verifier | 固定的 CI/业务 DB/文件内容/ACL oracle→pass + failed_checks | 不以自评为准；测试强度充分 | Final 说成功但环境失败 |
| Persistence | task_id、attempt、状态、反馈摘要、artifact/hash、verifier_revision | 重放一致性与并发 | 进程重启重新退款 |
| Policy / Scheduler | budget、progress、retry rules、状态机 | 有界重试与升级人工 | 相同错误无限重试 |

这些是课程抽象，并非 Loop Engineering 已存在行业强制标准。

**Task State（任务状态）**归属外层 Orchestrator，不等同于单个 Agent 的 Messages/Thread State，也不应替代真实业务数据库。

## 3. 一个严谨的任务状态机

~~~text
NEW -> RUNNING -> VERIFYING
  |        |         |
  |        |         +-- passed --> VERIFIED_SUCCESS [terminal]
  |        |         +-- failed + progress + budget --> RETRY_READY -> RUNNING
  |        |         +-- same failures repeated --> STAGNATED [terminal]
  |        +-- unsafe / unknown side effect --> ESCALATED [terminal]
  +-- invalid contract --> BLOCKED [terminal]

Any nonterminal --> BUDGET_EXHAUSTED / CANCELLED / FAILED
~~~

- **VERIFIED_SUCCESS**：环境 Oracle 通过；Agent Final 不能单独决定。
- **RETRY_READY**：失败可修复、风险可控、没有消耗完预算；反馈必须给出失败事实。
- **STAGNATED**：多次独立校验结果/证据完全相同且达阈值，说明无进展；可升级人工。
- **ESCALATED**：副作用结果未知、审批不足、判断需人为介入，不进行危险自动重试。
- **BUDGET_EXHAUSTED**：最大 attempts、单次 Run Budget、工具数/成本/总运行时间受限。
- **BLOCKED / CANCELLED / FAILED**：拒绝非法输入，可信取消，不可恢复错误分别处理。

**重试层级不同**：Tool Retry 在单个调用层；Agent Run Retry 重新启动一次内层执行；Task/Trigger Retry 可能源自队列重复投递，必须复用先前 task_id/State。对于任何具有副作用的工具，先查询实际状态/幂等回执，再判断是否能重试。

## 4. 状态持久化：不要将 7 个 ID 当成同一个

| ID | 角色 |
|---|---|
| task_id / trigger_dedupe_key | 长生命周期任务唯一性和重复触发去重 |
| attempt_id / run_id | 第几次 Agent 执行 |
| thread_id | LangGraph Thread/Checkpoint 恢复 |
| trace_id | 跨 API/工具/Verifier 的观测关联 |
| action_id / idempotency_key | **某次业务副作用**的请求唯一性 |
| verifier_revision | 验收条件的版本/冻结测试数据 hash |
| artifact_id / content_hash | 生成产物版本，区分“看似重复的输出” |

**最容易错的地方**：Checkpoint 保障图状态可恢复，不保证外部写入 exactly-once。业务 DB/消息系统需唯一约束、事务、CAS/Lease、状态查询和必要的补偿策略。

## 5. 独立验证如何设计？

评估强度由低到高：

1. 同一个模型自我评价（容易自我确认，不能独立证明完成）。
2. 第二个 Agent/LLM 查看 Trace、证据并给出理由（可辅助，但仍会错）。
3. **可信验证器**（单元/集成测试、无权修改的验收集、业务 DB 终态、文件哈希、权限策略、外部回执）。优先将机器可检的成功条件前置。

Verifier 应至少返回：pass/fail、failed_check IDs、evidence、verifier_revision。生成器不得自行更改 Verifier 或执行权限。CI 全绿仍可能漏测需求，关键业务还需要人工业务验收。

## 6. 和其他技术的准确关系

| 工程实践 | 关注的对象 |
|---|---|
| Prompt Engineering | 一次模型指令怎么表达 |
| Context Engineering | 每轮模型看到什么、压缩什么 |
| Harness Engineering | 模型循环/工具/权限/沙箱/状态/追踪的执行底座 |
| LangGraph | 通过节点、边、状态、Interrupt/Checkpoint 显式编排 |
| **Loop Engineering** | 触发多个 Agent Runs、机器验证、反馈、持久状态、停止与人工升级 |

它们可以在一个系统里融合；外层循环未必使用 LLM，未必需要 LangGraph，单 Agent + 固定 CI 流水线也可能是足够的实现。

## 7. 面试中的完整故障解析：退款接口超时

- Agent 提议 refund_order，服务端 ACL/审批成功，真实业务接口写入成功但网络回执丢失。
- 内层工具看到 timeout **不等于**退款没发生。
- 外层 Verifier 必须核对业务账本/带唯一键的回执。若无法确认，任务应 ESCALATED，不得机械 retry 整个退款 Agent。
- 记录 tool action_id、tenant、订单、业务唯一键、attempt_id/trace_id 和确认状态。Thread Snapshot 与业务 DB 事实分离。
- 用户只看到「处理中/需要人工核对」，不能看到虚假的「退款成功」。

## 8. 指标与公平对照

至少：Verified Task Success（分母：全部应完成任务）、Correct Abstention（分母：应拒绝场景）、Attempts per Task、Time/Cost per Verified Task、Stagnation Rate、Escalation Rate、Safety Violation、P95 End-to-End。失败尝试必须计入成本/耗时；单次模型完成率不等于 Verified Task Success。

比较三组：A 人工逐次 Prompt；B 一轮 Agent；C 有限 Outer Loop + 独立 Verifier。冻结任务、模型、工具/权限、环境和预算；不能仅选最好的一次结果作为证明。

相关：[原 Mini Agent](../../labs/MINI-AGENT-LOOP.md) · [Agent 深学](../README.md) · [Harness](../../AGENT-HARNESS-ENGINEERING.md)。
