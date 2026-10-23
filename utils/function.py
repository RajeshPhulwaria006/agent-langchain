def run_specialist(agent, task: str) -> str:
    result = agent.invoke({
        "messages": [{"role": "user", "content": task}]
    })
    return str(result["messages"][-1].content)