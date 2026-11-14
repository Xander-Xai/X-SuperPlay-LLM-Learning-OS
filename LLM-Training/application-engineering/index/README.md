# 应用工程机器索引｜10 条横向技能专题，不扩增训练模块编号

> 这是 2026-11-14 资料与实践导航，包含 Prompt/Context/RAG/Ragas/Agent/Harness/MCP/Eval/Project/Security **10 条专题**。上游已存在的完整教程/研究链接使用固定 Git SHA；本仓维护关系、差异和教学纵切。**CURRICULUM_ONLY** 不代表实际模型执行或个人 L2/L4 达标。

## 日常查询

~~~bash
python LLM-Training/application-engineering/tools/route_application.py --search harness
python LLM-Training/application-engineering/tools/route_application.py --search 上下文
python LLM-Training/application-engineering/tools/route_application.py --id APP-RAGAS
python LLM-Training/application-engineering/tools/route_application.py --module M10
python LLM-Training/application-engineering/tools/validate_application_engineering.py
~~~

## 专题总表

| ID | 主题 | 本仓专业+白话讲义 | 训练模块关联 | 上游专项资料 | 官方来源 |
|---|---|---|---|---|---|
| APP-PROMPT | Prompt Engineering | [学习卡](../PROMPT-ENGINEERING.md) | [M02](../../modules/M02.md)、[M06](../../modules/M06.md)、[M10](../../modules/M10.md) | [固定 SHA 来源](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/market/prompt-engineering-demand-to-practice-20261029.md) | [官方](https://developers.openai.com/api/docs/guides/prompt-engineering) |
| APP-CONTEXT | Context Engineering | [学习卡](../CONTEXT-ENGINEERING.md) | [M02](../../modules/M02.md)、[M03](../../modules/M03.md)、[M10](../../modules/M10.md)、[M11](../../modules/M11.md) | [固定 SHA 来源](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/market/context-engineering-demand-to-lab-20261029.md) | [官方](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) |
| APP-RAG | RAG Engineering | [学习卡](../RAG-ENGINEERING.md) | [M02](../../modules/M02.md)、[M03](../../modules/M03.md)、[M10](../../modules/M10.md) | [固定 SHA 来源](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/practice/rag/README.md) | [官方](https://docs.langchain.com/oss/python/langchain/retrieval) |
| APP-RAGAS | Ragas Evaluation | [学习卡](../RAGAS-EVALUATION.md) | [M10](../../modules/M10.md) | [固定 SHA 来源](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/market/market-driven-rag-learning-loop.md) | [官方](https://docs.ragas.io/en/latest/getstarted/quickstart/) |
| APP-AGENT | Agent / Tool Calling | [学习卡](../AGENT-HARNESS-ENGINEERING.md) | [M06](../../modules/M06.md)、[M08](../../modules/M08.md)、[M10](../../modules/M10.md) | [固定 SHA 来源](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/market/agent-market-to-lab-20261029.md) | [官方](https://openai.github.io/openai-agents-python/testing/) |
| APP-HARNESS | Agent Harness Engineering | [学习卡](../AGENT-HARNESS-ENGINEERING.md) | [M06](../../modules/M06.md)、[M09](../../modules/M09.md)、[M10](../../modules/M10.md)、[M11](../../modules/M11.md) | [固定 SHA 来源](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/HARNESS-ENGINEERING-LEARNING-20261029.md) | [官方](https://cloud.google.com/discover/agent-harness) |
| APP-TOOLS | Tool/MCP Safety | [学习卡](../AGENT-HARNESS-ENGINEERING.md) | [M06](../../modules/M06.md)、[M08](../../modules/M08.md)、[M10](../../modules/M10.md) | [固定 SHA 来源](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/labs/harness-verification-sandbox-20261029/README.md) | [官方](https://openai.github.io/openai-agents-python/guardrails/) |
| APP-EVAL | Task / Trace Evals | [学习卡](../RAGAS-EVALUATION.md) | [M10](../../modules/M10.md)、[M11](../../modules/M11.md) | [固定 SHA 来源](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/assessments/ai-native-agent-rubric-20261029.md) | [官方](https://developers.openai.com/api/docs/guides/trace-grading) |
| APP-PRODUCTION | Project/Product/Production Engineering | [学习卡](../PROJECT-PRODUCTION-ENGINEERING.md) | [M09](../../modules/M09.md)、[M10](../../modules/M10.md)、[M11](../../modules/M11.md) | [固定 SHA 来源](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/market/market-driven-rag-learning-loop.md) | [官方](https://openai.com/index/harness-engineering/) |
| APP-SECURITY | Application Security/Injection | [学习卡](../PROJECT-PRODUCTION-ENGINEERING.md) | [M02](../../modules/M02.md)、[M10](../../modules/M10.md)、[M11](../../modules/M11.md) | [固定 SHA 来源](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/59ea4e509507378860519d165113e21a9a9eb4d7/docs/labs/harness-verification-sandbox-20261029/README.md) | [官方](https://genai.owasp.org/) |

## 与现有三套索引的关系

- [六域 33 个宏观主题](../../index/upstream-knowledge-index.json)：全栈世界观和知识关系；
- [训练 12 模块/19 需求](../../index/learning-index.json)：预训练、后训练、模型工程实战；
- [基础 90 概念](../../index/foundation-coverage.json)：数学/Tokenizer/架构/系统细颗粒学习；
- **此处 10 个应用专题**：应用运行时横切能力，不改 M01–M12 编号、不向上游添加第二份市场事实。

## 统一口径

RAG ≠ Ragas；Harness Runtime ≠ lm-evaluation-harness；Prompt ≠ Context；Tool Calling/MCP ≠ Server Authorization；学习等级 [L0–L4](../../assessments/CAPABILITY-RUBRIC.md) 和 [生产 G0–G8](../../production/PRODUCTION-READINESS.md) 互不替代。
