---
topic: ReAct 模式原理
concepts: [Thought-Action-Observation, ReAct 论文, 推理链, 与 Tool Agent 的区别]
prerequisites: [phase-1-tool-agent/]
understanding_score: null
last_quizzed: null
created: 2026-03-16
last_updated: 2026-03-16
---

# ReAct：Thought → Action → Observation

## Why This Matters

Phase 1 的 Tool Agent 让 LLM "能用工具"，但它的推理过程是不透明的。
ReAct 模式要求 LLM **显式地把思考过程写出来**，每一步都可以追踪。

这不只是为了好看——显式思考让 LLM 在复杂任务里犯更少的错误。

---

## 核心心智模型

```
ReAct = Reason + Act

每一步：
  Thought:   "我需要先找到这篇论文的作者..."
  Action:    search("ReAct paper authors")
  Observation: "作者是 Yao et al., 2022"

  Thought:   "有了作者信息，现在需要找他们的机构..."
  Action:    search("Shunyu Yao affiliation")
  Observation: "Princeton University + OpenAI"

  Thought:   "信息已经足够了，可以回答了"
  Final Answer: "ReAct 论文由普林斯顿大学和 OpenAI 的研究者共同发表..."
```

---

## ReAct vs 普通 Tool Agent

| 特性 | Tool Agent (Phase 1) | ReAct Agent |
|------|---------------------|-------------|
| 推理过程 | 隐式，在 LLM 内部 | 显式，写出 Thought |
| 可调试性 | 难以追踪 | 每步都可见 |
| 复杂任务 | 容易迷失方向 | 更有条理 |
| 实现复杂度 | 简单 | 稍复杂（需要解析格式） |

---

## ReAct 的两种实现方式

### 方式 1：提示工程（Prompt-based）
通过 System Prompt 告诉 LLM 按 Thought/Action/Observation 格式输出：

```python
REACT_SYSTEM_PROMPT = """
你是一个使用 ReAct 模式的 AI 助手。

在每一步，你必须按以下格式输出：
Thought: [你的推理过程]
Action: [tool_name]
Action Input: [{"param": "value"}]

收到 Observation 之后，继续下一步 Thought/Action，
直到你能够给出最终答案：
Final Answer: [最终回答]

重要规则：
- 必须在 Action 之前写出 Thought
- 不要跳过步骤
- 每次只执行一个 Action
"""
```

### 方式 2：原生 Tool Calling + 日志增强
利用 Anthropic API 原生的 tool calling，在 Agent Loop 里打印推理过程。

Phase 2 项目我们用**方式 2**，更稳定，不依赖 LLM 遵守格式。

---

## 关键洞察

> ReAct 的本质是：在行动之前强制 LLM "说出" 它的想法。

这在心理学上有对应：人在解决复杂问题时，大声说出思考过程（"think aloud"）会犯更少错误。

对 LLM 同样有效。

---

## Practice

**思考题：**
下面是一个用户问题："2024 年最受欢迎的 Python AI 框架是哪些？"

用 ReAct 格式，手写出你认为 Agent 应该经历的推理步骤（不用写代码，写中文就行）：

```
Thought 1: ...
Action 1: ...
Observation 1: ...

Thought 2: ...
Action 2: ...
...

Final Answer: ...
```

写完后在下一篇教程里看实际实现是否和你的预想一致。

---

## Q&A

（在这里追加你学习过程中遇到的问题）
