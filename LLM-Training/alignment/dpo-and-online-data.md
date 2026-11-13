# DPO 与偏好数据：静态、策略自采样、Online DPO

## 为什么还需要偏好优化

SFT 学的是被展示的目标回答；DPO 用 chosen/rejected 的相对偏好，改变模型对候选响应的概率偏好，通常不需要预先训练独立 Reward Model。注意 **正确性、格式与偏好不是同一个指标**，仍应以可验证任务和人工抽检衡量。

## 关键概念

- Policy πθ、Reference πref、chosen yw、rejected yl、beta 及 log probability。
- DPO 损失可以理解为：鼓励 chosen 相对 rejected 获得更高的策略-参考模型 log-prob 差。
- DPO 的 reference-free、不同 loss type 和其他变体需要看实现版本，不要把某一配置当作通则。

## 两类离线数据与在线区别

| 类型 | 构造 | 风险与解释 |
|---|---|---|
| 外部静态偏好 | 公开数据/教师样本 | 可能偏离当前策略或任务 |
| SFT 策略自采样后固定 | SFT 模型 N 候选，经规则/人/评审模型排序 | 训练中模型改变后，这批固定数据不再持续 on-policy |
| Online DPO | 训练过程中持续采样与偏好反馈 | 训练更复杂、成本更高；不保证一定优于离线 |

**研究假设**：当前模型采样的数据可能与当前能力更匹配，但并非普遍更好；控制样本数量、任务分布、标签质量、训练步数后再评估。

## 训练计划

1. 固定 SFT Checkpoint + 独立测试集。
2. 用相同任务准备离线外部组与策略自采样组；记录采样温度、候选数量和排序证据。
3. 各自 DPO 训练，保存 beta、reference、学习率、训练配置和日志。
4. 对比偏好胜率、正确率、工具调用成功率、回复长度、拒答与过度优化情况。
5. 如果预算允许，另做 Online DPO 小实验，不能混称为同一方法。

详见 [04 DPO 实验](../experiments/04-dpo/README.md)。

官方资料：[DPO 论文](https://arxiv.org/abs/2305.18290) · [TRL DPO](https://huggingface.co/docs/trl/dpo_trainer) · [TRL Online DPO](https://huggingface.co/docs/trl/online_dpo_trainer)。

