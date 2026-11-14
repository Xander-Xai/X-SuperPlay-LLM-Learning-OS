# 从“会训练/会调 API”到可上线能力：LLM 生产门禁

> **学习覆盖目标，不是本仓当前已上线产品的声明。** 没有真实授权产品时，可先用合成/公开 fixture 做生产环境模拟；通过模拟并不自动获得客户验收或生产 SLA。真正的业务指标、部署凭据和客户数据属于下游实际项目仓。

## 0. 先定义“上线”的含义

`docker compose up` 或 `vllm serve` 成功 ≠ 系统可上线。

**生产就绪至少包含**：正确性 + 安全/权限 + 性能/成本 + 可观测/恢复 + 可回滚 + 运维归责 + 用户实际验收。

先定义任务目标：功能、谁能访问、场景输入规模、可用性目标、P95、预算、风险等级和失败时允许怎样降级。没有业务证据时可定义教学 SLO，但标明 **SYNTHETIC**，不可声称满足真实客户 SLA。

## 1. Go/No-Go（每个场景适配，不能强制所有平台同一数值）

| Gate | 必须测什么 | 最少证据 | 典型失败 / No-Go |
|---|---|---|---|
| G0 需求与方案 | 规则/API/RAG/训练/自托管方案对比 | 原始需求 + 成本/性能 baseline + ADR | 为追新模型强行训练 |
| G1 数据与许可 | PII、版权/条款、训练/评估拆分、保留期限 | data card、样本 hash、敏感字段脱敏记录 | 未授权客户数据进公开训练集 |
| G2 任务正确性 | Task success、Tool args、Evidence support、拒答 | 冻结测试集、负例、错误分类 | 测试集泄漏、只测漂亮 demo |
| G3 安全与权限 | 认证/授权、越权 Tool Call、Prompt injection、机密 | 威胁模型、访问矩阵、注入/越权测试 | 低权限用户能读高权限证据 |
| G4 接口可靠性 | timeout、retry、幂等、SSE 中断、取消、故障恢复 | 集成测试、工具副作用去重证据 | 失败重试导致重复扣款/写入 |
| G5 性能/成本 | TTFT、E2E P95、tokens/s、VRAM、并发、单请求成本 | 固定环境压测配置与原始样本 | 只记录单条热缓存推理 |
| G6 运维可观测 | traces、指标、结构化日志、告警、错误关联 | trace ID→工具调用→模型输出 | 出错无法定位模型/检索/工具 |
| G7 变更与回滚 | model revision、tokenizer/chat template、索引版本、adapter | 发布清单、灰度/回滚演练 | 无法恢复上一个有效版本 |
| G8 使用反馈 | 合法用户反馈、漂移、失败采样、再训练闭环 | 反馈分类、再评估触发机制 | 将未经确认的反馈直接当标注 |

**禁止“一刀切 PASS”**：对于纯推理 API 服务，可以不做训练检查，但必须验证服务与工具边界；对于单机离线工具，可降低外网/高可用门槛，但仍需保障数据与正确性。

## 2. 不同能力验收切片

### A. RAG / 引用回答

```text
Authorized Query → Access Filter → Retrieval → Evidence Gate → Generation → Citation Check
                          ↘ 没证据 / 无权限 → 规范拒答
```

最小可测项：受限用户不可访问高权限 chunk；回答每一个关键断言都有支持它的 passage；文档版本变更后能失效旧引用；无证据时拒答而非编造。评估和应用路径可从上游 [RAG LAB](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/tree/main/docs/practice/rag) 查阅，不需要首先微调。

### B. 多轮 Agent / Tool Calling

```text
User Request → Tool Schema → Authorization → Function Call
    → Timeout/Retry/Idempotency → Observation → Final Answer → Audit
```

最小可测项：参数合法和业务语义合法是两种不同指标；写工具不能只验证 JSON 格式；敏感接口必须执行前权限检查。应具备重复请求防重、工具不可用时降级、可恢复事务/审批。模型输出“不执行”不构成系统级安全保证。

### vLLM 入口鉴权新增拒绝项（2026-11-14 官方核对）

**G3 强制安全项**：仅设置 vLLM --api-key 不能保证整站请求受保护；官方明确例举 /invocations 等不同于 /v1 的入口。自托管服务必须放到可控网络和统一反向代理/网关后，匿名请求测试应覆盖实际暴露的全部路径，而不只是 /v1。若测试环境存在未授权可调用推理的路径，标记 **NO-GO**。操作与原始来源见 [官方版本检查单](../resources/OFFICIAL-RUNTIME-DELTA-20261114.md)。

### C. 自托管模型/推理服务

- 验证服务协议及 `chat_template` / parser 与模型 revision 一致。
- 冷启动、热启动和并发/输出长度相同条件下对比 TTFT、E2E latency、throughput、error rate、显存。
- 限流、排队、OOM 降级、超长上下文拒绝/截断、请求取消。
- 灰度回滚演练：旧模型/adapter 与 tokenizer 同版本恢复，固定任务集正确性不回退。
- 提醒：量化/合并 adapter 可能更改质量；必须重复任务级回归。

### D. 自训练/偏好/RL 后模型上线

- Train/Val/Test 和 Synthetic/Teacher/Verifier 数据来源隔离。
- 公开模型许可、蒸馏/老师模型生成条款、训练数据许可核查。
- checkpoint、adapter、推理配置、reward config、训练 seed、数据 snapshot 可追溯。
- 与不训练的 Base/RAG/Prompt 方案**做同一评估**，新模型不优则可以拒绝上线。
- RL 需要额外检查 reward hacking、越权工具、长文本导致资源滥用、不同温度/采样的分布外表现。

## 3. 示例：端到端上线模拟测试协议

**已有可运行的任务评测教学纵切**：[合成任务级评测](../labs/task-evaluation/README.md) 显示指标分母、失败样本与不确定性；它没有真实模型/引用裁判，也没有测吞吐/P95。

**已有可运行的最小教学纵切**：[合成工具网关](../labs/synthetic-tool-gateway/README.md) 使用标准库实现白名单、角色授权、库存/引用验证、脱敏 trace 和负例；可从这里练习再添加真实 API、超时/幂等、模型输出、任务级评测。**该 Toy 没有部署/压测或真实 LLM，因此不是生产通过证据**。

**明确区分已实现与计划**：当前仓库已有的合成工具网关实际只有 **2 个虚构产品 A/B、2 篇合成证据 doc-A/doc-B**；另一个独立的任务评测 Toy 有 **16 条预标注虚构结果**。两者互不代表真实工具执行或生产延迟。**以下是尚未实现的扩展演练提案（NOT RUN）**：将两个虚拟工具扩展到 20 个虚构产品、20 篇证据文档，并另建 30 条固定任务。不得声称已经有 20/20/30 的执行日志。

1. 定义 30 条固定测试任务，分成：正常 10、无权限 5、过期证据 5、工具超时 5、错误参数/恶意输入 5。
2. 实现**零训练版本**：API 模型 + JSON schema + 只读沙盒、强制鉴权；记录基线。
3. 若证据显示可改进，再用 SFT/QLoRA 等训练；训练集与 30 条最终测试任务隔离。
4. 独立重跑 30 条测试，输出 selection/argument/execution/citation/拒答 5 类指标，另有 TTFT/P95、资源和成本。
5. 注入“非法工具调用”“返回敏感字段”“重复副作用”“超时后重试”负例，看系统是否安全拒绝/恢复。
6. 模拟发布 A→B，故意让 B 参数解析下降，再执行回滚；保留版本 SHA、测试结果和日志。
7. 记录 **No-Go 时的原因**，回流需求卡而不是为了完成课程而硬上线。

以上任务数据量**只是结构和工具链演练**，不能用于证明统计显著的生产准确率或真实负载 capacity；真实上线需要按风险、流量与业务另定样本/SLI。

## 4. 发布材料最小清单

```text
release/
  ADR.md                # 为什么选此方案，不使用更简单方案的证据
  model-manifest.json    # model/tokenizer/adapter/data/code SHA
  eval-summary.md        # 测试集划分、主指标、错误样本、置信限制
  perf-report.md         # hardware、concurrency、TTFT、P95、tokens/s、OOM
  threat-model.md        # prompt injection/permissions/tool execution
  runbook.md             # 启动、健康检查、限流、超时、故障与回滚
  rollback-evidence.md   # 真的演练过，不只是写了计划
```

**不要在学习仓放真实客户的日志、合同、密钥或生产数据**。若需保留，只链接经许可的脱敏证据或明确访问权限的项目仓。

## 5. 资料与回链

学习对应模块：[M10](../modules/M10.md)（评测） · [M11](../modules/M11.md)（推理） · [M09](../modules/M09.md)（性能/恢复） · [M06](../modules/M06.md)（工具微调） · [M02](../modules/M02.md)（数据和许可）。**定义什么叫“学会”**见 [能力 Rubric](../assessments/CAPABILITY-RUBRIC.md)，所有工程关键事实回到项目仓以原始证据核实。

