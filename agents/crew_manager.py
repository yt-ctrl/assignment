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

    def get_weather_agent(self):
        """Weather specialist sub-agent that automatically uses the weather tool."""
        return Agent(
            role='Weather Specialist',
            goal='Provide accurate and current weather information for any location',
            backstory='You are an expert meteorologist with real-time weather data access. '
                      'When asked about weather, you automatically use your weather tool to fetch current conditions.',
            tools=[self.weather_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            function_calling_llm=self.llm
        )

    def get_news_agent(self):
        """News specialist sub-agent that automatically uses the news tool."""
        return Agent(
            role='News Reporter',
            goal='Provide the latest news headlines and updates on any topic',
            backstory='You are a seasoned journalist with access to breaking news from around the world. '
                      'When asked about news, you automatically use your news tool to fetch the latest headlines.',
            tools=[self.news_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            function_calling_llm=self.llm
        )

    def get_router_agent(self):
        """Main routing agent that delegates to appropriate sub-agents."""
        return Agent(
            role='Query Router',
            goal='Analyze user queries and delegate to the appropriate specialist agent',
            backstory='You are an intelligent routing agent. Your job is to understand what the user needs '
                      'and delegate the query to either the Weather Specialist or News Reporter. '
                      'You do not answer queries yourself - you always delegate to the right specialist.',
            tools=[],
            llm=self.llm,
            verbose=True,
            allow_delegation=True  # Enable delegation to sub-agents
        )

    def run_crew(self, query):
        """
        Creates and runs a crew with main routing agent and specialized sub-agents.
        The router agent automatically delegates to the appropriate sub-agent.
        """
        # Create all agents
        router_agent = self.get_router_agent()
        weather_agent = self.get_weather_agent()
        news_agent = self.get_news_agent()

        # Create task for the router agent
        task = Task(
            description=f"Analyze this query and delegate to the appropriate specialist: '{query}'",
            expected_output="A complete answer to the user's query obtained from the appropriate specialist.",
            agent=router_agent
        )

        # Create crew with all agents
        crew = Crew(
            agents=[router_agent, weather_agent, news_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
