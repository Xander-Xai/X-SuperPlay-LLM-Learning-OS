# M08 Agentic RL 实验桥｜从多步工具轨迹到真实模型优化

> **状态：NOT RUN（真实 LLM Agentic RL）**。这是既有 **03 Agent Tool SFT + 05 GRPO** 的跨实验延伸，**不增加第 6 类训练实验**，不替换原 01–06；本目录没有生产订单工具、GPU Checkpoint 或真实训练精度。先完成 [标准库轨迹 Lab](../../labs/agentic-rl-trajectory/README.md)。

## 目标与边界

比较 A 冻结模型+Harness、B 工具轨迹 SFT、C 相同 SFT 起点经过环境 RL。证明的是**在可复位、独立评测的环境内，策略更新是否改善任务完成**，不是 Prompt/工具编排改变效果。只有基线有可学信号、奖励可靠且版本可复现时才运行 C。

### 流程与数据契约

\`\`\`text
train task ID + env seed + env snapshot
  → reset → policy(model/tokenizer/chat_template revision)
  → tool call(action tokens) → tool observation(non-policy tokens)
  → ... max_steps/done
  → trajectory: task_id/episode_id/actor_revision/tool_request_id
  → verifier: task_success + safety + cost + reward_components
  → [group advantage / KL if configured] → policy update → held-out test
\`\`\`

**最小 JSONL 契约示意**：字段结构因具体框架而异；训练前需将消息和 token spans 映射到安装版本的格式。

\`\`\`json
{"task_id":"train-order-001","episode_id":"ep-0001","env_seed":42,"policy_revision":"sha-of-policy","messages":[{"role":"assistant","tool_call":{"name":"lookup","args":{"order_id":"mock-1"}}},{"role":"tool","content":"mock-policy-check-required"}],"actions":[{"tool_name":"lookup","authorized":true}],"terminal":{"success":false,"unsafe_side_effect":false},"reward_components":{"task":0.0,"safety":0.0},"done_reason":"max_steps"}
\`\`\`

上例是**字段示意，非真实 rollout**。不得包含真实姓名、电话、订单号、密钥或未经脱敏的工具响应。工具结果不能作为 policy 需预测的 assistant target。

## 运行前五道门

1. **隔离**：可重置、幂等、无生产支付/退款/外网副作用，日志可撤销；高风险工具在执行层拦截。
2. **数据**：train/dev/test 按订单/用户/模板簇隔离，保存 snapshot hash；reward grader 不可读测试标签。
3. **策略基线**：保留相同 SFT checkpoint、tokenizer、tools、prompt、采样设置，B/C 资源预算匹配或注明不可比。
4. **技术兼容**：锁定 \`torch/transformers/trl/peft/accelerate\`、CUDA、模型 revision；根据当前 [TRL GRPO](https://huggingface.co/docs/trl/grpo_trainer) 文档核对 \`tools\`/\`environment_factory\`、组内同初始环境、Tool Message 前缀稳定性、Loss mask、Reference/KL、截断；不照搬示例参数。
5. **预检**：先采集不更新参数的 10–30 条轨迹，人工校验 reward、错误类型、重复执行和权限拦截；通过后才考虑小步更新。

## 三种方案的实验记录

| 组 | 模型/变化 | 验证内容 |
|---|---|---|
| A: Frozen | 冻结 SFT 模型 + 固定 Harness | 原始任务成功、错误工具调用、延迟/成本 |
| B: SFT | 从相同基线使用正确工具轨迹监督 | 轨迹模仿对成功率的影响 |
| C: Agentic RL | 从 B 同一 checkpoint，环境 Rollout + reward + policy update | 环境反馈的增益是否超过噪声/奖励投机 |

需要更严格比较时增加 D：相同预算的更多 SFT 数据/更多采样；避免把新增计算量误称 RL 的独占收益。

**记录**：task success、权限违规/实际副作用、拒绝正确率、调用次数、tokens、P50/P95 延迟、reward per-component、reward std、长度/截断、近似 KL/clip（如果框架产生）、显存峰值、seed、run ID。单一 reward_mean 不能视为“训练成功”。

## 小资源升级路线

1. 单机 CPU [Toy Lab](../../labs/agentic-rl-trajectory/README.md)：**小型表格 Q-learning** 确实更新策略；不含 LLM/GRPO。
2. 0.6B 级小模型 LoRA + 简单验证器：先用 [实验 05](../05-grpo/README.md) 证明真实 RLVR Loop（可能需要 GPU，本仓未跑）。
3. 有资源再添加可重置状态环境；使用当前 TRL 工具/环境接口，原生小批量运行并比较。
4. 研究 [Agent Lightning v1.0](https://github.com/microsoft/agent-lightning/blob/main/docs/README.md) 与 [verl](https://verl.readthedocs.io/en/latest/start/agentic_rl.html) 的异步/多机架构，先审接口，再决定是否迁移。

**16GB 风险**：长轨迹 KV、group 候选数、序列长度、梯度/优化器、Reference/Value、内存碎片都影响峰值；动态调整 batch/候选/长度，回退到离线轨迹和短序列。不得保证“单卡跑 Agent Lightning/verl 大模型”或固定训练成功率。

## 失败注入（至少五条有原始证据）

- 仅格式 JSON 正确但调用错误工具；
- 未核实政策直接请求退款（应被环境硬拦截）；
- 同组 reward 全等；
- 不同初始订单状态误分到同一 GRPO group；
- tool response 被误纳入 assistant loss；
- 超时重试导致重复执行；
- 训练 reward 升而 held-out 任务正确率降。

## 退出门槛与提交模板

- **L1**：解释 state/obs/action/reward/return、为什么 Agent 调用≠Agentic RL。
- **L2**：提供运行命令、代码 SHA、模型/数据版本、原始 rollout + 参数确实更新 + 测试。
- **L3**：A/B/C 公平对照、负例和错误分析，能识别 reward hacking 与系统问题。
- **L4**：新环境盲测迁移，安全门禁/真实 Go/No-Go 单独审查。

真实模型运行前后均按 [实验模板](../EXPERIMENT-TEMPLATE.md) 另存 run_id、日志与不可逆的测试集说明；未运行标记 NOT RUN。背景知识：[学习路径](../../reinforcement-learning/AGENTIC-RL-LEARNING-PATH.md) · [原始来源](../../resources/RL-AGENTIC-PRIMARY-SOURCES.md) · [训练与评估](../../evaluation/evaluation-protocol.md)。
