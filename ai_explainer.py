import ollama

def generate_explanation(summary_text, model = "llama3:latest"):
    prompt = f"""
    Explain the following Zakaat calculation clearly and briefly:
    {summary_text}

    Explain:
    1. What Nisab means
    2. Why Zakaat is 2.5%
    3. Whether the person owes Zakaat or not
    """
    try:
        response = ollama.chat(
            model = model,
            messages = [{
                "role": "user",
                "content": prompt
            }]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"AI explanation unavailable: {e}"
