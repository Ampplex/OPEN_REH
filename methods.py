from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from phi.tools.wikipedia import WikipediaTools
from dotenv import load_dotenv
import json
from finnhub_tools import FinnhubTools 
import tiktoken

load_dotenv()

def count_tokens(text: str) -> int:
    """
    Count tokens using tiktoken with cl100k_base encoding (closest to Gemini's tokenization)
    """
    try:
        # Use cl100k_base encoding (similar to what Gemini uses)
        encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(text)
        return len(tokens)
    except Exception as e:
        print(f"Error counting tokens: {e}")
        # Fallback to approximate count
        return len(text.split())

web_agent = Agent(
    name="Web Agent",
    model=Gemini(id="gemini-1.5-flash"),
    tools=[DuckDuckGo, YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True,
                         historical_prices=True, technical_indicators=True)],
    instructions=["Always include sources", "You are a finance agent who extracts information from the web", "Max words should be 50"],
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
    instructions=["Format the response in a clear, organized manner highlighting key metrics and insights.",
                  "You are a research specialist focused on providing comprehensive information about companies and financial topics", "Max words should be 50"],
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
        "You are a research specialist focused on providing comprehensive information about companies and financial topics.",
        "When asked about a company, extract the company's stock symbol and use get_company_profile to fetch data.",
        "Format the response in a clear, organized manner highlighting key metrics and insights.",
        "Max words should be 50"
        # "For company queries, always include: company profile, key financials, recent news, and peer comparison.",
        # "If the company name is provided without a symbol, try to extract or ask for the symbol."
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
        "Format the response in a clear, organized manner highlighting key metrics and insights.",
        "Use the Wikipedia search tool to get information about companies and financial concepts.",
        "Max words should be 50"
        # "Always attempt to use the search tools before stating you cannot answer.",
        # "Combine information from multiple sources when possible.",
        # "Include sources for the information provided."
    ],
    show_tool_calls=False,
    markdown=False
)

def run_agent(agent, prompt):
    import time  # For measuring response time
    
    start_time = time.time()  # Record start time
    response = agent.run(prompt, stream=False)  # Get the response
    
    response_time = time.time() - start_time  # Calculate response time
    token_usage_count = count_tokens(response.get_content_as_string())

    response_content = response.get_content_as_string() if hasattr(response, "get_content_as_string") else str(response)
    
    return response_content, token_usage_count, response_time


def print_responses():
    prompt = "What is the company information for Apple Inc. (AAPL)?"
    agents = [finance_agent1, finance_agent2, finance_agent3]
    
    # Run each agent and collect their responses
    responses_with_details = []
    
    # Run each agent and collect their responses, token counts, and response times
    for agent in agents:
        response_content, token_count, response_time = run_agent(agent, prompt)
        cleaned_response = response_content.replace('*', '')  # Remove asterisks
        responses_with_details.append((cleaned_response, token_count, response_time))
    
    return responses_with_details

final_response = print_responses()

# Print the details for each agent's response
for idx, (response, tokens, time_taken) in enumerate(final_response):
    print(f"Agent {idx + 1} Response: {response}")
    print(f"Agent {idx + 1} Tokens Used: {tokens if tokens is not None else 'Not Provided'}")
    print(f"Agent {idx + 1} Response Time: {time_taken:.2f} seconds\n")

    #     "finance_agent": finance_agent1.agent_data,
    #     # "finance_agent": finance_agent1.print_response("What is the company information for Apple Inc. (AAPL)?", stream=True),
    #     # "finance_agent": finance_agent2.print_response("What is the company information for Apple Inc. (AAPL)?", stream=True),
    #     # "finance_agent": finance_agent3.print_response("What is the company information for Apple Inc. (AAPL)?", stream=True),