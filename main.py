import sys
import os
from agents.main_agent import MainAgent
from dotenv import load_dotenv

# Add the current directory to sys.path to ensure imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    load_dotenv()
    
    # Check for API keys
    if not os.getenv("OPENWEATHER_API_KEY") or not os.getenv("GNEWS_API_KEY"):
        print("Warning: API keys are missing in .env file.")
        print("Please copy .env.example to .env and add your keys.")
    
    agent = MainAgent()
    print("--- Multi-Agent AI System ---")
    print("I can help you with weather and news.")
    print("The system uses semantic routing to understand your intent.")
    print("Type 'exit' to quit.")
    
    while True:
        try:
            user_input = input("\nUser: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("Goodbye!")
                break
            
            response = agent.handle_query(user_input)
            print(f"Agent: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
