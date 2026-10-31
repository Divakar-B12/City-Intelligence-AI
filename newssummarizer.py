from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser 


load_dotenv()

search_tool = TavilySearchResults(max_result = 3)

# llm = ChatGroq(model = "openai/gpt-oss-120b")

# prompt = ChatPromptTemplate.from_template(
#     """
# You are helpfull assistant

# summarize the following news into clean bullet points

# {news}
# """
# )

# chain = prompt | llm | StrOutputParser()

# news_result = search_tool.run("Tell me upcomming dhanush movies")

# result = chain.invoke({"news" : news_result})

# print(search_tool.description)
print(search_tool.name)
