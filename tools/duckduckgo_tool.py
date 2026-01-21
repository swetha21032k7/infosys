from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper

def get_duckduckgo_tool():
    wrapper = DuckDuckGoSearchAPIWrapper(max_results=5)
    return DuckDuckGoSearchResults(api_wrapper=wrapper, name="DuckDuckGo", description="Useful for recent developments and news.")