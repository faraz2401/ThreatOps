pipeline {
    agent any

    stages {

        stage('Setup Python') {
            steps {
                sh '''
                    python3 --version
                    python3 -m venv venv || true
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt pyyaml
                '''
            }
        }

        stage('Run Analyzer') {
            steps {
                sh '''
                    . venv/bin/activate
                    python3 analyzer.py
                '''
            }
        }
    }

    post {
        success {
            echo 'ThreatOps analysis PASSED'
        }

        failure {
            echo 'ThreatOps analysis FAILED – blocking pipeline'
        }

        unstable {
            echo 'ThreatOps analysis UNSTABLE – review findings'
        }
    }
}

