from langchain_core.prompts import ChatPromptTemplate
from utils.llm_config import get_llm
from utils.prompt_templates import SUMMARY_PROMPT

def create_summarize_agent():
    llm = get_llm(model_name="gemini-pro", temperature=0.2)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SUMMARY_PROMPT),
        ("human", "Research Data:\n{data}")
    ])
    chain = prompt | llm

    def invoke_summarize(research_output):
        try:
            result = chain.invoke({"data": str(research_output)})
            return result.content
        except Exception as e:
            return f"Summarization failed: {e}"

    return invoke_summarize