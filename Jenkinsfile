stage('Test') {
    steps {
        bat 'python -m pip install --upgrade pip'
        bat 'python -m pip install -r requirements.txt'
        bat 'python -m pip install pytest'
        bat 'python -m pytest -v'
    }
}