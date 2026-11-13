# M08 补足：PPO-RLHF、GRPO 与 RLVR 的技术边界

## 1. 经典 RLHF / PPO 训练链路

```text
SFT policy + preference pairs → reward model
policy 对 prompt rollout → RM 输出 reward
估计 advantage（如通过 value/critic）→ PPO clipped objective + 适当 KL 约束
参数更新 → 新 rollout → 外部任务评估
```

- `policy` 是回答生成分布，`reference` 常用于约束偏移。
- `reward` 是对完成结果的评价；`value` 估计未来回报；`advantage` 衡量相对期望效果；它们不能混为一谈。
- PPO clip 对策略比率进行裁剪，通常配合 KL、entropy、value loss 等，具体实现需按代码确认。
- Reward、采样策略、训练目标和外部评测器之间会出现偏差，可能导致 Reward Hacking。

## 2. GRPO

同一 Prompt 生成 K 个候选，用组内相对 Reward 构建 Advantage，通常省去独立 Critic 的开销。并不意味着不需要任何参考策略，是否加载 Reference / 使用 KL 取决于实现和 `beta`。16GB 实践见 [GRPO Playbook](grpo-16gb-playbook.md)。

## 3. RLVR 与 Agentic RL

- RLVR：通过可自动验证的最终结果（数学答案、代码测试等）构造奖励；不等同于“所有奖励都完全客观”。
- Agentic RL：状态、工具动作、环境观测、可回放轨迹和奖励归因更复杂；建议先在确定性沙盒做多步工具执行，再讨论真实 Agent。

## 4. PPO vs DPO vs GRPO：回答面试问题

| 对比 | PPO | DPO | GRPO |
|---|---|---|---|
| 策略在线采样 | 通常需要 | 离线 DPO 不需要，Online DPO 需要 | 通常需要 |
| 奖励反馈 | 经典为 RM + KL | 偏好对隐式目标 | 可验证奖励或评分 |
| 优势估计 | 常配 critic/value | 无显式 advantage | 组内相对 advantage |
| 主要成本 | policy/value/reward/rollout | 偏好数据、参考与更新 | rollout、多候选与更新 |

## 5. 练习

写出一个两候选 toy prompt 的 reward/advantage，对比当 `r=[1,1]` 与 `r=[1,0]` 时组内反馈的不同。阅读 [TRL PPO](https://huggingface.co/docs/trl/ppo_trainer)、[TRL GRPO](https://huggingface.co/docs/trl/grpo_trainer) 并指出实现选择与本概念图的差异。**验收**：不把 GRPO 的奖励提升当作真实能力提升证据。

