# Context Engineering｜组装、压缩与保护每一次模型调用的上下文

**专业**：在每轮推理前，将 system/developer 指令、任务目标、历史消息、记忆、检索文档、工具状态与输出契约，在有限 Token 与权限预算下进行**有来源、可验证的选择和组装**。它是动态运行时操作，不等于把 Prompt 写长。

**大白话**：Prompt 是开会的议程，Context 是每次会议桌上**究竟摆哪几份材料**、哪些是机密、哪份过时、哪些要收走。把桌子加大不代表员工就能找对页。

## 1. 五个层次

1. **输入完整性/优先级**：指令权威层级 > 低信任文件/工具输出；来源于 RAG 的内容作为**引用数据**，不是新的高权限命令。
2. **检索/选择**：需要证据先处理身份与检索过滤，按相关性、来源、时效选最少有用内容。
3. **预算与压缩**：为指令、证据、历史、工具 schema、输出空间设预算；对长历史做 Summarize/Trim/Memory；不能默默丢弃尚未完成的承诺、待审批事务或权限/源 ID。
4. **状态和记忆**：Thread-level checkpoint 保存当前执行状态；跨会话长期记忆要有用户授权、更新/过期策略与删除/更正路径；RAG 知识库并不自动等于用户记忆。
5. **质量与安全**：Context precision、关键证据保留率、Token 数/成本、误引入高权限指令、跨租户泄露率、可重放性；必须测试有效性而不仅仅测试窗口没溢出。

## 2. 专业与白话对应

| 方法 | 技术作用 | 代价/失败风险 | 最小实验 |
|---|---|---|---|
| Context Packing | 在输入 Token Budget 内选择材料 | 排序错误丢最关键证据 | 固定 Token 预算，比按相关性与“全文塞入” |
| Query-aware Retrieval | 用问题选择证据，不是把所有资料塞进 Prompt | 检索失败使上下文再好也错 | 加一条语义改写、别名负例 |
| History Summarization | 历史压缩成任务状态 | 遗漏约束、错误转述，信息不可逆 | 长对话重放，核对未完成事项 |
| External Memory | 用独立存储的事实/状态按需检索 | 陈旧、误归属、隐私保留 | 更正用户偏好/撤销授权案例 |
| Tool Output Trimming | 清理冗长日志、只留证据/结果 | 丢失关键报错/引用 ID | 保留 error code、trace ID、source ID |
| Context Isolation | 跨用户/角色/租户隔离数据 | Prompt Injection 或越权读 | 低权限用户查询带高权限诱饵文档 |

## 3. 三种容易误判的情况

- **Context 长 ≠质量高**：模型可能遗漏中段关键事实，重召回或显式约束比扩大窗口更有效。
- **“引用了材料” ≠“指令安全”**：外部文档可写恶意指令；分隔低信任内容有帮助，但**服务端的权限、工具执行隔离不可省**。
- **Summary ≠原始持久状态**：用于说明上下文的摘要不能可靠代替事务流水、工具结果凭证或审批记录。

## 4. 可执行练习与退出门槛

从 [离线应用纵切 Lab](labs/README.md) 使用 100/40/20 单位的**近似词预算**（不是模型 Tokenizer 实测），观察相关证据是否被选择、隐藏文档是否被过滤、预算不足时失败行为是否显式。随后换真实 Tokenizer 和可审计历史记录，再测压缩前后质量与源定位。

完成 L2 需交 **输入上下文 Manifest、Token/来源/权限占比、相同固定问题集质量和成本对照、至少两条低权限/过时材料负例**。是否真正改善由独立任务指标判断。

**官方资料**：[Anthropic Effective Context Engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) · [Anthropic Memory vs Compaction](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools) · [LangChain Context Engineering](https://docs.langchain.com/oss/python/learn) · [上游专项](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/market/context-engineering-demand-to-lab-20261029.md)。

**预算验收澄清**：本仓离线 Lab 中的 budget 只对 **Retrieved Evidence** 使用空白分隔代理单位，不包含指令、工具描述、消息历史和生成输出预留空间。真实模型端的完整 Context Budget 需要**目标模型的 Tokenizer**计算，并为输入/输出留冗余；不能将代理单位误记为 Token 数或显存实测。
