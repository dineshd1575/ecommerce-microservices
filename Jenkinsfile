pipeline {
    agent any

    environment {
        PROJECT_DIR = '/home/ec2-user/AWS-Microservices-DevOps/ecommerce-microservices'
        JWT_SECRET_KEY = 'test-only-secret-key-for-ci-pipeline-123456789'
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
                sh '''
                    echo "Checking Docker Compose configuration..."
                    docker compose config -q
                    echo "Docker Compose validation successful"
                '''
            }
        }

        stage('Build') {
            steps {
                sh '''
                    docker compose build
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                   set -e

                   for service in user_auth product_management order_processing
                   do
                       echo "Running tests for $service"

                       docker compose run --rm \
                         --no-deps \
                         -e JWT_SECRET_KEY="$JWT_SECRET_KEY" \
                         --entrypoint python \
                         $service -m unittest discover -s . -p test_app.py -v
                   done
               '''
           }
        }
        stage('Deploy') {
            steps {
                sh '''
                   set -e

                   echo "Removing old microservice containers..."

                   docker rm -f \
                      user_auth_container \
                      product_management_container \
                      order_processing_container 2>/dev/null || true

                  echo "Deploying latest microservices..."

                  docker compose up -d --remove-orphans --force-recreate

                  echo "Deployment completed"
                  docker compose ps
              '''
            }
        }
        stage('Health Check') {
            steps {
                sh '''
                    set -e

                    for service in user_auth_container product_management_container order_processing_container
                    do
                        STATUS=$(docker inspect \
                            --format='{{.State.Health.Status}}' $service)

                        echo "$service : $STATUS"

                        test "$STATUS" = "healthy"
                    done

                    curl -fsS http://localhost:8088/auth/health
                    curl -fsS http://localhost:8088/products/health
                    curl -fsS http://localhost:8088/orders/health
                '''
            }
        }
    }

    post {
        success {
            echo 'E-commerce Microservices Pipeline SUCCESS!'
        }

        failure {
            echo 'E-commerce Microservices Pipeline FAILED!'
        }

        always {
            echo 'Pipeline execution completed.'
        }
    }
}
