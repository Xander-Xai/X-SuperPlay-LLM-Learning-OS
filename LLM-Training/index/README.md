# LLM-Learning-OS 专项仓索引

本目录同时提供**机器可检索入口**和**人类可读的知识与跨仓导航**：

- [learning-index.json](learning-index.json)：固定的 12 个模块 ID、前置依赖、18 种需求入口、5 条能力纵线、20 条权威来源及生产门禁映射。
- [上游/本仓关系与编号映射](UPSTREAM-DOWNSTREAM.md)：上游 Atlas、旧 M00–M17、模型源码仓、本专项学习仓、实际产品仓的事实边界。
- [总路线 V3](../ROADMAP-V3-DEMAND-DRIVEN.md)：使用方式、领域深度和生产能力，而不是僵化日历。
- [需求索引](../demand-driven/README.md)、[关系图](../knowledge-graph/dependency-and-capability-map.md)。
- [权威参考](../resources/AUTHORITATIVE-INDEX.md)、[生产验收](../production/PRODUCTION-READINESS.md)。

## 一条命令查阅

在根目录：

```bash
python LLM-Training/tools/route_learning.py --list
python LLM-Training/tools/route_learning.py --id tool-calling
python LLM-Training/tools/route_learning.py --search '延迟'
python LLM-Training/tools/validate_learning_index.py
python -m unittest discover -s LLM-Training/tools -p 'test_learning_index.py' -v
```

**不会**扫描私人 GitHub 项目、自动下载模型、读取本地数据或以 CI 成功判定学员能力。索引内容是人工审校的**导航目录**而非智能语义搜索/不断同步的数据库。

## 各索引字段含义

`modules[].prerequisites` 是理解一个概念的**推荐必要基础**；并不意味着所有任务必须从第一个模块学起。`demands[].modules` 为从当前问题进入的**建议排查路径**，该顺序与通用拓扑不同。每个 demand 保留 `DESIGN_ONLY` 状态，真实操作要有实验日志另建证据卡。

`sources[].url` 是来源入口；**这不证明每一版文档均适用于当前环境**。扩增来源时先核对公开可靠性、失效链接、许可证和版本。

索引验收在现有 docs CI 中运行，只验证结构、关联 ID、有效仓内路径与状态约束；不能证实外部 HTTP 可达、性能提升或上线成功。

