import math
import random

# Define possible accents and convincingness levels
ACCENTS = ["en-US", "en-GB", "en-IN", "en-AU", "en-CA"]
CONVINCINGNESS_LEVELS = [
    { "rate": 0.9, "pitch": 1.2 },  
    { "rate": 1.0, "pitch": 1.0 },  
    { "rate": 1.1, "pitch": 0.9 },  
    { "rate": 1.2, "pitch": 0.8 }
]

# Ensure `tags` structure is initialized
def initialize_tags(tags):
    if "accents" not in tags:
        tags["accents"] = {}

    for accent in ACCENTS:
        for convincingness in CONVINCINGNESS_LEVELS:
            key = (accent, convincingness["rate"], convincingness["pitch"])
            if key not in tags["accents"]:
                tags["accents"][key] = {"num_success": 0, "num_attempts": 0}

# UCB Selection of Best Accent and Convincingness
def select_next_accent_and_convincingness(tags):
    initialize_tags(tags)

    total_attempts = sum(entry["num_attempts"] for entry in tags["accents"].values()) + 1  # Avoid division by zero
    c = 2  # Exploration parameter

    # Compute UCB scores for each combination
    ucb_values = {}
    for key, data in tags["accents"].items():
        S = data["num_success"]
        N = max(1, data["num_attempts"])  # Avoid division by zero
        
        ucb = (S / N) + c * math.sqrt(math.log(total_attempts) / N)
        ucb_values[key] = ucb

    # Select the combination with highest UCB score
    best_accent, best_rate, best_pitch = max(ucb_values, key=ucb_values.get)
    
    return best_accent, { "rate": best_rate, "pitch": best_pitch }

# Update stats after each attempt
def update_tags(tags, current_accent, current_convincingness, was_tricked):
    initialize_tags(tags)

    key = (current_accent, current_convincingness["rate"], current_convincingness["pitch"])

    if key not in tags["accents"]:
        tags["accents"][key] = {"num_success": 0, "num_attempts": 0}

    # Increment attempts for this accent/convincingness
    tags["accents"][key]["num_attempts"] += 1

    if was_tricked:
        # If the model successfully tricked the user, increase success count
        tags["accents"][key]["num_success"] += 1
    else:
        # If the human got it right (model failed), decrease confidence in this combination
        tags["accents"][key]["num_success"] = max(0, tags["accents"][key]["num_success"] - 1)
