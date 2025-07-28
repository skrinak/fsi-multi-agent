#!/usr/bin/env python3
"""
Company Analysis Tool

A command-line tool that uses the Strands Agent SDK and Finnhub API to provide comprehensive company analysis.
Combines Finnhub financial data with web scraping for complete company intelligence and research.
"""

import datetime as dt
import urllib.parse
import os
from typing import Dict, Union, Any
from dotenv import load_dotenv

# Third-party imports
from bs4 import BeautifulSoup
import finnhub
import requests
from strands import Agent, tool
from strands.models import BedrockModel
from strands_tools import think, http_request

# Load environment variables
load_dotenv()


@tool
def get_company_info(ticker: str) -> Union[Dict, str]:
    """
    Fetches comprehensive company information using Finnhub API with web scraping fallback.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        
    Returns:
        Dictionary with comprehensive company information or error message
    """
    try:
        if not ticker.strip():
            return {"status": "error", "message": "Ticker symbol is required"}

        # Initialize Finnhub client
        api_key = os.getenv('FINNHUB_API_KEY')
        if not api_key:
            return {"status": "error", "message": "FINNHUB_API_KEY not found in environment variables"}
        
        finnhub_client = finnhub.Client(api_key=api_key)
        ticker = ticker.upper().strip()

        # Get company profile from Finnhub
        try:
            profile = finnhub_client.company_profile2(symbol=ticker)
            if not profile:
                return {"status": "error", "message": f"No company profile found for ticker {ticker}"}
        except Exception as e:
            return {"status": "error", "message": f"Error fetching company profile: {str(e)}"}

        # Get additional company news for recent developments
        try:
            # Get company news from past 30 days
            from_date = (dt.datetime.now() - dt.timedelta(days=30)).strftime("%Y-%m-%d")
            to_date = dt.datetime.now().strftime("%Y-%m-%d")
            news = finnhub_client.company_news(ticker, _from=from_date, to=to_date)
            recent_news_count = len(news) if news else 0
            latest_headline = news[0].get('headline', 'No recent news') if news else 'No recent news'
        except Exception as e:
            recent_news_count = 0
            latest_headline = f"Error fetching news: {str(e)}"

        # Helper function to safely get values
        def safe_get(data, key, default="N/A"):
            value = data.get(key)
            return value if value is not None and value != "" else default

        # Compile comprehensive company information
        company_data = {
            "status": "success",
            "data": {
                "symbol": ticker,
                "company_name": safe_get(profile, 'name'),
                "sector": safe_get(profile, 'finnhubIndustry'),
                "industry": safe_get(profile, 'finnhubIndustry'),  # Finnhub uses same field
                "description": safe_get(profile, 'description', 'Company description not available'),
                "website": safe_get(profile, 'weburl'),
                
                # Market Information
                "market_cap": safe_get(profile, 'marketCapitalization'),
                "shares_outstanding": safe_get(profile, 'shareOutstanding'),
                "country": safe_get(profile, 'country'),
                "currency": safe_get(profile, 'currency'),
                "exchange": safe_get(profile, 'exchange'),
                
                # Company Details
                "ipo_date": safe_get(profile, 'ipo'),
                "employees": safe_get(profile, 'employeeTotal', 'N/A'),
                "phone": safe_get(profile, 'phone'),
                "address": f"{safe_get(profile, 'address', '')} {safe_get(profile, 'city', '')} {safe_get(profile, 'state', '')}".strip(),
                
                # Company Identifiers
                "logo": safe_get(profile, 'logo'),
                "ticker_symbol": ticker,
                
                # Recent Activity
                "recent_news_count": recent_news_count,
                "latest_headline": latest_headline,
                
                # Metadata
                "date": dt.datetime.now().strftime("%Y-%m-%d"),
                "data_source": "Finnhub API",
                "last_updated": dt.datetime.now().isoformat()
            }
        }

        # Try to enhance with web scraping if website is available
        if profile.get('weburl') and profile['weburl'] != 'N/A':
            try:
                web_info = _scrape_company_website(profile['weburl'])
                if web_info.get('status') == 'success':
                    company_data['data']['web_scraped_info'] = web_info['data']
            except Exception as e:
                company_data['data']['web_scraped_info'] = f"Web scraping failed: {str(e)}"

        return company_data

    except Exception as e:
        return {"status": "error", "message": f"Error fetching company info: {str(e)}"}


def _scrape_company_website(url: str) -> Dict[str, Any]:
    """
    Helper function to scrape additional company information from website.
    
    Args:
        url: Company website URL
        
    Returns:
        Dictionary with scraped information
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract basic information
        title = soup.find('title')
        title_text = title.get_text().strip() if title else "No title found"
        
        # Try to find meta description
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        description = meta_desc.get('content', 'No description found') if meta_desc else "No description found"
        
        # Count links and basic page structure
        links = soup.find_all('a', href=True)
        internal_links = [link for link in links if url in link.get('href', '')]
        
        return {
            "status": "success",
            "data": {
                "page_title": title_text,
                "meta_description": description,
                "total_links": len(links),
                "internal_links": len(internal_links),
                "scraped_at": dt.datetime.now().isoformat(),
                "url_scraped": url
            }
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Web scraping failed: {str(e)}",
            "data": {}
        }


@tool
def get_stock_news(ticker: str) -> Union[Dict, str]:
    """
    Fetches comprehensive stock news using Finnhub API with web scraping fallback.
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT')
        
    Returns:
        Dictionary with comprehensive news coverage or error message
    """
    try:
        if not ticker.strip():
            return {"status": "error", "message": "Ticker symbol is required"}

        # Initialize Finnhub client
        api_key = os.getenv('FINNHUB_API_KEY')
        if not api_key:
            return {"status": "error", "message": "FINNHUB_API_KEY not found in environment variables"}
        
        finnhub_client = finnhub.Client(api_key=api_key)
        ticker = ticker.upper().strip()

        # Get company name for context
        try:
            profile = finnhub_client.company_profile2(symbol=ticker)
            company_name = profile.get('name', ticker) if profile else ticker
        except Exception:
            company_name = ticker

        print(f"Searching news for {ticker} ({company_name})")

        all_news = []
        sources_tried = []

        # 1. Try Finnhub company news API
        sources_tried.append("Finnhub API")
        try:
            # Get news from past 7 days for recent coverage
            from_date = (dt.datetime.now() - dt.timedelta(days=7)).strftime("%Y-%m-%d")
            to_date = dt.datetime.now().strftime("%Y-%m-%d")
            
            news_data = finnhub_client.company_news(ticker, _from=from_date, to=to_date)

            if news_data and len(news_data) > 0:
                for item in news_data[:10]:  # Get top 10 recent news items
                    # Convert timestamp to readable date
                    try:
                        news_date = dt.datetime.fromtimestamp(item.get('datetime', 0)).strftime("%Y-%m-%d %H:%M")
                    except:
                        news_date = "Date unavailable"
                    
                    news_item = {
                        "title": item.get("headline", "No title available"),
                        "summary": item.get("summary", "")[:300] if item.get("summary") else "No summary available",
                        "url": item.get("url", ""),
                        "source": item.get("source", "Finnhub"),
                        "date": news_date,
                        "category": item.get("category", "General"),
                        "sentiment": "neutral"  # Finnhub doesn't provide sentiment directly
                    }
                    if news_item["title"] and news_item["url"]:
                        all_news.append(news_item)

                print(f"Found {len(all_news)} news items from Finnhub API")
        except Exception as e:
            print(f"Error with Finnhub API: {str(e)}")

        # 2. Try MarketWatch
        if len(all_news) < 5:
            sources_tried.append("MarketWatch")
            try:
                url = f"https://www.marketwatch.com/investing/stock/{ticker.lower()}"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,images/webp,*/*;q=0.8",
                }

                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Look for news articles
                    articles = soup.select(".article__content")

                    for article in articles[:5]:
                        title_elem = article.select_one(".article__headline")
                        link_elem = article.select_one("a.link")

                        if title_elem and link_elem:
                            title = title_elem.text.strip()
                            link = link_elem.get("href", "")

                            # Make sure link is absolute
                            if link and not link.startswith("http"):
                                link = f"https://www.marketwatch.com{link}"

                            news_item = {
                                "title": title,
                                "summary": "",  # MarketWatch doesn't show summaries in the list
                                "url": link,
                                "source": "MarketWatch",
                                "date": dt.datetime.now().strftime("%Y-%m-%d"),
                            }

                            if (
                                news_item["title"]
                                and news_item["url"]
                                and news_item not in all_news
                            ):
                                all_news.append(news_item)

                    print(f"Found {len(articles)} news items from MarketWatch")
            except Exception as e:
                print(f"Error with MarketWatch: {str(e)}")

        # 3. Try CNBC
        if len(all_news) < 5:
            sources_tried.append("CNBC")
            try:
                # Use search to find news about the company
                search_query = f"{company_name} stock"
                url = f"https://www.cnbc.com/search/?query={urllib.parse.quote(search_query)}&qsearchterm={urllib.parse.quote(search_query)}"

                headers = {
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,images/webp,*/*;q=0.8",
                }

                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Look for search results
                    articles = soup.select(".SearchResult-searchResultContent")

                    for article in articles[:5]:
                        title_elem = article.select_one(".Card-title")
                        link_elem = article.select_one("a.resultlink")

                        if title_elem and link_elem:
                            title = title_elem.text.strip()
                            link = link_elem.get("href", "")

                            news_item = {
                                "title": title,
                                "summary": "",
                                "url": link,
                                "source": "CNBC",
                                "date": dt.datetime.now().strftime("%Y-%m-%d"),
                            }

                            if (
                                news_item["title"]
                                and news_item["url"]
                                and news_item not in all_news
                            ):
                                all_news.append(news_item)

                    print(f"Found {len(articles)} news items from CNBC")
            except Exception as e:
                print(f"Error with CNBC: {str(e)}")

        # 4. Try Seeking Alpha
        if len(all_news) < 5:
            sources_tried.append("Seeking Alpha")
            try:
                url = f"https://seekingalpha.com/symbol/{ticker.upper()}/news"

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,images/webp,*/*;q=0.8",
                }

                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Look for news articles
                    articles = soup.select("article")

                    for article in articles[:5]:
                        title_elem = article.select_one(
                            'a[data-test-id="post-list-item-title"]'
                        )

                        if title_elem:
                            title = title_elem.text.strip()
                            link = title_elem.get("href", "")

                            # Make sure link is absolute
                            if link and not link.startswith("http"):
                                link = f"https://seekingalpha.com{link}"

                            news_item = {
                                "title": title,
                                "summary": "",
                                "url": link,
                                "source": "Seeking Alpha",
                                "date": dt.datetime.now().strftime("%Y-%m-%d"),
                            }

                            if (
                                news_item["title"]
                                and news_item["url"]
                                and news_item not in all_news
                            ):
                                all_news.append(news_item)

                    print(f"Found {len(articles)} news items from Seeking Alpha")
            except Exception as e:
                print(f"Error with Seeking Alpha: {str(e)}")

        # 5. Try Google News as a fallback
        if len(all_news) < 5:
            sources_tried.append("Google News")
            try:
                search_query = f"{company_name} stock news"
                url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}&tbm=nws"

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,images/webp,*/*;q=0.8",
                }

                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")

                    # Try different selectors for Google News
                    news_elements = []
                    selectors = [
                        "div.SoaBEf",
                        "div.dbsr",
                        "g-card",
                        ".WlydOe",
                        ".ftSUBd",
                    ]

                    for selector in selectors:
                        if not news_elements:
                            news_elements = soup.select(selector)

                    # If still no results, try to find any links with news-like content
                    if not news_elements:
                        all_links = soup.find_all("a")
                        for link in all_links:
                            href = link.get("href", "")
                            if (
                                "news" in href.lower()
                                and link.text
                                and len(link.text.strip()) > 20
                            ):
                                news_elements.append(link)

                    for element in news_elements[:5]:
                        # Try to find title and link
                        title = None
                        link = None

                        # If it's a link element directly
                        if element.name == "a":
                            title = element.text.strip()
                            link = element.get("href", "")
                            if link.startswith("/url?q="):
                                link = link.split("/url?q=")[1].split("&")[0]
                        else:
                            # Try to find a link inside the element
                            link_elem = element.find("a")
                            if link_elem:
                                title = link_elem.text.strip()
                                link = link_elem.get("href", "")
                                if link.startswith("/url?q="):
                                    link = link.split("/url?q=")[1].split("&")[0]

                        if title and link and len(title) > 10:
                            news_item = {
                                "title": title,
                                "summary": "",
                                "url": link,
                                "source": "Google News",
                                "date": dt.datetime.now().strftime("%Y-%m-%d"),
                            }

                            if (
                                news_item["title"]
                                and news_item["url"]
                                and news_item not in all_news
                            ):
                                all_news.append(news_item)

                    print(f"Found {len(news_elements)} news items from Google News")
            except Exception as e:
                print(f"Error with Google News: {str(e)}")

        # Print the news items we found
        if all_news:
            print(
                f"\nFound a total of {len(all_news)} news items from {', '.join(sources_tried)}"
            )
            for idx, item in enumerate(all_news[:5], 1):
                print(f"\nNews {idx}:")
                print(f"Title: {item['title']}")
                print(f"Source: {item['source']}")
                print(f"URL: {item['url']}")
                if item["summary"]:
                    print(f"Summary: {item['summary'][:100]}...")

            return {
                "status": "success",
                "data": {
                    "symbol": ticker,
                    "company_name": company_name,
                    "recent_news": all_news[:5],  # Return at most 5 news items
                    "sources_checked": sources_tried,
                    "date": dt.datetime.now().strftime("%Y-%m-%d"),
                },
            }
        else:
            # If no news found, return an empty list
            print(
                f"\nNo news found for {ticker} after checking {', '.join(sources_tried)}"
            )
            return {
                "status": "no_results",
                "message": f"No news found for {ticker} after checking {', '.join(sources_tried)}",
                "data": {
                    "symbol": ticker,
                    "company_name": company_name,
                    "recent_news": [],
                    "sources_checked": sources_tried,
                    "date": dt.datetime.now().strftime("%Y-%m-%d"),
                },
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching news: {str(e)}",
            "data": {
                "symbol": ticker,
                "recent_news": [],
                "date": dt.datetime.now().strftime("%Y-%m-%d"),
            },
        }


def create_initial_messages():
    """Create initial conversation messages."""
    return [
        {
            "role": "user",
            "content": [{"text": "Hello, I need help analyzing a company using comprehensive financial data."}],
        },
        {
            "role": "assistant",
            "content": [
                {
                    "text": "I'm ready to help you analyze companies using Finnhub API and comprehensive research tools. Please provide a ticker symbol for detailed analysis."
                }
            ],
        },
    ]


def create_company_analysis_agent():
    """Create and configure the company analysis agent with Finnhub integration."""
    return Agent(
        system_prompt="""You are a comprehensive company analysis specialist using Finnhub API for institutional-grade data. Follow these steps:

<input>
When user provides a company ticker:
1. Use get_company_info to fetch comprehensive company profile from Finnhub API
2. Use get_stock_news to gather recent news and market sentiment
3. Analyze all available data sources including web scraping when available
4. Provide detailed, investment-grade analysis in the format below
</input>

<output_format>
1. Company Overview:
   - Company Name, Industry, and Exchange Information
   - Business Description and Core Operations
   - Geographic Presence and Market Position
   - Key Company Facts (IPO date, employees, headquarters)

2. Corporate Information:
   - Market Capitalization and Share Structure
   - Exchange Listing and Currency
   - Company Contact Information and Website
   - Recent Corporate Developments

3. Market Intelligence:
   - Recent News Analysis and Market Sentiment
   - Key Headlines and Industry Developments
   - Media Coverage Assessment
   - Market Perception and Investor Interest

4. Data Quality and Sources:
   - Finnhub API Data Coverage
   - Web Scraping Results (if available)
   - News Sources Analyzed
   - Data Freshness and Reliability

5. Investment Research Summary:
   - Company Strengths and Competitive Advantages
   - Key Risk Factors and Challenges
   - Recent Developments Impact Assessment
   - Overall Investment Research Profile

6. Additional Intelligence:
   - Website Analysis Results (if available)
   - Multi-source News Validation
   - Information Quality Assessment
   - Recommended Follow-up Research Areas
</output_format>

<analysis_guidelines>
- Leverage Finnhub's institutional-grade financial data
- Cross-reference multiple news sources for accuracy
- Provide context for any data limitations or gaps
- Focus on actionable investment research insights
- Highlight unique company characteristics and differentiators
- Note data recency and reliability for all sources
- Provide professional-grade analysis suitable for investment decisions
</analysis_guidelines>""",
        model=BedrockModel(model_id="us.amazon.nova-pro-v1:0", region="us-east-1"),
        tools=[get_company_info, get_stock_news, http_request, think],
    )


def main():
    """Main function to run the company analysis tool with Finnhub integration."""
    # Check for API key before starting
    if not os.getenv('FINNHUB_API_KEY'):
        print("❌ Error: FINNHUB_API_KEY not found in environment variables")
        print("Please add your Finnhub API key to a .env file:")
        print("FINNHUB_API_KEY=your_api_key_here")
        return

    # Create and initialize the agent
    company_analysis_agent = create_company_analysis_agent()
    company_analysis_agent.messages = create_initial_messages()

    print("\n🏢 Company Analysis Tool (Finnhub API + Multi-Source Intelligence) 🔍")
    print("=" * 75)
    print("Enter stock ticker symbols for comprehensive company research and analysis")
    print("Type 'exit' to quit\n")

    while True:
        query = input("Company Ticker> ").strip()

        if query.lower() in ['exit', 'quit', 'q']:
            print("\n👋 Goodbye! Happy researching!")
            break

        if not query.strip():
            print("Please enter a company ticker symbol.")
            continue

        print(f"\n🔍 Conducting comprehensive analysis for {query.upper()}...")
        print("-" * 50)

        try:
            # Create the user message with proper Nova format
            user_message = {
                "role": "user",
                "content": [
                    {"text": f"Please provide comprehensive company analysis including market intelligence for: {query}"}
                ],
            }

            # Add message to conversation
            company_analysis_agent.messages.append(user_message)

            # Get response
            response = company_analysis_agent(user_message["content"][0]["text"])
            print(f"{response}\n")

        except Exception as e:
            print(f"❌ Error analyzing {query}: {str(e)}\n")
            
            # Check if it's an API key issue
            if "FINNHUB_API_KEY" in str(e):
                print("💡 Tip: Make sure your .env file contains a valid Finnhub API key")
                break
        finally:
            # Reset conversation after each query
            company_analysis_agent.messages = create_initial_messages()


if __name__ == "__main__":
    main()
