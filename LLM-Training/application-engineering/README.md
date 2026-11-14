# 大模型应用工程专项｜RAG、Agent、Harness、Context、Prompt 与评测

> **定位**：这是 [V3 全栈地图](../knowledge-graph/LLM-FULL-STACK-ATLAS.md) 的应用层实践延伸，不是新设 M13–M20、替换 [M01–M12](../README.md)，也不是从本仓复制上游 [AI-Learning-OS](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS) 的完整市场/训练资料。原始实验、客户、职位事实保留在对应仓。本目录状态 **CURRICULUM_READY / REAL_APPLICATION_NOT_RUN / LEARNER_UNASSESSED**。

## 先分清七种东西

| 主题 | 专业定义与关注层 | 白话类比 | 进入专题 |
|---|---|---|---|
| Prompt Engineering | 提示词指令、输出格式、例子与行为约束的设计、版本、测试 | 给员工一份清楚的任务说明 | [Prompt](PROMPT-ENGINEERING.md) |
| Context Engineering | 每轮模型调用可见的上下文选取、组装、预算、维护、隔离、压缩 | 这次开会把哪些材料放上桌 | [Context](CONTEXT-ENGINEERING.md) |
| RAG | 推理时用检索召回证据并约束回答，模型权重一般不变 | 允许查最新手册 | [RAG](RAG-ENGINEERING.md) |
| Agent / Tool Use | 模型提出下一步动作，系统依据状态和权限真正执行工具 | 能提交申请的员工 | [Agent + Harness](AGENT-HARNESS-ENGINEERING.md) |
| Agent Harness | 包围模型的执行、状态、工具、安全、观察、恢复和评测环境 | 员工所在的工厂、流程和门禁 | [Harness](AGENT-HARNESS-ENGINEERING.md) |
| Ragas / Evals | 对 RAG 和 Agent 结果、轨迹、检索、证据、任务进行可重复评价 | 质检工位及考试卷 | [Ragas/评测](RAGAS-EVALUATION.md) |
| Project / Product / Production Engineering | 需求、契约、实现、发布、监控、回滚、成本与持续运营 | 把试验机器做成可靠商品 | [工程交付](PROJECT-PRODUCTION-ENGINEERING.md) |

**用词说明**：用户所说的 contact/protect engineering 本专项按常见的 **Context/Prompt Engineering** 建索引，同时单列 **Project/Product/Production Engineering** 以覆盖可能涉及的真实产品交付。Prompt、Context、Harness、RAG 与训练算法既有交集又不能相互替代；“lm-evaluation-harness”是评测框架名称，不等于执行 Agent 的 Harness。

## 一张关系图，同时看模型生命周期和应用调用链

~~~mermaid
flowchart TD
  T["M01–M08 数据/训练/后训练，亦可直接用现成模型 API"] --> M["可调用的模型"]
  P["Prompt：规则、指令、示例、输出契约"] --> C["Context：本轮输入组装+Token 预算"]
  R["RAG：可授权/新鲜证据与出处"] --> C
  S["会话状态/记忆/工具返回：受权限与来源约束"] --> C
  C --> M
  M --> H["Harness：调度、权限、工具、重试、状态与回放"]
  H --> K{"需要工具？"}
  K -->|"是"| A["服务端 ACL/审批/幂等→执行→观察"]
  A --> S
  K -->|"否"| O["最终输出/拒绝/证据"]
  O --> E["Evals：Ragas/Trace/Task Success + 负例"]
  H --> E
  E --> G["G0–G8 生产/版本/成本/回滚门禁"]
  G -.->|"新需求或真实缺口"| P
  G -.->|"确认需更新模型权重"| T
~~~

**注意方向**：RAG 只是可能提供 Context 的一部分；Context 不是单一 Prompt；Agent 是策略/决策+执行流程，Harness 是运行与约束环境；生产性能/安全需要服务端机制，提示词不能代替 ACL。最重要的边界参见 [交叉知识关系图](ROADMAP-RELATIONS.md)。

## 从问题入手，不用从头学

| 当前问题 | 首选路径 | 先别做什么 | 最短证据 |
|---|---|---|---|
| 引用编造/召回不足 | [RAG](RAG-ENGINEERING.md) → [Ragas](RAGAS-EVALUATION.md) | 直接 CPT/GRPO | Recall@k、支持的 Claim、拒答负例 |
| 内容太长、检索文档占满窗口 | [Context](CONTEXT-ENGINEERING.md) → [Prompt](PROMPT-ENGINEERING.md) | 盲目买更大上下文模型 | Token 预算、正确资料保留率、溢出率 |
| Agent 乱调用/越权/重复执行 | [Harness](AGENT-HARNESS-ENGINEERING.md) → [生产门禁](../production/PRODUCTION-READINESS.md) | 用“你必须安全”替代服务端检查 | 拒绝/审批/幂等/重放和 Trace |
| API 输出结构错或不听指令 | [Prompt](PROMPT-ENGINEERING.md) → [Tool SFT M06](../modules/M06.md) | 先训练模型 | Structured-output 合约与负例 |
| Ragas 分数高但结果仍错 | [Ragas](RAGAS-EVALUATION.md) → [M10](../modules/M10.md) | 只追单一 LLM Judge Score | 标注一致性、人工校准、任务正确率 |
| 要交付可用应用 | [Project/Production](PROJECT-PRODUCTION-ENGINEERING.md) | 只做 Demo、跳过权限和观测 | E2E + 性能成本 + Go/No-Go |

## 如何实操、如何核验

- [可运行离线教学 Lab](labs/README.md)：**纯标准库、合成数据、模拟决策**，演示分层 Context、Prompt、RAG、工具 Harness 与失败回放，不需要 API Key，不执行真实模型。
- [机器可读应用能力路由](index/application-engineering-index.json) + [验证器](tools/validate_application_engineering.py) 确保资源/前置/实验/上游回链都可定位。
- 真正学习 L2/L3 时必须替换模拟组件，固定模型/数据/工具 Revision，用真实允许执行的测试环境跑端到端，按 [唯一 Rubric](../assessments/CAPABILITY-RUBRIC.md) 收证据；不能以“资料有入口”冒充实际完成。

## 上游权威内容已经存在，不重复建设

| 专项 | 上游已有的操作与训练来源（固定 2026-11-14 Git SHA） |
|---|---|
| RAG | [市场驱动 RAG 路线](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/market/market-driven-rag-learning-loop.md) · [练习系统](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/practice/rag/README.md) |
| Prompt | [需求到实验](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/market/prompt-engineering-demand-to-practice-20261029.md) · [Rubric](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/assessments/ai-native-prompt-engineering-rubric.md) |
| Context | [课程与市场映射](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/market/context-engineering-demand-to-lab-20261029.md) · [上下文烟雾测试](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/labs/context-engineering-market-smoke-20261029/README.md) |
| Harness | [专项入口](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/HARNESS-ENGINEERING-LEARNING-20261029.md) · [验证沙箱](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/labs/harness-verification-sandbox-20261029/README.md) |

本仓只管理跨域关系和可复现的最小学习路径，上游仍是它自己的课程事实主权。

### 严格复验补充：冻结用例和正式评测边界

[19 条合成检索／工具回归测试](labs/README.md) · [固定评测用例](labs/benchmark_cases.json) · [可选 Ragas Faithfulness 脚本](labs/ragas_live_optional.py)。此处的 19 是基准案例数量，不是此前训练索引的 19 条需求；不新设第 11 条应用工程专题。
