# 四周专项路线｜从 Agent Loop 到可验证的任务自动循环

> 每天参考 120–150 分钟：官方资料 25–30 / 机制图 20 / 编程 60–70 / 失败注入+复盘 20–30 分钟。以任务和证据为单位，不必等四周结束才可继续应用。优先级从 P0 到 P2。能力级别按 [仓库 L0–L4](../../../assessments/CAPABILITY-RUBRIC.md)。

| 周 | 必须学的细节 | 实操任务 | 退出标准 |
|---|---|---|---|
| W1 · P0 内层 | Agent/Workflow、Messages、Tool Calling ID、Action/Observation、ReAct、Stop、ACL | 跑既有 Mini Agent，自己加一个工具失败分支 | 能独立画 Agent Loop、解释 Tool 和 Final、保存负例 |
| W2 · P0 外层 | Trigger、稳定 task_id、Task Contract、Verifier、Retry/Stop、反馈、安全审批 | 跑本仓 Outer Loop Toy，模拟失败→修复→通过 | 冻结验收前置、重复触发不重复开任务、严格停机 |
| W3 · P0 持久性/异常 | State、Run ID、Thread ID、Checkpoint、Writer/Verifier 分离、预算、无进展检测、Tool/Run/Trigger 三层重试 | 修改 Toy 预算/状态；设计 LangGraph + DB 测试方案 | 能解释崩溃恢复与副作用未知的转人工条件 |
| W4 · P1/P2 工程迁移 | 真实 CI/数据库对照、评价器独立、调度、追踪、成本、沙箱、人体审批 | 选客服或 Coding Agent，画生产图并冻结最小任务集 | 对比一轮 Agent 与有限 Outer Loop，报告分母/成本/风险 |

## 前三天具体做什么

**Day 1：内层 Loop。** 30 分钟读 [Anthropic](https://www.anthropic.com/research/building-effective-agents) 的 Agents 部分；60 分钟跑 [Mini Loop](../../labs/MINI-AGENT-LOOP.md) 并修改 max_steps；30 分钟注入非法工具与跨租户；20 分钟闭卷解释 Function Calling 不自动执行 Python。

**Day 2：外层 Loop。** 30 分钟精读 [IBM Loop Engineering](https://www.ibm.com/think/topics/loop-engineering)；70 分钟跑 [Outer Loop](labs/README.md)，观察失败→反馈→二次执行→独立通过；30 分钟修改允许尝试次数与验收预期；20 分钟画双层循环，指出哪个不是 LLM。

**Day 3：可靠性与退出。** 25 分钟读 [LangGraph 持久化](https://docs.langchain.com/oss/python/langgraph/persistence)；65 分钟跑重复触发、状态重载、无进展、权限拒绝、费用/尝试上限；35 分钟根据 [案例](CASE-STUDY.md) 设计退款/代码两条流程；25 分钟口述「为什么 Agent 自称完成仍是失败」。

## 8 个专题优先级

| 主题 | 优先级 | 需要的原理/实验 |
|---|---|---|
| Agent Loop / Tool Calling | P0 | Model/Host 分离、ID、Budget/Stop |
| Independent Verification | P0 | CI/DB/File Oracle；防自我评分 |
| Retry / Termination / Progress | P0 | 可恢复与不可恢复错误、attempt/timeout、无进展 |
| Task State / Idempotency | P0 | trigger/task/run/action IDs、持久状态 |
| Error/Trace/Eval | P0 | 调用链与分母，错误隔离 |
| Scheduler / Event Integration | P1 | Webhook、Cron、Queue 和去重 |
| LangGraph/Workflow Integration | P1 | Graph state vs Outer Task state、Interrupt |
| Distributed Consensus/Parallel Runners | P2 | CAS/lease、竞争、Outbox；纯 Toy 不包含 |

## 推荐学习策略

坚持「先做单次 Agent，再做触发/验收/反馈外循环，最后做真实系统验证」三阶段。每学一个概念只做最小实验、至少两个失败负例、固定数据与验证器、写出适用边界，再进行闭卷解释。不要先开始复杂框架、分布式任务编排或多 Agent；**单 Agent + 固定测试 + 有限重试**即可理解基本原理。

### 求职面试浓缩版（1 周）

Day 1 Agent Loop → Day 2 外层 Loop → Day 3 状态/幂等 → Day 4 业务权限/人工审批 → Day 5 Evals/Trace → Day 6 客服场景时序 → Day 7 10 分钟白板和异常追问。

**可复现证据卡**：task_id / goal / trusted identity / frozen verifier revision / model+SDK version / run ids / result/failed checks / attempts / environment actual state / failure codes / budget / code SHA / L0–L4 judgement / remaining unknown. 个人掌握程度无法由仓库 CI 自动决定。
