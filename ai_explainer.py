import subprocess

def generate_explanation(summary_text, model = "llama3:latest"):
    prompt = f"""
    Explain the following Zakaat calculation clearly and briefly:
    {summary_text}
    Explain why Zakaat is 2.5% and what Nisab means
    """
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input = prompt.encode(),
            stdout = subprocess.PIPE,
            strderr = subprocess.PIPE
        )
        return result.stdout.decode()
    except:
        return "AI explanation unavailable"
