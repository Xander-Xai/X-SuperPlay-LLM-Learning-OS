# 合成数据、拒绝采样与后训练数据工程（P0）

## 1. 目标

不能止于下载公开 SFT/DPO 数据集并训练。要能回答：数据哪里来、为何可信、坏数据如何检测、工具调用轨迹如何验证、偏好对为何代表真实任务。

## 2. 数据生成流水线

~~~mermaid
flowchart LR
  T[任务种子与模板] --> M[教师模型或当前策略 N 次采样]
  M --> V[工具/规则/单元测试验证]
  V --> F[格式/事实/安全/重复过滤]
  F --> H[人工抽检和分层采样]
  H --> Split[按任务族与来源去重切分]
  Split --> Train[SFT / DPO / RL 数据]
~~~

推荐字段：task_id、scenario、source_id、schema_version、prompt、tools、messages、expected_tool_trace、observations、citations、verifier_result、generator_model_revision、filter_reason、split、timestamp、license。

### Rejection Sampling / RFT

同一个 Prompt 生成 N 个候选；先做可机验的正确性（数学答案、API schema、代码测试、文档证据），再保留符合条件的轨迹作为监督样本。**不是简单挑最流畅的答案**；如果验证器失准，会把错误当成金标。

### 教师蒸馏式造数

强模型可生成指令、步骤、推理轨迹或工具计划；对事实引用和真实工具返回必须另行验证。合成 CoT 不等于真实/可靠推理过程；对外发布或训练前检查数据许可、隐私和政策限制。

### 偏好对

- Prompt 固定，chosen 与 rejected 应对应同一任务；尽量说明排名依据（正确性、证据、工具调用成功、格式）。
- 区分外部静态集、当前策略采样后固定的离线数据、训练中持续重新采样的 Online DPO。
- 按任务难度、失败类型、工具种类统计分布；不要用重复模板淹没真实多样性。

## 3. 质量门槛

- JSON/schema 通过率；Tool Name/Arguments 检验；数据与工具输出一致性。
- 引用 ID 必须在可检索证据集中存在，内容支持结论。
- 近重复去重与训练/测试任务族隔离，防止模板泄漏。
- 记录拒绝原因和保留率；抽检样本覆盖所有任务类，发现重大缺陷应回退生成步骤。
- 同一评测集不得用于挑选训练样本或训练超参。

## 4. 本仓库应用

使用“企业产品库存 + 知识检索”沙盒；**不直接使用真实商业敏感数据**，如使用内部数据须有授权和脱敏。见 [Agent 工具轨迹](../sft-peft/agent-tool-calling-loss-mask.md)。

