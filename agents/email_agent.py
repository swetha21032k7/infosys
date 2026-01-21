from langchain_core.prompts import ChatPromptTemplate
from utils.llm_config import get_llm
from utils.prompt_templates import EMAIL_PROMPT

def create_email_agent():
    llm = get_llm(model_name="gemini-pro", temperature=0.4)
    prompt = ChatPromptTemplate.from_messages([
        ("system", EMAIL_PROMPT),
        ("human", "Summary:\n{summary}")
    ])
    chain = prompt | llm

    def invoke_email(summary_text):
        try:
            result = chain.invoke({"summary": summary_text})
            return result.content.strip()
        except Exception as e:
            return f"Email generation failed: {e}"

    return invoke_email