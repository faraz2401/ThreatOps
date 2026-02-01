import sys

print("ThreatOps initialized")

threats_found = False   # change this based on real logic

# Example logic (replace with real detection)
if threats_found:
    print("🚨 Threats detected")
    sys.exit(2)   # non-zero = Jenkins FAILURE
else:
    print("✅ No threats found")
    sys.exit(0)   # zero = Jenkins SUCCESS
