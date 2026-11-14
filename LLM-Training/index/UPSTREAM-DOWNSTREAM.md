# 上游 AI-Learning-OS ↔ 本专项 LLM-Learning-OS：仓库分工与索引

## 1. 仓库的“上下游”不是产品开发的依赖链

| 层 | 唯一职责 | 不在此维护 |
|---|---|---|
| [AI-Learning-OS（上游）](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS) | 六域 L0–L3 Atlas、跨领域 canonical knowledge、需求/市场方法论、跨赛道成长 | 每个专项仓的实验副本和部署数据 |
| [LLM-Learning-OS（本仓）](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS) | LLM 专项学习路线、需求跳学、模块对照、权威来源索引、可复现课程小实验、个人能力验收方法 | 真实客户业务事实、私有数据、固定下游 SaaS 产品源码 |
| [MiniMind upstream](https://github.com/jingyaogong/minimind) / [Xander-Xai/minimind fork](https://github.com/Xander-Xai/minimind) | 模型机制和训练循环**实际代码来源与对照** | 本仓单独造另一份模型源码 |
| [Xander-Xai/mini_qwen](https://github.com/Xander-Xai/mini_qwen) / Transformers、TRL | 高层框架抽象对照；需要时阅读，不是第二门必须完整复现的基础课 | Canonical Knowledge 的独立副本 |
| 实际产品或业务项目仓 | 产品代码、部署、权限、SLO、真实实验日志、客户/运营事实 | 本仓课程叙述 |

**核心约定**：源代码与官方论文是证据；上游 Canonical Knowledge 是跨技术的稳定定义；本仓是能力训练入口、实验方法和版本化资料索引。源代码版本变化时先复核，再更新稳定定义；不把一段实现当普遍定律。

## 2. 三个一键入口

- 上游 [六域 Atlas](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/tree/main/docs/atlas) 与 [METHODOLOGY](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/main/METHODOLOGY.md)。
- 本仓 [Roadmap V3](../ROADMAP-V3-DEMAND-DRIVEN.md) / [需求路由](../demand-driven/README.md) / [机器索引](learning-index.json)。
- 上游现存的 [LLM 训练双仓 Trace](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/main/docs/projects/llm-training-dual-repo/README.md) 和 [旧深工程 Track](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/main/docs/tracks/deep-engineering/llm-training/README.md)，属于**可选对照与历史固定版本阅读**，不是强制每一项训练都跑 MiniMind+mini_qwen。

## 3. 不要把两个仓的“模块编号”直接当相同概念

上游历史深工程 Track 使用 M00–M17，针对双仓源码比较；本仓 V2/V3 使用 M01–M12，针对完整能力领域。编号仅本仓内部稳定，**名称相同不等于内容和评估要求相同**。

| 本仓知识域 | 上游旧 Track 可能相关模块 | 关键区别 |
|---|---|---|
| M01 数学/优化 | M03、M11–M13、M15 部分机制 | 本仓显式补基础与训练计算状态 |
| M02 数据/Tokenizer | M01、M03–M05 | 上游 M01 才是 Tokenizer，本仓 M01 是数学 |
| M03 Transformer | M02、M03 | 本仓包含 KV/Serving 连接 |
| M04 Pretrain | M03、M04、M16 | 共同目标为从数据到 CE/梯度 |
| M05 CPT | M04、M16 + 自定实验 | 旧 Track 没有独立等价 CPT 模块 |
| M06 SFT/PEFT/Tool | M05、M06 | 增加多轮工具、数据生成及 Chat Template |
| M07 Preference | M07–M10 | 偏好数据、DPO、RM、在线变体合并为知识域 |
| M08 PPO/GRPO/RLVR | M11–M14 | 优化算法与 RLVR 奖励 regime 必须分清 |
| M09 Training Systems | M15 | 除并行外还包含 Profile、恢复、资源建模 |
| M10 Evaluation | M16、M17 的验证部分 | 独立学习/生产全阶段评估 |
| M11 Compression/Serving | M15–M16 的部分应用 | 旧 Track 没有完全等价 Serving 模块 |
| M12 Advanced | 无完整一对一对应 | 多模态、MoE、长上下文等横向专题 |

**没有实施按同名 ID 自动同步**。需要复用某个原有 Track 时，以标题/内容和具体 SHA 而不是数字比对。

## 4. 证据与状态边界

- 学习仓的一页实验说明：`DESIGNED / NOT RUN`，不能被称为“已经训练完成”。
- 一个 CPU Toy 单测绿：只能证明该 Toy 的梯度/掩码合同；真实 Qwen Chat Template 和 GPU 模型训练另验。
- 一个运行过的实验：有固定模型/数据/revision/seed/环境与输出，最多证明该实验配置的结果。
- **本人能独立完成**：还需闭卷解释、未知样例迁移、故障修复；CI 不能代为评级。
- 真实项目上线：以实际项目仓的负载、安全、日志、回滚和用户/业务验收为准。

## 5. 更新索引和边界规则

1. 任何新需求先回 [需求卡](../demand-driven/DEMAND-CARD-TEMPLATE.md)。
2. 研究报告保留官方源码/文档原始出处、版本及适用范围。
3. 如果是跨领域稳定原理，建议向上游 Canonical Knowledge 提交简洁原理增量；如果只是 LLM 专项练习/配置，本仓维护。
4. 若来自 Career OS/OPC/真实客户任务，仅引用许可的脱敏证据，原始事实不复制进课程。
5. 如果要更新可检索结构，同时更新 [learning-index.json](learning-index.json) 并运行 [索引校验](../tools/validate_learning_index.py)；禁止同时维护两套不一致的机器索引。

