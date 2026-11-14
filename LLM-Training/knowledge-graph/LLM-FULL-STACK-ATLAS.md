# 大模型全链路知识总地图｜六域 × 12 模块 × 需求跳学

> **定位**：这是 [LLM Roadmap V3](../ROADMAP-V3-DEMAND-DRIVEN.md) 的**全栈放大镜**，不是新的一套与 M01–M12 冲突的模块编号，也不是将上游资料复制一份。上游知识依据为 [AI-Learning-OS 固定快照](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/tree/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a)；逐条资料见 [上游映射表](../resources/UPSTREAM-RESOURCE-MAP.md)。

## 0. 一句话：你要的不是“学完 12 章”，而是用完整地图按需跳学

**完整地图**保证知道有哪些能力；**关系图**保证明白它们为什么相连；**需求路由**保证今天从哪里开始；**可运行实验**证明学过的机制；**验收与生产门禁**判断能否独立解决问题和上线。

训练生命周期、实际应用的一次请求、个人学习顺序，是**三种不同的顺序**，不应强制统一。

## 1. 从建模到业务的全景图

~~~mermaid
flowchart TD
  D["需求/预算/基线<br/>先决定是否需要训练"] --> CH{"选择技术路径"}
  CH -->|参数训练| DATA["数据/Tokenizer<br/>M02"]
  CH -->|免训练| API["现成模型/API/规则"]
  DATA --> PRE["架构 + Pretrain<br/>M01/M03/M04"]
  PRE --> CPT["CPT 可选<br/>M05 Replay"]
  PRE --> SFT["SFT/LoRA/QLoRA 可选<br/>M06"]
  CPT --> SFT
  SFT --> PREF["DPO 可选<br/>M07"]
  SFT --> RL["PPO/GRPO/RLVR 可选<br/>M08"]
  PREF -.-> RL
  PRE --> EVAL
  CPT --> EVAL
  SFT --> EVAL
  PREF --> EVAL
  RL --> EVAL
  API --> EVAL["独立评估/回归<br/>M10"]
  EVAL --> SERVE["量化/合并/解码/Serving<br/>M11"]
  SERVE --> CTX["Prompt / Context Engineering"]
  CTX --> APP{"需外部知识或动作吗？"}
  APP -->|知识| RAG["Embedding/Rerank/RAG"]
  APP -->|动作| TOOL["Tool Calling / MCP<br/>服务端授权"]
  APP -->|无需工具| ANSWER["基础生成/结构化输出"]
  RAG --> AGENT["按需 Workflow / Agent / Memory"]
  TOOL --> AGENT
  AGENT --> OPS["LLMOps：安全/监控/回滚/成本"]
  ANSWER --> OPS
  OPS --> FB["脱敏反馈 + 冻结测试集"]
  FB --> D
  SYS["训练系统 M09<br/>显存/并行/恢复"] -.-> PRE
  SYS -.-> SFT
  SYS -.-> RL
  MM["多模态 M12：图/音/视频跨域"] -.-> PRE
  MM -.-> APP
  SEC["横切：评估/权限/治理/成本"] -.-> EVAL
  SEC -.-> OPS
~~~

**四条重要边界**：

1. RAG/Prompt/Context Engineering **不必改变模型参数**；“要做 RAG”不意味着要先学预训练。
2. CPT、DPO、GRPO 均为**按需**，SFT → DPO/GRPO 是常见对照起点，不是唯一强制串行训练链路。
3. LLM 只是 Agent 的一部分，完整 Agent 还有工具、环境、状态、审批、错误恢复、安全、评估；Workflow 可以不让模型自主决定流程。
4. 安全、评估、成本和多模态均是**跨域视角**，不是“最后学完其他章节才能学”的独立末尾课。

## 2. 六域与大白话类比

| 知识域 | 专业层：解决什么问题 | 大白话：在企业/工厂中像什么 | 对应当前学习模块 |
|---|---|---|---|
| **F 基础模型** | 数据、Tokenizer、Architecture、Pretrain、CPT、Multimodal | 培训一名新员工：准备教材、建立知识和基本技能 | [M01](../modules/M01.md)–[M05](../modules/M05.md)、M12 |
| **S 训练系统** | GPU/HBM、Kernel、数值精度、DDP/FSDP、Checkpoint | 训练学校的厂房、电力、分工和存档 | [M09](../modules/M09.md) + M01/M04 |
| **P 后训练** | SFT、合成数据、偏好对、Reward、DPO/PPO/GRPO | 岗前训练和考核：示范、评分、纠错 | [M06](../modules/M06.md)–[M08](../modules/M08.md) |
| **E 模型工程** | 评估、Decode、KV Cache、蒸馏、量化、Serving | 将训练好的员工安排进可承载高并发的生产车间 | [M10](../modules/M10.md)/[M11](../modules/M11.md)、M03 |
| **A 应用系统** | Prompt、Context、Retrieval、RAG、Tools/MCP、Agent、Memory | 给员工工作手册、资料库、工具、授权与任务流程 | M02/M06/M10/M11/M12 跨域 |
| **O LLMOps** | 测试、权限、安全、监控、版本、回滚、成本、治理 | 质量检测、审计、售后和运营成本控制 | M09/M10/M11 + [G0–G8](../production/PRODUCTION-READINESS.md) |

知识主权仍由上游 [六域 Atlas](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/README.md)、[多模态横切](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/multimodal-vertical.md) 和 [关系约定](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/relationship-rules.md) 维护；本仓负责跳学、解释与实操索引。

## 3. 生产应用的一次请求怎么走（与训练链路完全不同）

~~~mermaid
flowchart LR
  USER["用户 / 业务 API"] --> AUTH["认证/租户/权限"]
  AUTH --> ORCH["Workflow/Agent<br/>State/路由/审批"]
  ORCH --> CT["Context<br/>消息/证据/记忆"]
  CT --> L["LLM Inference"]
  L --> KIND{"生成答案还是使用外部能力？"}
  KIND -->|知识| RET["Retriever → Reranker → Evidence Gate"]
  RET --> CT
  KIND -->|动作| T["Tool Call → 服务端 ACL → 执行"]
  T --> OB["Observation/Timeout/Retry"]
  OB --> ORCH
  KIND -->|生成结果| V["Task/Citation/Claim 验证"]
  V --> RESP["用户响应"]
  RESP --> TRACE["Tracing/Feedback/Eval"]
  TRACE -.-> ORCH
~~~

**MCP 的位置**：Model Context Protocol 规范化 Host/Client/Server 连接和资源/工具协议；它不是 Tool Calling 的全部，也不保证自动授权、模型自主规划或运行安全。2026-07-28 官方规范使用无状态核心，SDK/第三方服务器仍需核对实际实现版本：[MCP 官方规范](https://modelcontextprotocol.io/specification/2026-07-28)。

## 4. 关系必须有含义，而不只是两点连线

~~~mermaid
flowchart LR
  TOK["Data/Tokenizer"] -->|供应训练输入| BASE["Base Model"]
  ATT["Decoder Attention"] -->|实现模型架构| BASE
  BASE -->|可直接训练| SFT["SFT"]
  BASE -->|可选领域延续| CPT["CPT"]
  CPT -->|可继续适配| SFT
  SFT -->|提供起点| DPO["DPO"]
  SFT -->|提供起点| GRPO["GRPO"]
  EVAL["Held-out Evaluation"] -.->|评测| DPO
  EVAL -.->|评测| GRPO
  EMB["Embedding/Rerank"] -->|提供证据| RAG["RAG"]
  SERVE["LLM API/Serving"] -->|提供模型能力| RAG
  SERVE -->|提供模型能力| AGENT["Workflow/Agent"]
  TOOLS["Tool Calling/MCP"] -->|提供动作接口| AGENT
  RAG -->|可以作为知识工具| AGENT
  ACL["后端认证授权"] -.->|保护| TOOLS
  TRACE["Tracing/Eval"] -.->|观察| AGENT
~~~

上图的关系方向十分关键。“RAG 可以是 Agent 的知识工具”不是“先学完 RAG 才能学 Agent”；“SFT 常是 GRPO 的起点”不是“所有 GRPO 必须经过同一 SFT”。机器索引内记录了 [30 条带类型关系](../index/upstream-knowledge-index.json)。

## 5. 容易混淆的 11 组专业概念

| 概念 | 专业区别 | 通俗理解 |
|---|---|---|
| Pretrain vs SFT | 自回归语言建模 vs 指令/任务行为监督，可能同用 CE 但分布/掩码不同 | 学会语言与世界知识 vs 学岗位规程 |
| CPT vs RAG | 更新领域模型权重 vs 推理时检索外部事实 | 重新学习知识 vs 临时查最新手册 |
| SFT vs DPO vs GRPO | 教师监督目标输出 vs 偏好对相对对数概率优化 vs 多候选奖励下更新策略 | 示范动作 / 两份答案择优 / 反复练习按分数纠偏 |
| Encoder vs Decoder | Encoder 适合双向表示，Decoder 主要用于自回归生成 | 图书管理员理解全文 vs 写作助手逐字续写 |
| Embedding vs Reranker | 向量召回表征 vs 对已有候选重新排序 | 先粗找书，再精挑真正相关的书 |
| RAG vs Fine-tuning | 外部证据更新 vs 改变参数中的行为/知识分布 | 开卷考试 vs 长期培训 |
| Tool Calling vs MCP | 模型发出结构化动作意图 vs 跨应用的工具/资源协议 | 员工填写操作单 vs 标准化工具插座 |
| Workflow vs Agent | 固定控制流 vs 动态选择下一步（两者可以结合） | 标准流水线 vs 能按反馈调整动作的员工 |
| KV Cache vs Checkpoint | 推理时复用历史 K/V vs 恢复训练需要模型/优化器/调度/RNG/采样状态 | 实时会议笔记 vs 完整存档 |
| Model Eval vs System Eval | 模型输出能力 vs 端到端权限/任务/引用/成本 | 单人考试成绩 vs 真能按时交付工作 |
| Token/s vs TTFT/P95 | 吞吐、首字时间、尾延迟衡量不同瓶颈 | 每小时出餐量不等于每桌等多久 |

知识依据：[Stanford CS336 2026](https://cs336.stanford.edu/)、[Hugging Face LLM Course](https://huggingface.co/learn/llm-course/en/chapter1/1)、[TRL 官方](https://huggingface.co/docs/trl/index)、[vLLM](https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/)、[HF Agents Course](https://huggingface.co/learn/agents-course/en/unit1/introduction)。

## 6. 怎么真正“按需，以点带面”

例如当前问题是“多轮工具调用经常乱填库存”：

1. 先做不训练基线：固定虚构或授权测试集，统计 Tool Selection、Argument、Execution、Evidence 与 E2E。
2. 按症状先跳 **A04 Tool Calling → A05 Workflow → M06 Tool SFT/Mask → M10 Eval**。如果错误是后端越权，直接跳 **O03 权限**，不需要微调。
3. AI 导师解释当前不懂的最小概念，给**专业定义、公式/接口字段、大白话类比、源代码入口和反例**；以权威来源核对。
4. 最小实操：[工具调用合成网关](../labs/synthetic-tool-gateway/README.md)；只有确有模型能力缺口，再启动 [Agent SFT](../experiments/03-agent-tool-sft/README.md)。
5. 改一个陌生任务验证迁移，如订单状态查询；一旦当前任务验收通过，**停止补课**，不必先读完 M01–M12。

直接使用：[需求路线卡](../demand-driven/AI-NATIVE-NEED-ROUTES.md) · [AI 原生学习闭环](../learning-method/AI-NATIVE-LEARNING-LOOP.md) · [33 主题搜索](../index/README.md)。

## 7. 学习验收与生产上线不能混淆

**L1 理解**：专业解释 + 大白话 + 反例；**L2 实现**：代码可执行和可修改；**L3 迁移**：陌生任务与排错；**L4 生产**：依 [G0–G8](../production/PRODUCTION-READINESS.md) 留下权限、SLO、监控、回滚和真实用户证据。

索引完成/CI 通过/CPU Toy 通过，只证明课程资产的局部正确性，**不证明 Qwen 已训练、个人已掌握或产品已上线**。本仓是学习系统，真实客户数据与部署证据由相应工程项目仓维护。
