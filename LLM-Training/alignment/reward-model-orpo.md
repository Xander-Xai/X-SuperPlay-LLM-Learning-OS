# M07 补足：Reward Modeling、ORPO 与 DPO 的关系

## 1. Reward Modeling (RM)

经典 RLHF 流程中，给定相同 prompt 的 chosen/rejected 回答，训练一个评分模型 `r(x,y)`，使 `r(chosen)>r(rejected)`。常见 pairwise loss 为 `-log sigmoid(r_chosen-r_rejected)`。这不是模型回答本身的正确性证明：标注偏差、长度偏好、领域覆盖不足会传递到 RL 奖励。

**练习**：拿三组有明确工具验证证据的偏好对，打印模型评分差并解释误判；没有训练 RM 的情况下用人工拟分数做公式演练，明确这是模拟。

## 2. DPO

DPO 直接以 chosen/rejected 以及 policy/reference log probability 优化策略，不需要先训练独立 RM、再做 PPO 的经典两步。不要把 DPO 当成“用奖励自动回传的 PPO”，损失和采样形式都不同。详见 [DPO 专题](dpo-and-online-data.md)。

## 3. ORPO

ORPO 是一种偏好优化方案，将被选回答的 NLL 与基于 odds-ratio 的偏好损失结合。需要区分其目标与 DPO 的 reference 模型方案；不能宣称 ORPO 必然更省显存/更好，需在相同训练与测试预算下比较。

## 4. 必考对照

| 方法 | 需要什么数据 | 需要单独 RM？ | 主要风险 |
|---|---|---|---|
| RM + PPO | chosen/rejected 训练 RM；在线 rollout | 经典配方通常需要 | RM 偏差、训练/采样复杂 |
| DPO | 偏好对；可以静态离线 | 通常不需要 | 静态分布、参考策略与长度偏差 |
| ORPO | instruction + chosen/rejected | 通常不需要 | odds-ratio 配方和超参敏感 |

原始资料：[InstructGPT](https://arxiv.org/abs/2203.02155) · [DPO](https://arxiv.org/abs/2305.18290) · [ORPO](https://arxiv.org/abs/2403.07691)。**验收**：能清楚说出每种方法的数据流、损失、是否 online，以及何种能力指标证明其价值。

