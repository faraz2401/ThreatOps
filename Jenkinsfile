pipeline {
    agent any

    options {
        timestamps()
    }

    environment {
        VENV_DIR = "venv"
        THREATOPS_BLOCK_SEVERITY = "HIGH"   // MEDIUM allowed, HIGH blocked
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo "🐍 Setting up Python venv and dependencies"
                sh '''
                    set -eux
                    python3 -m venv "${VENV_DIR}"
                    "${VENV_DIR}/bin/pip" install --upgrade pip
                    "${VENV_DIR}/bin/pip" install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo "✅ Running basic sanity test"
                sh '''
                    set -eux
                    "${VENV_DIR}/bin/python" -c "print('Test stage passed')"
                '''
            }
        }

        stage('Run ThreatOps Analyzer') {
            steps {
                echo "🔍 Running analyzer (will generate artifacts automatically)"
                sh '''
                    set -eux
                    "${VENV_DIR}/bin/python" analyzer.py
                '''
            }
        }
    }

    post {
        always {
            echo "📦 Archiving artifacts"
            archiveArtifacts artifacts: 'artifacts/**', fingerprint: true
        }

        success {
            echo "✅ ThreatOps Analyzer PASSED"
            slackSend(
                channel: '#threatops-alerts',
                message: '✅ ThreatOps pipeline SUCCESS (Analyzer Passed)'
            )
        }

        failure {
            echo "❌ ThreatOps Analyzer FAILED"
            slackSend(
                channel: '#threatops-alerts',
                message: '❌ ThreatOps pipeline FAILED (Analyzer Blocked)'
            )
        }
    }
}
