# 仓库治理看板｜GitHub PR / Branch / Issue 与未完成实验

> 2026-11-15 静态快照，**实时状态始终以 GitHub Issues、Pull Requests 与 Branches 页为准**。此文档解释治理原则与已证实的阶段状态，不是自动刷新的完成率排行榜。

## 当前可追溯事项

| 优先级 | Issue | 工作范围 | 当前阶段 |
|---|---|---|---|
| P0 | [#25 清理合并遗留分支](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/issues/25) | 已有 [GitHub Actions 安全清理器](governance/README.md)，按真实 GitHub API 回读验收 | [Issue #25](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/issues/25) 已结案，历史远程分支由 PR #29/#30 及工作流实际清理并回读；新增 PR #31 的残留分支单独核验 |
| P1 | [#20 MiniMind / CPT](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/issues/20) | 01/02 真实 GPU 实验、基线与防遗忘 | NOT RUN |
| P1 | [#21 Tool SFT / DPO / GRPO](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/issues/21) | 03/04/05 同一模型起点与独立评估 | NOT RUN |
| P1 | [#22 Agentic RL](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/issues/22) | 可重置多步环境 A/B/C 真实策略更新 | NOT RUN |
| P1 | [#23 RAG 真正评测](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/issues/23) | 合成 120-case 之外的真实 Embedding/任务评测 | NOT RUN |
| P2 | [#24 Serving / G0–G8](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/issues/24) | 06 vLLM/Profiler/端到端回归、安全门禁 | NOT RUN |

**依赖建议**：优先 #20 或 #21 取得真实模型/数据基线，#22 才能评估 Agentic RL 的增量；#23 可独立并行；#24 需目标模型和测试环境。任务被阻塞时保留 Issue，不用把未执行写成“已完成”。

## PR 治理证据与分支清理

- 原有 PR #1–#19 与后续 PR #26–#31 均已合并；最新 main CI 以对应提交 SHA 为准；所有最新 open PR 均以 GitHub 实时列表为准。**“Merged” 表示代码完成合并，不证明下方真实 GPU/LLM 训练已执行。**
- 曾残留 23 条已合并/历史分支。首次删除工作流 [Actions #43621192846](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/actions/runs/43621192846) 通过带写权限的 `GITHUB_TOKEN` **实际删除并回读确认 22 条**；唯一跳过的是 `docs/agent-loop-and-loop-engineering-20261115`，原因是核查后 SHA 变化（按设计拒绝误删）。
- 进一步验证该分支最新 SHA `e91e079f` 已随 [PR #28](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/pull/28) 合并；另有首轮清理自身的 [PR #29](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/pull/29) 分支需要清理。已在 [SHA-pinned 清单](governance/branch-retirement-manifest.json) 中复核与更新两者；如发生新的 PR 或 HEAD 变化仍会再次停止并保护新代码。
- **PR #31 的残留分支 `audit/agent-loop-verifier-contract-and-retirement-20261115` 已在本次清理清单中精确锁定；合并后的 main workflow 执行删除，必须二次读取远程证据才能标记完成。最终远程状态以 [Issue #25](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/issues/25) 的验收记录和 [Branches API](https://api.github.com/repos/Xander-Xai/X-SuperPlay-LLM-Learning-OS/branches?per_page=100) 为准**；此文档不是实时状态缓存。
- 所有后续 PR 的新工作分支只在有真实合并证据、无引用/新提交时清理，严禁 force reset 代替删除。

## 长期规则

以 [贡献/治理规范](../CONTRIBUTING.md) 和 GitHub 模板为准：一任务一 Issue、一可审查变更一 PR、CI + 可核实日志、合并后验证 main、证据充分才关闭 Issue；没有 GPU/业务授权时接受保留真实实验 NOT RUN 状态。
