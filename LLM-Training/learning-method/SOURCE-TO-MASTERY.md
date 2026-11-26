# Source-to-Mastery｜LLM 资料学习与知识内化适配

> **定位：专项适配，而非第二套方法论。** 上游权威为 [AI-Learning-OS Source-to-Mastery](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/main/docs/learning/source-to-mastery.md) 和 [METHODOLOGY](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/main/METHODOLOGY.md)。本仓沿用 [AI-Native 学习闭环](AI-NATIVE-LEARNING-LOOP.md)、[LLM L0–L4 Rubric](../assessments/CAPABILITY-RUBRIC.md)、[需求卡](../demand-driven/DEMAND-CARD-TEMPLATE.md) 与 [实验记录](../experiments/EXPERIMENT-TEMPLATE.md)。
>
> **状态：GUIDE / EXAMPLES_NOT_RUN。** 以下只设计学习方法和示范练习，不代表用户已闭卷答题、执行 GPU 训练、完成 Agent 真模型测试或达到个人能力 PASS。

## 前置目标质询（Grill Me）

简单定义或代码解释直接回答。复杂路线、批量学习或指定训练/Agent 方案但目标不明时，先问真实目的、时间、现有能力证据和最低可验证结果；判断是否需要训练、新框架或完整课程，给出可逆基线与机会成本。每轮只问影响结果的关键问题，已有资料自行核实；确认目标 L0–L4、单一 Gap、实验预算及 Stop Rule 后进入既有学习闭环。主动 Grill Me 则深度质询，已确认任务不重复问。原 M01–M12、Rubric、实验和进度权威不变，不把 AI 代做视为本人掌握。

## 1. 外部资料与实际需求，双入口汇合

~~~text
岗位 / 项目 / Bug / 研究问题 ──┐
                            ├→ 目标与基线 → 初诊 Gap → LLM 六域/知识节点 → AI-Native 学习闭环
好博客 / 论文 / 官网 / 教程 ───┘                                    ↓
                                       自己解释 → 最小练习 → 负例/受控对照
                                                              ↓
                                       独立验收 → 增量知识/来源 → 延迟迁移
~~~

- **资料驱动可以合法探索**：标注 `SELF_CHOSEN`，不因没有客户或岗位就拒绝学习；同时明确目标、预算、来源可靠性和 Stop Rule。
- **需求驱动优先解决问题**：若现成 API/RAG/规则足够，先做无训练基线；不因为看到优秀的训练论文就强行选择 SFT/GRPO。
- **所有学习仍回原体系**：用 [需求路由](../demand-driven/README.md)、[六域知识地图](../knowledge-graph/LLM-FULL-STACK-ATLAS.md)、[能力单元](SIX-CAPABILITY-UNITS.md) 选择已有节点，不新设 M13、第二个学习进度表或第二个 Mastery Level。

### 学习到哪一层就够？（只使用本仓 L0–L4）

| 本次目的 | 建议目标 | 可观察的最低结果 |
| --- | --- | --- |
| 查参数 / 定义 / 临时排错 | L0–L1 或任务已解决即止 | 能定位准确版本、解释相关输入输出、问题解决证据 |
| 读懂技术文章与机制 | L1 | 关闭资料后解释专业机制、白话解释和适用边界 |
| 深入使用源码 / 训练机制 | L2 | 自己改动最小实现，复现实验并记录版本、输出 |
| 分析模型效果或工程失效 | L3 | 基线、两个不同类别负例、受控对照和诊断证据 |
| 应对陌生任务 | L4 | 独立迁移/修复并解释取舍；生产仍另经 G0–G8 |

**本仓等级含义与上游主仓不是逐字相同的量表**；以本仓 [Rubric](../assessments/CAPABILITY-RUBRIC.md) 为唯一评分依据，不做等级数字直接换算。课程文档、Toy 单测、模型训练与个人独立能力的状态必须分别记录。

## 2. 每学一篇资料，执行五个动作

### A. 定目标、建立轻量地图（AI 导航）

先写：这篇材料解决什么问题？为什么值得学？想达到本仓 L 几？现有哪一个 M01–M12 / Agent / RAG 节点最相关？已有 Lab 是否足够？什么情况停止？

登记**标题/作者、原文 URL、发表与访问日期、模型/框架/规范版本、值得验证的观点**。旧论文的实验结论不自动等于当下官方 API 的行为；对当前协议参数以官方对应版本为准。

AI 帮你整理 3–8 个节点的地图即可，不要求翻译全文或复制作者整篇摘要。先查 [资源角色分工](../resources/TRAINING-SOURCE-ROLES.md) 与 [权威原始资料](../resources/AUTHORITATIVE-INDEX.md)，避免同义重复。

### B. 带问题精读、闭卷提取（AI 考官）

只读一个小节，回答三个问题：

1. 作者解决了什么失败或瓶颈？
2. 机制如何作用于数据/张量/损失/运行时状态？为什么可能有效？
3. 这里的证据支持多大范围的结论？替代方案或边界是什么？

阅读时只记“问题、关键原文定位、待验证主张”。**关掉页面和 AI 完整答案**，再自己解释、画流转图、写最小公式、预测代码输出。AI 对缺口按方向→定位→局部提示→完整示例渐进辅助；接受提示的尝试不得伪装为完全独立考试。

### C. 最小实践（复用本仓实验，不为每篇文章新造项目）

- **理解原理**：手算小张量或在 [TinyGPT](../labs/tiny-gpt/README.md) 预测/修改 Mask、Shift、Loss。
- **训练论文**：先用数学或 CPU Toy 复核机制，再按 [实验 01–05](../experiments/README.md) 设计受控对照；真模型 GPU 未运行就保持 `NOT RUN`。
- **LLM 应用博客**：复用 [Agent Loop](../application-engineering/labs/MINI-AGENT-LOOP.md)、[RAG 实验](../application-engineering/rag-deep-dive/LABS.md) 或对应知识节点。
- **官网/API**：用精确版本、短例子解决当前问题即可，不强制写复杂 Demo。

亲自输出可观察结果，并留可复核的模型/代码/数据版本、命令、输入、预期和实测；纯纸面设计须标明未执行。

### D. 主动找反例、做失败归因

按场景选至少两个**适用**的不同类别问题；如 Mask 位置错误、数据泄漏、OOM、越权 Tool Call、检索无证据、Reward Hacking 或不公平对照。

记录：**触发条件 → 预期 → 实际 → 根因/替代解释 → 修复/对照 → 复测**。

“论文提到会失败”不是“我已踩过这个坑”；单纯生成测试脚本也不代表真正运行成功。实验仍受 [能力 Rubric](../assessments/CAPABILITY-RUBRIC.md) 的真实性、独立性与受控比较门槛约束。

### E. 增量沉淀 + 间隔复测

把内容分开存放，而不是一篇文章产生一整套平行课程：

| 类型 | 记录在哪里 | 不应该混淆什么 |
| --- | --- | --- |
| **Source**：原文主张、版本、争议 | 既有 [来源索引](../resources/AUTHORITATIVE-INDEX.md)、对应专题 SOURCES 或 [论文阅读清单](../papers/READING-LIST.md)，只登记真正新增且适用的来源 | 作者原话 ≠ 最新官方规范 |
| **Knowledge**：自己的闭卷理解和机制 | 既有 M 模块、Agent/RAG 专题、知识图的相关段落；增量补充并回链来源 | AI 摘要 ≠ 我已经理解 |
| **Practice / Evidence**：个人实现、日志、失败修复 | [需求卡](../demand-driven/DEMAND-CARD-TEMPLATE.md) + [实验模板](../experiments/EXPERIMENT-TEMPLATE.md) + 原代码目录 | CI Toy PASS ≠ 实际 GPU 或本人独立 PASS |
| **Progress**：学习与考核状态 | 唯一 [learning-progress](../learning-progress.md)，按原 Rubric 真实更新 | 资料新增 ≠ 进度升级 |

不是所有查阅都应创建新文件：短资料只留引用或解决结果即可。按本仓已有学习闭环进行当日闭卷、约 1/3–4/7 天抽问与陌生迁移，间隔依遗忘和任务调整。目标完成即停止本轮。

## 3. 两种具体示范（均未执行个人学习）

### 案例一：Lilian Weng 的 Agent 综述 → Tool Use

- **Source**：Lilian Weng, *LLM Powered Autonomous Agents*（2023-06-23）：https://lilianweng.github.io/posts/2023-06-23-agent/ ；作为历史研究综述，不直接等同于今天的 MCP / Function Calling 规范。
- **路由**：先去 [Agent 深学](../application-engineering/agent-deep-dive/README.md) 对照既有 Tool / Loop 知识，再从 [M06](../modules/M06.md) 理解 Tool-Calling 数据/模板的训练侧角色。
- **闭卷题**：“模型提出 Tool Call”和“代码校验权限后执行”为什么必须分开？
- **最小实验**：优先读/改 [Mini Agent Loop](../application-engineering/labs/mini_agent_loop.py)，选择错误参数、工具超时和越权中的两个可测试负例，记录真实运行结果。
- **验收**：按 L0–L4 目标执行；不把 2023 年原文与后续自主形成的工程结论混写为同一来源。

### 案例二：读 GRPO 论文或 TRL 文档 → 学会做对照

- **路由**：[M08](../modules/M08.md) → [GRPO 数学 Toy](../labs/preference-rl-math/README.md) → 真模型需要时才到 [实验 05](../experiments/05-grpo/README.md)。
- **闭卷题**：组内奖励相同或方差接近零时，会如何影响 Advantage？为何 Reward 变高不等于任务正确率提高？
- **最小验证**：在已有数学实验上先预测奖励分组的行为，再用不同奖励/长度偏差形成反例；若要声称真实模型收益，必须有相同预算基线、held-out 任务指标和实际模型日志。
- **沉淀**：更新已有 M08 解释和对应实验记录，不再建一份“GRPO 博客完整抄录”。

## 4. 可复制给 AI 导师的起手式

> 我提供一篇【博客/论文/官网/教程 URL】。请遵循 [本仓 AI-Native 学习闭环](AI-NATIVE-LEARNING-LOOP.md) 和 [Source-to-Mastery 上游方法](https://github.com/Xander-Xai/X-SuperPlay-AI-Learning-OS/blob/main/docs/learning/source-to-mastery.md)：先确定我为什么学、当前已有能力、目标 L0–L4 与 Stop Rule；判断来源的发表时间和版本，定位本仓 M01–M12/Agent/RAG 已有模块与实验。一次只学一个 Gap，让我先用自己的话闭卷解释或预测行为，再给纠错/逐级提示。按需给最小实验、两类负例及受控对照，明确 AI 参与范围；没有运行证据写 NOT RUN。最终只建议更新已有来源/知识/需求卡/实验与 learning-progress，不新设等级和进度表，也不替我宣布个人考试 PASS。

**一句话：用上游学习内化流程选择和消化材料，用本仓的既有模块、实验、Rubric 和唯一进度表证明自己真正掌握。**
