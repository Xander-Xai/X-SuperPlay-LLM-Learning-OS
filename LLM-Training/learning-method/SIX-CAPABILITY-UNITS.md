# 六个能力单元（按需求选择，不是 6 周排课）

> 这 6 个单元是**学习成果与能力覆盖清单**，不要求依次通关，更不是“预计六周完成”；同一实验可以支持多个能力单元，但不能重复计算为不同真实训练结果。见 [总 Roadmap V3](../ROADMAP-V3-DEMAND-DRIVEN.md)、[课程 Rubric](../assessments/CAPABILITY-RUBRIC.md)。

| 单元 | 什么时候学 | 专业问题与白话理解 | 实战入口 | 最小验收证据 |
|---|---|---|---|---|
| U1 底层机制 | 不懂 Logits/Loss/Backward | Attention 受 Causal Mask 约束、CE 只预测下一 token；像**一边写一边预测下一个字** | [可执行 TinyGPT](../labs/tiny-gpt/README.md)、[M01](../modules/M01.md)、[M03](../modules/M03.md) | Tensor shape、Mask 负例、梯度、单次 Shift、训练 Batch Loss |
| U2 Pretrain | 只会调用 Trainer，不会追踪一次训练 | 数据→前向→梯度→更新→恢复；像**知识基础训练与全套存档** | [MiniMind](../experiments/01-minimind-whitebox/RUNBOOK-FIRST-DAY.md)、[M04](../modules/M04.md) | 真实 Base 权重、Validation 曲线、Checkpoint 状态与恢复 |
| U3 SFT/QLoRA/CPT | 指令/领域知识不足 | CPT 改分布；SFT 学行为；QLoRA 是省资源方式；像**复训岗位 vs 查手册/岗前培训** | [实验 02](../experiments/02-qwen-cpt-replay/README.md) 与 [03](../experiments/03-agent-tool-sft/README.md)、[M06](../modules/M06.md) | 同数据/同预算基线、真实 Tokenizer Assistant Mask、资源与任务差异 |
| U4 Preference/DPO | 模型输出冗长、偏好退化 | 偏好对比优化与 Reference log-ratio；像**从同题两个答案中学习偏好** | [DPO 数值 Toy](../labs/preference-rl-math/README.md) → [实验 04](../experiments/04-dpo/README.md) | Pair provenance、SFT/DPO 独立对照、WinRate+任务指标 |
| U5 RL/GRPO/RLVR | 有可验证奖励、需要优化多次尝试 | Rollout、Reward、Group Advantage 与策略更新；像**反复试题并根据客观评分纠正** | [GRPO Toy](../labs/preference-rl-math/README.md) → [实验 05](../experiments/05-grpo/README.md) | Reward/Accuracy/Length/资源和奖励投机负例；未跑真实训练就 NOT RUN |
| U6 训练工程/评估/部署 | P95 高、显存 OOM、无法发布/回滚 | Profiler/FSDP/ZeRO/Serving/Eval 等；像**训练工厂的设备、质检与运营** | [M09](../modules/M09.md)、[M10](../modules/M10.md)、[M11](../modules/M11.md)、[实验 06](../experiments/06-deployment/README.md) | 原始 Profile、质量/成本/权限回归、演练回滚记录 |

## 六个单元的关系，不等于学习顺序

~~~mermaid
flowchart LR
  A["U1 机制"] -->|底层可验证| B["U2 Pretrain"]
  B -->|提供 Base| C["U3 SFT/CPT"]
  C -->|可选分支| D["U4 DPO"]
  C -->|可选分支| E["U5 RL/GRPO"]
  F["U6 Eval/Systems"] -.->|贯穿| B
  F -.->|贯穿| C
  F -.->|贯穿| D
  F -.->|贯穿| E
  API["现成模型/API"] -->|直接进入| F
~~~

图中 B→C 是一种典型的**模型来源依赖**，不是要求你先训练 Base 才能使用开源 Qwen；U4/U5 不强制串行；U6 不需要等其他单元完成才学习。真正的个人跳学策略见 [AI-Native 学习闭环](AI-NATIVE-LEARNING-LOOP.md)。

## 两个防止“学完一堆概念却不会用”的规则

- **要求每个研究点交四份证据**：专业原理/白话笔记、可以复现的代码或独立命令、真实执行日志（未执行写 NOT RUN）、与简单基线的结果对照。Toy 日志不能填写成 Qwen 训练日志。
- **达到当前任务目标就停止**：学习只是为了支撑未来任何下游项目所需能力，知识图保持完整，当前深入深度由业务/面试/好奇心触发。用 [需求卡](../demand-driven/DEMAND-CARD-TEMPLATE.md) 记录下一次进入的位置和验证边界。
