"""
Scoring and Career Prediction Module
Implements weighted scoring and rule-based career matching
"""

def calculate_weighted_score(assessment_data):
    """
    Calculate weighted scores for different careers based on assessment
    
    Weights:
    - Interest Score: 40%
    - Personality Score: 20%
    - Skills Score: 20%
    - Academic Fit: 20%
    """
    
    scores = {}
    
    # Define career database with required attributes
    career_db = get_career_database()
    
    interests = assessment_data.get('interests', [])
    technical_skills = assessment_data.get('technical_skills', [])
    soft_skills = assessment_data.get('soft_skills', [])
    personality = assessment_data.get('personality', '')
    education = assessment_data.get('education_level', '')
    
    for career in career_db:
        interest_score = 0
        skill_score = 0
        personality_score = 0
        academic_score = 0
        
        # Interest matching (40%)
        matching_interests = set(interests) & set(career['related_interests'])
        if len(career['related_interests']) > 0:
            interest_score = (len(matching_interests) / len(career['related_interests'])) * 40
        
        # Skills matching (20%)
        all_skills = technical_skills + soft_skills
        matching_skills = set(all_skills) & set(career['required_skills'])
        if len(career['required_skills']) > 0:
            skill_score = (len(matching_skills) / len(career['required_skills'])) * 20
        
        # Personality matching (20%)
        if personality:
            personality_type = personality.split('(')[0].strip()
            if personality_type in career['personality_fit']:
                personality_score = 20
            elif len(career['personality_fit']) > 0:
                personality_score = 10
        
        # Academic fit (20%)
        if education:
            if any(edu in education for edu in career['education_requirements']):
                academic_score = 20
            else:
                academic_score = 10
        
        # Calculate total weighted score
        total_score = interest_score + skill_score + personality_score + academic_score
        scores[career['name']] = min(int(total_score), 100)
    
    return scores


def predict_career_cluster(assessment_data):
    """
    Predict top career clusters using rule-based logic + ML scoring
    """
    
    scores = calculate_weighted_score(assessment_data)
    career_db = get_career_database()
    
    # Sort careers by score
    sorted_careers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    # Get top careers with details
    top_careers = []
    for career_name, score in sorted_careers[:10]:
        career_info = next((c for c in career_db if c['name'] == career_name), None)
        if career_info:
            top_careers.append({
                'name': career_name,
                'score': score,
                'reason': generate_reason(assessment_data, career_info),
                'salary': career_info['salary_range'],
                'growth': career_info['growth_potential'],
                'skills': career_info['required_skills']
            })
    
    return top_careers


def generate_reason(assessment_data, career_info):
    """
    Generate personalized reason why this career fits
    """
    
    interests = assessment_data.get('interests', [])
    skills = assessment_data.get('technical_skills', []) + assessment_data.get('soft_skills', [])
    
    matching_interests = set(interests) & set(career_info['related_interests'])
    matching_skills = set(skills) & set(career_info['required_skills'])
    
    reason_parts = []
    
    if matching_interests:
        reason_parts.append(f"Your interests in {', '.join(list(matching_interests)[:2])} align perfectly")
    
    if matching_skills:
        reason_parts.append(f"you already have {len(matching_skills)} relevant skills")
    
    if assessment_data.get('career_priority'):
        priority = assessment_data['career_priority']
        if 'High Salary' in priority and 'High' in career_info['salary_range']:
            reason_parts.append("offers excellent financial growth")
        elif 'Work-Life Balance' in priority:
            reason_parts.append("provides good work-life balance")
        elif 'Social Impact' in priority and 'Impact' in career_info.get('benefits', ''):
            reason_parts.append("creates meaningful social impact")
    
    return '. '.join(reason_parts) if reason_parts else "This career matches your overall profile well"


def get_career_database():
    """
    Career database with comprehensive information
    """
    
    careers = [
        {
            'name': 'Software Engineer',
            'related_interests': ['Technology & Programming', 'Science & Research'],
            'required_skills': ['Programming (Python, Java, etc.)', 'Problem Solving', 
                              'Analytical Thinking', 'Teamwork'],
            'personality_fit': ['Analytical & Logical', 'Investigative & Curious'],
            'education_requirements': ['12th Grade - Science', 'Undergraduate', 'Diploma (Engineering)'],
            'salary_range': '₹4-25 LPA (Entry to Senior)',
            'growth_potential': 'Excellent - High demand globally',
        },
        {
            'name': 'Data Scientist',
            'related_interests': ['Technology & Programming', 'Science & Research'],
            'required_skills': ['Data Analysis', 'Programming (Python, Java, etc.)', 
                              'Analytical Thinking', 'Problem Solving'],
            'personality_fit': ['Analytical & Logical', 'Investigative & Curious'],
            'education_requirements': ['Undergraduate', 'Postgraduate'],
            'salary_range': '₹6-30 LPA',
            'growth_potential': 'Excellent - AI/ML boom',
        },
        {
            'name': 'Doctor (MBBS)',
            'related_interests': ['Healthcare & Medicine', 'Science & Research', 'Social Work'],
            'required_skills': ['Critical Thinking', 'Empathy', 'Communication', 'Problem Solving'],
            'personality_fit': ['Social & Empathetic', 'Investigative & Curious'],
            'education_requirements': ['12th Grade - Science'],
            'salary_range': '₹8-50 LPA',
            'growth_potential': 'Very High - Always in demand',
        },
        {
            'name': 'Chartered Accountant (CA)',
            'related_interests': ['Business & Finance'],
            'required_skills': ['Analytical Thinking', 'Time Management', 'Critical Thinking'],
            'personality_fit': ['Analytical & Logical'],
            'education_requirements': ['12th Grade - Commerce', 'Undergraduate'],
            'salary_range': '₹7-40 LPA',
            'growth_potential': 'Very High - Prestigious career',
        },
        {
            'name': 'UX/UI Designer',
            'related_interests': ['Art & Design', 'Technology & Programming'],
            'required_skills': ['Graphic Design', 'Creativity', 'Problem Solving', 'Communication'],
            'personality_fit': ['Creative & Artistic', 'Analytical & Logical'],
            'education_requirements': ['12th Grade', 'Undergraduate', 'Diploma'],
            'salary_range': '₹3-20 LPA',
            'growth_potential': 'High - Growing digital economy',
        },
        {
            'name': 'Digital Marketing Manager',
            'related_interests': ['Business & Finance', 'Media & Entertainment', 'Technology & Programming'],
            'required_skills': ['Digital Marketing', 'Communication', 'Creativity', 'Analytical Thinking'],
            'personality_fit': ['Creative & Artistic', 'Social & Empathetic'],
            'education_requirements': ['12th Grade', 'Undergraduate'],
            'salary_range': '₹4-18 LPA',
            'growth_potential': 'Very High - Digital transformation',
        },
        {
            'name': 'Mechanical Engineer',
            'related_interests': ['Engineering & Manufacturing', 'Technology & Programming'],
            'required_skills': ['CAD/3D Modeling', 'Problem Solving', 'Analytical Thinking'],
            'personality_fit': ['Practical & Hands-on', 'Analytical & Logical'],
            'education_requirements': ['12th Grade - Science', 'Diploma (Engineering)', 'Undergraduate'],
            'salary_range': '₹3-15 LPA',
            'growth_potential': 'Good - Manufacturing sector',
        },
        {
            'name': 'Content Creator/YouTuber',
            'related_interests': ['Media & Entertainment', 'Art & Design'],
            'required_skills': ['Video Editing', 'Creativity', 'Communication', 'Digital Marketing'],
            'personality_fit': ['Creative & Artistic', 'Social & Empathetic'],
            'education_requirements': ['10th Grade', '12th Grade'],
            'salary_range': '₹2-50 LPA (highly variable)',
            'growth_potential': 'High - Creator economy boom',
        },
        {
            'name': 'Psychologist',
            'related_interests': ['Healthcare & Medicine', 'Social Work', 'Science & Research'],
            'required_skills': ['Empathy', 'Communication', 'Analytical Thinking', 'Problem Solving'],
            'personality_fit': ['Social & Empathetic', 'Investigative & Curious'],
            'education_requirements': ['12th Grade', 'Undergraduate', 'Postgraduate'],
            'salary_range': '₹3-12 LPA',
            'growth_potential': 'Good - Mental health awareness rising',
        },
        {
            'name': 'Business Analyst',
            'related_interests': ['Business & Finance', 'Technology & Programming'],
            'required_skills': ['Data Analysis', 'Analytical Thinking', 'Communication', 'Problem Solving'],
            'personality_fit': ['Analytical & Logical', 'Social & Empathetic'],
            'education_requirements': ['Undergraduate', 'Postgraduate'],
            'salary_range': '₹5-20 LPA',
            'growth_potential': 'Very High - Critical role',
        },
        {
            'name': 'Civil Engineer',
            'related_interests': ['Engineering & Manufacturing', 'Environment & Sustainability'],
            'required_skills': ['CAD/3D Modeling', 'Problem Solving', 'Analytical Thinking'],
            'personality_fit': ['Practical & Hands-on', 'Analytical & Logical'],
            'education_requirements': ['12th Grade - Science', 'Diploma (Engineering)', 'Undergraduate'],
            'salary_range': '₹3-12 LPA',
            'growth_potential': 'Good - Infrastructure development',
        },
        {
            'name': 'Investment Banker',
            'related_interests': ['Business & Finance'],
            'required_skills': ['Analytical Thinking', 'Communication', 'Critical Thinking', 'Problem Solving'],
            'personality_fit': ['Analytical & Logical', 'Social & Empathetic'],
            'education_requirements': ['Undergraduate', 'Postgraduate'],
            'salary_range': '₹8-50 LPA',
            'growth_potential': 'Excellent - High rewards',
        },
        {
            'name': 'Teacher/Professor',
            'related_interests': ['Teaching & Education', 'Social Work'],
            'required_skills': ['Communication', 'Empathy', 'Creativity', 'Leadership'],
            'personality_fit': ['Social & Empathetic', 'Investigative & Curious'],
            'education_requirements': ['Undergraduate', 'Postgraduate'],
            'salary_range': '₹3-15 LPA',
            'growth_potential': 'Stable - Respectable profession',
        },
        {
            'name': 'Product Manager',
            'related_interests': ['Technology & Programming', 'Business & Finance'],
            'required_skills': ['Leadership', 'Communication', 'Analytical Thinking', 'Problem Solving'],
            'personality_fit': ['Analytical & Logical', 'Social & Empathetic'],
            'education_requirements': ['Undergraduate', 'Postgraduate'],
            'salary_range': '₹10-40 LPA',
            'growth_potential': 'Excellent - Strategic role',
        },
        {
            'name': 'Architect',
            'related_interests': ['Art & Design', 'Engineering & Manufacturing'],
            'required_skills': ['CAD/3D Modeling', 'Creativity', 'Problem Solving', 'Analytical Thinking'],
            'personality_fit': ['Creative & Artistic', 'Practical & Hands-on'],
            'education_requirements': ['12th Grade', 'Undergraduate'],
            'salary_range': '₹3-20 LPA',
            'growth_potential': 'Good - Real estate growth',
        },
    ]
    
    return careers