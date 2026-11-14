# 2026-11-14 用户训练路线增量融合与严格验收

> 本文是仓库资产的差异审计、验收标准和证据边界；不能用文档或 CPU 教学通过推断 MiniMind/Qwen 的真实 GPU 训练已完成。实际 CI 以本 PR 最新提交对应的 Actions 工作流为准，合并后还须验证 main SHA。

## 一、没有重复建设的部分

- V3 训练 12 模块、V2 四个里程碑、六域全栈知识 Atlas、需求驱动原理与上游 AI-Learning-OS 双向索引：继续保留。
- 四个主资源 Stanford CS336 / MiniMind / Raschka / nanochat：原论文索引已收录，此次只是明确职责和适用时机。
- MiniMind → Qwen CPT/Tool SFT → DPO/GRPO → Serving：原有 01–06 实验目录均保留，状态以原文件真实运行证据为准。
- Chinchilla / InstructGPT / DPO / DeepSeekMath / DeepSeek-R1：原论文书目已收录，本轮补充按问题选读和课程之间的链接。

## 二、实际缺口与本次补充

| 用户要求 | 原有证据与差距 | 本次实际新增 |
|---|---|---|
| A 手写最小 GPT | 旧 CPU Toy 只优化假 Logits，没有 Transformer | [TinyGPT PyTorch](labs/tiny-gpt/tiny_gpt.py)、[8 个单测](labs/tiny-gpt/test_tiny_gpt.py)、[教学与失败注入说明](labs/tiny-gpt/README.md) |
| 实验 A–E 与旧编号一致 | 01–06 已有，但未和用户新字母路线明确定义映射 | [实验交叉索引](experiments/EXPERIMENTS-A-E-CROSSWALK.md)，区分训练算法和部署 |
| 六个能力学习单元 | 4 个里程碑与 L0–L4 已有，但未组织成 6 个按需退出目标 | [U1–U6 非线性能力单元](learning-method/SIX-CAPABILITY-UNITS.md) |
| 预训练 Batch 与后训练信号的完整关系 | 已有多个机制模块，但技术术语多、缺少一个可复用例子 | [从语料到助手的训练信号总图](knowledge-graph/TRAINING-SIGNAL-AND-LIFECYCLE.md)，含 Pretrain/CPT/SFT/DPO/GRPO + 库存工具示例 |
| 权威资料与源码/项目选型 | 多数已有；Pythia、Megatron Core/Parallelism Guide 缺独立引用及索引关联 | [新来源职责与直达链接](resources/TRAINING-SOURCE-ROLES.md) 和机器索引新增 5 条来源、1 条 TinyGPT 需求 |
| 按需学习而不是线性课程 | V3 已建立 | 新增练习、资源与 6 单元均接入 V3 和 README，保留原入口 |

## 三、严格验收清单

1. 必须确认为当前主分支增量，不覆盖任何已有上游或 12 模块资料。
2. check_repo.py 应检查新必需文件和所有 Markdown 相对链接；外部网页核查是**抽样**，不把 URL 的 HTML 打开等同于代码兼容。
3. validate_learning_index.py / test_learning_index.py 检验 25 个来源、19 条需求、手写 GPT 别名/源码引用和可选练习路径；不存在的链接应触发错误。
4. GitHub CPU Job 必须执行真实 PyTorch TinyGPT 训练与 8 项单测：训练 Batch Loss 下降、因果未来不可见、CE Shift 一次、梯度非零、模型与优化器本地临时 Checkpoint 恢复等。此训练只用合成重复字符语料，**不是独立验证集性能**。
5. GitHub 既有 Mask/Shift、工具网关、DPO/GRPO 公式、Agent Task Eval、Atlas 索引和 Docs CI 均不得回退。
6. PR Checks 全部通过后才能合并，合并后读取 main SHA、TinyGPT 源码、Roadmap 和本验收材料确认存在。

## 四、技术与身份边界

- 训练资源的定价、硬件适配、依赖版本会改变，MiniMind 的低成本结果有特定实验环境，不可推广到任意 16GB GPU。
- TinyGPT 用字符级词表、learned positions、LayerNorm/GELU，未使用 Qwen 的具体 Tokenizer/现代 Attention 组件；只证明教学生成和优化链条能运行。
- 实验 01–05 MiniMind/Qwen 模型训练、DPO/GRPO 真实政策更新、06 部署负载与生产安全均**没有因为本次文档建设就自动 PASS**。
- 项目业务数据、真实用户权限、外部商业指标或客户订单属于各自产品仓，不放进教学仓。
