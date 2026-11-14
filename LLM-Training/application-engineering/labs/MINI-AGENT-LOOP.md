# Mini Agent Loop｜可运行的无框架学习实验

> 状态：SYNTHETIC_CPU / SCRIPTED_MODEL / NO_REAL_LLM / NO_NETWORK / NO_DB。Python 3.11 标准库、内存订单与固定模型决策；**不是 OpenAI/Anthropic/LangGraph SDK 的真实 Tool Calling 消息格式**。本实验是理解「模型提议 → 服务端校验 → 工具执行 → 观察回填 → 下一轮/停止」的最小教学切片。

## 从仓库根目录运行

~~~bash
python LLM-Training/application-engineering/labs/mini_agent_loop.py
python -m unittest discover -s LLM-Training/application-engineering/labs -p 'test_mini_agent_loop.py' -v
~~~

## 对照源码解释每一步

1. **ScriptedModel.decide**：返回预写的 ToolCall 或 Final；不代表语言模型有规划能力。
2. **run_agent**：限制模型决策次数、将工具结果加入教学用 history、记录 Trace、遇到异常立即给结构化失败，不允许后续伪造成功。
3. **ToolGateway.execute**：只允许 lookup_order/refund_order；查租户、参数、服务端可退款角色、审批。退款需要幂等键；同一可信 actor+tenant+key 同请求复用结果，不同请求冲突。
4. **Trace**：记录每步工具结果/失败，业务存储也可观察。教学 Trace 没有网络延迟、Token 或实际模型消耗。
5. **实际 SDK 迁移**：真实 Provider 有自己的 Tool Call ID 与消息协议；需按官方文档把 Assistant Tool Call 和匹配的 Tool Result 正确回传，不能直接复制本例的 history 字段当 API payload。

## 手动学习任务

- 把 max_steps 改为 1，观察两次工具调用导致 step_limit。
- 修改 lookup_order 的参数为数字、未知 ID、其他租户 ID，逐项归类失败。
- 先未审批尝试 refund，再使用可信 caller 提供的 approved order 重跑，比较业务状态。
- 使用同一幂等 key 重放；再绑定不同订单，确认不会复用错误的收据。
- 增加查询失败重试策略时，要区分只读和不可逆写操作；不要为学习方便直接重试退款。

## 能力证据 vs 不可声称的内容

| 可以由离线测试验证 | 不能由本实验证明 |
|---|---|
| 循环、步骤限制、工具 allowlist、参数类型检查 | 真实 LLM 的规划、生成和 Tool Call 格式 |
| 合成 Tenant/Actor 的权限逻辑 | 真实身份认证、跨服务权限隔离 |
| 内存版审批、幂等记录和副作用计数 | 数据库原子性、并发安全、网络重试或生产事务 |
| 确定性错误 Trace 和结果结构 | 实际 Trace 平台、线上性能、Token 成本、安全防御能力 |

在独立项目接入真实 API 后，记录准确模型版本、工具定义、请求/响应、预算与身份来源，并按 [Agent 主线](../AGENT-LEARNING-PATH.md) 和 [项目验收](../AGENT-PRACTICE-AND-EVAL.md) 重做负例。
