# agents/coder_agent.py
from model_api import generate_text

def generate_code(design: str, model_name: str) -> str:
    """
    Calls the Coder Agent model with the design specification.
    Returns the generated code (e.g. HTML/CSS/JS or Python code).
    """
    system_msg = (
        "You are a Coding agent. Based on the design specification provided, generate the complete source code. "
        "If it's a website, output HTML/CSS/JS files. If it's a Python application, output .py files. "
        "Provide code in markdown-style fenced blocks with the appropriate file extension."
    )
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": design}
    ]
    response = generate_text(messages, model_name)
    return response.strip()
