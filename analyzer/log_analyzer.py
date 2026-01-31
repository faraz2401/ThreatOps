import sys

RISK_KEYWORDS = ["ERROR", "FAIL", "EXCEPTION"]

log_file = "logs/sample.log"
risk_detected = False

with open(log_file, "r") as file:
    for line in file:
        for word in RISK_KEYWORDS:
            if word in line:
                print(f"[ThreatOps] RISK FOUND: {line.strip()}")
                risk_detected = True

if risk_detected:
    print("[ThreatOps] RESULT: RISK DETECTED")
    sys.exit(1)
else:
    print("[ThreatOps] RESULT: SAFE")
    sys.exit(0)
