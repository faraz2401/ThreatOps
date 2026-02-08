#!/usr/bin/env python3

import json
import sys
import yaml
from pathlib import Path

ARTIFACT_FILE = Path("artifacts/analysis.json")
BASELINE_FILE = Path("artifacts/baseline.json")
RULES_FILE = Path("rules/analyzer_rules.yml")

EXIT_OK = 0
EXIT_BLOCK = 1


def load_json(path, default):
    if path.exists():
        return json.loads(path.read_text())
    return default


def load_rules():
    if not RULES_FILE.exists():
        print("❌ rules/analyzer_rules.yml not found")
        sys.exit(EXIT_BLOCK)
    return yaml.safe_load(RULES_FILE.read_text())


def get_high_issues(analysis, rules):
    high_issues = set()
    for finding in analysis.get("findings", []):
        rule_id = finding.get("rule_id")
        severity = rules.get(rule_id, {}).get("severity", "LOW")
        if severity == "HIGH":
            high_issues.add(rule_id)
    return high_issues


def main():
    analysis = load_json(ARTIFACT_FILE, {})
    baseline = load_json(BASELINE_FILE, {"known_high_issues": []})
    rules = load_rules()

    known_high = set(baseline.get("known_high_issues", []))
    current_high = get_high_issues(analysis, rules)

    new_high = current_high - known_high

    print("🔍 ThreatOps Analysis Summary")
    print(f"Known HIGH issues   : {sorted(known_high)}")
    print(f"Current HIGH issues : {sorted(current_high)}")
    print(f"New HIGH issues     : {sorted(new_high)}")

    if new_high:
        print("\n🚨 BLOCKING BUILD — New HIGH severity issues detected")
        sys.exit(EXIT_BLOCK)

    print("\n✅ Build allowed — No new HIGH issues introduced")
    sys.exit(EXIT_OK)


if __name__ == "__main__":
    main()
