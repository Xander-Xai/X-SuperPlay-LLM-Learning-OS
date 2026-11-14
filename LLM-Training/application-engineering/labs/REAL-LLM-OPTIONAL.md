# 可选：真实模型 API 的 Tool Calling 教学路径

> **状态：FAKE_CLIENT_TESTED / LIVE_NOT_RUN。** 默认不联网、不安装第三方包、不读取 Key、不产生费用；使用 Chat Completions 的 function tools 协议，而非 Responses API 的 function_call_output 格式。实际 API 必须符合供应商支持的模型、参数、Python SDK 版本与账户预算。

## 零费用跑协议单元测试

~~~bash
python LLM-Training/application-engineering/labs/real_llm_optional.py
python -m unittest discover -s LLM-Training/application-engineering/labs -p 'test_real_llm_optional.py' -v
~~~

FakeClient 让你检查 Assistant Tool Call 的 id/name/arguments、匹配的 Tool Result、模型继续运行，以及未知工具、非法 JSON、跨租户、无审批和超预算终止。它不等于真实模型测试。

## 自愿实际 API 测试（有真实调用成本）

**前置**：在独立授权环境安装当前官方 openai Python SDK，并设置本地环境变量 OPENAI_API_KEY。绝不能写入仓库或将密钥打印到日志。需要主动指定目标模型、可用额度与 SDK 版本。

~~~bash
# 仅在确认模型支持 Chat Completions/Function Calling 时使用
python LLM-Training/application-engineering/labs/real_llm_optional.py --live --model YOUR_SUPPORTED_MODEL --max-turns 3 --max-seconds 45
~~~

- 脚本只使用虚构订单 o-1/o-2；Gateway 的 can_refund 永久 False，不会对任何真实财务系统产生写操作。
- 已添加 max_turns、max_tool_calls、单次输出 Token 上限、wall-clock 预算；客户端设置超时并禁用自动重试。但网络请求超过总限时、供应商服务异常与实际计费仍可能发生；**没有提供硬费用上限**，请在服务商控制台设置预算。
- 返回 completed 只意味着模型正常结束，**不意味着真实退款、真实模型质量、生产鉴权或业务结果正确**。需要人工阅读结果与工具返回，另外评估工具准确率。
- 如果模型使用 Responses API，其输出是 function_call / function_call_output，并应依据官方 [Function Calling 指南](https://developers.openai.com/api/docs/guides/function-calling) 重写适配器；不可直接使用此 Chat Completions 格式。
- 测试要求保存 python、openai SDK 版本、model ID、测试用例、脱敏 Trace、模型费用和代码 SHA；无这些证据不能把 LIVE_NOT_RUN 标为已完成。
