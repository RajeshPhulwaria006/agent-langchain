from langchain.agents import create_agent
from langchain.tools import tool
from utils import run_specialist
from agents import research_agent, engineering_agent

@tool
def ask_research_specialist(task: str) -> str:
    """Delegate conceptual research and evidence analysis."""
    return run_specialist(research_agent, task)


@tool
def ask_engineering_specialist(task: str) -> str:
    """Delegate software architecture and implementation analysis."""
    return run_specialist(engineering_agent, task)
