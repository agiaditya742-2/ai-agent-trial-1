# tools/internet_tools.py

"""
Provides tools for interacting with the live internet, including web searches
and reading website content.
"""

import json
import logging
import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [%(levelname)s] - (InternetTools) - %(message)s')

def search_web(query: str, api_key: str = None, search_engine_id: str = None):
    """
    Performs a web search using the Google Custom Search JSON API.

    Args:
        query (str): The search query.
        api_key (str): The Google API key.
        search_engine_id (str): The Custom Search Engine ID.

    Returns:
        str: A JSON string of search results, or an error message.
    """
    if not api_key or not search_engine_id:
        logging.warning("API key or Search Engine ID is not set. Using simulated search.")
        return json.dumps({
            "results": [{"title": "Simulated Search Result", "url": "https://example.com", "snippet": "This is a placeholder result."}],
            "provider": "Simulation"
        }, indent=2)

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': search_engine_id,
        'num': 5  # Request top 5 results
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        results = response.json().get('items', [])

        # Format the results for the agent
        formatted_results = [
            {"title": item.get('title'), "url": item.get('link'), "snippet": item.get('snippet')}
            for item in results
        ]
        return json.dumps({"results": formatted_results, "provider": "Google"}, indent=2)

    except requests.exceptions.RequestException as e:
        logging.error(f"Error during web search: {e}")
        return f"Error: Could not perform web search. Details: {e}"

def read_website_content(url: str) -> str:
    """
    Reads the main text content from a given URL.

    Args:
        url (str): The URL of the website to read.

    Returns:
        str: The extracted text content, or an error message.
    """
    logging.info(f"Fetching content from URL: {url}")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Use BeautifulSoup to parse the HTML and extract text
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove script and style elements
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        # Get text and clean it up
        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        # Truncate for brevity in agent's context
        return text[:2000] + "..." if len(text) > 2000 else text

    except requests.exceptions.RequestException as e:
        logging.error(f"Error reading website content from {url}: {e}")
        return f"Error: Could not read website content. Details: {e}"

if __name__ == '__main__':
    print("--- Testing Live Internet Tools ---")

    # Test Case 1: Search (will use simulation as no key is provided)
    print("\n[1] Testing Web Search (Simulated)")
    search_results = search_web("What is artificial intelligence?")
    print(search_results)

    # Test Case 2: Read Website Content
    print("\n[2] Testing Website Reading")
    # Using a reliable and simple website for the test
    content = read_website_content("http://info.cern.ch/hypertext/WWW/TheProject.html")
    print(f"Content from CERN website:\n---\n{content[:300]}...\n---")

    print("\n--- Internet Tools Test Complete ---")
