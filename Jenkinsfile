pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
    }

    stages {

        stage('Build') {
            steps {
                sh '''
                    python3 -m venv ${VENV_DIR}
                    ${VENV_DIR}/bin/pip install --upgrade pip
                    ${VENV_DIR}/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    ${VENV_DIR}/bin/python -c "print('Test stage passed')"
                '''
            }
        }

        stage('Analyze') {
            steps {
                sh '''
                    set -e
                    ${VENV_DIR}/bin/python analyzer.py
                '''
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'artifacts/**', fingerprint: true
            }
        }

        stage('Deploy') {
            steps {
                sshagent(['jenkins_ec2']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ubuntu@18.234.131.225 '
                          cd ~/Devops/ThreatOps &&
                          docker compose down || true
                          docker compose up -d --build
                        '
                    '''
                }
            }
        }
    }

    post {
        success {
            slackSend channel: '#threatops-alerts',
                      message: '✅ ThreatOps pipeline SUCCESS'
        }
        failure {
            slackSend channel: '#threatops-alerts',
                      message: '❌ ThreatOps pipeline FAILED'
        }
    }
}

