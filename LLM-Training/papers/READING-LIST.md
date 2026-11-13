# 权威学习资源与论文索引（按需求查，不要求全读）

> 学习时以原项目 README/官方文档**当前版本**为准；GitHub main 分支和框架 API 可能调整。第三方项目是参考资源，不复制其代码或数据到本仓库。

## 四个主要学习源

| 资源 | 唯一职责 | 入口 |
|---|---|---|
| MiniMind | 底层源码唯一实战主线，Pretrain→SFT→其他后训练 | https://github.com/jingyaogong/minimind |
| Stanford CS336 | 预训练、Scaling、GPU、数据、系统和对齐理论 | https://cs336.stanford.edu/ |
| Raschka, Build a Large Language Model From Scratch | 张量维度、Attention、PyTorch 细节按需查 | https://github.com/rasbt/LLMs-from-scratch |
| nanochat | 最后学习端到端训练项目组织，不与 MiniMind 同时复现 | https://github.com/karpathy/nanochat |

## 分模块工程资料

| 模块 | 入口 | 看什么 |
|---|---|---|
| M01–M04 | https://huggingface.co/learn/llm-course/chapter1/1 | Tokenizer/Trainer/LLM 基础 |
| M02 | https://github.com/mlfoundations/dclm | 数据过滤、混合、模型与语料关系 |
| M04–M05 | https://github.com/Lightning-AI/litgpt | 预训练、continued pretrain、训练效率 |
| M06 | https://huggingface.co/docs/peft/index | LoRA/QLoRA |
| M06–M08 | https://huggingface.co/docs/trl/index | SFT/DPO/GRPO/PPO 与 Trainer |
| M06–M08 | https://github.com/huggingface/smol-course | 后训练教学与练习 |
| M06–M07 | https://github.com/huggingface/alignment-handbook | 对齐配方 |
| M09 | https://docs.pytorch.org/docs/stable/distributed.fsdp.fully_shard.html | FSDP2 |
| M09 | https://github.com/NVIDIA/Megatron-LM | 分布式模型并行 |
| M08–M09 | https://github.com/volcengine/verl | 工业 RL Rollout/Actor/Reference |
| M08–M09 | https://github.com/OpenRLHF/OpenRLHF | 工业 RLHF 工程 |
| M10 | https://github.com/EleutherAI/lm-evaluation-harness | 基准评估 |
| M11 | https://docs.vllm.ai/en/latest/ | 推理引擎 |
| M08 / 16GB | https://docs.unsloth.ai/get-started/reinforcement-learning-rl-guide | 低显存 RL 方案 |
| Qwen 模型 | https://huggingface.co/Qwen/Qwen3-0.6B-Base | 基线模型卡 |
| Qwen 工具 | https://qwen.readthedocs.io/en/latest/framework/function_call.html | 工具调用序列化 |

## 推荐论文阅读顺序（问题 → 论文 → 源码）

1. Transformer 与 Attention: [Attention Is All You Need](https://arxiv.org/abs/1706.03762)。问题：自注意力和因果遮挡为什么能做序列预测？
2. RoPE: [RoFormer](https://arxiv.org/abs/2104.09864)。问题：位置如何进入 Query/Key？
3. Scaling: [Training Compute-Optimal Large Language Models (Chinchilla)](https://arxiv.org/abs/2203.15556)。问题：参数、token 数与 FLOPs 如何权衡？
4. 优化与高效微调: [LoRA](https://arxiv.org/abs/2106.09685) / [QLoRA](https://arxiv.org/abs/2305.14314)。问题：哪些权重更新？为什么省显存？
5. RLHF: [InstructGPT](https://arxiv.org/abs/2203.02155)。问题：SFT→奖励模型→PPO 的历史训练方案。
6. 偏好对齐: [Direct Preference Optimization](https://arxiv.org/abs/2305.18290)。问题：如何从 chosen/rejected 直接优化？
7. GRPO: [DeepSeekMath](https://arxiv.org/abs/2402.03300)。问题：组内优势为何可替代独立 Critic？
8. Reasoning RL: [DeepSeek-R1](https://arxiv.org/abs/2501.12948)。问题：可验证奖励、冷启动与多阶段训练有什么区别？
9. 训练系统: [FlashAttention](https://arxiv.org/abs/2205.14135) / [ZeRO](https://arxiv.org/abs/1910.02054)。问题：瓶颈在 IO、参数状态还是通信？

## 每篇论文只要完成的六个问题

**问题/背景 → 方法和关键假设 → 一个核心公式 → 对应代码 → 资源代价 → 适用边界**。论文中的公开结论不能不经实验直接移植成自己机器上的确定性能数字。

若发现失效链接：在文档更新中记录原 URL、可用替代 URL、检查日期，不默默删除来源。

