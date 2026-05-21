import requests
import json
from datetime import datetime


class GitHubTicketManager:
    """Automatically create GitHub Issues for lab documentation"""
    
    def __init__(self, token, owner, repo):
        """
        Initialize GitHub ticket manager
        
        Args:
            token: GitHub Personal Access Token (ghp_...)
            owner: GitHub username
            repo: Repository name (e.g., 'kubernetes-lab-tickets')
        """
        self.token = token
        self.owner = owner
        self.repo = repo
        self.api_url = f"https://api.github.com/repos/{owner}/{repo}"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def create_ticket(self, title, description, labels=None, assignee=None):
        """
        Create a new GitHub Issue (ticket)
        
        Args:
            title (str): Ticket title
            description (str): Detailed description
            labels (list): List of labels to add (e.g., ['bug', 'kubernetes'])
            assignee (str): GitHub username to assign to
        
        Returns:
            dict: Response with ticket URL and number
        """
        
        payload = {
            "title": title,
            "body": description,
            "labels": labels or []
        }
        
        if assignee:
            payload["assignee"] = assignee
        
        response = requests.post(
            f"{self.api_url}/issues",
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 201:
            data = response.json()
            return {
                "success": True,
                "ticket_number": data["number"],
                "url": data["html_url"],
                "message": f"Ticket #{data['number']} created successfully"
            }
        else:
            return {
                "success": False,
                "error": response.json().get("message", "Unknown error"),
                "status_code": response.status_code
            }
    
    def close_ticket(self, issue_number, solution_comment=None):
        """
        Close a ticket and optionally add a comment with solution
        
        Args:
            issue_number (int): GitHub issue number
            solution_comment (str): Comment to add before closing
        
        Returns:
            dict: Response confirming closure
        """
        
        # Add solution comment if provided
        if solution_comment:
            comment_url = f"{self.api_url}/issues/{issue_number}/comments"
            comment_payload = {"body": solution_comment}
            
            requests.post(
                comment_url,
                headers=self.headers,
                json=comment_payload
            )
        
        # Close the issue
        update_url = f"{self.api_url}/issues/{issue_number}"
        payload = {"state": "closed"}
        
        response = requests.patch(
            update_url,
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "message": f"Ticket #{issue_number} closed successfully"
            }
        else:
            return {
                "success": False,
                "error": response.json().get("message", "Unknown error")
            }
    
    def add_comment(self, issue_number, comment):
        """
        Add a comment to an existing ticket
        
        Args:
            issue_number (int): GitHub issue number
            comment (str): Comment text (supports markdown)
        
        Returns:
            dict: Response with comment details
        """
        
        url = f"{self.api_url}/issues/{issue_number}/comments"
        payload = {"body": comment}
        
        response = requests.post(
            url,
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 201:
            return {
                "success": True,
                "message": "Comment added successfully"
            }
        else:
            return {
                "success": False,
                "error": response.json().get("message", "Unknown error")
            }
    
    def list_tickets(self, state="open", labels=None):
        """
        List all tickets (issues)
        
        Args:
            state (str): 'open', 'closed', or 'all'
            labels (list): Filter by labels
        
        Returns:
            dict: List of tickets
        """
        
        params = {"state": state}
        if labels:
            params["labels"] = ",".join(labels)
        
        response = requests.get(
            f"{self.api_url}/issues",
            headers=self.headers,
            params=params
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "tickets": response.json()
            }
        else:
            return {
                "success": False,
                "error": response.json().get("message", "Unknown error")
            }
    
    def get_ticket(self, issue_number):
        """
        Get details of a specific ticket
        
        Args:
            issue_number (int): GitHub issue number
        
        Returns:
            dict: Ticket details
        """
        
        response = requests.get(
            f"{self.api_url}/issues/{issue_number}",
            headers=self.headers
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "ticket": response.json()
            }
        else:
            return {
                "success": False,
                "error": response.json().get("message", "Unknown error")
            }
    
    def update_ticket(self, issue_number, title=None, description=None, labels=None, state=None):
        """
        Update a ticket
        
        Args:
            issue_number (int): GitHub issue number
            title (str): New title (optional)
            description (str): New description (optional)
            labels (list): New labels (optional)
            state (str): New state - 'open' or 'closed' (optional)
        
        Returns:
            dict: Updated ticket details
        """
        
        payload = {}
        if title:
            payload["title"] = title
        if description:
            payload["body"] = description
        if labels is not None:
            payload["labels"] = labels
        if state:
            payload["state"] = state
        
        response = requests.patch(
            f"{self.api_url}/issues/{issue_number}",
            headers=self.headers,
            json=payload
        )
        
        if response.status_code == 200:
            return {
                "success": True,
                "ticket": response.json()
            }
        else:
            return {
                "success": False,
                "error": response.json().get("message", "Unknown error")
            }


# ============ USAGE EXAMPLES ============

if __name__ == "__main__":
    import os
    
    # Get credentials from environment variables
    token = os.getenv("GITHUB_TOKEN")
    owner = os.getenv("GITHUB_OWNER", "your-github-username")
    repo = os.getenv("GITHUB_REPO", "kubernetes-lab-tickets")
    
    if not token:
        print("ERROR: GITHUB_TOKEN environment variable not set!")
        print("Set it with: export GITHUB_TOKEN='ghp_your_token_here'")
        exit(1)
    
    # Initialize the ticket manager
    tm = GitHubTicketManager(token, owner, repo)
    
    print("=== GitHub Ticket Manager Test ===\n")
    
    # Test 1: Create a ticket
    print("1. Creating a test ticket...")
    problem_description = """
## Problem Encountered
Pod deployment failed with ImagePullBackOff error

## Error Details
```
kubectl describe pod python-app-deployment-xyz123
```
Status: ImagePullBackOff
Events: Failed to pull image from ECR

## What I Tried
1. Verified image URI in deployment.yaml
2. Checked ECR repository exists
3. Verified Docker image was pushed

## Environment
- Date: 2025-04-21
- Cluster: my-python-cluster
- Region: us-east-1
"""
    
    result = tm.create_ticket(
        title="[TEST] ImagePullBackOff error when deploying to EKS",
        description=problem_description,
        labels=["test", "bug", "kubernetes", "eks"],
        assignee=owner
    )
    
    if result['success']:
        print(f"✅ Ticket created successfully!")
        print(f"   Ticket #: {result['ticket_number']}")
        print(f"   URL: {result['url']}\n")
        ticket_number = result['ticket_number']
    else:
        print(f"❌ Failed to create ticket: {result['error']}\n")
        exit(1)
    
    # Test 2: Add a comment
    print("2. Adding a comment with findings...")
    findings_comment = """
## Investigation Update
Found the issue! The ECR secret wasn't created in the Kubernetes cluster.

### Solution
```bash
kubectl create secret docker-registry ecr-secret \\
    --docker-server=123456789012.dkr.ecr.us-east-1.amazonaws.com \\
    --docker-username=AWS \\
    --docker-password=$(aws ecr get-login-password --region us-east-1)
```

After creating the secret and updating the deployment, pods now pull successfully.
"""
    
    result = tm.add_comment(ticket_number, findings_comment)
    
    if result['success']:
        print(f"✅ Comment added successfully!\n")
    else:
        print(f"❌ Failed to add comment: {result['error']}\n")
    
    # Test 3: Get ticket details
    print("3. Retrieving ticket details...")
    result = tm.get_ticket(ticket_number)
    
    if result['success']:
        ticket = result['ticket']
        print(f"✅ Retrieved ticket #{ticket['number']}")
        print(f"   Title: {ticket['title']}")
        print(f"   State: {ticket['state']}")
        print(f"   Comments: {ticket['comments']}\n")
    else:
        print(f"❌ Failed to get ticket: {result['error']}\n")
    
    # Test 4: List all tickets
    print("4. Listing all open tickets...")
    result = tm.list_tickets(state="open")
    
    if result['success']:
        tickets = result['tickets']
        print(f"✅ Found {len(tickets)} open tickets:\n")
        for ticket in tickets[:5]:  # Show first 5
            print(f"   #{ticket['number']}: {ticket['title']}")
    else:
        print(f"❌ Failed to list tickets: {result['error']}\n")
    
    # Test 5: Close the ticket with solution
    print(f"\n5. Closing ticket #{ticket_number}...")
    solution = """
## ✅ Solution
Created the ECR secret in Kubernetes cluster to allow pod image pulls.

### Steps Taken
1. Verified AWS credentials configured
2. Created docker-registry secret with ECR credentials
3. Updated deployment.yaml to reference ecr-secret in imagePullSecrets
4. Reapplied deployment: `kubectl apply -f deployment.yaml`

### Result
Pods now successfully pull images from ECR and enter Running state.

### Lessons Learned
- Kubernetes needs docker-registry secrets to authenticate with private container registries
- Always verify imagePullSecrets section in deployment manifests
- Use `kubectl describe pod` to debug ImagePullBackOff errors
"""
    
    result = tm.close_ticket(ticket_number, solution)
    
    if result['success']:
        print(f"✅ Ticket closed successfully!")
        print(f"   {result['message']}\n")
    else:
        print(f"❌ Failed to close ticket: {result['error']}\n")
    
    print("=== All Tests Complete ===")
