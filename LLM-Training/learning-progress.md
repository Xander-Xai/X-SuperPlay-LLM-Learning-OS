# 学习进度、里程碑验收与下次行动

**2026-11-14 课程补充**：[90 个核心概念入口](index/FOUNDATION-COVERAGE.md) 与 [数学](fundamentals/CORE-MATH-PROBABILITY-STATISTICS.md)、[Tokenizer](data-engineering/TOKENIZER-AND-DATA-FOUNDATIONS.md)、[架构家族](fundamentals/MODEL-FAMILIES-AND-GENERATION.md)、[复现/评估](training-systems/REPRODUCIBILITY-AND-EVAL-FOUNDATIONS.md) 已落盘；**不改变本文件真实 MiniMind/Qwen 实验 NOT STARTED 状态**。

**第四轮目录拓展仅限知识覆盖**：[六域知识 Atlas](knowledge-graph/LLM-FULL-STACK-ATLAS.md) + [上游参考资源](resources/UPSTREAM-RESOURCE-MAP.md) + [12 张跨域需求卡](demand-driven/AI-NATIVE-NEED-ROUTES.md)。完成索引与静态验收不改变下方任何模型训练 NOT STARTED 状态，不等于个人学习成果。

**新增第三轮深入验收**：[V3 审计报告](ACCEPTANCE-V3-AUDIT.md)：模块理论/实操/来源已深化，新增 DPO/GRPO 数学和任务评估 Toy；它们不代表真实模型训练或个人能力已通过。

**V3 需求驱动课程已补充设计文档**：[V3 Roadmap](ROADMAP-V3-DEMAND-DRIVEN.md) · [机器索引](index/README.md) · [能力评分](assessments/CAPABILITY-RUBRIC.md)。本次新增索引和 CI 不代表学习者完成 L0–L4，也不代表任何 GPU 训练已执行。

**学习/执行进度状态**：NOT STARTED / IN PROGRESS / READY FOR REVIEW / VERIFIED；实验 README 的 NOT RUN / RUNNING / PASS / FAIL / INCONCLUSIVE 是另一套**运行证据状态**，不能用课程静态文件或 CPU Toy 直接换算。**文档落盘不等于训练已跑通**。

| 阶段 | 状态 | 验收依据 | 证据路径 |
|---|---|---|---|
| Roadmap 与课程设计 | VERIFIED (DOCS ONLY) | 12 模块、4 阶段、官方资源、实验规范 | ROADMAP-V2.md |
| 01 MiniMind 白盒 | NOT STARTED | 模型组件对照 + Pretrain/SFT + Mask | experiments/01-minimind-whitebox/ |
| 02 Qwen CPT | NOT STARTED | Base/Domain/Replay + 调度器对照 | experiments/02-qwen-cpt-replay/ |
| 03 Agent Tool SFT | NOT STARTED | 生成/验证数据 + LoRA/QLoRA 对照 | experiments/03-agent-tool-sft/ |
| 04 DPO | NOT STARTED | 外部 vs 自采样离线偏好数据对照 | experiments/04-dpo/ |
| 05 GRPO | NOT STARTED | 真实 Rollout + Reward/Accuracy/Length/KL 记录 | experiments/05-grpo/ |
| 06 部署 | NOT STARTED | Profiler + vLLM + Agent 端到端回归 | experiments/06-deployment/ |

**学习资料验收见 [ACCEPTANCE-V2](ACCEPTANCE-V2.md)：文档合规通过不代表训练实验通过。**

新增 [实验 A TinyGPT](labs/tiny-gpt/README.md)、[A–E 对照](experiments/EXPERIMENTS-A-E-CROSSWALK.md) 和 [U1–U6 能力单元](learning-method/SIX-CAPABILITY-UNITS.md)。**这只是学习路径补全，不改变旧 MiniMind/Qwen 训练的 NOT RUN 状态。**

## 四个阶段退出门槛

- [ ] **阶段一**：能追踪一个 batch 的完整参数更新；张量/Mask 测试、Checkpoint 和独立验证曲线存在。
- [ ] **阶段二**：CPT 防遗忘和学习率对照、Agent 合成数据版本、SFT 效果对照全部留痕。
- [ ] **阶段三**：同源 SFT 分叉的 DPO/GRPO 对照，包含真实正确率和 Reward hacking 检查。
- [ ] **阶段四**：训练/推理资源剖析、verl 等架构理解、vLLM/Agent 端到端结果。

**补充静态 QA**：[学习资料目录/相对链接自动检查](tools/check_repo.py)；[CPU 教学单元测试](labs/README.md)（不替代 GPU 训练）。

**启动前建议先执行 [第一天 Runbook](experiments/01-minimind-whitebox/RUNBOOK-FIRST-DAY.md)**；CI 的 CPU Toy 成功与真实 GPU 训练成功严格区分。

## 第一个实际任务（无需另外造项目）

1. Clone MiniMind，记录 SHA、版本、CUDA 环境与模型配置。
2. 用一条固定 toy batch 跟踪 input_ids、Logits、Labels、CE Loss，明确 shift。
3. 在 MiniMind 原实现旁复写最小 RoPE/RMSNorm/SwiGLU/Attention 测试，并记录误差。
4. 按 [实验模板](experiments/EXPERIMENT-TEMPLATE.md) 建立第一次实验记录，再执行 Pretrain 和 SFT。

**历史示例排期（非默认执行顺序）**：过去可用白盒→SFT→CPT→Tool SFT→DPO→GRPO→部署覆盖主要能力。现在必须按 [需求驱动 V3](ROADMAP-V3-DEMAND-DRIVEN.md) 从当前问题跳入、仅补必要前置；不是固定第一周或第七周学习，也不能按日期证明掌握。

## 记录行为

每次学习后补充：已解决的问题、还不理解的依赖、下一次最小任务、真实实验路径；避免提交仅由推测构成的“PASS”。

