# 🚀 Deployment Guide - Streamlit Community Cloud

This guide will help you deploy your Amharic Chatbot to Streamlit Community Cloud for FREE.

## Prerequisites

- GitHub account with your code pushed to a public repository
- Google API Key (for Gemini)
- Streamlit Community Cloud account (free)

## Step-by-Step Deployment

### 1. Sign up for Streamlit Community Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign up"** or **"Continue with GitHub"**
3. Authorize Streamlit to access your GitHub account
4. Complete the signup process

### 2. Deploy Your App

1. **Click "New app"** button in the Streamlit dashboard
2. Fill in the deployment form:
   - **Repository**: `hassetshi/amharic-chatbot`
   - **Branch**: `main`
   - **Main file path**: `app.py`
   - **App URL** (optional): Choose a custom subdomain like `amharic-chatbot-yourname`

3. Click **"Deploy!"**

### 3. Configure Secrets (Important!)

Your app needs the Google API Key to work. Add it as a secret:

1. Once deployed, click on **"Settings"** (⚙️ icon) in your app dashboard
2. Go to **"Secrets"** section
3. Add your API key in this format:

```toml
GOOGLE_API_KEY = "AIzaSyD...your_actual_api_key...xyz"
```

4. Click **"Save"**
5. Your app will automatically restart with the new secrets

### 4. Update app.py to Read Streamlit Secrets

The app needs a small modification to read secrets from Streamlit Cloud. Update the `initialize_models()` function in [app.py](app.py):

```python
@st.cache_resource
def initialize_models():
    """Initialize the object detector and chatbot (cached)"""

    # Try to get API key from Streamlit secrets first, then from .env
    try:
        api_key = st.secrets["GOOGLE_API_KEY"]
    except:
        api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        st.error("⚠️ Google API Key not found. Please set GOOGLE_API_KEY in Streamlit secrets")
        st.stop()

    detector = ObjectDetector(model_path="yolov8n.pt")
    chatbot = AmharicChatbot(api_key=api_key)

    return detector, chatbot
```

### 5. Monitor Your App

- **App URL**: Your app will be available at `https://your-app-name.streamlit.app`
- **Logs**: View real-time logs in the Streamlit dashboard
- **Analytics**: Check usage statistics in the dashboard
- **Reboot**: Click "Reboot app" if something goes wrong

## Important Notes

### Resource Limits (Free Tier)

- **RAM**: 1 GB (sufficient for YOLOv8n model)
- **CPU**: Shared resources
- **Storage**: Limited (models auto-download)
- **Sleep**: Apps sleep after inactivity, wake up on first visit

### Model Considerations

The free tier works best with:
- `yolov8n.pt` (Nano) - ✅ Recommended
- `yolov8s.pt` (Small) - ⚠️ May work but slower
- Larger models - ❌ May exceed memory limits

### Auto-Updates

Your app automatically redeploys when you push to the `main` branch on GitHub!

## Troubleshooting

### App Crashes or Out of Memory

**Solution**: Use the nano model (yolov8n.pt) instead of larger models

```python
detector = ObjectDetector(model_path="yolov8n.pt")  # Smallest model
```

### API Key Not Found

**Solution**: Make sure you added the secret correctly:
1. Go to app settings → Secrets
2. Use exact format: `GOOGLE_API_KEY = "your_key"`
3. No extra quotes or spaces
4. Click Save and reboot

### Model Download Issues

**Solution**: The YOLOv8 model downloads on first run. If it fails:
1. Check the logs for errors
2. Reboot the app
3. The model will retry downloading

### Amharic Text Not Displaying

**Solution**: This is usually a browser issue
- Try Chrome, Firefox, or Edge
- Clear browser cache
- The Streamlit Cloud servers support Unicode/Ge'ez script

## Making Changes

1. Make changes to your local code
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push origin main
   ```
3. Streamlit Cloud automatically detects changes and redeploys
4. Watch the logs to ensure successful deployment

## Custom Domain (Optional)

You can use a custom domain:
1. Go to app settings
2. Click "Custom domain"
3. Follow the DNS configuration instructions

## Privacy & Security

- **Public Apps**: Free tier apps are public (anyone can access)
- **Secrets**: API keys are encrypted and not visible in logs
- **Code**: Must be in a public GitHub repository

## Need More Resources?

If you outgrow the free tier:
- Upgrade to Streamlit Cloud Teams ($20/month)
- Consider Google Cloud Run or AWS for production
- Use Docker for custom deployments

## Support

- [Streamlit Community Forum](https://discuss.streamlit.io/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Deployment Troubleshooting](https://docs.streamlit.io/streamlit-community-cloud/get-started/deploy-an-app#common-deployment-issues)

---

**Your app will be live at**: `https://your-app-name.streamlit.app`

**Deployment Time**: Usually 2-5 minutes for first deployment

**Cost**: $0 (Completely FREE!)

🎉 **Happy Deploying!**
