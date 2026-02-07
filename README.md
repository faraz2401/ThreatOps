# ThreatOps

ThreatOps is a DevOps project that analyzes CI/CD logs and automatically
detects risky operations before deployment.

## Features
- Log analysis for errors and failures
- Automated risk detection
- Pipeline-friendly exit codes
- Designed for Jenkins integration

## Project Structure
- analyzer/   → Log analysis logic
- logs/       → Sample logs
- scripts/    → Execution scripts

## Usage
Run ThreatOps using:
./scripts/run_threatops.sh

## ThreatOps CI Security Gate

This project includes a Python-based static analyzer enforced via Jenkins.

### Pipeline Flow
1. Jenkins creates isolated Python venv
2. Installs dependencies
3. Runs ThreatOps analyzer
4. Fails build on policy violations
5. Archives JSON security report

### Key Files
- analyzer.py — security rule engine
- rules/analyzer_rules.yml — policy definitions
- Jenkinsfile — CI enforcement
- artifacts/analysis.json — machine-readable output


