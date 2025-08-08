# 🚀 Deployment Guide - LLM Query Retrieval System

This guide provides multiple deployment options for your LLM Query Retrieval System through GitHub.

## 📋 Quick Start - Streamlit Cloud (Recommended)

### Step 1: Deploy to Streamlit Cloud (Free & Easy)
1. **Go to [Streamlit Cloud](https://share.streamlit.io/)**
2. **Sign in with your GitHub account**
3. **Click "New app"**
4. **Repository**: `parkavi817/llm-query-retieval`
5. **Branch**: `main`
6. **Main file path**: `streamlit_app/app.py`
7. **Requirements file**: `requirements-streamlit.txt`
8. **Click "Deploy"** - Your app will be live in 2-3 minutes!

**Live URL**: `https://share.streamlit.io/parkavi817/llm-query-retieval/main/streamlit_app/app.py`

## 🔄 Automated Deployment via GitHub Actions

Your repository is already configured with GitHub Actions for automated deployment. Every push to the main branch will trigger:
- Automated testing
- Docker image building
- Streamlit Cloud deployment

## 🐳 Docker Deployment Options

### Option A: Local Docker Deployment
```bash
# Build the Docker image
docker build -t llm-query-retrieval .

# Run the container
docker run -p 8501:8501 llm-query-retrieval

# Access at: http://localhost:8501
```

### Option B: Docker Compose
```bash
# Using Docker Compose
docker-compose up

# Access at: http://localhost:8501
```

## ☁️ Cloud Platform Deployments

### Heroku Deployment
```bash
# Install Heroku CLI
npm install -g heroku

# Login
heroku login

# Create app
heroku create llm-query-retrieval-app

# Deploy
git push heroku main
```

### Railway Deployment
1. **Go to [Railway](https://railway.app)**
2. **Connect your GitHub repository**
3. **Deploy automatically**

### AWS Deployment
1. **Use AWS Elastic Beanstalk**
2. **Use AWS ECS with Fargate**
3. **Use AWS Lambda + API Gateway**

## 📊 Monitoring & Updates

### GitHub Actions Status
Check your deployment status at:
- **Actions tab**: https://github.com/parkavi817/llm-query-retieval/actions

### Real-time Monitoring
- **Streamlit Cloud Dashboard**: https://share.streamlit.io/
- **GitHub Insights**: Repository → Insights → Actions

## 🆘 Troubleshooting

### Common Issues & Solutions

1. **Streamlit Cloud Deployment Fails**
   - Check requirements.txt for missing dependencies
   - Ensure all imports are correct
   - Verify file paths in streamlit_app/app.py

2. **GitHub Actions Fail**
   - Check the Actions tab for error logs
   - Ensure all secrets are configured
   - Verify Docker build process

3. **Docker Build Issues**
   - Check Dockerfile syntax
   - Ensure all dependencies are available
   - Verify base image compatibility

## 📞 Support
For deployment issues:
1. **Check GitHub Issues**: https://github.com/parkavi817/llm-query-retieval/issues
2. **GitHub Discussions**: https://github.com/parkavi817/llm-query-retieval/discussions
3. **Streamlit Community**: https://discuss.streamlit.io/

## 🎯 Next Steps
1. **Choose your deployment method** (Streamlit Cloud recommended)
2. **Follow the step-by-step instructions**
3. **Monitor your deployment** via GitHub Actions
4. **Scale as needed** based on usage

Your app is ready for production deployment! 🚀
