"""
Machine Learning Course Predictor
Uses rule-based logic to predict best courses and streams
"""

def predict_best_paths(assessment_data):
    """
    Predict best educational paths based on current stage and interests
    """
    
    education_level = assessment_data.get('education_level', '')
    interests = assessment_data.get('interests', [])
    technical_skills = assessment_data.get('technical_skills', [])
    budget = assessment_data.get('budget', 5000)
    
    courses = []
    
    # After 10th Grade
    if '10th' in education_level:
        courses = get_post_10th_courses(interests)
    
    # After 12th - Science
    elif '12th' in education_level and 'Science' in education_level:
        courses = get_post_12th_science_courses(interests, technical_skills)
    
    # After 12th - Commerce
    elif '12th' in education_level and 'Commerce' in education_level:
        courses = get_post_12th_commerce_courses(interests)
    
    # After 12th - Arts
    elif '12th' in education_level and 'Arts' in education_level:
        courses = get_post_12th_arts_courses(interests)
    
    # Diploma holders
    elif 'Diploma' in education_level:
        courses = get_post_diploma_courses(interests, technical_skills)
    
    # Undergraduate students
    elif 'Undergraduate' in education_level:
        courses = get_undergraduate_specializations(interests, technical_skills)
    
    # Postgraduate
    elif 'Postgraduate' in education_level:
        courses = get_postgraduate_courses(interests, technical_skills)
    
    # Filter by budget
    affordable_courses = [c for c in courses if is_affordable(c, budget)]
    
    return affordable_courses if affordable_courses else courses


def get_post_10th_courses(interests):
    """Courses after 10th grade"""
    
    courses = []
    
    if any(x in interests for x in ['Technology & Programming', 'Science & Research', 'Engineering & Manufacturing']):
        courses.append({
            'name': 'Science Stream (PCM - Physics, Chemistry, Maths)',
            'duration': '2 years',
            'cost': '₹50,000 - 2,00,000',
            'description': 'Opens doors to Engineering, Architecture, Computer Science',
            'colleges': ['State Board Schools', 'CBSE Schools', 'ICSE Schools']
        })
        courses.append({
            'name': 'Polytechnic Diploma (Engineering)',
            'duration': '3 years',
            'cost': '₹30,000 - 1,50,000',
            'description': 'Direct entry to engineering jobs or lateral entry to BE',
            'colleges': ['Government Polytechnics', 'Private Polytechnics']
        })
    
    if any(x in interests for x in ['Healthcare & Medicine', 'Science & Research']):
        courses.append({
            'name': 'Science Stream (PCB - Physics, Chemistry, Biology)',
            'duration': '2 years',
            'cost': '₹50,000 - 2,00,000',
            'description': 'Path to MBBS, BDS, Nursing, Pharmacy',
            'colleges': ['CBSE Schools', 'State Boards', 'ICSE Schools']
        })
    
    if any(x in interests for x in ['Business & Finance']):
        courses.append({
            'name': 'Commerce Stream',
            'duration': '2 years',
            'cost': '₹40,000 - 1,50,000',
            'description': 'Foundation for CA, CS, B.Com, BBA',
            'colleges': ['Commerce Colleges', 'Private Schools']
        })
    
    if any(x in interests for x in ['Art & Design', 'Media & Entertainment']):
        courses.append({
            'name': 'Arts/Humanities Stream',
            'duration': '2 years',
            'cost': '₹30,000 - 1,00,000',
            'description': 'Psychology, Design, Mass Communication, Literature',
            'colleges': ['Arts Colleges', 'Schools with Arts']
        })
    
    return courses


def get_post_12th_science_courses(interests, skills):
    """Courses after 12th Science"""
    
    courses = []
    
    if any(x in interests for x in ['Technology & Programming', 'Engineering & Manufacturing']):
        courses.append({
            'name': 'B.Tech/BE in Computer Science',
            'duration': '4 years',
            'cost': '₹4,00,000 - 20,00,000',
            'description': 'Software Development, AI/ML, Data Science careers',
            'colleges': ['IITs', 'NITs', 'BITS Pilani', 'VIT', 'SRM']
        })
        courses.append({
            'name': 'B.Tech in Electronics & Communication',
            'duration': '4 years',
            'cost': '₹4,00,000 - 18,00,000',
            'description': 'Telecom, IoT, Embedded Systems',
            'colleges': ['NITs', 'IITs', 'Anna University']
        })
    
    if 'Healthcare & Medicine' in interests:
        courses.append({
            'name': 'MBBS (Bachelor of Medicine, Bachelor of Surgery)',
            'duration': '5.5 years',
            'cost': '₹5,00,000 - 1,00,00,000',
            'description': 'Become a doctor, high prestige career',
            'colleges': ['AIIMS', 'JIPMER', 'Government Medical Colleges']
        })
        courses.append({
            'name': 'B.Pharmacy',
            'duration': '4 years',
            'cost': '₹2,00,000 - 10,00,000',
            'description': 'Pharmaceutical industry, drug research',
            'colleges': ['BITS Pilani', 'ICT Mumbai', 'JSS Mysore']
        })
    
    courses.append({
        'name': 'BSc in Data Science',
        'duration': '3 years',
        'cost': '₹2,00,000 - 8,00,000',
        'description': 'Analytics, AI/ML, Data Engineering',
        'colleges': ['Christ University', 'Symbiosis', 'Fergusson']
    })
    
    return courses


def get_post_12th_commerce_courses(interests):
    """Courses after 12th Commerce"""
    
    return [
        {
            'name': 'Chartered Accountancy (CA)',
            'duration': '4-5 years',
            'cost': '₹1,50,000 - 3,00,000',
            'description': 'Most prestigious accounting qualification',
            'colleges': ['ICAI Centers nationwide']
        },
        {
            'name': 'B.Com (Honors)',
            'duration': '3 years',
            'cost': '₹1,00,000 - 5,00,000',
            'description': 'Foundation for finance careers',
            'colleges': ['Delhi University', 'Mumbai University', 'Bangalore University']
        },
        {
            'name': 'BBA (Bachelor of Business Administration)',
            'duration': '3 years',
            'cost': '₹3,00,000 - 15,00,000',
            'description': 'Management, Marketing, HR careers',
            'colleges': ['Christ University', 'NMIMS', 'Symbiosis']
        },
        {
            'name': 'Company Secretary (CS)',
            'duration': '3-4 years',
            'cost': '₹1,00,000 - 2,00,000',
            'description': 'Corporate legal compliance specialist',
            'colleges': ['ICSI Centers']
        },
        {
            'name': 'CMA (Cost & Management Accountant)',
            'duration': '3-4 years',
            'cost': '₹1,20,000 - 2,50,000',
            'description': 'Cost accounting and management',
            'colleges': ['ICMAI Centers']
        }
    ]


def get_post_12th_arts_courses(interests):
    """Courses after 12th Arts"""
    
    courses = []
    
    if 'Art & Design' in interests:
        courses.append({
            'name': 'Bachelor of Design (B.Des)',
            'duration': '4 years',
            'cost': '₹4,00,000 - 16,00,000',
            'description': 'Product, Fashion, Graphic Design',
            'colleges': ['NID', 'NIFT', 'Pearl Academy']
        })
    
    if 'Media & Entertainment' in interests:
        courses.append({
            'name': 'Bachelor of Mass Communication',
            'duration': '3 years',
            'cost': '₹2,00,000 - 8,00,000',
            'description': 'Journalism, PR, Content Creation',
            'colleges': ['Xavier\'s Mumbai', 'Jamia', 'Symbiosis']
        })
    
    if 'Law & Politics' in interests:
        courses.append({
            'name': 'BA LLB (Integrated Law)',
            'duration': '5 years',
            'cost': '₹5,00,000 - 20,00,000',
            'description': 'Become a lawyer or legal advisor',
            'colleges': ['NLSIU Bangalore', 'NALSAR', 'NLUs']
        })
    
    courses.append({
        'name': 'BA in Psychology',
        'duration': '3 years',
        'cost': '₹1,50,000 - 6,00,000',
        'description': 'Counseling, HR, Clinical Psychology',
        'colleges': ['Delhi University', 'Christ University', 'Fergusson']
    })
    
    return courses


def get_post_diploma_courses(interests, skills):
    """Courses for diploma holders"""
    
    return [
        {
            'name': 'BE/B.Tech (Lateral Entry)',
            'duration': '3 years',
            'cost': '₹3,00,000 - 12,00,000',
            'description': 'Direct admission to 2nd year engineering',
            'colleges': ['VIT', 'Manipal', 'BITS Pilani', 'State Universities']
        },
        {
            'name': 'Specialized Certification Programs',
            'duration': '6-12 months',
            'cost': '₹50,000 - 3,00,000',
            'description': 'Industry-specific certifications (PLC, Automation, etc.)',
            'colleges': ['NIELIT', 'NSDC', 'Industry Training Centers']
        },
        {
            'name': 'Higher Diploma in Specialized Field',
            'duration': '1-2 years',
            'cost': '₹1,00,000 - 4,00,000',
            'description': 'Advanced technical skills',
            'colleges': ['Polytechnics', 'Technical Institutes']
        }
    ]


def get_undergraduate_specializations(interests, skills):
    """Specializations for current undergrad students"""
    
    courses = []
    
    if any(x in skills for x in ['Programming (Python, Java, etc.)', 'Data Analysis', 'AI/ML Basics']):
        courses.append({
            'name': 'AI & Machine Learning Specialization',
            'duration': '6-12 months',
            'cost': '₹30,000 - 2,00,000',
            'description': 'Deep Learning, Neural Networks, Computer Vision',
            'colleges': ['Coursera', 'edX', 'Great Learning', 'upGrad']
        })
        courses.append({
            'name': 'Full Stack Web Development',
            'duration': '4-8 months',
            'cost': '₹20,000 - 1,50,000',
            'description': 'MERN/MEAN Stack, DevOps',
            'colleges': ['Masai School', 'Coding Ninjas', 'Scaler Academy']
        })
    
    if 'Cloud Computing' in skills or 'Technology & Programming' in interests:
        courses.append({
            'name': 'Cloud Computing Certification (AWS/Azure/GCP)',
            'duration': '3-6 months',
            'cost': '₹15,000 - 1,00,000',
            'description': 'Cloud Architecture, DevOps',
            'colleges': ['AWS Training', 'Microsoft Learn', 'Google Cloud Training']
        })
    
    if 'Digital Marketing' in skills:
        courses.append({
            'name': 'Digital Marketing Professional',
            'duration': '3-6 months',
            'cost': '₹25,000 - 1,50,000',
            'description': 'SEO, SEM, Social Media Marketing',
            'colleges': ['Google Digital Garage', 'HubSpot', 'UpGrad']
        })
    
    return courses


def get_postgraduate_courses(interests, skills):
    """Postgraduate options"""
    
    return [
        {
            'name': 'MBA (Master of Business Administration)',
            'duration': '2 years',
            'cost': '₹10,00,000 - 50,00,000',
            'description': 'Leadership, Strategy, Consulting',
            'colleges': ['IIMs', 'ISB', 'FMS Delhi', 'XLRI']
        },
        {
            'name': 'M.Tech in Specialization',
            'duration': '2 years',
            'cost': '₹2,00,000 - 10,00,000',
            'description': 'Advanced technical specialization',
            'colleges': ['IITs', 'NITs', 'IISc']
        },
        {
            'name': 'MS in Data Science',
            'duration': '2 years',
            'cost': '₹3,00,000 - 15,00,000',
            'description': 'Advanced analytics, ML research',
            'colleges': ['IITs', 'IIIT', 'International Universities']
        }
    ]


def is_affordable(course, budget):
    """Check if course is affordable based on monthly budget"""
    
    cost_str = course['cost']
    # Extract first number from cost string
    import re
    numbers = re.findall(r'[\d,]+', cost_str.replace(',', ''))
    if numbers:
        min_cost = int(numbers[0])
        # Assume 12-month payment plan
        monthly_cost = min_cost / 12
        return monthly_cost <= budget
    return True


def load_model():
    """Placeholder for ML model loading"""
    # In production, you would load a trained sklearn model here
    return None