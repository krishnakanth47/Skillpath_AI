# 🌐 SkillPath AI - Deployment Guide

## 🎯 Deployment Options Comparison

| Platform | Cost | Difficulty | Best For |
|----------|------|------------|----------|
| **Streamlit Cloud** | FREE | ⭐ Easy | Quick deployment, demos |
| **Heroku** | FREE-$7/mo | ⭐⭐ Medium | More control, add-ons |
| **AWS EC2** | $5-20/mo | ⭐⭐⭐ Hard | Enterprise, scalability |
| **DigitalOcean** | $5-10/mo | ⭐⭐ Medium | Good balance |
| **Render** | FREE-$7/mo | ⭐ Easy | Modern alternative |

## 🚀 Option 1: Streamlit Community Cloud (RECOMMENDED - FREE)

### Prerequisites
- GitHub account
- Your code pushed to GitHub

### Step-by-Step Guide

#### 1. Prepare Your Repository

Create `.gitignore`:
```
venv/
__pycache__/
*.pyc
.env
*.pkl
saved_assessments/
.DS_Store
```

#### 2. Push to GitHub

```bash
# Initialize git
git init

# Add files
git add .

# Commit
git commit -m "Initial commit - SkillPath AI"

# Create GitHub repo (via GitHub website)
# Then connect and push
git remote add origin https://github.com/YOUR_USERNAME/skillpath-ai.git
git branch -M main
git push -u origin main
```

#### 3. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click **"New app"**
4. Select:
   - Repository: `YOUR_USERNAME/skillpath-ai`
   - Branch: `main`
   - Main file path: `app.py`
5. Click **"Deploy!"**

#### 4. Configure Settings (Optional)

In Advanced settings:
- **Python version**: 3.9 or 3.10
- **Secrets**: Add any API keys here

#### 5. Get Your URL

Your app will be live at:
```
https://YOUR_USERNAME-skillpath-ai-app-xxxxx.streamlit.app
```

### ✅ Streamlit Cloud Pros
- ✅ Completely FREE
- ✅ Automatic HTTPS
- ✅ Auto-deploys on git push
- ✅ Easy subdomain
- ✅ No server management

### ❌ Streamlit Cloud Cons
- ❌ Resource limits (1GB RAM)
- ❌ Public repos only (for free)
- ❌ Can't run background tasks

---

## 🐳 Option 2: Heroku

### Prerequisites
- Heroku account
- Heroku CLI installed

### Setup Files

#### 1. Create `Procfile`
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

#### 2. Create `runtime.txt`
```
python-3.10.12
```

#### 3. Update `requirements.txt`
```
streamlit==1.29.0
pandas==2.1.4
numpy==1.26.2
scikit-learn==1.3.2
plotly==5.18.0
pillow==10.1.0
```

### Deploy Steps

```bash
# Login to Heroku
heroku login

# Create app
heroku create skillpath-ai

# Add buildpack
heroku buildpacks:add --index 1 heroku/python

# Deploy
git push heroku main

# Open app
heroku open

# View logs
heroku logs --tail
```

### ✅ Heroku Pros
- ✅ Easy deployment
- ✅ Free tier available
- ✅ Good documentation
- ✅ Add-ons ecosystem

### ❌ Heroku Cons
- ❌ Dynos sleep after 30min inactivity (free tier)
- ❌ Limited free hours
- ❌ Can be slow to wake up

---

## ☁️ Option 3: AWS EC2

### Prerequisites
- AWS account
- Basic Linux knowledge

### Step-by-Step

#### 1. Launch EC2 Instance

1. Go to EC2 Dashboard
2. Click "Launch Instance"
3. Choose Ubuntu 22.04 LTS
4. Select t2.micro (free tier)
5. Configure security group:
   - Allow SSH (port 22)
   - Allow HTTP (port 80)
   - Allow Custom TCP (port 8501)
6. Download key pair (.pem file)

#### 2. Connect to Instance

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@YOUR_EC2_IP
```

#### 3. Setup Environment

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3-pip python3-venv -y

# Clone your repo
git clone https://github.com/YOUR_USERNAME/skillpath-ai.git
cd skillpath-ai

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 4. Run with Nginx (Production Setup)

Install Nginx:
```bash
sudo apt install nginx -y
```

Create systemd service `/etc/systemd/system/skillpath.service`:
```ini
[Unit]
Description=SkillPath AI Streamlit App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/skillpath-ai
Environment="PATH=/home/ubuntu/skillpath-ai/venv/bin"
ExecStart=/home/ubuntu/skillpath-ai/venv/bin/streamlit run app.py --server.port=8501

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl start skillpath
sudo systemctl enable skillpath
```

Configure Nginx `/etc/nginx/sites-available/skillpath`:
```nginx
server {
    listen 80;
    server_name YOUR_DOMAIN_OR_IP;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/skillpath /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. Add SSL (Optional but Recommended)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com
```

### ✅ AWS Pros
- ✅ Full control
- ✅ Scalable
- ✅ Professional setup
- ✅ Many additional services

### ❌ AWS Cons
- ❌ Requires Linux knowledge
- ❌ More maintenance
- ❌ Not free (after 12 months)

---

## 🎨 Option 4: DigitalOcean

### Quick Deploy with App Platform

1. Sign up at [DigitalOcean](https://www.digitalocean.com)
2. Click "Create" → "Apps"
3. Connect GitHub repository
4. Configure:
   - Build command: `pip install -r requirements.txt`
   - Run command: `streamlit run app.py --server.port=8080 --server.address=0.0.0.0`
   - Port: 8080
5. Deploy

### With Droplet (Manual)

Similar to AWS EC2 but simpler:

```bash
# Create droplet (Ubuntu 22.04)
# SSH into droplet
ssh root@YOUR_DROPLET_IP

# Setup (same as AWS EC2 steps 3-4)
```

---

## 🆕 Option 5: Render

### Simple Deployment

1. Go to [render.com](https://render.com)
2. Sign up/Login
3. Click "New" → "Web Service"
4. Connect GitHub repo
5. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
6. Deploy

### ✅ Render Pros
- ✅ Modern platform
- ✅ Free tier
- ✅ Auto SSL
- ✅ Easy to use

---

## 🔒 Security Best Practices

### 1. Environment Variables

Never commit sensitive data. Use `.env`:

```bash
# .env
OPENAI_API_KEY=your_key_here
DATABASE_URL=your_db_url
```

Load in app:
```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
```

### 2. HTTPS

Always use HTTPS in production:
- Streamlit Cloud: Automatic
- Others: Use Let's Encrypt/Certbot

### 3. Rate Limiting

Prevent abuse:
```python
import streamlit as st
from datetime import datetime, timedelta

def rate_limit():
    if 'last_request' not in st.session_state:
        st.session_state.last_request = datetime.now()
        return True
    
    time_diff = datetime.now() - st.session_state.last_request
    if time_diff < timedelta(seconds=5):
        st.error("Please wait before submitting again")
        return False
    
    st.session_state.last_request = datetime.now()
    return True
```

### 4. Input Validation

Sanitize user inputs:
```python
def validate_email(email):
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

---

## 📊 Monitoring

### Option 1: Built-in Streamlit Analytics

Access via Streamlit Cloud dashboard:
- Page views
- User sessions
- Error logs

### Option 2: Google Analytics

Add to `app.py`:
```python
st.markdown("""
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'GA_MEASUREMENT_ID');
    </script>
""", unsafe_allow_html=True)
```

### Option 3: Error Tracking with Sentry

```bash
pip install sentry-sdk
```

```python
import sentry_sdk

sentry_sdk.init(
    dsn="YOUR_SENTRY_DSN",
    traces_sample_rate=1.0
)
```

---

## 🔄 CI/CD Pipeline

### GitHub Actions Example

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Streamlit Cloud

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/
    
    - name: Deploy to Streamlit Cloud
      run: |
        # Streamlit Cloud auto-deploys on push
        echo "Deployed successfully!"
```

---

## 📝 Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] `.gitignore` configured
- [ ] `requirements.txt` updated
- [ ] Secrets/API keys secured
- [ ] Domain name purchased (optional)
- [ ] SSL certificate configured
- [ ] Analytics setup
- [ ] Error monitoring enabled
- [ ] Backup strategy in place
- [ ] Documentation updated

---

## 🆘 Troubleshooting

### App Won't Start

```bash
# Check logs
heroku logs --tail  # Heroku
sudo journalctl -u skillpath  # AWS/DigitalOcean

# Common issues:
# 1. Port binding
# 2. Missing dependencies
# 3. File permissions
```

### Memory Issues

Optimize:
```python
# Use caching
@st.cache_data
def load_data():
    return pd.read_csv('data.csv')

# Limit DataFrame size
df = df.head(1000)  # Only show first 1000 rows
```

### Slow Performance

1. Enable caching
2. Optimize images
3. Reduce data processing
4. Use CDN for static assets

---

## 🎉 Post-Deployment

1. **Test thoroughly** on production
2. **Share your app** on social media
3. **Collect feedback** from users
4. **Monitor usage** and errors
5. **Iterate and improve**

---

**Congratulations! Your SkillPath AI is now live! 🚀**