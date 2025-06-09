#!/bin/bash

### This script watches for the existence of a Docker image in a container registry
### and deploys a Kubernetes configuration file when the image is found.
### Usage: ./watch-and-deploy-kube.sh <image-tag> <kube-config-file>
### Example: ./watch-and-deploy-kube.sh v1.0.0 deployment.yaml

while true
do

    timeout 1s docker pull ghcr.io/ucsd-e4e/fishsense-data-processing-worker:$1 > /dev/null 2>&1
    if [ $? -eq 124 ]; then
        echo "Image exists, deploying to kubernetes..."

        break
    else
        echo "Image not found, waiting for 5 seconds..."
        sleep 5
    fi

done
    
# Deploy the changes to the Kubernetes cluster
kubectl apply -f $2
