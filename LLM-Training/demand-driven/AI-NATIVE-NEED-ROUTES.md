# AI-Native 需求驱动学习：12 条可从任意一点启动的路线卡

> **不按课程章数排队**。每张卡的逻辑是“问题 → 最低成本基线 → 必要概念 → 源码/实验 → 失败注入 → 独立验收/停止”。问题可以是真实授权任务、历史面试、自己选的练习或合成测试，但必须标明真实证据等级。此表是候选学习案例，不代表用户已有某客户订单、某面试或某模型训练结果。

## 开始前，先回答三个问题

1. 眼前最具体的一条失败是什么？能否输入一条真实或脱敏的最小可复现任务？
2. **如果完全不训练模型**，通过规则/Prompt/RAG/已发布模型/API 能否达标？如果可以，为什么要升级复杂度？
3. 本次判断通过的独立指标是什么，失败时退回哪一层？给自己一个小型研究时间盒（例如一次会话或一次实验），不要绑定两三个月排期。

## 12 张需求卡

### N01｜RAG 找不到证据或引用错

**从症状进入的最短知识顺序（不是全仓学习顺序）**：**A02 Retrieval/Embedding/Rerank** → **A03 RAG/Agentic RAG** → **E01 基础评测/正确性/回归** → **O03 安全/权限/隐私**。

- **第一件事**：先用 15 条固定 QA、包含无答案/越权/多跳的任务建立不训练基线。
- **专业机制/源码**：Recall@k 与 Citation Support 分开测；固定权限身份。
- **最小反例/实战**：把多条同义文档和错误引用放进测试集，分析是召回、重排还是生成层。
- **达到即可停止**：能交代失败在哪一层；不能只凭少量示例声称 RAG 可上线。
- **专项深入**：[M02](../modules/M02.md) · [M10](../modules/M10.md) · [M06](../modules/M06.md) · [M11](../modules/M11.md)。
- **上游原理**：[材料1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/05-applications.md) · [材料2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/practice/rag/README.md) · [材料3](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-rag-learning-research-20261029.md) · [材料4](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/playbooks/rag-agent-chatbot.md)。
- **权威参考**：[Ragas metrics](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) · [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit1/introduction) · [EleutherAI lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)。

### N02｜Agent 工具调用错误、越权或状态断裂

**从症状进入的最短知识顺序（不是全仓学习顺序）**：**A04 Function Calling 与 MCP** → **A05 Workflow/Agent/Multi-agent** → **A06 Memory/State/HITL** → **O03 安全/权限/隐私** → **O02 Observability/Tracing**。

- **第一件事**：从 JSON 参数、用户角色、工具权限和会话恢复各选一个最小负例。
- **专业机制/源码**：跑 Tool Gateway 合成测试，再到 LangGraph 状态/检查点。
- **最小反例/实战**：加入不可逆副作用前要求 HITL 与 idempotency；审查 MCP 版本。
- **达到即可停止**：换新的业务工具仍能正确拒答/恢复；未压测不称生产完成。
- **专项深入**：[M06](../modules/M06.md) · [M11](../modules/M11.md) · [M10](../modules/M10.md) · [M12](../modules/M12.md) · [M02](../modules/M02.md) · [M09](../modules/M09.md)。
- **上游原理**：[材料1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/05-applications.md) · [材料2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/playbooks/rag-agent-chatbot.md) · [材料3](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-agent-learning-research-20261029.md) · [材料4](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/06-production.md)。
- **权威参考**：[MCP 2026-07-28 specification](https://modelcontextprotocol.io/specification/2026-07-28) · [Qwen Function Calling](https://qwen.readthedocs.io/en/latest/framework/function_call.html) · [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview)。

### N03｜模型 OOM、吞吐不达标

**从症状进入的最短知识顺序（不是全仓学习顺序）**：**S01 训练显存与数值精度** → **S03 Kernel/Compiler/Profiler** → **E02 Prefill/Decode/KV Cache** → **E05 Serving/引擎/接口安全**。

- **第一件事**：拿一次真实或合成 microbatch 的权重、激活、KV Cache 做估算。
- **专业机制/源码**：记录 PyTorch allocated/reserved（需真实 GPU），再用 Profiler 找热点。
- **最小反例/实战**：固定模型只改 seq_len，比较显存与吞吐；如无 GPU 仅理论。
- **达到即可停止**：能解释 OOM 的实际分项；不以估算冒充实测。
- **专项深入**：[M01](../modules/M01.md) · [M09](../modules/M09.md) · [M03](../modules/M03.md) · [M11](../modules/M11.md)。
- **上游原理**：[材料1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/02-training-systems.md) · [材料2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/prefill-decode-kv-cache.md) · [材料3](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/projects/decoder-only-mini-inference/README.md) · [材料4](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/04-model-engineering.md)。
- **权威参考**：[PyTorch](https://pytorch.org/docs/stable/index.html) · [Stanford CS336 Spring 2026](https://cs336.stanford.edu/) · [Hugging Face Transformers](https://huggingface.co/docs/transformers/index)。

### N04｜想做 QLoRA/SFT 但 Mask 不懂

**从症状进入的最短知识顺序（不是全仓学习顺序）**：**P01 SFT 与 PEFT/QLoRA** → **F03 Tokenizer/数据/污染** → **F04 Decoder block 与因果注意力** → **E01 基础评测/正确性/回归**。

- **第一件事**：打印 Qwen 官方 Chat Template 展开和 token label mask。
- **专业机制/源码**：跑 CPU toy，再对比模板中 system/user/assistant/tool 的 loss token。
- **最小反例/实战**：故意让 tool observation 参与 loss，检查评测是否变化。
- **达到即可停止**：模型级数据和真实 tokenizer mask 校验，不用一个合成单测称 SFT 成功。
- **专项深入**：[M06](../modules/M06.md) · [M02](../modules/M02.md) · [M03](../modules/M03.md) · [M01](../modules/M01.md) · [M10](../modules/M10.md)。
- **上游原理**：[材料1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/03-post-training.md) · [材料2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/01-foundation.md) · [材料3](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-llm-learning-research-20261029.md) · [材料4](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/transformer-block.md)。
- **权威参考**：[Hugging Face TRL trainers](https://huggingface.co/docs/trl/index) · [Hugging Face PEFT](https://huggingface.co/docs/peft/index) · [Hugging Face Datasets](https://huggingface.co/docs/datasets/index)。

### N05｜DPO/GRPO Reward 上升但正确率下降

**从症状进入的最短知识顺序（不是全仓学习顺序）**：**P03 Reward Model/DPO/Online DPO** → **P04 PPO/GRPO/RLVR** → **E01 基础评测/正确性/回归** → **S01 训练显存与数值精度**。

- **第一件事**：先复现 DPO margin 和 GRPO group Advantage 的数值示例。
- **专业机制/源码**：做格式奖励可被投机的错误答案，用独立 verifier 复查。
- **最小反例/实战**：同一个 SFT checkpoint 独立对照 DPO vs GRPO 分支。
- **达到即可停止**：独立任务指标与成本验证；Reward 上涨不等于准确率提高。
- **专项深入**：[M07](../modules/M07.md) · [M08](../modules/M08.md) · [M10](../modules/M10.md) · [M01](../modules/M01.md) · [M09](../modules/M09.md)。
- **上游原理**：[材料1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/03-post-training.md) · [材料2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/04-model-engineering.md) · [材料3](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/02-training-systems.md)。
- **权威参考**：[Hugging Face TRL trainers](https://huggingface.co/docs/trl/index) · [verl RL training](https://github.com/volcengine/verl) · [EleutherAI lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)。

### N06｜行业知识更新快，要不要 CPT

**从症状进入的最短知识顺序（不是全仓学习顺序）**：**F01 问题定义/训练或不训练** → **F07 CPT/中训练/防遗忘** → **A03 RAG/Agentic RAG** → **E01 基础评测/正确性/回归**。

- **第一件事**：定义领域事实更新频率、引用需求、成本/许可。
- **专业机制/源码**：先跑 Base+RAG，只有结构性行为缺口才考虑 CPT。
- **最小反例/实战**：若要 CPT，比 Domain-only/Replay 与通用 PPL。
- **达到即可停止**：能给出为什么不训练的明确判断，并提交对照证据。
- **专项深入**：[M10](../modules/M10.md) · [M05](../modules/M05.md) · [M06](../modules/M06.md)。
- **上游原理**：[材料1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/01-foundation.md) · [材料2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/market/llm-demand-to-practice-20261029.md) · [材料3](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/05-applications.md) · [材料4](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-rag-learning-research-20261029.md)。
- **权威参考**：[Stanford CS336 Spring 2026](https://cs336.stanford.edu/) · [Hugging Face Datasets](https://huggingface.co/docs/datasets/index) · [Ragas metrics](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/)。

### N07｜理解模型推理 TTFT、KV Cache

**从症状进入的最短知识顺序（不是全仓学习顺序）**：**F05 现代注意力 RoPE/GQA/MLA** → **E02 Prefill/Decode/KV Cache** → **E05 Serving/引擎/接口安全** → **S03 Kernel/Compiler/Profiler**。

- **第一件事**：固定 Prompt/Completion 长度，先解释 Prefill 与 Decode。
- **专业机制/源码**：追踪 Q/K/V 与 cache memory，测 TTFT/TPOT/Token/s。
- **最小反例/实战**：改变并发/Batch，观察平均与 P95 分开变化。
- **达到即可停止**：只有真实固定环境测量才写性能数值，失败可归因。
- **专项深入**：[M03](../modules/M03.md) · [M09](../modules/M09.md) · [M11](../modules/M11.md)。
- **上游原理**：[材料1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/modern-attention-and-position.md) · [材料2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/prefill-decode-kv-cache.md) · [材料3](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/projects/decoder-only-mini-inference/README.md) · [材料4](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/04-model-engineering.md)。
- **权威参考**：[Stanford CS336 Spring 2026](https://cs336.stanford.edu/) · [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) · [vLLM serving](https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/)。

### N08｜多模态产品：图片、音频和文本

**从症状进入的最短知识顺序（不是全仓学习顺序）**：**F08 多模态基础与投影融合** → **X01 跨域多模态处理链** → **A03 RAG/Agentic RAG** → **E01 基础评测/正确性/回归**。

- **第一件事**：选定图片 OCR 的简单样本与相同问题。
- **专业机制/源码**：比较 OCR+RAG 和 VLM 输出，分离识别错误与检索错误。
- **最小反例/实战**：增加模态缺失、低清图/音频噪音负例。
- **达到即可停止**：以任务级指标而非演示图漂亮程度判断收益。
- **专项深入**：[M12](../modules/M12.md) · [M03](../modules/M03.md) · [M10](../modules/M10.md) · [M06](../modules/M06.md)。
- **上游原理**：[材料1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/multimodal-vertical.md) · [材料2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-cv-research-20261029.md) · [材料3](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/05-applications.md) · [材料4](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-rag-learning-research-20261029.md)。
- **权威参考**：[Hugging Face Multimodal Generation](https://huggingface.co/docs/transformers/tasks/any_to_any) · [Ragas metrics](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) · [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit1/introduction)。

### N09｜模型上线安全、监控、回滚

**从症状进入的最短知识顺序（不是全仓学习顺序）**：**O01 LLMOps 评估与模型版本** → **O02 Observability/Tracing** → **O03 安全/权限/隐私** → **O04 成本/反馈/构建或购买** → **E05 Serving/引擎/接口安全**。

- **第一件事**：给服务设定合成 SLO、安全权限、异常恢复与回滚条件。
- **专业机制/源码**：加入请求 trace、限流、越权/注入、版本回滚测试。
- **最小反例/实战**：模拟新模型 B 参数正确率下降，按规则回滚 A。
- **达到即可停止**：G0–G8 视场景验收；缺实测证据就 No-Go。
- **专项深入**：[M10](../modules/M10.md) · [M11](../modules/M11.md) · [M09](../modules/M09.md) · [M02](../modules/M02.md)。
- **上游原理**：[材料1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/06-production.md) · [材料2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/market/llm-demand-to-practice-20261029.md) · [材料3](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/cross-cutting-planes.md) · [材料4](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/04-model-engineering.md)。
- **权威参考**：[NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) · [EleutherAI lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) · [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md)。

### N10｜不想训练，想用 API/Prompt 快速实现

**从症状进入的最短知识顺序（不是全仓学习顺序）**：**F01 问题定义/训练或不训练** → **A01 Prompt 与 Context Engineering** → **E05 Serving/引擎/接口安全** → **E01 基础评测/正确性/回归**。

- **第一件事**：对同一测试集建立规则、Prompt、API、RAG 四组候选。
- **专业机制/源码**：比较首字延迟、预算、权限和任务级质量。
- **最小反例/实战**：用不相关文档和错误上下文引入反例。
- **达到即可停止**：不训练基线达到目标即停止，不为追新架构增加复杂度。
- **专项深入**：[M10](../modules/M10.md) · [M05](../modules/M05.md) · [M06](../modules/M06.md) · [M02](../modules/M02.md) · [M11](../modules/M11.md) · [M09](../modules/M09.md)。
- **上游原理**：[材料1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/01-foundation.md) · [材料2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/market/llm-demand-to-practice-20261029.md) · [材料3](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/05-applications.md) · [材料4](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-context-engineering-research-20261029.md)。
- **权威参考**：[Stanford CS336 Spring 2026](https://cs336.stanford.edu/) · [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit1/introduction) · [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)。

### N11｜从零理解 Decoder/Tokenizer/预训练

**从症状进入的最短知识顺序（不是全仓学习顺序）**：**F02 架构家族 Encoder/Decoder/Seq2Seq** → **F03 Tokenizer/数据/污染** → **F04 Decoder block 与因果注意力** → **F06 Pretrain/Checkpoint/Scaling** → **S04 训练可靠性与复现**。

- **第一件事**：先在 Decoder-Only 上追踪 prompt→token→logits→next token。
- **专业机制/源码**：用 MiniMind 和上游 Decoder-Only Concept Map 对齐模型 shape。
- **最小反例/实战**：修改 causal mask 检测未来信息泄漏。
- **达到即可停止**：能解释一个 batch 与一次 decode 的区别并执行独立测试。
- **专项深入**：[M03](../modules/M03.md) · [M02](../modules/M02.md) · [M01](../modules/M01.md) · [M04](../modules/M04.md) · [M09](../modules/M09.md) · [M10](../modules/M10.md)。
- **上游原理**：[材料1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/architecture-comparison.md) · [材料2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/01-foundation.md) · [材料3](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-llm-learning-research-20261029.md) · [材料4](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/transformer-block.md)。
- **权威参考**：[Hugging Face LLM Course](https://huggingface.co/learn/llm-course/en/chapter1/1) · [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) · [Hugging Face Datasets](https://huggingface.co/docs/datasets/index)。

### N12｜未来研究分布式训练、Agentic RL

**从症状进入的最短知识顺序（不是全仓学习顺序）**：**S02 分布式并行与状态切分** → **S04 训练可靠性与复现** → **P04 PPO/GRPO/RLVR** → **P05 Reasoning/Agentic RL** → **O02 Observability/Tracing**。

- **第一件事**：先画 Actor/Rollout/Reference/Reward/Controller 的数据和权重流。
- **专业机制/源码**：看 verl 及 FSDP 源码，单卡仅做概念/数学 toy。
- **最小反例/实战**：列出通信、显存、长轨迹奖励中的失败边界。
- **达到即可停止**：不把画架构图当真实多 GPU 性能验证。
- **专项深入**：[M09](../modules/M09.md) · [M04](../modules/M04.md) · [M10](../modules/M10.md) · [M08](../modules/M08.md) · [M12](../modules/M12.md) · [M11](../modules/M11.md)。
- **上游原理**：[材料1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/02-training-systems.md) · [材料2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/03-post-training.md) · [材料3](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/multimodal-vertical.md) · [材料4](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/06-production.md)。
- **权威参考**：[PyTorch](https://pytorch.org/docs/stable/index.html) · [verl RL training](https://github.com/volcengine/verl) · [Stanford CS336 Spring 2026](https://cs336.stanford.edu/)。

## 不需要为了“完整知识地图”付出几个月的学习时间

看清全局，可以花一次会话读 [六域主图](../knowledge-graph/LLM-FULL-STACK-ATLAS.md) 和 [术语对照](../resources/UPSTREAM-RESOURCE-MAP.md)。记住“名字+所在位置+输入输出+跟谁协作”即可；尚未用到的知识点保持 **L0 我知道它在哪里**。

遇到需求，再升级到：**L1 理解专业定义/原理/白话 → L2 自己运行并修改 → L3 陌生任务迁移 → L4 适用场景的生产门禁**。不是每个知识都必须提前做 L3/L4。

## 自动检索入口

在仓库根目录：

~~~bash
python LLM-Training/tools/route_atlas.py --list
python LLM-Training/tools/route_atlas.py --need N02
python LLM-Training/tools/route_atlas.py --search "RAG"
python LLM-Training/tools/route_atlas.py --domain A
python LLM-Training/tools/route_atlas.py --topic A04
~~~

该工具是**离线关键词/主题导航**，不是理解任意中文意图的 Agent；没有命中时对照 [需求卡模板](DEMAND-CARD-TEMPLATE.md) 人工增加新路线，千万不要虚构来源。

## AI 导师协同学习

把当前需求带给 [AI-Native 学习闭环操作手册](../learning-method/AI-NATIVE-LEARNING-LOOP.md) 使用：AI 负责生成多种解释和疑难定位候选，真实源码/官方文档与自己执行结果负责验收。**AI 可以缩短找资料与解释时间，不能代替调试、代码执行与独立能力检验。**
