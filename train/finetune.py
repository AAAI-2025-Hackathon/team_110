import openai
import time

## I should load it from env. but tool azy 
## FIx before push
openai.api_key = "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"
client = openai.OpenAI(api_key="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")


# ✅ Step 2: Upload the dataset file
file_path = "../dataset/mongoDump_formatted_02_20_2025_prepared.jsonl"

file_response = client.files.create(
    file=open(file_path, "rb"),
    purpose="fine-tune"
)

file_id = file_response.id
print(f"✅ Dataset uploaded! File ID: {file_id}")

# ✅ Step 3: Start fine-tuning job
fine_tune_response = client.fine_tuning.jobs.create(
    training_file=file_id,
    model="gpt-3.5-turbo"
)

job_id = fine_tune_response.id
print(f"🚀 Fine-tuning started! Job ID: {job_id}")

# ✅ Step 4: Monitor fine-tuning progress
while True:
    job_status = client.fine_tuning.jobs.retrieve(job_id)
    status = job_status.status
    print(f"⏳ Fine-tuning status: {status}")

    if status == "succeeded":
        fine_tuned_model = job_status.fine_tuned_model
        print(f"🎉 Fine-tuning completed! Model ID: {fine_tuned_model}")
        break
    elif status == "failed":
        print("❌ Fine-tuning failed. Check logs for details.")
        break

    time.sleep(30)  # Wait 30 seconds before checking again