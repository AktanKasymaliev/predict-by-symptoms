from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chains.question_answering import load_qa_chain

from langchain.vectorstores.base import VectorStoreRetriever

from .templates import CONDENSE_QUESTION_PROMPT
from .prompts import get_intent_prompt, get_chat_prompt

def get_chat_chain(retriever: VectorStoreRetriever):
    question_gen_llm = OpenAI(
        temperature=0,
        verbose=True,
    )
    streaming_llm = OpenAI(
        streaming=True,
        verbose=True,
        temperature=0,
    )
    question_generator = LLMChain(llm=question_gen_llm, prompt=CONDENSE_QUESTION_PROMPT)
    doc_chain = load_qa_chain(
        llm=streaming_llm,
        chain_type="stuff",
        prompt=get_chat_prompt(),
    )

    qa = ConversationalRetrievalChain(
        retriever=retriever,
        question_generator=question_generator,
        doc_chain=doc_chain,
        )
    return qa

def get_intents_chain():
    chat = ChatOpenAI(
        temperature=0,
        verbose=True,
    )
    prompt = get_intent_prompt()
    return LLMChain(llm=chat, prompt=prompt)

