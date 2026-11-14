## 当前入口：需求驱动的 LLM 专项学习 V3（2026-11-14）

**本仓是独立的 LLM 学习与能力验收体系，不是某个下游产品的交付代码仓。** 保留 V2 的 M01–M12、MiniMind 白盒与 Qwen3 实验；学习时按工程问题跳到对应模块，不必机械从第 1 章开始。生产能力通过多种可迁移切片验收，而不是让本仓绑定一个 Agent 项目。

- [Roadmap V3｜需求驱动扩展](LLM-Training/ROADMAP-V3-DEMAND-DRIVEN.md) · [按问题跳学](LLM-Training/demand-driven/README.md) · [知识依赖与能力关系图](LLM-Training/knowledge-graph/dependency-and-capability-map.md)
- [机器索引（12 模块 / 18 需求 / 20 来源）](LLM-Training/index/README.md) · [权威资料](LLM-Training/resources/AUTHORITATIVE-INDEX.md) · [上线门禁](LLM-Training/production/PRODUCTION-READINESS.md)
- [上游 AI-Learning-OS 的责任分工与旧 M00–M17 映射](LLM-Training/index/UPSTREAM-DOWNSTREAM.md)

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

