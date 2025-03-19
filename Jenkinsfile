pipeline {
    agent any
    
    environment {
        AWS_REGION = 'ap-south-1'  // Set the AWS region for your resources
    }
    
    stages {
        stage('TF Init') {
            steps {
                script {
                    echo 'Executing Terraform Init'
                    // Run terraform init to initialize the working directory
                    sh 'terraform init'
                }
            }
        }

        stage('TF Validate') {
            steps {
                script {
                    echo 'Validating Terraform Code'
                    // Run terraform validate to check if the configuration is valid
                    sh 'terraform validate'
                }
            }
        }

        stage('TF Plan') {
            steps {
                script {
                    echo 'Executing Terraform Plan'
                    // Run terraform plan to show the actions Terraform will take
                    sh 'terraform plan'
                }
            }
        }

        stage('TF Apply') {
            steps {
                script {
                    echo 'Executing Terraform Apply'
                    // Run terraform apply to provision the infrastructure
                    sh 'terraform apply -auto-approve'
                }
            }
        }

        stage('Invoke Lambda') {
            steps {
                script {
                    echo 'Invoking your AWS Lambda'
                    // Use the AWS CLI to invoke the Lambda function
                    sh 'aws lambda invoke --function-name InvokeAPI-Lambda201 --payload "{} --log-type Tail" result.json'
                    // Print the Lambda execution result
                    sh 'cat result.json'
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check the logs for errors.'
        }
    }
}
