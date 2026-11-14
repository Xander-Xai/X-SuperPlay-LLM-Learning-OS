# 基础缺口 D0｜Tokenizer、特殊标记、数据与切分边界

> 对应 [M02](../modules/M02.md) 和 [M06 Tool SFT](../modules/M06.md)。解决“数据准备好了为什么模型还是乱学/乱码？”的问题，不要求先从头学 NLP。来源：[HF Tokenizers](https://huggingface.co/docs/tokenizers/index) · [LLM Course 6](https://huggingface.co/learn/llm-course/en/chapter6/1) · [Dataset Cards](https://huggingface.co/docs/hub/en/datasets-cards) · [TRL SFT](https://huggingface.co/docs/trl/sft_trainer) · [DataComp-LM](https://github.com/mlfoundations/dclm)。

## 1. 字符、Byte、Token、ID、Embedding

一种常见过程是“UTF-8 原始文本→Normalizer→Pre-tokenizer→Subword Model→PostProcessor/Special Tokens→ID 序列→Embedding”。具体配置取决于模型，不是所有 Tokenizer 都采用完全相同的实现。

- **专业**：Token 是词表符号，Token ID 是整数索引，Embedding 将其映射到向量；词表、特殊标记、Chat Template 必须与目标模型版本匹配。
- **白话**：把句子先切成拼图块，再给每块一个货号；机器先处理号码，向量化后才进入 Transformer。
- **负例**：中文一个汉字不一定是一个 Token，特殊标记可能有独立 ID，不能随便拿另一个模型的词表替换。

## 2. 四种 Tokenizer 的核心差别

| 技术 | 专业定义 | 大白话 | 最小实践 |
|---|---|---|---|
| Character/Byte | 字符或 UTF-8 Byte 为基础离散单元；Byte 可覆盖更多字符但序列可能长 | 每字/字节当积木 | 对比中英文 UTF-8 byte、字符、Token 数 |
| BPE | 通过训练逐步合并常见相邻子词形成词表，可从字节或字符起步 | 经常一起出现的积木粘成新积木 | 模拟两轮合并，比较词表规模 |
| WordPiece | 一类基于子词词表匹配和训练打分准则的分词，常用于 BERT 家族 | 用可用零件拼出词 | 比较长词拆分与未知词行为 |
| Unigram | 从候选子词中选择高概率分段，训练时调整和剪枝词表 | 不同切法选概率最高的 | 比较同字符串 BPE 与 Unigram 的输出 |

真实规则参考 [Hugging Face Tokenizers](https://huggingface.co/docs/tokenizers/index) 和 [课程第 6 章](https://huggingface.co/learn/llm-course/en/chapter6/1)。不同训练算法/模型修订会改变上述行为。

## 3. 七个数据治理必检查项

| 项目 | 专业/机制 | 大白话 | 需要保存的证据 |
|---|---|---|---|
| 使用许可 | 数据来源、商用许可/隐私/留存目的 | 能下载不等于能训练或分发 | Dataset Card、License、可用范围 |
| 质量与偏差 | 格式/语言/领域覆盖、错误标注、PII 风险 | 原材料有问题成品就不稳 | 抽样审计、拒绝理由分桶 |
| 精确/近重复 | Hash、MinHash 或相似性检测 | 换标点复制试题仍算泄漏 | 去重报告与阈值 |
| Train/Val/Test 隔离 | 按任务族/文档/实体/时间分割 | 考试不能用训练答案 | Split ID 与污染扫描 |
| Domain Mixing | 重采样/配比改变有效 Token 分布 | 不同原料配比改变模型口味 | 每域有效 Token 统计 |
| Padding/Truncation/Packing | Batch 组装需考虑 attention、position、label 及文档边界 | 多张订单装箱不能混单 | 展开 Attention/Labels 负例 |
| 版本与来源 | Dataset Hash、Tokenizer/Template Revision、Seed、许可变更 | 记录配方、生产批次和机器版本 | 运行 Manifest |

## 4. Chat Template 与 Loss Mask 不是同一层

Chat Template 管理 system/user/assistant/tool 角色怎么序列化；Loss Mask 决定哪些 Token 参与训练目标。**Assistant-only Mask 适用于特定指令微调目标，而不是所有 Pretrain/CPT 的硬规则**。

建议用真实模型 Tokenizer 渲染 user→assistant tool call→tool observation→assistant final；逐 Token 展开 labels，断言工具观测和用户请求不被误监督、Assistant 目标保留。当前 TRL 的 Assistant-only 功能需要 generation/endgeneration 区间，部分模型有官方模板补丁，仍要验证当前安装版本。参考 [TRL/GRPO 版本卡](../resources/OFFICIAL-RUNTIME-DELTA-20261114.md)。

## 5. 易错负例和最小实验

- 同一文档的不同改写混入训练和评测，导致虚高；
- Packing 两份独立文档后，仅有 Causal Mask **不保证文档间注意力隔离**；还需明确 Position/Document Boundary/Attention 和 Loss 规则；
- PAD、EOS、BOS、UNK 混淆导致截断、循环、未知词或错误停止；
- 不同词表模型的 Token PPL 被直接比较而未统一字节口径；
- 以 JSON 合法代替 Tool 参数/执行成功，以模型拒答代替服务端鉴权。

1. **Token 比率**：准备 20 条自建中英文文本，同一数据用两种 Tokenizer 比 Token/Byte/截断。
2. **泄漏注入**：一份产品资料改写后放到 Test，观察 Exact Hash 与近重复的不同检出能力。
3. **Mask 验证**：先运行 [CPU Shift/Mask Toy](../labs/README.md)，再在 [M06](../modules/M06.md) 用真实 Tokenizer 测 Chat Template；CPU Toy 只验证已经按角色对齐的 Token 数组。
4. **预训练数据核对**：进入 [MiniMind 固定版 Runbook](../experiments/01-minimind-whitebox/RUNBOOK-FIRST-DAY.md)，校验数据版本、许可与 Hash 后训练。

**退出门槛**：会解释 Byte/BPE/WordPiece/Unigram 区别，有分词/数据污染负例、正确的 Token Mask 和可追溯的数据授权；不需要一次学完整 NLP。
