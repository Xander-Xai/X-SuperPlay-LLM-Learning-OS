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
 
**严格说明（2026-11-14 审计修订）**：这里的 Context Budget 仅是**检索材料的空白分隔代理成本**，不计算 System Prompt、Tool Schema、历史或预留输出；真实 Token Budget 必须用目标 Tokenizer 全量计算。样例的 `system/user/tool` 列表只演示信任角色边界，**不是可直接提交给任意 API 的完整 Tool Calling 消息序列**（常需 Assistant Tool Call / Tool Call ID）。Idempotency Key 在真实系统里必须由受信身份、租户和业务操作共同确定，不能从用户自报角色判断身份。模拟工具的 actor_id 也不是已认证用户。

## 复验新增：固定数据集驱动的完整离线评测

此前的 20 项单测可证明局部函数的条件，但缺少逐条输入/期望/结果和分母的版本化评测。现新增：

~~~bash
python LLM-Training/application-engineering/labs/evaluate_benchmark.py
python -m unittest discover -s LLM-Training/application-engineering/labs -p 'test_*.py' -v
# Ragas 脚本默认绝不联网
python LLM-Training/application-engineering/labs/ragas_live_optional.py
~~~

- [19 条固定合成用例](benchmark_cases.json)：10 个检索/拒答案例，9 个工具/权限/幂等案例，均有 ID、失败类别、Gold/期望工具结果；
- [可重放基准程序](evaluate_benchmark.py)：独立统计正例 Recall@k、无证据时拒答、未授权材料、工具结果与副作用；错误时返回非零退出码，附带 failed_ids 和 failed_families；
- [回归反例测试](test_evaluate_benchmark.py)：故意更改预算、Gold 文档 ID、Expected Inventory，必须明确报错或判失败；
- **不会混淆的指标**：Recall@k 只对有 Gold 的正例计算。没有 Gold 的用例归入拒答，不塞入 Recall 分母。此处并未评估语言模型回答的 Faithfulness、事实正确率或真实任务完成率。

### 可选运行真实 Ragas Faithfulness（会使用外部模型，CI 不执行）

先在专用环境中按 [Ragas 官方 collections Faithfulness 文档](https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/faithfulness/) 安装兼容的 ragas 与 openai；在本地配置你授权使用的 OPENAI_API_KEY 后，执行：

~~~bash
python LLM-Training/application-engineering/labs/ragas_live_optional.py --live --model gpt-4o-mini
~~~

脚本只发送一条合成问答和一条允许公开的人工固定证据给实际 LLM Judge；可能产生费用。模型与 API 可用性需按实际账户确认。缺失 --live 或 API Key 时直接退出，绝不自动调用。**此项并未在用户环境或 CI 中真实运行，因此没有真实 Ragas 分数。**
