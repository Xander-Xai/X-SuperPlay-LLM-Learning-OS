# 大模型训练信号总图｜一批数据怎么变成一个助手

> 这是一份跨 [M01–M12](../README.md) 的概念对照卡，目的是把训练“阶段、优化目标、输入输出、适用时机”串起来。它不是额外训练阶段或强制学习顺序。实际实验从 [需求路由](../demand-driven/README.md) 进入。

## 1. 建模链路与使用链路不是一回事

~~~mermaid
flowchart TD
  DATA["原始语料→清洗/许可/去重→Tokenizer"] --> BASE["Decoder 模型初始化+Pretrain<br/>Next Token CE→Base"]
  BASE --> CPT["可选 CPT/Mid-Training<br/>领域/长上下文数据"]
  BASE --> SFT["SFT / LoRA / QLoRA<br/>任务轨迹/Assistant Mask"]
  CPT --> SFT
  SFT --> DPO["偏好优化 DPO / ORPO（分支）"]
  SFT --> RL["在线奖励优化 PPO / GRPO（分支）"]
  BASE --> SERVE["评测→推理服务"]
  SFT --> SERVE
  DPO --> SERVE
  RL --> SERVE
  SERVE --> USE["Prompt/Context → RAG/Tools/Agent"]
  USE --> EVAL["任务级正确性/安全/延迟/成本/反馈"]
  EVAL -. "确认数据/目标问题后迭代" .-> DATA
~~~

这张图只是主干：**CPT、DPO、GRPO 不是人人必走**；Distillation 可以在不同阶段发生；数据、评估、隐私和安全贯穿整个流程；LoRA/QLoRA 是参数更新技术，不是 Pretrain→SFT 之间另一个时间阶段。

## 2. 一次 Pretrain Batch 的机制（专业 → 白话）

假设 Decoder-only 模型接收 ID 序列 [x₀, x₁, …, xT]：

1. **数据/Tokenizer**：把文本映射成整数 ID，并形成训练 Batch。像把原料分类、编号装盒；这里的质量和污染会决定模型到底学到什么。
2. **Embedding + Transformer**：输出每个位置的 Logits [B,T,V]，包含每个词表 ID 的预测分数。像在写一句话时不断预测下一个字。
3. **Causal Attention**：位置 t 只能使用 t 及之前输入，不能偷看未来。像考试规定不能看到后面的标准答案。
4. **Cross Entropy**：对各有效位置 t 的下一个 Token 取负对数似然。形式可记为 \(\mathcal L=-\frac{1}{N}\sum_{t \in \mathrm{valid}}\log p_\theta(x_{t+1}\mid x_{\le t})\)。只有需要的有效位置计入 Loss；**Trainer/模型只能做一次 Shift**。
5. **Autograd/Backward**：计算参数梯度 ∇θL。像确定导致预测错误的机器零件及误差方向。
6. **AdamW / Scheduler**：根据梯度和优化器历史状态更新参数；记录 LR、Loss、Tokens/Sec、显存。像持续微调生产设备。
7. **Checkpoint/验证**：保存 Model、Optimizer、Scheduler、RNG、采样进度，单独在未训练数据上评估。像不仅存结果，还把过程状态完整存档。

**训练和生成的时间维度不同**：训练阶段在 Causal Mask 约束下对许多位置的下一个 Token Loss 做并行计算；生成阶段一般自回归逐 Token 解码，并利用 KV Cache 缓存历史状态。这是 [M03](../modules/M03.md)、[M04](../modules/M04.md)、[M11](../modules/M11.md) 的关键联系。

## 3. 为什么一个库存工具任务会经过不同阶段？

场景：用户说“查询产品 A 的库存，按 JSON 返回”。

| 阶段 | 专业训练信号 / 操作 | 大白话 | 它**不能**单独保证什么 |
|---|---|---|---|
| Base Pretrain | 基于原始文本 Next Token 自监督训练 | 学会“库存、产品”这些语言模式 | 不保证会解析业务参数/合法调用工具 |
| CPT | 在授权领域语料上继续语言建模 | 行业术语加强班 | 不保证最新库存真实且有权限 |
| Tool SFT | 用真实结构化轨迹训练 Assistant 的 Tool Call 和 Final；Tool Observation 需按 Mask 规则处理 | 给员工示范怎么填操作单和读仓库回执 | 不保证后端执行权限、幂等、安全 |
| DPO | 通过 chosen/rejected 与 Reference log-ratio 改变回答偏好 | 从两份候选中选择更值得信赖的回答 | 更偏好一个回答 ≠ 库存事实正确 |
| PPO/GRPO + RLVR | 在可验证环境中 Rollout，按 Reward/Advantage 更新策略 | 多轮练习并根据真实查到的结果反馈 | Reward 可能被投机；需要独立任务指标 |
| RAG / Tool Execution | 在推理阶段检索当前信息，由服务端身份检查后执行工具 | 允许员工**带资料**并请求有权限的工具 | 不改变权重，不能代替模型训练 |
| Eval/LLMOps | Tool Selection/Arguments/Execution/Citation/E2E、TTFT/P95/安全/回滚 | 看任务有没有真完成，是否能安全持续工作 | 演示成功不代表生产可靠 |

针对同一问题，不一定要训练：**先测试规则、Schema、Prompt、API 和工具网关**；若任务已达标，停止。必要时再做 SFT/Preference/RL。对应 [合成 Tool Gateway](../labs/synthetic-tool-gateway/README.md)、[M06](../modules/M06.md)、[M10](../modules/M10.md)。

## 4. 常见概念误区与直接实验

| 误解 | 正确机制 | 入口 |
|---|---|---|
| Pretrain/CPT/SFT 都有 CE，所以三者一样 | 任务数据分布、初始化点、角色 Mask、评估目标有根本区别 | [M04](../modules/M04.md)/[M05](../modules/M05.md)/[M06](../modules/M06.md) |
| GRPO 一定要先 DPO | 可以从同一个 SFT baseline 分叉；GRPO 还需要奖励/采样/优化链 | [DPO/GRPO 公式 Toy](../labs/preference-rl-math/README.md) |
| 训练 Loss 下降说明 Chat 效果好 | 训练集过拟合/数据污染/Chat 目标不一致都可使 Loss 与业务任务分离 | [Task Eval Toy](../labs/task-evaluation/README.md) |
| 模型有权限概念就能保障工具安全 | 权限强制在工具服务器执行，模型输出只是未经信任的意图 | [合成 Tool Gateway](../labs/synthetic-tool-gateway/README.md) |
| TinyGPT Toy 代表完整预训练成功 | 字符级重复语料上的 Loss 下降只验证机制，无法证明真实模型泛化 | [实验 A](../labs/tiny-gpt/README.md) |
| DDP 就是 FSDP / TP | DDP 复制模型；FSDP 分片状态；TP 切分层；PP 切层深度；CP 切序列；EP 切专家 | [M09](../modules/M09.md) / [Megatron Core](https://docs.nvidia.com/megatron-core/developer-guide/latest/user-guide/parallelism-guide.html) |

## 5. 何时需要继续学习哪一个点？

不理解公式 → [TinyGPT CPU](../labs/tiny-gpt/README.md)；不理解训练前向/恢复 → [MiniMind](../experiments/01-minimind-whitebox/RUNBOOK-FIRST-DAY.md)；不理解领域知识 CPT vs RAG → [实验 02](../experiments/02-qwen-cpt-replay/README.md)；Tool Mask 错误 → [实验 03](../experiments/03-agent-tool-sft/README.md)；偏好结果下降 → [实验 04](../experiments/04-dpo/README.md)；GRPO 奖励投机 → [实验 05](../experiments/05-grpo/README.md)；模型能跑但服务不稳定 → [实验 06](../experiments/06-deployment/README.md)。

**专业资料**：[Stanford CS336](https://cs336.stanford.edu/)、[MiniMind](https://github.com/jingyaogong/minimind)、[Raschka](https://github.com/rasbt/LLMs-from-scratch)、[TRL](https://huggingface.co/docs/trl/index)。建议做 **问题/公式/源码/实验/失败/对照** 的短证据卡，而非机械复制整章内容。
