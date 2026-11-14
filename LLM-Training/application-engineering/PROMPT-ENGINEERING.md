# Prompt Engineering｜可版本化的指令与输出契约，不是“魔法咒语”

**专业**：通过任务定义、消息角色、必要上下文、Few-shot 示例、输出 Schema、失败处理与固定测例，设计稳定的模型行为。**大白话**：不是喊“你是全世界最聪明的 AI”，而是写一份可执行、可验收的工作说明。

## 1. 结构化 Prompt 不是万能模板

一份可维护的生产 Prompt 应标注：

- **身份/目标**：模型要解决什么问题，哪些场景不需要回答；
- **任务输入**：用户请求和动态参数，通过有类型/经过验证的变量注入；
- **受信指令与低信任资料**：不能把外部 PDF、网页、工具文本提升为系统指令；
- **决策边界**：哪些情况调用工具、哪些必须拒答/澄清/请求人工审批；
- **输出协议**：JSON Schema/严格字段/缺失值/引用要求，不要只靠“请返回合法 JSON”；
- **样例**：少量多样化的正例/负例；不要无限堆模板；
- **版本/指标**：文件名、SHA、模型 Snapshot/Revision、数据集版本、准确率/成本/P95 对照。

在代码中把 Prompt 当可测试的应用逻辑。**2026 年 OpenAI 官方文档**建议采用版本化代码和有类型参数；新的集成不应依赖已宣布淘汰的旧式可复用 Prompt 对象。具体 API 变更以发布时官方文档为准：[OpenAI Prompting](https://developers.openai.com/api/docs/guides/prompting) 与 [Prompt Engineering](https://developers.openai.com/api/docs/guides/prompt-engineering)。

## 2. 六种常用手段

| 技术 | 什么情况下用 | 反例/边界 |
|---|---|---|
| 明确目标与约束 | 输出含糊、角色/格式不对 | 任务目标不清时给再多角色词也没用 |
| Few-shot | 输出结构/边界样例多样 | 演示样本泄漏到独立测试 |
| Structured Outputs | 消费端有固定 Schema | JSON 合法≠数据库写入有权限 |
| Tool Calling Instructions | 工具选择/参数/幂等规则 | 模型指令不能代替网关实际授权 |
| Prompt Versioning | 迭代模型或上线更新 | 改了 Prompt 同时改模型/数据不能归因 |
| 失败与拒答规则 | 无证据、风险或授权不足 | 模型自信拒答不等于服务端保护 |

**不要强制模型展示私有思维链**；需要诊断时要求简短决策依据、证据或结构化可观测字段。Prompt 优化是**实验迭代**，不是输出越长越好。

## 3. 最小需求驱动对照

问题：“查某产品库存，按 product_id、quantity、as_of 输出 JSON”。先做 Rule/SQL/API baseline；确定 Prompt v1/v2 的不同变量、约定服务端 Schema Validation、权限及工具异常。固定不少于一组正常/越权/缺货/数据缺失/恶意工具返回负例；分别统计正确参数率、拒绝/澄清率、JSON validity、越权率、延迟/Token。

从 [离线应用纵切 Lab](labs/README.md) 看指令与非可信资料如何隔离，再迁移到真实 LLM 的 Structured Outputs。教学代码无法证明真实模型会遵守这些规则。

**相关学习**：[M02 Tokenizer/Template](../modules/M02.md) → [M06 Tool SFT](../modules/M06.md)（可选）→ [Agent Harness](AGENT-HARNESS-ENGINEERING.md) → [Eval](RAGAS-EVALUATION.md)。[上游 Prompt 需求与 Rubric](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/market/prompt-engineering-demand-to-practice-20261029.md)。
