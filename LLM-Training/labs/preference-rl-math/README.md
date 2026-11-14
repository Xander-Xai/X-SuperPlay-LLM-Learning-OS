# DPO/GRPO 原理实验：能跑、能改、能发现奖励投机（无模型）

> **SYNTHETIC FORMULA LAB / NOT LLM TRAINING**。Python 标准库即可运行。只验证数值目标和偏好/奖励陷阱，没有 policy network、checkpoint、rollout 或训练循环。

## 一键运行

在仓库根目录：

```bash
python LLM-Training/labs/preference-rl-math/alignment_math.py
python -m unittest discover -s LLM-Training/labs/preference-rl-math -p 'test_*.py' -v
```

## 先学专业定义，再看大白话

- **DPO**：优化同一 prompt 下 chosen/rejected 的相对 *sequence log probability*（与 reference policy 对比），示例 `loss = softplus(-β·margin)`。直觉：不是要求“chosen 的概率一定达到某值”，而是比较相对优劣。
- **GRPO**：在同 Prompt 的 K 个候选内将奖励转换为相对优势；这是 policy optimization 的一个环节，不等于完整 GRPO 训练。直觉：班内全员同分时没有区分信号。
- **Reward Hacking**：目标奖励（如带 `<answer>` 格式）和真正任务正确性（如答案 4）不一致时，模型可能学会错误捷径。

## 自己动手的 4 步

1. 把 DPO 的 policy chosen logp 从 -3 改为 -1.5，看同一 reference 下 loss 怎样变化；若 chosen/rejected 长度不等，讨论为何需固定可比的 token logp/长度协议。
2. 把组奖励从 `[0,1,1,0]` 改为 `[0,0,0,0]`；解释 zero variance group 为什么没有有效相对信号。
3. 制作只奖励 JSON/格式的坏验证器：让错误答案得高分，再用真正计算结果的验证器纠偏。
4. 改变 epsilon / beta，写一份假设→输出→原因→失败边界记录，不把 toy 成功写成真实模型精度改善。

## 下一阶段升级（实际 GPU/环境执行后才计）

- [04 DPO 训练方案](../../experiments/04-dpo/README.md)：真实偏好数据、SFT checkpoint、TRL DPO 与固定测试集。
- [05 GRPO 训练方案](../../experiments/05-grpo/README.md)：真实 Rollout、Reward/Advantage/Policy Update 与独立验证。
- [能力 Rubric](../../assessments/CAPABILITY-RUBRIC.md)：本 Lab 最多提供部分 L1/L2 证据，不能证明已掌握训练或上线。

## 原始可信来源

[DPO 原论文](https://arxiv.org/abs/2305.18290) · [DeepSeekMath GRPO](https://arxiv.org/abs/2402.03300) · [TRL GRPO 实现](https://huggingface.co/docs/trl/grpo_trainer)。示例的标准差采用**总体标准差**；TRL 不同版本、优势归一化与 KL 配置可能不同，必须读自己的版本源码。

