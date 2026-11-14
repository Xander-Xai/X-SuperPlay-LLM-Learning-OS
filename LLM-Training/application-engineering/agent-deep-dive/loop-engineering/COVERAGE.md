# Agent Loop / Loop Engineering 课程覆盖与验收边界

> 本表衡量课程和 Toy 代码的存在与契约，不代表学习者已具备 L4 能力，也不代表企业系统已通过上线门禁。

| 必须学习的主题 | 文档/实验 | 状态 |
|---|---|---|
| Agent Loop 的 Message、Tool Call、Observe、Stop | [CORE](CORE.md) + [既有 Mini Loop](../../labs/MINI-AGENT-LOOP.md) | DOC_READY / SYNTHETIC_TESTED |
| Loop Engineering 新术语及非标准化边界 | [官方资料](SOURCES.md) + [CORE](CORE.md) | SOURCE_REVIEWED |
| Trigger / dedupe / Task Contract | [CORE](CORE.md) + [Outer Loop](labs/README.md) | SYNTHETIC_TESTED |
| Runner vs Independent Verifier、拒绝自我打分 | [CORE](CORE.md) + [单测](labs/test_outer_loop.py) | SYNTHETIC_TESTED |
| Result、Trajectory、Environment 三层验证 | [CORE](CORE.md) + [实验 SOP](LABS.md) | DOC_READY / REAL_NOT_RUN |
| Persistent Task State、Run/Thread/Action ID | [CORE](CORE.md) + [Toy JSON](labs/outer_loop.py) | SYNTHETIC_TESTED / MULTI_WORKER_NOT_RUN |
| Tool/Agent/Task 三层重试和副作用保护 | [CORE](CORE.md) + [客服案例](CASE-STUDY.md) | DOC_READY / REAL_DB_NOT_RUN |
| Budget、Stagnation、Stop、Escalation | [Toy](labs/README.md) + [单测](labs/test_outer_loop.py) | SYNTHETIC_TESTED |
| 4 周学习路线与 Day 1/2/3 | [ROADMAP](ROADMAP.md) | DOC_READY |
| Coding Agent 和客服完整场景 | [CASE-STUDY](CASE-STUDY.md) + [LABS](LABS.md) | SOP_READY / REAL_RUN_NOT_RUN |
| 6 组实验及失败注入、指标 | [LABS](LABS.md) | LAB_A_B_TOY / LAB_C_F_NOT_RUN |
| 规范内索引、校验器和 CI | [manifest](loop-course-manifest.json) / [validator](validate_loop_course.py) | CHECKED_ON_CI |

**严格区分**：Toy ScriptedRunner 不等于真实 Agent，ExactText Verifier 不等于真实 CI 或业务 DB，单进程 JSON + os.replace 不代表分布式事务、没有外部安全副作用、也没有 Token / 美元成本计量。实际能力等级按 [仓库统一 Rubric](../../../assessments/CAPABILITY-RUBRIC.md)；生产按 [G0–G8](../../../production/PRODUCTION-READINESS.md)。

## 当前范围外（独立项目完成）

- 真实 LLM SDK 工具调用和质量评价；
- GitHub Webhook/Actions 与容器沙箱的完整任务自动修复；
- Celery/Redis/PostgreSQL 的持久幂等、并行 Workers、重启恢复与故障注入；
- 客服真实业务数据库核对与授权/审批；
- 长期 Token/费用与任务 P95 的真实统计。

需要源码、环境版本、冻结测试数据、原始 Trace 和业务终态证据后才能更新为通过。
