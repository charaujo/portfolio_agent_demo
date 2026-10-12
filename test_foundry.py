
import os
import traceback

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

endpoint = os.getenv("FOUNDRY_ENDPOINT", "").rstrip("/") + "/"
deployment = os.getenv("FOUNDRY_DEPLOYMENT", "")
api_key = os.getenv("FOUNDRY_API_KEY", "")

print("Endpoint:", endpoint)
print("Deployment:", deployment)
print("API key configured:", bool(api_key))

try:
    client = OpenAI(
        base_url=endpoint,
        api_key=api_key,
        timeout=30.0,
        max_retries=0,
    )

    response = client.responses.create(
        model=deployment,
        input="Reply with exactly: Connection successful.",
        max_output_tokens=100,
    )

    print("SUCCESS!")
    print("Response:", response.output_text)

except Exception as e:
    print("\nCONNECTION FAILED")
    print("Exception type:", type(e).__name__)
    print("Error:", str(e))
    print("\nFULL TRACEBACK:")
    traceback.print_exc()
