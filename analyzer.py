#!/usr/bin/env python3

import sys
import json
import yaml
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).parent
ARTIFACT_FILE = BASE_DIR / "artifacts" / "analysis.json"
RULES_FILE = BASE_DIR / "rules" / "analyzer_rules.yml"

def load_rules():
    with open(RULES_FILE, "r") as f:
        return yaml.safe_load(f)

def load_artifact():
    if not ARTIFACT_FILE.exists():
        print("Artifact file missing:", ARTIFACT_FILE)
        return {}
    with open(ARTIFACT_FILE, "r") as f:
        return json.load(f)

def evaluate(findings, rules):
    t = rules["thresholds"]

    if findings.get("critical", 0) >= t["critical"]:
        return "fail"
    if findings.get("high", 0) >= t["high"]:
        return "unstable"
    if findings.get("medium", 0) >= t["medium"]:
        return "unstable"
    return "pass"

def main():
    rules = load_rules()
    data = load_artifact()
    findings = data.get("findings", {})

    result = evaluate(findings, rules)
    print(f"[{datetime.utcnow()}] {rules['messages'][result]}")
    print("Findings:", findings)

    sys.exit(rules["exit_codes"][result])

if __name__ == "__main__":
    main()

