# 2026-11-14 严格复验｜六域课程、知识关系与官方实现边界

> 本报告是学习资产验收计划与逐条可复核证据来源，不能替代任何模型真实训练、生产负载或学习者独立能力评估。当前 PR 的 CI 完成状态应以该 PR 最新 HEAD 对应的 GitHub Actions 为准；验收后最终确认 main 分支 SHA。

## 一、已核查的事实

- 连接 GitHub 主仓（2026-11-14）检查 [LLM 专项](https://github.com/Xander-Xai/X-SuperPlay-LLM-Learning-OS) 与 [AI 学习上游](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS) 的 main、文件树、双向索引和 12 模块。上游有 841 份仓库文件，专项仓原有 90 份仓库文件；这是文件数，不是课程质量指标。
- 原课程的 **12 模块、六域地图、33 个索引主题、30 个类型关系、12 个跨域需求入口、21 个官方/原始来源目录** 均存在；此外原 M01–M12 的训练实验手册仍保留。
- 上游固定 SHA 与历史 0–49 原始主题矩阵的关系已明确。历史来源有可能与最新版不一致，不等于需要重新学习 50 个章节。
- 抽查官方入口包括 [Stanford CS336](https://cs336.stanford.edu/)、[HF LLM Course](https://huggingface.co/learn/llm-course/en/chapter1/1)、[HF Agents Course](https://huggingface.co/learn/agents-course/en/unit1/introduction)、[TRL Chat Templates](https://huggingface.co/docs/trl/chat_templates)、[TRL GRPOTrainer](https://huggingface.co/docs/trl/grpo_trainer)、[vLLM API](https://docs.vllm.ai/en/latest/serving/online_serving/openai_compatible_server/)、[MCP 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28)、[Ragas](https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/)、[LangGraph](https://docs.langchain.com/oss/python/langgraph/overview)、[HF Multimodal](https://huggingface.co/docs/transformers/tasks/any_to_any) 与 [OpenTelemetry GenAI](https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-spans.md)。这是有界的页面抽样，不是 21/21 外链可达证明。

## 二、发现并修复的实际差距

| 缺口 | 修复动作 | 不声称什么 |
|---|---|---|
| 有 30 条关系边，但 CLI 只能按关键词输出孤立主题 | 增加 --relate 查看入边/出边和 --path 两点间最短关联路径，逐边输出原始关系方向；添加正常/异常单测及 CI smoke | 无向图遍历 ≠ 学习先修关系/全知语义搜索 |
| 官方运行时有影响上线的新版细节 | 将 Tool SFT generation mask、GRPO Tool Prefix-Preservation + rollout/训练一致性、vLLM HTTP 鉴权限制、MCP stateless 协议升级并列为按需求检索的专项卡 | 文档核查 ≠ 在 GPU/服务器上实际配置和实测 |
| 生产手册中 20 产品/20 文档/30 测试是计划，但容易被读成已完成 | 写明真实合成工具网关 fixture 实际 **2 产品/2 文档**；任务评测 fixture 实际 **16 个预标注样本**；20/20/30 仅为待执行扩展 | 玩具测试 ≠ 真实客户场景或生产质量 |
| 之前的验收报告残留“仍需查看当时 PR CI”的临时措辞 | 增加正式后续复验引用，避免新读者把历史 PR 状态误读为当前状态 | 本次合并必须以最新 PR/主分支重新核对 |

## 三、自动化验收（本报告写入时尚未确认最新 PR CI）

- 运行 check_repo.py 检测相对 Markdown 链接、所有 12 模块深度标记和新的必需文件；
- 运行 validate_atlas.py、validate_learning_index.py；
- 运行原有 Atlas、learning-index、DPO/GRPO 数学、合成 Tool Gateway、任务评测单测以及 CPU Torch Toy；
- 新增关系反查单测：A04 出边/入边、A04→O02 的**无向关联**路径，原始关系方向不被篡改；未知 ID 时明确无结果；
- 合并前必须确认 GitHub Actions docs 和 cpu-toy 都成功，新增相对 Markdown 链接无断链；
- 合并后再次读取 main 下本文件、关系工具与官方风险卡，确认被实际落盘。

## 四、仍未通过的真实能力验收

**MiniMind / Qwen 真实 Pretrain、CPT、SFT、DPO、GRPO、16GB 训练显存、vLLM 负载和 Agent 真实端到端任务性能均未在本次核查中运行。** 需要单独选择需求、固定环境、运行真实实验、保存日志，不能以课程 CI 绿灯冒充。
