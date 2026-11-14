# Agent 系统化课程：原始要求逐项严格验收（2026-11-15）

## 总结

**状态：CURRICULUM_AND_SYNTHETIC_QA_PASS / REAL_LLM_NOT_RUN / LEARNER_UNASSESSED / PRODUCTION_NOT_ASSESSED**。

任务来源：用户要求把「从底层原理到企业级 Agent」的八大知识模块、8 周完整路线、权威资料、三项目、学习策略与 Day 1–3 操作完整落盘，并遵守原仓规范严格验收。

本次不替换已有 [原 Agent 路线](application-engineering/AGENT-LEARNING-PATH.md)；增补 [Agent Deep Dive 总入口](application-engineering/agent-deep-dive/README.md)。原有 M01–M12、10 个应用横向专题、19 条合成评测、L0–L4 Rubric 和 G0–G8 生产门禁全部保留。原表所述「L1 知道→L4 工程」是通俗表达；仓库唯一能力等级仍是 [Rubric](assessments/CAPABILITY-RUBRIC.md)。

## 对原始清单的验收结果

| 验收项 | 落盘证据 | 结果 |
|---|---|---|
| 八层知识地图、LLM/Workflow/Agent/Tool/MCP/RAG/Harness 关系 | [总入口](application-engineering/agent-deep-dive/README.md) + [CORE1–4](application-engineering/agent-deep-dive/CORE-01-04.md) | 文档 PASS |
| 模块 1–4 的定义、消息/Loop、工具、LangGraph、记忆/协作、失败边界 | [CORE1–4](application-engineering/agent-deep-dive/CORE-01-04.md) | 文档 PASS |
| 模块 5–8 的工程、评测/安全、MCP/Skills/A2A/Harness、系统设计 | [CORE5–8](application-engineering/agent-deep-dive/CORE-05-08.md) | 文档 PASS |
| 8 周、P0/P1、20/25/30/25、每日 150min、Day 1/2/3 | [学习日历](application-engineering/agent-deep-dive/STUDY-SCHEDULE.md) | 文档 PASS |
| 稳定权威来源、责任/发布日期/版本边界 | [来源审计](application-engineering/agent-deep-dive/SOURCES.md) | 重点官网抽查完成 |
| 三项目、实验 A–E、故障注入与指标分母 | [实验 SOP](application-engineering/agent-deep-dive/LABS.md) + [原项目评测协议](application-engineering/AGENT-PRACTICE-AND-EVAL.md) | A 合成测试 PASS；B/C 真实环境 NOT_RUN |
| 纯 Python Mini Agent 及原有 16 项单测 | [Mini Loop](application-engineering/labs/MINI-AGENT-LOOP.md) | SYNTHETIC PASS |
| 真实模型 Tool Calling 的可选练习和消息关联 | [可选适配器](application-engineering/labs/REAL-LLM-OPTIONAL.md) + [FakeClient](application-engineering/labs/test_real_llm_optional.py) | 12 项离线模拟 PASS；实际 API LIVE_NOT_RUN |
| 8 模块/8 周/3 天/3 项目/10 来源和旧等级保持一致 | [Manifest](application-engineering/agent-deep-dive/agent-curriculum-manifest.json) / [Validator](application-engineering/agent-deep-dive/validate_agent_curriculum.py) / [测试](application-engineering/agent-deep-dive/test_agent_curriculum.py) | 校验 0 问题，8 项负例/合同 PASS |
| README/索引/文档 QA/CI | 根 README、Training README、应用工程入口、check_repo.py、.github/workflows | PASS |
| 真实 LangGraph Checkpoint/Interrupt、MCP、Celery/Redis/PostgreSQL、生产性能 | 独立实验 SOP 已写 | NOT_RUN / NOT_ASSESSED |
| 用户个人闭卷、陌生任务独立迁移 | 个人学习需要实际输出与考核 | LEARNER_UNASSESSED |

## 可复查 GitHub 证据

- 合并 PR：[PR #19](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/pull/19)。
- 合并提交：[20e4ef38c98e4ebd8df176b53c7145481c1c28e5](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/commit/20e4ef38c98e4ebd8df176b53c7145481c1c28e5)。
- PR 通过的 GitHub Actions：[43616312245](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/actions/runs/43616312245)；docs 与 cpu-toy 均 success；包含新 Agent Deep Dive 8 项合同测试、Provider FakeClient 12 项测试和原 Mini Agent 16 项测试，既有 RAG/RL 等测试保持通过。
- PR 前已修复一次机器索引明确术语缺失：Module A4 加入 Memory/短期/长期边界；失败日志经修正后重跑通过。
- 合并后重新读取 main 的主入口、两份课程、日历、资料、实验、覆盖台账、可选适配器、CI 文件，文件内容存在；不把「页面可打开」等同于「使用者掌握」。

## 严格不声称

1. 本仓现有 ScriptedModel 和 FakeClient 不是真实模型推理；单测只验证工具调用协议的教学逻辑。
2. 10 项官方资料来源是学习导航，网站与库版本会变化；本轮抽查的关键官网入口可访问，但不是永久在线保证或全部外链的定期 HTTP 监控。
3. 本仓未实测真实模型成本、LangGraph 真框架/实际分布式 Checkpoint、Redis/Celery/PostgreSQL 事务、MCP 通信、线上负载或生产数据安全。
4. User 学习等级必须由本人提供闭卷/代码/负例/盲测证据；CI PASS 不代表 L4。
5. 需要真正投产时，走 [G0–G8](production/PRODUCTION-READINESS.md)，不能将本次「资料落盘 PASS」用于生产 SLA 背书。

## 继续学习的具体入口

先按 [Day 1–3 操作](application-engineering/agent-deep-dive/STUDY-SCHEDULE.md) 自己运行合成 Loop、工具错误与客服流程复盘，再按 Week 3/5/6 在独立项目实现真实状态机、故障和评测，保留真实日志。完成当前岗位要求后按需求跳学，不要求一次性学完所有框架。
