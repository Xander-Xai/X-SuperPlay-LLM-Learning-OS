# X-SuperPlay-LLM-Learning-OS｜贡献与治理规范

> 该仓库是**学习、实验和能力验收知识库**，不是已经部署的生产应用。PR、Issue、分支与实验状态应形成同一条可审计证据链。2026-11-15 起适用；历史 PR #1–#18 已全部合并，不要求倒补模板。

## 1. Single source of truth

- **课程结构**：`LLM-Training/README.md`、M01–M12、五类训练实验（01–05）与部署验收（06）；不随意新增平行 M13/实验07/重复索引。
- **学习状态**：`LLM-Training/learning-progress.md`；L0–L4 只参考 [Capability Rubric](LLM-Training/assessments/CAPABILITY-RUBRIC.md)，生产 G0–G8 单独判断。
- **工程未完成事项**：GitHub **open Issues**，以可执行验收条件为准，见 [Backlog](LLM-Training/MAINTENANCE-BACKLOG.md)。
- **提交记录**：PR 解释变化，CI 记录静态检查和 CPU 测试；真实 GPU、外部服务、业务数据必须有独立运行证据。

## 2. Issue 流程

1. **新增任务前**：搜索 open/closed Issue 与现有课程、实验入口，避免以同义词重复报任务。
2. **每个 Issue 写清**：用户问题、范围/非范围、权威来源与链接、最小改动、复现命令、验收指标、阻塞条件、相关 PR。
3. **状态语义**：
   - Open：尚有可核实工作，或被硬件/授权/数据/时间阻塞；
   - Closed / completed：验收项有 PR/commit、CI 和需要的实际日志；纯文档/CPU 任务不升级真实模型实验状态；
   - Closed / not planned：已明确放弃且给出原因；重复 Issue 关联原任务；
   - 不能仅因文档存在、CI 绿色或 PR 已合并，就关闭需要 **真实 GPU/LLM/生产数据** 的 Issue。
4. 问题新增后优先做最小可复现样例与负例；学习计划不按周数自动完成。

## 3. Branch → PR → Main

- 默认分支是 `main`；使用短生命周期命名：`docs/...`、`feat/...`、`fix/...`、`test/...`、`audit/...`、`chore/...`。
- 一个可审查交付使用一个分支和一个 PR，PR 描述 **为什么、做了什么、证据、未验证什么、关联 Issue**。
- PR 至少核对：改动清单、相对链接、索引/模块一致性、单测/失败注入、官方来源版本、是否泄漏隐私/密钥/模型权重。
- `docs` 和 `cpu-toy` 工作流（若改动相关）必须 success；不能绕过失败只为显示已合并。涉及外部 GPU/LLM 的 PR 必须说明 **CI 未覆盖范围**。
- 优先 Squash merge；**合并后再次确认 main 上对应 push CI**。主分支与并行 PR 并发更新时先同步头部并重新验证，不能把旧 SHA 的成功挪用为新 SHA 成功。
- **分支删除门禁**：只有 PR 已 merged/原分支为 main 的祖先、无仍开放 PR 引用、非保护分支且没有未经审查的新 commit 时才删除；先保留 GitHub 上 PR、squash commit 与测试记录用于审计。删除前后的 branch 列表都应核对。
- 禁止用 `update_ref` force/reset 来冒充删除分支；删除须调用受权限限制的 GitHub API 并回读。仓库已有 [受审、SHA-pinned、只对 main 执行的清理工作流](LLM-Training/governance/README.md)，每个清理候选须对应已合并 PR 或 main 祖先，且实时检验无开放 PR、无 SHA 变更；权限不足必须停下并留下 Issue。

## 4. 资料与实验质量

- 资料优先 P0：作者论文原文/机构官方文档/官方源码；P1：作者官方课程；社区经验只能作为辅助发现。记录 URL、版本/commit、核查日期、失败替代路径。
- 运行证据：代码 SHA、模型和 tokenizer revision、数据许可证与 hash、train/dev/test 切分、硬件/驱动/包版本、Seed、命令、检查点及日志、独立测试、失败样例和对照；不得提交密钥、私有数据、模型二进制、未经许可全文。
- 教学范围：**SYNTHETIC** / **CPU TOY** / **DOCS ONLY** / **GPU NOT RUN** 必须区分，不能凭 toy 通关宣称实际生产 Agent、GRPO、RAG、vLLM 已验证。
- 若更改状态为 `PASS`，需符合 [实验模板](LLM-Training/experiments/EXPERIMENT-TEMPLATE.md) 和仓库现有状态 QA；不满足则保持 `NOT RUN` 或 `INCONCLUSIVE`。

## 5. 日常维护频率建议

- 每次 PR 合并：核对 main CI、关闭**确实完成**的关联 Issue、清理符合门禁的 head branch。
- 每周：复核 open Issue 的进展/阻塞，必要时精简重复任务；检查源码 API 变化对课程操作手册的影响。
- 每月：抽查权威来源可访问性、依赖/模型版本、学习实验的有效性；若外部接口变化，创建单独 Issue 和最小兼容复现。
- 不强制将未计划执行的 GPU 实验写成“逾期”；明确资源和实际优先级即可。

## 治理记录

首次专项基线：[仓库治理清单](LLM-Training/MAINTENANCE-BACKLOG.md)。本规范本身通过文档 CI 不等于清理远程分支或完成真实训练。
