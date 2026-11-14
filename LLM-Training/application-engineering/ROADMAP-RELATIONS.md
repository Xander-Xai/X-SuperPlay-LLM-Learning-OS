# 应用工程依赖关系与非线性学习地图

这不是 M01→M12 的机械课程重排。关系边采用 **PROVIDES_CONTEXT / EXECUTES / EVALUATES / IMPLEMENTS / REQUIRES_SECURITY / OPTIMIZES**，并区分技术依赖与学习探索路径。

## 专业关系

~~~mermaid
flowchart LR
  M["Base / SFT / RL 模型（M04/M06/M08）"] -->|"PROVIDES_CAPABILITY"| A["Agent / 文本生成"]
  P["Prompt Engineering"] -->|"SHAPES_INSTRUCTIONS"| C["Context Engineering"]
  R["RAG（Retriever/Reranker/ACL）"] -->|"PROVIDES_CONTEXT"| C
  MEM["Memory/State + Tool Observations"] -->|"PROVIDES_CONTEXT"| C
  C -->|"PACKS_TOKENS"| A
  H["Harness / Runtime"] -->|"EXECUTES_AND_CONTROLS"| A
  H -->|"REQUIRES_SECURITY"| ACL["Server ACL / HITL / Sandbox"]
  A -->|"PROPOSES_ACTION"| H
  E["Evals / Ragas / Trace"] -->|"EVALUATES"| A
  E -->|"EVALUATES"| R
  E -->|"EVALUATES"| H
  PROD["Project/Production"] -->|"VALIDATES_RELEASE"| H
  PROD -->|"VALIDATES_RELEASE"| E
~~~

大白话：模型是工人；Prompt 是任务说明；Context 是当前桌面的资料；RAG 是借书室；Agent 是做出下一步动作的人；Harness 是流水线、工具和门禁；Ragas 是考试评分工具；生产工程是可长期运营的产品与责任体系。

## 八种常见混淆

1. **RAG≠CPT**：RAG 通常在推理时查资料，CPT 改变模型参数。先测检索/数据库/规则足不足。
2. **RAG≠Ragas**：RAG 是检索增强生成系统；Ragas 是评价系统/工具库，不会自动使模型变强。
3. **Harness≠Agent 模型**：Harness 运行/恢复/限制 Agent；它可以运行规则程序或外部 API 模型。
4. **Agent Harness≠lm-evaluation-harness**：后者是 EleutherAI 的基准评测工具，不是运行带工具的 Agent。
5. **Prompt≠Context**：Prompt 指令是 Context 的部分；Context 还可能包含检索、工具结果、记忆和系统状态。
6. **Context Window≠有效知识**：窗口再长也可能被污染、截断或丢失关键信号；要测资料保留和答案质量。
7. **MCP≠授权协议的全部**：MCP 连接/描述工具；真正 IAM、租户隔离、审批、幂等必须在服务端执行。
8. **Prompt Injection≠普通提问**：外部资料与工具返回是低信任内容；不能因其中出现“系统指令”文字就给它更高优先级。

## 与 M01–M12 的反查映射

| 应用技能 | 要补的训练/模型基础 | 不必预先做 |
|---|---|---|
| Prompt/Structured Outputs | M02 Tokenizer+Chat Template、M06 SFT Mask、M10 评测 | 从零预训练 |
| Context/RAG | M02 上下文长度与分割、M03 Attention、M10 任务评测、M11 KV | DPO、GRPO |
| Agent/Harness | M06 Tool SFT 可选、M08 Agentic RL 可选、M09 状态与成本、M10 评测、M11 运行时 | 必须先多智能体训练 |
| Ragas/Trace | M10 评测统计、M11 延迟/吞吐、数据许可与标注 | 先训 14B |
| Project/Production | M09 资源、M10 评估、M11 推理服务与 [G0–G8](../production/PRODUCTION-READINESS.md) | 生产数据放进学习仓 |

## 判定一个需求属于哪层

真实问题 → 定义指标和免训练 Baseline → 检查 **Retrieval / Prompt / Context / Tool Contract / Harness / Model** 哪层错误 → 做一个最小可控更改 → 用固定 Eval Set 比较 → 失败回退/满足后停止。任何“训练更大模型才能解决”都应先有对照证据。

[应用工程总索引](README.md) · [六域全栈 Atlas](../knowledge-graph/LLM-FULL-STACK-ATLAS.md) · [实验目录](labs/README.md)。
