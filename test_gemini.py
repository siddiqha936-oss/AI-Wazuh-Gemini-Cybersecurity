
import json
from google import genai

client = genai.Client()

with open("alert.json", "r") as file:
    alert = json.load(file)

prompt = f"""
You are a cybersecurity analyst.

Analyze this Wazuh security alert:

{json.dumps(alert, indent=2)}

Explain:
1. What happened?
2. What is the severity?
3. Why did Wazuh generate this alert?
4. Is it potentially dangerous?
5. What should a security analyst check next?

Give a clear and simple cybersecurity analysis.
"""

response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=prompt
)

print("\n===== GEMINI WAZUH ALERT ANALYSIS =====\n")
print(response.text)