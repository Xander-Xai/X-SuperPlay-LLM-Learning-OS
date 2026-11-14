# Agent Loop × Loop Engineering 专题严格落盘验收（2026-11-15）

> **最终口径：CURRICULUM_AND_SYNTHETIC_QA_PASS / REAL_LLM_NOT_RUN / REAL_CI_NOT_RUN / DISTRIBUTED_NOT_RUN / LEARNER_UNASSESSED / PRODUCTION_NOT_ASSESSED**。机器测试只确认资料、合同和合成状态机，不等于现实可自动部署或自主退款。

## 1. 实际仓库核查

2026-11-15 的 main 原本已有：Agent Loop 原理、Mini Agent Python 脚本和负例测试、Harness 专题、LangGraph State/Checkpoint/Interrupt、Agent Eval 与工程课件；**未找到独立的 Loop Engineering 学习体系、跨 Run 的触发/独立验证/反馈/停止课程或专门外层循环实验**。

按此差距，新增 [专项入口](application-engineering/agent-deep-dive/loop-engineering/README.md)、[完整机制](application-engineering/agent-deep-dive/loop-engineering/CORE.md)、[4 周计划](application-engineering/agent-deep-dive/loop-engineering/ROADMAP.md)、[官方/学术来源](application-engineering/agent-deep-dive/loop-engineering/SOURCES.md)、[6 项实验](application-engineering/agent-deep-dive/loop-engineering/LABS.md)、[客服/Coding Agent 案例](application-engineering/agent-deep-dive/loop-engineering/CASE-STUDY.md)、[覆盖矩阵](application-engineering/agent-deep-dive/loop-engineering/COVERAGE.md)。

## 2. 教学实现和 CI

| 条目 | 验收证据 | 结果 |
|---|---|---|
| Agent Loop 原有教具保留 | [Mini Agent Loop](application-engineering/labs/MINI-AGENT-LOOP.md) | 保留原有 16 项合成测试 |
| Agent 与外层 Loop 区别 | CORE 的五种 Loop、Task State、Handoff/Verifier/Stop | DOC_READY |
| 外层完整任务合同 | [outer_loop.py](application-engineering/agent-deep-dive/loop-engineering/labs/outer_loop.py) | SYNTHETIC_TOY |
| 触发去重、验收、重试、持久/恢复、安全 | [20 项负例与单测](application-engineering/agent-deep-dive/loop-engineering/labs/test_outer_loop.py) | PASS |
| 4 周、6 Labs、5 重要一手资料和目录口径 | [manifest](application-engineering/agent-deep-dive/loop-engineering/loop-course-manifest.json) + [validator](application-engineering/agent-deep-dive/loop-engineering/validate_loop_course.py) + [9 项合同测试](application-engineering/agent-deep-dive/loop-engineering/test_loop_course.py) | PASS |
| README/Agent 深学/Harness 的互链与相对链接 | [根首页](../README.md) + check_repo.py | PASS |
| 既有 RAG、RL、Agent 课程与原 CI 保留 | workflow | PASS |

- 合并 PR：[PR #28](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/pull/28)；合并 SHA：[d729c50d0ee9343819bc2fdc6312b6e86ab12ef8](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/commit/d729c50d0ee9343819bc2fdc6312b6e86ab12ef8)。
- 合并前 CI：[GitHub Actions 43620855913](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/actions/runs/43620855913)；docs 与 cpu-toy **success**。
- 日志校验：Documentation QA 为 markdown=136、local_links=1792、required=169、issues=0；Loop Course validator 为 6 topics / 4 weeks / 6 labs / 5 sources / issues=0；Outer Loop 单测 **20 PASS**，课程合同单测 **9 PASS**。
- 合并后已重新从 main 读取课程总入口、CORE、路线、来源、Outer Loop、测试与 CI，文件存在。

## 3. 特别重要的未验证项

- Toy ScriptedRunner 是一轮 **虚构 Agent Run**，不是 LLM；IndependentVerifier 的 exact-text 规则不是真实 CI、业务 DB 或模型评估。
- JSON TaskStore + os.replace 单进程原子文件替换，不是分布式安全事务、并发 Worker 租约或真正 Exactly Once；本课程**未进行** GitHub Webhook、Celery、PostgreSQL、真实业务退款或线上高并发验证。
- 预算 used_units 是 Toy 每轮假计数，不是真实 Token 或美元；它不能推断费用或 SLA。
- Loop Engineering 2026 年仍属于新兴概念；IBM/预印本的描述不能冒充行业统一标准。
- 真正学习者的 L0–L4、企业生产 G0–G8 需要本人动手和实际工程证据。**CI PASS 不能证明一个人具备 L4，也不代表可对客上线。**

## 4. 首要学习建议

先运行原 [Agent Mini Loop](application-engineering/labs/MINI-AGENT-LOOP.md)，然后做 [Outer Loop 教学实验](application-engineering/agent-deep-dive/loop-engineering/labs/README.md)，对比 Agent 自称成功与独立 Verifier 的结论；按 [四周任务](application-engineering/agent-deep-dive/loop-engineering/ROADMAP.md) 逐步引入触发、恢复、幂等、任务指标，最后使用客服或 Coding Agent 的独立授权测试项目证明真实系统行为。
