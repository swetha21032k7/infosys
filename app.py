import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
# Load API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    st.error("❌ GOOGLE_API_KEY not found. Please add it to your .env file or Streamlit Secrets.")
    st.stop()

# Import agents
from agents.research_agent import create_research_agent
from agents.summarise_agent import create_summarize_agent
from agents.email_agent import create_email_agent

# Import tools
from tools.wiki_tool import get_wiki_tool
from tools.duckduckgo_tool import get_duckduckgo_tool
from tools.arxiv_tool import get_arxiv_tool

# Initialize session state
if 'research_output' not in st.session_state:
    st.session_state.research_output = None
if 'summary_output' not in st.session_state:
    st.session_state.summary_output = None
if 'email_output' not in st.session_state:
    st.session_state.email_output = None
if 'processing' not in st.session_state:
    st.session_state.processing = False

# App config
st.set_page_config(page_title="AI Research Assistant", layout="wide")
st.title("🧠 AI Research Assistant")

# Sidebar instructions
with st.sidebar:
    st.header("How It Works")
    st.markdown("""
    1. Enter a research question  
    2. Click **Start Research**  
    3. Three specialized agents work sequentially:
       - 🔍 Research Agent gathers facts
       - 📊 Summarizer creates insights
       - ✉️ Email Agent drafts communication
    """)

# Input form
query = st.text_input("What would you like to research?", "")

col1, col2 = st.columns([1, 4])
with col1:
    start_btn = st.button("Start Research", disabled=st.session_state.processing or not query)

# Tabs
tab1, tab2, tab3 = st.tabs(["Research Data", "Summary", "Draft Email"])

if start_btn:
    st.session_state.processing = True
    st.session_state.research_output = None
    st.session_state.summary_output = None
    st.session_state.email_output = None

    with st.spinner("🔍 Conducting research..."):
        try:
            # Initialize tools
            tools = [
                get_wiki_tool(),
                get_duckduckgo_tool(),
                get_arxiv_tool()
            ]

            # Create agent
            research_agent = create_research_agent(tools)
            research_result = research_agent(query)

            st.session_state.research_output = research_result

            with st.spinner("📊 Generating executive summary..."):
                summarize_agent = create_summarize_agent()
                summary_result = summarize_agent(research_result)
                st.session_state.summary_output = summary_result

                with st.spinner("✉️ Drafting professional email..."):
                    email_agent = create_email_agent()
                    email_result = email_agent(summary_result)
                    st.session_state.email_output = email_result

            st.success("✅ Research Complete!")

        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
        finally:
            st.session_state.processing = False

# Display tabs
with tab1:
    if st.session_state.research_output:
        st.json(st.session_state.research_output)
    else:
        st.info("No research data yet. Enter a query and click 'Start Research'.")

with tab2:
    if st.session_state.summary_output:
        st.markdown(st.session_state.summary_output)
    else:
        st.info("Summary will appear here after research completes.")

with tab3:
    if st.session_state.email_output:
        st.subheader("Final Email Draft")
        st.text_area("", value=st.session_state.email_output, height=400)
    else:
        st.info("The final email draft will appear here.")