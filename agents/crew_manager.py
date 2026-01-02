import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.tools import WeatherTool, NewsTool
from dotenv import load_dotenv

load_dotenv()

class CrewManager:
    def __init__(self):
        # Initialize Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            verbose=True,
            temperature=0.5,
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
        # Initialize Tools
        self.weather_tool = WeatherTool()
        self.news_tool = NewsTool()

    def classify_intent(self, query):
        """
        Uses the LLM to semantically route the query to the correct category.
        """
        prompt = f"""
        Analyze the user query and classify it into exactly one of these categories: 'weather', 'news', or 'unknown'.
        
        - 'weather': Queries about current weather, temperature, forecast, or atmospheric conditions.
        - 'news': Queries about current events, headlines, world news, or specific topics in the news.
        - 'unknown': Anything else that doesn't fit the above.

        User Query: "{query}"
        
        Return only the category name in lowercase.
        """
        response = self.llm.invoke(prompt)
        category = response.content.strip().lower()
        
        # Basic validation to ensure we get one of the expected strings
        if category in ["weather", "news"]:
            return category
        return "unknown"

    def get_weather_agent(self):
        return Agent(
            role='Weather Specialist',
            goal='Provide accurate weather information for a given location',
            backstory='You are an expert meteorologist with access to real-time weather data.',
            tools=[self.weather_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def get_news_agent(self):
        return Agent(
            role='News Reporter',
            goal='Provide the latest news headlines for a given topic',
            backstory='You are a seasoned journalist who stays on top of global events.',
            tools=[self.news_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def run_crew(self, query, category):
        """
        Creates and runs a crew based on the query category.
        """
        if category == "weather":
            agent = self.get_weather_agent()
            task = Task(
                description=f"Fetch and summarize the weather for the location mentioned in: '{query}'",
                expected_output="A friendly weather report.",
                agent=agent
            )
        elif category == "news":
            agent = self.get_news_agent()
            task = Task(
                description=f"Fetch and summarize the latest news for the topic mentioned in: '{query}'",
                expected_output="A concise list of news headlines.",
                agent=agent
            )
        else:
            return "I'm sorry, I can only handle weather and news requests."

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
