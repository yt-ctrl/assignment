import os
import requests
from crewai.tools import BaseTool
from dotenv import load_dotenv

load_dotenv()

class WeatherTool(BaseTool):
    name: str = "Weather Tool"
    description: str = "Fetches current weather details for a specified location."

    def _run(self, location: str) -> str:
        api_key = os.getenv("OPENWEATHER_API_KEY")
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": location,
            "appid": api_key,
            "units": "metric"
        }
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            if response.status_code == 200:
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                return f"The weather in {location} is {description} with {temp}°C."
            return f"Error: {data.get('message', 'Unknown error')}"
        except Exception as e:
            return f"Error fetching weather: {str(e)}"

class NewsTool(BaseTool):
    name: str = "News Tool"
    description: str = "Fetches the latest news headlines for a specified topic."

    def _run(self, topic: str) -> str:
        api_key = os.getenv("GNEWS_API_KEY")
        base_url = "https://gnews.io/api/v4/search"
        params = {
            "q": topic,
            "apikey": api_key,
            "lang": "en",
            "max": 3
        }
        try:
            response = requests.get(base_url, params=params)
            data = response.json()
            if response.status_code == 200:
                articles = data.get('articles', [])
                if not articles: return "No news found."
                return "\n".join([f"- {a['title']} ({a['source']['name']})" for a in articles])
            return f"Error: {data.get('errors', 'Unknown error')}"
        except Exception as e:
            return f"Error fetching news: {str(e)}"
