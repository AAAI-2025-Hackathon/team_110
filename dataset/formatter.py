import json

# Input and output file names
input_file = "mongoDump_refactored_02_20_2025.JSONL"  # Update this to your actual input filename
output_file = "mongoDump_formatted_02_20_2025.JSONL"

# Open the malformed JSON file and read it line by line
with open(input_file, "r", encoding="utf-8") as f:
    raw_data = f.read()

# Split based on JSON object separators (assuming each starts with '{"messages":[')
raw_entries = raw_data.strip().split("\n{")

# Add back the opening "{" that was removed during splitting
json_objects = ["{" + entry if i > 0 else entry for i, entry in enumerate(raw_entries)]

# Process and reformat
with open(output_file, "w", encoding="utf-8") as f_out:
    for json_str in json_objects:
        try:
            # Parse JSON
            json_obj = json.loads(json_str)

            # Extract user prompt
            user_prompt = ""
            assistant_response = ""

            for message in json_obj["messages"]:
                if message["role"] == "user":
                    user_prompt = message["content"]
                elif message["role"] == "assistant":
                    assistant_response = message["content"]

            # Convert the assistant response into valid JSON format
            assistant_json = json.loads(assistant_response)

            # Create the OpenAI fine-tuning format
            formatted_entry = {
                "prompt": user_prompt,
                "completion": json.dumps(assistant_json, ensure_ascii=False)
            }

            # Write each example as a single JSONL line
            f_out.write(json.dumps(formatted_entry, ensure_ascii=False) + "\n")

        except json.JSONDecodeError as e:
            print(f"Skipping invalid JSON entry: {e}")

print(f"Conversion complete! Saved to {output_file}")