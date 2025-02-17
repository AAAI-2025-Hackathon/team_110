import openai
import os
from backend.mockResponses import get_mock_response

# Load OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

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
    If the OpenAI API is unavailable or fails, returns a mocked response.
    """
    # Select misinformation categories based on difficulty level
    selected_misinfo = misinfo_categories[:fake_level]

    # Check if OpenAI API key is available
    if not OPENAI_API_KEY:
        print("[INFO] No OpenAI API key found. Returning mock response.")
        return get_mock_response()  # Get a random mock response

    try:
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
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.7
        )

        # Extract JSON output
        return response["choices"][0]["message"]["content"]

    except Exception as e:
        print(f"[ERROR] OpenAI API request failed: {e}. Returning mock response.")
        return get_mock_response()  # Return mock response on failure