pipeline {
    agent any

    options {
        timestamps()          // STEP #22
        ansiColor('xterm')
    }

    environment {
        // 🔧 Application
        APP_NAME       = "ThreatOps"
        VENV_DIR       = "venv"
        ARTIFACT_DIR  = "artifacts"

        // 🚀 Deployment
        EC2_USER       = "ubuntu"
        EC2_HOST       = "18.234.131.225"
        APP_DIR        = "/home/ubuntu/Devops/ThreatOps"
        DOCKER_COMPOSE = "docker compose"
    }

    stages {

        stage('Build') {
            steps {
                echo "🔧 [BUILD] Preparing Python environment"
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
                echo "🧪 [TEST] Running sanity tests"
                sh '''
                    set -x
                    ${VENV_DIR}/bin/python -c "print('Test stage OK')"
                '''
            }
        }

        stage('Configuration (Chef)') {
            steps {
                echo "🍳 [CHEF] Applying system configuration"
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
                    mkdir -p ${ARTIFACT_DIR}
                    ${VENV_DIR}/bin/python analyzer.py
                '''
            }
        }

        stage('Archive Artifacts') {
            steps {
                echo "📦 [ARCHIVE] Archiving analyzer outputs"
                archiveArtifacts artifacts: '${ARTIFACT_DIR}/**', fingerprint: true
            }
        }

        stage('Deploy') {
            steps {
                echo "🚀 [DEPLOY] Deploying ${APP_NAME} to EC2"
                sshagent(['jenkins_ec2']) {
                    sh '''
                        set -x
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "
                            cd ${APP_DIR} &&
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
            echo "✅ ${APP_NAME} pipeline SUCCESS"
            slackSend(
                channel: '#threatops-alerts',
                message: "✅ ${APP_NAME} pipeline SUCCESS"
            )
        }

        failure {
            echo "❌ ${APP_NAME} pipeline FAILED"
            slackSend(
                channel: '#threatops-alerts',
                message: "❌ ${APP_NAME} pipeline FAILED"
            )
        }
    }
}

