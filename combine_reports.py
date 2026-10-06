with open("incident_response.txt", "r") as file:
    incident_report = file.read()

with open("analysis_result.txt", "r") as file:
    gemini_analysis = file.read()

combined = (
    "AI-POWERED WAZUH INCIDENT REPORT\n"
    "================================\n\n"
    "INCIDENT RESPONSE RECOMMENDATIONS\n"
    "---------------------------------\n"
    + incident_report
    + "\n\nGEMINI AI ALERT ANALYSIS\n"
    "------------------------\n"
    + gemini_analysis
)

with open("combined_incident_report.txt", "w") as file:
    file.write(combined)

print("Combined report created successfully.")
print("Saved to combined_incident_report.txt")
