# V2.0 学习路线落盘：严格验收报告

- 日期：2026-11-14（北京时间）
- 仓库：Xander-Xai/X-SuperPlay-LLM-Learning-OS
- 原始落盘：[PR #1](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/pull/1)（已合并）
- 补全与审计：[PR #2](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/pull/2)
- 验收范围：**学习体系文档、目录结构、源码/实验入口、可运行 CPU 教学用例与相对路径检查**；不包含实际 GPU 训练或模型表现证明。

## 1. 发现的缺口与修复证据

| 首轮差距 | 修复 | 验收证据 |
|---|---|---|
| 只有 Roadmap 总表，M01–M12 无独立入口 | 补齐 [M01–M12](modules/M01.md) 分页，每页有先修、知识点、任务、问题、验收 | modules/ 下 12 份文档 |
| 缺学习入口 README、Pretrain/Posttrain 关系页 | 补 [学习中心](README.md)、[关系页](knowledge-graph/pretrain-posttrain-relations.md) | README 和知识导航直达 |
| Tokenizer/Packing/预训练与经典 RLHF 讲解偏少 | 补 [数据专题](data-engineering/tokenizer-and-packing.md)、[白盒 Pretrain](pretraining/pretraining-lab.md)、[Reward/ORPO](alignment/reward-model-orpo.md)、[PPO](reinforcement-learning/ppo-rlhf-fundamentals.md) | 单模块入口和专题互链 |
| 训练实验只有文字说明，不便立刻验证细节 | 补 [CPU Toy Lab](labs/README.md)、[PyTorch 代码](labs/toy_train.py)、[5 项单元测试](labs/test_toy_train.py) | 本次工作环境实测 5/5 单测通过；没有下载/训练真实模型 |
| 没有自动检查结构和内部链接 | 补 [仓库检查脚本](tools/check_repo.py) 和 [GitHub Actions](../.github/workflows/learning-docs-check.yml) | 检查必须存在文件、相对链接、未运行状态；运行状态另见 PR |
| 5 类训练实验和 6 项实验编号容易混淆 | [学习中心](README.md) 明确 01–05 为训练类、06 为部署验收，并修正 [实验依赖图](experiments/README.md) | Roadmap/实验导航一致 |

## 2. 原方案关键覆盖范围

- **12 模块**：M01–M12 均有独立学习入口，M05 CPT 为 P1、M06/M07 合成和偏好数据为 P0、M09 基础诊断与 M10 评估前置。
- **4 里程碑**：白盒底座 → Qwen 真实微调与数据工程 → DPO/GRPO 对齐 → 工程部署，采用验收退出而非日历硬切。
- **1 条底层代码主线**：MiniMind；真实模型实验 Qwen3-0.6B Base，不重复造 TinyGPT。
- **5 类训练实验**：MiniMind、CPT、Tool SFT、DPO、GRPO；外加 06 部署和 Profiler。
- **Agent/RAG 前置**：多轮 assistant/tool 轨迹、Tool Calling schema、引用验证和 assistant-only mask。
- **16GB GRPO**：原生 TRL 起步、Unsloth/vLLM 视兼容性加速，不保证显存低于固定值或效果提升。
- **对照严谨性**：CPT Base/Domain/Replay，Cosine/WSD 单变量；DPO/GRPO 从同一 SFT 分支；评估集隔离与失败记录。
- **学习资源**：[论文/课程清单](papers/READING-LIST.md)、[面试题](interview-qa/QUESTION-BANK.md)、[故障排查](troubleshooting/COMMON-FAILURES.md)。

## 3. 来源与链接抽样审查

- 仓库 Markdown 相对路径曾在 PR 审查阶段发现两处未创建的验收文档链接，现已补建 [ACCEPTANCE-V2.md](ACCEPTANCE-V2.md)。
- [Stanford CS336 Spring 2026](https://cs336.stanford.edu/) 的旧 GitHub Pages 地址不可访问；已将本仓库的引用统一更新到官方有效域名。
- 抽样确认 [Qwen3-0.6B-Base](https://huggingface.co/Qwen/Qwen3-0.6B-Base)、[TRL GRPO](https://huggingface.co/docs/trl/grpo_trainer)、[TRL Online DPO](https://huggingface.co/docs/trl/online_dpo_trainer)、[Qwen Function Calling](https://qwen.readthedocs.io/en/latest/framework/function_call.html) 和 [Unsloth RL Guide](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide) 可访问。
- **外链只进行了针对性抽检**；尚未逐个验证全仓库所有外部链接。静态脚本只检查仓库内相对路径，不能替代 HTTP 外链巡检。

## 4. 验证与限制（不得混淆）

| 验收对象 | 结果 | 证明范围 |
|---|---|---|
| GitHub PR #1 | MERGED | 原有文档已在 main |
| 本轮 12 模块与必须文件 | PASS（Git 树清单核对） | 文件存在，不等于每个知识点已掌握 |
| Toy Shift/Mask | PASS：CPU 5/5 单元测试 | 合成 Token IDs 的标签/shift/梯度；非真实 Qwen Chat Template |
| 仓库离线链接校验 | 由 check_repo.py + CI 执行；以实际检查记录为准 | 静态相对路径和必需文件；**不验证互联网外链** |
| MiniMind Pretrain/SFT | NOT RUN | 需在本机执行、留存日志/Checkpoint |
| Qwen CPT / Full SFT / LoRA / QLoRA | NOT RUN | 需有评估/显存/忘却对照 |
| DPO / GRPO / vLLM Deployment | NOT RUN | 需真实采样、评估与服务日志 |

## 5. 最终验收结论

**文档与学习路线可执行层面：通过（以 PR #2 合并并复验静态检查为最终交付条件）。**
**模型训练效果层面：未验收，不得声称完成。**

下一个真正的执行任务：从 [01 MiniMind 白盒](experiments/01-minimind-whitebox/README.md) 开始，按 [实验模板](experiments/EXPERIMENT-TEMPLATE.md) 保存 commit、数据版本、训练/评估日志和 checkpoint。CPU Toy 只能当做预检。
