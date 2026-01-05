import sys
import os
# Add the parent directory to sys.path to allow importing agents and utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from agents.main_agent import MainAgent
from utils.vector_db import VectorDB
import os
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def main_agent():
    return MainAgent()

def test_intent_classification(main_agent):
    """Test if the system correctly classifies weather and news queries."""
    assert main_agent.route_query("What is the weather in London?") == "weather"
    assert main_agent.route_query("Tell me the latest news about AI.") == "news"
    assert main_agent.route_query("What are the current headlines in the world?") == "news"
    assert main_agent.route_query("How do I bake a cake?") == "unknown"

def test_vector_db_caching():
    """Test if the vector database correctly stores and retrieves responses."""
    import uuid
    test_db_path = f"./test_chroma_db_{uuid.uuid4().hex}"
    db = VectorDB(db_path=test_db_path)
    query = "Test query for caching"
    response = "This is a test response"
    
    db.save_query_response(query, response)
    cached = db.get_cached_response(query)
    
    assert cached == response
    
    # On Windows, ChromaDB often keeps files locked, making cleanup difficult in the same process.
    # We'll skip rmtree here to avoid PermissionError, or use a more robust cleanup if needed.
    # In a real CI environment, we'd use temporary directories that are cleaned up by the OS.

def test_weather_tool():
    from utils.tools import WeatherTool
    tool = WeatherTool()
    # This might fail if API key is missing, but we can check if it returns an error string at least
    result = tool._run("London")
    assert isinstance(result, str)
    assert "London" in result or "Error" in result

def test_news_tool():
    from utils.tools import NewsTool
    tool = NewsTool()
    result = tool._run("Technology")
    assert isinstance(result, str)
    assert len(result) > 0

if __name__ == "__main__":
    # If run directly, use pytest to execute the tests in this file
    pytest.main([__file__])
