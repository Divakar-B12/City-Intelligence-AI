
# ============================================================
# 1. Loading all the libraries
# ============================================================

from dotenv import load_dotenv
load_dotenv()

import os
import requests

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient
from rich import print
from langchain.agents.middleware import wrap_tool_call

from langchain.agents import create_agent


# ============================================================
# 2. Creating Tools
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

    # Check API response
    if response.status_code != 200:
        return data.get("message", "Unable to fetch weather")

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"Weather in {city}: {desc}, {temp}°C"


# print(get_weather.invoke({"city": "Bengaluru"}))


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


# print(get_news.invoke({"city": "Bengaluru"}))


# ============================================================
# 3. Initializing the LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b"
)


# # ============================================================
# # 4. Binding Tools with LLM
# # ============================================================

# tools = {
#     "get_weather": get_weather,
#     "get_news": get_news
# }

# llm_with_tool = llm.bind_tools(
#     [get_weather, get_news]
# )


# # ============================================================
# # 5. Agent Loop
# # ============================================================

# messages = []

# print("[bold cyan]City Intelligence System[/bold cyan]")
# print("[yellow]Type 'exit' to quit[/yellow]\n")


# while True:

#     user_input = input("You: ")

#     if user_input.lower() == "exit":
#         break

#     messages.append(
#         HumanMessage(content=user_input)
#     )

#     while True:

#         result = llm_with_tool.invoke(messages)

#         messages.append(result)

#         # Check whether the LLM wants to call a tool
#         if result.tool_calls:

#             for tool_call in result.tool_calls:

#                 tool_name = tool_call["name"]

#                 # ---------------- Human in the Loop ----------------

#                 confirm = input(
#                     f"\nAgent wants to call {tool_name}. "
#                     "Approve? (yes/no): "
#                 )

#                 if confirm.lower() != "yes":

#                     print(
#                         "[bold red]Tool call denied. "
#                         "I cannot get the requested information.[/bold red]"
#                     )

#                     break

#                 # ---------------- Execute Tool ---------------------

#                 tool_result = tools[tool_name].invoke(tool_call["args"])

#                 messages.append(
#                     ToolMessage(
#                         content=str(tool_result),
#                         tool_call_id=tool_call["id"]
#                     )
#                 )

#             else:
#                 continue

#             break

#         else:

#             print("\n[bold green]Final Answer:[/bold green]\n")
#             print(result.content)

#             print("\n" + "=" * 50 + "\n")

#             break


@wrap_tool_call
def human_approval(request, handler):
    """Ask for human approval before every tool call"""
    tool_name = request.tool_call["name"]
    confirm = input(f"Agent wants to call '{tool_name}'. Approve? (yes/no): ")

    if confirm.lower() != "yes":
        return ToolMessage(
            content="Tool call denied by user.",
            tool_call_id = request.tool_call["id"]
        )
    
    return handler(request)

agent = create_agent(
    llm,
    tools= [get_weather, get_news],
    system_prompt="You are a helpfull city assistant",
    middleware=[human_approval]
)


print("City Agent | Type exit to quit")

while True:
    user_input = input("You : ")

    if user_input.lower() == 'exit':
        break

    result = agent.invoke({"messages": [{"role": "user", "content": user_input}]})

    print("Bot :", result['messages'][-1].content)
    


