---
topic: RAG Agent - 向量检索增强生成
concepts: [Embedding, 向量数据库, 相似度检索, RAG Pipeline, Codebase QA]
prerequisites: [phase-3-plan-execute/]
understanding_score: null
last_quizzed: null
created: 2026-03-16
last_updated: 2026-03-16
---

# RAG Agent：让 Agent 读懂你的代码库

## Why This Matters

前面的 Agent 靠的是 LLM 本身的知识。
但有一类问题 LLM 无法回答：**"你们公司这个项目的 X 模块是怎么实现的？"**

RAG（Retrieval-Augmented Generation）就是给 Agent 一个"外挂知识库"，
让它能回答基于你自己文档/代码的问题。

对前端开发者来说，最实用的应用是：**Codebase QA Assistant**。

---

## 核心心智模型

```
问题：搜索引擎怎么找到相关文档的？
答案：把文档变成数字（向量），用数字计算"相似度"

RAG 的工作流程：

索引阶段（一次性）：
  代码文件
    ↓ Embedding 模型
  每个文件 → 一串数字（向量）
    ↓
  存入向量数据库

查询阶段（每次提问）：
  用户问题
    ↓ 同一个 Embedding 模型
  问题向量
    ↓ 相似度搜索
  最相关的几个代码片段
    ↓ 传给 LLM
  LLM 结合代码片段回答问题
```

---

## Lesson 1：Embedding（向量嵌入）

```python
# 用 Anthropic 的 embedding API
from anthropic import Anthropic

client = Anthropic()

def get_embedding(text: str) -> list[float]:
    """把文本转成向量"""
    # 注意：实际用 voyage-3 或 text-embedding-3-small 等模型
    # 这里演示概念
    response = client.embeddings.create(
        model="voyage-3",
        input=text
    )
    return response.embeddings[0].embedding

# 两段相似的文本，它们的向量"距离"应该很近
code1 = "def get_user(user_id: int) -> User:"
code2 = "async def fetch_user_by_id(id: int):"
comment = "获取用户信息的函数"

# 向量相似度（余弦相似度）
import numpy as np

def cosine_similarity(a: list[float], b: list[float]) -> float:
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

---

## Lesson 2：向量数据库（用 ChromaDB）

```bash
uv add chromadb
```

```python
# agent/vector_store.py
import chromadb
from chromadb.utils import embedding_functions
import os

class CodeVectorStore:
    def __init__(self, collection_name: str = "codebase"):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        # 使用 OpenAI 或 voyage 的 embedding
        self.ef = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.ef
        )

    def add_documents(self, documents: list[dict]):
        """
        添加文档到向量库
        documents: [{"id": "file.py:10-30", "content": "代码片段", "metadata": {...}}]
        """
        self.collection.add(
            ids=[d["id"] for d in documents],
            documents=[d["content"] for d in documents],
            metadatas=[d.get("metadata", {}) for d in documents]
        )

    def search(self, query: str, n_results: int = 5) -> list[dict]:
        """搜索最相关的代码片段"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return [
            {
                "id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            }
            for i in range(len(results["ids"][0]))
        ]
```

---

## Lesson 3：代码索引器

```python
# agent/indexer.py
import os
from pathlib import Path
from .vector_store import CodeVectorStore

def chunk_code_file(file_path: str, chunk_size: int = 50) -> list[dict]:
    """
    把代码文件切成小块（chunk），每块约 50 行
    """
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    chunks = []
    for i in range(0, len(lines), chunk_size):
        chunk_lines = lines[i:i + chunk_size]
        chunk_content = "".join(chunk_lines)

        if chunk_content.strip():  # 跳过空块
            chunks.append({
                "id": f"{file_path}:{i}-{i + len(chunk_lines)}",
                "content": chunk_content,
                "metadata": {
                    "file": file_path,
                    "start_line": i,
                    "end_line": i + len(chunk_lines)
                }
            })
    return chunks

def index_codebase(root_dir: str, extensions: list[str] = None) -> CodeVectorStore:
    """
    索引整个代码库
    """
    if extensions is None:
        extensions = [".py", ".ts", ".js", ".tsx", ".jsx"]

    store = CodeVectorStore()
    all_chunks = []

    for path in Path(root_dir).rglob("*"):
        if path.suffix in extensions and ".venv" not in str(path) and "node_modules" not in str(path):
            chunks = chunk_code_file(str(path))
            all_chunks.extend(chunks)
            print(f"索引：{path} ({len(chunks)} 块)")

    print(f"\n总计索引 {len(all_chunks)} 个代码块")
    store.add_documents(all_chunks)
    return store
```

---

## Lesson 4：Codebase QA Agent

```python
# agent/codebase_agent.py
from anthropic import AsyncAnthropic
from .vector_store import CodeVectorStore

client = AsyncAnthropic()

async def ask_codebase(question: str, store: CodeVectorStore) -> str:
    """RAG 流程：检索 + 生成"""

    # Step 1: 检索相关代码片段
    relevant_chunks = store.search(question, n_results=5)

    # Step 2: 构建上下文
    context = "\n\n".join([
        f"文件：{chunk['metadata']['file']}（第{chunk['metadata']['start_line']}-{chunk['metadata']['end_line']}行）\n"
        f"```\n{chunk['content']}\n```"
        for chunk in relevant_chunks
    ])

    # Step 3: 传给 LLM 回答
    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system="你是一个代码助手，根据提供的代码片段回答关于代码库的问题。如果代码片段里没有相关信息，请直说。",
        messages=[{
            "role": "user",
            "content": f"根据以下代码片段回答问题：\n\n{context}\n\n问题：{question}"
        }]
    )

    return response.content[0].text

# 使用示例
async def main():
    from dotenv import load_dotenv
    load_dotenv()

    # 索引你的项目
    store = index_codebase("./")

    # 提问
    questions = [
        "agent loop 是在哪个文件里实现的？",
        "工具注册是怎么工作的？",
        "如何添加一个新工具？"
    ]

    for q in questions:
        print(f"\n问：{q}")
        answer = await ask_codebase(q, store)
        print(f"答：{answer}")
```

---

## 完成标准

- [ ] 能索引一个真实的代码库（比如本课程的项目代码）
- [ ] 能回答关于代码实现细节的问题
- [ ] 检索到的代码片段真正相关（不是乱的）
- [ ] 当问题超出代码库范围时，Agent 能说明无法回答

---

## Q&A

（在这里追加你学习过程中遇到的问题）
