# Agent 权威资料、阅读顺序与来源审计

> 复核日期：2026-11-15。P0 指官方规范/原始论文/框架官方文档/作者一手工程，P1 指权威发布者课程。链接可用不保证示例在不同 SDK 版本仍能运行。使用时记录 checked_on、版本、安装包 tag/commit 和实际命令。

## 原文 10 项精读路线

| 顺序 | 来源（优先官方长期入口） | 用途 | 注释 |
|---|---|---|---|
| 1 | [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/unit0/introduction) | 系统入门、练习与项目 | P1；同一课程还含 LangGraph 单元 |
| 2 | [Anthropic Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) | Workflow vs Agent、经典模式 | P0；发表于 **2024-12-19**，原文提示工具生态已更新 |
| 3 | [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) | Agent/Tool/Handoff/Session/Trace | P0；对照对应 SDK 版本 |
| 4 | [LangGraph Workflows and Agents](https://docs.langchain.com/oss/python/langgraph/workflows-agents) | 显式状态图和动态流程 | P0 |
| 5 | [HF LangGraph 教程](https://huggingface.co/learn/agents-course/en/unit2/langgraph/introduction) | 代码实操 | P1，遇到旧 API 应回到框架官方 |
| 6 | [Context Engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) | 上下文预算与压缩 | P0 |
| 7 | [LangGraph Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | Checkpoint/Store/Thread | P0 |
| 8 | [OpenAI Agent Tracing](https://openai.github.io/openai-agents-python/tracing/) | Trace/Span/Tool/Handoff | P0 |
| 9 | [Anthropic Agent Evals](https://www.anthropic.com/research/demystifying-evals-for-ai-agents) | 多轮任务评测、轨迹 | P0；发表于 **2026-01-09** |
| 10 | [Google ADK](https://google.github.io/adk-docs/) | 横向比较另一套 Agent 抽象 | P0，选学，不要求全栈学多套框架 |

**建议顺序**：1 → 2 → 3 → 4 → 6 → 7 → 8 → 9，其他资料按需查阅，配合 [八周计划](STUDY-SCHEDULE.md)。

## 关键难点补充

| 主题 | 官方/一手链接 | 必须能解决的问题 |
|---|---|---|
| Tool Calling 细节 | [OpenAI Function Calling](https://developers.openai.com/api/docs/guides/function-calling) | Chat Completions tool_call_id 与 Responses function_call_output **不可混用** |
| ReAct | [原始论文](https://arxiv.org/abs/2210.03629) | Action/Observation 迭代，不等于强制泄露模型内部思考 |
| LangGraph Graph API | [Thinking in Graph API](https://docs.langchain.com/oss/python/langgraph/thinking-in-graph-api) | Node/State/Edge |
| LangGraph HITL | [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts) | 恢复时的状态与副作用 |
| LangGraph 容错 | [Fault Tolerance](https://docs.langchain.com/oss/python/langgraph/fault-tolerance) | 重试/幂等/缺少回执 |
| Tools | [Writing Effective Tools](https://www.anthropic.com/engineering/writing-tools-for-agents) | Schema/错误/歧义 |
| Multi-agent | [Anthropic Multi-Agent Research](https://www.anthropic.com/engineering/multi-agent-research-system) | 协作成本与取舍 |
| MCP | [MCP 规范入口](https://modelcontextprotocol.io/specification/) | 当前导向 2026-07-28 版；复现时固定版本 URL |
| Agent Skills | [Agent Skills Specification](https://agentskills.io/specification) | SKILL.md 最低要求与附件组织 |
| A2A | [A2A Protocol](https://a2a-protocol.org/latest/) | 独立 Agent 的互操作，不等于本地 Handoff |
| Harness | [Anthropic Long-running Apps](https://www.anthropic.com/research/harness-design-long-running-apps) | 长任务、上下文重置、单/多 Agent 对照 |
| Graph Eval | [LangSmith Graph Evaluation](https://docs.langchain.com/langsmith/evaluate-graph) | 图结果/轨迹评测 |
| Agent 安全 | [OWASP Agentic Top 10](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) | 注入、越权、工具风险 |
| 工程基础 | [FastAPI](https://fastapi.tiangolo.com/) / [OpenTelemetry](https://opentelemetry.io/docs/) | 接口和可观测性 |

**Computer Use（P2 权威扩展）**：[Anthropic 官方 Computer Use Tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) 与 [OpenAI 官方 Computer Use](https://developers.openai.com/api/docs/guides/tools-computer-use)。两者官方页面在 2026-11-15 已抽查可访问；实际工具版本和安全要求必须以对应模型和运行版本为准。

## 官方网站抽查（2026-11-15）

- Anthropic Building Effective Agents：页面可打开、发布于 2024-12-19，并在正文注明部分工具生态已变化；用于经典架构思想，**不是**当前 SDK API 的全部证据。
- OpenAI Agents SDK Running Agents：可打开，包含 Runner loop、tools、state、durable execution 内容；实际接口需确认安装版本。
- OpenAI Function Calling：可打开，包含 Responses API 与 Chat Completions 两套示例；不能跨格式随意混用。
- LangGraph Persistence/Interrupts/Fault Tolerance/Thinking in Graph API：可打开，文档明确 Checkpointer vs Store、恢复时的语义；必须真框架实测。
- MCP 主规范：当期官方入口重定向到 **2026-07-28**；具体实验务必固定规范版本。
- Agent Skills：可打开，最低要求是 SKILL.md，scripts/references/assets 可选。
- A2A 当前官方入口：包含协议、任务生命周期和 SDK 导航。
- Anthropic Agent Evals：可打开，发布于 **2026-01-09**；评测方法需自行设计数据集。
- Hugging Face Agents Course Unit 0：可打开，有 Unit 1、LangGraph、Agentic RAG 和最终项目。
- Anthropic Harness Design for Long-running Apps：可打开，发布于 **2026-03-24**。

这些是本轮**重点抽查**，不是自动化逐链接 HTTP 监控，不保证每个其它外链实时可用。

## 更新流程

学习记录必须保存 source_id、publisher、original URL、checked_on、发布/版本日期、SDK tag 与实际实验代码 SHA；不复制第三方全文。外链失效从官方主页/源码/tag 找替代，记录替换来源和差异，不静默改成社区转载。原有 [Agent 资源索引](../AGENT-OFFICIAL-RESOURCES.md) 仍保留；此页是带审核日期的深学参考，不创建新的训练模块。
