# 🧠 MindWell – AI-Powered Mental Health Wellness Platform

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Flask](https://img.shields.io/badge/Framework-Flask-green)
![HTML](https://img.shields.io/badge/Frontend-HTML%2FCSS%2FJS-orange)
![Database](https://img.shields.io/badge/Database-SQLite-lightgrey)
![ML](https://img.shields.io/badge/AI-Machine%20Learning-red)
![Status](https://img.shields.io/badge/Status-Active-success)

---
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-green.svg)](https://flask.palletsprojects.com/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

> **MindWell-AI** is a comprehensive mental health platform that combines AI-powered emotional support, mood tracking, journaling, and self-assessment tools to help users monitor, analyze, and improve their mental well-being.

## 🌟 Live Demo

[![Live Demo](https://img.shields.io/badge/demo-live-green.svg)](https://your-demo-url.com)


## 📌 Project Description

**MindWell** is an AI-powered web-based Mental Health Wellness Platform designed to help users monitor, analyze, and improve their mental well-being. The platform provides an intelligent and interactive environment where users can track moods, write journals, and receive AI-based mental wellness recommendations.

The system uses **Flask (Python)** for backend development, **HTML, CSS, JavaScript** for frontend, and integrates a **Machine Learning model** for mood prediction.

---

## 🎯 Objective

The main objectives of MindWell are:

- Provide a digital mental health self-monitoring platform
- Track user mood patterns over time
- Predict user mood using Machine Learning
- Encourage journaling for emotional awareness
- Provide personalized mental wellness recommendations


## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)
- [Disclaimer](#-disclaimer)

---

## ✨ Features

### 🤖 AI Mental Health Chatbot
- **Real-time emotion detection** - Identifies 7+ emotions (happy, sad, anxious, stressed, angry, lonely, neutral)
- **Intelligent conversation memory** - Remembers context across 20+ messages
- **Crisis detection & support** - Identifies crisis keywords and provides emergency resources
- **Evidence-based coping strategies** - Suggests personalized techniques based on emotional state
- **Resource recommendations** - Curated articles, videos, and mental health apps

### 📊 Mood Tracking & Analytics
- **Daily mood logging** - Record emotions with intensity levels
- **Visual mood dashboard** - Interactive charts showing emotional patterns
- **Trend analysis** - Detects improving, stable, or declining mood patterns
- **Personalized insights** - AI-generated recommendations based on mood history

### 📝 Private Journaling
- **Secure personal entries** - Private space for thoughts and reflections
- **AI-generated prompts** - Guided journaling based on current emotional state
- **Search & filter** - Find entries by date, mood, or keywords
- **Export functionality** - Download journal entries for personal records

### 📋 Self-Assessment Tools
- **Depression screening** (PHQ-9)
- **Anxiety assessment** (GAD-7)
- **Well-being evaluation** (WHO-5)
- **Detailed results** - Score interpretation and recommendations
- **Progress tracking** - View assessment history over time

### 🔮 AI Mood Prediction
- **Machine learning model** - Predicts future mood patterns
- **Personalized forecasts** - 7-day mood predictions based on history
- **Proactive suggestions** - Alerts before predicted low mood periods

### 📚 Resource Library
- **Curated content** - Articles, videos, and podcasts
- **Crisis hotlines** - Immediate access to emergency support
- **Book recommendations** - Mental health reading list
- **App suggestions** - Recommended mental health apps

### 👤 User Management
- **Secure authentication** - Flask-Login with password hashing
- **Profile management** - Personal information and preferences
- **Privacy controls** - User-controlled data visibility

---

## 🛠️ Technology Stack

### Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| Python | 3.11+ | Core programming language |
| Flask | 2.3.3 | Web framework |
| Flask-Login | 0.6.2 | User authentication |
| SQLite3 | - | Database management |
| OpenAI API | 1.3.0 | Optional advanced AI (fallback available) |

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| HTML5 | - | Structure |
| CSS3 | - | Styling |
| JavaScript | ES6 | Interactivity |
| Jinja2 | 3.1.2 | Templating |
| Chart.js | - | Data visualization |

### AI/NLP Components
| Module | Purpose |
|--------|---------|
| Sentiment Analyzer | Emotion detection from text |
| Crisis Detector | Safety protocol activation |
| Coping Strategies DB | Evidence-based techniques |
| Mood Integration | Pattern recognition |
| Resource Recommender | Personalized suggestions |

---

## 🏗️ Architecture
## 🏗️ Architecture
┌─────────────────────────────────────────────────────────────┐
│ Client Browser │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────────────┐ │
│ │ Dashboard │ │ Mood Tracker│ │ Journal │ │
│ │ Chatbot UI │ │ Assessments │ │ Resources │ │
│ └─────────────┘ └─────────────┘ └─────────────────────┘ │
└─────────────────────────────┬───────────────────────────────┘
│ HTTP/JSON
▼
┌─────────────────────────────────────────────────────────────┐
│ Flask Application │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ Routes (app.py) │ │
│ │ /login /register /dashboard /api/chat /mood │ │
│ └──────────────────────────────────────────────────────┘ │
│ │ │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ AI Chatbot Engine │ │
│ │ ┌────────────────┐ ┌─────────────────────────────┐ │ │
│ │ │Sentiment │ │Crisis Detection │ │ │
│ │ │Analyzer │ │ │ │ │
│ │ └────────────────┘ └─────────────────────────────┘ │ │
│ │ ┌────────────────┐ ┌─────────────────────────────┐ │ │
│ │ │Coping │ │Mood Integration │ │ │
│ │ │Strategies │ │ │ │ │
│ │ └────────────────┘ └─────────────────────────────┘ │ │
│ │ ┌────────────────┐ ┌─────────────────────────────┐ │ │
│ │ │Resource │ │Conversation Memory │ │ │
│ │ │Recommender │ │ │ │ │
│ │ └────────────────┘ └─────────────────────────────┘ │ │
│ └──────────────────────────────────────────────────────┘ │
│ │ │
│ ┌──────────────────────────────────────────────────────┐ │
│ │ Database Layer │ │
│ │ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ │ │
│ │ │Users │ │Moods │ │Journals│ │Assess- │ │ │
│ │ │ │ │ │ │ │ │ments │ │ │
│ │ └────────┘ └────────┘ └────────┘ └────────┘ │ │
│ └──────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ Data Storage │
│ mental_health.db (SQLite) │
└─────────────────────────────────────────────────────────────┘

text

---

## 📥 Installation

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git (optional, for cloning)

### Step 1: Clone the Repository

```bash
git clone https://github.com/laxmipriya-345/MindWell-AI.git
cd MindWell-AI
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Step 4: Set Up Environment Variables
Create a .env file in the root directory:

env
# Flask Configuration
FLASK_SECRET_KEY=your-secret-key-here
FLASK_APP=app.py
FLASK_ENV=development

# Database
DATABASE_URL=sqlite:///mental_health.db

# Optional: OpenAI API (fallback works without it)
OPENAI_API_KEY=your-openai-api-key-here
Step 5: Initialize Database
bash
python init_db.py
Step 6: Run the Application
bash
python app.py
Step 7: Access the Application
Open your browser and navigate to:

text
http://localhost:5000

🎮 Usage Guide
1. Create an Account
Navigate to /register

Enter username, email, and password

Click "Register"

2. Login
Go to /login

Enter your credentials

3. Explore Dashboard
View mood insights and recent activities

Interact with AI chatbot (bottom-right corner)

Access all features from navigation menu

4. Use AI Chatbot
Type your feelings or questions

Get immediate emotional support

Receive coping strategies and resources

Sample Questions to Try:

"I'm feeling anxious about work"

"I feel sad and lonely"

"What helps with stress?"

"I'm overthinking everything"

"I didn't get the job I wanted"

5. Track Your Mood
Go to Mood Tracker

Select your mood and intensity

Add notes about your day

View trends in Mood Analysis
6. Write Journal Entries
Navigate to Journal
Create new entries with AI-generated prompts
View and edit past entries
7. Take Self-Assessments
Go to Self Assessment
Complete mental health screening tools
View results and recommendations
8. View AI Predictions
Visit Prediction page
See AI-generated mood forecasts
Get proactive suggestions
<img width="242" height="863" alt="Screenshot 2026-02-23 095438" src="https://github.com/user-attachments/assets/5bd15938-1125-43df-b987-c1100a413dbc" />
MindWell-AI/
│
├── app.py                      # Main Flask application
├── database.py                 # Database models and connection
├── init_db.py                  # Database initialization script
├── reset_db.py                 # Database reset utility
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── README.md                   # Project documentation
├── LICENSE                     # MIT License
│
├── 🤖 AI Modules
│   ├── minimal_chatbot.py      # Core chatbot engine
│   ├── sentiment_analyzer.py   # Emotion detection
│   ├── crisis_detector.py      # Safety protocol
│   ├── coping_strategies.py    # Strategies database
│   ├── mood_integration.py     # Mood tracking integration
│   ├── resource_recommender.py # Resource suggestions
│   ├── ai_model.py             # ML mood prediction
│   └── mood_analysis.py        # Mood analytics
│
├── 🎨 Templates/
│   ├── base.html               # Base template
│   ├── index.html              # Landing page
│   ├── dashboard.html          # Main dashboard
│   ├── chatbot_component.html  # Chatbot UI
│   ├── login.html              # Login page
│   ├── register.html           # Registration page
│   ├── mood_tracker.html       # Mood logging
│   ├── mood_analysis.html      # Mood visualization
│   ├── journal.html            # Journal entries
│   ├── new_journal_entry.html  # Create entry
│   ├── mental_health_check.html # Self-assessment
│   ├── assessment_result.html  # Assessment results
│   ├── prediction.html         # AI predictions
│   ├── resources.html          # Resource library
│   ├── chat_history.html       # Chat history
│   └── profile.html            # User profile
│
├── 🎨 Static/
│   ├── css/
│   │   ├── style.css           # Main styles
│   │   └── dark-theme.css      # Dark theme
│   └── js/
│       ├── main.js             # Main JavaScript
│       └── chatbot.js          # Chatbot interactions
│
└── 📊 Data Storage
    └── mental_health.db         # SQLite database (created after init)
Development Guidelines
Follow PEP 8 style guide for Python code
Write meaningful commit messages
Update documentation for new features
Test thoroughly before submitting

Future Enhancements:
🤖 AI Chatbot for mental health support
📊 Mood trend visualization
🔔 Reminder notifications
🚑 Emergency contact integration
👨‍💻 Admin analytics panel
☁️ Cloud deployment (AWS)

🏆 Conclusion

MindWell is an intelligent and user-friendly mental health platform that combines web technologies and machine learning to support emotional well-being. It encourages self-awareness, journaling, and proactive mental health management.
🤝 Contributing
Contributions are welcome! Please follow these steps:

Fork the repository

Create a feature branch

bash
git checkout -b feature/amazing-feature
Commit your changes

bash
git commit -m 'Add amazing feature'
Push to branch

bash
git push origin feature/amazing-feature
Open a Pull Request

Development Guidelines
Follow PEP 8 style guide for Python code

Write meaningful commit messages

Update documentation for new features

Test thoroughly before submitting

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.


👩‍💻 Author
Laxmipriya Rout
B.Tech Computer Science & Engineering
Centurion University of Technology and Management
📧 Contact
Project Maintainer: Laxmipriya
GitHub: @laxmipriya-345
Project Link: https://github.com/laxmipriya-345/MindWell-AI

Acknowledgments :
Mental health professionals for insights and strategies
Open-source community for amazing tools
All contributors who help improve this project
⭐ Support
If you like this project, please ⭐ star this repository!
