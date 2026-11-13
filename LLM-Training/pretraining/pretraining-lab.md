# M04：Pretrain 白盒学习手册（以 MiniMind 为唯一底座）

## 0. 目标：一个 Batch 从哪里来、怎样更新权重

```text
原始文本 → Token IDs → input_ids / labels
→ embedding + causal transformer → logits [B,T,V]
→ shift-one token cross-entropy → loss
→ backward → gradients
→ AdamW.step / schedule → new weights
→ validation + checkpoint
```

## 1. 先做不依赖大模型的 CPU 小实验

进入 [labs](../labs/README.md)：真实测试 assistant/tool mask、shift-one 以及梯度是否产生。此实验只是教学验证，**不是独立 TinyGPT 或真实预训练**。

## 2. MiniMind 代码精读顺序

| 位置 | 追问 |
|---|---|
| [model/model_minimind.py](https://github.com/jingyaogong/minimind/blob/master/model/model_minimind.py) | embedding、RoPE、GQA、RMSNorm、MLP、Logits 形状是什么？ |
| [dataset/lm_dataset.py](https://github.com/jingyaogong/minimind/blob/master/dataset/lm_dataset.py) | 原文怎样进入 Tokenizer、如何生成 labels / masks？ |
| [trainer/train_pretrain.py](https://github.com/jingyaogong/minimind/blob/master/trainer/train_pretrain.py) | forward、loss、accumulation、backward、optim、scheduler 各在哪？ |
| [trainer/train_full_sft.py](https://github.com/jingyaogong/minimind/blob/master/trainer/train_full_sft.py) | SFT 与 Pretrain 数据、loss mask 差别在哪里？ |

上游会变更：Clone 后记录 commit SHA，以当前项目 README 的命令/数据配置为准。

## 3. 每一步都写可验收证据

1. 截取一个 toy batch，标注 `input_ids [B,T]`、`labels [B,T]`、`logits [B,T,V]`。
2. 检查模型是否内部 shift，避免 Trainer 又 shift 一次。常见目标是 logits[t] 预测 labels[t+1]。
3. 训练前后记录 loss、grad_norm、学习率、参数 hash 或差值。若未更新参数，检查冻结、loss ignore_index、梯度累积。
4. 同步记录 optimizer state 和 scheduler state（不能只保留推理权重）。
5. 对照独立 validation loss，不能仅展示一次 batch loss 下降。

## 4. 显存模型

`参数 + 梯度 + 优化器状态 + 激活 + 临时张量 + 框架/分配器`。BF16、是否 master FP32、optimizer 分片、activation checkpointing 都影响实际计算。用 [系统专题](../training-systems/memory-and-distributed.md) 的测量方法验证。

## 5. Go / No-Go

- [ ] 所有关键 shapes 能手写复原且与断点一致。
- [ ] causal mask 和 shift-one 有可运行测试。
- [ ] Pretrain/SFT 权重和评估相互区分，Checkpoint 有恢复证据。
- [ ] 训练曲线、环境、数据版本、tokens_seen 留档。

完整执行清单：[实验 01](../experiments/01-minimind-whitebox/README.md)。这页不是已执行的训练报告。

