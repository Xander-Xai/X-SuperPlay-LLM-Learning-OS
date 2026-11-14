# LLM Training 学习中心｜需求驱动的 V3 扩展与 V2 基础

## 全栈 6 域知识入口（优先看这组，不改变 12 模块原有编号）

- **完整大模型全景与关系图**：[LLM 全链路 Atlas](knowledge-graph/LLM-FULL-STACK-ATLAS.md)（包含训练与推理两条不同链路、六域与多模态、11 组易混淆原理）。
- **上游+官方资料逐项链接**：[33 主题知识资料总索引](resources/UPSTREAM-RESOURCE-MAP.md) · [机器索引](index/upstream-knowledge-index.json)（固定上游 SHA，不复制大段内容）。
- **需求驱动而非机械课程**：[12 条问题实战卡](demand-driven/AI-NATIVE-NEED-ROUTES.md) · [AI-Native 学习闭环](learning-method/AI-NATIVE-LEARNING-LOOP.md) · [终端查询](tools/route_atlas.py)。
- **本轮审查材料**：[全栈跨仓扩展验收范围](ACCEPTANCE-FULL-STACK-20261114.md)。

## 本仓当前 V3 导航｜从需求跳学，不按线性顺序打卡

- [Roadmap V3：深度覆盖、知识依赖与生产能力](ROADMAP-V3-DEMAND-DRIVEN.md)
- [需求入口和 18 张机器索引卡](demand-driven/README.md) · [一个实战任务卡模板](demand-driven/DEMAND-CARD-TEMPLATE.md) · [五个真实工程故障的合成教学案例](demand-driven/worked-demand-cards.md)
- [知识依赖图 V3](knowledge-graph/dependency-and-capability-map.md) · [20 份权威来源导航](resources/AUTHORITATIVE-INDEX.md)
- **可运行课程纵切**：[CPU Loss Mask](labs/README.md) · [DPO/GRPO 数学与 Reward Hacking](labs/preference-rl-math/README.md) · [Agent 任务级指标评测](labs/task-evaluation/README.md) · [合成 Tool Gateway](labs/synthetic-tool-gateway/README.md)。
- [可运行合成工具网关实验](labs/synthetic-tool-gateway/README.md)（标准库即可运行，验证工具授权/参数/证据/负例，不冒充大模型训练）
- [L0–L4 独立能力 Rubric](assessments/CAPABILITY-RUBRIC.md) · [实战阶梯](labs/capability-ladder.md) · [生产 Go/No-Go](production/PRODUCTION-READINESS.md)
- [机器索引与上下游双向关系](index/README.md) · [命令行按需检索](tools/route_learning.py)

**V3 深度补充**：M01–M12 的独立页面现包含专业机制、白话类比、可操作实验、注入失败样本、模块级权威参考与 Go/No-Go。验收记录见 [V3 审计](ACCEPTANCE-V3-AUDIT.md)。

**定位**：这是训练、推理、Agent、RAG 与评测等技能的学习基地；学到的知识可用于多种下游产品，但不要求本仓服务某个固定项目。原有的 [V2 十二模块导航](ROADMAP-V2.md) 和 5 类训练实验继续有效。

---

**从此页进入 12 个模块，而不是按日历从头到尾死读。** 本仓库内容为学习资料/实验计划；GPU 训练结果仍标记 NOT RUN。最新审核记录见 [验收报告](ACCEPTANCE-V2.md)。

## 一眼看懂路线

```text
M01 数学 → M02 Tokenizer/数据 → M03 Transformer → M04 Pretrain
                                                 ├─ M05 CPT（可选）
                                                 └─ M06 SFT / LoRA / 工具轨迹
                                                             ├─ M07 DPO/偏好
                                                             └─ M08 PPO/GRPO/RLVR
M09 训练系统 + M10 评估：贯穿每一个训练阶段
M11 蒸馏/量化/部署 → Agent/RAG 应用反馈；M12 前沿专题按需选修
```

**主线**：MiniMind（唯一源码白盒化实战底座）→ Qwen3-0.6B-Base（真实开源模型 CPT/SFT/DPO/GRPO 实验）→ RAG/Agent 工具闭环。CS336 作为理论字典；Raschka 按需补难点；nanochat 最后看工程组织。

## 12 模块：单点进入与退出

| 模块 | 独立入口 | 优先级 | 学到什么程度 |
|---|---|---|---|
| M01 数学/Autograd | [M01](modules/M01.md) | P0 | L2 |
| M02 Tokenizer/数据 | [M02](modules/M02.md) | P0 | L2 |
| M03 Transformer | [M03](modules/M03.md) | P0 | L2 |
| M04 Pretrain | [M04](modules/M04.md) | P0 | L2 |
| M05 CPT | [M05](modules/M05.md) | P1 | L1→按需 L2 |
| M06 SFT/QLoRA/Tool Call | [M06](modules/M06.md) | P0 | L2 |
| M07 偏好优化 | [M07](modules/M07.md) | P0 | L2 |
| M08 PPO/GRPO/RLVR | [M08](modules/M08.md) | P0 | L2 |
| M09 训练系统 | [M09](modules/M09.md) | P0 基础/P1 进阶 | L1→L2 |
| M10 全链路评估 | [M10](modules/M10.md) | 贯穿 P0 | L2 |
| M11 蒸馏、Serving | [M11](modules/M11.md) | P1 | L1→L2 |
| M12 高级专题 | [M12](modules/M12.md) | P2 | L1 |

L1：能解释定义、依赖、公式和边界；L2：能够定位源码、运行实验、排查问题、用真实日志验收；L3：可推导、消融和扩展实现。详见 [知识依赖图](knowledge-graph/concept-dependencies.md)。

## 4 个里程碑、5 类训练实验 + 1 个部署验收

| 里程碑 | 训练实验 | 验收 |
|---|---|---|
| 1 白盒化底座（约 1–2 周） | [01 MiniMind Pretrain→SFT](experiments/01-minimind-whitebox/README.md) | shape/loss/optimizer/mask + 真实 checkpoint |
| 2 数据与真实模型（约 1–2 周） | [02 CPT Replay](experiments/02-qwen-cpt-replay/README.md) + [03 Agent Tool SFT](experiments/03-agent-tool-sft/README.md) | 受控配比/调度器对照、合成轨迹质量与成功率 |
| 3 偏好与强化学习（约 2 周） | [04 DPO](experiments/04-dpo/README.md) + [05 GRPO](experiments/05-grpo/README.md) | 从相同 SFT 基线分叉，独立正确率与 Reward Hacking 检查 |
| 4 系统与部署（约 1 周） | [06 Deployment / Profiler](experiments/06-deployment/README.md)（不计训练实验） | 性能、端到端 Agent 与系统架构 |

5 类训练实验：① MiniMind Pretrain/SFT、② CPT、③ Agent Tool SFT、④ DPO、⑤ GRPO；**06 是部署与系统验收，不算第 6 类训练实验**。全程采用 [实验记录模板](experiments/EXPERIMENT-TEMPLATE.md)。

## 先从这里学

1. 想先搭全局框架：[预训练 vs 后训练关系](knowledge-graph/pretrain-posttrain-relations.md) 和 [全流程图](knowledge-graph/full-training-pipeline.md)。
2. 想直接开始：先做 [纯 CPU Shift/Mask 教学测试](labs/README.md)，之后进入 [MiniMind 白盒实验](experiments/01-minimind-whitebox/README.md) 与 [第一天操作手册](experiments/01-minimind-whitebox/RUNBOOK-FIRST-DAY.md)。
3. 想补 Tokenizer：[BPE / Packing / 数据污染](data-engineering/tokenizer-and-packing.md)。
4. 想补经典 RLHF：[Reward Modeling/ORPO](alignment/reward-model-orpo.md) 和 [PPO 基础](reinforcement-learning/ppo-rlhf-fundamentals.md)。
5. 想反向跳学：从 [知识依赖图](knowledge-graph/concept-dependencies.md) 或 [面试题库](interview-qa/QUESTION-BANK.md) 出发。
6. 学习材料：[权威资源与论文清单](papers/READING-LIST.md)；失败时：[故障排查](troubleshooting/COMMON-FAILURES.md)。

## 不虚报进度

仓库静态检查与 CPU Toy 测试不等于完整模型训练通过。所有尚未得到**模型日志、独立评估与版本记录**的任务始终标记 NOT RUN。每轮依据 [评估协议](evaluation/evaluation-protocol.md) 与 [进度清单](learning-progress.md) 验收。

