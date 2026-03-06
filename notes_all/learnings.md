# Learning Log

## Phase 0: Architecture Design

### 💡 Key Insights
1. 什么比例用户需要Agent
2. Create Prompt 这一步决定：信息排序;Token 长度控制;是否做摘要;是否加系统指令;是否添加引用编号
3. 

### 🔄 Misconceptions Fixed
- 我以为：
- 实际上：

### 🎯 Interview Talking Points
- 
001
在你的ESG问答系统中，什么比例的用户查询需要Agent？

估算：
- 简单查询（"Tesla emissions是多少"）：____%
- 对比查询（"Tesla vs Apple"）：____%  
- 复杂查询（"分析Tesla近3年趋势"）：____%

如果70%是简单查询，你会：
A. 所有查询都用Agent（一致性好，但成本高）
B. 先判断查询类型，简单的用普通RAG，复杂的用Agent（省成本，但复杂度高）
C. 全部用普通RAG，等发现问题再优化（先上线，再迭代）

002
Create Prompt 的完整工程拆解
You are an environmental performance analyst.
Answer strictly using the provided context.
If the information is insufficient, state so clearly.

Context:
[1] Tesla reduced emissions by 1.2M tons in 2023.
[2] Apple's carbon footprint decreased 15% year-over-year.

Task:
Compare Tesla and Apple's emissions performance.

Instructions:
- Highlight key differences.
- Cite the source numbers.
- Keep the response concise.

---

## Phase 1: [待填]

### 💡 Key Insights

### 🔄 Misconceptions Fixed

### 🎯 Interview Talking Points

---