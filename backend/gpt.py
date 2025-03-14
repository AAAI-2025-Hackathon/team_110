import openai
import os, json, sys

package_path = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, package_path)
from mockResponses import get_mock_response

# Load OpenAI API Key
#python -c "import os; print(os.getenv('OPENAI_API_KEY'))"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = "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"
### API KEY ###
### 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 ###


# Misinformation categories
MISINFO_CAT = [
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

TOPIC_CAT = [
    "Political",
    "Historic",
    "Facts",
    "FakeKickStarters",
    "Science",
    "Futuraism",
    "Enterrtainment",
    "Technology"
]    

def generate_summaries(input_data):
    """
    Generates a fake and real summary of a given topic based on structured input.
    
    :param input_data: JSON object containing the topic.
    :return: JSON object with fake summary, real summary, and explanation.
    """

    if OPENAI_API_KEY == None:
        print("[WARN] Defaulting to mocks due to no API keys")
        return get_mock_response()

    # Convert input data to a formatted string
    prompt = f"""
        Generate a fake and real summary of a story or an event related to "{input_data['topic']}". 
        Both summaries must argue for the same fact but one must be factually incorrect. 
        The fake summary should use the following manipulation techniques: {", ".join(input_data["manipulation_methods"])}. 

        Ensure that:
        - If the fake summary appears credible, set the real summary as an empty string.
        - If the real summary appears too fake or unbelievable, set the fake summary as an empty string.

        Use institutions and references to add credibility where appropriate.
        Additionally, provide an explanation of how the fake summary misleads.

    For example:
        "fake_summary": "Plasma Kinetics, a US-based startup, claims it can capture hydrogen gas from the exhaust of incinerators and shipping vehicles. Their patented technology stores hydrogen in a thin film for easy transport, allowing later extraction for energy production. Independent studies have confirmed their breakthrough, and the company is set for mass production.",
        "real_summary": "Plasma Kinetics is developing a hydrogen storage solution but does not capture hydrogen from exhaust gases. Their technology involves solid-state hydrogen storage in a film, improving transportation efficiency. While promising, it has yet to achieve large-scale adoption due to high production costs and energy conversion losses.",
        "explanation": "Plasma Kinetics does not extract hydrogen from waste gases but focuses on storage. While their approach could enhance hydrogen distribution, its real-world feasibility remains uncertain due to cost and efficiency concerns. Claims of independent verification are overstated, as the technology is still in early testing stages."
        """

    # Call OpenAI API with function calling
    response = openai.ChatCompletion.create(
        model="gpt-4-turbo",
        messages=[{"role": "user", "content": prompt}],
        functions=[
            {
                "name": "generate_summary",
                "description": "Generates a fake and real summary of a given topic.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fake_summary": {"type": "string", "description": "A fake yet plausible summary."},
                        "real_summary": {"type": "string", "description": "The accurate factual summary."},
                        "explanation": {"type": "string", "description": "How the fake summary misleads."}
                    },
                    "required": ["fake_summary", "real_summary", "explanation"]
                }
            }
        ],
        function_call="auto",
        temperature=0.7
    )

    #print(response)
    # Extract structured response
    structured_output = response["choices"][0]["message"]["function_call"]["arguments"]

    # Parse JSON response and return it
    return json.loads(structured_output)
