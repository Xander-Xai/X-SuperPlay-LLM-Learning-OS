# 完整场景复盘｜Coding Agent 和多智能体客服的双层循环

## 场景 1：Coding Agent 自动修复 Issue（最推荐学习）

用户提出「修复项目中订单查询 Bug，提交可通过测试的 PR」。

**外层 Loop Engineering**：
1. GitHub Issue 事件触发，只接收受信事件/仓库/身份；使用 issue_id + repo + goal revision 去重。
2. 冻结验收：目标用例必须通过、原有测试不回退、不得改动受保护目录或测试用例本身、费用/attempt 数设限。
3. 分配任务至独立沙箱，启动一次 Agent Run，记录 task_id/attempt_id/code_sha。
4. 内层 Agent Loop 执行：查看错误日志 → 搜索代码 → 修改文件 → 调用测试工具 → 观察执行结果 → 输出修改说明/Final。
5. **外层独立 Verifier** 执行 CI/tests + Diff ACL + Frozen Gold Tests；失败则总结错误，返回下一轮输入，而不是让模型自己判成功。
6. 两次同样失败/目标无变化或预算耗尽，停止；无法解释的安全/权限问题转人工；通过后交给人工 Review 与合并。
7. 最终结果不是「PR 创建」，而是「符合冻结规则且人工批准的变更」。性能报告包含所有失败尝试。

**如何学习**：先跑 [Outer Loop 离线实验](labs/README.md)，再在独立测试仓用真实 CI 替换 exact-text Verifier。保持同一冻结任务比较三种架构：手动 Prompt、单 Agent Run、有独立 Verifier 的外层 Loop。

## 场景 2：客服退货退款（你的工程面试高价值场景）

**一次客户请求的内层 Agent Loop**：
- API 获取受信 tenant/actor/session，Router 识别退款意图；
- 查询订单/知识，Agent 提议工具调用，Tool Gateway 对 ACL/Schema/审批检查；
- LangGraph 的 State + Checkpointer 记录可恢复图执行；审批 Interrupt 等待可信审批；
- Worker/业务 DB 执行真实退款并记录幂等键与 Trace。

**整个业务任务的外层 Loop**：
- Task ID 将原始申请、多个 Agent Runs、审批和最终业务验证关联。
- Verifier 不是看回答「退款成功」，而是查业务账本/受信回执，确认退款正确完成或应拒绝。
- 如 HTTP 超时：不确定是否已退款，不得盲重试；先用 action_id/idempotency_key 查状态，仍未知则升级人工。
- 如证据不足/用户未授权：正确拒绝或请用户补材料，比循环请求模型更合适。
- SLA/时间/费用/attempt 超限必须有终态，避免工单无期限挂起。

### 这一场景涉及的五个状态概念

| 状态 | 典型例子 | 不要混淆 |
|---|---|---|
| Task State | 工单 102 等待批准、尝试 2/3 | 不等于某轮 LLM 消息 |
| LangGraph Thread State | 当前走到 approval_interrupt | 不等于业务 DB |
| Business State | 订单已退款金额/流水号 | 不等于模型说完成 |
| Queue/Worker State | 任务在队列、租约/心跳 | 不等于状态永久持久 |
| Verifier State | 哪些业务检查通过、版本号 | 不等于生成器自评 |

## 面试中的七个问题

1. Agent Loop 和外层 Loop Engineering 有什么区别？内层模型输出 Final 外层为何可能继续？
2. 退款请求网络超时后，为什么不能重试整次 Agent Run？
3. Task/Thread/Run/Trace/Action 五种 ID 该放在哪里？
4. 如何防止 Agent 修改自己的验收测试或规避测试？
5. Trigger/Webhook 被重复投递两次，为什么要做去重？
6. 验收连续相同失败两次，下一步该如何停止或升级人工？
7. 如果固定 Workflow 就能解决退款流程，还有必要上多个 Agent 和无限 Loop 吗？

## 30 秒面试口述范本

「Agent Loop 负责一次运行内部的动态模型/工具交互；Loop Engineering 管整项任务的触发、独立验证、状态、有限迭代与终止。系统只有在可信的业务状态或 CI 通过时才认定成功；执行超时、权限和副作用不确定时不会简单重试，而是核对幂等记录并升级人工。这样可以把会使用工具的 Agent 变成可控、可审计的任务执行系统。」

此口述是**架构建议**，不是任何具体项目已经通过线上验证的事实。需以实际代码和日志答辩。
