pipeline {
    agent any
    stages {
        stage('Build Flask app') {
            steps {
                sh 'docker build -t tweet_app .'
            }
        }
        stage('Run docker images') {
            parallel {
                stage('Run Redis') {
                    steps {
                        sh 'docker run -d -p 6379:6379 --name redis redis:alpine'
                    }
                }
                stage('Run Flask App') {
                    steps {
                        sh 'docker run -d -p 5000:5000 --name tweet_app_c tweet_app'
                    }
                }
            }
        }
        stage('Testing') {
            steps {
                sh 'python test_app.py'
            }
        }
        stage('Docker images down') {
            steps {
                sh 'docker rm -f redis'
                sh 'docker rm -f tweet_app_c'
                sh 'docker rmi -f tweet_app'
            }
        }
    }
}

