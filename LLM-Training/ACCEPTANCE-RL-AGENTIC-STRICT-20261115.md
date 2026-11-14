# RL / Agentic RL / Pretraining / Post-training 七部分逐项严格复验（2026-11-15）

> **审计目标**：按提问中的七部分材料，检查内容、入口、来源与可运行性；不重复建设 12 个模块，也不把“代码已提交 / CI 成功”当成用户完成模型训练。基线：此前 [PR #16](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/pull/16) 已合并。此次为其后续增量修补。

## 1. 七部分覆盖矩阵：证据优先

| 用户材料章节 | 对应已落盘资料（权威入口、实验及验收） | 本次结论 |
|---|---|---|
| 一、四者包含关系与训练阶段 | [跨模块关系图](knowledge-graph/pretrain-posttrain-relations.md) / [完整主线](reinforcement-learning/AGENTIC-RL-LEARNING-PATH.md) / M04/M06/M08 | 已具备；强调 RL 是方法，Agentic RL 是交互形式 |
| 二、四者区别、退款例子、Agent 不等于 RL | [专题第 1–3、7 节](reinforcement-learning/AGENTIC-RL-LEARNING-PATH.md) / [合成工具策略更新 Lab](labs/agentic-rl-trajectory/README.md) | 已具备；对比固定执行 vs 真正表格策略更新 |
| 三、为何值得关注、Agentic Loop 与工程化难点 | [专题第 2、8 节](reinforcement-learning/AGENTIC-RL-LEARNING-PATH.md) / [Agent Harness](application-engineering/AGENT-HARNESS-ENGINEERING.md) | 已具备；Rollout、环境、工具、奖励、Credit Assignment |
| 四、学习优先级（P0/P1/P2）及 70/20/10 | [专题第 5–6 节](reinforcement-learning/AGENTIC-RL-LEARNING-PATH.md) / M04/M06/M07/M08/M09/M10 | 已具备；本次明确增加优先级与时间分配说明 |
| 五、28 天路线、RTX 5060 Ti 16GB | [专题第 6 节](reinforcement-learning/AGENTIC-RL-LEARNING-PATH.md) / [单卡 GRPO](reinforcement-learning/grpo-16gb-playbook.md) / [小模型 SFT→GRPO runbook](experiments/mini-posttrain-sft-grpo/README.md) | **本轮补缺**：新增具体数据、代码、命令、版本与独立测评 |
| 六、权威学习资源 | [原始来源分级表](resources/RL-AGENTIC-PRIMARY-SOURCES.md) / [论文清单](papers/READING-LIST.md) | 已收录，部分动态接口本轮重新核验 |
| 七、客服沙盒 A/B/C 与项目竞争力 | [Agentic RL 真实模型实验桥](experiments/agentic-rl-bridge/README.md) / [可运行模拟退款 Q-learning](labs/agentic-rl-trajectory/README.md) / [评估协议](evaluation/evaluation-protocol.md) | 设计与教学测试已有；**A/B/C 真实模型效果对照 NOT RUN** |

## 2. 高质量原始链接（2026-11-15 核验）

| 来源 | 本次核验的入口 | 可信度和用途 | 版本边界 |
|---|---|---|---|
| Hugging Face 作者/官方社区文章 | https://huggingface.co/blog/huggingface/train-agents | 2026-10-20 发布的 Agent 后训练课程，SFT/蒸馏/RL/环境/Harness 的学习主线 | 是教育材料，不是强制算法流水线 |
| TRL 官方 SFTTrainer | https://huggingface.co/docs/trl/sft_trainer | `completion_only_loss`、LoRA/PEFT 接口 | 需记录实际安装版和模板 Loss mask |
| TRL 官方 GRPOTrainer | https://huggingface.co/docs/trl/grpo_trainer | `GRPOConfig`、自定义 reward、`environment_factory` | 环境接口标明 transformers ≥ 5.2；不等于本地已测试 |
| Microsoft Agent Lightning v1.0 | https://github.com/microsoft/agent-lightning/blob/main/docs/README.md | Harness/Gateway/Trainer 解耦、v1.0 改版入口 | v0.x 教程不得直接当作 v1 运行命令 |
| verl 原始文档 | https://verl.readthedocs.io/en/latest/start/agentic_rl.html | 异步 Rollout、Agent Loop、LangGraph 多轮环境 | 按其 revision/对应实现核查 |
| DeepSeekMath、R1 原论文 | https://arxiv.org/abs/2402.03300 · https://arxiv.org/abs/2501.12948 | GRPO 与推理 RL 的原始研究 | 论文结论不是个人硬件的实测结果 |
| OpenAI Spinning Up | https://spinningup.openai.com/en/latest/spinningup/rl_intro.html | RL 经典数学与 MDP 入门 | 不是当前 TRL 的 API 操作手册 |

**静态检查局限**：本仓 GitHub CI 能核对本地 Markdown 相对路径、教学脚本/数据/Reward，不会保证外部文档未来始终有效，也不会验证随机库版本和用户 GPU 驱动兼容。访问外部资料应记录日期、URL、版本与替代源。引用第三方论文/文档，不复制受版权保护的大段内容。

## 3. 本轮实际修复项

1. 新增 [数据、奖励与严格格式检查](experiments/mini-posttrain-sft-grpo/data_and_reward.py) 和 [标准库单元测试](experiments/mini-posttrain-sft-grpo/test_data_and_reward.py)：train/dev/test 操作数范围隔离、SHA-256、错误数值/尾随文本 Reward Hacking 负例。
2. 新增 [可选择执行的 TRL 训练脚本](experiments/mini-posttrain-sft-grpo/train_with_trl.py)：`data-check`、`preflight`、`sft`、`grpo`、`eval` 五个入口；LoRA SFT 后**沿用训练出的 SFT adapter**做 GRPO，保留独立 eval。
3. 新增 [完整实操手册](experiments/mini-posttrain-sft-grpo/README.md)：环境/模型版本核验、命令、输出路径、显存风险、真实训练证明条件及失败矩阵。它是既有实验 03+05 的横向补充，**不是新的强制训练阶段**。
4. 补强 README / M08 / 03 / 05 / 来源导航与原有 CI 的可发现性，不改变 12 模块、五类训练实验及 01–06 的状态契约。

## 4. 严格状态分层

| 层级 | 何种证据才可宣称通过 | 当前结论 |
|---|---|---|
| 文档 | 内链/必需文件/分类术语/结构一致 | 已在 PR #17 首次 CI run 43615096128 的 docs 任务通过 |
| CPU 教学 | 标准库测试、数据独立性、奖励负例 | 已在 PR #17 首次 CI run 43615096128 的 docs 任务通过；非 LLM 训练 |
| 真实单轮 GRPO | CUDA 真实日志、模型参数/adapter 更新、独立 dev/test、失败分析 | **NOT RUN** |
| 真实多步 Agentic RL | 可重置的环境、LLM tool rollout、token mask、真实策略更新、A/B/C 独立对照 | **NOT RUN** |
| 学员个人能力 | L0–L4 Rubric 的自主复述、动手、诊断和陌生迁移证据 | **NOT ASSESSED** |
| 生产上线 | G0–G8 工程/安全门禁 | **NOT ASSESSED** |

结论：**仓库的学习入口和实验设计可以完整覆盖原七部分，但 CPU 合成实验通过不等于用户已经训练出 Agentic RL 模型**。文档/CI 结果应与真实 GPU、最终测试结果明确分开。实现日志以 GitHub Actions 同一 commit 的真实结论为准。

## 5. GitHub Actions 验收证据

- [PR #17 首次完整测试](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/actions/runs/43615096128)：针对提交 `6a119521d95c8df985071f3f98fb02ed6e1a305e`，`docs` 与 `cpu-toy` 均为 **SUCCESS**。
- `docs` 明确包含：仓库模块/状态/相对链接检查、需求索引与 Atlas 校验、DPO/GRPO 数学负例、**新算术数据与奖励单测、训练脚本语法检查**、Agentic Q-learning CPU 实验。
- `cpu-toy`：保留既有 TinyGPT/Shift-Mask 等 CPU 教学链路测试。
- 此结果只对所指提交负责，合并主分支后需再次核对对应 push run；**未运行 GPU 训练，未生成真实模型效果指标**。
