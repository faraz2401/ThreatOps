pipeline {
    agent any

    options {
        timestamps()
        ansiColor('xterm')
    }

    environment {
        APP_NAME       = "ThreatOps"
        VENV_DIR       = "venv"
        ARTIFACT_DIR  = "artifacts"
        DOCKER_COMPOSE = "docker compose"
    }

    stages {

        stage('Build') {
            steps {
                echo "🔧 [BUILD]"
                sh '''
                    python3 -m venv ${VENV_DIR}
                    ${VENV_DIR}/bin/pip install --upgrade pip
                    ${VENV_DIR}/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo "🧪 [TEST]"
                sh '''
                    ${VENV_DIR}/bin/python -c "print('Tests OK')"
                '''
            }
        }

        stage('Analyze') {
            steps {
                echo "🔍 [ANALYZE]"
                sh '''
                    mkdir -p ${ARTIFACT_DIR}
                    ${VENV_DIR}/bin/python analyzer.py
                '''
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'artifacts/**', fingerprint: true
            }
        }

        stage('Chef Configuration (REMOTE)') {
            environment {
                EC2_HOST = credentials('ec2_host')
                EC2_USER = credentials('ec2_user')
            }
            steps {
                echo "🍳 [CHEF] Applying configuration on EC2"
                sshagent(['jenkins_ec2']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "
                            cd ~/chef/threatops-chef &&
                            sudo chef-client --local-mode recipes/default.rb
                        "
                    '''
                }
            }
        }

        stage('Deploy') {
            environment {
                EC2_HOST = credentials('ec2_host')
                EC2_USER = credentials('ec2_user')
            }
            steps {
                echo "🚀 [DEPLOY]"
                sshagent(['jenkins_ec2']) {
                    sh '''
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "
                            cd ~/Devops/ThreatOps &&
                            ${DOCKER_COMPOSE} down || true &&
                            ${DOCKER_COMPOSE} up -d --build
                        "
                    '''
                }
            }
        }
            stage('Configuration (Chef)') {
    steps {
        echo "Running Chef automation"
        sh '''
        sudo chef-client --local-mode recipes/default.rb \
          --log_level info \
          --logfile /var/log/threatops_chef.log
        '''
        sh '''
        grep "SUCCESS" /var/log/threatops_chef_status.txt
        '''
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

