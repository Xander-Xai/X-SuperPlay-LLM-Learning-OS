# 实验 06 — Profiler、工业 RL 架构和 Agent 部署

**状态：NOT RUN**。

## 学习与交付

1. PyTorch Profiler / CUDA memory stats：记录 SFT 与 GRPO 训练中 allocated、reserved、peak、耗时热点、Activation/Optimizer 状态的估算与实测差异。
2. 手绘 DDP、ZeRO-1/2/3、FSDP、TP/PP/CP/EP 显存/通信关系；无需在单卡强造多机结果。
3. 阅读 verl 或 OpenRLHF 的 worker/actor/rollout/reference/weight sync 架构，并对照 [工业架构笔记](../../training-systems/memory-and-distributed.md)。
4. 精读 nanochat 的端到端目录组织，对比 MiniMind 和生产分布式系统的不同职责。
5. 将微调模型经兼容的推理服务接入模拟的 RAG/Agent 工具链；按同一任务集比较 Base、SFT、DPO、GRPO（如对应实验成功）。
6. 记录 TTFT、P50/P95 latency、tokens/s、VRAM、工具参数准确率、执行成功、引用正确率、失败率和并发条件。

## Done

- [ ] 有实测 Profile/性能日志与复现配置。
- [ ] 能解释 Rollout Engine 与 Training Engine 分离部署及权重同步。
- [ ] 工具调用端到端测试与回归可执行。
- [ ] 能明确区分“模型微调改善”与“推理服务/提示词变动带来的改善”。

