# LLM 独立能力验收 Rubric（L0–L4）

> 对一个具体任务进行评分，不因课程章节打卡自动升级。评估人可以是自己闭卷、同行复核或自动测试，但**必须写明谁评估以及证据来源**。机器单测只证明局部代码，不证明本人会解释或独立完成。

| 级别 | 什么叫通过 | 最低证据 | 常见假通过 |
|---|---|---|---|
| L0 知道位置 | 找到知识在训练/后训练/推理哪个域 | 说明输入输出和一个替代方案 | 罗列名词 |
| L1 真正理解 | 专业定义+白话+公式+适用边界 | 闭卷解释 3 问、写出反例 | 复制文档 |
| L2 自己实现 | 读懂源码并修改、跑测试可复现 | 代码 SHA、配置、数据/seed、输出 | 只调高层 API 无法定位 |
| L3 诊断/比较 | 失败复现、受控对照、明确结论边界 | baseline、negative cases、profile、回归 | 只拿 Loss/Reward 进步截图 |
| L4 陌生任务迁移 | 解决未提前给过的任务并排障，必要时符合发布门禁 | 盲测、独立修复、跨场景结果、Go/No-Go | CI 成功即说个人掌握 |

**映射规则**：V2 的 L1/L2/L3 是学习深度建议，不是个人历史测试成绩；V3 通过 L0–L4 明确了独立迁移等级，不能将旧标签直接视为新 L4 PASS。上游方法论还可能有其自身层级表达，记录语义和来源，不进行机械整数换算。

## 五项不可绕过的硬条件

1. **真实性**：每条“通过”有原始运行日志、环境、完整模型/数据版本、SHA；合成数据标记 SYNTHETIC。
2. **反例**：至少两类错误/失效输入被覆盖，且能解释何种方法会失效。
3. **基线与归因**：写清不训练的方案，至少一个受控变量对照；无法匹配预算时说明不公平。
4. **独立性**：闭卷追问或独立修改一个陌生问题，不能只依赖辅助 AI 自动生成。
5. **停止规则**：达到当前任务目标立即停止不必要的扩大；不能无限扩展实验来“填满模块”。

## 生产门禁与评分的边界

- 仅研究原理的任务：L4 可以通过陌生迁移，不强制实际部署。
- 目标明确是真实上线：L4 还要验证 [生产门禁 G0–G8](../production/PRODUCTION-READINESS.md)，但具体风险/场景适配。
- 本仓 CI 通过仅代表代码和文档静态合同通过，**不代表真实模型、真实业务、个人技能级别通过**。

## 闭卷复核样例

- 如果模型 tool call JSON 合法但参数错误，如何区分模型问题、模板问题、工具定义问题？
- 假设 vLLM 服务 P95 升高，什么数据能证明是 KV Cache 而非排队/网络？
- 为什么 DPO 用自采样静态数据不等于真正持续 On-policy？
- 如果 CPT 领域 Loss 低、通用退化，如何设计 Data Replay 与非训练基线？
- 为什么 GRPO 训练的 Reward 上涨，依旧可能被判 FAIL？
- 新场景允许更低正确率但要求更小显存时，你如何做指标权衡和回滚？

## 最低交付格式

```text
Task ID / Status / Level Requested / Examiner
Original Problem / No-training Baseline / Core Mechanism
Code SHA / Model Revision / Data Hash / Exact Command / Seed
Main Metric / Guardrails / Negative Cases / Failure Trace
Controlled Change / Before-After / Unknown Transfer
Evidence URLs / PASS-FAIL-INCONCLUSIVE / Stop or Next Gap
```

