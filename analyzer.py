#!/usr/bin/env python3

import json
import yaml
import os
import sys
from datetime import datetime

# -----------------------------
# Configuration
# -----------------------------
RULES_FILE = "rules/analyzer_rules.yml"
ARTIFACTS_DIR = "artifacts"
ARTIFACT_FILE = os.path.join(ARTIFACTS_DIR, "analysis.json")


# -----------------------------
# Load Rules
# -----------------------------
def load_rules():
    if not os.path.exists(RULES_FILE):
        print(f"❌ Rules file not found: {RULES_FILE}")
        sys.exit(1)

    with open(RULES_FILE, "r") as f:
        return yaml.safe_load(f)


# -----------------------------
# Run Analysis
# -----------------------------
def run_analysis():
    rules = load_rules()
    findings = []

    for rule in rules.get("rules", []):
        findings.append({
            "id": rule.get("id"),
            "description": rule.get("description"),
            "severity": rule.get("severity"),
            "status": "DETECTED"
        })

    result = {
        "tool": "ThreatOps Analyzer",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "total_findings": len(findings),
        "findings": findings
    }

    return result


# -----------------------------
# Write Artifact
# -----------------------------
def write_artifact(result):
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)

    with open(ARTIFACT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    print(f"📄 Analysis report written to {ARTIFACT_FILE}")


# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    result = run_analysis()
    write_artifact(result)

    high_findings = [
        f for f in result.get("findings", [])
        if f.get("severity") == "HIGH"
    ]

    print("\n🔍 Findings Summary")
    print("-------------------")
    for f in result.get("findings", []):
        print(f"- [{f['severity']}] {f['id']}: {f['description']}")

    if high_findings:
        print("\n❌ HIGH severity findings detected. Failing pipeline.")
        sys.exit(1)
    else:
        print("\n✅ No HIGH severity findings. Pipeline passed.")
        sys.exit(0)

