pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'YOUR_DOCKERHUB_USERNAME/devops-challenge'
        IMAGE_TAG = "${BUILD_NUMBER}"
        DOCKER_CREDENTIALS = 'dockerhub-credentials'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                    docker build \
                    -t ${DOCKER_IMAGE}:${IMAGE_TAG} \
                    -t ${DOCKER_IMAGE}:latest .
                '''
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: "${DOCKER_CREDENTIALS}",
                        usernameVariable: 'DOCKER_USERNAME',
                        passwordVariable: 'DOCKER_PASSWORD'
                    )
                ]) {
                    sh '''
                        echo "$DOCKER_PASSWORD" | docker login \
                        -u "$DOCKER_USERNAME" \
                        --password-stdin

                        docker push ${DOCKER_IMAGE}:${IMAGE_TAG}
                        docker push ${DOCKER_IMAGE}:latest

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy PostgreSQL') {
            steps {
                sh '''
                    kubectl apply -f k8s/postgres.yaml
                    kubectl rollout status deployment/postgres --timeout=120s
                '''
            }
        }

        stage('Deploy Backend') {
            steps {
                sh '''
                    sed "s|IMAGE_PLACEHOLDER|${DOCKER_IMAGE}:${IMAGE_TAG}|g" \
                    k8s/backend.yaml > /tmp/backend.yaml

                    kubectl apply -f /tmp/backend.yaml
                    kubectl apply -f k8s/service.yaml

                    kubectl rollout status deployment/backend --timeout=120s
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    echo "===== Kubernetes Nodes ====="
                    kubectl get nodes

                    echo "===== Pods ====="
                    kubectl get pods -o wide

                    echo "===== Services ====="
                    kubectl get svc

                    echo "===== Deployments ====="
                    kubectl get deployments
                '''
            }
        }
    }

    post {
        success {
            echo 'CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed. Check the stage logs for details.'
        }

        always {
            sh 'docker images | grep devops-challenge || true'
        }
    }
}
