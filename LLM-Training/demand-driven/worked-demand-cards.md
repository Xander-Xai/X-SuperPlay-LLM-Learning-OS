# 五张代表性需求卡｜从问题直接进入学习

> 全部是**教学示例 / SYNTHETIC / NOT RUN**，不是曾经上线、客户需求或训练结果。每张都可独立进入，顺序不固定。复制 [模板](DEMAND-CARD-TEMPLATE.md) 后再记录真实操作。

## D01：RAG 文本有引用但引用不支持结论

**问题**：模型引用正确格式的 source_id，却把召回片段里没有的库存数字当事实。

- **先不要训练**：做 20 条虚构文档/提问/证据标注；分别记录 Retriever Hit@K、Evidence Support、Unsupported Claim Rate。
- **原理最小路径**：M10（claim-level 评估）→ M06（拒答/证据约束行为）；若检索不好才补 M02（数据组织与去重）/Embedding。
- **对照**：A 规则引用绑定；B 仅 Prompt 更严；C 如果 B 明确不足再引入结构化 Tool-SFT；相同 held-out 数据集。
- **负例**：同名文档不同版本；用户无权访问证据；没有库存来源但回答出现数字；引用合法却不支持该句。
- **验收**：正确引用/拒答按标注可计算，负例不会从无证据造数；P95/成本不得明显变坏而未解释。
- **不使用**：在检索证据缺失、权限过滤错误时，不先用 CPT 或 GRPO 硬救。
- **来源**：[上游 RAG 练习](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/tree/main/docs/practice/rag)、[Eval Protocol](../evaluation/evaluation-protocol.md)。

## D02：Function Calling 工具选择对，但参数和多轮状态错

**问题**：query_inventory 要求 product_id，模型把商品名称当 ID；工具响应被错当 Assistant 继续学习。

- **零训练基线**：固定 schema 和 tool parser，尝试 prompt/schema 校正 + 容错解析，运行成功率作为基线。
- **最短依赖**：M06（多轮监督与模板）→ M02（Tokenizer/role boundary）→ M10（selection/args/e2e）；需要时再 M07。
- **动手**：[CPU Toy Mask](../labs/README.md)→[MiniMind 训练原理](../experiments/01-minimind-whitebox/README.md)→[Qwen Tool SFT](../experiments/03-agent-tool-sft/README.md)，分别验证生成工具调用和环境 Tool Observation 的标签。
- **负例**：缺失参数、JSON schema 合法但 ID 错、超时重试导致重复写、无权限敏感接口。
- **验收**：Tool selection、Argument Accuracy、Execution Success、state restore、权限边界用相同测试集对照。
- **停止条件**：Prompt/Schema 已达到要求时可以不训练；不是每个工具错误都要 DPO。

## D03：线上 20 并发时 P95 翻倍，不能只优化模型权重

**问题**：单请求 TTFT 正常，批量场景 Prefill/Decode 或排队导致延迟剧增。

- **首先定位瓶颈**：确定客户端、网络、队列、batching、KV Cache、prefill、decode 的时间占比；固定 context/output length、concurrency、硬件和 warm/cold。
- **最短依赖**：M11 Serving → M09 Profiler/内存 → M03 KV/GQA；M01/M04 不默认必须补。
- **实验**：同条件比较 batch/并发限额、prefix cache、max_model_len、quantization 之一；记录 TTFT/P95/tokens/s/GPU 峰值/Tool Call 解析成功率。
- **负例**：超时/取消、超长 Prompt、冷启动 OOM、流式中断、模型返回无效 JSON。
- **上线门槛**：压力测试、错误率、限流/熔断、监控告警、版本化回滚；不把 1 个 curl 成功当上线。
- **来源**：[vLLM docs](https://docs.vllm.ai/en/latest/)。

## D04：CPT 领域 Loss 更低但通用问题退化

- **基线**：保持原始 Base，固定域内/域外 held-out；数据是模拟术语手册或经授权数据。
- **最短依赖**：M05 CPT/Replay → M10 Evaluation → M02 去重/混合。
- **训练矩阵**：Base、Domain-only、80/20 Replay（配比是假设不是定律）；在同一配比下另做 WSD/Cosine 调度器对照。
- **指标**：domain CE、general CE、事实问答任务、时间成本；尽量多个 seed。
- **负例**：近重复测试污染、领域数据版本重复、学到格式而非知识、不同 tokenizer 引起 PPL 不可比。
- **结论允许**：“不如 RAG”“在当前预算下没有改进”；这同样是成功的诊断。

## D05：GRPO Reward 上升但验证集准确率没涨

- **第一步**：不要增加训练步数，先审奖励函数、Group std、独立 Eval 和截断率。
- **最短依赖**：M08 Advantage/Clip/Reward → M10 评估隔离 → M09 低显存 Rollout；M07 只补偏好/验证器需要的部分。
- **动作**：对固定算术题做 K=2–4 候选 rollout，记录 per-component reward；先更新 0 步检验 scorer 再决定训练。
- **负例**：只输出格式就得分、答案从 prompt 泄漏、模型复述评分器标记、group 全部同分。
- **16GB 回退**：原生 TRL/LoRA/短序列优先；Unsloth/vLLM 是实测后加速选项，不能预先假设显存和吞吐。
- **独立评估**：任务正确率、答题长度、clip、KL（如适用）、tokens/s、OOM；若 Reward 造假，直接停训修 scorer。

五张示范仅教如何定义和筛查学习任务，不假装已经证明任何方案有效。

