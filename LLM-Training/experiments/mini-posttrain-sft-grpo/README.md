# 小模型后训练实操：SFT → GRPO（M06/M08 进阶，可选）

> **REAL GPU TRAINING: NOT RUN / NOT VERIFIED**。这里提供可审计的真实模型训练入口，而不是只写学习清单。2026-11-15 根据 Hugging Face 官方 [SFTTrainer](https://huggingface.co/docs/trl/sft_trainer)、[GRPOTrainer](https://huggingface.co/docs/trl/grpo_trainer)、[PEFT](https://huggingface.co/docs/peft/index) 接口编写；**只对纯标准库数据与奖励代码做 CI 测试，未在用户的 RTX 5060 Ti 16GB 实机运行，也没有锁定经过实测的 CUDA/包组合**。失败/显存不足时记录证据，不得先写 PASS。

这不是新的第七类实验：**实验 03 的 SFT 与实验 05 的 GRPO 的最小交叉练习**。原 MiniMind 与 Qwen3-0.6B-Base 主线不受影响。本演示默认模型 `Qwen/Qwen3-0.6B` 已经是指令模型，演示的是**在同一 checkpoint 上继续 SFT + RL**，不冒充“从 Base 训练出完整 Chat 模型”。

## A. 严格隔离的数据与奖励（CPU/无依赖）

在仓库根目录：

```bash
python LLM-Training/experiments/mini-posttrain-sft-grpo/data_and_reward.py
python LLM-Training/experiments/mini-posttrain-sft-grpo/train_with_trl.py --mode data-check
python -m unittest discover -s LLM-Training/experiments/mini-posttrain-sft-grpo -p 'test_*.py' -v
```

- 合成任务为简单整数加法；train/dev/test 分配**不同的操作数范围**（不只是行 ID），每组会输出 count 与 SHA-256；`train` 240 条、`dev` 49 条、`test` 49 条。
- SFT 使用 `prompt/completion`，Completion 为严格 `<answer>N</answer>`；GRPO 使用 `prompt/answer` 和 `exact_reward`。
- 奖励解析 `fullmatch`：多答案、尾随解释、格式正确但数值错误都得 0；拒绝把 “JSON 合法” 误当任务成功。
- 因为训练集只含有限的简单加法、测试范围不同，该实验是**教学级外推测试**，不能证明通用推理增强或生产任务泛化。
- 不能以测试集反复调参；允许在 dev 调整，最后对确定版本执行一次 test。

## B. 实机安装与版本门禁

在可用 NVIDIA CUDA 的 Linux/WSL2 虚拟环境操作。**先按当前 [PyTorch 安装页](https://pytorch.org/get-started/locally/) 安装兼容驱动/CUDA 的 torch**，再安装当前相互兼容版本的 `transformers trl peft datasets accelerate`，运行时记录精确 `pip freeze`，不要盲目复制未经本机验收的固定版本组合。部分 TRL Agent Environment API 需要 transformers ≥ 5.2.0，但这里的单轮算术 GRPO **没有**使用该新 API。

```bash
python -m pip install transformers trl peft datasets accelerate
python LLM-Training/experiments/mini-posttrain-sft-grpo/train_with_trl.py --mode preflight
python -c "import torch; print(torch.__version__, torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'NO CUDA')"
python -m pip freeze > runs-posttrain-freeze.txt
```

正式运行前固定并记录：**Git SHA、model/tokenizer revision（不要用浮动 main 做严格复现）、dataset SHA-256、CUDA/torch/trl/peft 版本、seed、设备及显存**。检查 Model Card 的 license 与使用限制。这里写的是建议配置，不承诺训练一定成功或效果提升。

## C. 真实小模型实验命令（使用时核对当前官方 API）

脚本文件：[train_with_trl.py](train_with_trl.py)。建议先从 **2–5 个 step Smoke Test** 确认 `completion_only_loss` 对 prompt token 做正确 mask、LoRA 可训练参数确实更新、保存 adapter 能加载，再增大 step。

```bash
# 0. 无模型微调的基线：先只在 dev 上评价
python LLM-Training/experiments/mini-posttrain-sft-grpo/train_with_trl.py --mode eval --checkpoint base --split dev

# 1. 真正的 LoRA SFT：生成 runs/mini-sft-grpo/sft/adapter_config.json
python LLM-Training/experiments/mini-posttrain-sft-grpo/train_with_trl.py --mode sft --steps 20
python LLM-Training/experiments/mini-posttrain-sft-grpo/train_with_trl.py --mode eval --checkpoint sft --split dev

# 2. 从 SFT adapter 接着做 GRPO（不是从 Base 重新初始化）
python LLM-Training/experiments/mini-posttrain-sft-grpo/train_with_trl.py --mode grpo --steps 20
python LLM-Training/experiments/mini-posttrain-sft-grpo/train_with_trl.py --mode eval --checkpoint grpo --split dev

# 3. 调参完全停止后，才在 test 做同一轮定稿评估
python LLM-Training/experiments/mini-posttrain-sft-grpo/train_with_trl.py --mode eval --checkpoint base --split test
python LLM-Training/experiments/mini-posttrain-sft-grpo/train_with_trl.py --mode eval --checkpoint sft --split test
python LLM-Training/experiments/mini-posttrain-sft-grpo/train_with_trl.py --mode eval --checkpoint grpo --split test
```

- 采用 LoRA `r=8`、`q_proj/v_proj`，SFT 每卡 micro-batch 1；GRPO 每卡 batch 2 / `num_generations=2`、短 completion、`use_vllm=False`。**属于探索配置**，不是实测显存证明；OOM 时缩短序列/步数、减少梯度累积（可能不降单步激活）、换更小模型/转云端，完整记录变更。
- 当前 GRPO `beta=0` 表示不额外施加显式 Reference KL；记录时不能写成“KL 被严格约束”。
- 训练脚本先写 `run-manifest.json`，状态始终提醒 `STARTED_NOT_VERIFIED`；执行者必须自己附实际 stdout、trainer state、loss/reward/group std、显存峰值、adapter diff、评估明细和复现命令，再评审是否 `PASS`。
- 两阶段都使用相同的算术任务，但**这是分阶段流水线，不是 SFT 与 GRPO 公平归因消融实验**；想研究增益需保留单独 SFT checkpoint、匹配采样预算、使用相同模型和 Harness，并用多种数据/seed 重复。
- `eval` 采用 greedy decoding 并严格评判输出；模型可能输出思维标记或额外文本而被判错，这暴露了 prompt、模板、奖励与模型之间的不匹配，不应偷偷放松评分规则来美化结果。

## D. 失败归因与验收

| 现象 | 检查顺序 | 必须留下的证据 |
|---|---|---|
| Import / incompatible API | 确认 TRL/Transformers/PEFT 版本，重新读官方文档 | requirements、版本与具体报错 |
| CUDA OOM | 峰值显存、batch、长度、模型加载方式 | GPU 型号、具体参数、OOM 堆栈 |
| SFT Loss 下降，但泛化差 | 数据过简单、completion mask、测试外推难度 | train/dev/test 样本与独立结果 |
| GRPO Reward 都为 0 | 输出未达到严格格式、采样缺乏多样性或任务太难 | 原始 completions、reward_components、group std |
| Reward ↑ Accuracy ↔ / ↓ | Reward hacking、长度/截断、样本泄漏或过拟合 | 前后任务级输出及 5 条失败案例 |
| 无法保存/加载 adapter | 模型基座、Tokenizer revision、Adapter 版本 | adapter_config、重载命令、生成验证 |

**退出门槛**：能出示真实模型参数更新、模型 checkpoint、训练日志、独立评估（含失败类型）、环境/数据版本与可重复命令，才可把实验 03/05 的本次 Run 标记 VERIFIED。没有 GPU/运行证据，保持 NOT RUN；此处静态/CPU 测试通过不代表 CUDA 上可运行。

关联：[跨模块学习总纲](../../reinforcement-learning/AGENTIC-RL-LEARNING-PATH.md) · [实验 03](../03-agent-tool-sft/README.md) · [实验 05](../05-grpo/README.md) · [Agentic RL 环境桥](../agentic-rl-bridge/README.md) · [统一实验模板](../EXPERIMENT-TEMPLATE.md)。
