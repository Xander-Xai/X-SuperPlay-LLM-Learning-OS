# X-SuperPlay-LLM-Learning-OS

需求驱动的大模型学习操作系统：覆盖基础架构、预训练、持续预训练、SFT、DPO、RL、评估、推理和工程化。核心原则：**知识地图完整、只维护一条底层实战主线、按问题跳学、用实验证据验收**。

> 2026-11-14：首期落地 **LLM Training Roadmap V2.0**；内容属于学习计划和实验规范，**不代表已经执行模型训练**。

## 开始学习

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

