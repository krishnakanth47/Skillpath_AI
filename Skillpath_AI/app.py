import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import pickle
import os
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="SkillPath AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - UPDATED WITH FLOATING ICON AND WHITE HEADER
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        text-align: center;
        padding: 1rem 0;
        animation: fadeIn 1.5s;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .sub-header {
        font-size: 1.3rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .result-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 1rem 0;
    }
    
    .roadmap-month {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 2px solid #e0e0e0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .skill-badge {
        display: inline-block;
        background: #667eea;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        margin: 0.2rem;
        font-size: 0.9rem;
    }
    
    .score-bar {
        background: #e0e0e0;
        border-radius: 10px;
        height: 25px;
        margin: 0.5rem 0;
    }
    
    .score-fill {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.7rem 2rem;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Floating Icon Styles */
    .floating-icon-container {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
    }
    
    .floating-icon-link {
        display: block;
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        text-decoration: none;
        transition: all 0.3s ease;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .floating-icon-link:hover {
        transform: scale(1.1) translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
        animation: none;
    }
    
    .floating-icon-link img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        border-radius: 50%;
    }
    
    .floating-icon-link svg {
        width: 30px;
        height: 30px;
        fill: white;
    }
    
    .floating-tooltip {
        position: absolute;
        bottom: 70px;
        right: 0;
        background: rgba(0, 0, 0, 0.85);
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 13px;
        white-space: nowrap;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        pointer-events: none;
        font-family: Arial, sans-serif;
    }
    
    .floating-tooltip::after {
        content: '';
        position: absolute;
        bottom: -6px;
        right: 20px;
        width: 0;
        height: 0;
        border-left: 6px solid transparent;
        border-right: 6px solid transparent;
        border-top: 6px solid rgba(0, 0, 0, 0.85);
    }
    
    .floating-icon-link:hover .floating-tooltip {
        opacity: 1;
        visibility: visible;
        bottom: 75px;
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        }
        50% {
            box-shadow: 0 4px 25px rgba(102, 126, 234, 0.7);
        }
    }
    
    .floating-icon-link {
        animation: pulse 2s infinite;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'assessment_data' not in st.session_state:
    st.session_state.assessment_data = {}

# Import utility functions
from utils.scoring import calculate_weighted_score, predict_career_cluster
from utils.roadmap_generator import generate_personalized_roadmap
from utils.ml_predictor import load_model, predict_best_paths

# Function to add floating icon
def add_floating_icon():
    """Add a floating icon that links to portfolio"""
    import os
    import base64
    
    # Try to load profile image
    profile_image_path = "profile.png"  # You can change this to your image filename
    
    if os.path.exists(profile_image_path):
        try:
            with open(profile_image_path, "rb") as f:
                profile_data = base64.b64encode(f.read()).decode()
                image_html = f'<img src="data:image/png;base64,{profile_data}" alt="Profile">'
        except Exception as e:
            # Fallback to SVG icon if image fails
            image_html = '''<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
            </svg>'''
    else:
        # Fallback to SVG icon
        image_html = '''<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 3c1.66 0 3 1.34 3 3s-1.34 3-3 3-3-1.34-3-3 1.34-3 3-3zm0 14.2c-2.5 0-4.71-1.28-6-3.22.03-1.99 4-3.08 6-3.08 1.99 0 5.97 1.09 6 3.08-1.29 1.94-3.5 3.22-6 3.22z"/>
        </svg>'''
    
    st.markdown(f"""
    <div class="floating-icon-container">
        <a href="https://krishnakanth-portfolio47.vercel.app/" 
           target="_blank" 
           class="floating-icon-link"
           rel="noopener noreferrer">
            {image_html}
            <div class="floating-tooltip">For any suggestions</div>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    # Logo section
    try:
        st.image("logo.png", width=275)
    except:
        # Fallback to emoji if image fails
        st.markdown("""
        <div style='text-align: center; padding: 0.5rem 0;'>
            <div style='font-size: 3rem;'>🎓</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-top: -10px;'>
        <h2 style='margin: 0; font-size: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>SkillPath AI</h2>
        <p style='margin: 0; font-size: 0.8rem; color: #888;'>Career Advisor</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### Navigation")
    
    if st.button("🏠 Home", use_container_width=True, key="nav_home"):
        st.session_state.page = 'home'
        st.rerun()
    
    if st.button("📋 Assessment", use_container_width=True, key="nav_assessment"):
        st.session_state.page = 'assessment'
        st.rerun()
    
    if st.button("🎯 Results", use_container_width=True, key="nav_results"):
        if st.session_state.assessment_data:
            st.session_state.page = 'results'
            st.rerun()
        else:
            st.warning("Complete assessment first!")

# HOME PAGE
def show_home():
    # Auto-Rotating Banner Carousel with Base64 Embedded Images
    import os
    import base64
    import streamlit.components.v1 as components
    
    # List of banner images
    banners = ["banner1.png", "banner2.png", "banner3.png"]
    
    # Check which banners exist and convert to base64
    available_banners = []
    for banner in banners:
        if os.path.exists(banner):
            try:
                with open(banner, "rb") as f:
                    banner_data = base64.b64encode(f.read()).decode()
                    available_banners.append(banner_data)
            except Exception as e:
                st.error(f"Error loading {banner}: {e}")
    
    if available_banners and len(available_banners) > 1:
        # Create banner images as base64 data URLs
        banner_images = [f'data:image/png;base64,{b}' for b in available_banners]
        
        # Create HTML carousel
        carousel_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
        <style>
        body {{
            margin: 0;
            padding: 0;
            background: transparent;
        }}
        
        .banner-slide {{
            display: none;
            width: 100%;
            height: 100%;
            position: absolute;
            top: 0;
            left: 0;
        }}
        
        .banner-slide.active {{
            display: block;
            animation: fadeIn 1s ease-in-out;
        }}
        
        .banner-slide img {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.3s ease;
        }}
        
        .banner-carousel:hover img {{
            transform: scale(1.02);
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        .banner-dots {{
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            text-align: center;
            z-index: 10;
        }}
        
        .dot {{
            height: 12px;
            width: 12px;
            margin: 0 5px;
            background-color: rgba(255, 255, 255, 0.5);
            border-radius: 50%;
            display: inline-block;
            transition: all 0.3s ease;
            cursor: pointer;
        }}
        
        .dot.active {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            transform: scale(1.3);
        }}
        </style>
        </head>
        <body>
        <div class="banner-carousel" id="carousel">
            <!-- Slides will be added by JavaScript -->
        </div>
        
        <script>
        const bannerImages = {banner_images};
        const carousel = document.getElementById('carousel');
        let currentSlide = 0;
        let slides = [];
        let dots = [];
        
        // Create slides
        bannerImages.forEach((imageSrc, index) => {{
            const slideDiv = document.createElement('div');
            slideDiv.className = 'banner-slide' + (index === 0 ? ' active' : '');
            
            const img = document.createElement('img');
            img.src = imageSrc;
            img.alt = 'Banner ' + (index + 1);
            img.onerror = function() {{
                console.error('Failed to load image:', imageSrc.substring(0, 50) + '...');
            }};
            
            slideDiv.appendChild(img);
            carousel.appendChild(slideDiv);
            slides.push(slideDiv);
        }});
        
        // Create dots
        const dotsDiv = document.createElement('div');
        dotsDiv.className = 'banner-dots';
        
        bannerImages.forEach((_, index) => {{
            const dot = document.createElement('span');
            dot.className = 'dot' + (index === 0 ? ' active' : '');
            dot.onclick = () => showSlide(index);
            dotsDiv.appendChild(dot);
            dots.push(dot);
        }});
        
        carousel.appendChild(dotsDiv);
        
        function showSlide(index) {{
            slides.forEach(slide => slide.classList.remove('active'));
            dots.forEach(dot => dot.classList.remove('active'));
            
            slides[index].classList.add('active');
            dots[index].classList.add('active');
            currentSlide = index;
        }}
        
        function nextSlide() {{
            currentSlide = (currentSlide + 1) % bannerImages.length;
            showSlide(currentSlide);
        }}
        
        // Auto-advance every 5 seconds
        setInterval(nextSlide, 5000);
        </script>
        </body>
        </html>
        """
        
        # Render the HTML component
        components.html(carousel_html, height=350)
    
    elif available_banners and len(available_banners) == 1:
        # Only one banner - show with base64
        st.markdown(f"""
        <style>
        .single-banner {{
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
            margin-bottom: 2rem;
        }}
        .single-banner img {{
            width: 100%;
            border-radius: 20px;
        }}
        </style>
        <div class="single-banner">
            <img src="data:image/png;base64,{available_banners[0]}" alt="Banner">
        </div>
        """, unsafe_allow_html=True)
    
    else:
        # Fallback if no banners found
        st.warning("⚠️ No banner images found! Add banner1.png, banner2.png, banner3.png to your project folder.")
        st.markdown("""
        <div style='
            width: 100%;
            height: 250px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 20px 60px rgba(102, 126, 234, 0.4);
            margin-bottom: 2rem;
        '>
            <h1 style='color: white; font-size: 3rem; margin: 0;'>🎓 SkillPath AI</h1>
        </div>
        """, unsafe_allow_html=True)
    
    # Main header and subtitle with gradient background
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    '>
        <h1 class="main-header">🎓 SkillPath AI</h1>
        <p style="text-align: center; color: rgba(255,255,255,0.9); font-size: 1.3rem; margin: 0;">Your Personalized AI Career & Education Advisor</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")  # Add spacing
    
    # Hero section - Feature Cards
    st.markdown("## 💡 What We Offer")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Smart Assessment</h3>
            <p>AI-powered evaluation of your interests, skills, and personality</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🚀 Career Roadmap</h3>
            <p>Month-by-month personalized learning path to your dream career</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>📚 Course Recommendations</h3>
            <p>Best courses and colleges matched to your profile</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    st.divider()
    
    # How it works
    st.markdown("## 🔍 How It Works")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("### 1️⃣ Complete Assessment")
        st.write("Answer questions about your interests, skills, and goals")
    
    with col2:
        st.markdown("### 2️⃣ AI Analysis")
        st.write("")
        st.write("")
        st.write("Our ML models analyze your profile")
    
    with col3:
        st.markdown("### 3️⃣ Get Suggestions")
        st.write("Receive personalized career and course suggestions")
    
    with col4:
        st.markdown("### 4️⃣ Follow Roadmap")
        st.write("Access your customized learning path")
    
    st.divider()
    
    # CTA
    st.markdown("### 🎉 Ready to discover your perfect career path?")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Your Journey", use_container_width=True, type="primary", key="start_journey_home"):
            st.session_state.page = 'assessment'
            st.rerun()

# ASSESSMENT PAGE
def show_assessment():
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    '>
        <h1 class="main-header">📋 Career Assessment</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress tracking
    if 'step' not in st.session_state:
        st.session_state.step = 1
    
    progress = st.session_state.step / 5
    st.progress(progress)
    st.write(f"**Step {st.session_state.step} of 5**")
    
    # Step 1: Academic Level
    if st.session_state.step == 1:
        st.markdown("## 🎓 Your Academic Stage")
        
        education_level = st.selectbox(
            "Current Education Level",
            ["10th Grade", "12th Grade - Science", "12th Grade - Commerce", 
             "12th Grade - Arts", "Diploma (Engineering)", "Diploma (Other)",
             "Undergraduate (1st/2nd Year)", "Undergraduate (3rd/4th Year)", 
             "Postgraduate"]
        )
        
        stream_details = st.text_input("Specific Stream/Branch (if applicable)", 
                                       placeholder="e.g., Computer Science, Mechanical, Biology")
        
        current_percentage = st.slider("Current Academic Performance (%)", 40, 100, 75)
        
        if st.button("Next →", type="primary", key="step1_next"):
            st.session_state.assessment_data['education_level'] = education_level
            st.session_state.assessment_data['stream_details'] = stream_details
            st.session_state.assessment_data['academic_performance'] = current_percentage
            st.session_state.step = 2
            st.rerun()
    
    # Step 2: Interests & Skills
    elif st.session_state.step == 2:
        st.markdown("## 💡 Interests & Skills")
        
        interests = st.multiselect(
            "Select your interests (Choose 3-5)",
            ["Technology & Programming", "Healthcare & Medicine", "Business & Finance",
             "Art & Design", "Science & Research", "Teaching & Education",
             "Engineering & Manufacturing", "Media & Entertainment", "Law & Politics",
             "Sports & Fitness", "Social Work", "Environment & Sustainability"]
        )
        
        technical_skills = st.multiselect(
            "Technical Skills you have",
            ["Programming (Python, Java, etc.)", "Data Analysis", "Web Development",
             "Mobile App Development", "Digital Marketing", "Video Editing",
             "Graphic Design", "CAD/3D Modeling", "Networking", "Database Management",
             "AI/ML Basics", "Cloud Computing"]
        )
        
        soft_skills = st.multiselect(
            "Soft Skills you possess",
            ["Leadership", "Communication", "Problem Solving", "Teamwork",
             "Critical Thinking", "Creativity", "Time Management", "Adaptability",
             "Empathy", "Analytical Thinking"]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", key="step2_back"):
                st.session_state.step = 1
                st.rerun()
        with col2:
            if st.button("Next →", type="primary", key="step2_next"):
                st.session_state.assessment_data['interests'] = interests
                st.session_state.assessment_data['technical_skills'] = technical_skills
                st.session_state.assessment_data['soft_skills'] = soft_skills
                st.session_state.step = 3
                st.rerun()
    
    # Step 3: Personality & Learning Style
    elif st.session_state.step == 3:
        st.markdown("## 🧠 Personality & Learning Preferences")
        
        personality = st.radio(
            "Which describes you best?",
            ["Analytical & Logical (I love solving problems with data and logic)",
             "Creative & Artistic (I express myself through creativity)",
             "Social & Empathetic (I enjoy helping and connecting with people)",
             "Practical & Hands-on (I learn best by doing things)",
             "Investigative & Curious (I love researching and discovering)"]
        )
        
        learning_style = st.radio(
            "Preferred Learning Style",
            ["Visual (Videos, diagrams, infographics)",
             "Reading/Writing (Books, articles, notes)",
             "Hands-on (Projects, experiments, practice)",
             "Auditory (Lectures, podcasts, discussions)"]
        )
        
        work_environment = st.radio(
            "Ideal Work Environment",
            ["Office/Corporate", "Remote/Freelance", "Field Work", 
             "Laboratory/Research", "Creative Studio", "Healthcare Facility"]
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", key="step3_back"):
                st.session_state.step = 2
                st.rerun()
        with col2:
            if st.button("Next →", type="primary", key="step3_next"):
                st.session_state.assessment_data['personality'] = personality
                st.session_state.assessment_data['learning_style'] = learning_style
                st.session_state.assessment_data['work_environment'] = work_environment
                st.session_state.step = 4
                st.rerun()
    
    # Step 4: Career Goals & Preferences
    elif st.session_state.step == 4:
        st.markdown("## 🎯 Career Goals & Preferences")
        
        career_priority = st.radio(
            "What matters most in your career?",
            ["High Salary & Financial Growth", "Work-Life Balance", 
             "Creative Freedom", "Job Security & Stability",
             "Making Social Impact", "Continuous Learning"]
        )
        
        timeframe = st.selectbox(
            "When do you want to start working?",
            ["Immediate (0-6 months)", "Short-term (6-12 months)",
             "Medium-term (1-2 years)", "Long-term (2-4 years)", "After further studies (4+ years)"]
        )
        
        budget = st.slider("Monthly Budget for Learning (₹)", 0, 50000, 5000, 1000)
        
        time_available = st.slider("Hours per week you can dedicate to learning", 5, 40, 15, 5)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", key="step4_back"):
                st.session_state.step = 3
                st.rerun()
        with col2:
            if st.button("Next →", type="primary", key="step4_next"):
                st.session_state.assessment_data['career_priority'] = career_priority
                st.session_state.assessment_data['timeframe'] = timeframe
                st.session_state.assessment_data['budget'] = budget
                st.session_state.assessment_data['time_available'] = time_available
                st.session_state.step = 5
                st.rerun()
    
    # Step 5: Additional Information
    elif st.session_state.step == 5:
        st.markdown("## ✨ Final Details")
        
        location_preference = st.multiselect(
            "Preferred location for study/work",
            ["Same City", "Within State", "Anywhere in India", "Abroad"]
        )
        
        industry_interests = st.multiselect(
            "Industries you're interested in",
            ["IT & Software", "Healthcare", "Finance & Banking", "E-commerce",
             "Manufacturing", "Education", "Consulting", "Media & Entertainment",
             "Government", "Startups", "Automotive", "Aerospace"]
        )
        
        concerns = st.text_area(
            "Any specific concerns or challenges?",
            placeholder="e.g., Limited budget, need to work part-time, family expectations..."
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("← Back", key="step5_back"):
                st.session_state.step = 4
                st.rerun()
        with col2:
            if st.button("🎯 Get My Recommendations", type="primary", key="step5_submit"):
                st.session_state.assessment_data['location_preference'] = location_preference
                st.session_state.assessment_data['industry_interests'] = industry_interests
                st.session_state.assessment_data['concerns'] = concerns
                
                # Generate results
                with st.spinner("🤖 AI is analyzing your profile..."):
                    import time
                    time.sleep(2)
                    st.session_state.page = 'results'
                    st.session_state.step = 1  # Reset for next time
                    st.rerun()

# RESULTS PAGE
def show_results():
    st.markdown("""
    <div style='
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    '>
        <h1 class="main-header">🎯 Your Personalized Career Plan</h1>
    </div>
    """, unsafe_allow_html=True)
    
    data = st.session_state.assessment_data
    
    # Generate predictions
    career_scores = calculate_weighted_score(data)
    top_careers = predict_career_cluster(data)
    courses = predict_best_paths(data)
    roadmap = generate_personalized_roadmap(data, top_careers[0])
    
    # Overview
    st.markdown("## 📊 Profile Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Education Level", data.get('education_level', 'N/A').split('-')[0])
    with col2:
        st.metric("Academic Score", f"{data.get('academic_performance', 0)}%")
    with col3:
        st.metric("Interests", len(data.get('interests', [])))
    with col4:
        st.metric("Skills", len(data.get('technical_skills', [])) + len(data.get('soft_skills', [])))
    
    st.divider()
    
    # Top Career Recommendations
    st.markdown("## 🚀 Top Career Recommendations")
    
    for i, career in enumerate(top_careers[:5], 1):
        score = career_scores.get(career['name'], 75)
        
        # Create expandable section for each career
        with st.expander(f"**{i}. {career['name']} - Match Score: {score}%**", expanded=(i==1)):
            st.write(f"**Why this fits you:** {career['reason']}")
            st.write(f"**Salary Range:** {career['salary']}")
            st.write(f"**Growth Potential:** {career['growth']}")
            st.write(f"**Required Skills:** {', '.join(career['skills'][:5])}")
            
            # Progress bar for match score
            st.progress(score / 100)
    
    st.divider()
    
    # Course Recommendations
    st.markdown("## 📚 Recommended Courses & Streams")
    
    for i, course in enumerate(courses[:5], 1):
        with st.expander(f"**{i}. {course['name']}**", expanded=(i==1)):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Duration:** {course['duration']}")
            with col2:
                st.write(f"**Cost Range:** {course['cost']}")
            
            st.write(course['description'])
            st.write(f"**Top Colleges:** {', '.join(course['colleges'][:3])}")
    
    st.divider()
    
    # Skill Gap Analysis
    st.markdown("## 🎯 Skill Gap Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Skills You Have")
        current_skills = data.get('technical_skills', []) + data.get('soft_skills', [])
        if current_skills:
            for skill in current_skills:
                st.write(f"✓ {skill}")
        else:
            st.write("No skills listed")
    
    with col2:
        st.markdown("### 📈 Skills to Develop")
        recommended_skills = top_careers[0]['skills']
        skills_to_learn = [s for s in recommended_skills if s not in current_skills]
        if skills_to_learn:
            for skill in skills_to_learn[:8]:
                st.write(f"• {skill}")
        else:
            st.write("You have all required skills!")
    
    st.divider()
    
    # Learning Roadmap
    st.markdown("## 🗺️ Your 6-Month Learning Roadmap")
    st.markdown(f"**Target Career:** {top_careers[0]['name']}")
    st.write("")
    
    for month in roadmap:
        with st.container():
            st.markdown(f"### 📅 {month['month']}")
            st.markdown(f"**Focus:** {month['focus']}")
            
            st.markdown("**Goals:**")
            for goal in month['goals']:
                st.markdown(f"- {goal}")
            
            st.markdown(f"**Resources:** {', '.join(month['resources'])}")
            st.markdown(f"**Time Commitment:** {month['time']}")
            st.markdown("---")
    
    st.divider()
    
    # Action Items
    st.markdown("## ✅ Immediate Action Items")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 This Week")
        st.write("- Research top 3 recommended careers")
        st.write("- Connect with professionals on LinkedIn")
        st.write("- Start with one free online course")
        st.write("- Set up learning schedule")
    
    with col2:
        st.markdown("### 📅 This Month")
        st.write("- Complete at least 2 beginner courses")
        st.write("- Build your first mini-project")
        st.write("- Join relevant communities/forums")
        st.write("- Create LinkedIn profile if not done")
    
    st.divider()
    
    # Download Report
    st.markdown("## 📥 Download Your Report")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Download Full Report (PDF)", use_container_width=True, type="primary", key="download_report"):
            # Generate PDF content
            pdf_content = generate_text_report(data, top_careers, roadmap)
            
            st.download_button(
                label="💾 Click Here to Download",
                data=pdf_content,
                file_name=f"SkillPath_Career_Report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain",
                use_container_width=True,
                key="download_report_btn"
            )
            st.success("✅ Report ready! Click the button above to download.")
        
        if st.button("🔄 Retake Assessment", use_container_width=True, key="retake_assessment"):
            st.session_state.assessment_data = {}
            st.session_state.page = 'assessment'
            st.rerun()

# Helper function for text report generation
def generate_text_report(data, careers, roadmap):
    """Generate a downloadable text report"""
    
    report = f"""
╔═══════════════════════════════════════════════════════════════╗
║           SKILLPATH AI - CAREER RECOMMENDATION REPORT          ║
║                  Generated: {datetime.now().strftime('%B %d, %Y')}                  ║
╚═══════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STUDENT PROFILE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Education Level: {data.get('education_level', 'N/A')}
Academic Performance: {data.get('academic_performance', 0)}%
Interests: {', '.join(data.get('interests', []))}
Technical Skills: {', '.join(data.get('technical_skills', []))}
Soft Skills: {', '.join(data.get('soft_skills', []))}
Personality Type: {data.get('personality', 'N/A')}
Career Priority: {data.get('career_priority', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOP 5 CAREER RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    for i, career in enumerate(careers[:5], 1):
        report += f"""
{i}. {career['name']} - Match Score: {career['score']}%
   
   Why This Fits You:
   {career['reason']}
   
   Salary Range: {career['salary']}
   Growth Potential: {career['growth']}
   
   Required Skills:
   {', '.join(career['skills'][:5])}
   
   {'─' * 60}
"""
    
    report += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6-MONTH LEARNING ROADMAP
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Target Career: {careers[0]['name']}

"""
    
    for month in roadmap:
        report += f"""
📅 {month['month']}
   Focus: {month['focus']}
   Time Commitment: {month['time']}
   
   Goals:
"""
        for goal in month['goals']:
            report += f"   • {goal}\n"
        
        report += f"""
   
   Resources:
   {', '.join(month['resources'])}
   
   {'─' * 60}

"""
    
    report += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
IMMEDIATE ACTION ITEMS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This Week:
• Research top 3 recommended careers
• Connect with professionals on LinkedIn
• Start with one free online course
• Set up learning schedule

This Month:
• Complete at least 2 beginner courses
• Build your first mini-project
• Join relevant communities/forums
• Create LinkedIn profile if not done

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

© SkillPath AI - Empowering Students to Make Better Career Decisions
Generated with ❤️ for your success

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    return report

# Main app logic
if st.session_state.page == 'home':
    show_home()
elif st.session_state.page == 'assessment':
    show_assessment()
elif st.session_state.page == 'results':
    show_results()

# Add floating icon to all pages
add_floating_icon()

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p>🎓 SkillPath AI | Empowering Students to Make Better Career Decisions</p>
    <p> Learn what it takes to face the world </p>
</div>
""", unsafe_allow_html=True)