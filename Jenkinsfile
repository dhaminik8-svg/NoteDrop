pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Source code is available in the workspace.'
            }
        }

        stage('Build') {
            steps {
                bat 'python --version'
                bat 'python -m py_compile app.py'
            }
        }

        stage('Test') {
            steps {
                bat 'python -m pip install -r requirements.txt'
                bat 'python -m pip install pytest'
                bat 'python -m pytest -v'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Application validation completed.'
                echo 'Docker deployment will be configured in the next stage.'
            }
        }
    }

    post {
        success {
            echo 'NoteDrop pipeline completed successfully!'
        }
        failure {
            echo 'NoteDrop pipeline failed. Check the console output.'
        }
        always {
            echo 'Pipeline execution finished.'
        }
    }
}
