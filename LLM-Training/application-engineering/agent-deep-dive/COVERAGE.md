# 原始要求与实际落盘的逐项覆盖台账

> 本表只说明资料、实验规格和合成测试**存在**，不是学习者已掌握，更不是生产上线通过。适用原始用户输入的八层知识地图、八周计划、三项目、精选资料与前三天动作。

| 原要求 | 对应文档 | 可核验结果 | 状态 |
|---|---|---|---|
| 八层完整知识地图、Workflow/Agent/Tool/MCP/RAG/Harness 区分 | [总导航](README.md) + [核心前四](CORE-01-04.md) | 概念、时序与关键混淆 | DOC_READY |
| 8 周计划、P0/P1/P2、150 分钟/天、20/25/30/25 | [学习日历](STUDY-SCHEDULE.md) | 周计划与每日操作 | DOC_READY |
| 模块 1 Messages、ReAct、Loop、Tool Calling、停止 | [模块1](CORE-01-04.md) + [Mini Loop](../labs/MINI-AGENT-LOOP.md) | 合成测试、真实 API FakeClient 12 项 | SYNTHETIC_TESTED/LIVE_NOT_RUN |
| 模块 2 工具/规划/Context/Guardrails | [模块2](CORE-01-04.md) + [现有纵切](../labs/README.md) | 合成权限/Tool 测试 | SYNTHETIC_TESTED |
| 模块 3 LangGraph State/Reducer/Command/Send/Checkpoint/Interrupt | [模块3](CORE-01-04.md) + [实验B](LABS.md) | 机制/运行卡 | DOC_READY/LANGGRAPH_NOT_RUN |
| 模块 4 Memory、RAG、六种协作模式 | [模块4](CORE-01-04.md) + [实验C](LABS.md) | 架构取舍与负例 | DOC_READY/MULTI_AGENT_NOT_RUN |
| 模块 5 API/SSE/Celery/Redis/PostgreSQL/幂等/DLQ/回滚 | [模块5](CORE-05-08.md) + [实验D](LABS.md) | 故障注入清单 | DOC_READY/REAL_DB_NOT_RUN |
| 模块 6 Tracing/Evals/Safety/成本/P95 | [模块6](CORE-05-08.md) + [19 固定案例](../labs/README.md) | 合成结果、独立分母 | SYNTHETIC_TESTED/REAL_EVAL_NOT_RUN |
| 模块 7 MCP/Skills/A2A/Sandbox/Harness | [模块7](CORE-05-08.md) + [实验E](LABS.md) | 官方规范与操作卡 | DOC_READY/MCP_NOT_RUN |
| 模块 8 工程交付/架构/面试 | [模块8](CORE-05-08.md) + [24 题](../AGENT-INTERVIEW-QUESTIONS.md) | 面试卡与独立迁移要求 | DOC_READY/LEARNER_UNASSESSED |
| 10 条精选高质量资料、权威来源维护 | [来源抽查](SOURCES.md) | 2026-11-15 重点官方入口人工验证 | SOURCE_INDEX_READY |
| 三递进项目及退款链路穿透式复盘 | [实验 A–E](LABS.md) + [项目协议](../AGENT-PRACTICE-AND-EVAL.md) | A 合成教学；B/C 真环境未运行 | PARTIAL |
| Day 1/2/3 可操作任务与时间预算 | [前三天手册](STUDY-SCHEDULE.md) | 命令、输入、负例、产出 | DOC_READY |
| L0–L4 与 P0 求职优先级 | [学习日历](STUDY-SCHEDULE.md) + [Rubric](../../assessments/CAPABILITY-RUBRIC.md) | 沿用唯一能力口径 | DOC_READY/LEARNER_UNASSESSED |

## 状态定义

- DOC_READY：文档与相对链接存在；不等于已运行。
- SYNTHETIC_TESTED：预写模型/合成订单下的确定性单测；不等于真实 LLM、真实权限或事务保证。
- SOURCE_INDEX_READY：重点官网抽查及版本风险已记录；不保证未来链接永久有效。
- REAL_*_NOT_RUN / LEARNER_UNASSESSED：没有真实端到端执行与个人能力证据；既不能记 PASS 也不是代码 Fail。
- PROD：只有实际上线场景通过 [G0–G8](../../production/PRODUCTION-READINESS.md) 后才能声称满足生产门禁。

## 自动化约束

[机器清单](agent-curriculum-manifest.json) → [验证器](validate_agent_curriculum.py) → [回归测试](test_agent_curriculum.py)。CI 检查 8 模块、8 周、3 项目、3 天和官方来源、教学代码存在；另执行 16 项原 Mini Loop 测试及 12 项 Provider FakeClient 测试。GitHub CI 通过时仅说明这些合同，不声明 LangGraph/Redis/PostgreSQL/MCP 实测或个人能力达标。

**增量边界**：保留原有 M01–M12、10 应用专题、19 条固定合成评测、旧项目课程与已有 QA。此处是此前 PR #14 的深度课程补全。
