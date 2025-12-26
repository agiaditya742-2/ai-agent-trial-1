# tools/api_tools.py

import requests

class ApiTools:
    """
    A collection of tools for interacting with external APIs.

    This class centralizes all the logic for making API calls to external
    services, such as weather forecasts or news headlines. Each method in this
    class represents a specific tool that the ToolAgent can use.

    For this project, the API calls are simulated to avoid the need for real
    API keys and to ensure the system can run offline. To connect to real APIs,

    """

    def get_weather(self, city):
        """
        Fetches the current weather for a specified city.

        Args:
            city (str): The name of the city.

        Returns:
            str: A string describing the weather, or an error message.
        """
        print(f"[ApiTools] Fetching weather for '{city}'...")
        # In a real implementation, you would make an API call here.
        # Example:
        # try:
        #     response = requests.get(f"https://api.weatherapi.com/v1/current.json?key=YOUR_KEY&q={city}")
        #     response.raise_for_status()
        #     data = response.json()
        #     return f"The weather in {city} is {data['current']['condition']['text']}."
        # except requests.exceptions.RequestException as e:
        #     return f"Sorry, I couldn't fetch the weather. Error: {e}"

        # Simulated response
        return f"The simulated weather in {city.capitalize()} is sunny with a gentle breeze."

    def get_news(self):
        """
        Fetches the latest news headlines.

        Returns:
            str: A string containing a few simulated news headlines.
        """
        print("[ApiTools] Fetching latest news...")
        # In a real implementation, you'd call a news API.
        # Example:
        # response = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_KEY")
        # headlines = [article['title'] for article in response.json()['articles']]
        # return "Here are the top headlines:\n- " + "\n- ".join(headlines)

        # Simulated response
        return (
            "Here are the latest simulated news headlines:\n"
            "- AI agents are becoming increasingly popular in software development.\n"
            "- New Python version released with performance improvements.\n"
            "- Tech companies focus on sustainable energy solutions."
        )

if __name__ == '__main__':
    # Example usage for testing the ApiTools directly

    api_tools = ApiTools()

    # Test case 1: Get weather for a city
    city = "San Francisco"
    weather = api_tools.get_weather(city)
    print(f"Weather request for '{city}':\n{weather}\n")

    # Test case 2: Get latest news
    news = api_tools.get_news()
    print(f"News request:\n{news}\n")
