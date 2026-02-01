pipeline {
    agent any

    environment {
        SLACK_WEBHOOK = credentials('slack-webhook')
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Chef System Preparation') {
            steps {
                sh '''
                sudo chef-client --local-mode /home/faraz24/Devops/threatops-chef/recipes/default.rb
                '''
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run ThreatOps Analyzer') {
            steps {
                sh '''
                . venv/bin/activate
                python analyzer.py
                '''
            }
        }
    }

    post {
        success {
            sh '''
            curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"✅ ThreatOps Pipeline SUCCESS\"}" \
            "$SLACK_WEBHOOK" || true
            '''
        }
        failure {
            sh '''
            curl -X POST -H 'Content-type: application/json' \
            --data "{\"text\":\"❌ ThreatOps Pipeline FAILED\"}" \
            "$SLACK_WEBHOOK" || true
            '''
        }
    }
}

