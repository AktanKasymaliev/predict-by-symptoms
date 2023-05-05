from langchain import FewShotPromptTemplate, PromptTemplate
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)


def get_intent_prompt():
    INTENT_EXAMPLES = [
        {"input": "Hey, I have a headache", "intent": "symptom"},
        {"input": "I don't feel good", "intent": "symptom"},
        {"input": "hey, how are you?", "intent": "None"},
        {"input": "how does this shit work?", "intent": "None"},
        {"input": "I love you!", "intent": "None"},
        {"input": "this is bullshit", "intent": "None"},
        {"input": "a random stuff", "intent": "None"},
    ]
    example_formatter_template = """
    input: {input}\n
    intent: {intent}\n
    """

    example_prompt = PromptTemplate(
        input_variables=["input", "intent"],
        template=example_formatter_template,
    )
    few_shot_prompt = FewShotPromptTemplate(
        examples=INTENT_EXAMPLES,
        example_prompt=example_prompt,
        prefix="You are an intent classification bot.",
        suffix="You should output only an intent name without accompanying texts.",
        input_variables=[],
        example_separator="\n\n",
    )
    system_message_prompt = SystemMessagePromptTemplate(prompt=few_shot_prompt)
    human_prompt = PromptTemplate(
        input_variables=["input"], template="input: {input}\nintent: "
    )
    human_message_prompt = HumanMessagePromptTemplate(prompt=human_prompt)
    chat_prompt = ChatPromptTemplate.from_messages(
        [system_message_prompt, human_message_prompt]
    )

    return chat_prompt

def get_chat_prompt():
    template = """
    You are bot who talks like human and you can answer only for medical questions.
    But if you don't know, say that you don't know.  Without greetings and etc
    Use the following portion of a long dataset and information about person to see 
      if any of the text is relevant to answer the question. 

    Chat history with patient: {chat_history}

    Retell briefly in human-understandable language to the patient using this dataset from the Python programming language
    and reply to patient.
        Question or complains of patient: {complain}
        About person: {person}
        Intent: {intent}
        Your dataset for patient's related question: {dataset}
    Your answer:
    """
    return PromptTemplate(
        input_variables=["dataset", "intent", "complain", "person", "chat_history"],
        template=template,
    )