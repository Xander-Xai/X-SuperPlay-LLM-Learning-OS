# 仓库治理看板｜GitHub PR / Branch / Issue 与未完成实验

> 2026-11-15 静态快照，**实时状态始终以 GitHub Issues、Pull Requests 与 Branches 页为准**。此文档解释治理原则与已证实的阶段状态，不是自动刷新的完成率排行榜。

## 当前可追溯事项

| 优先级 | Issue | 工作范围 | 当前阶段 |
|---|---|---|---|
| P0 | [#25 清理合并遗留分支](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/issues/25) | 19 条历史可清理分支，保护活跃 PR #19 | 阻塞：缺 GitHub delete-ref 工具/网页已登录上下文 |
| P1 | [#20 MiniMind / CPT](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/issues/20) | 01/02 真实 GPU 实验、基线与防遗忘 | NOT RUN |
| P1 | [#21 Tool SFT / DPO / GRPO](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/issues/21) | 03/04/05 同一模型起点与独立评估 | NOT RUN |
| P1 | [#22 Agentic RL](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/issues/22) | 可重置多步环境 A/B/C 真实策略更新 | NOT RUN |
| P1 | [#23 RAG 真正评测](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/issues/23) | 合成 120-case 之外的真实 Embedding/任务评测 | NOT RUN |
| P2 | [#24 Serving / G0–G8](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/issues/24) | 06 vLLM/Profiler/端到端回归、安全门禁 | NOT RUN |

**依赖建议**：优先 #20 或 #21 取得真实模型/数据基线，#22 才能评估 Agentic RL 的增量；#23 可独立并行；#24 需目标模型和测试环境。任务被阻塞时保留 Issue，不用把未执行写成“已完成”。

## PR 核查摘要

- PR #1–#18：2026-11-15 在 GitHub connector 逐条读取，`merged=true` 且`state=closed`。
- PR #19：核查时为新开放的 Agent Curriculum 深度补强，须根据其**最新 head SHA**、审查与 `docs/cpu-toy` 再决定是否合并；**不要清理其分支 `docs/agent-deep-audit-20261115`**。
- 所有历史 PR 的 CI 通过属于各自 commit 的结果，不应等同于新主分支的长期稳定性证明。

## 分支清理与剩余障碍

- 发现共 20 条非 `main` 分支：18 条对应已合并 PR #1–#18、一条 `feat/llm-crossstack-upstream-demand-map-20261114` 是 main 历史祖先、一条现对应开放 PR #19。
- 可核验的 19 条清理候选和双重检查列在 [Issue #25](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/issues/25)；本轮现有连接器**没有提供 branch deletion 操作**，因此不能声称已删。若用户建立已登录的 GitHub 浏览器会话或提供具有 delete-ref 能力的连接，则可在二次核验后实际清理。
- 不要通过 force update 分支到 main 来伪装删除；不动 `main`、保护分支和开放 PR 的工作分支。

## 长期规则

以 [贡献/治理规范](../CONTRIBUTING.md) 和 GitHub 模板为准：一任务一 Issue、一可审查变更一 PR、CI + 可核实日志、合并后验证 main、证据充分才关闭 Issue；没有 GPU/业务授权时接受保留真实实验 NOT RUN 状态。
