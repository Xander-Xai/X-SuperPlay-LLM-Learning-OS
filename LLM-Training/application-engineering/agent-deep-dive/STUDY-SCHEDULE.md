# Agent 8 周学习计划、执行策略与前三天操作手册

> 八周是参考节奏，不强制按日历逐章打卡。优先处理真实工程问题，达标停止。既有 [L0–L4](../../assessments/CAPABILITY-RUBRIC.md) 仍是唯一评分体系；生产上线独立经过 G0–G8。

## 学习时间怎么分配

- 每天建议 **150 分钟**：官方文档+原理 30 分钟、编程和实验 70 分钟、失败注入/Trace 30 分钟、闭卷复盘 20 分钟。实践中可每天 2–3 小时。
- 跨模块投入比例建议：**底层原理 20% + 框架/编排 25% + 生产工程 30% + 评测与项目复盘 25%**。这是按知识领域的分配，和每天按活动划分时间是**两个不同维度**。
- 每个专题形成「问题 → 官方资料与版本 → 基线 → 最小代码 → 两类负例 → 固定对照 → 原始日志 → 结论边界 → 闭卷」的证据卡。不用阅读篇幅和打卡数冒充 L2–L4。

## 原始求职 P0 / P1 / P2 知识优先级

| 级别 | 专题 | 为什么 |
|---|---|---|
| P0 | Agent Loop / Function Calling | 基础运行机制 |
| P0 | LangGraph State / Checkpoint / Interrupt | 核心项目的恢复语义 |
| P0 | 工具幂等 / 容错 / 异步架构 | 区分 Demo 和真正可靠服务 |
| P0 | 多 Agent 编排与架构选型 | 解释 Router / Supervisor 的取舍 |
| P0 | Tracing / Agent Evals | 用数据证明成功、成本和安全 |
| P1 | Memory / Context Engineering | 稳定长任务和长对话 |
| P1 | MCP / Agent Harness | 扩展工具及运行时能力 |
| P2 | A2A / Computer Use / 高级自主规划 | 按具体岗位拓展 |

**Computer Use** 是在受控浏览器/桌面上观察界面、操作鼠标和键盘并核验结果的 Agent 能力；不是 MCP、A2A 或 Harness 的同义词。优先保证沙箱隔离、敏感数据与凭据权限、域名限制、审计。参考 [Anthropic 官方](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool) / [OpenAI 官方](https://developers.openai.com/api/docs/guides/tools-computer-use)。

## 八周进度表

| 周 | 优先级 | 主要知识 | 当周交付 | 可核验退出条件 |
|---|---|---|---|---|
| W1 | P0 | Message、Function Calling、Agent Loop、ReAct、Stop | 原生 Python Mini Agent | 解释工具决策/执行，负例和超限均正确 |
| W2 | P0 | Tool Schema、并行调用、错误回传、Planning、Context | 3–5 工具助手 | 合法 JSON 仍不可越权，异常分桶 |
| W3 | P0 | LangGraph State/Node/Edge/Reducer/Command/Send/Interrupt/Checkpoint | 可中断/恢复客服图 | 真实框架版本下测试状态与重放 |
| W4 | P0 | Memory、Agentic RAG、Router、Supervisor、Handoff | 单/多 Agent 对照 | 固定数据/工具/模型与成本，结论可解释 |
| W5 | P0 | FastAPI、SSE、Celery/Worker、Redis、PostgreSQL、幂等 | 异步任务与故障恢复服务 | 写入成功丢回执不会重复退款 |
| W6 | P0 | Trace、Evals、Task Success、Cost、P95、Prompt Injection | 冻结案例评测报告 | 报结果/轨迹/业务状态/失败分母 |
| W7 | P1 | MCP、Skills、A2A、Sandbox、Harness、长任务 | 只读 MCP 与长任务 Harness 操作方案 | 外部工具输出不会获得授权 |
| W8 | P0 | 项目重构、消融、系统设计、面试口述 | 工程仓库+面试材料 | 陌生任务独立排障、10 分钟完整解释 |

**求职压缩路线**：W1 → W3 → W5 → W6 → W8。W2 工具授权/Context 和 W4 多 Agent 选型按遇到的具体问题补齐；W7 的 A2A/Computer Use 暂时不必深入。选择最简可用架构，达标停止。

## Day 1：Agent Loop 从原理到实验（150 分钟）

1. **00–30**：阅读 [HF Agents Unit 1](https://huggingface.co/learn/agents-course/unit1/introduction) 与 [OpenAI Function Calling](https://developers.openai.com/api/docs/guides/function-calling)，手画 User → Assistant ToolCall → Gateway → Tool Result → Assistant Final；标明每一步谁负责、哪些内容可信。
2. **30–100**：从仓库根目录运行：

~~~bash
python LLM-Training/application-engineering/labs/mini_agent_loop.py
python -m unittest discover -s LLM-Training/application-engineering/labs -p 'test_mini_agent_loop.py' -v
~~~

3. **100–130**：把 max_steps 改为 1、未知工具、错误 order_id 类型分别执行。记录 step_limit、UNKNOWN_TOOL、INVALID_ARGS，验证不会在 Tool Error 后冒充退款成功。
4. **130–150**：闭卷说明 Agent vs Workflow、Function Calling 的执行边界、ReAct。保存流程图、测试输出和两个负例。

**交付**：一张执行链路图、能跑的原生 Python 实验、异常日志。今天不要求接真实大模型。

## Day 2：Tool Design、Planning 与 Context（150 分钟）

1. **00–30**：读 [Anthropic 工具设计](https://www.anthropic.com/engineering/writing-tools-for-agents)，设计 lookup_order、search_knowledge、request_refund（前二只读，后一需审批和幂等）的字段与输出契约。
2. **30–100**：扩充/复用 [工具网关合成实验](../labs/README.md)，加可信 tenant/actor、参数校验、超时错误返回和操作预算；单独对比固定 Workflow 与 Agent 动态选择。
3. **100–130**：三个负例：跨租户 order_id、恶意知识库内容要求写入、同键不同 payload；记录真实状态和 Tool Trace。
4. **130–150**：解释 Prompt/Context/Harness 区别、计划器与 ReAct 的取舍。

**交付**：3 个工具 Schema、错误/ACL 测试、上下文预算表。真实 API 仅在愿意承担成本的情况下使用 [可选协议实验](../labs/REAL-LLM-OPTIONAL.md)。

## Day 3：穿透式复盘多智能体客服（150 分钟）

1. **00–30**：画现有客服架构的真实证据与未知项，涵盖 API、SSE、Router、LangGraph、专业 Agent、Celery、Redis、PostgreSQL、Trace 和 HITL。没有代码证据的结构标「待核实」。
2. **30–100**：用虚构退款任务说明：身份在哪里进入？何时路由？模型何时提出 ToolCall？Gateway 怎样鉴权？审批何时 Interrupt？业务 DB 怎样更新？最终输出怎样校验？
3. **100–130**：注入「退款已成功但 HTTP 回执丢失」「审批恢复重复」「SSE 断线」；按模型/工具/权限/运行时/外部服务分桶归因。
4. **130–150**：30 秒自述、3 分钟技术追问、10 分钟端到端讲解，并保存图与证据。

**交付**：一张架构图、一张时序图、正常和异常 Trace 设计。只写流程不等于实际业务已通过。

## 后续每天的停止规则

每次只选 1–3 个最小前置；固定变量跑实验；至少两类失败输入；保存版本、命令、原始日志，能闭卷解释后才升级 Rubric。已有仓库分级为 **L0 定位、L1 机制理解、L2 独立实现、L3 受控诊断、L4 陌生任务迁移**。原文「知道→理解→实现→工程」是通俗描述，不能机械把其 L1–L4 映射为仓库 L1–L4。生产能力另经 [G0–G8](../../production/PRODUCTION-READINESS.md)。
