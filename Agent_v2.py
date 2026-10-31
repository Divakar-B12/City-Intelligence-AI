
# ============================================================
# 1. Loading all the libraries
# ============================================================

from dotenv import load_dotenv
load_dotenv()

import os
import requests

from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import ToolMessage
from langchain.agents.middleware import wrap_tool_call
from langchain.agents import create_agent

from tavily import TavilyClient
from rich import print


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
# 3. Initializing the LLM
# ============================================================

llm = ChatGroq(
    model="openai/gpt-oss-120b"
)


# ============================================================
# 4. Human-in-the-Loop Middleware
# ============================================================

@wrap_tool_call
def human_approval(request, handler):
    """Ask for human approval before every tool call."""

    tool_name = request.tool_call["name"]

    confirm = input(
        f"\nAgent wants to call '{tool_name}'. "
        "Approve? (yes/no): "
    ).strip().lower()

    if confirm != "yes":

        print(
            "[bold red]Tool call denied by user.[/bold red]"
        )

        return ToolMessage(
            content="Tool call denied by user.",
            tool_call_id=request.tool_call["id"]
        )

    print(
        f"[bold green]Executing {tool_name}...[/bold green]"
    )

    return handler(request)


# ============================================================
# 5. Creating the Agent
# ============================================================

agent = create_agent(
    model=llm,
    tools=[
        get_weather,
        get_news
    ],
    system_prompt="You are a helpful city assistant.",
    middleware=[
        human_approval
    ]
)


# ============================================================
# 6. Running the Agent
# ============================================================

print("\n[bold cyan]========================================[/bold cyan]")
print("[bold cyan]       CITY INTELLIGENCE AI AGENT       [/bold cyan]")
print("[bold cyan]========================================[/bold cyan]")

print("\n[yellow]Available Tools:[/yellow]")
print("1. Weather Information")
print("2. Latest City News")

print("\n[green]Type 'exit' to quit.[/green]\n")


while True:

    user_input = input("You: ").strip()

    if user_input.lower() == "exit":
        print("\n[bold yellow]Thank you for using City Intelligence AI![/bold yellow]")
        break

    if not user_input:
        continue

    try:

        # Invoke the agent
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            }
        )

        # Display final response
        print("\n[bold green]Bot:[/bold green]")
        print(result["messages"][-1].content)

        print("\n" + "=" * 55 + "\n")

    except Exception as e:

        print(f"\n[bold red]Error: {e}[/bold red]\n")
