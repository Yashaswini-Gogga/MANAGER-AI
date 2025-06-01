# agents/requirements_agent.py
from model_api import generate_text

def analyze_requirements(prompt: str, model_name: str) -> str:
    """
    Calls the Requirements Agent model to analyze the user prompt.
    Returns a detailed list of requirements (functional and non-functional).
    """
    system_msg = (
        "You are a Requirements Analysis agent. "
        "Extract all functional and non-functional requirements from the user's prompt. "
        "Be thorough and bullet-point them if possible."
    )
    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt}
    ]
    response = generate_text(messages, model_name)
    return response.strip()
