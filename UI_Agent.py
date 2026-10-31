
# ============================================================
# 1. Loading all the libraries
# ============================================================

from dotenv import load_dotenv
load_dotenv()

import os
import requests
import streamlit as st

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient


# ============================================================
# 2. Streamlit Page Configuration
# ============================================================

st.set_page_config(
    page_title="City Intelligence AI",
    page_icon="🌍",
    layout="wide"
)


# ============================================================
# 3. Custom CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: #FFFFFF;
}

.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #FFFFFF;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    color: #9CA3AF;
    font-size: 16px;
    margin-bottom: 30px;
}

.tool-card {
    background-color: #1C2333;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #303A4F;
    margin-bottom: 12px;
}

.tool-title {
    font-size: 17px;
    font-weight: 700;
    color: #FFFFFF;
}

.tool-description {
    color: #AAB4C5;
    font-size: 13px;
}

div.stButton > button {
    border-radius: 8px;
    font-weight: 600;
    height: 42px;
}

[data-testid="stChatMessage"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 4. Creating Tools
# ============================================================

# -------------------- Weather Tool --------------------------

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city."""

    API_KEY = os.getenv("OPENWEATHER_API_KEY")

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    response = requests.get(url, timeout=10)
    data = response.json()

    if response.status_code != 200:
        return data.get("message", "Unable to fetch weather")

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"Weather in {city}: {desc}, {temp}°C"


# -------------------- Tavily News Tool ----------------------

tavily_client = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


@tool
def get_news(city: str) -> str:
    """Get latest news about the city."""

    response = tavily_client.search(
        query=f"Latest news about {city}",
        topic="news",
        search_depth="basic",
        max_results=3
    )

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}"

    news_list = []

    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")

        news_list.append(
            f"- {title}\n{url}\n{snippet[:100]}"
        )

    return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)


# ============================================================
# 5. Initializing the LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b"
)


# ============================================================
# 6. Binding Tools with LLM
# ============================================================

tools = {
    "get_weather": get_weather,
    "get_news": get_news
}

llm_with_tool = llm.bind_tools(
    [get_weather, get_news]
)


# ============================================================
# 7. Session State
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "pending_tool_calls" not in st.session_state:
    st.session_state.pending_tool_calls = []

if "agent_running" not in st.session_state:
    st.session_state.agent_running = False


# ============================================================
# 8. Sidebar
# ============================================================

with st.sidebar:

    st.markdown("## 🌍 City Intelligence AI")

    st.caption("Powered by LangChain + Groq + Tavily")

    st.divider()

    st.markdown("### 🛠️ Available Tools")

    st.markdown("""
    <div class="tool-card">
        <div class="tool-title">🌤️ Weather Information</div>
        <div class="tool-description">
            Get real-time weather information for any city.
        </div>
    </div>

    <div class="tool-card">
        <div class="tool-title">📰 Latest City News</div>
        <div class="tool-description">
            Search for the latest news using Tavily.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown("### 🤖 AI Configuration")

    st.success("Groq LLM Connected")
    st.info("LangChain Tool Calling Enabled")
    st.info("Human-in-the-Loop Enabled")

    st.divider()

    if st.button("🗑️ Clear Conversation", use_container_width=True):

        st.session_state.messages = []
        st.session_state.chat_history = []
        st.session_state.pending_tool_calls = []
        st.session_state.agent_running = False

        st.rerun()

    st.caption("City Intelligence AI | Built with Streamlit")


# ============================================================
# 9. Main UI
# ============================================================

st.markdown(
    '<div class="main-title">🌍 City Intelligence AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Your AI assistant for weather updates and city news.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# 10. Display Chat History
# ============================================================

for chat in st.session_state.chat_history:

    with st.chat_message(chat["role"]):

        st.markdown(chat["content"])


# ============================================================
# 11. Agent Execution Function
# ============================================================

def run_agent():

    while True:

        result = llm_with_tool.invoke(
            st.session_state.messages
        )

        st.session_state.messages.append(result)

        # Check whether the LLM wants to call a tool
        if result.tool_calls:

            st.session_state.pending_tool_calls = result.tool_calls

            return

        else:

            assistant_response = result.content

            st.session_state.chat_history.append({
                "role": "assistant",
                "content": assistant_response
            })

            st.session_state.pending_tool_calls = []

            return


# ============================================================
# 12. Tool Approval and Execution
# ============================================================

if st.session_state.pending_tool_calls:

    st.warning("⚠️ Agent wants to execute the following tool(s).")

    for index, tool_call in enumerate(
        st.session_state.pending_tool_calls
    ):

        tool_name = tool_call["name"]

        with st.container(border=True):

            st.markdown(f"### 🔧 {tool_name}")

            st.json(tool_call["args"])

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "✅ Approve",
                    key=f"approve_{index}",
                    use_container_width=True
                ):

                    try:

                        tool_result = tools[tool_name].invoke(
                            tool_call["args"]
                        )

                        st.session_state.messages.append(
                            ToolMessage(
                                content=str(tool_result),
                                tool_call_id=tool_call["id"]
                            )
                        )

                        st.session_state.chat_history.append({
                            "role": "assistant",
                            "content": f"🔧 Executed **{tool_name}** successfully.\n\n{tool_result}"
                        })

                        st.session_state.pending_tool_calls.pop(index)

                        st.rerun()

                    except Exception as e:

                        st.error(f"Tool execution failed: {e}")

            with col2:

                if st.button(
                    "❌ Deny",
                    key=f"deny_{index}",
                    use_container_width=True
                ):

                    st.session_state.pending_tool_calls = []

                    st.session_state.messages.append(
                        ToolMessage(
                            content="Tool execution was denied by the user.",
                            tool_call_id=tool_call["id"]
                        )
                    )

                    st.session_state.chat_history.append({
                        "role": "assistant",
                        "content": f"❌ Tool call **{tool_name}** was denied."
                    })

                    st.rerun()


# ============================================================
# 13. Chat Input
# ============================================================

user_input = st.chat_input(
    "Ask about weather or latest city news..."
)

if user_input:

    st.session_state.messages.append(
        HumanMessage(content=user_input)
    )

    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("🤖 AI is thinking..."):

        run_agent()

    st.rerun()
