# Agent
> This is basic level agent which takes user input and runs **tools** on the basis of prompt.

---
## Tools

### research tool
- It supposed to be execute when user needs research dependencies

### engineering tool
- It supposed to be execute when user needs to build or develope something

> it is now just have two basic tools but can be addon when needed 

---

## folder structure
```
├── agents
│   ├── __init__.py
│   └── agents.py
├── models
│   ├── __init__.py
│   └── models.py
├── tools
│   ├── __init__.py
│   └── tools.py
├── utils
│   ├── __init__.py
│   └── function.py
├── main.py
└── output.md
```

---
## .env setup
```.env
GROQ_API_KEY="gsk_fINIWEqNq...NvwHQOiqN8EqCC"
```

## Run
```bash
python -m venv venv
pip install -r requirements.txt
python main.py
```

## Author
*~ Rajesh Phulwaria*