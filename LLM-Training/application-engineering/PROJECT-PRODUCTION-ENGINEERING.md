# Project / Product / Production Engineering｜从演示到能长期使用的 AI 产品

> 本页同时回应可能称为 “Project Engineering / Product Engineering” 的工程交付问题；**这不是把“Prompt Engineering”替换成产品经理学科**。与本仓学习工程的分工：这里是技术验收入口，具体 PRD、市场、成本、客户与业务决策保留对应产品/OPC 仓。

## 1. 六步交付链

1. **发现需求/不训练基线**：用户、工作流、约束、数据授权、成功标准。先对照纯规则/SQL/FAQ/API，证明需要 LLM/RAG/Agent。
2. **行为契约与数据契约**：用户输入、模型输出 Schema、Tool 参数类型、权限、失败与拒答、文档版本/来源。
3. **薄纵切 MVP**：先完成**一个有真实测试集的端到端工作流**，而不是增加工具数量；Prompt/Context/检索/工具执行/网关/模型分层可替换。
4. **离线与在线评测**：准确率/证据/Tool Success/成本/延迟/安全/可用性；有对照数据，失败加入回归集；不以几个成功 Demo 判断上线。
5. **发布/恢复**：身份和租户权限、秘密管理、限流/预算/观测/告警、版本与回滚、审批和事件审计，关注用户数据保留与合规。
6. **反馈/演化**：用户反馈经过合法脱敏进入评测/产品改进；明确什么时候改 Prompt、RAG、Harness、模型权重，避免无证据的重训。

## 2. 哪些事应在哪层做？

| 需求 | 首选责任层 | 为什么不是直接调 Prompt |
|---|---|---|
| 输出字段验证 | API/schema + deterministic validation | LLM 可能格式正确却语义错误 |
| 私有文档访问 | Retriever、Gateway、DB 的 ACL | 模型文字不具鉴权权限 |
| 用户要求写/删数据 | Tool + HITL + Idempotency + Audit | Prompt 不能保障事务一致性 |
| 服务时延预算 | Queue/Model Serving/Context Budget/Cache | 模型指令不改变 GPU 负载 |
| 引用与事实对齐 | Retrieval/Evidence Gate/Answer Validation | 没找到证据时写得再好也不真实 |
| Long Running / Resume | Harness Checkpoint + Event Log | Chat Summary 不等于持久事务状态 |
| 功能变更 | CI + Eval + Canary + Rollback | Prompt 版本变更可能破坏旧样本 |

## 3. 发布证据包（G0–G8 同口径）

- G0：用户任务与免训练 Baseline；
- G1：数据来源、授权、许可与保留；
- G2：正例/负例/拒答/工具参数的可复核功能；
- G3：工具/数据库/检索 ACL、攻击面、Prompt Injection 边界；
- G4：Retry/Idempotency/超时/失败恢复；
- G5：固定负载下 TTFT/P95、吞吐、并发与费用上限；
- G6：脱敏 Trace、监控、报警与事故回放；
- G7：Release/版本/灰度/回滚；
- G8：用户真实反馈、保留与持续学习闭环。

**本仓 [生产门禁](../production/PRODUCTION-READINESS.md) 为唯一 G0–G8 标准**；本页只是引用，避免发明第二套不一致的验收。真实产品未在此仓发布，状态 **LEARNING_ONLY / NO_REAL_DELIVERY_EVIDENCE**。

官方资料：[OpenAI Harness Engineering](https://openai.com/index/harness-engineering/) · [OpenAI Agents SDK Testing](https://openai.github.io/openai-agents-python/testing/) · [LangChain RAG/Agents](https://docs.langchain.com/oss/python/learn) · [OWASP GenAI Security Project](https://genai.owasp.org/)。
