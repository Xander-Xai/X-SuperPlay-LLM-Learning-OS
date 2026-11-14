# 训练学习资源角色分工｜四个主资源与专项按需查

> **资料角色是降低重复劳动的策略，不是课程必须按顺序读完的规定。** 本仓 [原有权威书目](../papers/READING-LIST.md) 已经包含这些资源的大部分，本表补充“发生什么问题就读哪个源码/哪份官方文档”，与 [六域知识 Atlas](../knowledge-graph/LLM-FULL-STACK-ATLAS.md) 对齐。

## 四条最优先的主线，各司其职

| 主线 | 解决什么 | 大白话 | 何时进入 |
|---|---|---|---|
| [Stanford CS336 2026](https://cs336.stanford.edu/) | 数据/Tokenizer/Transformer、训练系统/Kernel、Scaling、数据过滤、SFT+Reasoning RL；5 组重实现作业 | “大学完整实验课”：解释为什么及如何量化 | 想知道深层原理，或遇到源码/算子性能盲区 |
| [MiniMind 官方](https://github.com/jingyaogong/minimind) | 轻量 Pretrain、SFT、LoRA、DPO、PPO、GRPO 等训练入口，具体能力以当前 upstream 为准 | “自己的小型训练车间”：从数据到权重贯通 | 要亲自跑小模型训练、对照 Base/SFT |
| [Raschka LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) | Attention/GPT/梯度、从零 PyTorch 实现细节 | “把机器盖子拆开” | 看不懂 QKV、Loss、shape 或模型内部 |
| [Karpathy nanochat](https://github.com/karpathy/nanochat) | 训练数据、Base/SFT/RL、评估与推理组织的端到端工程参考 | “看成熟的小工厂怎样布置工位” | MiniMind 能复述主流程后，按需理解项目组织 |

原则：底层训练只保留 MiniMind 一条主要外部执行主线；本仓 TinyGPT 只是很小的教学复现，不再额外完整造一套 GPT 项目。nanochat、LitGPT 与 Raschka 是**按需参考，不要求把它们全部跑一遍**。

## 专项资料的实际使用条件（只补足已有索引遗漏/歧义）

| 遇到的问题 | 优先资料 | 实际检查 |
|---|---|---|
| Tokenizer/BPE、Datasets | [HF LLM Course](https://huggingface.co/learn/llm-course/en/chapter6/1)、[HF Datasets](https://huggingface.co/docs/datasets/index) | Special Tokens、Padding/Packing、Train/Test 泄漏 |
| 预训练数据过滤、去重 | [DataComp-LM 官方项目](https://github.com/mlfoundations/dclm) | 注意官方仓库是 **mlfoundations/dclm**，不要沿用未核验的其他拼法 |
| 训练框架和参数管理 | [LitGPT](https://github.com/Lightning-AI/litgpt) | Pretrain/Continued Training/Finetune 设计；不强制另起模型训练 |
| SFT/DPO/GRPO/PPO | [TRL](https://huggingface.co/docs/trl/index)、[HF smol-course](https://github.com/huggingface/smol-course)、[Alignment Handbook](https://github.com/huggingface/alignment-handbook) | 当前版本数据格式、Mask、Reference、奖励配置 |
| 高效微调 | [PEFT](https://huggingface.co/docs/peft/index) | Rank、Target Modules、量化训练与 Merge 风险 |
| DP/TP/PP/CP/EP | [NVIDIA Megatron Core Parallelism Guide](https://docs.nvidia.com/megatron-core/developer-guide/latest/user-guide/parallelism-guide.html) | GPU 数/通信、内存、Layer/Sequence/Experts 各自切分的维度 |
| FSDP2/ZeRO | [PyTorch FSDP2](https://docs.pytorch.org/docs/main/distributed/fsdp.fully_shard.html)、[DeepSpeed ZeRO](https://www.deepspeed.ai/tutorials/zero/) | 参数/梯度/优化器状态和通信，DDP ≠ 参数分片 |
| 训练能力随 checkpoint 变化 | [EleutherAI Pythia](https://github.com/EleutherAI/pythia) | 比较固定训练中间检查点的 PPL/指标，**不表示你已重训 Pythia** |
| LM 评估和污染 | [LM-Evaluation-Harness](https://github.com/EleutherAI/lm-evaluation-harness) | 任务定义、Prompt 配置、解码、样本重复与污染 |
| 低显存 GRPO | [Unsloth 官方 RL 指南](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide) | 显存/吞吐/依赖均需实际测试，绝不承诺本机一定跑通 |

## 最易搞混的训练算法

| 主题 | 核心公式或机制 | 通俗解释 |
|---|---|---|
| Pretrain / CPT | 自回归负对数似然；CPT 从已有 Base 权重继续训练 | 从零学语言规律 / 有基础后专修某类知识 |
| SFT | 对指定目标输出的交叉熵，支持 Assistant-only Loss | 老师教规范做事，必须先圈对“谁的作业算分” |
| LoRA / QLoRA | 低秩可训练更新，量化基座 + 适配器不是新阶段 | 用较少可调零件修改技能 |
| DPO | 结合参考策略对 chosen/rejected 的相对 Log Probability | 比较两份答案偏好，不等同真实任务正确 |
| PPO / GRPO / RLVR | PPO/GRPO 是优化策略，RLVR 是可验证 Reward 机制 | 多次实践按得分调整策略；奖励不是事实真相 |
| Distillation / Quantization | 教师迁移 / 量化节省显存或计算 | 模仿成熟员工技能 / 压缩存储和计算精度 |

[完整 12 模块](../README.md) · [六域 Atlas](../knowledge-graph/LLM-FULL-STACK-ATLAS.md) · [版本风险卡](OFFICIAL-RUNTIME-DELTA-20261114.md)。
