from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()

web_agent = Agent(
    name="Web Agent",
    model=Gemini(id="gemini-1.5-flash"),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,
    markdown=True
)

finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    model=Gemini(id="gemini-1.5-flash"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True,
                         historical_prices=True, technical_indicators=True)],
    show_tool_calls=True,
    markdown=True
)

agents_team_lead = Agent(
    team=[web_agent, finance_agent],
    model=Gemini(id="gemini-1.5-flash"),
    instructions=["Always include sources", "Use tables to display data", "Only respond to query or questions related to finance"],
    show_tool_calls=True,
    markdown=True
)

agents_team_lead.print_response("Summarize analyst recommendations and share the latest news for Nvidia and Tesla", stream=True)