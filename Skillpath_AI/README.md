# 🎓 SkillPath AI - Complete Setup Guide

## 📁 Project Structure

Create the following folder structure:

```
skillpath_ai/
│
├── app.py                          # Main Streamlit application
├── requirements.txt                 # Python dependencies
│
├── utils/                          # Utility modules
│   ├── __init__.py                 # Empty file to make it a package
│   ├── scoring.py                  # Weighted scoring & career matching
│   ├── roadmap_generator.py        # Learning roadmap generation
│   └── ml_predictor.py             # Course prediction logic
│
├── data/                           # Data files
│   └── sample_dataset.csv          # Training dataset
│
└── model/                          # ML models (optional)
    └── career_model.pkl            # Trained model (if using ML)
```

## 🚀 Installation Steps

### Step 1: Create Project Directory

```bash
mkdir skillpath_ai
cd skillpath_ai
```

### Step 2: Create Folder Structure

```bash
# Create folders
mkdir utils data model

# Create __init__.py for utils package
touch utils/__init__.py

# On Windows, use:
# type nul > utils/__init__.py
```

### Step 3: Create Files

Copy each code artifact into the respective file:

1. **app.py** - Main application (root directory)
2. **requirements.txt** - Dependencies (root directory)
3. **utils/scoring.py** - Scoring module
4. **utils/roadmap_generator.py** - Roadmap generator
5. **utils/ml_predictor.py** - ML predictor
6. **data/sample_dataset.csv** - Sample dataset

### Step 4: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🎯 How to Use

### 1. **Home Page**
- View features and overview
- Click "Start Your Journey" button

### 2. **Assessment (5 Steps)**
- **Step 1**: Select education level and academic performance
- **Step 2**: Choose interests and skills
- **Step 3**: Define personality and learning style
- **Step 4**: Set career goals and budget
- **Step 5**: Add location and industry preferences

### 3. **Results Page**
- View top 5 career recommendations with match scores
- See recommended courses and colleges
- Analyze skill gaps
- Get 6-month personalized roadmap
- Download report (coming soon)

## 🔧 Customization Guide

### Adding New Careers

Edit `utils/scoring.py`, find `get_career_database()` function:

```python
{
    'name': 'Your New Career',
    'related_interests': ['Interest 1', 'Interest 2'],
    'required_skills': ['Skill 1', 'Skill 2'],
    'personality_fit': ['Personality Type'],
    'education_requirements': ['Education Level'],
    'salary_range': '₹X-Y LPA',
    'growth_potential': 'High/Medium/Low',
}
```

### Adding New Roadmaps

Edit `utils/roadmap_generator.py`, find `get_roadmap_template()` function:

```python
'Your Career Name': [
    {
        'phase': 'Month 1 Name',
        'focus': 'What to focus on',
        'goals': ['Goal 1', 'Goal 2', 'Goal 3'],
        'resources': ['Resource 1', 'Resource 2']
    },
    # Add 5 more months...
]
```

### Adding New Courses

Edit `utils/ml_predictor.py`, modify the relevant function:

```python
courses.append({
    'name': 'Course Name',
    'duration': 'X years',
    'cost': '₹X - Y',
    'description': 'What students will learn',
    'colleges': ['College 1', 'College 2', 'College 3']
})
```

### Modifying UI Colors

Edit `app.py`, find the CSS section:

```python
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #YOUR_COLOR1 0%, #YOUR_COLOR2 100%);
    }
</style>
""", unsafe_allow_html=True)
```

## 📊 ML Model Training (Optional)

To train a simple ML model:

```python
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

# Load data
df = pd.read_csv('data/sample_dataset.csv')

# Prepare features (you'll need to encode categorical variables)
# This is a simplified example
X = df[['education_level', 'interests', 'technical_skills']]
y = df['recommended_career']

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# Save model
with open('model/career_model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

## 🌐 Deployment Options

### Option 1: Streamlit Community Cloud (Recommended - FREE)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy!

**Note**: Make sure your GitHub repo includes:
- `app.py`
- `requirements.txt`
- All `utils/` files
- `data/` files

### Option 2: Heroku

```bash
# Install Heroku CLI
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT" > Procfile

# Deploy
heroku login
heroku create skillpath-ai
git push heroku main
```

### Option 3: AWS/Azure/GCP

Use their respective Python/Streamlit deployment guides.

## 🎨 UI Enhancements

### Add Logo

Place your logo in the project folder and update:

```python
st.sidebar.image("path/to/your/logo.png", width=80)
```

### Add Background Image

```python
st.markdown("""
<style>
    .stApp {
        background-image: url("your_image_url");
        background-size: cover;
    }
</style>
""", unsafe_allow_html=True)
```

## 🐛 Troubleshooting

### Import Error

```
ModuleNotFoundError: No module named 'utils'
```

**Solution**: Ensure `utils/__init__.py` exists (can be empty)

### Port Already in Use

```bash
# Run on different port
streamlit run app.py --server.port 8502
```

### Data Not Loading

**Solution**: Check file paths are relative to `app.py` location

## 📈 Future Enhancements

1. **PDF Report Generation**
   - Use ReportLab or FPDF
   - Include charts and roadmap

2. **Real ML Model**
   - Collect more data (500+ samples)
   - Train Random Forest or XGBoost
   - Add prediction confidence scores

3. **User Accounts**
   - Firebase authentication
   - Save progress across sessions
   - Track completed roadmap items

4. **Chatbot Integration**
   - Add AI chatbot for Q&A
   - Use OpenAI API or Anthropic Claude

5. **College Database**
   - Integrate with college APIs
   - Show real-time admission data
   - Add college comparison tool

6. **Job Board Integration**
   - Connect with Naukri/LinkedIn APIs
   - Show relevant job openings
   - Salary trend analysis

## 📞 Support

For issues or questions:
- Check error messages in terminal
- Ensure all dependencies are installed
- Verify file structure matches guide

## 🎉 Success Checklist

- [ ] Project structure created
- [ ] All files copied
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] App runs without errors
- [ ] Can complete full assessment
- [ ] Results page displays correctly
- [ ] Navigation works smoothly

## 📝 License

Free to use for educational purposes. Please credit if used commercially.

---

**Made with ❤️ using Streamlit and Python**

Happy Coding! 🚀