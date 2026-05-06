# ATS Resume Checker - Deployment Guide

## 📋 Overview
This guide explains how to deploy the ATS Resume Checker to Streamlit Cloud.

## 🚀 Deployment Steps

### 1. **Local Testing**
```bash
# Install dependencies
pip install -r requirements.txt

# Create .streamlit/secrets.toml with your API key
echo 'GOOGLE_API_KEY = "your-key-here"' > .streamlit/secrets.toml

# Run the app
streamlit run app.py
```

### 2. **Push to GitHub**
```bash
git add .
git commit -m "ATS Resume Checker - Production Ready"
git push origin main
```

### 3. **Deploy on Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository, branch, and `app.py`
4. Configure secrets:
   - Go to App settings → Secrets
   - Add your `GOOGLE_API_KEY` (same format as local secrets.toml)

## 🔐 Security Best Practices
✅ Never commit `.env` or `.streamlit/secrets.toml` to GitHub
✅ Use Streamlit Cloud's Secrets manager for API keys
✅ Keep `google-genai` library updated
✅ Monitor API usage and set spending limits

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
- **Solution**: Add `GOOGLE_API_KEY` to Streamlit secrets

**Issue**: "Error processing PDF"
- **Solution**: Ensure PDF is valid and not corrupted. Max size is 50MB

**Issue**: "Timeout errors"
- **Solution**: Large PDFs may take longer. Consider splitting into multiple pages

## 📝 Environment Variables
The app now supports both:
- `.env` file (for local development)
- Streamlit secrets (for production)

Priority: `st.secrets` > environment variables
