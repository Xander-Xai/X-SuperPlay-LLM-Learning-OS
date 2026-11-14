# 实验 05 — 16GB 单卡 GRPO / RLVR

**状态：NOT RUN**。从与 DPO 相同的 SFT Checkpoint 分叉；先实现原生 TRL 的小模型可验证奖励闭环。

**开始前的无 GPU 演练**：[GRPO Group Advantage / zero-variance / 奖励投机](../../labs/preference-rl-math/README.md)。该练习没有策略更新，真实实验需另行执行。

## 阶段

- [ ] 从简单算术或确定性任务抽取训练/held-out，先测模型原始正确率。
- [ ] 在更新策略前校验多候选 Rollout、Reward、group variance、优势估计。
- [ ] LoRA + 短序列/micro batch 1 + num_generations 2–4 做最短训练运行，遇到 OOM 则降 token 或退回更小模型。
- [ ] 完成 SFT vs GRPO 固定评测，记录 reward、accuracy、response_length、clip、近似 KL（若存在）、显存、耗时。
- [ ] 分析至少 5 条奖励投机/失败轨迹；检查“仅输出格式不输出正确答案”的情况。
- [ ] 可选：Unsloth、vLLM colocate 与原生方案对照，必须完整注明版本及兼容性。

**不可提前声称**：16GB 必定小于 10GB 占用、一定数倍加速、一定提升准确率、一定出现 CoT 自然增长。RL 复杂度/时长受实际条件影响。

专题：[GRPO 低显存 Playbook](../../reinforcement-learning/grpo-16gb-playbook.md)。


## 可选进阶：多轮 Agent 环境（非新编号实验）

完成简单可验证的 GRPO/RLVR 真正训练后，再依据 [Agentic RL Bridge](../agentic-rl-bridge/README.md) 把 rollout 扩展到可重置的多步工具环境。其 [CPU 标准库沙盒](../../labs/agentic-rl-trajectory/README.md) 只是 Tabular Q-learning 教学，不可记录为本实验真实 GRPO PASS；训练资料见 [权威来源表](../../resources/RL-AGENTIC-PRIMARY-SOURCES.md)。

## 真实模型最小代码入口（2026-11-15）

在 CPU 数学实验之后，按照 [小模型 SFT→GRPO 可选实操](../mini-posttrain-sft-grpo/README.md) 做数据/Reward 测试、SFT adapter 继续 GRPO、held-out 评测和结果记录。该演示是**单轮可验证算术任务**，训练脚本未实际在 CUDA 跑通，且不等于 Agentic RL 多步环境。正式任务必须根据 [实验模板](../EXPERIMENT-TEMPLATE.md) 用实测日志更新状态。
