# Agent 五项实验 SOP｜三阶段项目的实际证据

> 合成演示 A 已接入 CI；B–E 为**操作指导**，未实际运行真实框架、数据库、MCP 或模型。在取得完整日志和评估前不可声明生产能力已验证。

## 实验 A：无框架 Agent Loop 与可选真实工具协议

~~~bash
python LLM-Training/application-engineering/labs/mini_agent_loop.py
python -m unittest discover -s LLM-Training/application-engineering/labs -p 'test_mini_agent_loop.py' -v
python -m unittest discover -s LLM-Training/application-engineering/labs -p 'test_real_llm_optional.py' -v
~~~

- 观察合成脚本如何从 Tool Call 进入 Gateway，执行并回填 Observation。覆盖 UNKNOWN_TOOL、INVALID_ARGS、APPROVAL_REQUIRED、FORBIDDEN_TENANT、STEP_LIMIT、IDEMPOTENCY_CONFLICT。
- 真实 API 的 **Chat Completions Tool Call ID / Tool Message** 可用 [可选真实模型实践](../labs/REAL-LLM-OPTIONAL.md) 对照，默认只跑 Fake Client；联网必须显式 --live、配置 Token 和模型、限预算。工具数据仍全是虚构订单。
- L2 需要学习者自己修改一种异常、重跑测试，解释每条消息的来源；仓库 CI 不能替代个人闭卷评估。

## 实验 B：LangGraph 状态机与审批恢复

- 使用真实 LangGraph 版本，创建 StateGraph，节点 verify_actor → route → lookup_order → approval_interrupt → refund_once → verify_business_state → final。
- 明确 State 的可变字段、Reducer、Thread ID、Checkpointer、Store 和业务 DB 的分工；在 interrupt 前后保存 checkpoint/Thread/DB 状态，使用 Command resume。
- 注入撤销审批、相同 Thread 重放、错误 Thread、两并行节点写冲突、退款成功后响应丢失。
- **预期**：未经授权禁止退款；重复请求不重复业务副作用；恢复前后状态可解释。只有真实运行日志、安装版本和业务 DB 状态才能标 L2+。

## 实验 C：Workflow vs 单 Agent vs 多 Agent

用至少 20 条**合成或授权**冻结测试用例，覆盖订单查询、拒答、退款审批、跨租户、失败重试。固定模型、数据、Prompt、工具权限、预算和评分器；比较固定 Workflow、一个 Agent、Router+专业 Agent（必要时 Supervisor）。记录 Task Success、Correct Abstention、Tool Accuracy、Handoff、Token/成本、P95 和越权数。注入 Handoff 循环、共享 State 竞争、跨用户记忆污染。

## 实验 D：生产工程和故障注入

| 操作 | 失败模式 | 必须核验 |
|---|---|---|
| SSE 断连 | 客户端取消连接 | run_id 可重查，后台状态不靠 SSE 推断 |
| Worker 宕机 | 写前/写后/回执前中断 | Checkpoint 与 DB 事实一致 |
| 幂等测试 | 同键同 Payload / 同键不同 Payload | 唯一约束、副作用次数 |
| 并发 | 多 Worker 同业务操作 | 没有重复退款 |
| ACL | 伪造身份/越权订单 | 服务端拒绝，有脱敏审计 |
| 监控 | 模型超时、Tool 429/500 | Trace、P95、失败分桶与费用 |

推荐独立项目使用 FastAPI、Celery/Redis、PostgreSQL、Docker；没有真实事务和故障日志时不得宣称 exactly-once。

## 实验 E：MCP/Skills 与长任务 Harness

在独立测试环境创建只读 MCP Server，观察 Host/Client/Server 工具发现与调用。使用仅含参考资料的 Skill 学习 SKILL.md 资源加载；确认载入不等于获得执行权限。长任务 Research/Coding Harness 需计划、进度、持久记录、恢复、实际文件/测试验证。A2A 选学，不强制接入分布式 Agent。攻击负例：恶意网页或 Tool Output 要求读取越权文件、重复任务、无限工具调用。

## 三个项目的最终交付

| 项目 | 训练阶段 | 退出材料 |
|---|---|---|
| Mini Agent | A | 一张架构图、合成 Tool Trace、实际代码和异常测试；可选真实 LLM |
| Customer Service Agent 2.0 | B/C/D | 订单/知识/退款三链、审批恢复、数据库一致性、基线与评测报告 |
| Mini Coding/Research Harness | E | 多阶段任务、可恢复进度和真实验证结果 |

最终证据卡：Task ID、数据是否合成、模型/SDK/工具版本、命令、输入输出、失败注入、真实 DB 终态、指标的分子分母、代码 SHA、测试负责人、L0–L4 结论和生产门禁。详见既有 [项目/评测协议](../AGENT-PRACTICE-AND-EVAL.md)。
