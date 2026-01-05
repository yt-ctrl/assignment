# Multi-Agent AI System (CrewAI + Gemini)

This project implements a multi-agent system using the **CrewAI** framework and **Google Gemini (2.5 Flash)** LLM. It handles weather and news queries, interacts with external APIs, and utilizes a vector database (ChromaDB) for semantic caching.

## Features

- **CrewAI Framework**: Orchestrates specialized agents for weather and news.
- **Gemini 2.5 Flash**: Powers the reasoning and natural language generation of the agents.
- **Semantic Routing**: Uses LLM-based intent classification to route queries to the correct agent, replacing simple keyword matching.
- **Weather Agent**: Uses a custom `WeatherTool` to fetch data from OpenWeatherMap.
- **News Agent**: Uses a custom `NewsTool` to fetch headlines from GNews.
- **Vector Database Integration**: Uses ChromaDB to cache query-response pairs for faster retrieval and reduced API/LLM costs.

## Prerequisites

- Python 3.10+
- OpenWeatherMap API Key
- GNews API Key
- Google AI (Gemini) API Key ([Get it here](https://aistudio.google.com/app/apikey))

## Setup Instructions

1. **Clone the repository**.
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/Scripts/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Configure Environment Variables**:
   - Copy `.env.example` to `.env`.
   - Add your API keys:
   ```env
   OPENWEATHER_API_KEY=your_key
   GNEWS_API_KEY=your_key
   GOOGLE_API_KEY=your_gemini_key
   ```

## Usage

Run the main application:
```bash
python main.py
```

## Project Structure

- `agents/`:
    - `crew_manager.py`: Defines CrewAI agents, tasks, and the crew setup.
    - `main_agent.py`: The entry point for query routing and caching logic.
- `utils/`:
    - `tools.py`: Custom CrewAI tools for Weather and News APIs.
    - `vector_db.py`: ChromaDB integration for semantic caching.
- `tests/`:
    - `test_agents.py`: Pytest suite for validating agents, tools, and database.
- `main.py`: CLI interface.

## Test Cases and Results

The system includes a comprehensive test suite in [tests/test_agents.py](tests/test_agents.py).

### Test Cases:
1. **`test_intent_classification`**: Validates the semantic router's ability to distinguish between weather, news, and unrelated queries.
2. **`test_vector_db_caching`**: Verifies that the ChromaDB integration correctly stores and retrieves cached responses.
3. **`test_weather_tool`**: Tests the integration with the OpenWeatherMap API.
4. **`test_news_tool`**: Tests the integration with the GNews API.

### Sample Test Results:
```text
====================== test session starts ======================
platform win32 -- Python 3.11.x, pytest-8.x.x
collected 4 items

tests/test_agents.py ....                                 [100%]

======================= 4 passed in 4.52s =======================
```
