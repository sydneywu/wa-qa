import faiss
from langchain import OpenAI
from langchain import HuggingFaceHub
from langchain.chains import RetrievalQA
import pickle
import argparse
from langchain.chat_models import ChatOpenAI
import os
from dotenv import load_dotenv

load_dotenv()


def ask_llm(question: str):

    llm_model_name = os.getenv('LLM_MODEL_NAME')

    # Load the LangChain.
    index = faiss.read_index("docs.index")

    with open("faiss_store.pkl", "rb") as f:
        store = pickle.load(f)

    store.index = index
    # Initialise Langchain - Conversation Retrieval Chain
    #qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(temperature=0), vectorstore.as_retriever(), verbose=True)
    #qa = RetrievalQA.from_llm(ChatOpenAI(temperature=0), vectorstore.as_retriever(), verbose=True)
    qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(temperature=0,model_name=llm_model_name), chain_type="stuff", retriever = store.as_retriever(), verbose=True)

    answer = qa(question)
    result = answer['result']
    print(result)
    return result
