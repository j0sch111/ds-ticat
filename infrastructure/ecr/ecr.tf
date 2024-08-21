provider "aws" {
  region = "us-west-2" # Change this to your desired region
}

resource "aws_ecr_repository" "ds-ticat_lambda" {
  name = "ds-ticat"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Environment = "dev"
  }
}

output "lambda_repository_url" {
  value = aws_ecr_repository.ds-ticat_lambda.repository_url
}

output "lambda_repository_name" {
  value = aws_ecr_repository.ds-ticat_lambda.name
}

resource "aws_ecr_repository" "ds-ticat_sagemaker" {
  name = "ds-ticat"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Environment = "dev"
  }
}

output "sagemaker_repository_url" {
  value = aws_ecr_repository.ds-ticat_sagemaker.repository_url
}

output "sagemaker_repository_name" {
  value = aws_ecr_repository.ds-ticat_sagemaker.name
}
