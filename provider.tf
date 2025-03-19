provider "aws" {
  region  = "ap-south-1" # Don't change the region
}

# Add your S3 backend configuration here
terraform {
  backend "s3" {
    bucket = "467.devops.candidate.exam"      # Your S3 bucket for storing the Terraform state
    region = "ap-south-1"                      # Region of the S3 bucket
    key    = "sumit.dange" # Replace with your first and last name
    encrypt = true                             # Enable encryption for security
  }
}
