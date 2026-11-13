# GRPO / RLVR 单卡 16GB 实操手册（M08）

## 目的与执行原则

学习在线 Rollout → Reward → Advantage → Policy Update → Eval 的闭环，而非承诺一张 16GB 显卡能跑任何规模的 RL。第一次实验优先选 0.6B 模型、简单可验证任务；只有基线能部分解决任务，奖励才能提供有效区分。**首要验收是正确的训练流程与可解释指标，不要求 Reward/Accuracy 必须上升**。

## 1. 核心概念

| 术语 | 大白话 | 技术意义 |
|---|---|---|
| Rollout | 让模型现场答题 | 基于当前策略生成 completion |
| Reward | 自动打分或环境反馈 | correctness、schema、执行成功等 |
| Group | 同题多答 | 用同一 Prompt 的候选形成比较 |
| Advantage | 比同组平均表现好多少 | 估计更新方向；具体算法有变体 |
| KL | 与参照策略偏移多少 | 控制策略漂移；不是每个配置都启用 |
| Clipping | 限制过激更新 | 策略比率裁剪与稳定性 |
| Reward hacking | 钻评分规则漏洞 | 高 Reward 不代表任务成功 |

常见简化优势：A_i=(r_i-mean(r_group))/(std(r_group)+eps)。**只是概念化公式**；实际 TRL/GRPO 各实现对归一化、长度处理和 clipping 可能不同。

## 2. 三层执行方案

| 层次 | 操作 | 何时升级 |
|---|---|---|
| A：最低风险 | TRL 原生，LoRA，短 prompt/completion，micro-batch 从 1 起，先不用 vLLM | 训练流程、日志与 baseline 稳定 |
| B：低显存 | 测试 Unsloth + TRL 的兼容组合；重新测显存和吞吐 | A 能跑且希望优化效率 |
| C：高吞吐 | 探索 vLLM colocate、sleep/standby 等模式，检查权重同步 | B 有余量并确认 CUDA/版本兼容 |

**推荐起点，不是保证能运行的配方**：Qwen3-0.6B、num_generations 2–4、prompt 256–512 tokens、completion 128–256 tokens、micro-batch 1、LoRA rank 8/16。根据 OOM 或模型无效回答降低长度/候选数，必要时回退到 MiniMind 小模型。

任何“显存 <10GB”“Rollout 占 70%”“加速数倍”都必须在本机带环境/配置实测后才能写进报告。vLLM 的 GPU 内存使用量、参考模型、KV Cache、反向传播激活共同决定峰值，不能只估权重大小。

## 3. 奖励设计

建议阶段：
1. 先做可严格检查的小规模算术或固定答案任务。严格答案匹配规则和输出格式奖励分开记录。
2. 再做模拟工具调用：可验证 JSON schema、工具选择、参数正确、执行成功、回答证据正确。
3. 最后讨论 Agentic RL：多步环境、工具延迟、环境状态、轨迹级/步骤级 Reward 和 credit assignment。

Reward 必须防投机：例如“只要输出 JSON 就给高分”会诱导模型忽略正确性。采用 held-out 的外部评测器检验真实性。

## 4. 必须记录的指标

- Train: reward_mean / per-component reward、approx_kl（若适用）、clip_ratio、grad_norm、ratio、学习率、loss。
- Rollout: output_length、truncation、group reward std、生成延迟、tokens/s、GPU 峰值。
- Eval: 独立任务 accuracy / tool execution / citation validity、平均输出长度与错误类别。
- 版本: TRL/Transformers/PEFT/Unsloth/vLLM/PyTorch/CUDA、模型 revision、seed、数据快照。

**重要配置细节**：部分 GRPO 配方默认 beta=0，可能未启用显式 reference KL，报告应按实际配置记录，不能假定 KL 永远非零。

## 5. 任务拆解与验收

- [ ] 单条 Prompt 生成 K completion，打印奖励与分组。
- [ ] 不更新参数时验证 rollout 和 reward 正确性。
- [ ] 小步训练并保存训练/验证日志，检查 NaN/OOM。
- [ ] GRPO vs 同起点 SFT baseline 的独立测试集对比。
- [ ] 至少手动分析 5 个失败/奖励投机样本。
- [ ] 可选：Unsloth/vLLM 与原生方案的吞吐/显存对照。
- [ ] 说明不确定性，不能仅用几百步实验宣称推理能力提升。

参考：[TRL GRPO](https://huggingface.co/docs/trl/grpo_trainer) · [Unsloth RL](https://docs.unsloth.ai/get-started/reinforcement-learning-rl-guide) · [DeepSeekMath](https://arxiv.org/abs/2402.03300)。详见 [05 GRPO 实验](../experiments/05-grpo/README.md)。

