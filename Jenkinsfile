pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

stage('Chef System Preparation') {
    steps {
        sh '''
        sudo chef-client --local-mode ~/Devops/threatops-chef/recipes/default.rb
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
            echo 'ThreatOps pipeline completed successfully'
        }
        failure {
            echo 'ThreatOps pipeline failed'
        }
    }
}
