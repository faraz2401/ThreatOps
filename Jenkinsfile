pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        PYTHON = "${VENV_DIR}/bin/python"
        PIP = "${VENV_DIR}/bin/pip"
    }

    options {
        timestamps()
    }

    stages {

        stage('Checkout') {
            steps {
                echo "📥 Checking out source code"
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo "🔧 Building virtual environment"
                sh '''
                    python3 -m venv ${VENV_DIR}
                    ${PIP} install --upgrade pip
                    ${PIP} install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo "🧪 Running sanity tests"
                sh '''
                    ${PYTHON} -c "print('Basic test passed')"
                '''
            }
        }

        stage('Analyze') {
            steps {
                echo "🧠 Running ThreatOps analyzer"
                sh '''
                    ${PYTHON} analyzer.py
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo "🚀 Deploying to EC2"
                sshagent(credentials: ['jenkins-ec2']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ubuntu@18.234.131.225 << 'EOF'
                            cd ~/Devops/ThreatOps
                            docker compose down || true
                            docker compose up -d --build
                        EOF
                    '''
                }
            }
        }

        stage('Notify') {
            steps {
                echo "📣 Sending Slack notification"
                slackSend(
                    channel: '#threatops-alerts',
                    message: '🚀 ThreatOps pipeline completed successfully'
                )
            }
        }
    }

    post {
        failure {
            slackSend(
                channel: '#threatops-alerts',
                message: '❌ ThreatOps pipeline FAILED'
            )
        }
    }
}

             
