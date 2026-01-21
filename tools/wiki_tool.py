from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

def get_wiki_tool():
    api_wrapper = WikipediaAPIWrapper(top_k_results=3, doc_content_chars_max=5000)
    return WikipediaQueryRun(api_wrapper=api_wrapper, name="Wikipedia", description="Useful for general knowledge and academic topics.")