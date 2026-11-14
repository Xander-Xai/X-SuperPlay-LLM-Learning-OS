# 实验 04 — DPO：外部静态数据 vs 当前策略自采样

**状态：NOT RUN**。以实验 03 的**同一 SFT Checkpoint** 为起点，先比较独立 DPO 分支，不与 GRPO 混杂。

**开始前的无 GPU 演练**：[DPO 相对 log-prob / beta / 失真 reward 数值实验](../../labs/preference-rl-math/README.md)。通过玩具单测只说明理解公式，不构成 DPO 模型训练完成。

## 输入

prompt + chosen + rejected。偏好对来源分两组：A 外部/教师，B 当前 SFT 模型自采样若干候选后自动验证与人工抽检。匹配数据条数、任务类别、奖励质量与训练预算。**B 训练固定数据集仍是离线 DPO，不是在线 DPO。**

## 动作

1. 定义偏好证据：正确调用工具、参数合法、引用支持而非凭主观流畅度选。
2. 固定 SFT 基线；记录 reference model、beta、loss type、tokenization、max lengths。
3. 运行 A/B 独立分支并保存数据生成和排序证据。
4. 看 held-out 偏好胜率、工具任务成功、错误分类、回答长度与过度拒答。
5. 可选：研究 TRL Online DPO 与离线策略自采样的区别。

## Done

- [ ] 两组原始偏好数据、过滤和拆分可复现。
- [ ] DPO 训练指标及独立正确率/胜率齐全。
- [ ] 能解释 chosen/rejected logprobs、reference 和 beta 的影响。
- [ ] 对照结论不写成“自采样一定优于外部数据”。

专题：[DPO](../../alignment/dpo-and-online-data.md)。

