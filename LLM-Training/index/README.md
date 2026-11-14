# LLM-Learning-OS 专项仓索引

**上游全栈 Atlas 扩展（2026-11-14）**：

- [33 主题/6 域/30 类型关系/12 需求机器目录](upstream-knowledge-index.json) · [已对 Git 树核对的 23 个上游路径清单](upstream-path-manifest.json)。
- [完整训练/推理/应用关系图](../knowledge-graph/LLM-FULL-STACK-ATLAS.md) · [上游/官方逐项链接](../resources/UPSTREAM-RESOURCE-MAP.md) · [按需学任务卡](../demand-driven/AI-NATIVE-NEED-ROUTES.md)。
- [命令行 Atlas 检索](../tools/route_atlas.py)：--search RAG、--topic A04、--need N02、--domain A。原有 route_learning.py 继续提供 M01–M12 的模块级路由。

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
python LLM-Training/tools/route_learning.py --search 'QLoRA'
python LLM-Training/tools/route_learning.py --search '工具调用'
python LLM-Training/tools/route_learning.py --module M11
python LLM-Training/tools/validate_learning_index.py
python -m unittest discover -s LLM-Training/tools -p 'test_learning_index.py' -v
```

**不会**扫描私人 GitHub 项目、自动下载模型、读取本地数据或以 CI 成功判定学员能力。索引内容是人工审校的**导航目录**而非智能语义搜索/不断同步的数据库。

## 课程内可直接运行的验证

- [DPO/GRPO 公式与奖励漏洞](../labs/preference-rl-math/README.md)
- [Agent 任务级指标与 Wilson 区间](../labs/task-evaluation/README.md)
- [合成工具执行安全边界](../labs/synthetic-tool-gateway/README.md)
- [严格验收报告](../ACCEPTANCE-V3-AUDIT.md)

## 各索引字段含义

`modules[].prerequisites` 是理解一个概念的**推荐必要基础**；并不意味着所有任务必须从第一个模块学起。`demands[].modules` 为从当前问题进入的**建议排查路径**，该顺序与通用拓扑不同。每个 demand 保留 `DESIGN_ONLY` 状态，真实操作要有实验日志另建证据卡。

`sources[].url` 是来源入口；**这不证明每一版文档均适用于当前环境**。扩增来源时先核对公开可靠性、失效链接、许可证和版本。

模块级 `sources` 指向权威来源 ID，`practice` 指向实际起步练习，`question` 指当前需求触发点，`gates` 指生产阶段需要的门禁。需求级 `aliases` 使常见中文/英文关键词可查；`--module` 可反向查哪些工程问题会用到某模块。**所有需求记录仍为 DESIGN_ONLY**。

索引验收在现有 docs CI 中运行，只验证结构、关联 ID、有效仓内路径与状态约束；不能证实外部 HTTP 可达、性能提升或上线成功。


## 关系查询（新增）

~~~bash
# Tool Calling / MCP 与其他主题的全部已编目入边和出边
python LLM-Training/tools/route_atlas.py --relate A04

# Tool Calling 与 Observability 之间的关系探索路径
python LLM-Training/tools/route_atlas.py --path A04 O02
~~~

关系查询基于静态 JSON 的 30 条边。**--path 使用无向连通性寻找最短探索路径，但每条边保留原存储方向**；并不是自动学习计划、因果证明或全行业知识搜索。遗漏的边不应被编造。参考 [全景 Atlas](../knowledge-graph/LLM-FULL-STACK-ATLAS.md) 与 [官方实现复验](../resources/OFFICIAL-RUNTIME-DELTA-20261114.md)。

## 全栈 Atlas 离线验收命令

~~~bash
python LLM-Training/tools/route_atlas.py --need N02
python LLM-Training/tools/route_atlas.py --topic A04
python LLM-Training/tools/route_atlas.py --domain E
python LLM-Training/tools/route_atlas.py --search RAG
python LLM-Training/tools/validate_atlas.py
python -m unittest discover -s LLM-Training/tools -p 'test_atlas.py' -v
~~~

Atlas 的上游路径已在固定 SHA 的 Git 树验证；测试不会在线校验每个第三方 URL，也不会自动更新来源或替代自己做实验。
