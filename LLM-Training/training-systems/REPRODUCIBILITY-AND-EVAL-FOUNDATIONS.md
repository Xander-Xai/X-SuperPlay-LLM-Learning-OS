# 基础缺口 T0｜训练可靠性、数据切分与评估指标

> 对应 [M04](../modules/M04.md)、[M09](../modules/M09.md)、[M10](../modules/M10.md)、[M11](../modules/M11.md)。比起“会调用训练脚本”，本页解决：为什么一次实验不可信、为什么只存权重无法完整恢复、为什么 Reward/PPL 好不等于任务正确。
>
> 依据：[PyTorch Reproducibility](https://pytorch.org/docs/stable/notes/randomness.html)、[PyTorch FSDP2](https://docs.pytorch.org/docs/main/distributed.fsdp.fully_shard.html)、[CS336](https://cs336.stanford.edu/)、[LM-Evaluation-Harness](https://github.com/EleutherAI/lm-evaluation-harness)、[HF Dataset Cards](https://huggingface.co/docs/hub/en/datasets-cards)。2026-11-14 查阅，具体 API 以固定版本为准。

## 1. 训练不能只保存 Model Weights

| 状态 | 专业意义 | 大白话 | 丢失后会怎样 |
|---|---|---|---|
| Model Weights | 学到的参数 θ | 练习后的能力 | 无法恢复参数 |
| Optimizer State | AdamW 一/二阶矩、步数等 | 教练记住前面怎么调整 | 恢复后更新轨迹改变 |
| Scheduler State | 学习率 warmup/decay/step | 当前训练进度表 | 学习率恢复错误 |
| RNG/CUDA State | Python、NumPy、PyTorch、设备等随机状态 | 抽签记录 | Dropout/采样轨迹难复现 |
| Data/Sampler Cursor | 顺序、shuffle、epoch、样本偏移与 worker 状态 | 学到教材第几页 | 重复或漏样本、泄漏 |
| Config/Revision | 模型、Tokenizer、Chat Template、数据和源码 SHA | 全套机器/原料型号 | 同名实验不等于同方法 |
| DType/Distributed | BF16/FP16/FP32、精度/混合精度、FSDP/Sharding topology | 机器精度和工位分工 | 数值、通信/资源行为变化 |

**区别**：“能加载权重做推理”不等于“能完整恢复训练”。本仓 TinyGPT Toy 只验证**模型/优化器重新加载输出一致**，不是训练轨迹精确复现；真实恢复还必须处理 Scheduler、Sampler、数据管道、RNG、Dropout 等状态。官方 PyTorch 也明确：即使同样 Seed，跨设备和版本完全位精度复现**不保证**。

## 2. Loss、优化器和显存的故障坐标

| 现象 | 应检查的先后顺序 | 误区 |
|---|---|---|
| Loss 不下降 | 样本/label 数、Shift 是否重复、Mask、Gradient 非零、LR、数据难度、模型/目标错配 | 加 Epoch 不修错标签 |
| NaN/Inf | Softmax/CE 数值、全 ignore labels、FP16 scale、LR、grad norm、empty batch | 只要换 BF16 就一定不 NaN |
| GPU OOM | Weights/Grads/Optimizer/Activations、Workspace/Allocator、KV/rollout、Batch×Seq×dtype | 模型权重能放进显卡就能训练 |
| 训练速度慢 | DataLoader、CPU→GPU、Kernel launch/HBM、Profiler、梯度累积、Distributed communication | 模型 FLOPs 一样就会一样快 |
| 验证集退化 | 真实数据变化、过拟合、泄漏、模板、数据配比、CPT 遗忘 | Train Loss 下降代表泛化提升 |
| RL Reward 升但结果差 | 结果验证器、组内奖励方差、奖励投机、长度/截断、Reference/KL、独立任务集 | Reward 就是任务准确率 |

## 3. 哪个评估指标对应哪个问题？

| 指标 | 定义与分母 | 使用条件 / 常见误用 |
|---|---|---|
| Token NLL / PPL | 有效目标 Token 的平均 -log p，PPL=exp(NLL) | 特定 Tokenizer 与分词规范下才可比；不是任务成功率 |
| BPB | 总 NLL / (有效文本 UTF-8 Byte 数·ln 2)，须固定上下文和计数策略 | 解决不同词表 PPL 比较困难，但也要统一 Unicode/测试集和训练污染口径 |
| Exact Match/Accuracy | 正确样本数 / 全部符合定义的测试样本数 | 报告样本数/难度/容错；不能漏掉失败记录 |
| Precision/Recall/F1 | TP/(TP+FP)，TP/(TP+FN)，二者调和均值；需定义零分母规则 | 用于分类、检索/证据匹配，不自动替代生成事实正确 |
| Recall@k / MRR / nDCG | 检索命中和排序质量 | RAG 应拆“召回差”与“生成/引用差”，未定义标注相关性无法计算 |
| JSON Valid Rate | 合法 JSON / 全部应输出 JSON 的任务 | 格式对也可能工具错/参数错/越权 |
| Tool Selection/Argument/Execution | 各独立正确率（分母必须清楚） | 不能只对已经成功执行的工具操作统计，避免幸存者偏差 |
| Citation Support/Refusal | 有证据的断言被支持情况、无证据/不授权场景拒绝质量 | 伪造一条引用不应得分；必要时逐 claim 审核 |
| E2E Task Success | 真正完成定义任务的数量 / 全部候选任务 | 多步 Agent 的重要目标；必须包括超时、失败、无权限 |
| Preference Win Rate | 在固定盲评和候选顺序下胜出的次数 / 有效对照次数 | 不是事实正确率；记录 tie、judge 偏差与样本依赖 |
| Reward/KL/Length | 奖励目标、策略漂移与输出长度/截断的共同监控 | GRPO 的奖励可投机；KL 参数可能为 0 或未启用 |
| TTFT/TPOT/P95/吞吐 | 首输出、生成阶段逐 Token 耗时、请求尾延迟分位、稳定出吞吐 | 必须固定输入/输出长度、并发、warmup/queue，平均值掩盖尾延迟 |
| 置信区间与配对对比 | 二分类可用 Wilson interval；模型对比在同一任务上做 paired bootstrap | 不是重复同一请求 20 次就有 20 个独立用户；重复采样要匹配抽样单位 |

## 4. 训练、验证、测试、线上反馈为什么要隔离？

- **训练集**：给模型学习参数。
- **验证集**：用于选择模型、调学习率/停止时机/Prompt。反复用就会过拟合验证集。
- **最终测试集**：事先锁定、避免在其上选超参和修规则；按任务族/用户/文档/时间等合理单位防泄漏。
- **线上反馈**：有偏差、权限/隐私/样本选择问题，只有经过脱敏、许可检查、标注复核才能进入后续训练或回归集。

**反例**：一个产品说明书的不同改写分别进训练和 Test；Agent 测试只统计工具成功案例而把 404/超时/被拒绝丢弃；对照系统和新系统的 Temperature、Max Tokens 不同但宣称算法胜利。

## 5. 三个按需求执行的最小练习

1. 从 [任务级合成评测](../labs/task-evaluation/README.md) 读取**实际 16 条**预标注合成样本，运行 [脚本](../labs/task-evaluation/evaluate.py)，记录 JSON/工具/引用/E2E 的不同分母与 Wilson Interval。**真实样本数依代码数据文件，不应写成 15 或 30。**
2. 从 [TinyGPT](../labs/tiny-gpt/README.md) 只测试临时模型和优化器恢复；把“完全可恢复训练”列为未验证项，设计 Sampler/RNG/训练继续等额外检查。
3. 假设一个 0.6B 的 Qwen SFT/GRPO 发生 OOM，先列出 Memory 分项和修复顺序；只有实际 GPU 测试日志才能写“16GB 可跑”结论。真实验证须按 [实验模板](../experiments/EXPERIMENT-TEMPLATE.md) 记录版本、数据哈希、显存峰值与配置。

## 6. 建立能用来判断发布与否的报告

每次记录 **Run ID / 需求与基线 / Model-Tokenizer-Data-Code SHA / 分割方案 / 主要指标和分母 / 95% CI 与条件 / 负例 / 成本与时间 / 实际失败 / PASS/FAIL/INCONCLUSIVE / 下次动作**。生产性任务再加 [G0–G8](../production/PRODUCTION-READINESS.md)；只做研究可以止于陌生任务迁移，不必须实际部署。

**停止规则**：有证据回答今天的问题就停止，不为课程完成度主动制造额外训练。
