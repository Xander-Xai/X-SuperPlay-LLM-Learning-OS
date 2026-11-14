# 可运行的“工具调用→证据→安全边界”纵切实验

> 状态：**SYNTHETIC LAB / NO MODEL TRAINED / NO DEPLOYMENT CLAIM**。无需下载 Qwen、无 CUDA、无生产账户或真实企业数据。此练习的价值在于验证**模型输出不可信、工具执行要隔离、最终结构化答案必须来自证据**这三个系统级原则。

## 运行（标准库，Python 3.10+）

在仓库根目录执行：

```bash
python LLM-Training/labs/synthetic-tool-gateway/run_demo.py
python -m unittest discover -s LLM-Training/labs/synthetic-tool-gateway -p 'test_*.py' -v
```

单测覆盖：合法公开库存、staff 访问、guest 越权、未授权工具、额外参数、未知商品、伪造库存、伪造引用、模型伪造 role、trace 脱敏结构以及示范模式标记（共 11 项）。

## 学习的边界和下一层

```text
模型/规则生成的 tool call（本例是固定假输出）
      ↓
授权角色（必须来自已认证系统，不来自模型）
      ↓
tool allowlist + 参数严格校验
      ↓
只读 inventory / docs 的合成工具
      ↓
结构化库存和引用 ID 对照验证
      ↓
仅供学习的 trace 与测试结果
```

**这不是实际 LLM/Agent**：没有调用模型，也没有做自然语言 claim-level support check、真实 Web API、持久状态、超时重试、认证系统或高并发。若据此写“已上线企业客服/真实 RAG 通过验收”，属于错误结论。

## 逆向学习提示

- 为什么 guest 不能查询私有 B？对应 M06 Tool Call 边界和 [生产 G3](../../production/PRODUCTION-READINESS.md)。
- 为什么 schema 合法仍可能库存编造？对应 M10 Claim/Task Evaluation。
- 为什么工具调用模型训练的 Tool Observation 一般不做 assistant loss？对应 [多轮 Mask](../../sft-peft/agent-tool-calling-loss-mask.md)。
- 如何换成**真实只读 API**、增加 timeout、request_id、幂等重试、真实引用 claim 支持检查？先写风险模型与实验设计，再放到实际工程仓。
- 如何接 Qwen3 的 Tool Calling？先查看 [Qwen 官方工具模板](https://qwen.readthedocs.io/en/latest/framework/function_call.html)，将真实模型输出经 JSON schema parser 输入本 Gateway；不允许模型输出直接绕过系统授权。

练习完成后换陌生的“订单状态查询”两只读工具做独立迁移，保持权限和负例，按 [Rubric](../../assessments/CAPABILITY-RUBRIC.md) 评价；不能仅用 11 个单测通过证明学习者掌握。

资料路径：[需求驱动示例](../../demand-driven/worked-demand-cards.md) · [生产门禁](../../production/PRODUCTION-READINESS.md) · [实战阶梯](../capability-ladder.md)。

