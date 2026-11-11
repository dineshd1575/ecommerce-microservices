pipeline {
    agent any

    environment {
        JWT_SECRET_KEY = 'test-only-secret-key-for-ci-pipeline-123456789'
        AWS_REGION = 'ap-southeast-2'
        REGISTRY = '292594542747.dkr.ecr.ap-southeast-2.amazonaws.com'
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/dineshd1575/ecommerce-microservices.git'
            }
        }

        stage('Validate') {
            steps {
                sh 'docker compose config -q'
            }
        }

        stage('Build') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                    set -e

                    aws ecr get-login-password --region "$AWS_REGION" |
                    docker login --username AWS --password-stdin "$REGISTRY"

                    docker push "$REGISTRY/user-auth:v1"
                    docker push "$REGISTRY/product-management:v1"
                    docker push "$REGISTRY/order-processing:v1"

                    echo "All images pushed successfully"
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    set -e

                    for service in user_auth product_management order_processing
                    do
                        echo "Testing $service"

                        docker compose run --rm --no-deps \
                            -e JWT_SECRET_KEY="$JWT_SECRET_KEY" \
                            --entrypoint python \
                            "$service" \
                            -m unittest discover -s . -p test_app.py -v
                    done
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    set -e

                    docker rm -f nginx_reverse_proxy || true

                    docker rm -f user_auth_container \
                        product_management_container \
                        order_processing_container 2>/dev/null || true

                    docker compose up -d --remove-orphans --force-recreate

                    docker compose ps
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    set -e

                    for service in user_auth_container \
                        product_management_container \
                        order_processing_container
                    do
                        STATUS=$(docker inspect \
                            --format='{{.State.Health.Status}}' "$service")

                        echo "$service : $STATUS"
                        test "$STATUS" = "healthy"
                    done

                    curl -fsS http://localhost:8088/auth/health
                    curl -fsS http://localhost:8088/products/health
                    curl -fsS http://localhost:8088/orders/health

                    echo "All health checks passed"
                '''
            }
        }
    }

    post {
        success {
            echo 'E-commerce CI/CD Pipeline SUCCESS!'
        }

        failure {
            echo 'E-commerce CI/CD Pipeline FAILED!'
        }

        always {
            echo 'Pipeline execution completed.'
        }
    }
}
