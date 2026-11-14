# 权威资料索引：理论 → 源码 → 实验 → 限制

**补充专业基础官方资源**：[Dive into Deep Learning](https://d2l.ai/chapter_preliminaries/index.html)（数学/梯度/概率） · [Hugging Face Tokenizers 第 6 章](https://huggingface.co/learn/llm-course/en/chapter6/1)（BPE/WordPiece/Unigram） · [PyTorch 复现性](https://pytorch.org/docs/stable/notes/randomness.html)（跨设备/版本限制） · [Dataset Cards](https://huggingface.co/docs/hub/en/datasets-cards)。按 [90 项核心知识目录](../index/FOUNDATION-COVERAGE.md) 查阅，避免另造并行课程。

**技术框架会变**：针对 2026-11-14 抽查的 [TRL、vLLM、MCP 运行时变化与最小实验](OFFICIAL-RUNTIME-DELTA-20261114.md) 单独建了一张问题卡，避免只有书目而没有实际验收要求。

**新增六域纵向参考导航**：[AI-Learning-OS 上游 33 主题逐条知识与官方链接](UPSTREAM-RESOURCE-MAP.md)；先看 [全栈 Atlas](../knowledge-graph/LLM-FULL-STACK-ATLAS.md)，需要时才深入本文当前训练资源分组。课程不会强制用户预读所有外部链接。

> 来源分级：**P0 官方规范/论文原文/项目官方源码；P1 作者公开的课程与工程教程；P2 第三方博客或社区案例仅用于发现问题，不能代替结论。** 网址会变化，使用时固定版本/日期。此表是供学习的**资料目录**，不是声称所有资源已经本机运行。

四个主学习源及新增专项的具体场景入口见 [TRAINING-SOURCE-ROLES.md](TRAINING-SOURCE-ROLES.md)。其中 DataComp-LM 的官方链接是 mlfoundations/dclm，Megatron Core 需按部署版本对照 TP/PP/CP/EP，Pythia 是观察公开训练 Checkpoint 的来源，不是训练结果本身。

## 1. 基础、数据与训练（M01–M05）

| 需求 | 主要原始来源 | 应检查什么 | 跟哪个练习关联 |
|---|---|---|---|
| Autograd/显存 | [PyTorch Autograd](https://docs.pytorch.org/docs/stable/autograd.html) · [CUDA Memory](https://docs.pytorch.org/docs/stable/notes/cuda.html) | backward、in-place、allocated/reserved 区分 | M01 / GPU Profile |
| Transformer | [Attention Is All You Need](https://arxiv.org/abs/1706.03762) · [RoFormer/RoPE](https://arxiv.org/abs/2104.09864) | causal masking、RoPE、shape | M03 MiniMind 数值对照 |
| Scales/Training | [Stanford CS336](https://cs336.stanford.edu/) · [Chinchilla](https://arxiv.org/abs/2203.15556) | token/compute/数据质量与预算 | M04 模型/训练预算 |
| 预训练源码 | [MiniMind upstream](https://github.com/jingyaogong/minimind) | model/pretrain/sft 真实参数与版本 | [实验 01](../experiments/01-minimind-whitebox/README.md) |
| 数值难点 | [Raschka LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) | tensor/Attention 的解释，不再造第二套 TinyGPT | M01/M03 |
| 数据 | [DataComp-LM](https://github.com/mlfoundations/dclm) · [HF Datasets](https://huggingface.co/docs/datasets/index) | 去重/许可/污染/数据混合 | M02/CPT |
| 大模型真实基线 | [Qwen3-0.6B-Base](https://huggingface.co/Qwen/Qwen3-0.6B-Base) | Model Card、license、revision、模板 | 实验 02–05 |

## 2. Post-training、Preference、RL（M06–M08）

| 学习点 | 官方资料 | 做什么 |
|---|---|---|
| SFT 数据格式和 Assistant Mask | [TRL SFTTrainer](https://huggingface.co/docs/trl/sft_trainer) · [TRL Dataset Formats](https://huggingface.co/docs/trl/dataset_formats) | 真正对 tokenizer 模板 token 范围测 mask |
| PEFT/QLoRA | [HF PEFT](https://huggingface.co/docs/peft/index) · [LoRA](https://arxiv.org/abs/2106.09685) · [QLoRA](https://arxiv.org/abs/2305.14314) | target modules/rank/更新权重与 VRAM |
| DPO | [DPO 原论文](https://arxiv.org/abs/2305.18290) · [TRL DPO](https://huggingface.co/docs/trl/dpo_trainer) | logprobs/chosen/rejected/beta/Ref |
| Reward Model | [InstructGPT](https://arxiv.org/abs/2203.02155) · [TRL Reward](https://huggingface.co/docs/trl/reward_trainer) | preference pair 偏差和奖励可靠性 |
| PPO/GRPO | [TRL PPO](https://huggingface.co/docs/trl/ppo_trainer) · [TRL GRPO](https://huggingface.co/docs/trl/grpo_trainer) · [DeepSeekMath](https://arxiv.org/abs/2402.03300) | rollout、优势、clip、Reward Hacking |
| 可验证推理训练 | [DeepSeek-R1](https://arxiv.org/abs/2501.12948) | RLVR/合成轨迹/多阶段的适用边界 |
| 工具调用 | [Qwen Function Calling](https://qwen.readthedocs.io/en/latest/framework/function_call.html) | chat_template/parser/特殊 Token 与文本标记 |
| 单卡优化 | [Unsloth RL Guide](https://unsloth.ai/docs/get-started/reinforcement-learning-rl-guide) | 兼容性、真实 CUDA/版本、显存/吞吐实测 |

**版本提醒**：TRL 可能更换接口和算法状态；在线与离线、reference KL 是否启用都必须按安装的版本与配置确认。不把某一次 benchmark 的数值写成普遍规律。

## 3. 训练系统、推理与评估（M09–M11）

| 场景 | 官方来源 | 验证动作 |
|---|---|---|
| FSDP/Shard | [PyTorch FSDP2](https://docs.pytorch.org/docs/stable/distributed.fsdp.fully_shard.html) · [DeepSpeed ZeRO](https://www.deepspeed.ai/tutorials/zero/) | 参数/优化器/通信与资源模型 |
| 生产训练 | [Megatron-LM](https://github.com/NVIDIA/Megatron-LM) · [verl](https://github.com/volcengine/verl) · [OpenRLHF](https://github.com/OpenRLHF/OpenRLHF) | Actor/Rollout/Reference/Weight Sync |
| 训练效能 | [PyTorch Profiler](https://docs.pytorch.org/docs/stable/profiler.html) · [FlashAttention](https://arxiv.org/abs/2205.14135) | Profile、Activation/IO 和 compute |
| Serving | [vLLM Documentation](https://docs.vllm.ai/en/latest/) · [vLLM GitHub](https://github.com/vllm-project/vllm) | batching、KV、TTFT、error/rollback |
| Eval Harness | [EleutherAI lm-eval](https://github.com/EleutherAI/lm-evaluation-harness) | 固定任务/版本、运行结果与统计限制 |
| 框架学习 | [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/chapter1/1) · [smol-course](https://github.com/huggingface/smol-course) | Trainer/TRL 抽象与数据模板 |
| 训练项目组织 | [Karpathy nanochat](https://github.com/karpathy/nanochat) | 项目组织、端到端调试，不等于大型工业生产平台 |

注意 `lm-evaluation-harness` 新版本的 CLI/安装 extras 已变化，使用前先读 README 和当前命令说明，不复制历史旧命令；跟踪每次评估的任务配置和模型 revision。

## 4. 生产工程（学习范围跨 M02/M06/M09/M10/M11）

| 目标 | 官方源 | 需要验证 |
|---|---|---|
| Web API 可靠性 | [FastAPI](https://fastapi.tiangolo.com/) · [OpenAPI](https://spec.openapis.org/oas/latest.html) | 输入契约、错误码、限流/超时、集成测试 |
| 可观测性 | [OpenTelemetry](https://opentelemetry.io/docs/) | trace/metric/log 三种信号的关联与脱敏 |
| 容器/部署 | [Docker Docs](https://docs.docker.com/) · [Kubernetes Docs](https://kubernetes.io/docs/home/) | 复现环境、健康检查、滚动发布与回滚 |
| 安全威胁 | [OWASP LLM Top 10](https://genai.owasp.org/llm-top-10/) | Prompt injection、敏感信息、工具越权、模型供应链 |
| 模型/数据风险 | [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | 风险登记、使用限制、监测与反馈 |
| RAG/Agent | [上游六域 Knowledge Atlas](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/tree/main/docs/atlas) | 复用现有概念和应用/生产认知，不复制成平行事实 |

这部分是为了让你有能力理解真实上线所需事项，**不要求把所有平台都安装到本仓**；具体业务部署需要另建项目。

## 5. 来源审计约定

每条学习记录建议携带 `source_id`、`URL`、`publisher`、`checked_on`、`version/revision`、`what_it_supports`、`what_it_does_not_prove`，尤其区分“源码有此算法”“本机运行成功”“真实上线成功”三个不同等级。上游自己的 [来源审计](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/main/docs/sources/llm-training-repositories.md) 可以继续提供历史对照，但不能自动当最新版本事实。

通过 [learning-index.json](../index/learning-index.json) 机器索引检索模块/场景/来源；避免搜索关键词相似时误把第三方解释当官方标准。


## 6. 官方资料如何直达每个模块（人工审核导航，非在线链接巡检）

[learning-index.json](../index/learning-index.json) 提供 **12 模块 ↔ 官方来源 ID ↔ 起步实验 ↔ 生产门禁**的机器映射，终端可执行 `python LLM-Training/tools/route_learning.py --module M06`。查看每个 [M01–M12](../README.md) 页面也能直接找到对应论文/官方文档，不再只给一张全局大表。

**版本相关的一个重要细节**：[TRL 官方 SFT 文档](https://huggingface.co/docs/trl/sft_trainer) 在当前接口说明：`assistant_only_loss=True` 需要能产生 generation mask 的 Chat Template（`{% generation %}` / `{% endgeneration %}`）；部分已支持的 Qwen3 模板会由 TRL 处理，但不能据此认定自定义模板、所有历史版本都正确。应在真实 Tokenizer 上断言每个 assistant/tool 边界，不要依赖本仓合成 Token Toy 代替验证。

同样，[PyTorch FSDP2 当前官方文档](https://docs.pytorch.org/docs/main/distributed/fsdp.fully_shard.html) 说明了基于 DTensor 的分片与 All-Gather 生命周期；实际环境应以安装的 PyTorch 版本文档为准，不能假设所有 GPU 或后端都可复现。

**事实边界**：原始论文、官方实现与公开 Model Card 可作为技术参考；来源被编目并不意味着全部外部 URL 已逐个 HTTP 验证，不意味着代码在本机跑过，也不意味着个人已掌握对应能力。
