# Agent 与 Harness Engineering｜模型之外的执行和控制系统

**专业定义**：Agent 是围绕任务不断选择动作/工具/观察的策略与工作流；Harness 是支撑 Agent 可靠运行的**执行循环、工具适配、状态持久化、隔离、权限、容错、可观测、测试与恢复机制**。大白话：模型是提出方案的员工，Harness 是有门禁、工具、流水线、记录和质检的工作环境。

## 1. Harness 不等于“装几个 MCP/Skill”

~~~mermaid
flowchart TD
  A["Task / Goal / Approval Policy"] --> P["Planner / Tool Router / Model"]
  P --> G["Runtime: Step Limit / Timeouts / State"]
  G --> V["Tool Schema + Caller ACL + Idempotency / HITL"]
  V --> S{"Allowed?"}
  S -->|"No"| X["Deny + Audit / Ask Approval"]
  S -->|"Yes"| T["Tool Execution in Controlled Environment"]
  T --> E["Observation + Trace + Checkpoint"]
  E --> P
  P --> O["Final / Escalate / Refuse"]
  E --> Q["Trace Grader / Replay / Regression"]
  O --> Q
~~~

MCP 是 Host/Client/Server 的连接协议；Skill 是可按需加载的任务指令/资源组织，能充当 Harness 的一部分；Function Calling 是**模型表达工具调用意图**；**真正权限在服务端执行**。多 Agent 不是 Harness 的同义词，单 Agent + 持久状态/验证器/工具网关也可以形成 Harness。

## 2. 八项运行能力与测试

| 项目 | 专业机制 | 白话解释 | 验收负例 |
|---|---|---|---|
| Task Loop/Stop | 每步记录 Action/Observation/状态，并设时间/步数/Token 成本上限 | 员工不能一直申请做事不交作业 | 重复相同工具调用导致循环终止 |
| Tool Contracts | JSON Schema、类型/范围/必填、Tool allowlist、输出契约 | 表单不能填错字段 | 未知工具、类型错误、工具输出非法 |
| Authorization/HITL | 用户/租户/资源 ACL，副作用操作审批 | 无钥匙不能开仓库，付款要签字 | 低权限访问、未审批变更、撤销后重放 |
| Idempotency/Retry | 为每次副作用操作赋幂等 Key，安全重试和回放 | 网络重复下单不能扣两次 | 同 Key 不重复执行，不同 Payload 同 Key 必须拒绝 |
| State/Checkpoint | 持久化未完成步骤与事件日志；可回放/补偿 | 下次上班记得做到哪里 | 断开恢复后不重放已完成副作用 |
| Context/Memory | 选择本轮有效上下文，压缩与记忆过期/权限 | 只把需要的文件放上桌 | 隔离其他用户的历史、恶意文档不升级权限 |
| Observability/Tracing | Trace ID、step/tool/status/耗时/错误分桶、去敏 | 每次操作有可查的工单 | 失败不能被“只留成功”过滤 |
| Evals/Release Gates | Trace grading、任务级 Success、成本与安全指标 | 不只看“做了动作”，要看结果正确 | 工具调用成功但任务失败、错误引用 |

**失败归因**：模型提出错误动作 ≠ 工具执行 Bug ≠ 业务权限问题；要能用 Trace 区分。Tool 需要可验证返回，避免模型在失败时“假装成功”。Replay 有时会重新执行副作用；需设计幂等、检查点、补偿而不是盲目重试。工具权限不能由提示词本身保证。

## 3. “Harness”有两个常见用法

- **Agent Runtime Harness**：把模型变成能安全执行多步任务的系统，强调执行/状态/工具/恢复。参考 [Google Cloud 定义](https://cloud.google.com/discover/agent-harness)、[OpenAI Agents SDK Tracing](https://openai.github.io/openai-agents-python/tracing/) 与 [Testing](https://openai.github.io/openai-agents-python/testing/)。
- **Agent-first Software Engineering Harness**：让编码 Agent 有可读的 repo 文档、测试、CI、环境、任务拆分与审查反馈，如 [OpenAI Harness Engineering 实践](https://openai.com/index/harness-engineering/)；强调结构化环境比盲目加长系统指令更重要。
- **EleutherAI lm-evaluation-harness**：专门评测语言模型基准的工具，**不是**通用 Agent Runtime。见 [LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness)。

## 4. 实作路径

1. 先读 [上游 Harness 专项](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/HARNESS-ENGINEERING-LEARNING-20261029.md) 和 [上游沙箱](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/labs/harness-verification-sandbox-20261029/README.md)；
2. 在 [本仓离线纵切](labs/README.md) 运行 Tool Allowlist/ACL、步数、幂等和失败 Trace，并写一条不会误伤正常请求的负例；
3. 需要 Graph 的多轮事务时再进入 [LangGraph 官方学习](https://docs.langchain.com/oss/python/langgraph/overview)；在真实框架版本上检查持久化与 side effects；
4. 最后对相同任务固定 Prompt/模型/权限，比较有无 Checkpoint、重试、裁剪/恢复的 Task Success、成本和故障率；按 [生产 G0–G8](../production/PRODUCTION-READINESS.md) 发布。

**当前代码证据**：本仓离线 Harness Lab **无 LLM API、无真实队列/网络、无数据库事务、无操作系统 Sandbox**；通过其 CI 不能声称已具备企业级安全或生产能力。
