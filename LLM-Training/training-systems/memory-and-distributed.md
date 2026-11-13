# M09 训练系统工程：显存、Profile 与工业 RL 架构

## 单卡显存模型

粗略拆分：M_total ≈ M_weights + M_gradients + M_optimizer + M_activations + M_KV_cache + M_temporary + M_framework。混合精度、Master weights、bitsandbytes 状态、重计算和 KV Cache 复用都会改变具体口径。**训练显存不能仅按参数量 × 2 bytes 估算**。

首选测量：[PyTorch CUDA memory](https://docs.pytorch.org/docs/stable/notes/cuda.html) 与 torch.cuda.max_memory_allocated / max_memory_reserved；搭配 PyTorch Profiler 与 CUDA 内存快照，区分 allocated/reserved、峰值和碎片化。记录是否存在 CPU offload、checkpoint、flash attention、量化等优化。

## 分布式概念对照（了解原理即可，本机不必造多卡集群）

| 方式 | 核心 | 代价 |
|---|---|---|
| DDP | 每个 rank 完整参数、聚合梯度 | 模型状态复制 |
| ZeRO-1 | Shard optimizer | 更多通信/调度 |
| ZeRO-2 | + Shard gradients | 通信与分片管理 |
| ZeRO-3 | + Shard parameters | 参数聚合开销 |
| FSDP | 按策略 Shard model state | all-gather / reduce-scatter |
| TP | 同一层按张量切 | 强带宽通信 |
| PP | 按层切成阶段 | bubbles / microbatch 调度 |
| CP | 序列上下文切分 | Attention 跨设备通信 |
| EP | MoE experts 分片 | 路由和 all-to-all |

进一步研究 NCCL collectives、计算/通信重叠、activation recompute、长序列策略和 kernel fusion。

## 工业 RL 基本架构

~~~mermaid
flowchart LR
  Task["Task / Prompt queue"] --> Rollout["Rollout Workers: vLLM / SGLang"]
  Rollout --> Verify["Reward / Tool Execution / Verifier"]
  Verify --> Buffer["Trajectory / Logprobs / Advantages"]
  Buffer --> Actor["Training Workers: FSDP / Megatron"]
  Actor --> CKPT["Weights / Checkpoint"]
  CKPT --> Sync["Weight synchronization"]
  Sync --> Rollout
  Controller["Controller / Resource scheduling"] -.-> Rollout
  Controller -.-> Actor
~~~

**核心理解**：推理 Rollout 与参数更新可以分离部署，使用不同批量、计算模式和 GPU 资源；也可在单卡或同 GPU 上分时/共享显存。要解释每次策略更新后权重如何同步、版本滞后带来的 off-policy 问题、参考模型或奖励模型如何占资源。

资料：[PyTorch FSDP2](https://docs.pytorch.org/docs/stable/distributed.fsdp.fully_shard.html) · [DeepSpeed ZeRO](https://www.deepspeed.ai/tutorials/zero/) · [verl](https://github.com/volcengine/verl) · [OpenRLHF](https://github.com/OpenRLHF/OpenRLHF) · [Megatron Core](https://github.com/NVIDIA/Megatron-LM)。

## 部署与 Agent 集成验收

LoRA adapter/merge 与模型权重版本可追溯；必要时量化；vLLM 兼容 Qwen 工具模板和 token 格式；记录 GPU 显存、TTFT、tokens/s、P95、并发、工具解析与执行成功、引用正确性。不能只以“服务启动成功”验收。

