from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import json

from utils.llm_config import get_llm
from utils.prompt_templates import RESEARCH_PROMPT

# Define expected output structure
class ResearchOutput(BaseModel):
    title: str = Field(description="Title of the research")
    research_summary: str = Field(description="Brief summary")
    detailed_findings: List[str] = Field(description="List of verified findings")
    key_topics: List[str] = Field(description="Main subtopics")
    sources: List[Dict[str, str]] = Field(description="List of source objects")
    confidence: str = Field(description="high | medium | low")
    next_action: str = Field(description="Always 'Pass to Summarizer'")

def create_research_agent(tools):
    llm = get_llm(temperature=0.3)
    llm_with_tools = llm.bind_tools(tools)

    prompt = ChatPromptTemplate.from_messages([
        ("system", RESEARCH_PROMPT),
        ("human", "{input}")
    ])

    # Chain: Prompt + LLM + JSON Parser
    parser = JsonOutputParser(pydantic_object=ResearchOutput)

    def invoke_research(query: str) -> Dict[str, Any]:
        try:
            result = prompt | llm_with_tools | parser
            output = result.invoke({"input": query})
            return output
        except OutputParserException as e:
            # Fallback: Try parsing raw response manually
            raw = llm_with_tools.invoke(
                RESEARCH_PROMPT + "\n\n" + query
            ).content

            try:
                cleaned = raw.strip().lstrip("```json").rstrip("```")
                return json.loads(cleaned)
            except Exception:
                return {
                    "title": "Error in Research",
                    "research_summary": "Could not parse results due to formatting issues.",
                    "detailed_findings": [],
                    "key_topics": [],
                    "sources": [],
                    "confidence": "low",
                    "next_action": "Pass to Summarizer"
                }
        except Exception as e:
            return {
                "title": "Research Failed",
                "research_summary": f"An error occurred during research: {str(e)}",
                "detailed_findings": [],
                "key_topics": [],
                "sources": [],
                "confidence": "low",
                "next_action": "Pass to Summarizer"
            }

    return invoke_research