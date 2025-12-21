"""
Personalized Learning Roadmap Generator
Creates month-by-month learning plans based on career goals
"""

def generate_personalized_roadmap(assessment_data, target_career):
    """
    Generate a 6-month personalized learning roadmap
    """
    
    career_name = target_career['name']
    time_available = assessment_data.get('time_available', 15)
    budget = assessment_data.get('budget', 5000)
    learning_style = assessment_data.get('learning_style', '')
    
    # Get career-specific roadmap template
    roadmap_template = get_roadmap_template(career_name)
    
    # Customize based on user profile
    personalized_roadmap = []
    
    for i, month_template in enumerate(roadmap_template, 1):
        month_plan = {
            'month': f'Month {i}: {month_template["phase"]}',
            'focus': month_template['focus'],
            'goals': month_template['goals'],
            'resources': customize_resources(month_template['resources'], budget, learning_style),
            'time': f'{time_available} hours/week'
        }
        personalized_roadmap.append(month_plan)
    
    return personalized_roadmap


def get_roadmap_template(career_name):
    """
    Get roadmap template based on career
    """
    
    roadmaps = {
        'Software Engineer': [
            {
                'phase': 'Foundation',
                'focus': 'Programming Fundamentals',
                'goals': [
                    'Learn Python or Java basics',
                    'Understand data structures (arrays, lists, dictionaries)',
                    'Practice 20+ coding problems',
                    'Build a simple calculator app'
                ],
                'resources': ['Coursera Python for Everybody', 'LeetCode Easy Problems', 'YouTube CS Dojo']
            },
            {
                'phase': 'Intermediate Skills',
                'focus': 'Object-Oriented Programming & Algorithms',
                'goals': [
                    'Master OOP concepts',
                    'Learn sorting and searching algorithms',
                    'Solve 50+ medium-level problems',
                    'Build a to-do list web app'
                ],
                'resources': ['Udemy Java Masterclass', 'HackerRank', 'FreeCodeCamp']
            },
            {
                'phase': 'Web Development',
                'focus': 'Frontend & Backend Basics',
                'goals': [
                    'Learn HTML, CSS, JavaScript',
                    'Understand React or Angular basics',
                    'Build REST APIs with Node.js/Flask',
                    'Create a personal portfolio website'
                ],
                'resources': ['The Odin Project', 'MDN Web Docs', 'Scrimba React Course']
            },
            {
                'phase': 'Databases & Backend',
                'focus': 'Database Design & Server-Side Development',
                'goals': [
                    'Learn SQL and database design',
                    'Understand NoSQL (MongoDB)',
                    'Build full-stack CRUD application',
                    'Deploy app on Heroku/Vercel'
                ],
                'resources': ['MongoDB University', 'PostgreSQL Tutorial', 'DigitalOcean Guides']
            },
            {
                'phase': 'Projects & DSA',
                'focus': 'Real-World Projects & Problem Solving',
                'goals': [
                    'Build 2-3 portfolio projects',
                    'Practice advanced DSA problems',
                    'Contribute to open-source',
                    'Create GitHub profile'
                ],
                'resources': ['GitHub', 'LeetCode Hard', 'HackerRank']
            },
            {
                'phase': 'Job Preparation',
                'focus': 'Interview Prep & Networking',
                'goals': [
                    'Solve interview-style problems daily',
                    'Build strong LinkedIn profile',
                    'Apply to 20+ companies',
                    'Practice mock interviews'
                ],
                'resources': ['Pramp', 'InterviewBit', 'LinkedIn Learning']
            }
        ],
        'Data Scientist': [
            {
                'phase': 'Foundation',
                'focus': 'Python & Statistics Basics',
                'goals': [
                    'Learn Python programming',
                    'Understand descriptive statistics',
                    'Learn pandas and numpy',
                    'Analyze your first dataset'
                ],
                'resources': ['DataCamp Python', 'Khan Academy Statistics', 'Kaggle Learn']
            },
            {
                'phase': 'Data Analysis',
                'focus': 'Data Manipulation & Visualization',
                'goals': [
                    'Master pandas for data cleaning',
                    'Learn matplotlib and seaborn',
                    'Complete 3 data analysis projects',
                    'Create data dashboards'
                ],
                'resources': ['Kaggle Datasets', 'Plotly Dash', 'Tableau Public']
            },
            {
                'phase': 'Machine Learning',
                'focus': 'ML Fundamentals',
                'goals': [
                    'Understand supervised learning',
                    'Learn regression and classification',
                    'Implement ML algorithms from scratch',
                    'Build prediction models'
                ],
                'resources': ['Andrew Ng ML Course', 'Scikit-learn Docs', 'Kaggle Competitions']
            },
            {
                'phase': 'Advanced ML',
                'focus': 'Deep Learning & Neural Networks',
                'goals': [
                    'Learn TensorFlow/PyTorch',
                    'Understand neural networks',
                    'Build image classification model',
                    'Work with NLP basics'
                ],
                'resources': ['Fast.ai', 'DeepLearning.AI', 'PyTorch Tutorials']
            },
            {
                'phase': 'Projects & Portfolio',
                'focus': 'Real-World DS Projects',
                'goals': [
                    'Complete 3 end-to-end projects',
                    'Participate in Kaggle competitions',
                    'Create data science blog',
                    'Build project portfolio'
                ],
                'resources': ['Kaggle', 'Medium', 'GitHub Pages']
            },
            {
                'phase': 'Job Readiness',
                'focus': 'Interview Prep & Networking',
                'goals': [
                    'Practice SQL and Python interviews',
                    'Learn A/B testing concepts',
                    'Build strong GitHub profile',
                    'Network with data professionals'
                ],
                'resources': ['StrataScratch', 'DataCamp Interview Prep', 'LinkedIn']
            }
        ],
        'Digital Marketing Manager': [
            {
                'phase': 'Marketing Fundamentals',
                'focus': 'Digital Marketing Basics',
                'goals': [
                    'Understand marketing concepts',
                    'Learn SEO fundamentals',
                    'Study social media marketing',
                    'Create first campaign plan'
                ],
                'resources': ['Google Digital Garage', 'HubSpot Academy', 'Moz SEO Guide']
            },
            {
                'phase': 'Content & SEO',
                'focus': 'Content Marketing & Search Optimization',
                'goals': [
                    'Master keyword research',
                    'Write SEO-optimized content',
                    'Learn Google Analytics',
                    'Build content calendar'
                ],
                'resources': ['Ahrefs Blog', 'SEMrush Academy', 'Google Analytics Academy']
            },
            {
                'phase': 'Paid Advertising',
                'focus': 'Google Ads & Facebook Ads',
                'goals': [
                    'Get Google Ads certified',
                    'Learn Facebook Ads Manager',
                    'Create ad campaigns',
                    'Understand PPC strategy'
                ],
                'resources': ['Google Skillshop', 'Facebook Blueprint', 'WordStream Blog']
            },
            {
                'phase': 'Social Media',
                'focus': 'Social Media Strategy',
                'goals': [
                    'Master Instagram & LinkedIn marketing',
                    'Learn influencer marketing',
                    'Create viral content',
                    'Grow social media following'
                ],
                'resources': ['Hootsuite Academy', 'Buffer Blog', 'Later']
            },
            {
                'phase': 'Analytics & Tools',
                'focus': 'Marketing Analytics & Automation',
                'goals': [
                    'Master Google Analytics 4',
                    'Learn marketing automation',
                    'Use email marketing tools',
                    'Create analytics reports'
                ],
                'resources': ['Mailchimp Academy', 'Google Analytics', 'HubSpot CRM']
            },
            {
                'phase': 'Portfolio & Jobs',
                'focus': 'Build Portfolio & Get Hired',
                'goals': [
                    'Create marketing portfolio',
                    'Run personal brand campaigns',
                    'Network with marketers',
                    'Apply to marketing roles'
                ],
                'resources': ['Behance', 'LinkedIn', 'AngelList']
            }
        ],
        'UX/UI Designer': [
            {
                'phase': 'Design Fundamentals',
                'focus': 'Design Principles & Tools',
                'goals': [
                    'Learn design principles',
                    'Master Figma basics',
                    'Understand color theory',
                    'Create first design mockups'
                ],
                'resources': ['Figma YouTube', 'Coursera Design Courses', 'Dribbble']
            },
            {
                'phase': 'UX Research',
                'focus': 'User Research & Psychology',
                'goals': [
                    'Learn user research methods',
                    'Conduct user interviews',
                    'Create user personas',
                    'Build user journey maps'
                ],
                'resources': ['Nielsen Norman Group', 'UX Collective', 'Interaction Design Foundation']
            },
            {
                'phase': 'UI Design',
                'focus': 'Interface Design & Prototyping',
                'goals': [
                    'Master advanced Figma',
                    'Learn design systems',
                    'Create high-fidelity prototypes',
                    'Study mobile app design'
                ],
                'resources': ['Figma Community', 'Adobe XD Tutorials', 'Material Design']
            },
            {
                'phase': 'Interaction Design',
                'focus': 'Animations & Micro-interactions',
                'goals': [
                    'Learn Principle or Framer',
                    'Create animated prototypes',
                    'Understand usability testing',
                    'Build interactive designs'
                ],
                'resources': ['Framer Learn', 'LottieFiles', 'ProtoPie']
            },
            {
                'phase': 'Portfolio Projects',
                'focus': 'Real-World Design Projects',
                'goals': [
                    'Complete 3-5 case studies',
                    'Redesign existing apps/websites',
                    'Participate in design challenges',
                    'Build portfolio website'
                ],
                'resources': ['Behance', 'Daily UI Challenge', 'Webflow']
            },
            {
                'phase': 'Job Preparation',
                'focus': 'Portfolio & Interviews',
                'goals': [
                    'Perfect portfolio presentation',
                    'Practice design interviews',
                    'Network with designers',
                    'Apply to design roles'
                ],
                'resources': ['ADPList', 'Behance', 'LinkedIn', 'Cofolios']
            }
        ]
    }
    
    # Default roadmap for careers not in template
    default_roadmap = [
        {
            'phase': 'Foundation',
            'focus': 'Learn Fundamentals',
            'goals': [
                'Research the field thoroughly',
                'Identify key skills needed',
                'Start with beginner courses',
                'Connect with professionals'
            ],
            'resources': ['Coursera', 'edX', 'LinkedIn Learning', 'YouTube']
        },
        {
            'phase': 'Skill Building',
            'focus': 'Develop Core Competencies',
            'goals': [
                'Complete intermediate courses',
                'Practice hands-on projects',
                'Read industry publications',
                'Join relevant communities'
            ],
            'resources': ['Udemy', 'Skillshare', 'Industry Forums', 'Reddit']
        },
        {
            'phase': 'Practical Experience',
            'focus': 'Real-World Application',
            'goals': [
                'Work on personal projects',
                'Seek internships or volunteering',
                'Build portfolio of work',
                'Get feedback from mentors'
            ],
            'resources': ['Internshala', 'AngelList', 'LinkedIn', 'GitHub']
        },
        {
            'phase': 'Advanced Learning',
            'focus': 'Specialization',
            'goals': [
                'Take advanced courses',
                'Get certifications',
                'Attend workshops/webinars',
                'Stay updated with trends'
            ],
            'resources': ['Professional Certifications', 'Webinars', 'Industry Events']
        },
        {
            'phase': 'Portfolio Development',
            'focus': 'Showcase Your Work',
            'goals': [
                'Create professional portfolio',
                'Document all projects',
                'Get testimonials',
                'Build personal brand'
            ],
            'resources': ['Personal Website', 'LinkedIn', 'Medium', 'GitHub']
        },
        {
            'phase': 'Job Hunting',
            'focus': 'Career Launch',
            'goals': [
                'Polish resume and portfolio',
                'Network actively',
                'Apply strategically',
                'Prepare for interviews'
            ],
            'resources': ['LinkedIn', 'Naukri', 'Glassdoor', 'Mock Interviews']
        }
    ]
    
    return roadmaps.get(career_name, default_roadmap)


def customize_resources(resources, budget, learning_style):
    """
    Customize resources based on budget and learning style
    """
    
    customized = []
    
    for resource in resources:
        # Add budget-appropriate alternatives
        if budget < 5000:
            if 'Coursera' in resource:
                customized.append(f"{resource} (Audit for free)")
            elif 'Udemy' in resource:
                customized.append(f"{resource} (Wait for sales)")
            else:
                customized.append(resource)
        else:
            customized.append(resource)
    
    # Add style-specific resources
    if 'Visual' in learning_style:
        customized.append('YouTube video tutorials')
    elif 'Reading' in learning_style:
        customized.append('eBooks and documentation')
    elif 'Hands-on' in learning_style:
        customized.append('Interactive coding platforms')
    
    return customized[:5]  # Limit to top 5 resources