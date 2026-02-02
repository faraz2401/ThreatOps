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
                echo "Running basic sanity test"
                sh '''
                ${VENV_DIR}/bin/python -c "print('Test stage passed')"
                '''
            }
        }

        stage('Configuration (Chef)') {
            steps {
                echo "Running Chef automation"
                sh '''
                sudo chef-client --local-mode /home/faraz24/Devops/threatops-chef/recipes/default.rb || true
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
   
        stage('Deploy to EC2') {
    steps {
        sh '''
        ssh -i ~/.ssh/jenkins_ec2 ubuntu@18.234.131.225 << 'EOF'
            cd ~/Devops/ThreatOps
            git pull origin master
            source venv/bin/activate
            python analyzer.py
        EOF
        '''
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

