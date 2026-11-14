# 2026-11-14 严格复验：RAG / Ragas / Agent Harness / Context / Prompt

> **目的**：对用户明确关切的应用工程缺口进行仓库事实审计、官方资料核对、索引补齐与 CI 回归。不是凭空设立 M13–M20，也不是将上游市场资料搬到下游。**本报告在写入时不预填 PR 成功/测试数字**；验收以 PR 最新 SHA 对应 GitHub Actions 为准。

## 1. 起点及实际缺失

- 连接 GitHub 查看下游 LLM-Learning-OS 主分支 `dcd3e06761c8335ddddb49067dffba460c4df71d`、111 个 Git 文件（原有 12 模块、90 基础概念、六域 33 主题、训练 19 需求、25 来源），以及上游 AI-Learning-OS 主分支 `59ea4e509507378860519d165113e21a9a9eb4d7` 的 841 份 Git 文件（固定提交的递归树可能列出更多对象，计数仅针对本次实时 main 查看）。
- 下游六域 Atlas 里有 RAG/Agent/MCP、工具网关、任务级离线 Toy，但缺少完整且可检索的独立 **Context Engineering、Prompt Engineering、Agent Harness、Ragas** 的学习/评测路线；机器训练索引里几乎没有这些词的直接需求入口。
- 上游其实已有成体系专项：[RAG](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/practice/rag/README.md)、[Context](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/market/context-engineering-demand-to-lab-20261029.md)、[Prompt](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/market/prompt-engineering-demand-to-practice-20261029.md)、[Harness](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/HARNESS-ENGINEERING-LEARNING-20261029.md)，都有历史研究/练习状态但不能冒充学习者或生产已完成。
- 用户语音的 “contact engineering” 暂按业界 **Context Engineering**， “protect engineering” 按 **Prompt Engineering**；为避免漏掉 Project/Product/Production 可能性，同时补入技术交付手册。不要把用户拼写当作官方术语。

## 2. 本轮官方资料抽样（2026-11-14）

| 来源 | 支撑的结论 | 不证明什么 |
|---|---|---|
| [Anthropic Context](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) | Prompt 是指令，Context 包含检索、工具、记忆、历史等动态信息；控制上下文质量 | 我们已实现真实 LLM 的记忆压缩 |
| [OpenAI Prompt](https://developers.openai.com/api/docs/guides/prompt-engineering) | Prompt 设计需要测试、代码版本和结构化输出 | Prompt 保证工具授权 |
| [Google Agent Harness](https://cloud.google.com/discover/agent-harness) / [OpenAI Harness](https://openai.com/index/harness-engineering/) | Harness 涵盖工具/状态/运行/质量闭环，也可指 agent-first 软件工程环境 | 两种用法完全等同或都已上线 |
| [Ragas 指标](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) / [Quickstart](https://docs.ragas.io/en/latest/getstarted/quickstart/) | RAG 与 Agent 评测的 Precision/Recall/Faithfulness/Tool Call 等维度 | Toy 离线 Recall 就是 Ragas LLM-Judge 分数 |
| [OpenAI Agents SDK Testing/Tracing](https://openai.github.io/openai-agents-python/testing/) | Trace/Testing/Guardrails 是可靠 Agent 的重要组成 | 现有离线 Lab 已接入 Agents SDK |
| [LangChain Learn](https://docs.langchain.com/oss/python/learn) | RAG、Context、Deep Agents、多智能体课程可按需参考 | 框架版本/依赖/硬件已自动兼容 |

## 3. 本次交付与统一维护规则

- 新建 [应用工程专项](application-engineering/README.md)、[关系图](application-engineering/ROADMAP-RELATIONS.md) 以及六个技术细节指南：RAG、Context、Prompt、Harness、Ragas、Project/Production。
- 新建 **10 条应用工程横向专题 / 55 个核心实践点** 的 [机器索引](application-engineering/index/application-engineering-index.json)，每项带本仓讲义、实践入口、专业资料、上游固定 SHA、对应 M 模块，状态统一 `CURRICULUM_ONLY / NOT_RUN_REAL_MODEL_OR_PRODUCTION`。
- 新建 [无网络合成纵切](application-engineering/labs/README.md)，分开演示权限过滤/上下文预算、工具调用与幂等、步数/Trace、Source ID 召回代理指标。代码**没有 LLM 推理、Ragas Judge、持久数据库或真实沙箱**。
- 连接根 README、V3 Roadmap、六域 Atlas、上游资源地图、按需任务入口、索引、生产 G0–G8；原 M01–M12/90 词条/33 主题/19 训练需求不被重编号。
- 新增必要文件检查、应用索引合同/非法状态/无效路径/缺上游固定 SHA 负例、Prompt vs Context/RAG vs Ragas/Harness vs Eval Harness 区分、离线运行与安全负例的 CI 测试。

## 4. 本轮必须验收的项目

1. 下游原 111 文件保留，新增文件可在 GitHub 当前 HEAD 读取；上游固定 SHA 所有新引用路径真实存在。
2. `check_repo.py` 相对 Markdown 链接与 REQUIRED 无误。
3. `validate_application_engineering.py` 成功：10 条专题、M 模块关系、来源/上游固定 SHA、资料路径、状态不虚报；其他原有两个索引检查无回归。
4. `test_pipeline.py` 的全部合成负例（ACL/跨租户/恶意文本不当高权限指令/幂等/工具范围/Step Limit/指标分母）通过；**不等于模型抵御 Prompt Injection、真实 Ragas Eval 或生产安全**。
5. 原有 CPU TinyGPT/Shift Mask 与基础知识 QA 和所有学习文档 CI 继续 PASS。
6. 不在检查全绿前合并；合并后必须复读 main SHA/README/实验/索引/本报告。

## 5. 未完成的真实能力与未来按需任务

- 使用真实 Provider/Model 的 Prompt A/B、Ragas 评委评分与人工标注对齐 **NOT RUN**。
- 真实 Agent 的持久 Checkpoint、HITL、工具服务器 Auth、MCP 兼容、沙箱和网络攻击测试 **NOT RUN**。
- RAG 的 OCR/Embedding/Hybrid Retrieval/多租户 ACL 与跨版本 Eval/生产压测 **NOT RUN**。
- 真实产品上线/客户验收、成本 SLO 和持久回滚演练 **NOT RUN**。此项属于具体产品仓的记录，不应伪造进学习仓。

**建议下次学习**：由一个当前障碍进入 [应用工程路由](application-engineering/index/README.md) → [官方/上游资料](application-engineering/README.md) → [模拟负例](application-engineering/labs/README.md) → 真实模型/授权工程环境 → [Rubric](assessments/CAPABILITY-RUBRIC.md) + 有生产要求时 [G0–G8](production/PRODUCTION-READINESS.md)。
