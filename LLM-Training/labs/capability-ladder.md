# 能力阶梯与最小实作台｜不只读理论，也不替代真实产品仓

学习者可从任何任务进入，沿深度**L0→L4**提升（在当前任务内提升，不强求所有主题同级）。每项练习必须先定需求、主指标与不做训练基线，验证关键负例并做独立迁移。

## 六种练法（不同于六门课程）

| 练法 | 动作 | 实际产物 | 怎样证明不是只会照抄 |
|---|---|---|---|
| 1 定义/推导 | 输入、输出、公式、shape、边界 | 一页概念卡与失效例子 | 关资料解释一个未知例子 |
| 2 源码定位 | MiniMind/TRL/vLLM 找最短执行链 | 文件/函数路径、张量与事件表 | 在新版本中重新定位 |
| 3 最小可跑 | 合成/公开小数据跑单测 | 命令、数据 SHA、日志 | 换种子/扰动输入后重跑 |
| 4 消融与排障 | 只改变一变量，注入负例 | before/after、Profiling、错误原因 | 无法提升时也能解释证据 |
| 5 陌生迁移 | 换任务族、工具、数据域或模型 | 独立测试与新错误分类 | 不借用答案或泄漏测试 |
| 6 生产演练 | 负载、权限、观测、回滚 | release packet + Go/No-Go | 故障时定位和恢复 |

## 任务 A：谁在算 Loss？

- 看 [CPU Shift/Mask](README.md) 的 5 个测试，复现 `-100`、shift-one、梯度位置。
- 再在真实 MiniMind 里用 hooks 观察 `[B,T,V]`，对比 Pretrain 与 assistant-only SFT。
- **负例**：标签全是 -100、shift 两次、工具 observation 误计 loss。
- 证据：模型代码 commit、测试、输入/标签/梯度摘要。
- **不能冒充**：本仓 CPU Toy 的 PASS 不是 MiniMind 训练通过。

## 任务 B：先不训练的 Agent/RAG 基线

**可立即运行**：[合成工具网关及 11 项边界测试](synthetic-tool-gateway/README.md)：不是模型训练，而是真实可执行的授权/证据/参数防线。

- 两只读工具 + 数据源引用 ID；确保权限由工具层校验。
- 实现 10 条正常 + 5 条工具失败 + 5 条无权限/无证据的虚构样例。
- 记录 schema valid、argument accuracy、task success、unsupported claim 和 P95。
- 只在这条基线确有模型行为缺陷时，研究 [Qwen SFT](../experiments/03-agent-tool-sft/README.md)。
- **迁移**：把 inventory 工具改为 order-status（仍只读），重新定义参数与正确率。

## 任务 C：训练后的对照与责任边界

- 同一个 SFT checkpoint 分叉 DPO/GRPO；数据、reward、选题范围需记录。
- 用 held-out 测正确性/长度/错误样例，关注 reward 高但任务低的情形。
- **迁移**：换验证器输入格式，证明 reward 不依赖训练集里固有标记。
- 成果可以是“当前数据/算力不值得上 RL”。

## 任务 D：推理服务性能诊断

- 选定一个可推理的公开小模型，用本机实际支持的服务/设备测 baseline。
- 冷/热、1/多并发、短/长上下文，固定解码配置，分别记录 TTFT/E2E P95/tokens/s/VRAM。
- 选一个变量：batching、量化或 max_model_len，只改一个。
- **迁移**：换到另一个模型或设备，写清不可比条件和解释。

## 任务 E：CPT vs RAG 是不是训练问题？

- 同一领域任务固定集合与原始 Base。
- 测不训练的检索回答、域内 Domain-CPT、Replay-CPT 及成本。
- 不让 domain 数据/测试数据泄漏；即便最终 CPT 没提升，也能有可验收结论。
- **迁移**：改变领域/术语分布，重新做 Build-vs-Buy 决策。

## 任务 F：生产级失败恢复

- 以虚构工具链模拟：工具超时→重试/幂等→最终答复；另模拟灰度 B 模型解析变差→回滚 A。
- 测全链路 trace 是否可关联到工具 ID、输入版本、模型输出和事件。
- **迁移**：把工具替换为权限不同的只读 API，继续检验越权和回滚。
- 去 [生产门禁](../production/PRODUCTION-READINESS.md) 完成正式材料。

## 记录方式

每个任务取一张 [需求卡](../demand-driven/DEMAND-CARD-TEMPLATE.md)，并在 [实验模板](../experiments/EXPERIMENT-TEMPLATE.md) 中留下真实证据。**文档计划不是实际运行，也不等于个人掌握**。

