# AWS Deployment Guide for QR Code Generator API

## Overview
This guide covers deploying your FastAPI QR Code Generator on AWS using services like EC2, ECS/Fargate, or Lambda.

## Prerequisites
- AWS Account with appropriate permissions
- Docker installed locally
- AWS CLI configured with credentials
- Docker Hub account (for storing images) or AWS ECR

## Deployment Options

### Option 1: EC2 Deployment (Simple)

1. **Launch an EC2 Instance**
   - Choose Ubuntu 22.04 LTS AMI
   - Instance type: t3.small (or larger based on traffic)
   - Configure security group to allow traffic on port 8000 (or 80/443 with nginx)

2. **SSH into your instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip
   ```

3. **Install dependencies**
   ```bash
   sudo apt update
   sudo apt install -y python3.11 python3-pip git
   git clone <your-repo>
   cd qr-code-generator
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python3 main.py
   ```

5. **For production use PM2 or Gunicorn**
   ```bash
   pip install gunicorn
   gunicorn --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 main:app
   ```

---

### Option 2: ECS/Fargate Deployment (Recommended for Scalability)

#### Step 1: Create an ECR Repository
```bash
aws ecr create-repository --repository-name qr-code-generator --region us-east-1
```

#### Step 2: Build and Push Docker Image
```bash
# Build image
docker build -t qr-code-generator .

# Tag image for ECR
docker tag qr-code-generator:latest <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/qr-code-generator:latest

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com

# Push image
docker push <AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/qr-code-generator:latest
```

#### Step 3: Create ECS Cluster
```bash
aws ecs create-cluster --cluster-name qr-generator-cluster --region us-east-1
```

#### Step 4: Create Task Definition
Create `task-definition.json`:
```json
{
  "family": "qr-code-generator",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "qr-code-generator",
      "image": "<AWS_ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/qr-code-generator:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "hostPort": 8000,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/qr-code-generator",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "healthCheck": {
        "command": ["CMD-SHELL", "curl -f http://localhost:8000/health || exit 1"],
        "interval": 30,
        "timeout": 5,
        "retries": 3,
        "startPeriod": 10
      }
    }
  ]
}
```

Register the task definition:
```bash
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

#### Step 5: Create Fargate Service
```bash
aws ecs create-service \
  --cluster qr-generator-cluster \
  --service-name qr-generator-service \
  --task-definition qr-code-generator \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

---

### Option 3: Lambda Deployment (Serverless)

For Lambda, you need to use Mangum or similar ASGI adapter:

```bash
pip install mangum
```

Create `lambda_handler.py`:
```python
from mangum import Mangum
from main import app

handler = Mangum(app, lifespan="off")
```

Then deploy using AWS SAM or Serverless Framework.

---

## Storage Considerations for AWS

### For QR Code Storage (Choose one):

1. **EBS Volume** (for EC2)
   - Use persistent storage
   - Mount at /app/QR_code

2. **EFS** (for ECS/Fargate)
   - Shared file system
   - Managed and persistent

3. **S3** (Recommended for Scalability)
   - Modify code to save QR codes to S3
   - Add boto3 dependency: `pip install boto3`

**S3 Integration Example**:
```python
import boto3
s3 = boto3.client('s3')

def save_to_s3(image, bucket, key):
    s3.put_object(Bucket=bucket, Key=key, Body=image, ContentType='image/png')

def get_from_s3(bucket, key):
    return s3.get_object(Bucket=bucket, Key=key)['Body'].read()
```

---

## Environment Configuration

Create `.env` file for sensitive data:
```
AWS_REGION=us-east-1
S3_BUCKET=your-bucket-name
CLEANUP_DAYS=1
CORS_ORIGINS=https://yourdomain.com
```

---

## Monitoring & Logging

### CloudWatch Logs
Already configured in the task definition. View logs:
```bash
aws logs tail /ecs/qr-code-generator --follow
```

### CloudWatch Alarms
Create alarms for:
- CPU utilization > 70%
- Memory utilization > 80%
- API errors (5xx)
- High latency

---

## Load Balancing

Use Application Load Balancer (ALB) for better distribution:

1. Create ALB
2. Target Group pointing to ECS service
3. Security group allowing 80/443

---

## Auto-Scaling

Create Auto Scaling Policy (for ECS):
```bash
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/qr-generator-cluster/qr-generator-service \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 1 \
  --max-capacity 10
```

---

## Cost Optimization

1. **Use Fargate Spot** for non-critical workloads (up to 70% discount)
2. **Reserved Capacity** for consistent baseline traffic
3. **S3 lifecycle policies** to archive old QR codes
4. **CloudFront CDN** to cache generated QR codes

---

## Testing the Deployment

```bash
# Health check
curl http://your-endpoint.com/health

# Generate QR code
curl -X POST http://your-endpoint.com/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# Get QR code image
curl http://your-endpoint.com/qr/qr_20260212_105235_58e0421c
```

---

## Troubleshooting

### Container won't start
- Check CloudWatch logs: `aws logs tail /ecs/qr-code-generator --follow`
- Verify IAM permissions for ECR pull

### High latency
- Check container CPU/memory allocation
- Consider adding more instances
- Enable caching for generated QR codes

### QR codes not persisting
- Ensure storage is properly configured (EBS/EFS/S3)
- Check file permissions in container

---

## Security Best Practices

1. Use AWS Secrets Manager for sensitive data
2. Enable VPC encryption
3. Use IAM roles with least privilege
4. Enable ALB access logging
5. Use HTTPS/TLS certificates from AWS Certificate Manager
6. Implement rate limiting in FastAPI
7. Add authentication if needed (API keys, OAuth)

---

## Next Steps

1. Test locally with `python3 main.py`
2. Build Docker image and test
3. Push to ECR
4. Deploy to ECS/Fargate
5. Set up monitoring and alerts
6. Configure auto-scaling
7. Add domain name with Route 53
8. Enable HTTPS with ACM certificate
