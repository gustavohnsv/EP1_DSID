#!/bin/bash

# Input your Docker Hub username to push the images
DOCKER_USER="gustavohnsv"

# (optional)
TAG="latest"

# Build/Push processs
echo "🔧 Construindo benchmark_servers..."
docker build -t $DOCKER_USER/benchmark_servers:$TAG -f Dockerfile.servers .

echo "🔧 Construindo grpc-client..."
docker build -t $DOCKER_USER/grpc_client:$TAG -f Dockerfile.grpc-client .

echo "🔧 Construindo jsonrpc-client..."
docker build -t $DOCKER_USER/jsonrpc_client:$TAG -f Dockerfile.jsonrpc-client .

echo "✅ Tudo pronto!"
