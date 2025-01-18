from typing import Optional
import finnhub
import os
from datetime import datetime, timedelta
import json
from phi.tools import Toolkit
from phi.utils.log import logger

class FinnhubTools(Toolkit):
    def __init__(self):
        super().__init__(name="finnhub_tools")
        self._client = finnhub.Client(api_key=os.getenv('FINNHUB_API_KEY'))
        self.register(self.get_company_profile)
    
    def get_company_profile(self, query: str) -> str:
        """Get comprehensive company information using Finnhub API.
        
        Args:
            query (str): Company name or symbol (e.g., 'AAPL' or 'Apple Inc.')
        
        Returns:
            str: JSON string containing company information
        """
        try:
            # Extract symbol from query if company name is provided
            company_symbol = query.split('(')[-1].split(')')[0] if '(' in query else query.strip()
            
            logger.info(f"Fetching company profile for: {company_symbol}")
            
            # Get company profile
            profile = self._client.company_profile2(symbol=company_symbol)
            
            # Get company basic financials
            financials = self._client.company_basic_financials(company_symbol, 'all')
            
            # Calculate dates for news (last 30 days)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            # Get company news
            news = self._client.company_news(
                company_symbol,
                _from=start_date.strftime("%Y-%m-%d"),
                to=end_date.strftime("%Y-%m-%d")
            )[:5]
            
            # Get company peers
            peers = self._client.company_peers(company_symbol)

            # Compile comprehensive company information
            company_info = {
                "profile": {
                    "name": profile.get("name", ""),
                    "ticker": profile.get("ticker", ""),
                    "country": profile.get("country", ""),
                    "currency": profile.get("currency", ""),
                    "exchange": profile.get("exchange", ""),
                    "industry": profile.get("finnhubIndustry", ""),
                    "ipo": profile.get("ipo", ""),
                    "logo": profile.get("logo", ""),
                    "marketCap": profile.get("marketCapitalization", ""),
                    "website": profile.get("weburl", "")
                },
                "financials": {
                    "metric": financials.get("metric", {}),
                    "series": financials.get("series", {})
                },
                "recent_news": [
                    {
                        "headline": article.get("headline", ""),
                        "summary": article.get("summary", ""),
                        "datetime": article.get("datetime", ""),
                        "source": article.get("source", ""),
                        "url": article.get("url", "")
                    } for article in news
                ],
                "peers": peers
            }

            return json.dumps(company_info, indent=2)
        
        except Exception as e:
            logger.error(f"Error fetching company information: {str(e)}")
            return json.dumps({"error": f"Error fetching company information: {str(e)}"})