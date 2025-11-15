# 🚀 Google Cloud Run Deployment Guide

Deploy your Amharic Chatbot to Google Cloud Run with automatic CI/CD using GitHub Actions.

## Why Google Cloud Run?

- ✅ **FREE Tier**: 2 million requests/month, 360,000 GB-seconds/month
- ✅ **More Resources**: 2GB RAM, 2 CPU cores (vs Streamlit's 1GB)
- ✅ **Better for ML**: Handles PyTorch and YOLOv8 easily
- ✅ **Auto-scaling**: Scales from 0 to many instances
- ✅ **CI/CD**: Automatic deployment on git push

## Prerequisites

1. **Google Cloud Account** (free tier available)
2. **GitHub Account** with your code
3. **Google API Key** for Gemini

---

## Step-by-Step Setup

### Part 1: Google Cloud Setup

#### 1.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click **"Select a Project"** → **"New Project"**
3. Project name: `amharic-chatbot` (or your choice)
4. Click **"Create"**
5. **Copy your Project ID** (you'll need this later)

#### 1.2 Enable Required APIs

Run these commands in [Cloud Shell](https://console.cloud.google.com/home) or local terminal:

```bash
# Set your project ID
PROJECT_ID="your-project-id-here"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

Or enable via Console:
- Go to [APIs & Services](https://console.cloud.google.com/apis/library)
- Search and enable:
  - **Cloud Run API**
  - **Container Registry API**
  - **Cloud Build API**

#### 1.3 Create Service Account

1. Go to [IAM & Admin → Service Accounts](https://console.cloud.google.com/iam-admin/serviceaccounts)
2. Click **"Create Service Account"**
3. **Name**: `github-actions-deployer`
4. Click **"Create and Continue"**
5. **Grant these roles**:
   - Cloud Run Admin
   - Service Account User
   - Storage Admin
6. Click **"Done"**

#### 1.4 Create Service Account Key

1. Click on the service account you just created
2. Go to **"Keys"** tab
3. Click **"Add Key"** → **"Create new key"**
4. Choose **JSON** format
5. Click **"Create"**
6. **Download the JSON file** (keep it safe!)

---

### Part 2: GitHub Secrets Setup

Add these secrets to your GitHub repository:

1. Go to your repo: `https://github.com/hassetshi/amharic-chatbot`
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"** for each:

#### Secret 1: GCP_PROJECT_ID
- **Name**: `GCP_PROJECT_ID`
- **Value**: Your Google Cloud Project ID (e.g., `amharic-chatbot-123456`)

#### Secret 2: GCP_SA_KEY
- **Name**: `GCP_SA_KEY`
- **Value**: Paste the **entire contents** of the JSON key file you downloaded
  ```json
  {
    "type": "service_account",
    "project_id": "your-project",
    "private_key_id": "...",
    ...
  }
  ```

#### Secret 3: GOOGLE_API_KEY
- **Name**: `GOOGLE_API_KEY`
- **Value**: Your Google Gemini API key (e.g., `AIzaSyBXf...`)

---

### Part 3: Deploy

#### Option A: Automatic Deployment (Recommended)

1. **Push your code to GitHub**:
   ```bash
   git push origin main
   ```

2. **Watch the deployment**:
   - Go to your repo → **Actions** tab
   - You'll see the workflow running
   - Wait 5-10 minutes for build & deploy

3. **Get your URL**:
   - Once complete, check the workflow logs for the service URL
   - Or run: `gcloud run services describe amharic-chatbot --region us-central1 --format 'value(status.url)'`

#### Option B: Manual Deployment

```bash
# Set your project
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud run deploy amharic-chatbot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --set-env-vars GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

---

## Configuration

### Adjust Resources

Edit [.github/workflows/deploy-cloud-run.yml](.github/workflows/deploy-cloud-run.yml):

```yaml
--memory 2Gi    # Options: 512Mi, 1Gi, 2Gi, 4Gi
--cpu 2         # Options: 1, 2, 4
--timeout 300   # Max request time in seconds
```

### Change Region

Available regions:
- `us-central1` (Iowa) - Default, free tier eligible
- `us-east1` (South Carolina)
- `europe-west1` (Belgium)
- `asia-east1` (Taiwan)

### Environment Variables

Add more env vars in the workflow:

```yaml
--set-env-vars GOOGLE_API_KEY=${{ secrets.GOOGLE_API_KEY }},OTHER_VAR=value
```

---

## Cost Estimates (Free Tier)

**Free Tier Limits:**
- 2 million requests/month
- 360,000 GB-seconds/month
- 180,000 vCPU-seconds/month

**With 2GB RAM, 2 CPU:**
- Each request uses ~1 second
- **You get ~180,000 requests/month FREE**
- After that: ~$0.00002 per request

**Monthly cost estimate:**
- Light use (1,000 requests/month): **$0**
- Medium use (10,000 requests/month): **$0**
- Heavy use (200,000 requests/month): **~$0.40**

---

## Monitoring & Management

### View Logs

```bash
gcloud run services logs read amharic-chatbot --region us-central1
```

Or in Console: [Cloud Run → amharic-chatbot → Logs](https://console.cloud.google.com/run)

### Update Environment Variables

```bash
gcloud run services update amharic-chatbot \
  --region us-central1 \
  --set-env-vars GOOGLE_API_KEY=new_key
```

### Delete Service

```bash
gcloud run services delete amharic-chatbot --region us-central1
```

---

## Troubleshooting

### Build Fails

**Error**: "Permission denied"
- Check service account has correct roles
- Verify `GCP_SA_KEY` secret is valid JSON

**Error**: "API not enabled"
- Enable Cloud Run, Container Registry, and Cloud Build APIs

### Deployment Fails

**Error**: "Insufficient memory"
- Increase `--memory` to 4Gi
- Use smaller YOLOv8 model (yolov8n.pt)

**Error**: "API Key not found"
- Add `GOOGLE_API_KEY` to GitHub secrets
- Check spelling matches exactly

### App Crashes

**Check logs**:
```bash
gcloud run services logs read amharic-chatbot --region us-central1 --limit 50
```

**Common issues**:
- Model download fails: Check internet connectivity in logs
- Out of memory: Increase RAM or use smaller model
- Timeout: Increase `--timeout` value

---

## CI/CD Workflow

The GitHub Actions workflow automatically:

1. ✅ Checks out code
2. ✅ Authenticates to Google Cloud
3. ✅ Builds Docker image
4. ✅ Pushes to Container Registry
5. ✅ Deploys to Cloud Run
6. ✅ Shows deployment URL

**Triggered on**:
- Every push to `main` branch
- Manual trigger via Actions tab

---

## Security Best Practices

1. ✅ **Never commit secrets** - Use GitHub Secrets
2. ✅ **Rotate API keys** regularly
3. ✅ **Enable authentication** if needed:
   ```bash
   gcloud run services update amharic-chatbot \
     --region us-central1 \
     --no-allow-unauthenticated
   ```
4. ✅ **Monitor usage** in Cloud Console
5. ✅ **Set spending limits** in Billing

---

## Custom Domain (Optional)

1. Verify domain in [Google Search Console](https://search.google.com/search-console)
2. Add domain mapping:
   ```bash
   gcloud run domain-mappings create \
     --service amharic-chatbot \
     --domain your-domain.com \
     --region us-central1
   ```
3. Update DNS records as instructed

---

## Comparison: Streamlit Cloud vs Cloud Run

| Feature | Streamlit Cloud | Cloud Run |
|---------|----------------|-----------|
| **Free Tier** | Unlimited | 2M requests/month |
| **RAM** | 1 GB | 2-4 GB |
| **CPU** | Shared | 1-4 CPUs |
| **Timeout** | Limited | Up to 60 min |
| **ML Models** | Limited | ✅ Full support |
| **Auto-deploy** | ✅ Yes | ✅ Yes (via Actions) |
| **Custom Domain** | Limited | ✅ Full support |
| **Best For** | Simple apps | Production ML apps |

---

## Next Steps

1. ✅ Set up Google Cloud project
2. ✅ Add GitHub secrets
3. ✅ Push code to trigger deployment
4. ✅ Monitor logs and test app
5. ✅ Share your app URL!

---

## Support

- [Cloud Run Documentation](https://cloud.google.com/run/docs)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Pricing Calculator](https://cloud.google.com/products/calculator)

---

**Your app will be live at**: `https://amharic-chatbot-xxxxx-uc.a.run.app`

🎉 **Happy Deploying!**
