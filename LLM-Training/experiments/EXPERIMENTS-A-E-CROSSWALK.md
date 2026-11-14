# 用户提出的五个实战实验 A–E 与现有 01–06 的对应关系

> 这是**覆盖矩阵**，不是另造 5 个互相竞争的训练仓，也不是按字母必须依次完成的课表。相关代码及训练结果依然以对应目录为准；没有自己的真实模型日志时，实验 01–06 仍保留 NOT RUN。

| 用户实验 | 当前仓库可执行/规划入口 | 训练性质与关系 | 关键真实验收 |
|---|---|---|---|
| **A 手写最小 GPT** | [新增 TinyGPT CPU](../labs/tiny-gpt/README.md) + [现有 Shift/Mask](../labs/README.md) | 教学小模型；真实 PyTorch 参数更新，合成字符语料，**不等同 MiniMind Pretrain** | Causal Mask、张量、Loss/Gradient/AdamW、训练 Batch 下降、负例与临时 Checkpoint |
| **B MiniMind Pretrain → SFT** | [实验 01](01-minimind-whitebox/README.md) / [固定版本实操](01-minimind-whitebox/RUNBOOK-FIRST-DAY.md) | 必须实际在相应环境跑 Pretrain/SFT 才算 | Base+SFT 可加载权重、训练与独立验证、固定 Prompt、恢复状态 |
| **C CPT / SFT / LoRA / QLoRA** | [实验 02 CPT](02-qwen-cpt-replay/README.md) + [03 Tool SFT](03-agent-tool-sft/README.md) | 两种**不同训练目标**，不能把 CPT 的评测当成 SFT；LoRA/QLoRA 是更新策略 | Base+RAG 基线、CPT+Replay 消融、Tool SFT 标签掩码、资源/任务对照 |
| **D SFT → DPO** | [实验 04](04-dpo/README.md) + [偏好数学 Toy](../labs/preference-rl-math/README.md) | 偏好优化从验证过的 SFT 权重分支；DPO ≠ 必须 PPO 后才能做 | Pair 质量、β、Reference、WinRate、独立 E2E |
| **E GRPO / RLVR** | [实验 05](05-grpo/README.md) + [Reward 数学 Toy](../labs/preference-rl-math/README.md) | 先无模型 Reward/Group Advantage，再按资源执行在线 Rollout/Policy Update | Reward、独立 Accuracy、KL（如启用）、长度/截断、OOM/吞吐、Reward Hacking |
| **扩展：工程与上线** | [实验 06](06-deployment/README.md) + [G0–G8](../production/PRODUCTION-READINESS.md) | 不是第六个训练阶段；可基于未训练的 API / RAG / Agent 进行 | P95、权限、正确率、版本/监控、回滚和成本 |

## 开始任何实验前的共同检查

1. **先选一个真实或合成问题**，检查规则/Prompt/API/RAG 免训练基线能否完成；本学习仓不绑定单一下游产品。
2. **同预算受控比较**：记录模型权重 Revision、Tokenizer、Chat Template、训练和验证数据 Hash、算法参数、设备、CUDA/PyTorch 版本；只改一个关键变量。
3. **训练目标别混淆**：Pretrain/CPT 是下一 Token 预测，SFT 是指定 Assistant 输出监督，DPO 是偏好相对概率目标，GRPO 属奖励引导的策略优化。Distillation 可能跨阶段，Quantization 是精度/资源手段。
4. **每个实战至少留**：原理卡、源码/可运行代码、真实运行日志、独立结果对照；并加一个负例、失败回退。
5. **严格状态**：课程文件存在是 DESIGN_ONLY/NOT RUN；CPU Toy 在 CI 通过只说明 Toy 合同可复现；没有真实 MiniMind/Qwen GPU 实验日志就不能升级训练结果。

## 16GB 单卡资源策略（建议、非兼容性承诺）

- TinyGPT 的 CPU Toy 可以先不占 GPU；MiniMind 采用固定上游版本、mini 数据、短序列小 Batch。
- Qwen3-0.6B Base 用于实际模型 LoRA / QLoRA 及 CPT/SFT 教学；真实显存和依赖版本要实测，不能假设 1.5B 总是可完整 RL 训练。
- GRPO 的 Rollout、Actor、Reference（如存在）、Reward/Verifier、KV Cache 等会**同时或分阶段**占显存；先小模型短生成/低并发，必要时云端 GPU，再谈 vLLM/verl。
- 不要误把官方 MiniMind 低成本演示复现为“在任何 16GB 设备都 2 小时训练完成”，数据范围、硬件和配置不可直接套用。

**官方入口**：[MiniMind](https://github.com/jingyaogong/minimind) · [Qwen3-0.6B Base](https://huggingface.co/Qwen/Qwen3-0.6B-Base) · [TRL](https://huggingface.co/docs/trl/index) · [Stanford CS336 2026](https://cs336.stanford.edu/)。
