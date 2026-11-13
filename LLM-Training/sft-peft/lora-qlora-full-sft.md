# Full SFT / LoRA / QLoRA：一张表理解原理与代价

## 分类先行

- **SFT** 是监督学习阶段，常用目标为 response/assistant mask 下的 Token Cross-Entropy。
- **Full SFT** 更新所有选定可训练参数；显存消耗较高。
- **LoRA** 将某些矩阵更新写成低秩形式 ΔW = BA，冻结底座并训练 Adapter。
- **QLoRA** 通常用 4-bit 量化权重作为冻结底座，结合 LoRA 做反向传播；并非“4-bit 全量训练”。

## 基础公式与变量

设 W∈R^(d_out×d_in)，A∈R^(r×d_in)，B∈R^(d_out×r)，ΔW = (α/r)BA。关注 r、alpha、dropout、target modules、训练 dtype、optimizer、梯度检查点。

LoRA 对注意力 Q/K/V/O 与 MLP 各层不同配置的收益和参数量都不同；**不能只比较总参数数目而忽略更新矩阵覆盖范围**。

## 三组实验

| 组 | 要记录的内容 | 可能限制 |
|---|---|---|
| Full SFT | 权重、优化器状态、激活、训练参数量 | 单卡 16GB 的序列/batch 上限 |
| LoRA | Adapter 参数量、注入层、显存/吞吐 | 底座仍可能很耗显存 |
| QLoRA | 量化实现、计算 dtype、Adapter、峰值显存 | 量化误差和兼容性 |

将相同固定数据与评估集应用于三组；如果无法匹配参数容量或训练 FLOPs，应称为“实用配方对照”，不应宣称严格算法公平。

## 验收

训练 Loss、独立工具任务成功率、P95 推理延迟、peak VRAM、step/s、checkpoint 大小都有记录；能够解释为什么 BF16/FP16、AdamW、梯度、Activation 的显存口径不同。

官方参考：[PEFT LoRA](https://huggingface.co/docs/peft/main/en/conceptual_guides/lora) · [QLoRA 论文](https://arxiv.org/abs/2305.14314) · [TRL SFT](https://huggingface.co/docs/trl/sft_trainer)。

