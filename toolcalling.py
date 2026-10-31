from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.tools import tool

# from rich import print

load_dotenv()

# 1 creating a tool 

@tool
def get_text_lengh(text: str) -> int:
    """
    Returns the number of character in a given text
    """
    return len(text)

llm = ChatGroq(model = "openai/gpt-oss-120b")

# 2 Tool Binding

llm_with_tool = llm.bind_tools([get_text_lengh])

result = llm_with_tool.invoke("Return the number of character in a given text : 'hello how are you'")

# print(result.tool_calls[0])

# if result.tool_calls:
#     tool_call = result.tool_calls[0]

# tool_name = tool_call["name"]
# tool_args = tool_call["args"]


# tool_result = get_text_lengh.invoke(tool_args)

# final_response = llm_with_tool.invoke(f"the length of text is {tool_result}")


# print(final_response.content)


print(result.tool_calls[0])

print(get_text_lengh.invoke({'name': 'get_text_lengh', 'args': {'text': 'hello how are you'}, 'id': 'fc_470c2c83-5eb7-4fc2-aba9-7f66e873e200', 'type': 'tool_call'}))
