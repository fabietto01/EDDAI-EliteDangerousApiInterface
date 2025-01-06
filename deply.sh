#!/bin/bash

# Pull the latest changes from the git repository
git pull --rebase origin main

# Rebuild the Docker image
docker build --file eddai_EliteDangerousApiInterface\Dockerfile -t eddaielitedangerousapiinterface:latest "eddai_EliteDangerousApiInterface"

# Apply the latest migrations
docker run --env-file .env --rm eddaielitedangerousapiinterface:latest python manage.py migrate

# Start the services using docker-compose
docker-compose up -d --build