# V3 第三轮严格审计与补全（2026-11-14）

> **历史快照，非 2026-11-14 最新词条覆盖统计**：本报告当时计数如“18 条需求”是创建时记录，当前依照 [19 条专项需求](index/learning-index.json)、[90 条基础词条](index/FOUNDATION-COVERAGE.md)与 [最新一致性验收](ACCEPTANCE-FOUNDATION-CONSISTENCY-20261114.md)。请勿把历史阶段数据当作今天的完整索引数。

> **本报告是课程资产验收，不是学员技能、真实模型训练或产品上线的验收。** 检查 GitHub 当前 main 的 V3 Roadmap、模块、索引、课程源码与上游双向链接；本次差距修复通过 PR 提交，实际合并与 CI 结果以 GitHub PR 最新提交记录为准。

## 1. V3 初次合并后发现的三项真实不足

| 初次状况 | 问题 | 本轮修复 |
|---|---|---|
| 各 M01–M12 页面多数约千字节 | 只有知识点/任务清单，没有对单个业务问题的深度机制、白话解释、具体失败案例与模块级引用 | 为全部 12 模块新增“需求触发、机制输入输出、大白话类比、最小可做实验、负例、官方来源、模块联系和验收门槛” |
| learning-index 只有 12 模块标题和 18 个问题的简单匹配 | 无模块级 sources/practice/questions/gates；中英同义词、模块反向查找及循环依赖未验证 | 每模块新增 sources、practice、question、gates；18 需求加 aliases；路由支持 --module 反查；索引检查增加来源、练习、状态、环依赖、别名与反向索引单测 |
| 实战可执行覆盖仅 Loss Mask 和 Tool Gateway | DPO/GRPO 和评估概念依赖看图/纸面描述，不能直接动手确认公式/分母与奖励漏洞 | 增加 [DPO/GRPO 数学沙盒](labs/preference-rl-math/README.md) 与 [16 条合成 Agent 任务评估](labs/task-evaluation/README.md)，每个都有可运行脚本、负例测试、限制说明和深入下一步 |

## 2. 验收范围

| 项目 | 预期检查 | 证据来源 |
|---|---|---|
| 两仓分工 | 上游继续保留知识 Atlas；专项 M01–M12 独立，历史 M00–M17 不按数字互换 | [上下游索引](index/UPSTREAM-DOWNSTREAM.md) |
| 知识深度 | 12/12 每模块都有 V3 深入讲解、独立实验、来源与失败样例 | [模块入口](README.md) |
| 完整覆盖 | 4 里程碑、5 类训练实验、独立部署验收仍保留 | [Roadmap V3](ROADMAP-V3-DEMAND-DRIVEN.md) / [V2](ROADMAP-V2.md) |
| 需求检索 | 18 需求可关键词/别名/模块反查；没有命中时明确说明 | [CLI](tools/route_learning.py) / [机器索引](index/learning-index.json) |
| 权威参考 | 12 模块均通过 ID 绑定权威来源；关键 TRL mask 和 FSDP2 细节补充官方资料 | [资料库](resources/AUTHORITATIVE-INDEX.md) |
| 可运行学习资产 | 除既有 CPU mask/tool gateway 外，新增 DPO/GRPO 数学练习和指标评估 | [Labs](labs/capability-ladder.md) |
| 工程上线覆盖 | 正确性/数据/权限/性能/监控/回滚/反馈的 G0–G8 仍在 | [生产门禁](production/PRODUCTION-READINESS.md) |

## 3. 严格禁止夸大

- 新增后训练数学脚本只计算公式和示例 Reward；**没有 TRL 训练、Rollout、策略梯度反向传播或 Qwen checkpoint**。
- 新增评估脚本只读取预先标注的合成字段，**没有真实 LLM/Judge/引用校验/线上流量或 P95**。16 条样本只用于教学，不能主张真实准确率。
- 现有合成 Tool Gateway 只模拟系统授权边界；不是已接生产认证、重试幂等和客户数据的部署系统。
- 因此 MiniMind/Qwen CPT/SFT/DPO/GRPO 的 GPU 实验和生产发布依旧为 **NOT RUN / UNVERIFIED**。
- 部分关键官方文档已抽查；**没有开展全仓所有 HTTP 外链可用性巡检**。代码/库的版本兼容须由实际运行时另外确认。
- **CI 绿灯是课程资产正确性，不是学员独立掌握或业务结果**。

## 4. 最终验收记录填写规则

合并前：请查看本次 PR 最新 SHA 对应的 GitHub Actions 工作流（docs 与 cpu-toy 两个 Job），检查必需文件、相对链接、索引与两种新实验单测，检查失败必须先修复。合并后：读取 main 下此文档与新增源码，核对 main SHA。没有实际检查结果不要编造 Success 数值。

## 5. 下一步不是继续堆课程

从 [按问题检索](demand-driven/README.md) 选一个现实任务，例如 Tool-SFT Mask、vLLM P95 或 GRPO Reward Hacking，先运行最低成本基线，逐层完成可复现代码、任务级评价、陌生场景迁移；如要真实上线，再到各自实际项目仓验收 G0–G8。无需从 M01 按顺序学到 M12。
