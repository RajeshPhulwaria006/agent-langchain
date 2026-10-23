from langchain.agents import create_agent
from models import model

research_agent = create_agent(
    model=model,
    tools=[],
    system_prompt="""
    You are a research specialist.
    Explain concepts, assumptions, evidence requirements,
    limitations, and unresolved questions.
    Never claim to have browsed sources you did not access.
    """,
)

engineering_agent = create_agent(
    model=model,
    tools=[],
    system_prompt="""
    You are a software engineering specialist.
    Analyze architecture, APIs, validation, security,
    testing, maintainability, and deployment trade-offs.
    State assumptions when requirements are incomplete.
    """,
)