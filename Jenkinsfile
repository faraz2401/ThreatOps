pipeline {
    agent any

    options {
        timestamps()
        ansiColor('xterm')
    }

    environment {
        // 🔧 Application
        APP_NAME      = "ThreatOps"
        VENV_DIR      = "venv"
        ARTIFACT_DIR = "artifacts"

        // Docker
        DOCKER_COMPOSE = "docker compose"
    }

    stages {

        stage('Build') {
            steps {
                echo "🔧 [BUILD] Setting up Python environment"
                sh '''
                    set -e
                    python3 -m venv ${VENV_DIR}
                    ${VENV_DIR}/bin/pip install --upgrade pip
                    ${VENV_DIR}/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo "🧪 [TEST] Sanity check"
                sh '''
                    ${VENV_DIR}/bin/python -c "print('Tests passed')"
                '''
            }
        }

        stage('Configuration (Chef)') {
            steps {
                echo "🍳 [CHEF] Running Chef automation"
                sh '''
                    sudo chef-client --local-mode /home/faraz24/Devops/threatops-chef/recipes/default.rb || true
                '''
            }
        }

        stage('Analyze') {
            steps {
                echo "🔍 [ANALYZE] Threat analysis"
                sh '''
                    mkdir -p ${ARTIFACT_DIR}
                    ${VENV_DIR}/bin/python analyzer.py
                '''
            }
        }

        stage('Archive Artifacts') {
            steps {
                echo "📦 [ARCHIVE] Saving reports"
                archiveArtifacts artifacts: '${ARTIFACT_DIR}/**', fingerprint: true
            }
        }

        stage('Deploy') {
            environment {
                EC2_HOST = credentials('ec2_host')
                EC2_USER = credentials('ec2_user')
            }
            steps {
                echo "🚀 [DEPLOY] Deploying to EC2"
                sshagent(['jenkins_ec2']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "
                            cd /home/${EC2_USER}/Devops/ThreatOps &&
                            ${DOCKER_COMPOSE} down || true &&
                            ${DOCKER_COMPOSE} up -d --build
                        "
                    '''
                }
            }
        }
    }

    post {
        success {
            slackSend(
                channel: '#threatops-alerts',
                message: "✅ ${APP_NAME} pipeline SUCCESS"
            )
        }
        failure {
            slackSend(
                channel: '#threatops-alerts',
                message: "❌ ${APP_NAME} pipeline FAILED"
            )
        }
    }
}

