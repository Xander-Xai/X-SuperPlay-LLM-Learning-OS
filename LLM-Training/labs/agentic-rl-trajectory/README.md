# Agentic RL 多步环境 + Tabular Q-learning｜CPU 教学实验

> **SYNTHETIC / TABULAR RL / NOT LLM TRAINING**。仅 Python 标准库、无网络、无支付/订单调用、无真实副作用。它演示多步工具操作、硬权限门禁、状态反馈、轨迹采集与**确实发生的表格策略更新**，不是 LLM 的 PPO、GRPO 或真实 Agent Lightning 训练。

## 与现有实验的关系

- [DPO/GRPO 数学](../preference-rl-math/README.md)：公式、奖励分组、Reward Hacking；**没有训练策略**。
- [合成工具网关](../synthetic-tool-gateway/README.md)：函数调用安全与鉴权；**没有训练策略**。
- **当前实验**：环境 reset、多步状态与反馈、off-policy **Q-learning** 对 Q-table 做真实更新。它的作用是学习 Agentic RL 的环境与训练分工，而非声称模型权重发生更新。

## 一键运行（从仓库根目录）

```bash
python LLM-Training/labs/agentic-rl-trajectory/trajectory_lab.py
python -m unittest discover -s LLM-Training/labs/agentic-rl-trajectory -p 'test_*.py' -v
```

输出 before/after 是 Toy Policy 在固定合成任务集上的正确率、被拦截动作比例和平均工具步数；q_values 是训练前后有差异的表格参数。不能迁移成真实 LLM 的性能结论。

## 状态机与安全约束

```text
start --lookup--> looked_up --policy--> eligible / ineligible
eligible   --refund--> success (仅模拟状态变化)
ineligible --deny----> success
未经正确核验直接 refund → guardrail_blocked，绝无退款副作用
错误 deny 结束任务；无效动作给予负奖励并可能超时终止
```

Task.eligible 是**环境真值**，策略在完成 policy 核验前只能看到 start/looked_up，不准偷看标签。reset 隔离每个 episode，轨迹记录 state/action/reward/observation/termination。训练和测试只按合成任务 ID 隔离，不能视作真实数据泛化证据。

## 5 项动手任务

1. 对比 run_scripted（固定工具顺序、无学习）与 train_tabular_policy（Q-table 确实更新）；解释“调用工具≠训练”。
2. 手算 Q-learning TD 更新：Q(s,a) ← Q(s,a)+α[r+γ max_a' Q(s',a')−Q(s,a)]，指出和 GRPO 的关键差异。
3. 注入不合规 refund 并检查 guardrail_blocked 与 refund_executed=False：**硬门禁优先于奖励**。
4. 用 superficial_format_reward 评价失败/成功的 JSON：两者可能同分，证明格式奖励不等于任务正确率。
5. 修改动作代价/错误步骤上限，记录 seed、代码 SHA、测试前后结果；不能只展示训练结果不分析失败。

## 退出与真实训练升级

- [ ] 本仓脚本与 7 个单元测试通过；亲自解释各负例。
- [ ] 能说出状态/观测、动作、终局奖励、执行权限与信用分配的区别。
- [ ] 能清楚指出该 Toy 与 LLM Agentic RL 的区别：**表格 Q 更新 vs Token Policy Gradient**、无模型/Token Mask、无 GRPO 分组与真实 Rollout Worker。
- [ ] 后续 GPU 训练另开 run_id，按 [Agentic RL Bridge](../../experiments/agentic-rl-bridge/README.md)、[05 GRPO](../../experiments/05-grpo/README.md)、[实验模板](../../experiments/EXPERIMENT-TEMPLATE.md) 记录真实证据；保持当前 **NOT RUN**。

官方学习参照：[Spinning Up 基础概念](https://spinningup.openai.com/en/latest/spinningup/rl_intro.html) · [TRL GRPO Agent Training](https://huggingface.co/docs/trl/grpo_trainer) · [Agent Lightning v1.0](https://github.com/microsoft/agent-lightning/blob/main/docs/README.md)。
