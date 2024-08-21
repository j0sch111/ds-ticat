# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

terraform {
  required_version = ">= 0.13.1"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.19"
    }
    random = {
      source  = "hashicorp/random"
      version = ">= 2.0"
    }
  }
}

provider "aws" {
    region = "eu-central-1"
}

resource "aws_ecr_repository" "ds_ticat_lambda" {
  name = "ds-ticat"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Environment = "dev"
  }
}

output "lambda_repository_url" {
  value = aws_ecr_repository.ds_ticat_lambda.repository_url
}

output "lambda_repository_name" {
  value = aws_ecr_repository.ds_ticat_lambda.name
}


module "model_demo_invoke" {
  source        = "terraform-aws-modules/lambda/aws"
  version       = "4.6.0"
  create_role   = false
  timeout       = 30
  source_path   = local.lambda_src_path
  function_name = "ds-ticat-invoke"
  handler       = "index.lambda_handler"
  runtime       = "python3.11"
  lambda_role   = aws_iam_role.iam_for_lambda.arn
}

module "model_demo_invoke_image" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "ds-ticat-dev"
  description   = ""

  create_package = false

  image_uri    = "${aws_ecr_repository.project_lambda.repository_url}:latest"
  package_type = "Image"
}

resource "aws_iam_role" "iam_for_lambda" {
  name = "iam_for_lambda_usage"

  assume_role_policy = <<EOF
    {
    "Version": "2012-10-17",
    "Statement": [
        {
        "Action": "sts:AssumeRole",
        "Principal": {
            "Service": "lambda.amazonaws.com"
        },
        "Effect": "Allow",
        "Sid": ""
        }
    ]
    }
    EOF

}

## API Gateway

resource "aws_apigatewayv2_api" "lambda" {
  name          = "model_demo_invoke"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "lambda" {
  api_id = aws_apigatewayv2_api.lambda.id

  name        = "serverless_lambda_stage"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

resource "aws_apigatewayv2_integration" "model_demo_invoke_api" {
  api_id = aws_apigatewayv2_api.lambda.id

  integration_uri    = module.model_demo_invoke.lambda_function_invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "model_demo_invoke_route" {
  api_id = aws_apigatewayv2_api.lambda.id

  route_key = "POST /invoke"
  target    = "integrations/${aws_apigatewayv2_integration.model_demo_invoke_api.id}"
}

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.lambda.name}"

  retention_in_days = 30
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = module.model_demo_invoke.lambda_function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.lambda.execution_arn}/*/*"
}
