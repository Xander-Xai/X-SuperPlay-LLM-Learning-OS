# Agent / RAG 工具调用 SFT：多轮轨迹与 Loss Mask（P0）

## 1. 场景

一个企业知识查询 Agent：用户问产品库存及文档依据；模型需生成工具调用，读取工具的 observation，最后生成带可核验引用的答案。训练环境使用**模拟库存 API 和可审计知识库**。

## 2. 消息序列与标签策略

| 角色/回合 | 示例 | assistant-only Loss |
|---|---|---|
| system | 工具说明/约束 | 不算 |
| user | 查询产品 A | 不算 |
| assistant(tool_call) | 调用 query_inventory 和 search_docs | **算** |
| tool(observation) | 库存与文档片段 | 不算 |
| assistant(final) | 依据工具结果作答并引用 | **算** |

**关键原则**：使用模型官方 chat template 和 assistant mask 机制，而不是靠字符串搜索粗暴遮蔽；不同模型 template/TRL 版本对 generation markers、工具消息的支持不同，必须检查实际渲染 token 与标签。

## 3. 最小测试用例

构造 system + user + assistant(tool_call) + tool + assistant(final)：
1. 使用 tokenizer.apply_chat_template 或框架的正确接口序列化，打印 Token IDs、role 范围、是否存在 generation marker。
2. 将非 assistant 范围 labels 置为 -100；assistant 两段目标保留。不要假设工具输出也需要预测。
3. 断言所有 tool observation / user / system token 对应 labels == -100；两段 assistant 的非 padding token 至少部分 != -100。
4. 如果启用 packed sequences 或不同 template，再重复断言，特别关注 EOS、工具调用结束标记、截断边界和 token 对齐。
5. 训练后再用工具调用解析与执行成功率评估，而不仅看 training loss。

### 伪代码（不是可直接运行的 TRL 脚本）

~~~python
labels = input_ids.clone()
labels[~assistant_target_mask] = -100
labels[padding_mask] = -100
assert (labels[tool_observation_mask] == -100).all()
assert (labels[assistant_tool_call_mask] != -100).any()
assert (labels[assistant_final_mask] != -100).any()
~~~

提示：Causal LM 的 shift 通常在模型 loss 内部实现，务必核对当前框架，避免双重 shift。

## 4. Special Tokens

优先复用 Qwen 官方 [Tool Calling Template](https://qwen.readthedocs.io/en/latest/framework/function_call.html) 的工具调用序列化与边界标记。文本中显示的某些标签未必是**单个** special token。只有确实有需求并验证其不存在词表时，才考虑 tokenizer.add_special_tokens + resize_token_embeddings；检查初始化、是否冻结 embed_tokens/lm_head、权重 tying 与保存加载兼容。

## 5. 实验

- Baseline 直接推理 vs Tool SFT 后推理（相同工具、相同测试任务）。
- 按 schema-valid、tool-selection、argument-match、execution-success、citation-correctness、end-to-end-success 评分。
- 数据工程见 [合成数据与 RFT](../data-engineering/synthetic-data-and-rejection-sampling.md)，实验执行见 [03 Agent Tool SFT](../experiments/03-agent-tool-sft/README.md)。

