#!/usr/bin/env python3
import os
import json
from datetime import datetime, UTC
from pathlib import Path

# -----------------------------
# Config
# -----------------------------
ARTIFACT_DIR = Path("artifacts")
OUT_JSON = ARTIFACT_DIR / "analysis.json"
OUT_TXT = ARTIFACT_DIR / "analyzer_report.txt"

# MEDIUM allowed, HIGH blocked (your requirement)
BLOCK_SEVERITY = os.environ.get("THREATOPS_BLOCK_SEVERITY", "HIGH").upper()

# Simple patterns (you can expand later)
PATTERNS = [
    {
        "id": "RULE-001",
        "severity": "HIGH",
        "needle": "AWS_SECRET_ACCESS_KEY",
        "description": "Possible hardcoded AWS secret"
    },
    {
        "id": "RULE-002",
        "severity": "HIGH",
        "needle": "BEGIN RSA PRIVATE KEY",
        "description": "Private key material detected"
    },
    {
        "id": "RULE-003",
        "severity": "MEDIUM",
        "needle": "debug=True",
        "description": "Flask debug mode enabled"
    },
    {
        "id": "RULE-004",
        "severity": "MEDIUM",
        "needle": "SECRET_KEY=",
        "description": "Possible hardcoded secret key"
    },
]

SEVERITY_ORDER = {"LOW": 1, "MEDIUM": 2, "HIGH": 3}


def severity_rank(sev: str) -> int:
    return SEVERITY_ORDER.get(sev.upper(), 0)


def should_block(findings: list[dict]) -> bool:
    # Block if any finding severity >= BLOCK_SEVERITY
    threshold = severity_rank(BLOCK_SEVERITY)
    return any(severity_rank(f.get("severity", "LOW")) >= threshold for f in findings)


def scan_repo() -> list[dict]:
    findings = []

    # Scan common source files only (keeps it fast)
    exts = {".py", ".txt", ".yml", ".yaml", ".env", ".md", ".sh", ".conf", ".ini"}
    skip_dirs = {"venv", ".git", "__pycache__", "node_modules", "artifacts"}

    for path in Path(".").rglob("*"):
        if path.is_dir():
            continue

        # Skip big/irrelevant folders
        parts = set(path.parts)
        if parts.intersection(skip_dirs):
            continue

        if path.suffix.lower() not in exts:
            continue

        try:
            content = path.read_text(errors="ignore")
        except Exception:
            continue

        for rule in PATTERNS:
            if rule["needle"] in content:
                findings.append({
                    "id": rule["id"],
                    "severity": rule["severity"],
                    "description": rule["description"],
                    "file": str(path),
                    "needle": rule["needle"],
                })

    return findings


def write_artifacts(findings: list[dict]) -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        "timestamp_utc": datetime.now(UTC).isoformat(),
        "blocked_threshold": BLOCK_SEVERITY,
        "findings": findings,
        "summary": {
            "LOW": sum(1 for f in findings if f["severity"] == "LOW"),
            "MEDIUM": sum(1 for f in findings if f["severity"] == "MEDIUM"),
            "HIGH": sum(1 for f in findings if f["severity"] == "HIGH"),
            "total": len(findings),
        }
    }

    OUT_JSON.write_text(json.dumps(payload, indent=2))

    lines = []
    lines.append("🔍 ThreatOps Analyzer Report")
    lines.append(f"Timestamp (UTC): {payload['timestamp_utc']}")
    lines.append(f"Block threshold: {BLOCK_SEVERITY}")
    lines.append("")
    lines.append("Summary:")
    for k, v in payload["summary"].items():
        lines.append(f"  {k}: {v}")
    lines.append("")

    if findings:
        lines.append("Findings:")
        for f in findings:
            lines.append(f"- [{f['severity']}] {f['id']} {f['description']} ({f['file']})")
    else:
        lines.append("✅ No findings detected")

    OUT_TXT.write_text("\n".join(lines) + "\n")


def main() -> int:
    print("🔍 Running ThreatOps analysis...")

    findings = scan_repo()
    write_artifacts(findings)

    high = sum(1 for f in findings if f["severity"] == "HIGH")
    med = sum(1 for f in findings if f["severity"] == "MEDIUM")
    low = sum(1 for f in findings if f["severity"] == "LOW")

    print("✅ Analyzer completed")
    print(f"LOW findings    : {low}")
    print(f"MEDIUM findings : {med}")
    print(f"HIGH findings   : {high}")
    print(f"Artifacts saved : {OUT_JSON} , {OUT_TXT}")

    if should_block(findings):
        print("🚫 Build blocked due to HIGH severity findings")
        return 1

    print("✅ Build allowed — No HIGH severity findings")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
