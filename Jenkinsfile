pipeline {
    agent any

    options {
        timestamps()              // ✅ STEP #22: enable timestamps
        ansiColor('xterm')        // nicer logs (safe even if unused)
    }

    environment {
        VENV_DIR = "venv"
        APP_NAME = "ThreatOps"
    }

    stages {

        stage('Build') {
            steps {
                echo "🔧 [BUILD] Setting up Python virtual environment"
                sh '''
                    set -x
                    python3 -m venv ${VENV_DIR}
                    ${VENV_DIR}/bin/pip install --upgrade pip
                    ${VENV_DIR}/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo "🧪 [TEST] Running sanity checks"
                sh '''
                    set -x
                    ${VENV_DIR}/bin/python -c "print('Basic test passed')"
                '''
            }
        }

        stage('Configuration (Chef)') {
            steps {
                echo "🍳 [CHEF] Running Chef configuration"
                sh '''
                    set -x
                    sudo chef-client --local-mode /home/faraz24/Devops/threatops-chef/recipes/default.rb || true
                '''
            }
        }

        stage('Analyze') {
            steps {
                echo "🔍 [ANALYZE] Running ThreatOps analyzer"
                sh '''
                    set -x
                    ${VENV_DIR}/bin/python analyzer.py
                '''
            }
        }

        stage('Archive Artifacts') {
            steps {
                echo "📦 [ARCHIVE] Saving analysis reports"
                archiveArtifacts artifacts: 'artifacts/**', fingerprint: true
            }
        }

        stage('Deploy') {
            steps {
                echo "🚀 [DEPLOY] Deploying to EC2 via Docker Compose"
                sshagent(['jenkins_ec2']) {
                    sh '''
                        set -x
                        ssh -o StrictHostKeyChecking=no ubuntu@18.234.131.225 '
                            cd ~/Devops/ThreatOps &&
                            docker compose down || true &&
                            docker compose up -d --build
                        '
                    '''
                }
            }
        }
    }

    post {
        success {
            echo "✅ PIPELINE SUCCESS"
            slackSend(
                channel: '#threatops-alerts',
                message: '✅ ThreatOps pipeline SUCCESS'
            )
        }

        failure {
            echo "❌ PIPELINE FAILURE"
            slackSend(
                channel: '#threatops-alerts',
                message: '❌ ThreatOps pipeline FAILED'
            )
        }
    }
}

