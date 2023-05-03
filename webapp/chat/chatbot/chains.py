from langchain.chains.llm import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain

from .templates import CONDENSE_QUESTION_PROMPT
from .prompts import get_intent_prompt, get_chat_prompt

def get_stadealone_question_chain():
    question_gen_llm = OpenAI(
        temperature=0,
        verbose=True,
    )

    question = LLMChain(llm=question_gen_llm, prompt=CONDENSE_QUESTION_PROMPT)
    return question

def get_answer_chain():
    llm = OpenAI(
        temperature=0,
        verbose=True,
    )
    return LLMChain(llm=llm, prompt=get_chat_prompt())


def get_intents_chain():
    chat = ChatOpenAI(
        temperature=0,
        verbose=True,
    )
    prompt = get_intent_prompt()
    return LLMChain(llm=chat, prompt=prompt)

