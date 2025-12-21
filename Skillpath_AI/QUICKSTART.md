# ⚡ SkillPath AI - Quick Start (5 Minutes)

## 📦 One-Command Setup (Windows)

```bash
mkdir skillpath_ai && cd skillpath_ai && mkdir utils data model && type nul > utils\__init__.py
```

## 📦 One-Command Setup (Mac/Linux)

```bash
mkdir -p skillpath_ai/{utils,data,model} && cd skillpath_ai && touch utils/__init__.py
```

## 📋 Copy These Files

After creating the folder structure, create these files:

### 1️⃣ app.py
```python
# Copy the complete app.py code from artifact #1
```

### 2️⃣ requirements.txt
```
streamlit==1.29.0
pandas==2.1.4
numpy==1.26.2
scikit-learn==1.3.2
plotly==5.18.0
pillow==10.1.0
```

### 3️⃣ utils/scoring.py
```python
# Copy the complete scoring.py code from artifact #2
```

### 4️⃣ utils/roadmap_generator.py
```python
# Copy the complete roadmap_generator.py code from artifact #3
```

### 5️⃣ utils/ml_predictor.py
```python
# Copy the complete ml_predictor.py code from artifact #4
```

### 6️⃣ utils/__init__.py
```python
# Copy the __init__.py code from artifact #7
```

### 7️⃣ data/sample_dataset.csv
```csv
# Copy the CSV data from artifact #5
```

## 🚀 Install & Run (3 Commands)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py

# 3. Open browser to http://localhost:8501
```

## ✅ Verify Installation

You should see:
- ✅ Beautiful landing page with gradient header
- ✅ Sidebar navigation
- ✅ "Start Your Journey" button
- ✅ No error messages in terminal

## 🎯 Test the App

1. Click "Start Your Journey"
2. Complete 5-step assessment
3. View your personalized results
4. See career recommendations
5. Explore learning roadmap

## 🐛 Quick Fixes

### Error: "No module named 'utils'"
```bash
# Ensure you're in the right directory
cd skillpath_ai

# Check if utils/__init__.py exists
ls utils/__init__.py  # Mac/Linux
dir utils\__init__.py  # Windows
```

### Error: "No module named 'streamlit'"
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Port 8501 Already in Use
```bash
# Use different port
streamlit run app.py --server.port 8502
```

## 🎨 Customize in 2 Minutes

### Change Colors
In `app.py`, find this section:
```python
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```
Replace `#667eea` and `#764ba2` with your colors.

### Add Your Logo
```python
st.sidebar.image("path/to/logo.png", width=80)
```

### Change App Name
In `app.py`, line 8:
```python
page_title="Your App Name"
```

## 📊 Project Structure Check

```
skillpath_ai/
├── app.py                      ✅
├── requirements.txt            ✅
├── utils/
│   ├── __init__.py            ✅
│   ├── scoring.py             ✅
│   ├── roadmap_generator.py   ✅
│   └── ml_predictor.py        ✅
├── data/
│   └── sample_dataset.csv     ✅
└── model/                      ✅ (empty for now)
```

## 🌐 Deploy to Cloud (5 Minutes)

### Streamlit Cloud (FREE)

1. Push to GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app"
4. Select your repository
5. Click "Deploy"

✅ Your app is now live!

## 🎉 You're Done!

Your SkillPath AI platform is ready to help students discover their perfect career path!

### Next Steps:
- Add more careers to database
- Customize roadmaps
- Add your branding
- Share with students

---

Need help? Check the full README.md for detailed documentation.