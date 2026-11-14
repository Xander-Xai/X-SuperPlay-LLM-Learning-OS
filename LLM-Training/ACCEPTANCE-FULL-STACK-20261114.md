# 2026-11-14 大模型全栈知识打通：验收范围与证据边界

> 本轮对标用户要求：**上游其他大模型知识不能丢；训练/模型/应用/工程/运维之间关系必须清楚；有专业定义也有大白话；能按当前需求跳到权威原始材料与最小实验；课程不用按月份线性通关。** 这是学习资产整合验收，不是个人学习成绩或真实线上交付成绩。

## 已构建的导航产物（本轮文件与 CI 已合并；后续复验单独记录）

| 验收项 | 落盘文件 | 真实性限制 |
|---|---|---|
| 六域总图（Foundation/Sys/Post/ModelEng/App/LLMOps） | [全栈 Atlas](knowledge-graph/LLM-FULL-STACK-ATLAS.md) | 反映知识关系，不代表所有技术实践已执行 |
| 上游真实文件可追溯 | [23 条冻结上游路径](index/upstream-path-manifest.json) · [33 主题](index/upstream-knowledge-index.json) | 已用 GitHub 仓库树核对上游固定 SHA；不自动同步 |
| 原始专业参考 | [六域/主题/上游文件/官方课程链接](resources/UPSTREAM-RESOURCE-MAP.md) | 样本联网核查官方站点；非每一条外链 HTTP 通断与版本兼容审查 |
| “以点带面”按需学习 | [12 张跨域卡](demand-driven/AI-NATIVE-NEED-ROUTES.md) | 候选需求，不是用户真实客户记录 |
| AI 辅导和独立迁移 | [AI 原生学习闭环与可复用提示词](learning-method/AI-NATIVE-LEARNING-LOOP.md) | AI 解释不等于实际训练/掌握 |
| 与原 12 模块共存 | [Roadmap V3](ROADMAP-V3-DEMAND-DRIVEN.md) | M01–M12、4 里程碑、5 类训练实验与现有 18 需求路由保留 |
| 可机器检索与防错 | [CLI](tools/route_atlas.py)、[校验](tools/validate_atlas.py)、[测试](tools/test_atlas.py) | 离线字符串搜索，无完整语义搜索、无线下训练验证 |

## 验收必须包含

1. 读取主仓最新 main + 本 PR 基线 SHA，保证无未合并/覆盖上游变更。
2. 本轮引用的 23 个上游文件在固定 SHA 的 Git 树存在；每个主题指向上游文档、官方来源 ID 和本仓模块。
3. 本仓新的 Markdown 相对链接、JSON 主题 ID、关系边、需求卡引用可用且无 dangling path。
4. GitHub Actions 运行 **docs QA、旧 CPU Toy、索引 test_atlas.py 与 route_atlas smoke**；如有失败，修复后再合并。
5. 验证最终主仓 main 上 Roadmap/地图/资料库/CLI/验收报告存在。
6. 如同步上游首页，只做指针，不复制下游课程、不改写历史模块编号、不写未有证据的项目成果。

## 保留的限制

- 原有 MiniMind/Qwen 真实 CPT/SFT/DPO/GRPO GPU 训练与部署数据仍是 **NOT RUN**；本轮不改变。
- 课程路径和图并不能证明学习者达到 L3 或 L4；必须在陌生任务独立修改、排错和生产门禁上另验。
- 上游资料冻结为 2026-11-14 仓库快照；需要最新实现细节时要重新核对其 main / release / 官方版本。
- 不自动扫描/上传用户业务数据，所有需求案例必须说明是否为 synthetic/authorized/historical。
