# 训练基础可运行教学验证：CPU Shift + Assistant Loss Mask

**定位**：这是对 M01/M04/M06 的 1 分钟单元实验，独立于 MiniMind，仅用于验证分词后 **Token 级角色范围**、assistant-only 标签选择、一次右移和梯度位置。它没有训练真实模型，也不能取代 MiniMind 代码实战。

## 教学实验 A 已补全真实 Decoder 结构

现有 Loss Mask/Shift Toy 优化**可训练假 Logits**，不包含 Transformer；请另见 [手写 TinyGPT](tiny-gpt/README.md)，验证真实 QKV、因果性、Embedding、AdamW 与模型/优化器临时恢复。二者都只提供 CPU 合成教学证据，不表示真实 MiniMind/Qwen 已训练。

## 运行

GitHub Actions 的 `cpu-toy` 作业会在 CPU-only PyTorch 环境执行同一套测试；`docs` 作业只验证文档结构、内部链接与实验状态。

在仓库根目录执行：

```bash
python -m pip install torch  # 已有兼容的 PyTorch 则跳过
python LLM-Training/labs/toy_train.py
python -m unittest discover -s LLM-Training/labs -p 'test_*.py' -v
```

不要求 CUDA、联网模型下载或外部 API。教学代码中的 token IDs 是人为构造，**并非 Qwen tokenizer 真正输出**。

## 做完必须理解

1. 标签 `-100` 代表不计算 CE；其中 user/system/tool 位置被 mask，两段 assistant 的目标位置未 mask。
2. `logits[:,t]` 预测 `labels[:,t+1]`，因此有梯度的 **logits 时间位置**可能处于 tool observation 的最后一个 token（它负责预测后续 assistant 的第一个 token），**不能因此判定 Mask 错误**。
3. 真实 TRL/Qwen 训练必须基于目标 tokenizer 的实际 Chat Template / generation mask 验证 token 范围；本练习不提供生产数据打包实现。
4. `loss` 降低只说明 toy 参数学会拟合 toy 标签，**不代表训练过大模型**。

## 下一步

前往 [MiniMind 白盒实验](../experiments/01-minimind-whitebox/README.md)，在真实 `model_minimind.py` 和训练循环上复现和验证。

