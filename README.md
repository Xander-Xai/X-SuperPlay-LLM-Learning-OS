## 新增：完整训练专项的实战与来源补全（2026-11-14）

[训练信号主干（专业原理/白话）](LLM-Training/knowledge-graph/TRAINING-SIGNAL-AND-LIFECYCLE.md) · [实验 A–E 与原 01–06 对照](LLM-Training/experiments/EXPERIMENTS-A-E-CROSSWALK.md) · [可执行手写 TinyGPT](LLM-Training/labs/tiny-gpt/README.md) · [六项能力单元（非六周课表）](LLM-Training/learning-method/SIX-CAPABILITY-UNITS.md) · [四个主资源职责与专项参考](LLM-Training/resources/TRAINING-SOURCE-ROLES.md)。

保留原 V3、M01–M12、六域 Atlas 与现有实验目录，不再建立一套冲突的 01–12 章节。新增 CPU TinyGPT 是教学运行，绝不代表 MiniMind/Qwen GPU 训练已完成。

## 再验收更新｜关系可反查 + 官方工程变更核查（2026-11-14）

[Atlas 关系探索](LLM-Training/index/README.md)现支持按主题查看入边/出边以及两个概念之间的**关联路径**；不会把关联路径误当成必修课程顺序。[TRL、vLLM、MCP 官方变化与上线检查](LLM-Training/resources/OFFICIAL-RUNTIME-DELTA-20261114.md) 已补入 M06/M08/M11 和生产门禁。[最新严格复验](LLM-Training/ACCEPTANCE-RECHECK-20261114.md)记录课程验证与尚未执行的模型实验。

## 新增：六域大模型全景与上游知识打通（2026-11-14）

现在先看 [**大模型全链路知识地图（专业原理 + 白话 + 关系图）**](LLM-Training/knowledge-graph/LLM-FULL-STACK-ATLAS.md)，再按当前问题进入 [**12 条需求驱动任务卡**](LLM-Training/demand-driven/AI-NATIVE-NEED-ROUTES.md)，沿 [**33 主题上游/官方直达索引**](LLM-Training/resources/UPSTREAM-RESOURCE-MAP.md) 找材料。也可以用 [AI-Native 导师学习协议](LLM-Training/learning-method/AI-NATIVE-LEARNING-LOOP.md) 做单点讲解与实操验收。

**核心理念**：知识地图完整 ≠ 要按地图逐章学习；按真实问题从任一点进入 → 最小前置 → 真实/合成实战 → 负例/迁移 → 达标停止。现有 M01–M12 与全部训练实验保留，不绑定任何固定下游产品。新增索引基于上游 2026-11-14 提交快照；课程 CI 不代表 GPU 训练或个人学习通过。

**查询示例**：python LLM-Training/tools/route_atlas.py --search RAG；另有 --need N02 / --topic A04 / --domain A。

---

## 当前入口：需求驱动的 LLM 专项学习 V3（2026-11-14）

**本仓是独立的 LLM 学习与能力验收体系，不是某个下游产品的交付代码仓。** 保留 V2 的 M01–M12、MiniMind 白盒与 Qwen3 实验；学习时按工程问题跳到对应模块，不必机械从第 1 章开始。生产能力通过多种可迁移切片验收，而不是让本仓绑定一个 Agent 项目。

- [Roadmap V3｜需求驱动扩展](LLM-Training/ROADMAP-V3-DEMAND-DRIVEN.md) · [按问题跳学](LLM-Training/demand-driven/README.md) · [知识依赖与能力关系图](LLM-Training/knowledge-graph/dependency-and-capability-map.md)
- [机器索引（12 模块 / 18 需求 / 20 来源）](LLM-Training/index/README.md) · [权威资料](LLM-Training/resources/AUTHORITATIVE-INDEX.md) · [上线门禁](LLM-Training/production/PRODUCTION-READINESS.md)
- [上游 AI-Learning-OS 的责任分工与旧 M00–M17 映射](LLM-Training/index/UPSTREAM-DOWNSTREAM.md)

**第三轮课程深入验收入口**：[12 模块 V3 原理+实战](LLM-Training/README.md) · [DPO/GRPO 数学实验](LLM-Training/labs/preference-rl-math/README.md) · [Agent 任务级评测](LLM-Training/labs/task-evaluation/README.md) · [V3 审计报告](LLM-Training/ACCEPTANCE-V3-AUDIT.md)。

**状态边界**：课程、索引与教学 CI 可以审查，但 MiniMind/Qwen GPU 实验仍需真实日志；学员能力和生产上线不因文档/CI 通过自动升级。

---

# X-SuperPlay-LLM-Learning-OS

需求驱动的大模型学习操作系统：覆盖基础架构、预训练、持续预训练、SFT、DPO、RL、评估、推理和工程化。核心原则：**知识地图完整、只维护一条底层实战主线、按问题跳学、用实验证据验收**。

> 2026-11-14：首期落地 **LLM Training Roadmap V2.0**；内容属于学习计划和实验规范，**不代表已经执行模型训练**。

## 开始学习

**首选总导航：[LLM-Training 学习中心](LLM-Training/README.md)**（12 个模块独立入口、4 个里程碑、5 类训练实验 + 1 个部署验收）。

0. [MiniMind 第一天操作手册](LLM-Training/experiments/01-minimind-whitebox/RUNBOOK-FIRST-DAY.md)：从环境检查、数据获取到 Pretrain→SFT 的可复制命令（尚未实际 GPU 运行）。
1. [训练全流程 Roadmap V2.0](LLM-Training/ROADMAP-V2.md)：12 模块、4 里程碑、学习时间与严格验收。
2. [完整训练链路与架构图](LLM-Training/knowledge-graph/full-training-pipeline.md) / [知识依赖与跳学导航](LLM-Training/knowledge-graph/concept-dependencies.md)。
3. [实验总入口](LLM-Training/experiments/README.md)：MiniMind 白盒 → Qwen CPT → Agent SFT → DPO → GRPO → 部署。
4. [评估协议](LLM-Training/evaluation/evaluation-protocol.md) / [学习进度与验收](LLM-Training/learning-progress.md)。
5. [官方资源和论文](LLM-Training/papers/READING-LIST.md) / [面试问题](LLM-Training/interview-qa/QUESTION-BANK.md)。

## 实战约束

- 底层从零训练 **只选 MiniMind**；真实模型以 **Qwen3-0.6B-Base** 为基线；CS336/Raschka 用于补理论，nanochat 用于后期组织设计复盘。
- 本地主要面向 **RTX 5060 Ti 16GB + 32GB RAM**；GRPO 先小模型、短序列、LoRA/原生 TRL，再视兼容性测试 Unsloth/vLLM；任何显存和性能结论必须实测。
- 优先使用带可验证反馈的 **企业知识检索 / 工具调用 Agent** 场景；避免把随机样例或 Reward 变大当成效果提升。
- 从第一天保留模型、数据、代码版本与验证集记录；详见实验模板。

## 目录定位

**LLM-Training/** 是自包含的学习计划与实验手册，不复制第三方项目代码。下一步真正开始训练时，将代码放入各实验目录或单独项目，并引用对应环境、版本、日志及结果证据。

MIT License（以仓库 LICENSE 为准）。

