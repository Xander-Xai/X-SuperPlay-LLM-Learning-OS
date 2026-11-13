# 训练失败排查表：按现象进入原理

| 症状 | 优先检查 | 具体动作 |
|---|---|---|
| CUDA OOM | batch/seq length、activation、optimizer、KV cache | 减 seq/batch/num_generations，开 activation checkpointing/LoRA，记录 max_allocated |
| Loss NaN | LR 过高、数值精度、溢出、错误 label | 打印梯度范数、dtype、学习率、finite checks，验证 CE 与 mask |
| Loss 不降 | 数据 tokenization、shift/mask、冻结参数、scheduler | 检查 labels!=-100 数量、optimizer 目标参数、梯度非零 |
| 训练 Loss 低但工具调用差 | 训练-测试分布、模板、单轮/多轮偏差 | schema-valid 和执行成功率分项统计；检查工具消息序列化 |
| CPT 后通用能力降 | 分布漂移、LR、Replay 比例、过拟合 | 比较 Base/Domain/Replay 的 held-out 通用 CE 与任务指标 |
| DPO 后答非所问 | chosen/rejected 标注、reference、beta、长度偏好 | 抽检偏好对、评审器偏差、正确率和输出长度 |
| GRPO Reward 高但 Accuracy 不升 | reward hacking、验证器不严、奖励稀疏 | 手审轨迹，分解 reward，独立 held-out 评估 |
| GRPO 全零或同奖励 | 组内无区分度、题太难/太易 | 调难度、采样、多样性与验证器；看 group std |
| GRPO 推理很慢 | Rollout、模型权重加载、KV、采样长度 | 先 Profile 而非先加 vLLM；控制 prompt/completion |
| 训练复现不一致 | seed、数据顺序、CUDA 非确定性、版本 | 固定 SHA/revisions，记录 nondeterminism，重复种子 |
| 引用正确率低 | RAG 证据/引用映射与评测不一致 | 按 citation ID 核对 source passage 与 answer claim |
| vLLM Tool Call 解析失败 | Chat Template、模型版本、parser 配置 | 对照模型官方 Function Calling 序列化与服务端 parser |

## 每次排查只改一件事

建立记录：**现象 → 原始日志 → 可疑假设 → 单变量修复 → 对照结果 → 根因或未证实**。不应因为某个参数修改后一次任务成功就宣布根因已确定。

关联：[评估协议](../evaluation/evaluation-protocol.md) · [显存与系统](../training-systems/memory-and-distributed.md)。

