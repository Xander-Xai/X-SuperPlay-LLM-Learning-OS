# 学习进度、里程碑验收与下次行动

状态定义：NOT STARTED / IN PROGRESS / READY FOR REVIEW / VERIFIED。**文档落盘不等于训练已跑通**。

| 阶段 | 状态 | 验收依据 | 证据路径 |
|---|---|---|---|
| Roadmap 与课程设计 | VERIFIED (DOCS ONLY) | 12 模块、4 阶段、官方资源、实验规范 | ROADMAP-V2.md |
| 01 MiniMind 白盒 | NOT STARTED | 模型组件对照 + Pretrain/SFT + Mask | experiments/01-minimind-whitebox/ |
| 02 Qwen CPT | NOT STARTED | Base/Domain/Replay + 调度器对照 | experiments/02-qwen-cpt-replay/ |
| 03 Agent Tool SFT | NOT STARTED | 生成/验证数据 + LoRA/QLoRA 对照 | experiments/03-agent-tool-sft/ |
| 04 DPO | NOT STARTED | 外部 vs 自采样离线偏好数据对照 | experiments/04-dpo/ |
| 05 GRPO | NOT STARTED | 真实 Rollout + Reward/Accuracy/Length/KL 记录 | experiments/05-grpo/ |
| 06 部署 | NOT STARTED | Profiler + vLLM + Agent 端到端回归 | experiments/06-deployment/ |

**学习资料验收见 [ACCEPTANCE-V2](ACCEPTANCE-V2.md)：文档合规通过不代表训练实验通过。**

## 四个阶段退出门槛

- [ ] **阶段一**：能追踪一个 batch 的完整参数更新；张量/Mask 测试、Checkpoint 和独立验证曲线存在。
- [ ] **阶段二**：CPT 防遗忘和学习率对照、Agent 合成数据版本、SFT 效果对照全部留痕。
- [ ] **阶段三**：同源 SFT 分叉的 DPO/GRPO 对照，包含真实正确率和 Reward hacking 检查。
- [ ] **阶段四**：训练/推理资源剖析、verl 等架构理解、vLLM/Agent 端到端结果。

**补充静态 QA**：[学习资料目录/相对链接自动检查](tools/check_repo.py)；[CPU 教学单元测试](labs/README.md)（不替代 GPU 训练）。

## 第一个实际任务（无需另外造项目）

1. Clone MiniMind，记录 SHA、版本、CUDA 环境与模型配置。
2. 用一条固定 toy batch 跟踪 input_ids、Logits、Labels、CE Loss，明确 shift。
3. 在 MiniMind 原实现旁复写最小 RoPE/RMSNorm/SwiGLU/Attention 测试，并记录误差。
4. 按 [实验模板](experiments/EXPERIMENT-TEMPLATE.md) 建立第一次实验记录，再执行 Pretrain 和 SFT。

默认学习节奏：第一周白盒基础，第二周 SFT/Mask，第三周 CPT，第四周真实 Agent SFT，第五周 DPO，第六周 GRPO，第七周部署与复盘；如任务或面试需求变化，按依赖图跳学，**以验收结果而不是日期作为完成标准**。

## 记录行为

每次学习后补充：已解决的问题、还不理解的依赖、下一次最小任务、真实实验路径；避免提交仅由推测构成的“PASS”。

