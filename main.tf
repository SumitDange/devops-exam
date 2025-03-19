# Create Private Subnets in the existing VPC
resource "aws_subnet" "private_subnet" {
  count = length(var.private_subnet_cidrs)
  vpc_id = data.aws_vpc.vpc.id  # Referencing the existing VPC
  cidr_block = element(var.private_subnet_cidrs, count.index)
  availability_zone = "ap-south-1a"  # Use a specific AZ, or let it default
  map_public_ip_on_launch = false
  tags = {
    Name = "Private Subnet ${count.index + 1}"
  }
}

# Assuming the NAT Gateway ID (provided) as a data source
resource "aws_route_table" "private_route_table" {
  vpc_id = data.aws_vpc.vpc.id  # Use the existing VPC

  route {
    cidr_block = "0.0.0.0/0"  # Routing all internet traffic
    nat_gateway_id = data.aws_nat_gateway.nat.id  
  }

  tags = {
    Name = "Private Route Table"
  }
}

# Associating the private subnets with the route table
resource "aws_route_table_association" "private_subnet_association" {
  count = length(var.private_subnet_cidrs)

  subnet_id      = aws_subnet.private_subnet[count.index].id
  route_table_id = aws_route_table.private_route_table.id
}


# Security Group for Lambda Function
resource "aws_security_group" "lambda_sg" {
  vpc_id = data.aws_vpc.vpc.id  # Use the existing VPC
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]  # Allow outbound traffic to the internet via NAT Gateway
  }

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["10.0.0.0/16"]  # Allow inbound traffic from your VPC
  }
}


# Assuming the private subnet is already created using Terraform

resource "aws_lambda_function" "my_lambda" {
  function_name = "InvokeAPI-Lambda"
  role          = data.aws_iam_role.lambda.arn  # IAM Role for Lambda (using the data block)
  handler       = "lambda_function.lambda_handler"  # The Python handler function (index.py)
  runtime       = "python3.11"  # Runtime for Python
  filename      = "lambda_function/lambda_function.zip"  # Path to the zip file inside lambda_function folder # Ensuring that we have zipped Python code into a .zip file
  vpc_config {
    subnet_ids         = aws_subnet.private_subnet[*].id  # Subnet IDs from private subnets
    security_group_ids = [aws_security_group.lambda_sg.id]  # Attach appropriate security group
  }

  environment {
    variables = {
      PRIVATE_SUBNET_ID = aws_subnet.private_subnet[0].id  # Inject private subnet ID dynamically
    }
  }

  depends_on = [data.aws_iam_role.lambda]  # Ensure IAM role is available before Lambda creation
}


