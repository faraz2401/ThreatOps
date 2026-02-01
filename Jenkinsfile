pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
    }

    stages {

        stage('Build') {
            steps {
                echo "Building ThreatOps environment"
                sh '''
                python3 -m venv ${VENV_DIR}
                ${VENV_DIR}/bin/pip install --upgrade pip
                ${VENV_DIR}/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo "Running basic test"
                sh '''
                ${VENV_DIR}/bin/python analyzer.py
                '''
            }
        }

        stage('Configuration (Chef)') {
            steps {
                echo "Running Chef automation"
                sh '''
                sudo chef-client --local-mode /home/faraz24/Devops/threatops-chef/recipes/default.rb
                '''
            }
        }

        stage('Analyze') {
            steps {
                echo "Running ThreatOps analysis"
                sh '''
                ${VENV_DIR}/bin/python analyzer.py
                '''
            }
        }

        stage('Notify') {
            steps {
                echo "Sending Slack notification"
            }
        }
    }

    post {
    success {
        slackSend(
            channel: '#threatops-alerts',
            message: '✅ ThreatOps pipeline SUCCESS',
            tokenCredentialId: 'slack-token'
        )
    }
    failure {
        slackSend(
            channel: '#threatops-alerts',
            message: '❌ ThreatOps pipeline FAILED',
            tokenCredentialId: 'slack-token'
        )
         }
   }

}
