# LLM Training Roadmap V2.0 — 完整训练底座（保留，已拓展 V3）

**状态：学习体系文档已落盘；模型训练待执行。**

**重要：这份 V2 是保留的学习底座；当前以 [V3 需求驱动扩展路线](ROADMAP-V3-DEMAND-DRIVEN.md) 为入口。V3 不删改 12 模块/4 里程碑/5 类实验，只让学习顺序取决于当前问题，并覆盖生产能力。**

**学习中心：[12 模块导航](README.md) · [预训练/后训练对照](knowledge-graph/pretrain-posttrain-relations.md) · [CPU Toy Shift/Mask](labs/README.md) · [验收报告](ACCEPTANCE-V2.md)。** 更新：2026-11-14。

## 0. 学习目标与方法

目标是独立解释和复现 **文本数据 → Tokenizer → Transformer → Pretrain →（可选 CPT）→ SFT → 偏好对齐 / 强化学习 → 评估 → 压缩部署 → Agent 应用**。不是顺序阅读所有论文，更不是机械跑几条 Trainer 命令。

- **主线一：MiniMind**。在同一代码库中理解 RoPE、RMSNorm、SwiGLU、Attention、Pretrain、SFT；不重复新建完整的大模型训练框架。本仓另有 [极小 TinyGPT CPU 教学 Toy](labs/tiny-gpt/README.md)，只验证基础 Attention/Loss/Optimizer，不与 MiniMind 竞争真实训练主线。
- **主线二：Qwen3-0.6B-Base + Transformers/PEFT/TRL**。做 CPT、防遗忘、Tool SFT、DPO、GRPO 对照。不同训练阶段尽量使用同一个初始模型和规范化数据。
- **辅助：CS336** 是理论和系统设计参考；**Raschka** 用于张量和数学薄弱点；**nanochat** 留到最后精读。
- **训练阶段 ≠ 训练技术**：Pretrain/CPT/SFT/DPO/RL 是目标/流程；LoRA/QLoRA/量化是降低训练或推理成本的技术。
- **评估从第一天开始**，并将事实、实验推断和观点分开标注。

## 1. 十二模块及优先级

| 模块 | 需要理解与验证的核心点 | 优先级 |
|---|---|---|
| [M01 数学和 PyTorch](modules/M01.md) | 张量、链式法则、Autograd、CE、AdamW、混合精度、显存 | P0 |
| [M02 数据与 Tokenizer](modules/M02.md) | BPE、清洗、去重、Packing、抽样、分布、数据泄漏 | P0 |
| [M03 Transformer](modules/M03.md) | Causal Attention、RoPE、RMSNorm、SwiGLU、GQA、KV Cache | P0 |
| [M04 Pretraining](modules/M04.md) | Next-token CE、Batch/Seq、优化器、LR、Scaler、Checkpoint、Scaling Laws | P0 |
| [M05 CPT / Mid-training](modules/M05.md) | 领域继续训练、Replay、防遗忘、调度器对照 | P1 |
| [M06 SFT + PEFT](modules/M06.md) | Full SFT、LoRA、QLoRA、多轮工具调用、Mask、合成数据和拒绝采样 | P0 |
| [M07 Preference](modules/M07.md) | 偏好对构造、DPO、Reward Model、Online DPO、外部/自采样比较 | P0 |
| [M08 RL](modules/M08.md) | PPO、GRPO、RLVR、Rollout、Advantage、KL、奖励投机 | P0 |
| [M09 Training Systems](modules/M09.md) | 显存、Profiler、FlashAttention、DDP、ZeRO、FSDP、TP/PP/CP/EP、verl | 基础 P0 / 进阶 P1 |
| [M10 Evaluation](modules/M10.md) | PPL、BPB、任务准确率、工具调用、数据泄漏、消融与回归 | 贯穿 P0 |
| [M11 Distillation / Serving](modules/M11.md) | 蒸馏、量化、Adapter 合并、vLLM、吞吐和延迟 | P1 |
| [M12 Advanced](modules/M12.md) | MoE、长上下文、多模态、Agentic RL、test-time compute | P2 |

**历史 V2 学习深度标签（非当前统一等级）**：V2 将 L1=解释、L2=实现/调试、L3=推导/消融；当前 V3 的唯一规范为 [L0 定位→L1 理解→L2 实现→L3 诊断/比较→L4 陌生迁移](assessments/CAPABILITY-RUBRIC.md)，**旧成绩不可机械换算**。M01–M04、M06–M08 至少 L2；其余按需求 L1/L2。

## 2. 四个里程碑（灵活 5–7 周，不是强制进度）

| 阶段 | 聚焦 | 必须产出 | Go/No-go |
|---|---|---|---|
| 一：白盒化底座（1–2 周） | MiniMind 模型结构、训练循环、Pretrain→SFT、多轮 Mask | 可运行 Checkpoint、Tensor 形状记录、Mask 测试、显存估算 | 不能解释一个 Batch 的前向、损失与更新则不算通过 |
| 二：真实模型与数据（1–2 周） | Qwen CPT 领域/Replay 对照、Cosine/WSD、Full/LoRA/QLoRA、合成工具轨迹 | CPT 对照表、数据版本、工具调用基线及 SFT 报告 | 仅模型能回答几个演示问题不算通过 |
| 三：偏好与 RL（约2周） | SFT→DPO 与 SFT→GRPO 分支，最终可测试串行组合 | DPO 偏好对照、GRPO 奖励/准确率/KL/长度曲线 | 不能仅凭 Reward 上升宣布成功 |
| 四：系统和部署（约1周） | Profiler、DDP/FSDP/ZeRO 原理、verl、nanochat、vLLM/Agent | 显存报告、架构解释、端到端调用及回归测试 | 仅服务端成功启动不算通过 |

推荐时间分配：**45% 代码/实验、25% 原理/论文、20% 诊断/复盘、10% 表达/知识整理**。工作或面试提出新问题时，可通过 [依赖图](knowledge-graph/concept-dependencies.md) 跳学。

## 3. 五项调整如何体现在行动中

1. **减少重复**：MiniMind 唯一底层实操主线；Raschka 按需查；nanochat 末期精读；不同时维护 MiniMind 与独立 TinyGPT 两套重复实现。
2. **SFT 数据工程前置 P0**：任务模板、教师生成、事实/工具验证、拒绝采样（同题 N 候选择优）、去重、人工抽检、训练集拆分。
3. **Agent 数据前置 P0**：assistant(tool_call)、tool(observation)、assistant(final) 多轮序列；验证 assistant-only mask；优先复用 Qwen 官方 chat/tool template。
4. **CPT 改为诊断防遗忘**：Base、100% Domain、80/20 Domain+General；不同调度器另做实验；比对通用与领域数据分布。
5. **GRPO 低显存分级**：原生 TRL 最简跑通 → Unsloth 对照 → vLLM colocate/其他方案；单卡不保证低于 10GB、不保证训练收益。

## 4. 从业务需求反查学习专题

| 如果当前需要… | 直接进入 | 补齐的依赖 |
|---|---|---|
| 讲清 LoRA/QLoRA | [高效微调](sft-peft/lora-qlora-full-sft.md) | 梯度、线性层、量化、显存 |
| 看懂 Pretrain Loop | [白盒实验](experiments/01-minimind-whitebox/README.md) | Tokenizer、CE、Attention、AdamW |
| 改进 RAG/Agent Tool Calls | [多轮 SFT](sft-peft/agent-tool-calling-loss-mask.md) | Chat Template、Loss Mask、数据验证 |
| 研究领域 CPT | [防遗忘实验](continued-pretraining/cpt-replay-wsd.md) | 预训练损失、训练分布、评估协议 |
| 实践 DPO | [偏好对齐](alignment/dpo-and-online-data.md) | SFT、log-prob、参考模型 |
| 实践 GRPO | [16GB GRPO Playbook](reinforcement-learning/grpo-16gb-playbook.md) | Reward、Rollout、Advantage、TRL |
| 看工业 RL 架构 | [系统工程](training-systems/memory-and-distributed.md) | 显存状态、FSDP、异构服务 |

## 5. 执行与验收统一规范

- 先运行可复现的**小实验**，记录基线；然后只改变一个主要变量做对照。
- 固定数据划分与 Prompt、解码配置；严禁通过测试集挑选/调参后仍将其作为独立测试。
- 每次记录：代码 SHA、模型及 Tokenizer revision、数据 Hash、配置、Seed、软件和 CUDA 版本、设备/显存、训练及评估输出。
- 训练异常也保留日志：OOM、NaN、Reward Hacking、退化等。
- 产物：源码入口说明、关键公式、实验配置、真实曲线、基线对照、失败原因、下一步。
- 检查清单：[学习进度](learning-progress.md)；通用 [评估协议](evaluation/evaluation-protocol.md)；[实验模板](experiments/EXPERIMENT-TEMPLATE.md)。

## 6. 注意的技术边界

- 高质量数据非常重要，但“80% 由数据决定”不是通用可证的比例。
- 当前 SFT 模型采样一次后构造**固定**偏好集，与在训练中持续重新采样的 **Online DPO** 不相同；On-policy 数据不保证始终更好。
- CPT 不需要达到固定数十亿 Token 才能有效；本路线关注小预算条件下可测的影响，不宣称已完成真正领域注入。
- WSD 对比 Cosine 为实验问题，不设结论；GRPO 不保证固定显存/吞吐/性能，具体 KL 配置可能为 0。
- SFT、DPO、GRPO 是不同优化路径；先从同一 SFT Checkpoint **分叉对照**，再研究串行组合。
- 计划列出的实验均为**待执行**；无实测记录时不得填写性能数字。

## 7. 下一步

打开 [实验总导航](experiments/README.md)，从 **01 MiniMind 白盒** 开始；学习中的理论缺口参考 [基础模块](fundamentals/M01-M04.md)，所有官方资料见 [阅读清单](papers/READING-LIST.md)。

