pipeline{
  agent any
  stages {
    stage('Build app'){
      steps{
        sh 'docker-compose up'
      }
    }
    stage('Testing'){
      steps{
        sh 'python test_app.py'
      }
    }
    stage('Docker compose down'){
        sh 'docker-compose down'
    }
  }
}