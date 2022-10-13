# Solitan CV converter
Converts a Solita CV pdf into a word cv format from BNP paribas.

## Installation

1. To run front-end

```
cd frontend
npm install -force
npm run serve
```
2. To run back-end

```
cd backend
python main.py
```

## Deploymeny to Azure Cloud Services

### Backend API:
 
 The backend has been deployed as a container running on Azure Apps, the code has being build in the moment on a MAC using Buildx Docker to build it in the linux amd64 architecture needed for the azure instance.

```
 docker buildx build \
  --platform linux/amd64 \
  --load -t cvtransformer.azurecr.io/cv-transformer-flask-api:latest .
  ```
