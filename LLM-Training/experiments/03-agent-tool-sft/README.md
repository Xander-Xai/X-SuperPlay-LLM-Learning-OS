# 实验 03 — Agent 工具轨迹数据 + Full/LoRA/QLoRA SFT

**状态：NOT RUN**。目标是让训练与既有 RAG/Agent 工程衔接，不只是普通单轮问答 SFT。

## 沙盒场景

模拟 query_inventory(product_id)、search_docs(query, filters) 两个只读工具。准备正确值/引用来源的自动验证器。不要使用无授权的企业数据。

## 数据流水线

- [ ] 设计任务类别、工具 schema 和难度分布，准备隔离的测试集。
- [ ] 教师模型生成多轮候选与可选推理轨迹，按任务 ID 存档。
- [ ] 同题 N 采样 + 规则/工具验证 + rejection sampling。
- [ ] 记录过滤、去重、抽检、最终 train-val-test 版本。
- [ ] 验证 system/user/tool masked，assistant(tool_call/final) 两段计算 loss；使用官方 template。
- [ ] 记录 base → Full / LoRA / QLoRA 配方的显存/吞吐/准确性。

## 主要评测

Tool selection accuracy、arguments exact/semantic match、JSON/schema validity、tool execution success、citation correctness、end-to-end success、held-out loss。

## 结果与验收

保留每组训练配置、种子、真实日志、固定样本明细和错误类别；不把几条人工演示视为效果验证。

专题：[合成数据](../../data-engineering/synthetic-data-and-rejection-sampling.md) · [Tool mask](../../sft-peft/agent-tool-calling-loss-mask.md) · [LoRA](../../sft-peft/lora-qlora-full-sft.md)。

