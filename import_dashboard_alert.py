import json
import shutil
import subprocess
import sys
from pathlib import Path

folder = Path(__file__).resolve().parent
source = folder / "dashboard_alert.json"
target = folder / "real_alert.json"

try:
    with open(source, encoding="utf-8") as f:
        document = json.load(f)

    alert = document.get("_source", document)

    if not all(k in alert for k in ("agent", "rule", "data")):
        raise ValueError("Invalid Wazuh alert structure")

    if target.exists():
        shutil.copy2(target, folder / "real_alert_previous.json")

    with open(target, "w", encoding="utf-8") as f:
        json.dump(alert, f, indent=2)

    print("Alert imported successfully.")
    print("Agent:", alert["agent"].get("name"))
    print("Rule ID:", alert["rule"].get("id"))

except (OSError, ValueError, json.JSONDecodeError) as e:
    print("Import failed:", e)
    sys.exit(1)

for script in ("wazuh_gemini.py", "incident_response.py"):
    print(f"\nRunning {script}...")
    result = subprocess.run([sys.executable, script], cwd=folder)
    if result.returncode != 0:
        print(f"{script} failed. Stopping workflow.")
        sys.exit(result.returncode)

print("\nRunning combine_reports.py...")
result = subprocess.run(
    [sys.executable, "combine_reports.py"], cwd=folder
)

if result.returncode != 0:
    sys.exit(result.returncode)

print("\nAlert processing workflow completed.")
