# 实验 02 — Qwen3-0.6B Base CPT / Data Replay / Scheduler

**状态：NOT RUN**。使用同一个 Base revision 和固定域内、通用验证集；本阶段重点是**遗忘与训练动力学**。

## Plan

- A Base：不训练，只评估。
- B Domain CPT：100% 域数据，固定训练 token 预算。
- C Replay CPT：80% 域数据 + 20% 通用高质量数据，固定相同 token 预算。
- D Scheduler：在 B 或 C 的相同数据配方上额外比较 Cosine vs WSD，其他条件保持不变。

先从适配 16GB 的短序列和小 batch 开始；不保证全参数训练能满足内存。若无法匹配训练方法或模型参数更新范围，应详细记录差异，并避免宣称严格公平比较。

## 数据与评估

数据从训练集之外准备域内与通用 held-out；保留数据 hash、token 数、采样率和清洗规则。评估 PPL/CE、域内任务正确性、通用推理子集、Loss 曲线、梯度与显存。

## Done

- [ ] Base / Domain / Replay 三者评估口径一致。
- [ ] Domain vs Replay 的通用退化有可核验记录。
- [ ] 调度器对照只改变一种主要变量。
- [ ] 结果报告清楚标注小数据/单次运行的统计限制。

专题：[CPT 防遗忘](../../continued-pretraining/cpt-replay-wsd.md)。

