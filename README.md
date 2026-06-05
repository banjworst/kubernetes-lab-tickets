# Kubernetes Lab: From Flask App to Cloud Deployment

A hands-on DevOps project that demonstrates the complete workflow: building an app, containerizing it, storing it in the cloud, and deploying it to Kubernetes.

## What I Built

### 1. Flask Application
A simple Python web server with a health check endpoint.

```python
from flask import Flask
import socket

app = Flask(__name__)
hostname = socket.gethostname()

@app.route('/')
def hello():
    return f"Hello from {hostname}"

@app.route('/health')
def health():
    return {"status": "healthy"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

### 2. Docker Container
Packaged the Flask app in a Docker image (`hello-eks:v2`). Docker is like a box that contains everything an app needs to run: the code, Python, dependencies, everything.

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install flask
EXPOSE 8080
CMD ["python", "hello-eks.py"]
```

### 3. AWS ECR (Container Registry)
Uploaded the Docker image to AWS's container storage. Think of it as a cloud warehouse where Docker images are stored and can be pulled from anywhere.

### 4. Kubernetes Cluster (AWS EKS)
Set up a managed Kubernetes cluster on AWS. Kubernetes automatically manages containers — it keeps them running, restarts them if they crash, scales them up if needed, and handles all the networking.
A cluster is just a group of computers (instances) working together as one system. For this project I had 2 worker cpu's in my EC2 instances running in AWS and 1 control cpu that is managed by AWS itself.
The cluster gives me multiple servers so that if one crashes, the others keep running. This brings redundancy and allows my app to handle more traffic.

**Tools used:**
- **eksctl**: A command-line tool that automates cluster creation. Instead of manually configuring AWS for hours, one command does it all. Tell it what you want it to build and it automates the process.
- **kubectl**: A remote control for Kubernetes. You use it to deploy apps, check status, view logs, etc. (e.g. kubectl get pods = "find the current running pods/clusters)

### 5. Lab Ticket Manager
Built a professional ticketing dashboard to document the entire project. Create tickets with descriptions and labels which automatically sync to GitHub Issues.

**Live at**: https://lab-ticket-manager.onrender.com  
**Quick create**: Use `./ticket.sh "Title" "Summary" "Details" "label1,label2"` to create tickets remotely.

## Project Structure

```
kubernetes-lab/
├── hello-eks.py                 # Flask app
├── Dockerfile                   # Container definition
├── deployment.yaml              # Kubernetes deployment config
├── service.yaml                 # Kubernetes service config
├── ticket.sh                    # Script to quickly create tickets
└── manager/                     # Ticket Manager (deployed to Render)
    ├── ticketing_app.py
    ├── ticket_manager.py
    ├── ticket_ui_professional.html
    └── requirements.txt
```

## How It Works

1. **Local Development**: Write and test Flask app locally
2. **Containerize**: Build Docker image so it works anywhere
3. **Store in Cloud**: Push image to AWS ECR
4. **Orchestrate**: Deploy to Kubernetes cluster, which manages the containers automatically
5. **Document**: Log everything in the Ticket Manager

## Key Technologies

- **Python** (Flask) - Web framework
- **Docker** - Container platform
- **AWS** (ECR, EKS, IAM) - Cloud services
- **Kubernetes** - Container orchestration
- **GitHub Issues** - Ticket storage

## To Recreate This

```bash
# 1. Build Docker image locally
docker build -t hello-eks:v2 .
docker run -p 8080:8080 hello-eks:v2

# 2. Push to AWS ECR (requires AWS account, there is a free tier with a bit of storage but you have to pay attention and stop the cluster when it's not in use)
aws ecr create-repository --repository-name hello-eks --region us-east-1
# [login and push image]

# 3. Create Kubernetes cluster
eksctl create cluster \
  --name hello-eks-cluster \
  --region us-east-1 \
  --node-type t3.medium \
  --nodes 2

# 4. Deploy to cluster
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# 5. Get external IP and test
kubectl get service hello-eks-service
```

## Important Notes

**Costs**: AWS charges for EKS clusters and compute (~$0.08/hour). The cluster was deleted after testing to save costs. It can be recreated anytime with the command above.

**Ticket Manager**: Deployed separately on Render (free tier). The main Flask app would be deployed to the EKS cluster if it were still running.

## Screenshots

[Add screenshots here of:]
-<img width="1148" height="658" alt="Screenshot 2026-06-04 at 8 01 02 PM" src="https://github.com/user-attachments/assets/6979eb07-7c0e-48b6-828e-784ba3ffb65b" />
<img width="1894" height="948" alt="Screenshot 2026-06-04 at 8 01 29 PM" src="https://github.com/user-attachments/assets/3f866d8c-fbed-4fba-b3a8-ae623d5b0378" />
<img width="1453" height="1133" alt="Screenshot 2026-06-04 at 8 12 16 PM" src="https://github.com/user-attachments/assets/7ccb914c-6e6a-44af-a916-2186a921109c" />


## What This Shows

- Understanding of containerization and cloud deployment
- How to automate infrastructure setup
- Full DevOps workflow from code to production
- Professional documentation practices

---

**Created by**: Sanjay Sutherland  
**Status**: Complete
