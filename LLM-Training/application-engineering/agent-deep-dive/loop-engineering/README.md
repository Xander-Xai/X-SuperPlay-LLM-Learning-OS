# Agent Loop × Loop Engineering｜完整学习入口

> 更新：2026-11-15。定位：现有 Agent 深学的**横切进阶专题**；沿用 APP-AGENT / APP-HARNESS / APP-EVAL，不增加 M01–M12 或新的应用主题编号。等级依据 [L0–L4](../../../assessments/CAPABILITY-RUBRIC.md)。状态：DOC_READY / DETERMINISTIC_TOY_ONLY / REAL_LLM_NOT_RUN / PRODUCTION_NOT_RUN / LEARNER_UNASSESSED。

## 两句话看懂

- **Agent Loop（内层）**：模型在一次运行中反复「观察上下文 → 决策 → 提议工具 → 宿主校验执行 → 回填结果」，直到证据充分、拒绝、超限或人工接管。
- **Loop Engineering（外层任务控制）**：设计能**触发、调用、独立验收、反馈、持久化并安全终止** Agent 运行的自动化系统，即 Trigger → Task Contract → Agent Run → Independent Verifier → Feedback/State → Stop/Retry/Escalate。
- 后者是 2026 年新兴工程术语，不是统一标准，不是另一个 LLM 框架。一个成熟系统可能将内外层融合在单一编排器里；两层图只用于区分职责。

## 执行图

~~~mermaid
flowchart TD
    Trigger[Event/Schedule/Manual] --> Task[Task Contract: Identity/Goal/Verifier]
    Task --> Policy[Outer Policy: Budget/Attempts/Risk]
    Policy --> Runner[Agent Runner / Inner Loop]
    Runner --> Model[Model: final or tool_call]
    Model -->|tool| Gateway[Tool Gateway: ACL/HITL/Idempotency]
    Gateway --> Env[Environment Tools]
    Env --> Obs[Observation/Trace]
    Obs --> Runner
    Model -->|final/failure| Verifier[Independent Verifier: CI/DB/File/Policy]
    Verifier -->|pass| Done[VERIFIED_SUCCESS]
    Verifier -->|fail| Decision{Retry allowed and progress?}
    Decision -->|yes| State[Persist Feedback/Attempt State]
    State --> Policy
    Decision -->|no| Stop[FAILED/ESCALATED/STAGNATED]
~~~

**首要原则**：Agent 说「我完成了」不等于完成。要由独立的 CI、文件、数据库或业务系统实际状态验证。内层 Tool Retry、Agent Run Retry、外层事件重试彼此不同，必须分别设计幂等与终止条件。

## 阅读顺序

| 文件 | 学什么 | 可交付什么 |
|---|---|---|
| [CORE](CORE.md) | 五种 Loop、两层状态机、权限/持久化/重试/验收边界 | 一张完整时序图 |
| [ROADMAP](ROADMAP.md) | 4 周专项、Day 1–3 和求职压缩路径 | 可执行学习任务卡 |
| [SOURCES](SOURCES.md) | IBM 定义、Anthropic 工程、官方框架与研究限制 | 原文精读/版本表 |
| [LABS](LABS.md) | 6 组实验的输入、负例、预期和评测 | 真实命令与失败证据 |
| [CASE-STUDY](CASE-STUDY.md) | 客服退款链和 Coding Agent 的业务完整循环 | 架构解释和面试问答 |
| [Outer Loop 实验](labs/README.md) | 标准库离线触发/Run/Verifier/Persist/Retry | 单元测试与 Trace |
| [COVERAGE](COVERAGE.md) | 原课程与本次增量的覆盖核查 | 课件与运行边界 |

## 一键开始（仓库根目录，Python 3.11+）

~~~bash
# 单次 Agent 内部工具循环：旧课程
python LLM-Training/application-engineering/labs/mini_agent_loop.py

# 跨多个运行的任务反馈循环：本课程
python LLM-Training/application-engineering/agent-deep-dive/loop-engineering/labs/outer_loop.py
python -m unittest discover -s LLM-Training/application-engineering/agent-deep-dive/loop-engineering/labs -p 'test_outer_loop.py' -v
python LLM-Training/application-engineering/agent-deep-dive/loop-engineering/validate_loop_course.py
~~~

## 7 道闭卷题

1. 模型的 Final 为什么不能替代独立 Verifier？
2. Agent Loop、Evaluator–Optimizer Workflow、外层任务循环的不同控制边界？
3. 事件重复投递、一次完整 Agent 重跑、单工具重试为什么不同？
4. Task State、Graph Checkpoint、业务 DB 分别存什么？
5. 失败什么时候自动重试、什么时候要求人工审批？
6. 一直重复同一失败结果时何时触发 STAGNATED？
7. 什么时候直接固定 Workflow 即可，不必额外使用自动外层循环？

**证据声明**：新增标准库代码只提供合成文档/文件验收教学。尚未验证真实 LLM、分布式 Worker、数据库事务、真正 CI 系统、API 成本或生产 SLA。生产必须通过 [G0–G8](../../../production/PRODUCTION-READINESS.md)。

关联：[Agent 深学](../README.md) · [Harness](../../AGENT-HARNESS-ENGINEERING.md) · [Agent Loop Mini Lab](../../labs/MINI-AGENT-LOOP.md)。
