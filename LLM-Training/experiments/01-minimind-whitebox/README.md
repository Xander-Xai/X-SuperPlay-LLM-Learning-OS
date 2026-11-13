# 实验 01 — MiniMind 白盒 Pretrain → SFT

**状态：NOT RUN**。先跑当前 MiniMind README 的最小数据/模型配置；固定项目 commit，不照搬旧博客指令。

## Steps

1. Clone [MiniMind](https://github.com/jingyaogong/minimind) 并记录 SHA；查看 model/model_minimind.py、trainer/train_pretrain.py、trainer/train_full_sft.py、dataset/lm_dataset.py（若上游改动以当前仓库为准）。
2. 绘制每个张量 shape：input_ids→Embedding→Attention→MLP→Logits→CE Loss；用小 batch 的 hook 或断点验证。
3. 重新实现关键模型组件（RoPE、RMSNorm、SwiGLU、Causal Attention），按输入/输出/数值误差和 mask 语义做对照；不再额外建 TinyGPT。
4. 运行小模型 Pretrain → Full SFT，并保存权重与能复训的必要状态，比较相同 Prompt 的两个阶段。
5. 插入含两次 assistant 输出与一次 tool observation 的消息，进行 [Loss Mask](../../sft-peft/agent-tool-calling-loss-mask.md) 单元测试。
6. 计算权重/梯度/优化器/激活显存的估算，再用 torch.cuda 实测；记录差异。

## 产物与验收

- [ ] 实现通过单元测试（shape、数值、causal mask）。
- [ ] 训练流程完整；Checkpoint、Loss 曲线、训练环境可追溯。
- [ ] Tool 观测位置 Labels=-100，Tool Call 和 Final Answer 可训练。
- [ ] 能口述一次 optimizer.step 前后的梯度与状态变化。
- [ ] 拥有至少一个失败/异常排查案例。

注意单个 batch 的 loss 下降并不足以说明语言能力提升，必须保留独立验证数据。

