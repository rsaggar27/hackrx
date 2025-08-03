from typing import List
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain.chat_models.base import BaseChatModel

def retrieve_relevant_docs(vectorstore: FAISS, query: str, k: int = 3) -> List[Document]:
    """
    Retrieve top-k relevant documents for a given query using FAISS similarity search.

    Args:
        vectorstore (FAISS): The vectorstore containing embedded documents.
        query (str): The user's rephrased or raw question.
        k (int): Number of top documents to retrieve.

    Returns:
        List[Document]: Retrieved documents.
    """
    return vectorstore.similarity_search(query, k=k)

def build_context(docs: List[Document]) -> str:
    """
    Join the retrieved documents into a single string context.

    Args:
        docs (List[Document]): The retrieved documents.

    Returns:
        str: Combined context text.
    """
    return "\n".join([doc.page_content for doc in docs])

def build_prompt(context: str, question: str) -> str:
    """
    Construct an instruction-following prompt tailored to insurance QA.

    Args:
        context (str): Retrieved content from vectorstore.
        question (str): Rephrased or original question.

    Returns:
        str: Prompt for LLM.
    """
    return f"""
You are a helpful insurance advisor. Based only on the given context, answer the user's question about insurance coverage.

Instructions:
- If the question asks whether something is covered, answer with "Yes", "No", or "It depends", followed by a clear explanation.
- If the question asks about conditions, limitations, or requirements, summarize them accurately.
- If the context does not contain enough information, say so — do not guess or assume.
- Do not use any knowledge beyond the context provided.
- Keep the response clear and specific.

### Context:
{context}

### User Question:
{question}

Answer:
"""

def answer_question_with_retrieval(llm: BaseChatModel, vectorstore: FAISS, question: str, k: int = 3) -> str:
    """
    Retrieves relevant docs and uses the LLM to answer a question based on retrieved context.

    Args:
        llm (BaseChatModel): An instantiated LLM (e.g., ChatGroq, ChatOpenAI).
        vectorstore (FAISS): Vector DB containing embedded document chunks.
        question (str): The user's question.
        k (int): Number of top-k documents to retrieve.

    Returns:
        str: The final answer.
    """
    docs = retrieve_relevant_docs(vectorstore, question, k=k)
    context = build_context(docs)
    prompt = build_prompt(context, question)
    response = llm.invoke(prompt)
    return response.content
