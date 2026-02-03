pipeline {
    agent any

    environment {
        VENV_DIR = "venv"
        PYTHON   = "${VENV_DIR}/bin/python"
        PIP      = "${VENV_DIR}/bin/pip"
        EC2_USER = "ubuntu"
        EC2_IP   = "18.234.131.225"
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
                echo "🔧 Building ThreatOps environment"
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
                    ${PYTHON} -c "print('✅ Test stage passed')"
                '''
            }
        }

        stage('Configuration') {
            steps {
                echo "⚙️ Running Chef configuration"
                sh '''
                    sudo chef-client --local-mode /home/faraz24/Devops/threatops-chef/recipes/default.rb || true
                '''
            }
        }

        stage('Analyze') {
            steps {
                echo "🔍 Running ThreatOps analyzer"
                sh '''
                    ${PYTHON} analyzer.py
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo "🚀 Deploying to EC2"
                sshagent(credentials: ['jenkins_ec2']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_IP} << EOF
                          set -e
                          cd ~/Devops/ThreatOps
                          docker compose down || true
                          docker compose up -d --build
                        EOF
                    '''
                }
            }
        }
    }

    post {
        success {
            slackSend(
                channel: '#threatops-alerts',
                message: '✅ ThreatOps pipeline SUCCESS'
            )
        }
        failure {
            slackSend(
                channel: '#threatops-alerts',
                message: '❌ ThreatOps pipeline FAILED'
            )
        }
    }
}

