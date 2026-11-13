# Pretrain / CPT / SFT / DPO / PPO / GRPO：训练关系与决策表

这是 **M04–M08 交界知识**。训练阶段按目标定义；LoRA/QLoRA、量化、混合精度、FSDP 是实现或优化手段，不能作为等价训练阶段。

| 方法 | 初始化 | 数据/反馈 | 优化目标 | 常见产物 | 典型误区 |
|---|---|---|---|---|---|
| Pretrain | 随机/已有预训练进度 | 广域文本/代码 | 自回归 CE | Base model | Loss 下降就会指令跟随 |
| CPT / Midtrain | Base | 目标领域+通用混合语料 | 继续语言建模 CE | Domain-adapted base | 小预算就必然注入大量知识 |
| SFT | Base/CPT/Instruct | 指令+目标 assistant 输出 | 目标 token CE，常见 assistant-only mask | Instruct model | 将 tool observation 一并监督生成 |
| Reward Modeling | 通常 SFT backbone | 偏好对/反馈 | 训练奖励评分函数 | Reward model | 奖励评分即客观真实性 |
| DPO | 通常 SFT | chosen/rejected 数据 | 偏好对 log probability 目标 | 偏好优化模型 | 固定自采样数据一直是 on-policy |
| PPO-RLHF | 通常 SFT | 当前策略 rollout、RM/反馈 | 带优势估计及策略约束的 RL | RL 优化模型 | 把 KL、Critic 与 Reward 视为相同量 |
| GRPO/RLVR | 通常 SFT | 同题分组 rollout + 验证器 reward | 相对优势/策略目标（实现可变） | 强化学习优化模型 | Reward 变大必然代表能力变强 |

## CE 一样为什么仍是不同阶段？

对于 decoder-only，自回归训练通常以 `-log p(next_token | prefix)` 为基础。Pretrain 更重原始文本序列，CPT 更换语料分布与初始化，SFT 的目标是特定任务下的 assistant 行为，其监督范围、模板和评估标准不同。不能从“都用了 CE”推断“学到的能力相同”。

## 训练与工程手段的两个正交维度

- **训练目标**：LM loss、instruction CE、pairwise preference、policy optimization。
- **资源/更新方式**：Full parameters、LoRA、QLoRA、gradient checkpointing、量化、sharding、KV cache 优化。

同一个 SFT 目标可以用 Full 或 LoRA 完成；GRPO 也可以在 LoRA 参数上更新。因此不要把 QLoRA 画成 Pretrain→SFT 之间必须经过的阶段。

## 面试用场景判定

- 让模型学专业语料风格/术语并考察遗忘：先比较 CPT 与检索等方案。
- 让模型学会调用真实工具、使用正确 schema：SFT 数据与 Chat Template 优先。
- 让模型更偏好有证据、无幻觉的回答：构造偏好对考虑 DPO，仍以外部任务指标验证。
- 需要在环境中通过试错学多步动作：可研究 PPO/GRPO 等 RL；前提是环境及奖励可靠。

## 训练分支与对照

```text
同一 Base → [CPT domain / CPT replay / Base]  # 研究数据与遗忘
同一 Base → Agent Tool SFT checkpoint
                        ├─ DPO（静态偏好对）
                        ├─ GRPO（当前策略采样）
                        └─ 原 SFT 基线
最后独立比较，再视结果测试 DPO→GRPO 的串联。
```

资料：[Roadmap](../ROADMAP-V2.md) / [实验总入口](../experiments/README.md)。

