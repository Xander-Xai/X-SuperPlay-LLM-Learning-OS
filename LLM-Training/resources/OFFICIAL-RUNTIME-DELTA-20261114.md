# 2026-11-14 官方实现变化补丁｜SFT/Tool GRPO/vLLM/MCP

> 用途：从 [六域知识图](../knowledge-graph/LLM-FULL-STACK-ATLAS.md) 按需进入最容易踩坑的版本与系统信任边界。本页是近期官方资料核查与学习操作卡；不是本机兼容性测试、真实训练结果或线上安全认证。官方网页只抽查了所列重要入口，并非全仓外链巡检。

## 1. Tool SFT 不能只设置 assistant_only_loss=True

**专业原理**：[TRL SFTTrainer](https://huggingface.co/docs/trl/sft_trainer) 的 assistant-only 训练要依靠模板中 Jinja 的 generation/endgeneration 区间生成正确 Loss Mask。[TRL Chat Templates](https://huggingface.co/docs/trl/chat_templates) 包含对部分 Qwen3 模板的自动补丁，但不能推出任意自定义模板、历史版本都准确。

**大白话**：老师批改作业时要明确划出“学生写的答案才计分”的红框；配置勾选“只批学生答案”不代表真的圈对每一个字。工具返回是外部环境的事实，不应该被误当成 Assistant 生成目标。

**立即应做的可执行任务（需实际安装真实版本；尚未跑过标 NOT RUN）**：

1. 保存 Transformers、TRL、Tokenizer、Chat Template 的真实版本或 hash，以及一条脱敏结构化样本。
2. 将 system → user → assistant tool call → tool observation → assistant final 渲染成 Token IDs，导出 assistant generation mask 和 labels（忽略位置通常为 -100）。
3. 逐 Token 检查 system/user/tool observation 不计算 Assistant Loss，而所监督的 assistant tool call/final answer 保留；对于 thinking 内容与结束标记按实际任务明确训练目标。
4. 故意修改模板或删除 generation 区间，验证测试是否能识别异常。只检查监督 Token 数量大于 0 远远不够。

**来源**：[TRL SFT](https://huggingface.co/docs/trl/sft_trainer) · [TRL Chat Templates](https://huggingface.co/docs/trl/chat_templates) · [Qwen Function Calling](https://qwen.readthedocs.io/en/latest/framework/function_call.html)。关联 [M06](../modules/M06.md) / [M02](../modules/M02.md)。

## 2. 工具型 GRPO 还要检查“前缀不变”

**专业原理**：TRL 官方的 [Chat Templates](https://huggingface.co/docs/trl/chat_templates) 明确提出，GRPO 与工具调用组合时，向现有对话追加 Tool Message 不应修改已存在消息的 Token/文本序列化前缀（prefix-preserving）。否则 Rollout 生成时前缀与训练计算 log-prob 时前缀可能不一致。

**大白话**：现场会议录音与事后纪要，之前已经说过的话不能因为后来拿到工具反馈就被重新改写，否则你就不知道模型当时看到了什么。

**验收方法**：在实际安装的 Qwen/TRL 上，分别用 Rollout 相同的模板选项渲染原历史消息，以及追加 Tool Observation 的历史消息，核对原有前缀 Token 是否保持不变。注意 add_generation_prompt 与 Assistant 起始标记会改变比较边界，需与实际训练代码对齐；自定义模板应有一个故意违背前缀不变的失败负例。

[TRL GRPOTrainer](https://huggingface.co/docs/trl/grpo_trainer) 还定义 vLLM colocate/server 模式，以及生成与训练框架分布不一致时的 Importance Sampling 修正配置。GRPO 的 Loss、KL、组大小、截断和显存默认值都依赖版本，不可将旧教程写成普遍结论。对于单卡先从 TRL、LoRA、短序列、低并发起步；是否能在 16GB 上运行要实测。

**严格验收**：真实模型/Tokenizer 版本、前缀测试日志、奖励验证器、独立任务正确率、截断率、OOM/吞吐记录。此前的数学 Toy 不构成真实 GRPO 训练通过。

## 3. vLLM API Key 不等于全站安全

**专业原理**：[vLLM 官方 OpenAI-Compatible Server](https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/) 明确指出，服务的 API Key 认证只保护特定路径前缀（如 /v1、/v2、/inference、/cohere），而其他端点可能不受此机制保护；官方特别提及 /invocations。因此不应仅设置服务参数就将 HTTP 端点暴露至公共网络。

**大白话**：给正门安装门禁不等于整栋楼都上锁；侧门也需要统一控制。

**实际安全验收（只在拥有授权的测试环境操作）**：

- 将 vLLM 放在受限网络与反向代理/网关后，配置全路径统一鉴权、租户隔离、访问速率/大小限制；未知路径默认拒绝。
- 在自己的测试环境分别检查常规 /v1 和 /invocations 等不应公开的路径，匿名/未授权访问必须被拒绝或不被路由，不能只测正门。
- 固定服务版本、反代配置、端点清单，保存匿名负例、密钥撤销、回滚和日志证据。
- 还要核验 TLS、部署隔离、工具执行端权限；模型自身的“拒绝访问”不等于服务端安全。

关联 [M11](../modules/M11.md)、[G3/G5/G7 上线门禁](../production/PRODUCTION-READINESS.md)。**未实际部署就标 NOT RUN**。

## 4. MCP 更新不等于 Agent 自动授权

**专业原理**：[MCP 2026-07-28 规范](https://modelcontextprotocol.io/specification/2026-07-28) 和 [官方发布说明](https://blog.modelcontextprotocol.io/posts/2026-07-28/) 引入 stateless protocol core、header routing、缓存工具列表及扩展体系，旧的握手/会话机制有重要变更。不同版本客户端和服务端仍可能支持历史协议，不能把最新规范当成当前部署已实现能力。

**大白话**：换成统一规格的插座不会让工具自动获得安全授权或业务判断能力。

**最小任务**：记录 Client/Server SDK 与协议修订版本，确认实际采用的握手或 stateless 交互方式；再测 tools/list、tools/call 的 schema、身份和权限；添加越权、超时和不可用负例，并对副作用操作要求审批或幂等策略。

## 5. 按故障选最短学习路径

| 症状 | 先学什么 | 不应该马上做什么 | 留下什么证据 |
|---|---|---|---|
| Tool SFT 模型复述工具结果 | M06 Template/Mask | 直接增加 LoRA Rank/训练轮次 | Token-level labels/mask 与失败单测 |
| GRPO Tool Trajectory 分数异常 | M08 Prefix Preservation、采样校正 | 直接换大模型 | 原始前缀对照与固定配置 |
| vLLM 配了 API Key 却担心越权 | M11 全路径鉴权 | 直接公开所有服务端点 | 自有测试环境的匿名负例/网关规则 |
| MCP 客户端与服务端不兼容 | A04 协议修订/身份/授权 | 将 Tool Calling 与 MCP 混作一层 | SDK 版本、请求链路与脱敏日志 |

## 6. 来源与边界

上述官方页面在 2026-11-14 进行了针对性浏览；动态 latest 页面可能变化，运行时仍须确认具体版本和 Commit。没有本轮真实模型训练、GPU 显存测试、生产服务或客户数据，不声称上述工程验收已经通过。
