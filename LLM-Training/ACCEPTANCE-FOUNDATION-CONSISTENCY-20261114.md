# 2026-11-14 全仓大模型基础覆盖与一致性审计

> 验收对象：LLM-Learning-OS 主仓的**学习资料、索引、代码和自动化合同**。**不能将静态知识覆盖/CPU Toy 成功推定为个人掌握、真实 GPU 训练或线上产品就绪**。此报告不宣称“全部 AI 研究领域没有任何未收录技术”；审核范围是本仓定义的 LLM 模型/应用研发基础及 M01–M12 训练工程主干。

## 1. 原始清单与审计方法

本轮首先读取 GitHub 原 main（`90ac16ec017cf6f90e0be1b0fba6034400c6c388`）与上游 AI-Learning-OS 的实际仓库树，并按模块、知识层次、资料深度和运行证据逐项盘点。原仓含 **100 个 Git 文件、12 模块、6 六域/33 宏观知识主题、30 类关系边、12 个跨域任务卡、19 条专项需求、25 个专项原始来源**，以及 TinyGPT/合成评测/工具网关/RL 数学 Toy 和 01–06 的实验手册。

以以下公开原始资料做**抽样网页核对**（不是全部 URL 巡检，也不是本机安装兼容验证）：

- [D2L 基础数学/梯度/概率](https://d2l.ai/chapter_preliminaries/index.html)：线性代数、自动求导、概率统计与泛化基础；
- [Stanford CS336](https://cs336.stanford.edu/)：五组实现任务（Basics、Systems、Scaling、Data、Alignment/Reasoning RL）；
- [Hugging Face Tokenizers 第 6 章](https://huggingface.co/learn/llm-course/en/chapter6/1)：BPE、WordPiece、Unigram；
- [PyTorch Reproducibility](https://pytorch.org/docs/stable/notes/randomness.html)：跨 PyTorch 版本/平台不保证位级复现；
- [PyTorch FSDP2](https://docs.pytorch.org/docs/main/distributed.fsdp.fully_shard.html) 与 [NVIDIA Megatron Core](https://docs.nvidia.com/megatron-core/developer-guide/latest/user-guide/parallelism-guide.html)：参数分片及 DP/TP/PP/CP/EP 维度；
- [TRL SFT](https://huggingface.co/docs/trl/sft_trainer)、[vLLM Security](https://docs.vllm.ai/en/latest/usage/security/)：Assistant Mask 和服务安全版本边界；
- [Hugging Face Dataset Cards](https://huggingface.co/docs/hub/en/datasets-cards)：来源、许可证、偏差和数据描述。

## 2. 实际发现的知识覆盖差距及补救

| 发现 | 修改与现存知识的关系 | 深度界限 |
|---|---|---|
| M01 名词有 Tensor/CE/AdamW，但概率、ML、信息论、统计推断缺独立短课 | [数学/概率/信息论基础卡](fundamentals/CORE-MATH-PROBABILITY-STATISTICS.md) | 有专业/白话/公式/反例；未把全部数学定理或长期训练结果写成已掌握 |
| M02 有 BPE/Unigram/去重，但 WordPiece、特殊 Token、许可/污染/文档边界不集中 | [Tokenizer/数据治理卡](data-engineering/TOKENIZER-AND-DATA-FOUNDATIONS.md) | 真实 Tokenizer/Chat Template 训练仍须自己执行 |
| M03 有 Attention/RoPE，但 Encoder-only vs Decoder-only vs Seq2Seq、采样/Prefill 缺独立对照 | [模型家族与生成卡](fundamentals/MODEL-FAMILIES-AND-GENERATION.md) | 非每种模型都实际训练 |
| M04/M09/M10 的 Checkpoint、随机性、统计和评估指标分散 | [训练可靠性/评估卡](training-systems/REPRODUCIBILITY-AND-EVAL-FOUNDATIONS.md) | Train/Val/Test 和恢复机制均需真实实验验证 |
| “每天需要学哪里？”缺细颗粒覆盖表/CLI | [90 条核心基础索引](index/FOUNDATION-COVERAGE.md)、[JSON](index/foundation-coverage.json)、[离线路由](tools/route_foundations.py) | 仅表示对应文档/练习可找到，**不表示每条均有独立运行的实验** |

现有六域 **33 宏观主题**、训练 **12 模块**、**90 细颗粒概念**分属三种目录维度，不能相加成“135 项全都学会”；90 条词条是当前范围内的**有界基础导航审计**，不是穷尽未来所有 LLM 技术。

## 3. 前后冲突的具体修复

1. **L0–L4 语义**：唯一标准 [Rubric](assessments/CAPABILITY-RUBRIC.md)＝L0 定位、L1 解释、L2 独立实现、L3 诊断/受控比较、L4 陌生任务独立迁移；若任务实际发布，另走 [G0–G8](production/PRODUCTION-READINESS.md)。已统一 AI 学习手册、六域 Atlas、跨域需求路线和历史 V2 的映射说明。
2. **训练生命周期 vs 学习顺序**：修改 [旧生命周期图](knowledge-graph/full-training-pipeline.md) 的“这是学习顺序”，使其说明只是典型生产模型构建关系图，Pretrain/CPT/SFT/DPO/GRPO 不强制全部串行。
3. **计划排期 vs 按需跳学**：将 [学习进度](learning-progress.md) 七周流程标为历史示意排期，不能再称默认学习方式。
4. **资料覆盖计数**：更新入口 README/Index/Roadmap：19 专项需求、25 个专项来源；历史审计保留原当期数据，并明确不是当前库存。
5. **TinyGPT 与 MiniMind 主线**：明确 TinyGPT 仅为可运行极小 CPU Toy，完整开源真实训练底座仍为 MiniMind；避免 V2“不能新建 TinyGPT”与实际 Toy 混淆。
6. **合成评测条数**：M10 将不准确的“15 条”修为实际 [16 条预标注](labs/task-evaluation/synthetic_cases.json)，不把扩展提案 30 条当已实现。

## 4. 自动化验收目标与证据边界

新的 CI 必须同时运行：

- 全部 Markdown 相对链接、12 模块深度标志和必需文件检查；
- 原始 learning-index/Atlas 索引和现有合同单测；
- [基础覆盖校验](tools/validate_foundation_coverage.py)：90 词条，M01–M12 每模块至少 5 条，指南/练习实际存在，外部来源 HTTPS，禁止假造学习 PASS；
- [基础覆盖/反例测试](tools/test_foundation_coverage.py) 与 [查询测试](tools/test_route_foundations.py)，尤其捕捉 L4 误写成“上线”、过时的计数、M10 错误分母、无效路径和不存在主题；
- 旧 CPU Shift/Mask、DPO/GRPO、Synthetic Tool Gateway、Task Eval 以及 TinyGPT 的原有单测，不因目录重整而退化。

**本报告撰写时不预填 GitHub Actions 测试结果**。严格验收以 PR 最新 HEAD 的实际运行状态与日志为准；通过并合并后，再读取主分支检查落盘。

## 5. 还有哪些不是“已经会了”？

- **真实 GPU 模型实验**：MiniMind/Qwen 01–05 中的 Pretrain/CPT/SFT/DPO/GRPO，以及 06 的 vLLM 生产指标没有本次新日志。状态仍 NOT RUN/NOT STARTED。
- **每个词条都精通**：90 条是定位/参考/练习**覆盖范围**，对每条的 L2/L3/L4 达成要逐一提交可复核证据卡；其余保持 L0/L1 学习目标。
- **全部未来/所有学科知识**：Llama、Qwen 等模型架构细节会升级；多模态/扩散、模型编辑、前沿专用训练、跨机 GPU 扩展等按需求再细化，而非现在全部标 P0。
- **外部所有链接实时 100% 可达**：此次仅抽样检查官方学习资源，使用时记录版本；机器 CI 默认不请求外网。
- **生产系统安全/质量**：必须在有权限的真实环境完成监控、鉴权、回归、回滚、成本、风险验收。

下一步的重点不再是扩展“目录数量”，而是按一条具体需求从 [90 项基础入口](index/FOUNDATION-COVERAGE.md) → [对应模块](README.md) → [真实实验](experiments/README.md) → [Rubric](assessments/CAPABILITY-RUBRIC.md) 形成真实能力证据。
