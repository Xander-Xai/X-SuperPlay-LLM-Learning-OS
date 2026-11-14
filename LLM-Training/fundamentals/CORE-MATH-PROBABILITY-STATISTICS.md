# 基础缺口 F0｜数学、概率、信息论、机器学习与实验判断

**定位**：这是 [M01](../modules/M01.md) 的**可查词典与实操作业**。不要求先读完整本书；遇到某个公式/现象再精读一行。理论来源：[Dive into Deep Learning 数学与预备知识](https://d2l.ai/chapter_preliminaries/index.html)（数学有不同版本镜像，请确认具体页面）· [D2L 主站](https://d2l.ai/) · [Stanford CS336](https://cs336.stanford.edu/) · [PyTorch Autograd](https://docs.pytorch.org/docs/stable/autograd.html)。2026-11-14 抽样核对入口；外部页面更新可能改变章节。

## A. 先知道大模型用哪些数学工具（专业定义 + 白话 + 最小测试）

| 知识 | 定义/公式/输入输出 | 大白话 | 何时立刻学与最小动作 |
|---|---|---|---|
| Tensor、Shape、Stride、Broadcast | X∈ℝ[B,T,D]；Linear W∈ℝ[D,V] → Logits[B,T,V]；stride 决定内存步长 | 张量像多层货架，形状决定货怎么摆；broadcast 是自动配齐某些维度 | 遇到 QKV shape、OOM、matmul 报错：手画维度，打印 shape/stride 和连续性 |
| Matmul、Transpose、Norm | QKᵀ 的 T×D @ D×T 得 T×T；向量 L2 范数和 Frobenius 范数常用于梯度裁剪/权重分析 | 计算每个词与其他词的相似分数 | 按手算 2×2 矩阵，对照 PyTorch 矩阵乘法 |
| 特征值/SVD、低秩 | 矩阵可以通过低秩因子 A∈ℝ[r,in], B∈ℝ[out,r] 近似更新，r≪min(in,out) | 大部件的改动可以用少数“小旋钮”描述 | LoRA Rank/矩阵量理解不清时查，比较参数量 r(in+out) 与 out·in |
| 偏导、链式法则、梯度 | ∂L/∂W 由计算图逐层应用链式规则；有限差分 (L(W+ε)-L(W-ε))/(2ε) 只在合适精度与尺度下近似导数 | 发现哪个旋钮改变后，错误变大/变小 | 对简单 Linear→Softmax→CE 做手算/数值梯度与 autograd 比较 |
| 条件概率、Bayes、最大似然 | p(x_t｜x_{<t})；最大似然 θ*=argmaxΣlog pθ；独立性是需要验证的假设 | 给定前文，预测下一个字的可能性；别把相关当因果 | 学 Pretrain 时计算一个长度 3 的序列分解及 NLL |
| Softmax、LogSumExp 与 CE | softmax(z_i)=exp(z_i)/Σ exp(z_j)；交叉熵 H(p,q)=-Σp_i log q_i；分类 One-Hot 时为 -log q_y | 把分数变成概率，再处罚“给正确答案的概率太低” | 手算 2 类 CE，和 F.cross_entropy 比较；极大 logits 下用 log-softmax 避免溢出 |
| 熵、KL、交叉熵的区别 | H(p)=-Σp log p；D_KL(p||q)=Σp log(p/q)≥0；H(p,q)=H(p)+D_KL(p||q)（相同支持条件） | 熵=真实不确定性；KL=两套偏好相差多远；CE=按真实分布给模型打分 | 研究 DPO/GRPO KL 或模型输出分布漂移时，手算 Bernoulli(p=.8,q=.6) |
| Bits、Nats、BPB、PPL | 自然对数负对数似然以 Nat 表示；PPL=exp(平均 Token NLL)；BPB=总负对数似然 / (字节数·ln2)（同一计数规范下） | 一份文本平均需要多少“压缩信息量” | 比较不同 Tokenizer 时不直接比较 Token PPL；按字节口径核对是否可比 |
| SGD、Momentum、AdamW | 参数更新用梯度方向；AdamW 维护一/二阶动量并解耦 Weight Decay；Step/LR/Scale 会影响稳定性 | 改方向时别只看当前这一步，要参考历史趋势 | 打印 param、grad、step、exp_avg、exp_avg_sq；检查 optimizer.step() |
| Batch、梯度累积、LR、Warmup | 有效 Batch≈microbatch × accumulation × data_parallel_degree（假设各卡一致）；LR 调度和梯度缩放需匹配真实 token 更新节奏 | 小餐盘分多次端菜，再合并成一顿 | 保持 token 预算近似一致，单变量改变 accumulation；核对 loss 除法 |
| Generalization、Bias/Variance、Regularization | Train loss 下降与 Test error 下降不是同一目标；Weight Decay、Dropout、Early Stopping 会改变过拟合 | 把练过的题记住不代表会解新题 | 对重复训练语料 vs 陌生语料分别算 Loss，记录两条曲线 |
| 统计推断：方差、置信区间、Bootstrap | 对样本均值估计不确定性；Bootstrap **按正确独立单位**重抽样；小 n 和重复样本会误导区间 | 10 题全对不能宣称对所有人都 100% | 对 n=20 二分类结果计算 Wilson 区间，别把 20 次重试当 20 个独立用户 |
| Hypothesis/对照、消融与泄漏 | 固定 seed、样本集合、成本/解码配置、目标/保护指标；只改关键变量；Train/Val/Test 按实体/任务族去重隔离 | 实验像调一个旋钮看结果，不能同时换菜单和厨师 | 先固定 Baseline，挑一条负例，事后不要拿 Test 集调参数 |
| 数值精度/稳定与可复现性 | FP32、BF16、FP16、FP8 动态范围和精度不同；NaN 可能来自溢出/Mask/空监督；同种 Seed 不保证跨设备完全一致 | 用不同精度的尺子，量程不同；同样配方也可能因炉子不同有微差 | 记录 dtype、Autocast、Scaler、device、PyTorch 版本；测试全忽略 label 是否报错 |

## B. 8 分钟独立推导：2 类概率分布

令真实分布 p=(0.8,0.2)，预测 q=(0.6,0.4)。

- 专业：H(p)=-0.8·ln(0.8)-0.2·ln(0.2)；H(p,q)=-0.8·ln(0.6)-0.2·ln(0.4)；KL=H(p,q)-H(p)。
- 白话：真实样本偏向 A，模型低估了 A，交叉熵比“真实自己能达到的熵”更高，差额就是相对信息损失。
- 负例：把 KL(p||q) 和 KL(q||p) 当作完全相同；把 **reward 平均值**当作准确率；把没有 held-out 的 TinyGPT Train Loss 当测试分。
- 自测：手算后用 Python 标准库 math.log 写 4 行，检查 KL≥0、H(p,q)≥H(p)。

## C. 跟到真正的训练代码

1. [TinyGPT CPU](../labs/tiny-gpt/README.md)：沿 ids→Embedding→QKV→CE→Backward→AdamW 标张量 shape；这是基础教学，不是 GPT 大规模训练完成。
2. [Minimind Runbook](../experiments/01-minimind-whitebox/RUNBOOK-FIRST-DAY.md)：真实的模型前向、参数更新、Checkpoint，需亲自下载数据并运行。
3. [M09 训练系统](../modules/M09.md)：参数/梯度/优化器/激活的显存核算，区分总显存与 torch allocated/reserved。
4. [M10 统计验收](../modules/M10.md)：验证与最终测试隔离；正确率、置信区间、重复采样、任务级分母。
5. [PyTorch 复现性官方说明](https://pytorch.org/docs/stable/notes/randomness.html)：PyTorch 明确**跨设备、版本和平台不保证完全复现**；不要把一个 seed 写成全平台位精确一致。

**最小能力退出**：不看提示计算一项 CE、说明梯度传播、解释 PPL/BPB 的单位，并给出一个固定种子和一个反例。不了解其中某点时从本表跳入即可，不强制补完所有统计学课程。
