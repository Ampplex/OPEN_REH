import finnhub

class FinnhubTool:
    def __init__(self, api_key):
        self.client = finnhub.Client(api_key=api_key)

    def general_news(self, category, min_id=0):
        return self.client.general_news(category, min_id=min_id)


if __name__ == "__main__":
    # Initialize the FinnhubTool
    finnhub_tool = FinnhubTool(api_key="ctuo7lhr01qg98tdn5qgctuo7lhr01qg98tdn5r0")
    
    # Fetch general financial news
    news = finnhub_tool.general_news(category="general", min_id=0)
    
    print(news)