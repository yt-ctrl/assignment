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

    def get_autonomous_agent(self):
        """Creates an agent with access to all tools that autonomously decides which to use."""
        return Agent(
            role='Multi-Purpose Assistant',
            goal='Answer user queries by automatically selecting and using the appropriate tools',
            backstory='You are an intelligent assistant with access to weather and news tools. '
                      'Analyze the user query and automatically call the appropriate tool to get the information needed. '
                      'Use the Weather Tool for weather-related queries and the News Tool for news-related queries.',
            tools=[self.weather_tool, self.news_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            function_calling_llm=self.llm  # Enable automatic function calling
        )

    def run_crew(self, query):
        """
        Creates and runs a crew that autonomously determines which tool to use.
        """
        agent = self.get_autonomous_agent()
        task = Task(
            description=f"Answer the following query by automatically using the appropriate tool: '{query}'",
            expected_output="A clear and helpful response with the requested information.",
            agent=agent
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
