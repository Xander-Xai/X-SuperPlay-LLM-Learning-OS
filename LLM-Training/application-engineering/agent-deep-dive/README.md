# Agent 全体系精读课｜从机制到可验证的工程能力

> **2026-11-15 严格补全版**：用于逐项兑现用户给出的八层知识地图、八周路线、三项目、学习节奏和面试验收。已有 [Agent 主线](../AGENT-LEARNING-PATH.md) 仍是总导航，本目录是其**深度课件和执行手册**，不是新的训练 M13–M20，也不增加 APP-AGENT 等 10 条横向专题编号。

## 从这里开始

1. **先看自己缺什么**：[8 个知识模块逐项深度覆盖](CORE-01-04.md) / [后 4 个模块](CORE-05-08.md)；每个模块有专业机制、白话解释、输入输出、决策取舍、真实失败类型和复现题。
2. **把学习计划变成操作**：[8 周任务卡与前三天逐小时执行](STUDY-SCHEDULE.md)；可压缩和跳学，不能直接将阅读打卡算掌握。
3. **按问题查官方**：[带权威等级和使用条件的来源](SOURCES.md)；尽量长期入口，对日期和版本敏感的规范需记录使用版本。
4. **真正跑代码**：[实验操作清单](LABS.md) → [已合成 Agent Loop](../labs/MINI-AGENT-LOOP.md) → [可选真实 Chat Completions Provider Adapter](../labs/REAL-LLM-OPTIONAL.md)。
5. **检验有没有学会**：[课程覆盖和验收台账](COVERAGE.md) + [三项目/评测方案](../AGENT-PRACTICE-AND-EVAL.md) + [24 道面试题](../AGENT-INTERVIEW-QUESTIONS.md)。

~~~mermaid
flowchart TD
    G[业务目标与授权身份] --> W{固定 Workflow 是否足够?}
    W -->|足够| WF[最简 Workflow + 工具]
    W -->|不足| L[Agent Runtime Loop]
    L --> M[LLM 动态决策: final/tool_call]
    M -->|工具提议| T[Gateway: 解析/契约/权限/审批/幂等]
    T -->|允许| X[执行工具/业务 DB]
    T -->|拒绝| O[明确 Tool Error]
    X --> O
    O --> C[状态/上下文 + Trace/Checkpoint]
    C --> L
    M -->|终态| F[结果与业务状态复核]
    WF --> F
    F --> E[Eval: 任务成功/安全/延迟/成本]
    E --> P[工程门禁与版本]
~~~

## 原资料 8 项与本仓对应

| 原需求 | 深学课件 | 实操/证据 |
|---|---|---|
| 模块 1 原理、ReAct、Agent Loop | [CORE 1](CORE-01-04.md#模块-1agent-基础原理与-loop) | [Mini Loop](../labs/MINI-AGENT-LOOP.md) |
| 模块 2 工具、规划、上下文 | [CORE 2](CORE-01-04.md#模块-2工具规划与上下文工程) | [工具/上下文纵切](../labs/README.md) |
| 模块 3 LangGraph 状态机 | [CORE 3](CORE-01-04.md#模块-3langgraph-与状态机) | [LangGraph 运行卡](LABS.md#实验-b-langgraph-状态机与审批恢复) |
| 模块 4 多智能体、记忆、RAG | [CORE 4](CORE-01-04.md#模块-4记忆rag-与多-agent) | [架构对照](LABS.md#实验-c-单-agent-与多-agent-对照) |
| 模块 5 企业级运行 | [CORE 5](CORE-05-08.md#模块-5企业级-agent-工程) | [服务/故障实验](LABS.md#实验-d-生产工程和故障注入) |
| 模块 6 Evals、Trace、安全 | [CORE 6](CORE-05-08.md#模块-6评测可观测性安全) | [现有 19 案例](../labs/README.md) |
| 模块 7 MCP/Skills/A2A/Harness | [CORE 7](CORE-05-08.md#模块-7协议skills-与-harness) | [接口练习](LABS.md#实验-e-协议和长任务-harness) |
| 模块 8 交付与面试 | [CORE 8](CORE-05-08.md#模块-8综合交付与面试) | [项目](../AGENT-PRACTICE-AND-EVAL.md) / [面试题](../AGENT-INTERVIEW-QUESTIONS.md) |

**最重要的认知**：LLM ≠ Agent，工具调用提议 ≠ 工具执行权限，Workflow ≠ Agent，State ≠ Checkpoint ≠ 业务 DB，MCP ≠ A2A，RAG ≠ 长期记忆，自动测试通过 ≠ 个人掌握或生产系统已验证。

## 学习与验收统一口径

课程采用原文的学习时间分配作为**建议**：原理 20%，框架编排 25%，生产 30%，评测与复盘 25%。约 150 分钟/天：30 分钟官方原文、70 分钟动手、30 分钟实验/Trace、20 分钟闭卷复盘。

**保持仓库既有权威评分**：[L0–L4](../../assessments/CAPABILITY-RUBRIC.md) 不能另造并列的“四级验收体系”。
- L0：定位概念；L1：正确解释机制与边界；L2：独立实现且留证据；L3：受控诊断/比较；L4：陌生任务迁移。
- 原文的「知道→理解→实现→工程」仅是教学通俗表达，不等于仓库 L1/L2/L3/L4 的机械映射。工程上线需要额外 [G0–G8](../../production/PRODUCTION-READINESS.md)。
- 所有非真模型实验继续标为 SYNTHETIC / NO_REAL_LLM；Week 3–8 项目如果尚未真正运行，不得升级为 PASS。

## 快捷开始

~~~bash
python LLM-Training/application-engineering/labs/mini_agent_loop.py
python -m unittest discover -s LLM-Training/application-engineering/labs -p 'test_mini_agent_loop.py' -v
python LLM-Training/application-engineering/labs/evaluate_benchmark.py
python LLM-Training/application-engineering/agent-deep-dive/validate_agent_curriculum.py
~~~
