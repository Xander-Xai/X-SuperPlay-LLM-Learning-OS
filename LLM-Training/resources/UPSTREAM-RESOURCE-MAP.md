# 上游 AI-Learning-OS 知识资源总索引｜跨仓直达与权威学习入口

> 截止 2026-11-14：已按上游 Git 树核对 **33 个主题所引用的内部文件路径均存在**，并固定 [上游源提交](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/commit/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a)。本文件不复制全部原始内容，不自动同步私有仓，不声称逐条对外网 HTTP/版本兼容性都做了测试；官方课程/文档已抽样联网核实，其余是官方域名或论文的目录候选，使用时再复查。

## 先看哪些链接？

- **全局世界地图**：[上游六域 Atlas](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/README.md)（是什么、有几类）。
- **训练/模型专项**：[本仓 Roadmap V3](../ROADMAP-V3-DEMAND-DRIVEN.md)（现有 M01–M12） + [MiniMind/Qwen 实验](../experiments/README.md)。
- **知识点逐条解释**：[上游 Decoder-Only L2 概念图](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/concept-map.md)、[上下文/应用 Atlas](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/05-applications.md)、[生产 Atlas](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/06-production.md)。
- **按今天的问题选学**：[12 个需求任务卡](../demand-driven/AI-NATIVE-NEED-ROUTES.md) + [CLI 检索](../tools/route_atlas.py)。

所有术语引用建议记录：上游路径与 SHA、外部来源的发布日期或版本、当前自己的代码/data SHA、是否实际运行。不要把历史调研中的第三方 README 直接视为安全可用的实战项目。

## 逐域知识点和一键参考

### F｜基础模型：数据、架构、预训练

[上游本域总纲](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/01-foundation.md)

| 知识点 | 为什么要学 / 大白话 | 上游原文 | 官方/原始参考 | 专项模块 |
|---|---|---|---|---|
| F01 **问题定义/训练或不训练** | 先确认病因，再决定买药还是开刀 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/01-foundation.md) · [原文2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/market/llm-demand-to-practice-20261029.md) | [Stanford CS336 Spring 2026](https://cs336.stanford.edu/) | [M10](../modules/M10.md)/[M05](../modules/M05.md)/[M06](../modules/M06.md) |
| F02 **架构家族 Encoder/Decoder/Seq2Seq** | 图书管理员理解全文、翻译官先读后写、写作助手逐字续写 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/architecture-comparison.md) | [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/en/chapter1/1) · [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) | [M03](../modules/M03.md) |
| F03 **Tokenizer/数据/污染** | 原料检验与切料，混入试卷答案就不是真考试 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/01-foundation.md) · [原文2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-llm-learning-research-20261029.md) | [Hugging Face Datasets](https://huggingface.co/docs/datasets/index) · [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/en/chapter1/1) | [M02](../modules/M02.md) |
| F04 **Decoder block 与因果注意力** | 写句子只能看已写的字，不能偷看未来 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/transformer-block.md) · [原文2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/causal-mask-and-autoregression.md) | [Stanford CS336 Spring 2026](https://cs336.stanford.edu/) · [MiniMind code](https://github.com/jingyaogong/minimind) | [M03](../modules/M03.md)/[M01](../modules/M01.md) |
| F05 **现代注意力 RoPE/GQA/MLA** | 给记忆加坐标，减少多人重复保存同一份资料 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/modern-attention-and-position.md) | [Stanford CS336 Spring 2026](https://cs336.stanford.edu/) · [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) | [M03](../modules/M03.md)/[M09](../modules/M09.md) |
| F06 **Pretrain/Checkpoint/Scaling** | 背诵语言世界规律的基础训练，不等于学会遵守具体指令 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/01-foundation.md) · [原文2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/projects/llm-training-dual-repo/README.md) | [Stanford CS336 Spring 2026](https://cs336.stanford.edu/) · [MiniMind code](https://github.com/jingyaogong/minimind) | [M04](../modules/M04.md)/[M01](../modules/M01.md) |
| F07 **CPT/中训练/防遗忘** | 专精行业可能生疏通用知识，需定期复习 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/01-foundation.md) | [Stanford CS336 Spring 2026](https://cs336.stanford.edu/) · [Hugging Face Datasets](https://huggingface.co/docs/datasets/index) | [M05](../modules/M05.md)/[M10](../modules/M10.md) |
| F08 **多模态基础与投影融合** | 让读文字的专家学会看图听音，先要统一交互接口 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/multimodal-vertical.md) | [Hugging Face Multimodal Generation](https://huggingface.co/docs/transformers/tasks/any_to_any) | [M12](../modules/M12.md)/[M03](../modules/M03.md) |
| X01 **跨域多模态处理链** | 图文音视频是另外几种‘原材料’，都需质检、加工、复验 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/multimodal-vertical.md) · [原文2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-cv-research-20261029.md) | [Hugging Face Multimodal Generation](https://huggingface.co/docs/transformers/tasks/any_to_any) | [M12](../modules/M12.md)/[M03](../modules/M03.md)/[M10](../modules/M10.md) |

### S｜训练与计算系统：显存、并行、可靠性

[上游本域总纲](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/02-training-systems.md)

| 知识点 | 为什么要学 / 大白话 | 上游原文 | 官方/原始参考 | 专项模块 |
|---|---|---|---|---|
| S01 **训练显存与数值精度** | 仓库不只有货物，还有机器、半成品和缓存 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/02-training-systems.md) | [PyTorch](https://pytorch.org/docs/stable/index.html) | [M01](../modules/M01.md)/[M09](../modules/M09.md) |
| S02 **分布式并行与状态切分** | 多个厨房分工，分食材还是分厨师任务是两种切法 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/02-training-systems.md) | [PyTorch](https://pytorch.org/docs/stable/index.html) · [verl RL training](https://github.com/volcengine/verl) | [M09](../modules/M09.md) |
| S03 **Kernel/Compiler/Profiler** | 锅的火力、洗菜速度、人员移动决定整体出餐速度 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/02-training-systems.md) | [Stanford CS336 Spring 2026](https://cs336.stanford.edu/) · [PyTorch](https://pytorch.org/docs/stable/index.html) | [M09](../modules/M09.md)/[M03](../modules/M03.md) |
| S04 **训练可靠性与复现** | 训练存档必须包含进度、环境和未完成任务 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/02-training-systems.md) | [PyTorch](https://pytorch.org/docs/stable/index.html) · [Stanford CS336 Spring 2026](https://cs336.stanford.edu/) | [M04](../modules/M04.md)/[M09](../modules/M09.md)/[M10](../modules/M10.md) |

### P｜后训练：行为、偏好、强化学习

[上游本域总纲](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/03-post-training.md)

| 知识点 | 为什么要学 / 大白话 | 上游原文 | 官方/原始参考 | 专项模块 |
|---|---|---|---|---|
| P01 **SFT 与 PEFT/QLoRA** | 给员工示范标准服务动作，不要求它编造查询接口返回 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/03-post-training.md) | [Hugging Face TRL trainers](https://huggingface.co/docs/trl/index) · [Hugging Face PEFT](https://huggingface.co/docs/peft/index) | [M06](../modules/M06.md)/[M02](../modules/M02.md) |
| P02 **合成数据/拒绝采样/偏好对** | 试卷自动出题可以，但答案必须有核对标准 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/03-post-training.md) · [原文2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-llm-learning-research-20261029.md) | [Hugging Face TRL trainers](https://huggingface.co/docs/trl/index) | [M02](../modules/M02.md)/[M06](../modules/M06.md)/[M07](../modules/M07.md) |
| P03 **Reward Model/DPO/Online DPO** | 评委的喜好能改变答题风格，但不代表事实正确 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/03-post-training.md) | [Hugging Face TRL trainers](https://huggingface.co/docs/trl/index) | [M07](../modules/M07.md) |
| P04 **PPO/GRPO/RLVR** | 同一题的几份答案集体评分，全同分没法学习谁更好 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/03-post-training.md) | [Hugging Face TRL trainers](https://huggingface.co/docs/trl/index) · [verl RL training](https://github.com/volcengine/verl) | [M08](../modules/M08.md)/[M10](../modules/M10.md) |
| P05 **Reasoning/Agentic RL** | 棋局的最后输赢不能简单归因给最后一手棋 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/03-post-training.md) · [原文2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/multimodal-vertical.md) | [Hugging Face TRL trainers](https://huggingface.co/docs/trl/index) · [verl RL training](https://github.com/volcengine/verl) | [M08](../modules/M08.md)/[M12](../modules/M12.md) |

### E｜模型工程：评估、推理、服务

[上游本域总纲](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/04-model-engineering.md)

| 知识点 | 为什么要学 / 大白话 | 上游原文 | 官方/原始参考 | 专项模块 |
|---|---|---|---|---|
| E01 **基础评测/正确性/回归** | 体检不只看体重，要同时检查血压、血糖和症状 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/04-model-engineering.md) | [EleutherAI lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) · [Ragas metrics](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) | [M10](../modules/M10.md) |
| E02 **Prefill/Decode/KV Cache** | 先一次性整理所有资料，再逐字写作并保存历史索引 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/prefill-decode-kv-cache.md) · [原文2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/projects/decoder-only-mini-inference/README.md) | [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) · [vLLM serving](https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/) | [M03](../modules/M03.md)/[M11](../modules/M11.md) |
| E03 **Decoding/采样/测试时计算** | 写作时可按概率选词或多写几版再挑，不代表记忆改变 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/04-model-engineering.md) | [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) | [M11](../modules/M11.md)/[M12](../modules/M12.md) |
| E04 **量化/蒸馏/Adapter Merge** | 把厚百科压缩成便携本，容量小了不代表所有章节无损 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/04-model-engineering.md) | [Hugging Face PEFT](https://huggingface.co/docs/peft/index) · [vLLM serving](https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/) | [M11](../modules/M11.md)/[M06](../modules/M06.md) |
| E05 **Serving/引擎/接口安全** | 餐厅出餐不只靠厨师，还靠排队与门禁 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/04-model-engineering.md) · [原文2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/06-production.md) | [vLLM serving](https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/) · [OWASP GenAI Security](https://genai.owasp.org/llm-top-10/) | [M11](../modules/M11.md)/[M09](../modules/M09.md) |

### A｜应用：Prompt、RAG、Tools、Agent

[上游本域总纲](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/05-applications.md)

| 知识点 | 为什么要学 / 大白话 | 上游原文 | 官方/原始参考 | 专项模块 |
|---|---|---|---|---|
| A01 **Prompt 与 Context Engineering** | 给员工的工作台：任务说明、参考资料和当前状态摆放得对才高效 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/05-applications.md) · [原文2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-context-engineering-research-20261029.md) | [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit1/introduction) · [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) | [M02](../modules/M02.md)/[M10](../modules/M10.md) |
| A02 **Retrieval/Embedding/Rerank** | 图书馆找书：目录检索、语义找相似书、专家重排 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/05-applications.md) · [原文2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/practice/rag/README.md) | [Ragas metrics](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) | [M02](../modules/M02.md)/[M10](../modules/M10.md) |
| A03 **RAG/Agentic RAG** | 开卷考试：模型可以查资料，但引用必须能支持答案 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/05-applications.md) · [原文2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-rag-learning-research-20261029.md) · [原文3](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/playbooks/rag-agent-chatbot.md) | [Ragas metrics](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) · [Hugging Face Agents Course](https://huggingface.co/learn/agents-course/en/unit1/introduction) | [M10](../modules/M10.md)/[M06](../modules/M06.md) |
| A04 **Function Calling 与 MCP** | 工具调用像申请操作单，MCP 像统一的插座协议，插上不等于有权限 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/05-applications.md) · [原文2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/playbooks/rag-agent-chatbot.md) | [MCP 2026-07-28 specification](https://modelcontextprotocol.io/specification/2026-07-28) · [Qwen Function Calling](https://qwen.readthedocs.io/en/latest/framework/function_call.html) | [M06](../modules/M06.md)/[M11](../modules/M11.md) |
| A05 **Workflow/Agent/Multi-agent** | 流水线是既定步骤，智能员工会决定下一步做什么；多个员工不自动更好 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/05-applications.md) · [原文2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-agent-learning-research-20261029.md) | [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) · [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) | [M06](../modules/M06.md)/[M10](../modules/M10.md)/[M12](../modules/M12.md) |
| A06 **Memory/State/HITL** | 便签是当前步骤，档案柜保存长期事实，经理签字批准高风险动作 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/05-applications.md) | [LangGraph overview](https://docs.langchain.com/oss/python/langgraph/overview) | [M06](../modules/M06.md)/[M10](../modules/M10.md)/[M11](../modules/M11.md) |

### O｜LLMOps：发布、监控、安全、治理

[上游本域总纲](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/06-production.md)

| 知识点 | 为什么要学 / 大白话 | 上游原文 | 官方/原始参考 | 专项模块 |
|---|---|---|---|---|
| O01 **LLMOps 评估与模型版本** | 发货前的质量关、发货后的售后检查都必须存在 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/06-production.md) · [原文2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/market/llm-demand-to-practice-20261029.md) | [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) · [EleutherAI lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) | [M10](../modules/M10.md)/[M11](../modules/M11.md) |
| O02 **Observability/Tracing** | 生产线上要能追踪哪一工位出错，不能只看到最后产品坏了 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/06-production.md) | [OpenTelemetry GenAI semantic conventions](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md) | [M09](../modules/M09.md)/[M10](../modules/M10.md)/[M11](../modules/M11.md) |
| O03 **安全/权限/隐私** | 服务员说我想进金库不构成开门凭证 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/06-production.md) · [原文2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/cross-cutting-planes.md) | [OWASP GenAI Security](https://genai.owasp.org/llm-top-10/) · [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | [M02](../modules/M02.md)/[M10](../modules/M10.md)/[M11](../modules/M11.md) |
| O04 **成本/反馈/构建或购买** | 买成品电器还是自己造，先算总成本和售后 | [原文1](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/06-production.md) · [原文2](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/market/llm-demand-to-practice-20261029.md) | [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework) | [M10](../modules/M10.md)/[M11](../modules/M11.md) |

## 横切链接（随时按需翻，不属于某个固定学周）

- [多模态完整贯穿 F/S/P/E/A/O](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/multimodal-vertical.md)：图像、音频、视频编码与融合、后训练/评测/安全；不同于只读一个 VLM 教程。
- [四条跨域支撑线](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/cross-cutting-planes.md)：Eval、Safety、Observability、Governance 从第一天贯穿。
- [带类型的关系规则](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/atlas/relationship-rules.md)：区分前置、供应、实现、优化、评测、对比，不画伪依赖。
- [Decoder-only 专项](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/README.md)：语言模型训练→推理→KV Cache 的更细概念。
- [真实推理可观测练习设计](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/projects/decoder-only-mini-inference/README.md)：Prompt→Tokenize→Prefill→Decode，需自己跑证据。
- [上游需求驱动学习机制](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/market/llm-demand-to-practice-20261029.md)：市场/求职或自选任务→能力缺口→实战→独立验收；历史需求不表示当前市场。
- [上游 Agent 调研](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-agent-learning-research-20261029.md) · [上游 RAG 调研](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-rag-learning-research-20261029.md) · [LLM AI 导师调研](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-llm-learning-research-20261029.md)：第三方学习资源有调研快照和限制说明，不应全部复制/安装。
- [RAG/Agent 客服交付链](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/playbooks/rag-agent-chatbot.md)：用于学习工程全景，但不是此专项仓必须服务的某个固定下游产品。

## 已特别联网核查的官方资料口径（不是依赖安装测试）

1. [Stanford CS336 Spring 2026](https://cs336.stanford.edu/) 提供 Data/Architecture/Systems/Scaling/Alignment 贯穿的真实作业，不必全部执行方可从某章学习。
2. [Hugging Face LLM Course](https://huggingface.co/learn/llm-course/en/chapter1/1) 覆盖 Transformers、Datasets、Tokenizers、Accelerate；[TRL](https://huggingface.co/docs/trl/index) 有 SFT/DPO/GRPO 训练分类。
3. [HF Agents Course](https://huggingface.co/learn/agents-course/en/unit1/introduction) 与 [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) 区分模型、工具、Agent state/workflow。
4. [MCP 2026-07-28 官方规范](https://modelcontextprotocol.io/specification/2026-07-28) 引入无状态核心，旧版本教程中的会话/握手行为不能直接套用。
5. [Ragas 官方指标](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/) 区分 RAG Faithfulness/Context Recall 与 Tool Accuracy/Goal Success。
6. [HF Multimodal](https://huggingface.co/docs/transformers/tasks/any_to_any) 覆盖 text/image/audio/video 的 any-to-any 任务，不能用纯文本 tokenizer 知识解释一切。
7. [vLLM 官方 Serving 文档](https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/) 明确模型服务协议不等于所有端点都自动受 API Key 保护；发布需加完整网关安全边界。

## 上游延伸阅读｜0–49 全栈覆盖矩阵与 Decoder-Only L3 细节（按需查阅）

**重要补充**：上游不只有六域 Atlas。还存在对原始 **0–49 个知识主题**的覆盖矩阵、带版本信息的技术来源注册表，以及 Decoder-Only 的多份 L2/L3 原理卡。它们是本仓 **33 个主题导航的更细或更广的证据层**，不是要求额外按 50 章重新学一遍。下表全部路径已对 2026-11-14 固定 Git 树核对。

| 上游资料 | 何时打开 | 
|---|---|
| [全栈 0–49 主题覆盖矩阵](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/source-coverage-matrix.md) | 上游对一套 0–49 号完整 LLM/多模态知识材料的覆盖检查，作为本仓 33 主题的广度补充；绝不能按编号等同 M01–M12 |
| [上游论文与官方文档版本注册表](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/registry.yaml) | 比纯 URL 更可追溯的论文 ID、发布日期/版本及上游历史核验日期；新引用需要重新核查 |
| [上游 Source Full Stack 主题索引](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/llm-full-stack.md) | 从解码器、后训练、推理服务、MCP 四块追溯原始源 ID |
| [Decoder-Only 知识总览](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/README.md) | 基础概念与更深单点说明，适合当前问题需要时跳入 |
| [自回归语言建模](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/causal-language-modeling.md) | 专业概率分解，解释“训练可以并行，推理逐 Token 生成”的缘由 |
| [Causal Mask 与 Autoregression](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/causal-mask-and-autoregression.md) | 为什么训练不应看未来 Token，如何导致 masking 错误 |
| [Transformer Block](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/transformer-block.md) | QKV/FFN/残差与 shape 拆解 |
| [Training vs Inference](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/training-vs-inference.md) | 同一自回归目标在训练和推理执行方式的差别 |
| [Prefill/Decode/KV Cache](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/prefill-decode-kv-cache.md) | 推理 TTFT/TPOT 的核心原理 |
| [现代 Attention/Position](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/modern-attention-and-position.md) | RoPE/GQA/MLA 与显存/注意力效率的边界 |
| [架构家族比较](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/knowledge/foundation/decoder-only/architecture-comparison.md) | BERT/T5/Decoder-Only，避免错误地把所有模型叫生成模型 |
| [Decoder-Only 深工程 Track](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/tracks/deep-engineering/decoder-only/README.md) | 了解实现/服务源代码细节的可选项目型资料 |
| [AI 原生 NLP 学习候选](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-nlp-research-20261029.md) | 更传统的 NLP/检索/表示学习知识拓展，当前任务需要时再读 |
| [AI 原生 ML/Deep Learning 学习候选](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-deep-learning-research-20261029.md) | 优化/训练基础缺口时的可选延伸，不强制回炉 |
| [强化学习学习候选](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/fdf2c09fc5cfbf4967d2507a66a3e19625482d7a/docs/sources/ai-native-rl-learning-research-20261029.md) | 不懂 Policy/Advantage 时可定位基础强化学习，不直接替代 TRL/verl 官方源码 |

**查阅纪律**：优先从当前问题的本仓需求卡进入；若要了解覆盖是否遗漏，查看 0–49 矩阵；若对一条公式或架构困惑，再打开对应 L3 卡；涉及最新版 API 则查官方发行文档。上游原文件保持唯一知识正文，不在专项仓重复粘贴。

## 更新与避免冲突的规则

- 上游原内容改动应检查 commit diff；本仓**只保存指针与课程实践**，不做全量复制。
- 上游历史资料、外部官方文档和个人实验记录的“证据等级”不同。外部项目的存在不证明已安装可用。
- 新增 LLM 全景知识点先更新 [机器可读目录](../index/upstream-knowledge-index.json) 并通过 [校验](../tools/validate_atlas.py)；新增需求案例到 [需求卡](../demand-driven/AI-NATIVE-NEED-ROUTES.md)。
- 如需同步跨域稳定解释，提给上游 Canonical Knowledge；本仓只维护 LLM 专项学习路线、可执行练习和能力验收。

## 专项更新：上游已有 RAG/Harness/Context/Prompt（固定快照）

本文件以上游历史 Git SHA **fdf2c09...** 固定六域宏观主题来源；应用工程另外核查了更新的上游提交 **59ea4e509507378860519d165113e21a9a9eb4d7**，其完整课程不复制到此仓：

- [RAG 练习与学习路线](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/practice/rag/README.md)。
- [Prompt Engineering 需求/课程](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/market/prompt-engineering-demand-to-practice-20261029.md)。
- [Context Engineering 需求/实验](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/market/context-engineering-demand-to-lab-20261029.md)。
- [Harness Engineering 专项](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/HARNESS-ENGINEERING-LEARNING-20261029.md)。

对应新 [本仓应用层 10 条专题索引](../application-engineering/index/README.md)、[专业/白话路线](../application-engineering/README.md)、[Ragas 评测](../application-engineering/RAGAS-EVALUATION.md)。**两个固定提交分别代表不同时间的资料来源，不是两个互相覆盖的知识主权副本。**
