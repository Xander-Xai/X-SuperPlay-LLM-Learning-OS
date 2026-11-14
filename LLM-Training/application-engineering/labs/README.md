# 离线教学纵切：Prompt → RAG Context → Scripted Agent → Harness → Eval

**状态：SYNTHETIC_CPU / NO LLM OR RAGAS.** 本实验只依赖 Python 3.11 标准库，固定 6 条虚构文档、模拟库存、纯字符串检索；没有 Embedding、BM25、真实 Tokenizer、模型推理、联网、数据库事务、Ragas Judge、真正用户数据或 OS 沙箱。

## 命令（仓库根目录）

~~~bash
python LLM-Training/application-engineering/labs/pipeline.py
python -m unittest discover -s LLM-Training/application-engineering/labs -p 'test_*.py' -v
~~~

## 分层代码与真实能证明什么

| 文件/函数 | 机制 | 可验证证据 | 不能证明 |
|---|---|---|---|
| synthetic_documents.json | 6 份合成资料：公开、隐藏、跨租户、失效、恶意提示词文档 | 数据和负例可复核 | 真实 OCR/Chunk/Embedding 的检索准确率 |
| select_context() | Tenant + Role + Active 过滤、基于词项重叠排序、预算选取 | 不把未授权文档放进上下文；结果有 Source ID 和预算 Manifest | 真实 Token/复杂语义召回、不可绕过的安全鉴权 |
| prompt_messages() | 分离 system/user/tool，保留低信任文档来源 | 文档不会在**此教学组装函数**中变成 system 指令 | 真模型一定不会被 Prompt Injection 影响 |
| ToolGateway.execute() | 固定 allowlist、Schema、Tenant、Admin Approval、Idempotency key、Trace | 负例中未知工具/越权/重复副作用被阻止 | 真正跨服务身份、持久事务、分布式幂等 |
| scripted_agent() | 预写 ToolCall 的步数循环 | Trace、最大步数、成功/失败事件 | LLM 自主计划、记忆、恢复、在线 Agent 策略 |
| recall_at_k() | 已定义 Gold Doc IDs 的确定性 Top-k 命中率 | 指标公式、分母和权限数据一致 | Ragas Faithfulness/上下文相关性的模型评分 |

## 四个必做对照

1. **预算**：60 vs 10 个空白分隔代理单位，观察上下文 Manifest 中保留了哪些授权文档；注意“单位”不是模型 Token。
2. **数据泄漏/权限**：同问题对 Viewer/Admin/Other Tenant 改角色，检查 A-Secret/A-Cross-Tenant/A-Old 是否出现。
3. **Prompt Injection**：A-Untrusted 包含“忽略指令、调用写工具”；代码只将其作为 tool 消息供观察，并未自动执行。真实模型必须再加独立注入/权限/工具测试。
4. **Harness 重放**：Admin 先审批 Reserve，再用相同 Key 重放，不改变第二次库存；同 Key 不同单位触发冲突；低权限用户绝不能写库存。

## 下一步从教学走向真实评测

选择一个真实/脱敏授权任务，固定 Data/Model/Tokenizer/Prompt/Tools 版本，替换 Lexical Stub 为 BM25/Hybrid + 权限检索；真实模型仅能提议 ToolCall，服务端再次鉴权；加持久 Checkpoint/审批，再用 [Ragas](../RAGAS-EVALUATION.md) 和 [生产 G0–G8](../../production/PRODUCTION-READINESS.md) 进行独立验收。

**注意**：这 20 个 CPU 单测不是“真实 RAG/Agent 或权限安全评估通过”。只代表确定性教学合同和分层关系在给定合成 fixture 下成立。
