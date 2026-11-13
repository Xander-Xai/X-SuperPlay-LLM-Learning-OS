# M10 全链路评估与严格验收协议

**适用范围**：Pretrain、CPT、SFT、DPO、GRPO、上线回归。训练成功 ≠ 模型能力提升。

## 1. 数据划分

- train / validation / final_test 应按文档源、任务模板、客户/工具场景或时间做去重与隔离；记录划分依据及哈希。
- validation 用于调参和选择 checkpoint；**final_test 不能反复用于调参**。
- 合成数据须检查与测试任务近重复、教师/验证器泄漏；禁止以真实业务敏感资料做公开样例。
- 固定推理模板、工具 schema、temperature/top_p/max_tokens 和模型 tokenizer 版本；随机生成任务应重复多次并报告波动。

## 2. 统一指标表

| 场景 | 主指标 | 辅指标 / 陷阱 |
|---|---|---|
| Pretrain | held-out CE / PPL / BPB | PPL 跨 tokenizer 不可直接横比；不同分词可看 BPB |
| CPT | 域内 CE/PPL + 通用 CE/PPL | 少数据容易假进步或遗忘 |
| SFT | Tool success / exact answer / instruction following | 训练 Loss 不等于真实任务成功 |
| Tool Call | schema valid、tool selection、argument accuracy、execution success | Schema 正确但工具/参数错误 |
| RAG | citation correctness、unsupported claims、answer quality | 引用存在不等于引用支持结论 |
| DPO | held-out pairwise preference win rate + correctness | Judge 偏差、答案长度偏好 |
| GRPO | held-out objective task success、reward、approx_kl、length、clip ratio | 奖励投机、熵塌缩、Reward 上升而正确率不升 |
| Serving | TTFT、p50/p95 latency、tokens/s、VRAM、error rate | 冷/热启动、并发、KV cache 不同 |

## 3. 最少必备对照

- 每个 experiment 记录 **No-training baseline** 与训练后；必要时加入同预算竞争方案。
- SFT 出发分别运行 DPO 与 GRPO，避免串联导致无法归因；串行实验单独标记。
- CPT 的数据配比、Scheduler 变量独立比较；不能在同组同时改多个关键因素。
- 随机性不可忽略；有预算时至少重复多个种子并给出区间，没有预算要明确是单次探索性结果。
- 对失败分类：幻觉、工具选择错、参数错、工具调用时机错、引用无效、格式错、拒答过度、Reward hacking。

## 4. 实验审计字段（硬性）

| 字段 | 举例 |
|---|---|
| 代码 | Git SHA + dirty status |
| 模型 | model id/revision、tokenizer id/revision、adapter |
| 数据 | snapshot/hash、划分策略、数量与 token 数、许可 |
| 环境 | OS/WSL、GPU、VRAM、driver、CUDA、torch、transformers、trl、peft 等 |
| 配置 | batch、grad accum、seq len、LR、scheduler、precision、seed |
| 结果 | 原始日志、OOM/异常、验证曲线、测试明细、成本 |
| 判断 | 证据事实 vs 推断 vs 建议 |

## 5. 正式验收门槛

- **白盒**：数据→Logits→Loss→Gradient→Update 能追踪，Mask 单测通过。
- **CPT**：Base/Domain/Replay 与调度器对照全部可追溯。
- **SFT**：不只看 demo，独立 Tool Calling / RAG 评测有数值。
- **DPO**：偏好数据来源、质量和离线/在线类型准确表述。
- **GRPO**：Reward 之外同时看正确率/长度/策略偏移，至少分析失败案例。
- **部署**：回归通过，吞吐/延迟/错误率/工具调用准确率都有数据。

没有真实运行证据时，必须标记 **NOT RUN / 待验证**，不得伪造 PASS。配套模板：[EXPERIMENT-TEMPLATE](../experiments/EXPERIMENT-TEMPLATE.md)。

