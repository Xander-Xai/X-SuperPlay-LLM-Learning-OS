# 实验导航：一个底层主线 + 一个真实模型主线

> **所有实验当前状态：NOT RUN（仅创建学习与执行手册，未声称执行）。**

| ID | 目的 | 入口 | 必须交付 |
|---|---|---|---|
| 01 | MiniMind 白盒 Pretrain→SFT、多轮 Loss Mask | [01](01-minimind-whitebox/README.md) | 代码、训练曲线、Mask 测试、Checkpoint |
| 02 | Qwen CPT 防遗忘及 WSD/Cosine | [02](02-qwen-cpt-replay/README.md) | 3 组 CPT+基线、独立调度器对照 |
| 03 | Agent Tool-Calling 合成数据与 Full/LoRA/QLoRA SFT | [03](03-agent-tool-sft/README.md) | 数据版本、基线、微调对照 |
| 04 | DPO：外部 vs 自采样偏好 | [04](04-dpo/README.md) | DPO 分支、评估与误差分析 |
| 05 | GRPO：16GB 低成本可验证奖励 | [05](05-grpo/README.md) | Rollout/Reward/Accuracy/KL/长度等指标 |
| 06 | 系统工程 / vLLM / Agent 部署 | [06](06-deployment/README.md) | Profiler、部署回归与系统架构图 |

## 运行顺序与分叉

~~~mermaid
flowchart LR
  Mini[01 MiniMind] --> CPT[02 CPT]
  CPT --> SFT[03 Agent SFT]
  SFT --> DPO[04 DPO branch]
  SFT --> GRPO[05 GRPO branch]
  DPO --> Deploy[06 Deploy + Compare]
  GRPO --> Deploy
~~~

**注**：02 的 CPT 以同一 Qwen Base 为起点作诊断实验，不必把 CPT 结果串联到 03；03 可以直接从原始 Base 做 SFT。04/05 均从同一个经过验证的 SFT Checkpoint 分叉。

## 运行前通用检查

- [ ] 固定 commit / 模型 revision / tokenizer / 数据 hash。
- [ ] 已定义正确的 Train/Val/Test 切分，并验证不泄漏。
- [ ] 明确本次唯一主要实验变量和可比预算。
- [ ] 记录 CUDA/GPU、Package 版本、训练显存上限。
- [ ] 已预注册主要指标和失败类型。
- [ ] 使用 [模板](EXPERIMENT-TEMPLATE.md) 填写 run_id、实际日志与结论。

本仓库不自动下载模型/数据，避免意外显存、流量或存储消耗；任何真实运行需单独执行和记录。

