# Installing Category IPN Generator Plugin to Azure InvenTree Container

## 🎯 Recommended Method: Install via Git

This is the **easiest and most maintainable** method for Azure containers.

### Prerequisites
- Your InvenTree container running in Azure Container Apps
- Azure CLI installed locally
- This plugin code pushed to a Git repository (GitHub, Azure DevOps, etc.)

### Step-by-Step Instructions

#### 1. **Package the Plugin** (Optional - for testing)

```bash
cd /Users/Lokesh/EpconChat/CMS/Plugins/IPN_Numbering
python setup.py bdist_wheel
```

This creates: `dist/inventree_category_ipn_generator-1.0.0-py3-none-any.whl`

---

#### 2. **Push to Git Repository**

```bash
# If not already in a git repo
cd /Users/Lokesh/EpconChat/CMS
git add Plugins/IPN_Numbering
git commit -m "Add Category IPN Generator plugin v1.0.0"
git push origin main
```

---

#### 3. **Connect to Your Azure Container**

```bash
# Get container access
az containerapp exec \
  --name epcon-ai \
  --resource-group <your-resource-group> \
  --command /bin/bash
```

Or if using Azure Container Instances:
```bash
az container exec \
  --name epcon-ai \
  --resource-group <your-resource-group> \
  --exec-command /bin/bash
```

---

#### 4. **Install Plugin from Git**

Once inside the container:

```bash
# Install directly from your Git repository
pip install git+https://github.com/<your-org>/EpconChat.git#subdirectory=CMS/Plugins/IPN_Numbering

# Or if using Azure DevOps:
pip install git+https://dev.azure.com/<org>/<project>/_git/<repo>#subdirectory=CMS/Plugins/IPN_Numbering

# Or if using a specific branch:
pip install git+https://github.com/<your-org>/EpconChat.git@main#subdirectory=CMS/Plugins/IPN_Numbering
```

---

#### 5. **Verify Installation**

```bash
# Check if plugin is installed
pip list | grep inventree-category-ipn

# Should show:
# inventree-category-ipn-generator  1.0.0
```

---

#### 6. **Restart InvenTree**

```bash
# Option A: Using invoke (if available)
invoke server restart

# Option B: Using supervisorctl (common in containers)
supervisorctl restart inventree

# Option C: Exit and restart the entire container
exit
# Then restart container via Azure Portal or CLI
```

---

#### 7. **Activate Plugin in InvenTree UI**

1. Log into InvenTree: `https://epcon-ai.kindpebble-bfe407e4.eastus2.azurecontainerapps.io`
2. Go to **Settings** → **Plugins**
3. Find **"Category IPN Generator"**
4. Click **"Enable"** or toggle the switch
5. Configure settings:
   - ✅ Active: ON
   - ✅ On Create: ON
   - ✅ Skip if IPN Exists: ON
   - 🔢 Digit Length: 5
   - 📝 Separator: `-`

---

## 🐳 Alternative: Build Custom Docker Image (Production)

For a more permanent solution, build a custom image with the plugin pre-installed.

### Create `Dockerfile.custom`

```dockerfile
# Extend official InvenTree image
FROM inventree/inventree:stable

# Switch to root for installations
USER root

# Install plugin from git
RUN pip install --no-cache-dir \
    git+https://github.com/<your-org>/EpconChat.git#subdirectory=CMS/Plugins/IPN_Numbering

# Switch back to inventree user
USER inventree

# Use base image's entrypoint
```

### Build and Deploy

```bash
# Build custom image
docker build -f Dockerfile.custom -t epcon-inventree-custom:latest .

# Tag for Azure Container Registry
docker tag epcon-inventree-custom:latest <your-acr>.azurecr.io/epcon-inventree:latest

# Login to ACR
az acr login --name <your-acr>

# Push to registry
docker push <your-acr>.azurecr.io/epcon-inventree:latest

# Update Azure Container App
az containerapp update \
  --name epcon-ai \
  --resource-group <your-resource-group> \
  --image <your-acr>.azurecr.io/epcon-inventree:latest
```

---

## 📦 Alternative: Install from Local Wheel File

If you can't use Git, you can upload the wheel file directly.

### Option A: Upload to Azure Storage

```bash
# Build the wheel
python setup.py bdist_wheel

# Upload to Azure Blob Storage
az storage blob upload \
  --account-name <storage-account> \
  --container-name plugins \
  --name inventree_category_ipn_generator-1.0.0-py3-none-any.whl \
  --file dist/inventree_category_ipn_generator-1.0.0-py3-none-any.whl

# Get SAS URL
az storage blob generate-sas \
  --account-name <storage-account> \
  --container-name plugins \
  --name inventree_category_ipn_generator-1.0.0-py3-none-any.whl \
  --permissions r \
  --expiry 2025-12-31 \
  --https-only \
  --full-uri

# In container, install from URL:
pip install "https://<storage-account>.blob.core.windows.net/plugins/inventree_category_ipn_generator-1.0.0-py3-none-any.whl?<sas-token>"
```

### Option B: Copy File Directly

```bash
# Copy wheel to container (if you have SSH/exec access)
# This varies by Azure Container setup

# Inside container:
pip install /path/to/inventree_category_ipn_generator-1.0.0-py3-none-any.whl
```

---

## ✅ Verification Steps

After installation, verify everything works:

### 1. **Check Plugin is Loaded**

```bash
# Inside container
python manage.py shell

>>> from cat_code_ipn_generator.core import CategoryIPNGeneratorPlugin
>>> plugin = CategoryIPNGeneratorPlugin()
>>> print(plugin.NAME)
# Should print: CategoryIPNGenerator
>>> exit()
```

### 2. **Check Plugin in UI**

- Go to Settings → Plugins
- Look for "Category IPN Generator"
- Should show version 1.0.0

### 3. **Test IPN Generation**

- Create a new part in a category with codes
- Leave IPN field blank
- Save
- IPN should be automatically assigned (e.g., "01-18-00001")

---

## 🔧 Troubleshooting

### Plugin Not Showing in UI

```bash
# Rebuild plugin index
python manage.py collectplugins

# Restart server
invoke server restart
```

### Import Errors

```bash
# Check if package is installed
pip show inventree-category-ipn-generator

# Check Python path
python -c "import cat_code_ipn_generator; print(cat_code_ipn_generator.__file__)"
```

### Permission Issues

```bash
# Ensure running as inventree user
whoami  # Should show 'inventree'

# If root, switch user:
su - inventree
```

---

## 🎯 Recommended Approach for Your Setup

**For Testing/Development:**
→ Use **Install via Git** (Method 1)

**For Production:**
→ Use **Custom Docker Image** (Method 2)

This ensures the plugin persists across container restarts and is version-controlled.
