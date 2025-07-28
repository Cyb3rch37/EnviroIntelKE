#!/bin/bash
# Simple build script for Render
echo "Building frontend..."
cd frontend
npm install --production
npm run build

echo "Copying to backend..."
mkdir -p ../backend/static
cp -r build/* ../backend/static/

echo "Backend setup..."
cd ../backend
pip install -r requirements.txt

echo "Build complete!"
ls -la static/