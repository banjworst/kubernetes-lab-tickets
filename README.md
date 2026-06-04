# Kubernetes Lab: From Flask App to EKS Deployment

A hands-on cloud infrastructure project demonstrating the full DevOps workflow: containerization, cloud registry management, and Kubernetes orchestration on AWS.

## Project Overview

This lab showcases building a production-ready application deployment pipeline. I took a simple Flask app, containerized it with Docker, uploaded it to AWS ECR, and deployed it to a managed Kubernetes cluster (EKS) — all while documenting the process with a custom ticketing system.

**Why this matters**: This is the real-world workflow for DevOps and Cloud Security teams. Every step demonstrates skills that employers actually need.

## The Stack

- **Application**: Python Flask
- **Containerization**: Docker (ARM64 compatible)
- **Container Registry**: AWS ECR
- **Orchestration**: Kubernetes (AWS EKS)
- **Infrastructure Tools**: eksctl, kubectl
- **Documentation**: Custom Flask-based Lab Ticket Manager + GitHub Issues integration
- **Platform**: M4 Mac (ARM64 architecture)

## What I Built

### 1. Flask Application
A simple HTTP server with health check endpoint. The foundation of everything that comes after.

```python
@app.route('/')
def hello():
    return f"Hello from {hostname}"

@app.route('/health')
def health():
    return {"status": "healthy"}
```

### 2. Docker Container
Packaged the Flask app in a lightweight `python:3.11-slim` image. Built locally and tested on ARM64.

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install flask
EXPOSE 8080
CMD ["python", "hello-eks.py"]
```

### 3. AWS ECR Integration
Pushed the Docker image to Amazon's container registry, making it accessible to Kubernetes.

**Process:**
- Created ECR repository in us-east-1
- Tagged image with account ID
- Authenticated with AWS CLI
- Pushed to cloud

### 4. EKS Cluster Provisioning
Used `eksctl` to automate cluster creation instead of clicking through the AWS console for hours.

**Cluster Config:**
- 2 t3.medium worker nodes (auto-scaling 1-3)
- Region: us-east-1 (same as ECR for latency optimization)
- All networking and security handled automatically

### 5. Lab Ticket Manager
Built a professional ticketing dashboard to document the entire journey. **Now deployed and live on Render.**

**Features:**
- Create tickets with title, description, detailed notes, and labels
- All tickets sync automatically to GitHub Issues
- Modern UI with cloud-native design (cyan/blue theme)
- Terminal script (`ticket.sh`) for quick ticket creation with pre-filled data
- View and search all tickets in one place
- **Remotely accessible** - works from anywhere via web or terminal script

**Live URL**: https://lab-ticket-manager.onrender.com

**Why this matters**: Documentation is part of the job. This system shows I treat it seriously. Plus, having it deployed publicly demonstrates full-stack deployment skills.

## Project Structure

```
kubernetes-lab/
├── hello-eks.py              # Flask application
├── Dockerfile                # Container image definition
├── deployment.yaml           # Kubernetes deployment manifest
├── service.yaml              # Kubernetes service manifest
├── ticket.sh                 # Terminal script for ticket creation
│
└── manager/                  # Lab Ticket Manager (Deployed to Render)
    ├── ticketing_app.py      # Flask backend
    ├── ticket_manager.py     # GitHub API integration
    ├── ticket_ui_professional.html  # Professional UI
    ├── requirements.txt      # Python dependencies
    └── .env                  # Environment variables
```

**📍 Lab Ticket Manager Live**: https://lab-ticket-manager.onrender.com

## Key Learnings

### Technical
- **Docker**: ARM64 compatibility matters on M4 Mac
- **AWS**: IAM roles, ECR authentication, VPC networking
- **Kubernetes**: Deployments, services, health checks, auto-scaling
- **Infrastructure Automation**: One command replaces hours of manual setup

### Professional
- **Documentation**: Proper logging of work is non-negotiable
- **Workflow**: Code → Container → Registry → Orchestration
- **Testing**: Verify at every stage before moving to the next

## How to Use This Project

### Prerequisites
- M4 Mac (or any ARM64 system) or x86 Linux/Mac
- Docker installed
- AWS account with credits
- Git

### Steps

1. **Run locally**
   ```bash
   python hello-eks.py
   curl http://localhost:8080
   ```

2. **Build Docker image**
   ```bash
   docker build -t hello-eks:v2 .
   docker run -p 8080:8080 hello-eks:v2
   ```

3. **Set up AWS**
   ```bash
   # Create IAM user with programmatic access
   # Configure AWS CLI
   aws configure
   ```

4. **Create ECR repository**
   ```bash
   aws ecr create-repository --repository-name hello-eks --region us-east-1
   ```

5. **Push to ECR**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
   docker tag hello-eks:v2 YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/hello-eks:v2
   docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/hello-eks:v2
   ```

6. **Create EKS cluster**
   ```bash
   eksctl create cluster \
     --name hello-eks-cluster \
     --region us-east-1 \
     --nodegroup-name standard-workers \
     --node-type t3.medium \
     --nodes 2
   ```

7. **Deploy to Kubernetes**
   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   kubectl get service hello-eks-service
   ```

8. **Log your work**
   ```bash
   ./ticket.sh "Title" "One-line summary" "Detailed notes" "label1,label2"
   ```

## Screenshots & Documentation

[Add screenshots here of:]
- Lab Ticket Manager UI
- GitHub Issues created from tickets
- Terminal commands and outputs

## Deployment

### Lab Ticket Manager on Render

The Lab Ticket Manager is deployed on **Render** (free tier) and accessible at:
```
https://lab-ticket-manager.onrender.com
```

**Deployment Details:**
- **Platform**: Render.com (free tier)
- **Runtime**: Python 3
- **Source**: GitHub (`kubernetes-lab-tickets` repo)
- **Auto-deploy**: Enabled (redeploys on git push)

**Using the Remote Ticket Script:**

Instead of accessing locally, use the remote `ticket.sh`:

```bash
./ticket.sh "Your Title" "One-line summary" "Detailed notes" "label1,label2"
```

This opens the live web app with pre-filled data. Works from anywhere.

### EKS Cluster (Not Currently Running)

The Kubernetes cluster (`hello-eks-cluster`) was provisioned on AWS EKS but deleted to save costs. It can be recreated with:

```bash
eksctl create cluster \
  --name hello-eks-cluster \
  --region us-east-1 \
  --nodegroup-name standard-workers \
  --node-type t3.medium \
  --nodes 2
```

**Cost Note**: EKS clusters incur AWS charges (~$0.08/hour for compute). Delete when not actively deploying.

## What This Demonstrates

For **Cloud Security/DevSecOps roles**, this project shows:
- ✅ Container management and registry workflows
- ✅ Kubernetes fundamentals and deployment
- ✅ AWS infrastructure (IAM, networking, services)
- ✅ Infrastructure automation and IaC principles
- ✅ Professional documentation practices
- ✅ Full DevOps pipeline understanding
- ✅ Full-stack deployment (backend + frontend on cloud platform)

For **Employers**, this is evidence I can:
- Work with production-grade tools
- Understand cloud architecture
- Automate repetitive tasks
- Document my work properly
- Deploy applications remotely
- Solve real infrastructure problems

## Tools Used

- **Languages**: Python, YAML, Bash
- **Platforms**: AWS (ECR, EKS, IAM)
- **Tools**: Docker, kubectl, eksctl, Homebrew
- **Services**: GitHub Issues, Flask

## What's Next

This foundation opens doors to:
- Adding CI/CD pipeline (GitHub Actions, Jenkins)
- Implementing monitoring (CloudWatch, Prometheus)
- Adding security scanning (image scanning, RBAC)
- Multi-environment deployments
- Helm charts for templating

## Cost Notes

⚠️ **Important**: EKS clusters incur charges. This lab cost ~$0.08/hour for the compute resources. Delete the cluster when not in use:

```bash
eksctl delete cluster --name hello-eks-cluster --region us-east-1
```

## Key Takeaway

This isn't just a project — it's a complete demonstration of how modern infrastructure works. Every step mirrors what Cloud/DevSecOps teams do daily. From code to cloud, containerized, orchestrated, and documented.

---

**Created by**: Sanjay Sutherland  
**Date**: 2026  
**Status**: Complete
