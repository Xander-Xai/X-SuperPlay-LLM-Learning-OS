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

