# 离线 Outer Loop 实验｜触发 → Agent Run → 独立验证 → 反馈 → 停机

> 这是对已有 [Mini Agent Loop](../../../labs/MINI-AGENT-LOOP.md) 的**外层补充**。Python 3.11 标准库；不调用真实 LLM、API、GitHub CI、工具写操作或付费服务。脚本里的 ScriptedRunner 代表「整次 Agent 执行」，不是语言模型；IndependentVerifier 比较合成 artifact 和可信冻结 target。

## 直接运行

在仓库根目录：

~~~bash
python LLM-Training/application-engineering/agent-deep-dive/loop-engineering/labs/outer_loop.py
python -m unittest discover -s LLM-Training/application-engineering/agent-deep-dive/loop-engineering/labs -p 'test_outer_loop.py' -v
~~~

预期 demo：第一次 Runner 自称完成但 artifact 内容是 tests-fail → Verifier 拒绝；第二次产出 tests-pass → VERIFIED_SUCCESS；attempts=2。它只证明标准库状态和验证合同正确，**不代表 GitHub CI 真的运行了**。

## 逐段理解源码

| 源码对象 | 执行职责 | 警惕的边界 |
|---|---|---|
| OuterLoop.submit | 把 Trigger ID、受信身份、冻结验收目标、attempt/units 预算登记为 Task | 相同 trigger 不允许换 target/actor 绕过验收 |
| OuterLoop.step | 标记 RUNNING，启动某一次 Agent Run，等待 Tool/模型运行汇总产物 | 这里的 Runner 是 ScriptedRunner，非真实模型 |
| IndependentVerifier.evaluate | 根据**环境产物**与 target 比对，忽略 Runner 的 claim_done | ExactText 只是最低强度 Toy Oracle |
| OuterLoop._unchanged_twice | 两次失败检查和 artifact hash 完全相同判为无进展 | 只是一种启发式，不等于真实语义无进展 |
| TaskStore | 将 Task/Attempt/Feedback 保存到 JSON，通过临时文件 + os.replace 写入 | 单进程教学：不支持多 Worker 乐观锁/租约/事务 |
| OuterLoop.run | 在 QUEUED / RETRY_READY 中反复执行，直到终态 | 对 RUNNING 的未知中断默认 ESCALATED，禁止盲重放副作用 |

## 六项必做负例

1. Agent claim_done=True 但返回错误 artifact：不得 VERIFIED_SUCCESS。
2. 同一个 trigger_id 变更 target 或 Tenant：返回 TRIGGER_CONTRACT_CONFLICT。
3. 三次产生相同失败 Artifact：第二次触发 STAGNATED（阈值是教学策略，非硬标准）。
4. max_attempts / max_units 用尽：BUDGET_EXHAUSTED，不能继续跑。
5. Runner 声称可能已写入外部系统但状态不确定：ESCALATED，不能无脑重试。
6. 模拟 RUNNING 后进程重启：未知副作用优先升级人工，不能直接重复业务写入。

## 如何迁移到真实 Agent？

1. 保留**外层 Task Contract、可信事件 ID 和独立 Verifier**，将 ScriptedRunner 改为真正的 Agent SDK/LangGraph Runner；内层消息与工具仍由其 Harness 管理。
2. 将 Toy exact-text Verifier 改为 CI/JUnit/pytest、业务 DB/真实回执/产物哈希。Verifier 权限不得授予生成器，冻结规则不可被 Agent 修改。
3. 把 JSON StateStore 换成真正持久事务数据库，设计唯一触发/任务键、Worker 领取/租约、乐观锁/CAS、Crash Recovery 及 Outbox 等，再做多进程故障注入。
4. 叠加真实 time/token/cost budget、权限、HITL、审计、任务取消和追踪；**不得拿 Toy used_units 当 Token 或美元费用**。
5. 冻结任务集比较「人每轮手动 Prompt」vs「一轮 Agent」vs「Outer Loop + Verifier」，同时报 Verified Success、attempts、成本、安全、P95、正确拒绝和升级人工。

真实客服退款项目的完整迁移说明见 [案例](../CASE-STUDY.md)。按 [L0–L4](../../../../assessments/CAPABILITY-RUBRIC.md) 验收，真实生产再过 [G0–G8](../../../../production/PRODUCTION-READINESS.md)。
