import json
import finnhub
from phi.agent import Agent
from phi.model.google import Gemini
from dotenv import load_dotenv

load_dotenv()

# Initialize the finnhub client with the API key
finnhub_client = finnhub.Client(api_key="ctuo7lhr01qg98tdn5qgctuo7lhr01qg98tdn5r0")

def get_top_news_stories(num_stories: int = 5) -> str:
    """Fetches top news stories in the specified format using the Finnhub API.

    Args:
        num_stories (int): Number of stories to return. Defaults to 5.

    Returns:
        str: JSON string containing the top news stories.
    """
    # Fetch the top news stories from Finnhub (general category)
    response = finnhub_client.general_news('general', min_id=0)
    
    # Format the response to match the desired structure
    stories = []
    for story in response[:num_stories]:
        formatted_story = {
            "category": story.get("category", "general"),
            "datetime": story.get("datetime", 0),
            "headline": story.get("headline", ""),
            "id": story.get("id", 0),
            "image": story.get("image", ""),
            "related": story.get("related", ""),
            "source": story.get("source", ""),
            "summary": story.get("summary", ""),
            "url": story.get("url", "")
        }
        stories.append(formatted_story)
    
    return json.dumps(stories)

# Initialize the agent with the tool
agent = Agent(tools=[get_top_news_stories],model=Gemini(id="gemini-1.5-flash"), show_tool_calls=True, markdown=True)

# Ask the agent to summarize the top 5 news stories
agent.print_response("Give latest headlines", stream=True)