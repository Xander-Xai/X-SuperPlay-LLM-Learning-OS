# 已合并分支安全清理｜2026-11-15

> **目的**：兑现 [Issue #25](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/issues/25) 的实际远程分支删除，而不把“创建清单”当作完成。默认分支、任何仍被开放 PR 使用的分支、SHA 已变化的分支一律禁止删除。删除是 Git 远程引用操作；**不会删除已合并的 PR、main 内容或相关 Git commit 历史**，但会取消分支指针，需审慎执行。

## 执行机制

- [已审清单](branch-retirement-manifest.json) 当前固定 **24 条**经两轮复验的历史分支（其中 23 条已合并 PR，1 条 main 祖先）。第一轮 [Actions #43621192846](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/actions/runs/43621192846) 实际删除 22 条并回读确认；原清单中 docs/agent-loop 分支 SHA 变化，是因 [PR #28](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/pull/28) 在随后合并，已核实其最新 head SHA；另加入已合并 [PR #29](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/pull/29) 的残留分支。第二轮在每次删除前依旧重新读取实际 HEAD、PR 和 open PR，不根据旧结论盲删。
- [清理器](retire_merged_branches.py) 每次从 GitHub 实时读取：分支是否受保护、最新 SHA、有无开放 PR、指定 PR 是否确实已合并及 head 是否仍一致；对于孤儿祖先分支，要求与 main 比较结果的 `ahead_by == 0`。
- [GitHub Actions](../../.github/workflows/retire-merged-branches.yml) 只在 **main** 合并此功能时对清单执行删除。流程使用 GitHub 内置、限制权限的 `GITHUB_TOKEN`（`contents:write` / `pull-requests:read`），**不需外部 PAT、不存密钥**。也可以由仓库维护者在 main 上手动 Workflow Dispatch 重试。
- 每次调用 GitHub DELETE API 后，必须通过 GET 回读验证分支确实不存在；拒绝用 force push、update_ref 将分支指向 main 来冒充删除。删除失败（403/规则阻止）时 workflow 必须红灯，Issue #25 仍保留。
- 本次清理器还会对“承载清理器的 PR 分支”执行一次严格的 **已合并 PR + HEAD 匹配 + 无开放 PR** 检查，满足才删除，不会通配删除陌生分支。

## 本地静态检查（无令牌，无远程修改）

```bash
python -m unittest discover -s LLM-Training/governance -p 'test_*.py' -v
python -m py_compile LLM-Training/governance/retire_merged_branches.py
```

如需在已授权且允许读取 GitHub API 的本地环境预览（只读）：

```bash
GITHUB_REPOSITORY=Xander-Xai/X-SuperPlay-LLM-Learning-OS GITHUB_TOKEN=YOUR_TOKEN python LLM-Training/governance/retire_merged_branches.py --dry-run
```

注意：这里的 `YOUR_TOKEN` 是本地环境变量示意，禁止写入 .env 提交到仓库，禁止打印或分享令牌。没有通过 CI 的代码审核不要在本机加 `--apply`（该模式只接受 main 的 GitHub Actions 上下文）。

## 完成判据

1. PR CI `docs` 与 `cpu-toy` 通过、清理专项守卫单测通过。
2. main merge 后专项 workflow **SUCCESS**，记录其 run URL。
3. 通过 [Branches API](https://api.github.com/repos/Xander-Xai/X-SuperPlay-LLM-Learning-OS/branches?per_page=100) 回读，仅 `main` 与新开展工作必需的分支存在；对每个目标报告删除/跳过原因。
4. 仅在远程实际核验后关闭 [Issue #25](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS/issues/25)。
5. Issue #20–#24 涉及 GPU/外部模型/安全部署，**不会通过此清理任务擅自修改为完成**。

## 停止与故障处理

- 任一候选 SHA 变化、变为 protected、PR 重新开放、出现新引用：该候选 SKIP，不会被删除；需要人工复审后才能更新 manifest。
- 权限不足：workflow 会报 403，所有未删分支继续保留；维护者应检查 GitHub Actions 的 GITHUB_TOKEN 写权限或组织规则集，不能通过创建无审核的外部 PAT 绕过。
- 如果分支实际删除后需要恢复：在明确旧 SHA 与授权后通过 GitHub 创建分支指向原 SHA，完整原提交 SHA 已存在 manifest；这不是鼓励无需审核地恢复被删除的旧工作分支。

该工作流仅是 **PR/Branch 生命周期治理**，与真实 MiniMind、SFT、GRPO、Agentic RL、RAG 评测和 vLLM 的完成度无关。
