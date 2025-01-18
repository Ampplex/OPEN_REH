from phi.agent import Agent, Tool
from phi.model.google import Gemini
import finnhub

class FinnhubTool(Tool):  # Inheriting from Tool class
    def __init__(self, api_key):
        self.client = finnhub.Client(api_key=api_key)

    def general_news(self, category="general", min_id=0):
        try:
            news = self.client.general_news(category, min_id=min_id)
            if isinstance(news, list):
                formatted_news = "\n".join(
                    [f"Title: {article['headline']}\nSummary: {article['summary']}\nURL: {article['url']}\n"
                     for article in news[:5]]
                )
                return formatted_news
            return "No news available."
        except Exception as e:
            return f"Error fetching news: {e}"

# Initialize the FinnhubTool
finnhub_tool = FinnhubTool(api_key="ctuo7lhr01qg98tdn5qgctuo7lhr01qg98tdn5r0")

# Define the Agent
finance_agent = Agent(
    name="Finance News Agent",
    role="Provide financial insights and news.",
    model=Gemini(id="gemini-1.5-flash"),
    tools=[finnhub_tool],
    show_tool_calls=True,
    markdown=True
)

if __name__ == "__main__":
    finance_agent.print_response("Give financial news of today")