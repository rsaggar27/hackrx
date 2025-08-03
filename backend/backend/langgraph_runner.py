# from langchain.chat_models import ChatOpenAI
from langchain_groq import ChatGroq
# from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langgraph.graph import StateGraph, END
from .utils import document_loader, chunker, retriever, query_rephraser
import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from typing import TypedDict, List, Union

class GraphState(TypedDict):
    doc_url: str
    text: str
    questions: List[str]
    vectorstore: object
    answers: List[str]

load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
# llm = ChatOpenAI(temperature=0, model="gpt-4o", openai_api_key=api_key)
api_key = os.getenv("GROQ_API_KEY")
llm = ChatGroq(
        temperature=0,
        model="llama3-70b-8192",  # You can also try "mixtral-8x7b-32768"
        groq_api_key=api_key
    )
# embedding_model = OpenAIEmbeddings(openai_api_key=api_key)
embedding_model = HuggingFaceEmbeddings(
    model_name="intfloat/e5-large-v2",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True}
)

# Graph states
def question_node(state):
    questions = []
    questions = [query_rephraser.query_rephraser_fn(x) for x in state["questions"]]
    return {"questions":questions}

def download_node(state):
    text = document_loader.extract_text_from_url(state["doc_url"])
    return {"text": text, "questions": state["questions"]}


def chunk_embed_node(state):
    chunks = chunker.chunk_text(state["text"])
    docs = [Document(page_content=c) for c in chunks]
    vectorstore = FAISS.from_documents(docs, embedding_model)
    return {"vectorstore": vectorstore, "questions": state["questions"]}

def retrieve_answer_node(state):
    vectorstore = state["vectorstore"]
    questions = state["questions"]
    answers = []

    for q in questions:
        answer = retriever.answer_question_with_retrieval(llm, vectorstore, q, k=3)
        answers.append(answer)

    return {"answers": answers}

def run_graph(doc_url, questions):
    builder = StateGraph(GraphState)
    builder.add_node("download", download_node)
    builder.add_node("question", question_node)
    builder.add_node("chunk_embed", chunk_embed_node)
    builder.add_node("retrieve", retrieve_answer_node)

    builder.set_entry_point("question")
    builder.add_edge("question", "download")
    builder.add_edge("download", "chunk_embed")
    builder.add_edge("chunk_embed", "retrieve")
    builder.add_edge("retrieve", END)
    app = builder.compile()

    final_state = app.invoke({"doc_url": doc_url, "questions": questions})
    return final_state["answers"]

