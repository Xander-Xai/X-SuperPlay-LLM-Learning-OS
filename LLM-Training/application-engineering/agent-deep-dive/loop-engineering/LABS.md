# Agent Loop / Loop Engineering 六组学习实验 SOP

> A/B 为仓库可复现的 Python 标准库 Toy；C–F 为真实系统的**实验设计**，并不声称已运行 LangGraph、Redis/Celery、PostgreSQL、MCP 或 CI 外部服务。每个实验至少存：Task ID、输入、版本、命令、输出、负例、状态、证据与无法证明的范围。

## Lab A（P0）：一次 Agent 内部 Tool Calling

从仓库根目录运行：

~~~bash
python LLM-Training/application-engineering/labs/mini_agent_loop.py
python -m unittest discover -s LLM-Training/application-engineering/labs -p 'test_mini_agent_loop.py' -v
~~~

记录模型决策、Tool Gateway 校验、Tool Result 回填、最终结果和 Step Limit；负例：未知工具、跨租户 order_id、写操作未审批。验收：解释「模型决定下一步 ≠ 宿主允许写入」。

## Lab B（P0）：两层 Loop 与独立验收

~~~bash
python LLM-Training/application-engineering/agent-deep-dive/loop-engineering/labs/outer_loop.py
python -m unittest discover -s LLM-Training/application-engineering/agent-deep-dive/loop-engineering/labs -p 'test_outer_loop.py' -v
~~~

一个合成 Issue 在 attempt 1 输出 tests-fail 但 Agent 自述成功 → Verifier 不通过；attempt 2 输出 tests-pass → VERIFIED_SUCCESS。必须能列出 Trigger、Task Contract、Run、Verifier、State、Retry/Stop 六个对象。

**负例**：重复事件且改变目标、重复同一失败产物→STAGNATED、用尽 attempts/units、未知副作用→ESCALATED、进程重启状态为 RUNNING 的保守处理。

## Lab C（P0）：真实 GitHub Issue → CI 验收（独立授权测试仓）

实验条件：创建只含合成代码和单元测试的受控测试仓；不要在敏感仓库开启自动写入或部署。

1. 固定 Issue ID、分支/提交哈希、允许文件路径和 frozen acceptance tests。
2. Webhook 仅以验证后的身份/签名接入；同一事件重复送达必须重用 Task ID。
3. 启动 Agent Run，在沙箱修改允许的代码，不可让 Agent 编辑 verifier/CI 脚本。
4. Agent Final 后检查实际 Git Diff、pytest/CI、权限扫描，不以 Final 为准。
5. 失败仅返回可修复测试摘要，按预算进行最多 N 次受控迭代。
6. 只有机器验收通过且完成必要人工 Review 才可合并；超限自动 Stop/Escalate。

**测量**：Verified Fix Rate（分母：全部固定 Issue）、Attempts/Issue、CI 调用次数、成本、P95、stagnation、未授权变更次数。真实环境需留 Run URL、SHA 和 CI 日志。

## Lab D（P0）：退款的不可盲重试场景

1. 业务 Tool refund_order 写入成功，但网络回执丢失。
2. 外层收到 Timeout；**不得重启退款 Agent 自动重试支付/退款工具**。
3. 用受信幂等键和业务账本查询操作事实；状态仍未知时 ESCALATED/HITL。
4. 分开保存 Task State、LangGraph Thread Checkpoint、Business DB 账务状态。
5. 通过唯一约束和真实并发/重放测试证明没有重复副作用，不能靠假数据演示证明分布式 Exactly Once。

## Lab E（P1）：Verifier 正交性和失败分桶

冻结 20 条或以上合成/授权任务：成功、拒绝、模型自称成功但环境失败、工具权限拒绝、外部响应丢失、重复事件、预算耗尽、相同错误无进展。比较自评 LLM、第二评价器、独立 CI/DB Oracle 的不同能力。**报告**：任务成功/正确拒绝/环境状态、安全违规、成本、失败分桶的分子和分母，不把少量样本测得的 100% 当成真实安全保障。

## Lab F（P2）：长期运行与并发调度（独立部署）

增加 Cron/Webhook/Queue、Workers、DB 表、唯一事件 key、claim/lease、重试/死信、取消/优先级和重启恢复。注入重复事件、多 Worker 同时领取、进程崩溃、DB 写入前后故障。使用受信日志证明不会无界重跑且必要的高风险工具被阻止。**此 Lab 未在本仓实际部署**。

## 每个 Lab 的统一证据卡

~~~text
Lab / Status: NOT_RUN | PASS | FAIL | INCONCLUSIVE
Task / Trigger / Trusted Actor-Tenant / Scope
Goal / Frozen Acceptance & verifier_revision
Model/SDK/Runner/Tool Version / Data SHA / Code SHA
Run ID, Attempt ID, Trace ID / Exact command
Actual artifact/DB result / Verifier decision / Failed checks
Negative cases / Retry classification / Recovery method
max_attempts, wall-clock, token/cost budget (if real)
Task success numerator/denominator / latency & cost
Permissions/HITL / Escalation or Stop reason
L0–L4 examiner verdict / G0–G8 only for production
~~~
