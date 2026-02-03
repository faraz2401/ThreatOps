import sys

def run_analysis():
    print("🔍 Running ThreatOps analysis...")

    # Simulated logic (we'll improve later)
    threats_found = False   # change to True to test failure

    if threats_found:
        print("🚨 THREAT DETECTED!")
        return 1
    else:
        print("✅ No threats found")
        return 0

if __name__ == "__main__":
    exit_code = run_analysis()
    sys.exit(exit_code)

