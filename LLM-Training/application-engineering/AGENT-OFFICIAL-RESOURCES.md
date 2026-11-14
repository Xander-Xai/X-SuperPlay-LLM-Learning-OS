# Agent 官方资源索引｜学习职责、版本与审计

**2026-11-15 核查入口**：[资料出处与版本适用边界](agent-deep-dive/SOURCES.md)，包含 Anthropic 原文日期、MCP 当前规范版本及框架官方入口抽查记录。

> 整理于 2026-11-14，资料以长期官方入口为主。链接可能随 SDK 或规范版本变更；实际实现需要核对发布版本、发布日期、源码 tag。P0=官方规范/官方文档/一手工程文章；P1=官方作者课程；P2=第三方材料仅用于启发，不代替结论。本索引不是声称已安装或执行这些 SDK。

## 优先精读的十个入口

| 顺序 | 来源和等级 | 用途 | 学完需要解释/实现什么 |
|---|---|---|---|
| 1 | [HF Agents Course Unit 1](https://huggingface.co/learn/agents-course/unit1/introduction)（P1） | Message、Tool、Think/Act/Observe | 纯 Python Agent Loop |
| 2 | [Anthropic Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)（P0） | Workflow、Routing、Parallel、Evaluator | 何时不需要多 Agent |
| 3 | [OpenAI Agents SDK Runner](https://openai.github.io/openai-agents-python/running_agents/)（P0） | 模型循环、终止、工具执行、状态 | 对照原生 Loop |
| 4 | [OpenAI Agent Tools](https://openai.github.io/openai-agents-python/tools/)（P0） | 工具契约、错误 | 实现服务端 Gateway |
| 5 | [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)（P0） | 显式 StateGraph 和编排 | 画出客服图 |
| 6 | [LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence)（P0） | Thread、Checkpoint、Store | 区分会话与长期记忆 |
| 7 | [LangGraph Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)（P0） | 人工审批和恢复 | 处理重复副作用 |
| 8 | [Anthropic Context Engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents)（P0） | 上下文预算、历史、工具观察 | 优化模型输入 |
| 9 | [OpenAI Tracing](https://openai.github.io/openai-agents-python/tracing/)（P0） | Trace/Span/Tool/Handoff | 失败归因 |
| 10 | [Anthropic Agent Evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)（P0） | 多轮评测和轨迹 | 冻结测试集与分母 |

## 按需求阅读的一手资料

| 主题 | 参考 | 最小任务 |
|---|---|---|
| ReAct 思想 | [ReAct 原始论文](https://arxiv.org/abs/2210.03629) | 区分推理/动作/观察与不公开的模型内部推理 |
| 工具设计 | [Writing Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | 对重叠工具做对照 |
| LangGraph Durable | [Durable Execution](https://docs.langchain.com/oss/python/langgraph/durable-execution) | 崩溃恢复而不重复副作用 |
| LangGraph 状态设计 | [Thinking in LangGraph](https://docs.langchain.com/oss/python/langgraph/thinking-in-langgraph) | State/Node/Edge 的职责 |
| Handoff | [OpenAI Handoffs](https://openai.github.io/openai-agents-python/handoffs/) | 控制委派时上下文传递 |
| 多智能体一手案例 | [Anthropic Multi-Agent Research](https://www.anthropic.com/engineering/multi-agent-research-system) | 同基线对比协调成本 |
| Agentic RAG | [LangChain Retrieval](https://docs.langchain.com/oss/python/langchain/retrieval) | 动态检索与证据引用 |
| MCP | [MCP Specification](https://modelcontextprotocol.io/specification/) / [官方规范仓](https://github.com/modelcontextprotocol/modelcontextprotocol) | Host/Client/Server、Tools/Resources/Prompts |
| Skills | [Agent Skills Specification](https://agentskills.io/specification) | Skill 组织说明、脚本、参考材料 |
| A2A | [A2A Protocol](https://a2a-protocol.org/latest/) | 了解跨系统 Agent 协作，不作为入门前置 |
| ADK 对照 | [Google ADK](https://google.github.io/adk-docs/) | 比较 Runtime API |
| 生产服务 | [FastAPI](https://fastapi.tiangolo.com/) | API 与认证 |
| 可观测性 | [OpenTelemetry](https://opentelemetry.io/docs/) | Trace、Metric、Log |
| 安全 | [OWASP GenAI](https://genai.owasp.org/) | 注入、数据/工具权限边界 |
| RAG/Agent 指标 | [Ragas Docs](https://docs.ragas.io/en/latest/) | 指标适用范围与人工核验 |
| 框架源码 | [OpenAI Agents Python GitHub](https://github.com/openai/openai-agents-python) | 按 tag 查 SDK 实现 |

## 来源维护约定

- 在实验记录中保存 source URL、publisher、checked_on、文档版本、SDK version/commit、实际命令和支持的结论。
- 规范阅读指定版本，尤其 MCP 等可能跨版本改变传输/会话语义；不要混合旧教程和新 SDK。
- 页面迁移时先到官方目录、官方仓库与 release 查找，不替换成来历不明的镜像。
- **读取权威资料 ≠ 真正运行实现；复现模拟代码 ≠ 获得生产 SLA；看到案例提升数值 ≠ 自己实现了相同效果。**
- [既有上游固定版本资源](README.md#上游权威内容已经存在不重复建设) 保持独立来源事实，本页不复制其正文。

回到 [学习主线](AGENT-LEARNING-PATH.md) · [实践与评测](AGENT-PRACTICE-AND-EVAL.md)。
