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
    If there is no information but intent==symptom, try to make answer by yourself, 
    But if you don't know, say that you don't know.
    If there are several 'Supposed diagnosis' and 'Helpful Answer', list all them what diseases may be.

    Use and humanize the following pieces of information to make a diagnosis
    and reply to patient:
        Intent: {intent}
        Helpful Answer: {answer}
        Supposed diagnosis: {focus}
    """

    return PromptTemplate(
        input_variables=["answer", "focus", "intent"],
        template=template,
    )