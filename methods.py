from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.tools.wikipedia import WikipediaTools
from dotenv import load_dotenv
import json
from finnhub_tools import FinnhubTools 

load_dotenv()

web_agent = Agent(
    name="Web Agent",
    model=Gemini(id="gemini-1.5-flash"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=False,
    markdown=False
)

# Create WikipediaTools instance correctly
wikipedia_tools = WikipediaTools()  # Without knowledge_base, it will register search_wikipedia method
finnhub_tools = FinnhubTools()

finance_agent1 = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=Gemini(id="gemini-1.5-flash"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True,
                         historical_prices=True, technical_indicators=True)],
    instructions=["Answer in paragraph format only"],
    show_tool_calls=False,
    markdown=False,
)

# Finance Agent 2 - Finnhub Tools
finance_agent2 = Agent(
    name="Finance Research Agent",
    role="Financial Data and Analysis Expert",
    model=Gemini(id="gemini-1.5-flash"),
    tools=[finnhub_tools],
    instructions=[
        "You are a financial expert providing comprehensive company information and analysis.",
        "When asked about a company, extract the company's stock symbol and use get_company_profile to fetch data.",
        "Format the response in a clear, organized manner highlighting key metrics and insights.",
        "For company queries, always include: company profile, key financials, recent news, and peer comparison.",
        "If the company name is provided without a symbol, try to extract or ask for the symbol."
    ],
    show_tool_calls=False,
    markdown=False
)


# Improved finance_agent3 configuration
finance_agent3 = Agent(
    name="Research Finance Agent",
    role="Financial and Company Research Specialist",
    model=Gemini(id="gemini-1.5-flash"),
    tools=[
        WikipediaTools,
    ],
    instructions=[
        "You are a research specialist focused on providing comprehensive information about companies and financial topics.",
        "Use the Wikipedia search tool to get information about companies and financial concepts.",
        "Always attempt to use the search tools before stating you cannot answer.",
        "Combine information from multiple sources when possible.",
        "Include sources for the information provided."
    ],
    show_tool_calls=False,
    markdown=False
)


# finance_agent4 = Agent(
#     name="Finance Agent",
#     role="Get financial data",
#     model=Gemini(id="gemini-1.5-flash"),
#     tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True,
#                          historical_prices=True, technical_indicators=True)],
#     show_tool_calls=False,
#     markdown=False
# )

def print_resp():
    # print response of all the agents

    resp = finance_agent2.run("What is the company information for Apple Inc. (AAPL)?", stream=False)
    resp1 = resp.content
    resp1 = str(resp1).split("\n")
    tmp_str = ""
    for sent in resp1:
        for c in sent:
            if c.isalpha() or c == ' ':
                tmp_str += c
    print(tmp_str)


print_resp()

    # return json.dumps({
    #     "finance_agent": finance_agent1.agent_data,
    #     # "finance_agent": finance_agent1.print_response("What is the company information for Apple Inc. (AAPL)?", stream=True),
    #     # "finance_agent": finance_agent2.print_response("What is the company information for Apple Inc. (AAPL)?", stream=True),
    #     # "finance_agent": finance_agent3.print_response("What is the company information for Apple Inc. (AAPL)?", stream=True),
    # })