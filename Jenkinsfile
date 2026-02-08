pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
    steps {
        sh '''
            python3 -m venv venv
            venv/bin/pip install -r requirements.txt
        '''
    }
}

        stage('Run ThreatOps Analyzer') {
    steps {
        sh '''
            venv/bin/python analyzer.py
        '''
    }
}

    }

    post {
        success {
            echo "ThreatOps Analyzer PASSED"
        }
        failure {
            echo "ThreatOps Analyzer FAILED"
        }
        always {
            archiveArtifacts artifacts: 'artifacts/*.json', fingerprint: true
        }
    }
}

