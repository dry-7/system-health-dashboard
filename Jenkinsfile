
pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    environment {
        IMAGE_NAME = 'system-health-dashboard'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/python -m pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '.venv/bin/python -m pytest -q'
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t system-health-dashboard:ci .'
            }
        }

        stage('Tag') {
            steps {
                sh 'docker tag system-health-dashboard:ci system-health-dashboard:$BUILD_NUMBER'
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    docker run -d --name "health-ci-$BUILD_NUMBER" \
                      -e APP_ENV=testing \
                      "system-health-dashboard:$BUILD_NUMBER"
                '''

                retry(10) {
                    sleep 2
                    sh '''
                        docker exec "health-ci-$BUILD_NUMBER" python -c \
                        "import json, urllib.request; data=json.load(urllib.request.urlopen('http://127.0.0.1:5000/health', timeout=3)); assert data['status']=='UP'"
                    '''
                }
            }
        }
    }

    post {
        always {
            sh '''
                docker rm -f "health-ci-$BUILD_NUMBER" || true
            '''
        }
    }
}
