
import json
import time
import os
from google import genai

client = genai.Client()

ALERT_FILE = "real_alert.json"
RESULT_FILE = "analysis_result.txt"

last_alert = ""

print("===== WAZUH + GEMINI AUTOMATIC MONITOR =====")
print("Monitoring real_alert.json for new alerts...")
print("Press Ctrl+C to stop.")

while True:
    try:
        with open(ALERT_FILE, "r") as file:
            alert = json.load(file)

        current_alert = json.dumps(alert, sort_keys=True)

        if current_alert != last_alert:
            print("\n[+] New Wazuh alert detected!")

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

            with open(RESULT_FILE, "w") as result:
                result.write(response.text)

            print("[+] Gemini analysis completed.")
            print("[+] Result saved to analysis_result.txt")

            last_alert = current_alert

        time.sleep(5)

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
        break

    except Exception as e:
        print(f"[!] Error: {e}")
        time.sleep(5)
