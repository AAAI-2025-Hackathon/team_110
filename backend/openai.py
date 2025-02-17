import openai
import os


# Load OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Store key in environment variables

# Misinformation categories
misinfo_categories = [
    "Basic factual inaccuracies",
    "Contradiction",
    "Missing Context/Inaccurate history",
    "Irrelevant detail",
    "Anecdotal evidence",
    "Bad math/Incorrect science",
    "Causation vs Correlation confusion",
    "Physically/Scientifically impossible",
    "Extremely improbable scenario"
]

def generate_summaries(news_article, fake_level):
    """
    Generates a real and fake summary based on the given difficulty level.
    """
    # Select misinformation categories based on difficulty level
    selected_misinfo = misinfo_categories[:fake_level]

    # Create a structured prompt
    prompt = f"""
    You are an AI that generates both accurate and misleading summaries of news articles.

    ### TASK
    - Given a news article, generate:
      1. A **real** summary (accurate and unbiased).
      2. A **fake** summary using **one or more of these misinformation techniques**:
        {', '.join(selected_misinfo)}

    - Also, explain the **changes made** in the fake summary.

    ### INPUT ARTICLE:
    {news_article}

    ### OUTPUT FORMAT (JSON)
    {{
        "real_summary": "<Accurate summary>",
        "fake_summary": "<Manipulated summary>",
        "explanation": "<How the fake summary was altered>"
    }}
    """

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",  # Use GPT-4-turbo for better reasoning
        messages=[{"role": "system", "content": prompt}],
        temperature=0.7  # Add slight creativity
    )

    # Extract JSON output
    return response["choices"][0]["message"]["content"]