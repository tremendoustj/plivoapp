# PLIVO ASSIGNMENT

## Directory Structure :
- api_project :: Contains the source code for message api and it's associated test cases, Dockerfile and requirements.txt
- jenkins :: Contains the groovy file for the required pipeline.
- kubernetes-manifests :: Contains all the required mainfests that is to be applied on the kubernetes cluster.
- terraform :: Contains IaC code for creating a basic EKS Cluster.

### Prerequisites ::
1. AWS Credentials having necessary permissions to create various resources.
2. Docker
3. Terraform cli
4. Python3
5. Jenkins Setup


### 1. api_project
- Setup project
```sh
pip3 install -r requirements.txt
```
- To run the tests
```sh
python3 -m unittest discover -s tests
```
- To run the application
```sh
flask run
```

### 2. terraform
0. Move to terraform directory
``` 
cd terraform 
```
1. Setup AWS Credentials in the CLI
```
export AWS_ACCESS_KEY_ID=<ACCESS KEY>
export AWS_SECRET_ACCESS_KEY=<SECRET KEY>
export AWS_DEFAULT_REGION=us-west-2
```
2. To create an EKS Cluster
```
terraform init
terraform plan
terraform apply
```

### 3. Kubernetes Deployment

1. Set the kubeconfig from previous terraform apply of EKS cluster.
```
export KUBECONFIG="${PWD}/terraform/kubeconfig_plivoapp"
```
2. Apply all the manifests in kubernetes directory using kubectl.
```
kubectl apply -f <PATH-TO-MANIFEST.yaml>
```

### 4. JENKINS Setup.
1. Using pipeline script
- On a jenkins pipeline setup page, select pipeline script in the Pipeline option, and copy paste the contents
2. Using pipelin from SCM
    - In pipeline setup page, select pipeline from SCM
    - Provide name of the file as `Jenkinsfile`.
    - Update the github repo link and provide the correct credentials.

3. The Jenkins pipeline currently has four stages as below
   - Build : Building Docker image
   - Vulnerability Scanning : Security and vulnerability scanning using trivy
   - Push to ECR : If everything works fine, push the image to ECR.
   - Deploy : Deploy app to specific environment 