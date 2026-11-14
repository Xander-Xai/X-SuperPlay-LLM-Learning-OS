# RL / Agentic RL 与大模型预训练、后训练｜需求驱动完整学习路径

> **定位**：M04（Pretrain）→ M06（SFT）→ M07（Preference）→ M08（RL/Agentic RL）→ M09（训练系统）→ M10（评估）的跨模块导图，不增加第 13 个模块；是学习设计，**不是 GPU 训练完成证据**。资料复核日期：2026-11-14。学习深度以 [L0–L4 Rubric](../assessments/CAPABILITY-RUBRIC.md) 为准。

## 1. 四者不是同层概念

| 名称 | 是什么维度 | 核心训练信号 | 目标 | 不要误认为 |
|---|---|---|---|---|
| Pretraining 预训练 | **训练阶段** | 自回归下一 Token CE，常见但非唯一形式 | 得到 Base 模型 | 训练 Loss 小就能执行 Agent |
| Post-training 后训练 | **训练阶段/阶段集合** | SFT、偏好、RL、蒸馏等多种信号 | 改善指令、对齐、推理和任务行为 | 必须固定经过 SFT→DPO→PPO |
| RL 强化学习 | **优化范式** | 与策略动作相关的 Reward/Return/Advantage | 提高期望回报 | 后训练的同义词；RL 必须使用人类标签 |
| Agentic RL | **交互场景下的 RL** | 多步工具/环境 Rollout、轨迹反馈、策略更新 | 改善 Agent 决策与行动序列 | LangGraph + 工具日志 = Agentic RL |

正交概念：**PPO/GRPO** 是策略优化算法；**RLHF** 描述人类反馈来源/训练配方；**RLVR** 强调可验证奖励；**DPO** 通常用离线偏好对直接优化、不是在线 Rollout RL；**LoRA/QLoRA** 是参数高效更新技术。GRPO 可以用于可验证问答，也可用于具备相容环境接口的 Agent，多者并非互斥。

直觉：预训练让模型“会表达”，SFT 让模型“学示范”，DPO 让模型“偏爱合适输出”，RL 让模型“通过奖励学习”，Agentic RL 让它“通过多步行动后果学习”。这只是学习类比，实际能力来自数据、模型、目标与评估的共同作用。

## 2. 从语言模型到能学习的 Agent：两个不同闭环

### Base/Chat/Reasoning 训练闭环

```text
语料 → tokenizer/packing → next-token CE → Base
  └─ 指令/工具轨迹 → assistant-only SFT CE → Instruct/Tool Agent Policy
                        ├─ chosen/rejected → DPO/偏好优化
                        └─ on-policy rollout → 验证器/RM → PPO/GRPO 等 RL → eval
```

- Pretrain、CPT、SFT 可能都用 CE，但**初始化、数据分布、Loss mask、评估目标**不同。
- “能力形成”是连续的，不能按单篇论文把 Base/Instruct/Reasoning 理解成普适固定流水线。
- 经典 InstructGPT 给出 SFT→Reward Model→PPO 的历史例子；DeepSeek-R1 提供推理 RL 和冷启动/蒸馏实例，二者不是每个产品的强制训练步骤。

### Agentic RL 训练闭环

```text
任务 / 可重置环境
   ↓ reset（固定任务 ID、seed、快照）
Agent Harness（Prompt/Context/工具权限/超时/重试）
   ↓ LLM 采样动作 / tool call（policy θ）
工具执行 → 环境观测 → 新动作 → … → done / max_steps
   ↓ trajectory（含观测、可训练动作 token、工具错误、状态变化）
任务验证器 + Safety gate → terminal / step reward
   ↓ advantage / credit assignment / policy objective
Trainer 更新 θ（或 LoRA adapter）
   ↓ 独立 held-out 环境评估 + 长度/延迟/费用 + 回归
更新或回滚；绝不直接拿训练 Reward 当真实任务成功率
```

**必要区别**：Agent 只执行、仅调整 Prompt、或离线做行为分析，均不构成 Agentic RL。必须至少存在动作/策略相关训练反馈和**真实策略参数更新**；测试轨迹、优化工具 schema 本身不能假冒模型 RL。已有 [Agent Harness 工程笔记](../application-engineering/AGENT-HARNESS-ENGINEERING.md) 负责执行层，本页负责训练层。

## 3. 核心数学和工程变量

最小形式：观测 \(o_t\) → 策略 \(\pi_\theta(a_t \mid h_t)\)（历史 \(h_t\) 包含消息、工具观测、可见状态）→ 动作 \(a_t\) → 环境反馈 \(o_{t+1},r_t\)。轨迹 \(\tau=(o_0,a_0,r_0,\ldots,o_T)\)，有限回报 \(R(\tau)=\sum_t\gamma^t r_t\)。目标 \(J(\theta)=\mathbb{E}_{\tau\sim\pi_\theta}[R(\tau)]\)。一类策略梯度使用 \(\nabla_\theta\log\pi_\theta(a_t\mid h_t)A_t\)；PPO 用裁剪目标限制单次偏移。**这些只是原理级表达，不是 GRPO 或 Agentic RL 全部实现。**

GRPO 的入门近似：对同一 prompt/**同一起始状态**生成 G 条轨迹，用 \(A_i \approx (R_i-\bar R)/(\sigma_R+\epsilon)\) 做组内相对优势。版本差异涉及组标准差、是否 KL、截断/长度归一化、token mask、importance sampling，**以当前 TRL/verl 具体配置为准**。若同组全相同奖励，优势信息不足；若不同轨迹初始环境不同，组内相对奖励可能混入环境难度差异。

| 术语 | 专业意义 | 易错边界 |
|---|---|---|
| State / Observation | 环境真实状态 vs Agent 可见信息 | 不把订单真实资格提前泄露到策略输入 |
| Action / Tool Call | 可训练模型输出和外部执行调用 | 工具结果 token 与模型动作 token 不能无差别计 Loss |
| Rollout / Trajectory | 一次完整任务多步交互及关联 token | 需要轨迹 ID、episode ID、重试 ID、终止原因 |
| Reward / Return | 局部反馈与全程折扣/终局回报 | 成功、合规、格式必须分项记录，安全门禁不能被奖励抵消 |
| Advantage / Credit Assignment | 哪些动作真正改善结果 | 末尾成功不意味着每步工具选择都正确 |
| On-policy / Off-policy | 轨迹来自当前策略还是旧策略 | 异步更新造成策略滞后，应记录版本并审视校正机制 |
| Agent Harness / Trainer | 执行上下文/工具控制 vs 更新模型参数 | 两者接口可拆分，但版本与 tokenizer 必须一致 |

## 4. 从旧项目能力映射到学习差距

| 已有能力入口 | 可复用 | 需要新补的训练能力 |
|---|---|---|
| RAG 检索与 Evidence Gate | 独立任务数据、拒答/证据成功标准 | 可验证奖励、检索工具多步轨迹、污染/泄漏隔离 |
| LangGraph 多 Agent + Function Calling | 状态机、工具协议、Checkpoint、幂等 | 环境 reset/rollback、token 级训练轨迹、reward grader 与 credit assignment |
| LoRA/QLoRA SFT | 参数更新、数据格式、checkpoint | On-policy 采样、GRPO/TRL、策略漂移、训练/推理切换 |
| 任务级 Eval | 任务成功/工具正确/安全与延迟 | 固定独立环境，组内方差、KL/Clip、奖励投机定位 |

这只是技能迁移建议，不宣称已有项目实现过 RL。

## 5. 按问题选择学习入口（不是机械先修）

| 当前问题 | 最小前置 | 先完成的证据 | 深入资料 |
|---|---|---|---|
| 不理解 Base/SFT/RL 关系 | M04→M06→M08 原理 | 能解释 CE vs Reward、LoRA vs 算法 | [训练生命周期](../knowledge-graph/TRAINING-SIGNAL-AND-LIFECYCLE.md) |
| PPO、DPO、GRPO、RLVR 混乱 | 概率/对数概率、M07/M08 | 手算 DPO margin、GRPO zero variance | [数学 Lab](../labs/preference-rl-math/README.md) |
| Agent 能跑、却不知道能否学 | 工具调用、State、Harness | 用同一任务比较固定动作、规则策略与训练后策略 | [多步环境 Lab](../labs/agentic-rl-trajectory/README.md) |
| 奖励涨但效果不涨 | M08/M10 | 反例：格式奖励/数据泄漏/违规执行 | [评估协议](../evaluation/evaluation-protocol.md) |
| 准备真实 Agentic RL | M06、GRPO、复位环境 | 完整 run_id/实验计划、独立测试 | [Agentic RL Bridge](../experiments/agentic-rl-bridge/README.md) |
| 训练难以扩容 | M09、异步/分布式 | 能画 Actor/Reference/Rollout/Trainer、解释 stale policy | [权威来源表](../resources/RL-AGENTIC-PRIMARY-SOURCES.md) |

## 6. 可选 28 天深度路线（每周有退出条件）

这个“28 天”只是控制投入的参考，不构成固定课表。依据需求选一张卡→补必要前置→产出证据→结束。

| 阶段 | 核心主题 | 最小交付（L0–L4 按真实证据评级） |
|---|---|---|
| W1 / D1–7 | CE、SFT、奖励、Bellman、policy gradient、PPO、DPO、GRPO 分类 | 关系图 + 5 个闭卷追问 + DPO/GRPO 数学测试及失败解释 |
| W2 / D8–14 | TRL SFT/GRPO 文档、LoRA、16GB 资源门槛、分组采样 | **预演**完整配置、评估切分、reward 防投机；如有 GPU 真跑则单独附日志 |
| W3 / D15–21 | Harness、可重置订单/工具环境、轨迹、任务安全 | 标准库多步环境测试 + 冻结/规则/小型可学习策略对照，解释 toy 与 LLM 的区别 |
| W4 / D22–28 | verl / Agent Lightning / Agent GRPO，异步系统与归因 | 真实训练的可执行 runbook + 瓶颈/失败矩阵 + 面试架构复盘；未执行保持 NOT RUN |

**16GB 显存起点**：先 CPU toy → 0.6B 级模型、LoRA、短上下文/少量候选、原生 TRL；验证 CUDA/torch/transformers/trl/peft 的组合后再试 Unsloth/vLLM。多步环境长轨迹和 GRPO 多候选会增加 KV、激活及时间成本，不保证某组合能跑或提升；严禁提前编造 VRAM 与吞吐数值。

**更适合现实求职的时间配比建议**：应用工程化主线优先，再用 M04/M06/M07/M08 补模型训练认知，Agentic RL 先达到“能讲机制、会做最小对照”，明确要求 RL 算法岗位时再加大投入。

## 7. 模拟客服退款的训练设计（仅合成、无真实退款权限）

- Task：订单退款申请；环境真值含是否符合政策、是否需审批；策略只在工具核查后看得到可见信息。
- Actions：lookup / check_policy / request_approval / refund / deny（工具调用只能在模拟沙盒生效）。
- **优先硬门禁**：超权限退款永远被阻断，不能用负奖励代替工具权限控制。
- Reward 分项：完成正确且安全的任务 +，越权/错误 -；调用成本/延迟单独报告，不因“格式漂亮”盖过任务错误。
- Train split：合成订单 ID/模板/参数按固定规则划分；同一订单不能跨 train/held-out；最终测试只用一次，反复调参应另设 dev。
- 比较组：A 冻结策略+现有 Harness；B A 的 SFT 轨迹训练；C 相同 SFT 初始化+RL。模型、工具协议、数据规模、计算预算、评测器均须明确，若预算不匹配则只作观察性比较。
- 主指标：任务成功率；护栏：违规动作/错误副作用、拒答正确率、延迟、tokens/工具次数。报告置信区间或样本数，并按错误类型切分。

## 8. 反例与排障顺序

1. **Reward hacking**：仅对 JSON 或长度打高分，实际退款错误。先手工审查 10 条负例，再修改 verifier；真实目标和训练评分分开测。
2. **稀疏/零方差**：所有同组轨迹同分。审查任务难度、奖励区分度、采样温度/初始策略，而非盲目增加步数。
3. **环境泄漏**：资格、测试集标签或真实订单状态被提前注入 prompt。检查工具观测和 split。
4. **轨迹归因**：工具 timeout、重试、伪造观察写回了训练的 model action token。按消息角色、token mask 与前缀一致性审计。
5. **策略滞后**：异步 actor 产生旧版本轨迹；记录 actor/policy/reference revision 与训练消费时间。
6. **系统误差**：OOM、tokens 截断、训练 tokenizer 与推理 tokenizer 不一致。先排系统和 Chat Template，再讨论 RL 算法。

## 9. 适合面试的 10 个验证问题

1. 什么是训练阶段，什么是训练方法？CPT/SFT 与 LoRA/QLoRA 有何正交关系？
2. 为什么 PPO/GRPO 是算法，而 RLHF/RLVR 是反馈/训练路线？
3. DPO 什么时候不是在线 RL？自采样偏好数据冻结后算不算 on-policy？
4. State、Observation、Action、Reward、Return、Advantage 差在哪？
5. Agent 日志和 Agentic RL 训练轨迹的本质差别？
6. 为什么 group reward 全等时 GRPO 难以给出有效优势？
7. 如何给多步工具动作做 terminal reward 与 credit assignment？
8. 权限/审批为什么不能完全依赖 reward penalty？
9. 如何避免工具返回的文字被误当可训练 action token？
10. 为什么完整任务成功率、成本、违规率、训练 Reward 必须同时看？

**退出标准**：至少答出每问的机制、一个反例、可运行/可检查证据；真实 GPU/Agentic RL 训练没执行就保持 NOT RUN。后续：[官方资料索引](../resources/RL-AGENTIC-PRIMARY-SOURCES.md)、[实验桥](../experiments/agentic-rl-bridge/README.md)、[实验模板](../experiments/EXPERIMENT-TEMPLATE.md)。

## 10. 七部分资料严格复验后的 P0/P1/P2 取舍与真实训练入口（2026-11-15）

| 优先级 | 当前先做什么 | 合格证据 |
|---|---|---|
| P0 基础 | M04 Transformer/Pretrain、M06 SFT/LoRA/QLoRA，M07 DPO，M08 RL/PPO/GRPO/RLHF/RLVR | 能画 Base→SFT→RL 关系图，讲清 CE、偏好目标、奖励、Advantage、KL 和每种方法的边界 |
| P0 Agent 实践 | Harness、Tool Calling、轨迹、独立评估与权限硬门禁 | 用 [合成沙盒](../labs/agentic-rl-trajectory/README.md) 区分任务执行与参数更新 |
| P1 实践 | 0.5B–1.5B 规模的 LoRA SFT、RLVR GRPO、独立对照 | 按 [小模型 SFT→GRPO runbook](../experiments/mini-posttrain-sft-grpo/README.md) 留下真实模型 checkpoint、日志与 held-out 结果；没有 GPU 运行保持 NOT RUN |
| P1 Agentic RL | Rollout、Reward、Credit Assignment、多轮重置 | 使用 [多步环境实验桥](../experiments/agentic-rl-bridge/README.md) 构建同基线 A/B/C，不能只给代码截图 |
| P2 进阶 | verl、Agent Lightning、异步 Rollout/分布式训练 | 识别 Actor/Trainer/Reference/Reward/Environment 边界、异步策略滞后，按岗位再深入 |

**对 AI 应用工程求职的起始投入建议：70% RAG/Agent/后端工程化、20% 预训练与后训练原理、10% Agentic RL 小实验**；不是行业统计或硬性比率，RL 算法岗可提高后两项权重。已有项目经验不是自动通过本仓 L0–L4 的证明。

第 2 周原定“小模型后训练”现在有[实际命令与评估流程](../experiments/mini-posttrain-sft-grpo/README.md)：先做离线数据/Reward 单测，再在**用户 GPU 上实际运行** LoRA SFT→GRPO→dev/test 对照；当前仅完成代码落盘和 CPU 测试设计，不能预填 GPU PASS。第 3 周的表格 Q-learning 是 Agent 环境结构教学，真正多轮 **LLM Agentic RL** 仍另行验收。[七部分完整核对表](../ACCEPTANCE-RL-AGENTIC-STRICT-20261115.md)。
