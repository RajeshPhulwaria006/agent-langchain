# Agent LangChain

A simple multi-agent AI assistant built with **LangChain, Groq, and Python**. A supervisor agent analyzes a user's request, delegates work to research and software engineering specialists, and combines their responses into a single answer.

The project also includes a lightweight `pytest` evaluation suite to test specialist routing across different types of tasks.

## Features

- **Supervisor agent:** Understands the user's request and decides whether to delegate.
- **Research specialist:** Handles conceptual explanations, assumptions, evidence requirements, and limitations.
- **Engineering specialist:** Analyzes software architecture, APIs, validation, security, testing, and deployment trade-offs.
- **Tool-based delegation:** Exposes both specialists as tools available to the supervisor.
- **Evaluation suite:** Tests routing behavior across research, engineering, cross-disciplinary, and ambiguous or unsupported requests.
- **Groq-powered inference:** Uses `openai/gpt-oss-120b` through `ChatGroq`.

## Architecture

```text
User Request
     |
     v
Supervisor Agent
     |
     +-----------------------+
     |                       |
     v                       v
Research Specialist    Engineering Specialist
     |                       |
     +-----------+-----------+
                 |
                 v
       Combined Final Answer
```

The supervisor can call either specialist or both, depending on its interpretation of the task. The specialists currently generate responses using the same underlying model and do not have independent tools for browsing or executing software operations.

## Project Structure

```text
├── agents
│   ├── __init__.py
│   └── agents.py
├── models
│   ├── __init__.py
│   └── models.py
├── reports
│   └── evaluation.json
├── tools
│   ├── __init__.py
│   └── tools.py
├── utils
│   ├── __init__.py
│   └── function.py
├── .gitignore
├── README.md
├── agent_evals.py
├── main.py
├── output.md
└── requirements.txt
```

- `main.py` — creates the supervisor agent and accepts user input.
- `agents/agents.py` — defines the research and engineering specialists.
- `tools/tools.py` — exposes specialists as tools for the supervisor.
- `models/models.py` — configures the Groq chat model.
- `utils/function.py` — invokes a specialist and returns its response.
- `agent_evals.py` — contains automated routing and response checks.
- `output.md` — example agent output.
- `requirements.txt` — Python dependency list.
- `.env` — stores the API key locally; do not commit it.

## Requirements

- Python 3.10 or a compatible version supported by your installed dependencies
- A Groq API key
- Internet access for API requests

## Installation and Setup

Clone the repository and enter the project directory:

```bash
git clone https://github.com/RajeshPhulwaria006/agent-langchain.git
cd agent-langchain
```

Create and activate a virtual environment.

**Windows PowerShell**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**Linux / macOS**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the repository root:

```dotenv
GROQ_API_KEY=your_groq_api_key_here
```

Ensure `.env` is included in `.gitignore`.

## Run the Agent

Start the application:

```bash
python main.py
```

Enter a question or task when prompted. The supervisor will decide whether to call its specialist tools and then print the final answer.

Example input:

```text
Design a secure REST API for a personal expense tracker.
Explain authentication, authorization, validation, and testing.
```

## Agent Evaluation

The evaluation suite is implemented in `agent_evals.py` using `pytest`. It runs the supervisor against eight representative questions and checks for a non-empty response and expected specialist calls.

### Test Categories

| Category | Cases | Evaluation goal |
|---|---:|---|
| Conceptual / Research | 2 | Research specialist routing |
| Software Engineering | 2 | Engineering specialist routing |
| Cross-disciplinary | 2 | Delegation to both specialists |
| Ambiguous / Unsupported | 2 | Avoiding unnecessary delegation and handling limitations |

### Run Tests Locally

Install the test dependencies:

```bash
pip install pytest pytest-json-report
```

Run all evaluation cases:

```bash
pytest -v agent_evals.py
```

Stop at the first failure to inspect its traceback:

```bash
pytest -v -x agent_evals.py
```

The tests make live calls to the configured Groq model. Ensure your `.env` is loaded and the API key is valid before running them.

### Save a JSON Evaluation Report

Generate a machine-readable report:

```bash
pytest -v agent_evals.py \
  --json-report \
  --json-report-file=reports/evaluation.json
```

On Windows PowerShell, create the report directory first:

```powershell
New-Item -ItemType Directory -Force reports
pytest -v agent_evals.py --json-report --json-report-file=reports/evaluation.json
```

The JSON report records test outcomes and failure details. It can be inspected locally or uploaded as a GitHub Actions artifact. The `reports/` directory does not need to be committed unless you want to version a particular evaluation snapshot.

### Latest Evaluation Results

The following results are from one local test run:

| Test case | Result |
|---|---|
| `research_transformers` | Passed |
| `research_vanishing_gradients` | Passed |
| `engineering_expense_api` | Failed |
| `engineering_api_latency` | Failed |
| `both_scientific_rag` | Failed |
| `both_patient_triage` | Failed |
| `ambiguous_request` | Passed |
| `unsupported_live_data_no_unnecessary_delegation` | Passed |
| **Total** | **4 passed, 4 failed** |

**Pass rate: 50%** for this particular run.

These results are an initial evaluation snapshot, not a claim that the agent is production-ready. The four failed cases need to be investigated using their individual tracebacks and recorded tool calls.

### What the Tests Measure

- Whether the final response is non-empty.
- Whether required specialist tools were called.
- Whether explicitly forbidden tools were avoided in selected test cases.

These checks measure basic routing behavior. They do not yet establish factual accuracy, answer quality, safety, or end-to-end task success. Because the model is nondeterministic, results can vary between runs.

## Future Improvements

- Add task-success and answer-quality scoring.
- Measure latency and API usage.
- Record specialist tool calls and failure reasons for every case.
- Improve routing instructions and test consistency across repeated runs.
- Add GitHub Actions to execute evaluations automatically on pushes and pull requests.

## Tech Stack

- Python
- LangChain
- Groq API
- `langchain-groq`
- `python-dotenv`
- `pytest`
- `pytest-json-report`

## Author

**Rajesh Phulwaria**

GitHub: [RajeshPhulwaria006](https://github.com/RajeshPhulwaria006)
