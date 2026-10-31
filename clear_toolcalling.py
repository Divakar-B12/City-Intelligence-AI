from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.tools import tool
from langchain_core.messages import HumanMessage 

# from rich import print

load_dotenv()

# 1 creating a tool 

@tool
def get_text_length(text: str) -> int:
    """
    Returns the number of character in a given text
    """
    return len(text)

tools = {
    "get_text_length" : get_text_length
}

llm = ChatGroq(model = "openai/gpt-oss-120b")

# 2 Tool Binding

llm_with_tool = llm.bind_tools([get_text_length])


message = []
prompt = input("You : ")
query = HumanMessage(prompt)
message.append(query)
# print(message)

result = llm_with_tool.invoke(message)

message.append(result)

if result.tool_calls:
    tool_name = result.tool_calls[0]["name"]
    tool_message = tools[tool_name].invoke(result.tool_calls[0])
    message.append(tool_message)
    # print(message)
 
result = llm_with_tool.invoke(message)

print(result.content)