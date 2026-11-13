# 大模型训练面试：追问式题库

> 按“专业定义 → 大白话 → 公式/代码 → 实践证据 → 限制与取舍”五步作答。实验未运行时不要把预期结果表述成项目成果。

## 基础与预训练

1. 为什么 Decoder-only 模型使用 Causal Mask？张量维度如何变化？
2. 输入和标签的 shift 通常在哪里执行？Double shift 会怎样？
3. RoPE 如何影响 Q/K？RMSNorm 与 LayerNorm 有何不同？
4. AdamW 的一阶/二阶矩如何更新？与 weight decay 解耦有什么意义？
5. 为什么 Train Loss 下降却不能保证问答能力更好？
6. 预训练 Token 数、模型参数、上下文长度和 FLOPs 如何权衡？
7. 仅保存 model weights 能否精确恢复训练？还需要哪些状态？

## CPT、SFT、PEFT

8. CPT 与 SFT 哪些地方使用相同的损失？如何解释差异？
9. 什么是灾难性遗忘？Data Replay 如何设计公平对照？
10. WSD 与 Cosine 有什么不同？你如何验证效果？
11. LoRA 的 ΔW=BA 如何减少可训练参数？rank、target modules 如何影响容量？
12. QLoRA 底座是 4-bit 时，训练过程哪些参数仍在更新？
13. 在 system/user/assistant(tool_call)/tool/assistant(final) 中如何构造 Loss Mask？
14. 为什么不能随便为每个工具标记增加新 special token？

## 数据与偏好

15. 合成 SFT 数据怎么验证真实性？如何防训练测试泄漏？
16. Rejection sampling/RFT 与在线 RL 的不同在哪？
17. 为什么 Chosen/Rejected 不是越多越好？如何去重和检查标签质量？
18. 固定的 SFT 自采样数据是否仍然是在线 DPO？为什么？
19. DPO 的 reference model、beta、chosen 和 rejected log-probs 起什么作用？

## RL 与系统

20. GRPO 为什么同题采样多条回答？组内奖励全相同时怎么办？
21. Advantage、Reward、KL 与 Clipping 分别解决什么问题？
22. 为什么 Reward 上升、输出变长不一定是推理能力进步？
23. 单卡 16GB 运行 GRPO，最可能 OOM 的对象有哪些？回退顺序是什么？
24. DDP、ZeRO-1/2/3、FSDP 分别切分什么？
25. verl 中为什么将 Rollout 与 Actor 训练拆开？权重同步会带来什么问题？
26. Pretrain/QLoRA/SFT/DPO/GRPO 各有什么不同的核心评估指标？
27. 如何用同一套测试证明 Tool Calling 微调改善了真实业务，而不是改变了 Prompt？

## 模拟面试验收

每题记录 0–2 分：定义正确、技术原理、可复现实例、边界条件。总分 8 分；6 分及以上视为基本掌握，以下应回到对应模块补实验。

