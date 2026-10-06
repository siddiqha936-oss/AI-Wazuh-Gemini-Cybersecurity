import json
import time
import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ALERT_FILE = BASE_DIR / "real_alert.json"
RESPONSE_SCRIPT = BASE_DIR / "incident_response.py"

last_alert = None

print("===== AUTOMATIC INCIDENT RESPONSE MONITOR =====")
print("Watching real_alert.json for changes...")
print("Press Ctrl+C to stop.")

try:
    while True:
        try:
            with open(ALERT_FILE, "r") as file:
                alert = json.load(file)

            current_alert = json.dumps(alert, sort_keys=True)

            if current_alert != last_alert:
                print("\n[+] Alert change detected.")
                subprocess.run(
                    [sys.executable, str(RESPONSE_SCRIPT)],
                    cwd=BASE_DIR,
                    check=False
                )
                last_alert = current_alert

        except (FileNotFoundError, json.JSONDecodeError) as error:
            print(f"[!] Waiting for a readable alert: {error}")

        time.sleep(5)

except KeyboardInterrupt:
    print("\nMonitoring stopped.")
