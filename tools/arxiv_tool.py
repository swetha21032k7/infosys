from langchain_community.tools import ArxivQueryRun
from langchain_community.utilities import ArxivAPIWrapper

def get_arxiv_tool():
    api_wrapper = ArxivAPIWrapper(top_k_results=4, load_max_docs=2)
    return ArxivQueryRun(api_wrapper=api_wrapper, name="ArXiv", description="Useful for peer-reviewed scientific papers.")