import pytest
from main import supervisor

RESEARCH = "ask_research_specialist"
ENGINEERING = "ask_engineering_specialist"

# Each case contains:
# question, required specialists, forbidden specialists
TEST_CASES = [
    # Conceptual / research questions
    pytest.param(
        "Explain why transformers use self-attention instead of only RNNs.",
        {RESEARCH},
        set(),
        id="research_transformers",
    ),
    pytest.param(
        "Explain the vanishing gradient problem and how residual connections help.",
        {RESEARCH},
        set(),
        id="research_vanishing_gradients",
    ),

    # Software engineering tasks
    pytest.param(
        "Design a secure REST API for a personal expense tracker. "
        "Cover authentication, authorization, validation, and testing.",
        {ENGINEERING},
        set(),
        id="engineering_expense_api",
    ),
    pytest.param(
        "A FastAPI endpoint is slow because it makes several sequential "
        "HTTP requests. Explain how to diagnose and improve its latency.",
        {ENGINEERING},
        set(),
        id="engineering_api_latency",
    ),

    # Tasks needing both specialists
    pytest.param(
        "I want to build a RAG system for scientific papers. "
        "Explain how retrieval quality affects answer accuracy, then "
        "recommend an architecture and testing strategy.",
        {RESEARCH, ENGINEERING},
        set(),
        id="both_scientific_rag",
    ),
    pytest.param(
        "I am building an AI system to help doctors prioritize patients. "
        "Discuss the risks of model predictions and recommend safeguards, "
        "system architecture, and audit logging.",
        {RESEARCH, ENGINEERING},
        set(),
        id="both_patient_triage",
    ),

    # Ambiguous / unsupported / unnecessary delegation
    pytest.param(
        "Please improve it.",
        set(),
        {RESEARCH, ENGINEERING},
        id="ambiguous_request",
    ),
    pytest.param(
        "What is the exact current price of a stock right now? "
        "No live market data is provided, and you cannot browse. "
        "Explain this limitation and do not delegate.",
        set(),
        {RESEARCH, ENGINEERING},
        id="unsupported_live_data_no_unnecessary_delegation",
    ),
]


def get_called_specialists(result):
    """Extract specialist tool calls from the LangChain message trace."""
    called = set()

    for message in result.get("messages", []):
        # Tool calls are generally recorded on AI messages.
        for tool_call in getattr(message, "tool_calls", []):
            name = tool_call.get("name")
            if name in {RESEARCH, ENGINEERING}:
                called.add(name)

        # Also recognize tool-result messages if present.
        name = getattr(message, "name", None)
        if name in {RESEARCH, ENGINEERING}:
            called.add(name)

    return called


@pytest.mark.parametrize(
    "question, expected_tools, forbidden_tools",
    TEST_CASES,
)
def test_supervisor_behavior(question, expected_tools, forbidden_tools):
    result = supervisor.invoke({
        "messages": [
            {
                "role": "user",
                "content": question,
            }
        ]
    })

    messages = result.get("messages", [])
    assert messages, "The agent returned no messages."

    final_answer = messages[-1].content
    assert isinstance(final_answer, str) and final_answer.strip(), (
        "The agent returned an empty final answer."
    )

    called_tools = get_called_specialists(result)

    # Required delegation: all expected specialists must be called.
    assert expected_tools.issubset(called_tools), (
        f"Expected specialists: {expected_tools}; "
        f"actually called: {called_tools}"
    )

    # Unnecessary or explicitly forbidden delegation.
    assert not (forbidden_tools & called_tools), (
        f"Unexpected specialists called: {forbidden_tools & called_tools}"
    )

    print(f"\nQuestion: {question}")
    print(f"Expected tools: {expected_tools}")
    print(f"Actual tools: {called_tools}")
    print(f"Final answer: {final_answer[:300]}")
