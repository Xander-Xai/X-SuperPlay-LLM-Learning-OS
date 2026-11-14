# 第一天：MiniMind 白盒 Pretrain → SFT（RTX 5060 Ti 16GB / WSL2）

**状态：NOT RUN。** 这份操作手册对照 MiniMind 上游实际 CLI 参数编写；**尚未在你的 GPU 上执行**。目标是看懂一次 Batch 的前向、Loss、反向传播、优化器更新和 Checkpoint，不是追求小样本的模型效果。

## 0. 源码/硬件准备

审阅时的 MiniMind `master` 提交：`233d00fa068ec2b8c0d4f07b703934d6391a5a73`（2026-11-14）。源码：[README](https://github.com/jingyaogong/minimind/blob/master/README.md)、[train_pretrain.py](https://github.com/jingyaogong/minimind/blob/master/trainer/train_pretrain.py)、[train_full_sft.py](https://github.com/jingyaogong/minimind/blob/master/trainer/train_full_sft.py)、[eval_llm.py](https://github.com/jingyaogong/minimind/blob/master/eval_llm.py)。

在 WSL2 Ubuntu、适配 CUDA 的 PyTorch 环境：

```bash
git clone https://github.com/jingyaogong/minimind.git
cd minimind
git checkout 233d00fa068ec2b8c0d4f07b703934d6391a5a73
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -c "import torch; print(torch.__version__, torch.cuda.is_available())"
nvidia-smi
git rev-parse HEAD
```

如 `torch.cuda.is_available()` 为 `False`，先处理驱动或 CUDA 环境，不要套用 GPU 训练设置。首次安装依赖的精确版本和上游变动都要记录。

## 1. 官方数据与许可检查

从 [MiniMind 官方 ModelScope 数据目录](https://www.modelscope.cn/datasets/gongjy/minimind_dataset/files) 下载两份轻量数据，放置在本次克隆的 `dataset/` 目录：

```bash
test -s dataset/pretrain_t2t_mini.jsonl
test -s dataset/sft_t2t_mini.jsonl
sha256sum dataset/pretrain_t2t_mini.jsonl dataset/sft_t2t_mini.jsonl
head -n 1 dataset/pretrain_t2t_mini.jsonl
head -n 1 dataset/sft_t2t_mini.jsonl
```

预训练通常含 `text`，SFT 通常含 `conversations`；未经授权不要重新分发原始数据，必要时使用自建的虚构任务数据。

## 2. 单卡起步命令：保守小预算

以下 `hidden_size=512`、8 层、短序列、小 batch 是**建议的起点，不保证无 OOM 或模型质量**。所有训练命令从 `trainer/` 执行，因上游代码使用相对路径读取数据和保存输出。

```bash
mkdir -p logs
cd trainer

python train_pretrain.py --hidden_size 512 --num_hidden_layers 8 --batch_size 2 --accumulation_steps 4 --max_seq_len 256 --epochs 1 --num_workers 2 --log_interval 10 --save_interval 100 --dtype bfloat16 --device cuda:0 --data_path ../dataset/pretrain_t2t_mini.jsonl 2>&1 | tee ../logs/pretrain-first.log

python train_full_sft.py --hidden_size 512 --num_hidden_layers 8 --batch_size 2 --accumulation_steps 1 --max_seq_len 256 --epochs 1 --num_workers 2 --log_interval 10 --save_interval 100 --dtype bfloat16 --device cuda:0 --from_weight pretrain --data_path ../dataset/sft_t2t_mini.jsonl 2>&1 | tee ../logs/sft-first.log

cd ..
ls -lh out/pretrain_512.pth out/full_sft_512.pth
```

若某条命令失败，不要直接执行下一条。优先调低 `batch_size`、`max_seq_len` 或模型规格；**Pretrain、SFT、Eval 的结构参数必须一致**。上游默认从 `../out/` 查找 `--from_weight pretrain`，这与本手册输出路径相匹配。

## 3. 固定 Prompt 对照

```bash
python eval_llm.py --weight pretrain --hidden_size 512 --num_hidden_layers 8 --max_new_tokens 128
python eval_llm.py --weight full_sft --hidden_size 512 --num_hidden_layers 8 --max_new_tokens 128
```

对同一组非训练样例、同样解码参数记录两者输出。**5–10 条人工示例仅供检查行为**；要判断真实能力，需要单独建立 held-out 验证集和正确的评估脚本。

## 4. Source Walkthrough + 恢复训练

对照源文件找到 `model(input_ids,labels=labels)`、`loss=res.loss+res.aux_loss`、`scaler.scale(loss).backward()`、`scaler.step(optimizer)` 和 `optimizer.zero_grad()`，记录每步张量 shape、是否做 shift、何处决定学习率和显存消耗。

- `out/pretrain_512.pth` 和 `out/full_sft_512.pth` 用于模型加载；`checkpoints/*_resume.pth` 用于训练恢复，包含优化器等状态。恢复参数可使用 `--from_resume 1`，但也必须验证数据和随机状态恢复程度。
- 记录 `torch.cuda.max_memory_allocated()`、训练日志、Git SHA、数据 hash、PyTorch/CUDA/driver、seed；若需断点观察添加轻量日志钩子，避免修改梯度语义。
- 真实工具调用的 mask 必须以实际 Chat Template / token 范围测试，本仓库 [CPU Toy Lab](../../labs/README.md) 只验证合成 token 的原理。
- 最终填写 [实验模板](../EXPERIMENT-TEMPLATE.md)，更新 [进度表](../../learning-progress.md)；**没有真实日志时仍为 NOT RUN**。

## 5. 验收退出

必须有真实 Train/Validation 记录、至少两份可加载的权重、Checkpoint 恢复说明、关键 Shape/Mask 单测和异常分析。未完成也保留失败日志，不应随意声称阶段完成。详见 [实验 01 主验收](README.md)。
