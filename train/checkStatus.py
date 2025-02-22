import openai

# Set your API key
# openai.api_key = "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"

# # Replace with your actual job ID
# job_id = "ftjob-m0BfiJSm2zq99nRDN7kco0Ia"
import openai

# ✅ Set up OpenAI client
client = openai.OpenAI(api_key="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")

# ✅ Replace with your actual Job ID
job_id = "ftjob-m0BfiJSm2zq99nRDN7kco0Ia"

# ✅ Get job details
job_status = client.fine_tuning.jobs.retrieve(job_id)

# ✅ Print detailed status
print("🔍 Fine-tuning job details:")
print(f"ID: {job_status.id}")
print(f"Status: {job_status.status}")
print(f"Model: {job_status.fine_tuned_model if job_status.fine_tuned_model else 'Not available yet'}")

# ✅ If the job failed, print error message
if job_status.status == "failed":
    print("❌ Fine-tuning failed. Error details:")
    print(job_status.error.message)
