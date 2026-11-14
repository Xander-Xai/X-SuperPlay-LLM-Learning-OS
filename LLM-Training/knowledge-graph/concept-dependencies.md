# 知识依赖图与跳学策略（V2 基础）

**V3 已补充带语义的 [需求→依赖→实验→生产能力图](dependency-and-capability-map.md)**：本页保留简洁的基础依赖图，不应被误读为唯一学习顺序。

## 最短依赖路径

~~~mermaid
flowchart LR
  Math["张量 / 链式法则 / CE"] --> Torch["Autograd / AdamW"]
  Tok["Tokenizer / BPE"] --> Pre["Pretrain"]
  Attn["Causal Attention / RoPE"] --> Pre
  Torch --> Pre
  Pre --> CPT["CPT + Replay"]
  Pre --> SFT["SFT + Loss Mask"]
  SFT --> DPO["DPO / preference data"]
  SFT --> RL["GRPO / Reward / Advantage"]
  RL --> Sys["Rollout & training system"]
  DPO --> Eval["Evaluation / regression"]
  RL --> Eval
  SFT --> Tool["Agent Tool Calling"]
  Tool --> Eval
~~~

## 不必从头学的逆向入口

- **已有 Agent 工程，需要训练工具调用**：M06 [Tool Calling SFT](../sft-peft/agent-tool-calling-loss-mask.md) → 看不懂标签时回 M02/M03 → M07/08 对齐与 RL。
- **面试问 QLoRA**：M06 [LoRA](../sft-peft/lora-qlora-full-sft.md) → Linear 梯度/低秩 → NF4、Double Quantization 和显存状态。
- **训练 Loss NaN 或显存爆炸**：M09 [训练系统](../training-systems/memory-and-distributed.md) → M01 AdamW/混合精度 → M10 评估。
- **问 PPO、DPO、GRPO 差异**：M07 DPO → M08 GRPO → 先对比数据来源和目标，再看公式。
- **想做领域模型**：M05 CPT → Data Replay / LR → M10 通用能力对照；不要先承诺模型能替代 RAG。
- **想理解推理模型训练**：M08 可验证奖励 → M07 偏好 → M06 冷启动轨迹生成 → M12 长链推理与测试时计算。

## 阅读深度卡

每个新概念只需先回答：①专业定义；②白话解释；③输入和输出；④核心公式；⑤代码在哪；⑥一个可测失败例子；⑦与其他模块的关系。理解后才投入复杂复现。

详细学习目标见 [Roadmap](../ROADMAP-V2.md)。

