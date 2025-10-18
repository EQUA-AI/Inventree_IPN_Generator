#!/bin/bash
# Install IPN Generator Plugin to Azure InvenTree Container
# Usage: ./install_to_azure.sh

set -e

echo "🔨 Building plugin package..."
cd "$(dirname "$0")"
python setup.py bdist_wheel

echo "📦 Package built: $(ls -1 dist/*.whl | tail -1)"

# Get the wheel file path
WHEEL_FILE=$(ls -1 dist/*.whl | tail -1)
WHEEL_NAME=$(basename "$WHEEL_FILE")

echo ""
echo "✅ Plugin packaged successfully!"
echo ""
echo "📋 Next steps to install in Azure container:"
echo ""
echo "Method 1: Direct pip install (if you have container access)"
echo "  1. Copy wheel to container:"
echo "     az containerapp exec --name epcon-ai --resource-group <your-rg> --command /bin/bash"
echo "     # Inside container, run:"
echo "     pip install /path/to/$WHEEL_NAME"
echo "     invoke server restart"
echo ""
echo "Method 2: Install from Git (easiest)"
echo "  1. Push this plugin to your Git repo"
echo "  2. In container, run:"
echo "     pip install git+https://github.com/<your-org>/<your-repo>.git#subdirectory=Plugins/IPN_Numbering"
echo "     invoke server restart"
echo ""
echo "Method 3: Build custom Docker image (production)"
echo "  See Dockerfile.custom and build instructions in INSTALL_AZURE.md"
echo ""
