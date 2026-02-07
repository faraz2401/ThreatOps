pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python venv') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run ThreatOps Analyzer') {
            steps {
                sh '''
                    . venv/bin/activate
                    python analyzer.py
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'artifacts/analysis.json', fingerprint: true
        }
        failure {
            error "❌ ThreatOps Analyzer failed — build blocked"
        }
    }
}

