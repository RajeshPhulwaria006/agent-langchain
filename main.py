from langchain.agents import create_agent
from models import model
from tools import ask_research_specialist, ask_engineering_specialist

# main agent
supervisor = create_agent(
    model=model,
    tools=[
        ask_research_specialist,
        ask_engineering_specialist,
    ],
    system_prompt="""
    You are the supervisor for an AI engineering assistant.

    1. Understand the user's goal.
    2. Delegate to specialists when their expertise is useful.
    3. You may consult both specialists.
    4. Compare their findings and resolve inconsistencies.
    5. Return one coherent answer with assumptions and limitations.

    Do not claim a specialist performed an action that it did not.
    """,
)

if __name__ == "__main__":
    task = input("What should the agents analyze? \n:").strip()

    if not task:
        raise SystemExit("Enter a task.")

    result = supervisor.invoke({
        "messages": [{"role": "user", "content": task}]
    })

    print("\nFinal answer:")
    print(result["messages"][-1].content)

