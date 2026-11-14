# 官方与一手资料索引｜Agent Loop / Loop Engineering

> 查阅日期：2026-11-15。P0：厂商一手工程/框架官方；P1：研究论文（需看设计和局限）。Loop Engineering 是**新兴实践术语而非统一官方标准**，不能把 IBM 的概念描述误称为兼容性规范。

| 学习顺序 | 来源 | 类别/日期 | 重点问题 |
|---|---|---|---|
| 1 | [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) | P0，一手工程，2024-12-19 | Agent Loop、Workflow vs Agent、Evaluator-Optimizer、复杂度取舍 |
| 2 | [OpenAI Agents SDK: Running Agents](https://openai.github.io/openai-agents-python/running_agents/) | P0，框架官方，动态版本 | Runner、Tool、Handoff、模型决策次数与结束 |
| 3 | [IBM: What Is Loop Engineering?](https://www.ibm.com/think/topics/loop-engineering) | P0，一手工程解释，2026-07-17 | 为何将任务触发、验证和自动迭代当成工程对象 |
| 4 | [Loop Engineering: Building Blocks, Adoption, and Impact](https://arxiv.org/abs/2608.21884) | P1，2026-08-22 探索性研究/预印本 | 触发器、机器可检终止、持久状态、Verifier、预算、人类升级 |
| 5 | [LangGraph: Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | P0，框架官方 | Checkpointer、thread_id 与 Store |
| 6 | [LangGraph: Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | P0，框架官方 | HITL、恢复与重新执行 |
| 7 | [LangGraph: Durable Execution](https://docs.langchain.com/oss/python/langgraph/durable-execution) | P0，框架官方 | Task 边界、持久运行与副作用 |
| 8 | [Anthropic: Demystifying Evals for AI Agents](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) | P0，一手评测工程，2026-01-09 | 三层评测：结果、轨迹、真实环境 |
| 9 | [Loop Engineering for Agentic Software Systems](https://doi.org/10.1111/exsy.70442) | P1，2026-10-07 研究综述 | 设计视角、模式和未解决的验证问题 |
| 10 | [OpenTelemetry](https://opentelemetry.io/docs/) / [OWASP Agentic Top 10](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | 官方/安全社区 | 链路追踪、跨系统约束、潜在风险 |

## 精读顺序与可信边界

**Day 1–2**：Anthropic Agent Loop → 本仓纯 Python mini agent → OpenAI Runner；能解释内层循环和工具协议。

**Day 3–4**：IBM Loop Engineering → 2026 年研究论文 → 本仓 Outer Loop Toy；能解释外层 Trigger、Verifier、Persist、Retry、Stop。

**Day 5–7**：LangGraph Persistence/Interrupts/Durable → Anthropic Evals → OWASP；能识别权限、重复副作用、没有进展、验证器不可信、恢复中的状态错误。

研究局限：2026-08 预印本研究使用开源仓库启发式样本，不等于已通过随机实验证明自动循环更优；不能将研究中的数量和案例推演成自己项目指标。

框架版本风险：实际 SDK、状态/恢复语义以安装版本和官方 tag 为准。官方文档可迁移；学习记录应保留 URL、publisher、published_on、checked_on、revision、代码 SHA、使用的结论与不支持的外推。不可大量复制版权受保护原文。

## 相关资料如何复用

- [Agent 既有权威索引](../../AGENT-OFFICIAL-RESOURCES.md) 有 Tool、ReAct、Context、MCP 等，不重复复制。
- [训练中的 Agentic RL](../../../reinforcement-learning/AGENTIC-RL-LEARNING-PATH.md) 指优化模型策略；不等于运行时外层任务 Loop。
- [AI-Native 学习闭环](../../../learning-method/AI-NATIVE-LEARNING-LOOP.md) 是人为学习方法，不是 Agent Loop。
