# URL Health Monitor

A Python service that monitors the availability and response time of two external URLs and exposes Prometheus-formatted metrics.

## Prerequisites

- Python 3.8 or higher
- Docker
- kubectl CLI
- Kubernetes cluster + Helm 3

## Quickstart

### 0. Define image variables
```bash
export IMAGE_NAME=url-health-monitor   # or any repo/name you prefer
export IMAGE_TAG=latest                # or any tag/version you prefer
```

### 1. Clone the repository
```bash
git clone https://github.com/PavlinK1/url-health-monitor.git
cd url-health-monitor
```

### 2. Create & activate a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install Docker (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install -y docker.io
sudo usermod -aG docker $USER
newgrp docker or logout/login to apply group changes
# NOTE: Adding your user to the docker group lets you run Docker (and kind)
#       without sudo. Skip this step and you’ll need sudo for every command
#       below.
```

### 5. Install kubectl and helm
```bash
sudo snap install kubectl --classic
sudo snap install helm --classic
```

### 6. Build the Docker image
```bash
docker build -t $IMAGE_NAME:$IMAGE_TAG .
```

### 7. Create a local Kubernetes cluster with kind
```bash
# Install kind:
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.21.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Create cluster and load your image:
kind create cluster
kind load docker-image $IMAGE_NAME:$IMAGE_TAG
```

### 8. Update Helm chart values (Optional if variables are not used)
In `charts/url-health-monitor/values.yaml`, set your local image:
```yaml
image:
  repository: ${IMAGE_NAME}   # e.g. url-health-monitor
  tag:        ${IMAGE_TAG}    # e.g. latest
```

### 9. Deploy with Helm
```bash
helm upgrade --install url-health-monitor charts/url-health-monitor \
  --set image.repository=$IMAGE_NAME                                \
  --set image.tag=$IMAGE_TAG                                        \
  --wait
```

### 10. Verify deployment
```bash
kubectl get pods,svc -l app.kubernetes.io/instance=url-health-monitor
kubectl port-forward svc/url-health-monitor 8000:8000
# NOTE: AFTER port-forwarding open http://localhost:8000!!
```

## Cleanup

```bash
helm uninstall url-health-monitor
deactivate
```
