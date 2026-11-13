# M02：Tokenizer、Packing、数据质量与防污染

## 1. 原始数据真正怎样变成训练输入？

`source → 清洗/标准化 → 文档级去重 → 质量过滤 → 划分 split → Tokenizer → 加 special tokens → 分段/Packing → input_ids/attention_mask/labels`。顺序因数据集而异，但**测试集隔离必须早于任何基于测试结果的数据挑选**。

## 2. BPE 与特殊标记

- BPE 根据训练语料中的高频相邻 token/byte pair 合并子词；Tokenizer 的 vocab 与 merges 决定 token ID，不同模型不可任意共享。
- Byte-level BPE、Unigram 等只是不同分词方案。中文与代码需要分别检查每字符和每任务的 tokens/长度分布。
- `<tool_call>` 这类“显示在文本中的字符串”不一定是**单个 special token**。必须用实际模型 tokenizer 的 `tokenize`/`convert_tokens_to_ids` 和 `apply_chat_template` 验证。
- 如果确需扩词表，需检查 embedding/lm_head resize、权重 tying、保存、训练与部署协议；**优先用模型官方工具模板**。

## 3. Packing 和 Loss 不能只看长度

- **padding**：填充不应成为学习目标，labels 设 `-100`；推理/训练 attention mask 语义需区分。
- **packing**：合并多个短文档减少 padding，但跨文档 attention 是否允许、EOS 是否学习、是否使用 block-diagonal mask 依赖训练方案，不是总能自动隔离。
- **assistant-only SFT**：将 system/user/tool 位置设为 `-100`，只让 assistant 指定输出为目标。注意 labels mask 的位置与 logits 做 **shift-one** 后的对应关系。
- **truncation**：截断可把工具调用和其 observation 分开，也会消除完整 answer；验证被截掉的样本比例。

## 4. 数据质量检查

| 维度 | 记录 |
|---|---|
| 原始来源 | URL/授权/收集时间/许可证/敏感信息处理 |
| 清洗 | 文本长度、坏编码、HTML、重复、低质量过滤率 |
| 混合 | 领域/通用 token 比例、采样算法与随机种子 |
| 质量 | JSON parse rate、tool schema、引用有效性 |
| 污染 | 文档、模板、题目家族、近重复检测 |
| 预算 | token 总量、seq len、batch、packing 效率 |

## 5. 本地练习

使用 20 条虚构中文产品语料：
1. 统计分词前后长度，保存 tokenizer revision 和比例。
2. 用文档 ID 而非随机 chunk 拆分 train/val/test；断言不重叠。
3. 创建两段短文本进行 packing；明确是否跨文档关注、边界 token 和 loss mask。
4. 验证工具 observation 被排除在目标之外（参见 [教学测试](../labs/README.md)）。

**验收**：可解释至少三种数据泄漏、一次 packing 边界错误和 token 数为何影响预训练成本。更深入的合成数据见 [Synthetic/RFT](synthetic-data-and-rejection-sampling.md)。

