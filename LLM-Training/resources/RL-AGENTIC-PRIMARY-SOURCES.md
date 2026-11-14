# RL / Post-training / Agentic RL：权威原始资料导航

> 复核时间：**2026-11-14**。优先作者论文、研究机构与项目官方文档，**只引用链接不复制第三方内容**。此表是课程导航，不是每个版本都在本地安装通过。课程与代码接口可能变化；再次使用记录访问日期、Git SHA、安装版本和不兼容说明。P0=原始论文/项目原文，P1=作者/机构公开课程；P2=社区辅助阅读，不用于单独支撑结论。

## 先用 8 个核心来源完成闭环

| 类型/优先级 | 原始链接 | 重点内容 | 作业/验收 |
|---|---|---|---|
| RL 基础 / P1 | [OpenAI Spinning Up: Key Concepts](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html) | MDP、Return、Value、policy、on/off-policy；**经典 RL 教材，不是 LLM Agent 专项 API** | 画 \(s,a,r,s'\)，解释 \(V,Q,A\) |
| 预训练 / P1 | [Stanford CS336](https://cs336.stanford.edu/) | Tokenizer、CE、优化、Scaling、GPU/数据 | Base vs SFT loss 的数据与监督区分 |
| RLHF / P0 | [InstructGPT](https://arxiv.org/abs/2203.02155) | SFT→Reward Modeling→PPO **历史配方** | 说出 RM ≠ Critic ≠ Reward |
| DPO / P0 | [DPO 原论文](https://arxiv.org/abs/2305.18290) | preference margin / reference / beta | 手算 chosen/rejected，并说明不依赖实时 Rollout |
| GRPO / P0 | [DeepSeekMath](https://arxiv.org/abs/2402.03300) | Group Relative Policy Optimization | 手算零方差并比较 PPO 的 value 需求 |
| 推理 RL / P0 | [DeepSeek-R1](https://arxiv.org/abs/2501.12948) | RLVR、冷启动、蒸馏/后训练实验路径 | 区分模型案例与通用流程 |
| Agent 后训练课程 / P1 | [Hugging Face: A curriculum for post-training agents](https://huggingface.co/blog/huggingface/train-agents) | SFT→蒸馏→GRPO→环境→Harness/异步训练 | 画出环境状态与模型训练器的两侧 |
| Agentic RL 工程 / P0 | [Microsoft Agent Lightning v1.0 docs](https://github.com/microsoft/agent-lightning/blob/main/docs/README.md) | 真正 Agent Harness + Gateway/Rollout Controller/Trainer | 解释为何执行链路和模型更新必须解耦 |

## 官方实现源码与接口（配置随版本变化）

| 优先级 | 资料 | 应看部分 | 校验要求 |
|---|---|---|---|
| P0 | [TRL SFTTrainer](https://huggingface.co/docs/trl/sft_trainer) | assistant_only_loss、chat template、mask | 一条 tool 消息的 token/labels 核对 |
| P0 | [TRL DPOTrainer](https://huggingface.co/docs/trl/dpo_trainer) | policy/ref chosen/rejected | Reference 与 beta 配置复核 |
| P0 | [TRL PPOTrainer](https://huggingface.co/docs/trl/ppo_trainer) | PPO actor、value、reward、rollout | 与 GRPO 部件对照 |
| P0 | [TRL GRPOTrainer](https://huggingface.co/docs/trl/grpo_trainer) | tools、environment_factory、get_reward、KL、group std | **务必按当期版本检查**；当前文档环境接口注明需要 transformers>=5.2.0 |
| P0 | [TRL AsyncGRPOTrainer](https://huggingface.co/docs/trl/async_grpo_trainer) | 异步 Rollout、策略版本、新旧轨迹 | 标注实验策略滞后及恢复限制 |
| P0 | [Microsoft Agent Lightning v1.0](https://github.com/microsoft/agent-lightning) | README / docs / examples / releases | 注意 2026 v1 已重构，勿直接照抄旧 v0.x 教程 |
| P0 | [verl Agentic RL Training](https://verl.readthedocs.io/en/latest/start/agentic_rl.html) | Server 异步 Rollout、多轮 Tool Call、LangGraph | 按使用的 verl revision 核对 AgentLoop 接口 |
| P0 | [verl 源码](https://github.com/verl-project/verl) | Actor/Rollout/Reference/Value、Agent loop、Reward loop | 记录 PyTorch/vLLM/Ray 兼容矩阵 |
| P0 | [Hugging Face PEFT](https://huggingface.co/docs/peft/index) | LoRA/QLoRA 目标与权重保存 | 验证哪些权重实际更新 |
| P0 | [Qwen3-0.6B Base Model Card](https://huggingface.co/Qwen/Qwen3-0.6B-Base) | Model license、revision、基础模型约束 | 检查模型与工具模板是否匹配 |

补充：[TRL 官方安装](https://huggingface.co/docs/trl/installation) · [PyTorch reproducibility](https://pytorch.org/docs/stable/notes/randomness.html) · [HF datasets](https://huggingface.co/docs/datasets/index)。

## 阅读与落地顺序（按当前问题选择，不要求全读）

- **分类困惑**：Spinning Up → [跨模块关系](../knowledge-graph/pretrain-posttrain-relations.md) → InstructGPT/DPO/DeepSeekMath。
- **先会 GRPO**：[数学 Lab](../labs/preference-rl-math/README.md) → TRL GRPO 官方源码/文档 → [16GB Playbook](../reinforcement-learning/grpo-16gb-playbook.md)。
- **想理解 Agentic RL**：HF Agent 后训练课程 → [Agentic RL 学习路径](../reinforcement-learning/AGENTIC-RL-LEARNING-PATH.md) → [标准库环境 Lab](../labs/agentic-rl-trajectory/README.md)。
- **实战 Agent Harness RL**：TRL tools/environment_factory → Agent Lightning v1.0 docs → verl Agentic RL；从简单可重置环境再到真实业务。需要安全/审批的真实动作只在 Mock 测试，不连接生产接口。

## 核验与版本漂移记录模板

```text
source_url / checked_at / document_revision_or_commit
needed_feature / installed_library_version / feature_present(Y/N)
minimal_repro_command / expected_observation / observed_observation
compatibility_break / fallback / linked_experiment_run_id
```

**已发现的明确风险**：官方 TRL GRPO 当前 Agent Training 页面使用 `environment_factory`、`tools`，早期资料可能没有这些接口；当前环境示例注明 `transformers>=5.2.0`。Agent Lightning 2026 v1.0 与旧 v0.x 架构有明显差别。不要将未核实的旧命令当成固定“可直接运行”配置。

**外链质量标准**：官方身份/作者 → 可稳定定位原文 → 与当前目标直接相关 → 可记录版本 → 具有可测行为。**每次复验外链状态不能依靠本仓 CI 本地链接检查**；CI 主要验证相对路径和教学代码。

拓展关联：[M08](../modules/M08.md) · [Agentic RL 实验桥](../experiments/agentic-rl-bridge/README.md) · [实验规范](../experiments/EXPERIMENT-TEMPLATE.md)。

## 2026-11-15 严格复验：官方接口版本与可执行训练之间的桥梁

- 已重查 [Hugging Face Agent 后训练课程](https://huggingface.co/blog/huggingface/train-agents)，原文标记发布时间 **2026-10-20**，介绍 SFT/蒸馏/RL/环境/Harness 的学习顺序；不能当成所有模型必须遵循的固定训练流程。
- [TRL SFTTrainer](https://huggingface.co/docs/trl/sft_trainer) 官方文档：`prompt-completion` 数据可启用 `completion_only_loss=True`，LoRA 可通过 `peft_config` 训练；Chat 的 `assistant_only_loss` 则依赖有效 generation mask/chat template，不能混同。
- [TRL GRPOTrainer](https://huggingface.co/docs/trl/grpo_trainer) 官方文档：有可自定义 `reward_funcs` 与 Agent `environment_factory`；目前文档注明 Agent 环境 API 需要 **transformers>=5.2.0**，并非所有历史发行版都具备。
- [Agent Lightning v1.0 docs](https://github.com/microsoft/agent-lightning/blob/main/docs/README.md) 和 [verl Agentic RL](https://verl.readthedocs.io/en/latest/start/agentic_rl.html) 均可访问；Agent Lightning v1.x 与旧 v0.x 不可无检验混用。
- 新增 [小模型 SFT→GRPO 实操](../experiments/mini-posttrain-sft-grpo/README.md) 是**仓库自编的可审计参考脚本**，不同于官方已经实测通过的配方。只允许在真实安装版本与本机 CUDA 验证后写 PASS；CPU 单测不验证官方运行时 API 兼容。
- 一体化覆盖证据与对照详见 [严格验收审计](../ACCEPTANCE-RL-AGENTIC-STRICT-20261115.md)。本资料表只包含原始来源，不使用来历不明的汇总博文替代论文/文档。
