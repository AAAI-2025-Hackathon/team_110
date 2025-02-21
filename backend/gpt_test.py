from gpt import *

if __name__ == "__main__":
    # Example Input
    input_json = {
        "topic": "Science",
        "manipulation_methods": [
            "Basic factual inaccuracies",
            "Causation vs Correlation confusion",
            "Bad math/Incorrect science"
        ]
    }

    # Generate summaries
    result = generate_summaries(input_json)

    # Pretty print the JSON output
    print(json.dumps(result, indent=2))