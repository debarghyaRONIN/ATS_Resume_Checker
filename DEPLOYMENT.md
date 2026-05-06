# ATS Resume Checker - Deployment Guide

## 📋 Overview
This guide explains how to deploy the ATS Resume Checker to Streamlit Cloud. The app uses **Xai's Grok API** for intelligent resume analysis.

## 🚀 Deployment Steps

### 1. **Get Grok API Key**
1. Visit [api.x.ai](https://api.x.ai) 
2. Sign up or log in
3. Generate an API key from your dashboard
4. Keep it safe - you'll need it for deployment

### 2. **Local Testing**
```bash
# Install dependencies
pip install -r requirements.txt

# Create .streamlit/secrets.toml with your API key
echo 'GROK_API_KEY = "your-key-here"' > .streamlit/secrets.toml

# Run the app
streamlit run app.py
```

### 3. **Push to GitHub**
```bash
git add .
git commit -m "ATS Resume Checker - Grok Integration"
git push origin main
```

### 4. **Deploy on Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository, branch, and `app.py`
4. Configure secrets:
   - Go to App settings → Secrets
   - Add your `GROK_API_KEY` (same format as local secrets.toml)

## ✅ Why Grok?

- **Cost-effective**: Competitive pricing compared to other AI APIs
- **Multimodal**: Strong vision capabilities for resume analysis
- **Fast**: Quick response times for better user experience
- **Reliable**: Consistent performance for production use

## 🔐 Security Best Practices
✅ Never commit `.env` or `.streamlit/secrets.toml` to GitHub
✅ Use Streamlit Cloud's Secrets manager for API keys
✅ Monitor your Grok API usage and set spending limits
✅ Use environment variables for local development

## 📊 Production Features Enabled
✅ Error handling with user-friendly messages
✅ API key validation on startup
✅ PDF caching to reduce processing time
✅ Logging for debugging
✅ Input validation for all fields
✅ Optimized PDF conversion (1.5x resolution)
✅ Loading spinners for better UX
✅ File size validation (50MB max)

## 🐛 Troubleshooting

**Issue**: "API Key not found"
- **Solution**: Add `GROK_API_KEY` to Streamlit secrets

**Issue**: "Error processing PDF"
- **Solution**: Ensure PDF is valid and not corrupted. Max size is 50MB

**Issue**: "Request timeout"
- **Solution**: Check your internet connection. Grok API may take 10-30 seconds for large resumes

**Issue**: "401 Unauthorized"
- **Solution**: Verify your GROK_API_KEY is correct in Streamlit secrets

## 📝 Environment Variables
The app now supports both:
- `.env` file (for local development) - use GROK_API_KEY
- Streamlit secrets (for production) - use GROK_API_KEY

Priority: `st.secrets` > environment variables
