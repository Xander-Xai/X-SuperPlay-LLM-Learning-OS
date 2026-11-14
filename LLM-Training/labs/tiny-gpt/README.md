# 实验 A｜真正从 PyTorch 原语手写 Tiny Decoder-only GPT

**状态：CPU 教学源码已编写，真实运行结果以最新 CI 为准。不是 MiniMind / Qwen 真实预训练。**

这是原路线中此前尚未覆盖的最小 GPT 实验。已有的 [Shift/Mask Toy](../README.md) 只优化伪造的 Logits，不能代替 Transformer；此目录用 **Embedding → 位置嵌入 → QKV Causal Self-Attention → 残差 / LayerNorm / MLP → Logits → 单次 Shift CE → Autograd → AdamW → 临时 Checkpoint** 串起执行链。

## 直接运行

从仓库根目录（需要 Python 3.11 和 PyTorch CPU 环境，不需要联网或显卡）：

~~~bash
python LLM-Training/labs/tiny-gpt/tiny_gpt.py
python -m unittest discover -s LLM-Training/labs/tiny-gpt -p 'test_*.py' -v
~~~

本实验没有 BPE，采用**字符级** Tokenizer；训练语料是程序生成的重复英文句子。默认 25 个小步训练，固定评测 Batch 也参加训练，Loss 下降只能证明**优化和张量链路可工作**，不能证明泛化语言理解、对话能力或真实模型训练效果。生成采用 Argmax，不做温度采样。

## 专业解释 + 大白话 + 源码入口

| 层 | 专业定义 | 大白话 | 在源码哪里 |
|---|---|---|---|
| Tokenizer / Embedding | 每个字符 ID 映射到可训练向量，形状为 [B,T,C]；本实验非 BPE | 把不同字编成编号并换成坐标 | `toy_tokens`、`TinyGPT.tok` |
| Position | 为位置信息添加可训练嵌入 | 记住“这是第几个字” | `TinyGPT.pos` |
| Q/K/V + Mask | 缩放注意力 softmax(QKᵀ / √d) V；下三角 mask 避免读取未来 | 写第 5 个字不允许偷看第 6 个 | `CausalAttention` |
| Norm / FF / Residual | LayerNorm、GELU MLP 与残差更新隐藏状态 | 校准刻度、加工信息、保留原通道 | `Block` |
| 预测与 CE | Logits [B,T,V] 预测 Tokens 的下一位，目标右移一次 | 每一行看过前文猜下一个字 | `next_token_loss` |
| 训练更新 | Gradient=∇θL，AdamW 读取梯度和优化器状态更新权重 | 错误反馈→改参数→再验证 | `train_smoke` |
| 断点保存 | 模型/优化器/RNG/Step 的本地临时 Checkpoint | 不只存答案，还存学习进度 | `smoke` |

**公式**：给出 Tokens `x_0…x_T`，由位置 `t` 预测 `x_(t+1)`，损失为各位置的负对数似然均值。真实预训练时应考虑 Padding/Mask、分布式、数据采样位置与真正独立验证集；本教学不模拟上述生产问题。

## 你必须自己做的四步

1. **因果性**：修改未来 3 个 Token，检查前几个 Logits 不变；试着移除 Mask，确认单测能抓到未来信息泄漏。
2. **梯度和单次 Shift**：跟踪 QKV 的梯度；确认训练目标是 `ids[:, 1:]`、模型输入是 `ids[:, :-1]`。不要在模型和外部 Trainer 各 Shift 一次。
3. **受控实验**：固定 seed，只改学习率、序列长度或 Head 数之一，比较相同固定 Batch Loss；说明为何这**不能**充当独立 Test。
4. **Checkpoint 和恢复**：对照模型/优化器保存与重新加载后输出一致；进一步研究 sampler/RNG 恢复才能断言训练轨迹一致。

## 验收口径

- L1：你能画出 Batch/Tensor/Vocab 的维度，并白话解释 Attention、梯度和更新；
- L2：代码、单测、负例都在自己环境跑通，留命令与日志；
- L3：换一份自己设计的公开/虚构字符数据仍能定位 Loss 不降、Mask 错位和数值异常；
- L4：换陌生字符语料、独立定位错误并提供受控对照才可申请迁移能力验收。**生产上线是另行触发的 G0–G8 门禁，不是 L4 的定义**。本 Toy 仍不能证明生产上线能力；进入 [MiniMind Runbook](../../experiments/01-minimind-whitebox/RUNBOOK-FIRST-DAY.md)，再处理真实 Tokenizer、RoPE、Checkpoint、数据污染和独立验证。

**参考**：[Stanford CS336 作业 A1](https://cs336.stanford.edu/) · [Raschka《LLMs-from-scratch》](https://github.com/rasbt/LLMs-from-scratch) · [MiniMind](https://github.com/jingyaogong/minimind)。

**重要差异**：本教学用 learned position / LayerNorm / GELU，不是现代 Qwen 的 RoPE / RMSNorm / SwiGLU / GQA；这些应通过 [M03](../../modules/M03.md) 单独学习。
