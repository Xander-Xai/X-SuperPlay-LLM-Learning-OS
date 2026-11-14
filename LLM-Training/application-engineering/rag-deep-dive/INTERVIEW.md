# RAG 面试答辩：12 问、追问与证据卡

[学习导航](README.md) / [知识点](CORE-01-05.md) / [评测与生产](CORE-06-10.md)。

回答格式统一：**问题背景（10s）→ 为什么选方案（20s）→ 底层原理（20s）→ 实验证据（20s）→ 失败边界（10s）**。这是演练结构，不代表已验证个人真实简历指标。

| 题 | 回答必须包含 | 追问或误区 |
|---|---|---|
| 1. 从上传 PDF 到回答的完整链路？ | 解析/Chunk/元数据/索引、用户身份、路由、ACL、召回、排序、context、生成、引用、评测 | 离线版本切换、扫描页如何保留源页码 |
| 2. Chunk 大小如何选？ | tokenizer、结构边界、父子块、overlap、Gold Set 消融 | 为什么 overlap 过大损害去重与成本 |
| 3. Embedding 为何可语义检索？ | Encoder、Pool、对比学习、Cosine、负例、模型修订 | 不同模型向量维数能混合搜吗 |
| 4. BM25 与 Dense 如何取舍？ | 倒排与 tf/idf vs 向量相似、编码/同义词场景 | 为什么产品编号需保留 lexical |
| 5. HNSW 索引过程？ | 多层图、M、efConstruction、efSearch、FLAT 真值 | 为什么调参要同时看 Recall/内存/P95 |
| 6. RRF vs CrossEncoder？ | 名次融合公式 vs Query/Doc 联合打分、候选成本 | 为什么原始 BM25 分数不能直接与 cosine 相加 |
| 7. Rewrite 为什么可能变差？ | 语义漂移、错指代、原 Query 保留、并行消融 | “在欧盟呢”如何恢复原成分 |
| 8. Recall/MRR/nDCG 区别？ | Gold 单元、排序位置、相关性级别、分母 | Gold 为空的拒答例怎么计分 |
| 9. 找对证据仍然答错？ | Context 裁剪、事实冲突、Prompt、Claim/citation check | Faithfulness 高是否说明法律答案正确 |
| 10. 多租户和版本如何设计？ | 服务器权限、过滤、引用读取、缓存键、撤权/索引版本 | 为什么不能只依赖 Prompt |
| 11. P95 飙升如何查？ | trace 分阶段、候选数、Rerank、模型队列、Token | 先加卡还是先找到瓶颈 |
| 12. GraphRAG/Agentic RAG 何时用？ | 多跳关系/动态检索需求、复杂度与成本门槛 | 为什么单跳 FAQ 不应该无条件上 Agent |

## 真实项目映射清单（自行补充事实，不自动造数）

候选架构示例：OCR → BGE 文本索引、CLIP 图像索引 → ES+Milvus → RRF → CrossEncoder → Evidence Gate → LLM → Answer Gate。回答时应说明这只是架构示意：CLIP/BGE 不是直接共享同一向量空间；没有回放证据不声称所有门禁已经防攻击或“生产级”。

每一题至少准备一张：
- **设计目标**：用户问题/业务风险，怎么定义“正确”。
- **选型证据**：版本和 alternatives（BM25-only、Dense-only、混合、长上下文、SQL）。
- **性能指标**：N/K、Recall@K、误答、误拒、P95、成本，记录真实日志来源。
- **负例**：一个错误检索/生成案例、一个权限/过期/缓存反例。
- **修复证据**：单一变量改变前后样本、分析局限。
- **状态**：NOT RUN / PASS / FAIL / INCONCLUSIVE；未运行的数据直接标未知。

闭卷提问后按 [L0–L4 Rubric](../../assessments/CAPABILITY-RUBRIC.md) 验收，禁止把“能背出 12 问”视为 L4。
