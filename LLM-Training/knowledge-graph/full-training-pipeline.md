# 预训练 → 后训练 → 部署：完整链路与关系图

## 1. 全流程图

~~~mermaid
flowchart TD
  D["M02 数据采集、去重、质量过滤、混合"] --> T["Tokenizer / Packing / Batch"]
  T --> A["M01/M03 Transformer + Autograd"]
  A --> P["M04 Pretraining: next-token loss"]
  P --> B["Base Model"]
  B --> C["M05 CPT / Mid-training (可选)"]
  B --> S["M06 SFT: instructions / tools / masks"]
  C --> S
  X["Teacher / Tool verifier / Synthetic / Rejection sampling"] --> S
  S --> I["SFT Model"]
  I --> F["M07 DPO / Preference optimization"]
  I --> R["M08 GRPO / PPO / RLVR"]
  F --> H["Aligned Model"]
  R --> H
  H --> V["M10 Evaluation / Regression"]
  V --> O["M11 Quantization / Distillation / vLLM"]
  O --> G["RAG / Agent / Function Calling"]
  G -. "反馈与新数据" .-> D
  E["M09 Profiling / parallelism / memory"] -.-> P
  E -.-> S
  E -.-> R
  Z["M12 MoE / long context / multimodal / agentic RL"] -.-> A
  Z -.-> R
~~~

**注意**：这是学习顺序，不是唯一工业训练配方；DPO 与 RL 可以作为分支或组合，CPT 也可跳过；评估应贯穿各节点。

## 2. 为什么各阶段不能混淆

| 问题 | Pretrain | CPT | SFT | DPO | GRPO |
|---|---|---|---|---|---|
| 数据 | 广域文本/代码等 | 目标领域/混合文本 | 指令与目标输出 | prompt+chosen+rejected | prompt+在线生成+奖励 |
| 常见目标 | Causal LM CE | Causal LM CE | Masked instruction CE | 偏好损失 | 策略优化（相对优势等） |
| 初始模型 | 随机或续训权重 | 已有 Base | Base / 已训模型 | 通常 SFT 模型 | 通常 SFT / policy |
| 检验 | held-out token loss / 任务 | 领域提升与通用退化 | 指令/工具任务 | 偏好胜率和任务质量 | 可验证任务成功率与奖励投机 |
| 关键风险 | 不稳定、数据污染 | 灾难性遗忘 | Mask 错、过拟合 | 偏好数据偏差 | Reward hacking、采样开销 |

## 3. Agent 案例串联

企业用户问“查产品库存并提供文档依据”。

- Pretrain/CPT：模型学会产品术语和文档形式。
- SFT：教会正确生成工具调用、读取工具返回、按证据回答。
- DPO：更偏好引用正确、参数合法、不胡编的回答。
- RL：在有工具执行反馈的任务环境中，根据实际结果优化流程。
- Evaluation：库存值来自接口、引用能定位源文档、任务完整成功，不仅仅是语句流畅。

## 4. 读图前置

遇到不理解的缩写或公式，请从 [依赖图](concept-dependencies.md) 反查，不必重学所有课程。

