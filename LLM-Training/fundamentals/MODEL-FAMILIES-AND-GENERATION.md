# 基础缺口 A0｜模型架构家族、生成原理与现代 Attention

> 对应 [M03](../modules/M03.md)、[M11](../modules/M11.md)、[M12](../modules/M12.md)。讨论“为什么一个模型擅长向量表示，另一个擅长聊天”和“为什么推理慢”，**不是要求先训练三种架构**。上游：[架构家族对照](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/architecture-comparison.md)；官方：[Hugging Face LLM Course](https://huggingface.co/learn/llm-course/en/chapter1/1)、[Transformers](https://huggingface.co/docs/transformers/index)、[Stanford CS336](https://cs336.stanford.edu/)。

## 1. 四种常见任务与模型家族

| 类型 | 专业机制/训练目标 | 大白话 | 使用场景/不要混用 |
|---|---|---|---|
| Encoder-only（BERT 类） | 双向上下文编码；常用 MLM 等预训练目标，输出上下文表示 | 读完整文章后理解它 | 分类、实体、表示检索；不直接等同左到右聊天生成 |
| Decoder-only（GPT/Qwen 大语言模型常见形式） | 使用 Causal Mask，根据前文逐 Token 预测输出 | 看已经写过的内容继续写 | 自回归文本/工具格式/代码生成；上下文长度影响推理 |
| Encoder–Decoder（T5/BART 类） | Encoder 先编码输入，Decoder 对输入及已生成输出进行条件生成 | 一位阅读助手先读材料，再由写手写总结 | 翻译、摘要、条件生成；并非所有 Seq2Seq 都需要同样 Tokenizer |
| Embedding / Dual Encoder / Cross Encoder | 根据训练目标提取向量/匹配得分；Dual Encoder 可离线编码文档，Cross Encoder联合看 Query+Doc | 先找书，再由专家精排 | RAG 召回/重排；不是“压缩聊天模型得到向量”这么简单 |

**关键边界**：模型的训练目标、架构和部署接口同时决定能做什么；“支持 Transformer”不意味着接口/输出可互换。模型是 Encoder-only 或 Decoder-only 不直接决定其训练数据质量和适用语言。

## 2. Decoder 的结构：训练与生成如何不同

- Embedding：Token ID → [B,T,D]；传统 Token Embedding 还需要位置机制。
- Self-Attention：Q/K/V 从同一状态中线性变换，Attention(Q,K,V)=softmax(QKᵀ/√d+mask)V，头数/维度影响张量形状。
- Causal Mask：训练时同时为多个位置算下一 Token 目标，但每个位置不能访问未来 Token；推理时逐步生成。
- FFN、LayerNorm/RMSNorm、Residual：非线性加工、稳定训练与跨层信号通道。
- 位置：绝对 Learned Embedding、RoPE/相对位置、ALiBi 等方案不同；不能把 RoPE 描述成直接给 Token Embedding 加一个绝对向量。
- 注意力优化：MHA 头分别缓存 KV；MQA/GQA 共享部分 KV Head 以节省缓存；FlashAttention 优化精确注意力的访存，并非固定的“近似替代”。
- MoE：多个 Expert 由 Router 选择，激活参数量和总参数量不同，训练需要处理 Load Balance/通信。

## 3. PreFill、Decode、KV Cache、生成策略

| 技术 | 专业解释 | 白话 | 最小对照 |
|---|---|---|---|
| Prefill | 输入 Prompt 一次性进行历史上下文前向计算，填充历史 KV | 先读完所有材料和做索引 | 固定模型下测 Prompt 长度 vs TTFT |
| Decode | 以已生成 Token 为新输入逐步生成（具体框架可能批处理） | 每写一个字继续决定下一个字 | 固定输出长度比较 TPOT / output Token/s |
| KV Cache | 保留历史 K/V，减少每步重复计算；缓存开销随上下文/并发增长 | 保存笔记索引，省去重复开会 | 模拟 MHA/GQA 数量、dtype、上下文和并发对显存的影响 |
| Temperature | logit/temperature 调节采样分布，T 变小通常更集中 | 更保守还是更随机 | 同 seed/配置对比生成多样性；不把随机性等同正确性 |
| Top-k / Top-p | 截取概率候选集后采样；Top-p 按累计概率 | 先限定入围候选，再抽一个 | 对已知 4 类分布算保留项 |
| Beam Search / Best-of-N / Rerank | 多路径搜索或采样后用评分器选择；有额外推理/验证成本 | 写多个草稿由评委挑一个 | 分开记录 N、Tokens、验证器正确率 |
| Long-context | 增大输入长度会影响 Attention/KV/召回/位置泛化和端到端评估 | 书桌放了几百页不等于能找对答案 | 长短 Context 正反样例对照、注意 Needle 测试局限 |

**不要混淆**：高 Prefill 带宽吞吐不等于低 TTFT；Tokens/s 和 P95 不同；KV Cache 不等于训练 Checkpoint；Test-time Compute 不等于训练时 RL。

## 4. 两个练习：先做已有 Toy，再跑真实模型

1. [TinyGPT](../labs/tiny-gpt/README.md)：修改第 6～8 Token，验证前几个输出 Logits 不受未来干扰；它的 Learned Position/LayerNorm/GELU 不是 Qwen 现代结构。
2. [MiniMind](../experiments/01-minimind-whitebox/RUNBOOK-FIRST-DAY.md)：找出 Q/K/V 的 shape、RoPE、GQA/RMSNorm 位置，确认源码里 Loss Shift 是在哪一层完成；记录训练和推理接口的真实 revision。
3. [M11 推理服务](../modules/M11.md)：只在已经有自己的受控服务后测 TTFT/TPOT、吞吐和并发；未运行不得照抄“RTX 16GB 可以几百并发”等结论。
4. [RAG/Agent 六域地图](../knowledge-graph/LLM-FULL-STACK-ATLAS.md)：当需求是查实时知识时，优先比较 Embedding/Reranking/RAG 而不是先研究模型预训练。

## 5. 知识点短测

- 为什么 Tokenizer 相同但模型大小不同不能保证输出相同？
- 为什么修改未来 Token 不应该影响当前 Transformer Decoder 前面的 Logits？
- MHA/GQA 在固定 B,T,D, dtype 和层数下，KV Cache 的主要差异来自什么？
- “更长 Prompt 一定提升知识问答正确率”为什么错？
- 怎样区分 Encoder 模型抽取语义、Dual Encoder 检索、Decoder 对话、VLM 图文感知？

**退出**：至少画出一次 Encoder vs Decoder 的信息流，解释 QKV 的 [B,H,T,D] 和 Decode/KV 的性能关系；有源码和负例即可，无需同时训练 BERT/T5/GPT。
