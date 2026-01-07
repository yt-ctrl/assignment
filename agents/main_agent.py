from agents.crew_manager import CrewManager
from utils.vector_db import VectorDB

class MainAgent:
    def __init__(self):
        """
        Initializes the main agent with CrewAI manager and vector database.
        """
        self.crew_manager = CrewManager()
        self.db = VectorDB()

    def handle_query(self, query):
        """
        Main entry point for handling user queries.
        Checks cache first, then runs the autonomous CrewAI agent.
        """
        # 1. Check the vector database for a previously answered query
        cached_response = self.db.get_cached_response(query)
        if cached_response:
            return f"[From Cache] {cached_response}"

        # 2. Run the autonomous CrewAI agent (it will automatically select and use tools)
        try:
            response = self.crew_manager.run_crew(query)
            # Convert CrewOutput to string if necessary
            response_str = str(response)
        except Exception as e:
            return f"An error occurred while processing your request: {str(e)}"

        # 3. Store the response in the vector database
        if "Error" not in response_str and "Sorry" not in response_str:
            self.db.save_query_response(query, response_str)
            
        return response_str

if __name__ == "__main__":
    # Simple CLI for testing
    agent = MainAgent()
    print("Multi-Agent System Ready! (Type 'exit' to quit)")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            break
        print(f"Agent: {agent.handle_query(user_input)}")
