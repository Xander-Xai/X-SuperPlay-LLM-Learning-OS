# Agent 系统化学习主线｜原理、编排、工程与评测

**严格补充版（2026-11-15）**：[八模块细节讲义](agent-deep-dive/README.md) · [8 周与 Day 1/2/3](agent-deep-dive/STUDY-SCHEDULE.md) · [官方资料审核](agent-deep-dive/SOURCES.md) · [逐项覆盖检查](agent-deep-dive/COVERAGE.md) · [真实 Tool Calling 可选教学](labs/REAL-LLM-OPTIONAL.md)。此处仍是大纲，深学资料在关联目录。

> 修订日期：2026-11-14。状态：CURRICULUM_READY / REAL_AGENT_NOT_RUN / LEARNER_UNASSESSED。属于 [应用工程](README.md) 的 Agent 专项，不新增 M13–M20，不修改 12 个训练模块、10 个应用专题、33 个宏观主题、90 个基础概念或 19 条训练需求。统一能力等级使用 [L0–L4](../assessments/CAPABILITY-RUBRIC.md)，实际生产另过 [G0–G8](../production/PRODUCTION-READINESS.md)。

## 目标和训练方法

面向已有 RAG、LangGraph、多智能体项目经验，但需要补齐执行机制的开发者。完成后应能：独立实现 Agent Loop；说明模型提出工具调用与后端执行的边界；设计状态机、权限、审批、幂等和恢复；建立可复现任务级评测；解释为什么选择或放弃多 Agent。

- 8 周是每天约 2–3 小时的参考节奏，并非强制课表。按真实问题优先，遵守 [AI-Native 按需学习闭环](../learning-method/AI-NATIVE-LEARNING-LOOP.md)。
- 每个知识点都做：官方原文 → 机制图 → 最小实践 → 两个负例 → 受控对照 → 证据卡 → 闭卷追问。
- 主线是 Python 标准库 → LangGraph；OpenAI Agents SDK 用来横向理解另一种 Runtime，Google ADK 只做选学。没有理由一开始同时学五种框架。
- 先学固定 Workflow 基线；复杂编排不能只凭直觉增加，必须看成功率、成本和故障。
- 资料在 [官方资源表](AGENT-OFFICIAL-RESOURCES.md)；三段实验在 [实践与评测](AGENT-PRACTICE-AND-EVAL.md)；闭卷题见 [面试验收](AGENT-INTERVIEW-QUESTIONS.md)。

## 8 层知识地图

| 层 | 核心细节 | 容易混淆的边界 | 证明理解的最小证据 |
|---|---|---|---|
| A1 原理 | Messages、Function Calling、Tool ID、Agent Loop、ReAct、Stop Rule | Function Calling 是动作提议，不会自行执行函数 | 无框架 Mini Agent Loop |
| A2 工具/规划 | JSON Schema、语义校验、超时/重试、Plan、Reflection、Context Budget | Schema 合法不等于已授权；Prompt 不等于全部 Context | 工具契约+非法参数与越权负例 |
| A3 LangGraph | StateGraph、Node、Edge、Reducer、Command、Send、Subgraph、Interrupt、Checkpointer | State 不等于业务 DB；Checkpoint 不等于跨线程长期记忆 | 可暂停、恢复的客服图 |
| A4 记忆/RAG/协作 | 短期/长期记忆、Store、Agentic RAG、Router、Supervisor、Handoff | 多 Agent 不一定比单 Agent 好 | 固定任务集三种架构对比 |
| A5 生产 | FastAPI、SSE、Worker/Queue、DB、幂等、重放、故障恢复 | SSE 不提供后台任务持久性 | 注入响应丢失，不重复扣费/退款 |
| A6 安全/评测 | Traces、Task Success、Tool Accuracy、拒答、Prompt Injection、P95、Cost | 回复说成功不等于业务已成功 | 冻结任务集+实际状态核对 |
| A7 协议/Harness | MCP Host/Client/Server、Tools、Resources、Skills、A2A、Sandbox | MCP 不等于业务 ACL；A2A 不是本地多 Agent 的必要条件 | 只读 MCP 测试服务及不可信输出 |
| A8 综合 | 架构取舍、消融、故障归因、迁移、发布门禁 | 教学 CI 通过不等于上线通过或个人 L4 | 陌生任务独立复现和说明 |

### 端到端执行链（能不查资料画出来才算理解）

~~~mermaid
sequenceDiagram
  participant U as User
  participant API as Auth/API
  participant H as Harness
  participant M as Model
  participant T as Tool Gateway
  participant DB as Business DB
  U->>API: Request
  API->>H: trusted identity + budget
  loop until final or stop
    H->>M: messages + tool schema + context
    M-->>H: final or tool call
    alt tool call
      H->>T: validated args + trusted identity
      T->>T: allowlist / ACL / approval / idempotency
      T->>DB: authorized read or write
      DB-->>T: result
      T-->>H: observation / error
      H->>H: append trace and checkpoint
    end
  end
  H-->>API: final / fail / escalate
  API-->>U: result
~~~

**重要错误边界**：外部写操作已执行但响应超时，不能仅靠重新执行节点重试。必须先核对外部状态，并依赖业务幂等协议、事务与补偿策略。工具异常也不能被 Agent 改写成无证据的成功回答。

## Week 1｜Agent Loop、Tool Call 与 ReAct

**学**：System/User/Assistant/Tool 消息及 Tool Call ID；模型决策、工具执行与观察回填；Final/Refusal/Step Limit；ReAct、固定 Workflow 的区别。

**读**：[HF Agents Unit 1](https://huggingface.co/learn/agents-course/unit1/introduction) → [OpenAI Running Agents](https://openai.github.io/openai-agents-python/running_agents/) → [Anthropic Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents)。

**做**：[Mini Agent Loop](labs/MINI-AGENT-LOOP.md)；自己修改停止条件与工具返回；将教学 ScriptedModel 替换成真实 API 必须另建授权测试环境并明确计费。**负例**：未知工具、无终止循环。**验收**：能闭卷说明 Function Calling 不会自动执行 Python，能显示完整 Trace。

## Week 2｜工具、规划、上下文工程

**学**：JSON Schema、业务约束、权限、参数校验、结构化输出；Planning 与 Reflection；上下文选择、输出预算、对外部数据的不可信处理。

**读**：[Writing Tools for Agents](https://www.anthropic.com/engineering/writing-tools-for-agents) → [Context Engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) → [Prompt 专项](PROMPT-ENGINEERING.md)。

**做**：设计只读订单、知识检索、受审批退款三个工具，比较固定路由与动态工具选择。**负例**：合法 JSON 中的跨租户 ID；检索文档冒充 System 指令。**验收**：明确后台 allowlist/ACL/审批，不能用 Prompt 代替。

## Week 3｜LangGraph 状态机

**学**：StateGraph、Node/Edge、Conditional/Command、Reducer、Send、Thread ID、Checkpointer、Store、Interrupt、Subgraph、Streaming。

**读**：[LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview) → [Persistence](https://docs.langchain.com/oss/python/langgraph/persistence) → [Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)。

**做**：构造「意图→查询→审批中断→恢复→校验」图，并记录恢复前后状态。**负例**：恢复造成重复退款；并发节点覆盖 State。**验收**：解释 Checkpoint 与业务数据的角色，真实 LangGraph 实验要有运行证据，不能用本仓模拟冒充。

## Week 4｜记忆、Agentic RAG 和多 Agent

**学**：短期消息、长期 Store、写入/检索/遗忘、权限隔离；动态检索；Router、Supervisor、Handoff、Agent-as-Tool、并行和评价器。

**读**：[Anthropic Multi-Agent Research](https://www.anthropic.com/engineering/multi-agent-research-system) → [OpenAI Handoffs](https://openai.github.io/openai-agents-python/handoffs/) → [RAG 专项](RAG-ENGINEERING.md)。

**做**：相同冻结客服测试集比较固定 Workflow、单 Agent 与 Router/多 Agent；固定模型、工具、预算。**负例**：Handoff 循环；记忆泄漏。**验收**：能解释什么时候不值得引入多 Agent，报告总成本与 Task Success。

## Week 5｜企业级运行可靠性

**学**：FastAPI、认证/限流、SSE、任务队列、Redis/DB/Checkpoint 作用域、Worker 超时与恢复、幂等、补偿、DLQ、重试退避、取消。

**读**：[FastAPI](https://fastapi.tiangolo.com/) → [LangGraph Durable Execution](https://docs.langchain.com/oss/python/langgraph/durable-execution) → [OpenTelemetry](https://opentelemetry.io/docs/)。

**做**：在独立项目给客服流程加 API/异步任务；故障注入：已提交退款却丢失回执。**负例**：同 Key 不同 Payload；SSE 断连被误判为任务取消。**验收**：以真实测试数据库与 Trace 证明没有重复写操作。

## Week 6｜Agent Evals、安全与观测

**学**：Task Success、Tool Name/Arguments Accuracy、Trajectory、正确拒答、恢复成功率、Token/Cost、P95；Prompt Injection、工具输出低信任、服务端权限和 HITL。

**读**：[Agent Evals](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) → [OpenAI Tracing](https://openai.github.io/openai-agents-python/tracing/) → [OWASP GenAI](https://genai.owasp.org/)。

**做**：先运行 [既有 19 个合成评测案例](labs/README.md)，再给独立真实环境构建冻结数据集，记录失败分母。**负例**：答案声称成功而 DB 未修改；引用了跨租户证据。**验收**：输出分指标报告，不能拿一个“准确率”替代全面结果。

## Week 7｜MCP、Skills、A2A 与 Harness

**学**：MCP Host/Client/Server、Tools/Resources/Prompts、协议版本；Skills 的资源组织；A2A 跨 Agent 互操作；运行 Harness 的隔离、状态、审计。

**读**：[MCP Spec](https://modelcontextprotocol.io/specification/) → [Agent Skills Spec](https://agentskills.io/specification) → [A2A](https://a2a-protocol.org/latest/) → [Harness 专项](AGENT-HARNESS-ENGINEERING.md)。

**做**：为合成只读工具创建测试 MCP Server，模拟恶意工具内容和越权请求。**负例**：工具返回要求系统提权。**验收**：说清 MCP 连接不等于 IAM，A2A 不是多 Agent 必需的本地编排框架。

## Week 8｜综合交付与陌生任务迁移

**学**：架构选型、基线、消融、回滚、版本和成本；真实任务的根因诊断与面试表述。

**做**：[三段递进项目](AGENT-PRACTICE-AND-EVAL.md) 中选一个独立实现并验证；完成 [24 题闭卷验收](AGENT-INTERVIEW-QUESTIONS.md)。**负例**：多 Agent 增加成本却无收益；CI 通过但业务不可用。**验收**：10 分钟架构讲解、失败 Trace、对照报告与陌生任务独立排障。

## 求职压缩路线与跨仓关系

时间不足先学 **Week 1 → Week 3 → Week 5 → Week 6 → Week 8**。Week 2/4 的必要概念按问题补齐，Week 7 先 L0/L1。与原训练模块按需连：工具调用看 [M02](../modules/M02.md)/[M06](../modules/M06.md)，Agentic RL 看 [M08](../modules/M08.md)（不是必须训练），评估看 [M10](../modules/M10.md)，延迟资源看 [M09](../modules/M09.md)/[M11](../modules/M11.md)。

本仓已覆盖 Harness、RAG、Context、Prompt、Ragas 的详细原理；本文件负责学习顺序和贯通，不制造重复的同义课程。**课程就绪 ≠ 已跑真实 Agent ≠ 学员通过 L2–L4 ≠ 生产系统可用。**
