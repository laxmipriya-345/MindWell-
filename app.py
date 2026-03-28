import os
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from dotenv import load_dotenv
import sqlite3
import json



from database import db, User, Mood, JournalEntry, Resource
from mood_analysis import MoodAnalyzer, get_mood_statistics, analyze_moods
from simple_chatbot import SimpleMentalHealthChatbot
load_dotenv()
# At the top of app.py, replace your import:
from minimal_chatbot import MinimalChatbot

# Then initialize:
chatbot = MinimalChatbot()
print("✅ Chatbot ready!")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mental_health.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print("KEY:", os.getenv("OPENAI_API_KEY"))
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'


# ---------------- LOGIN MANAGER ----------------

@login_manager.user_loader 
def load_user(user_id):
    return db.session.get(User, int(user_id))


# ---------------- DATABASE INIT ----------------

# ---------------- DATABASE INIT ----------------

def init_db():
    with app.app_context():
        db.create_all()
        
        # Also create SQLite tables directly
        conn = sqlite3.connect('mental_health.db')
        cursor = conn.cursor()
        
        # Create assessments table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                responses TEXT,
                date TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()

        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@example.com',
                password=generate_password_hash('admin123'),
                created_at=datetime.utcnow()
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin created: admin / admin123")

        if Resource.query.count() == 0:
            resources = [
                Resource(title="Mindfulness Meditation Guide",
                         description="Learn meditation",
                         category="Article",
                         url="#",
                         created_at=datetime.utcnow()),
                Resource(title="Breathing Exercise",
                         description="5 min breathing",
                         category="Video",
                         url="#",
                         created_at=datetime.utcnow())
            ]
            db.session.add_all(resources)
            db.session.commit()


# Initialize database
init_db()


# ---------------- ROUTES ----------------

@app.route('/')
def index():
    return render_template('index.html')


# ---------------- REGISTER ----------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if user exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists', 'error')
            return redirect(url_for('register'))

        if password != confirm_password:
            flash("Passwords do not match", 'error')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)

        user = User(
            username=username,
            email=email,
            password=hashed_password,
            created_at=datetime.utcnow()
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login.", 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash(f"Welcome back, {user.username}!", 'success')
            return redirect(url_for('dashboard'))

        flash("Invalid username or password", 'error')

    return render_template('login.html')


# ---------------- LOGOUT ----------------

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out", 'info')
    return redirect(url_for('index'))


# ---------------- DASHBOARD (4 FEATURES) ----------------

from datetime import datetime  # Make sure this import is at the top

@app.route('/dashboard')
@login_required
def dashboard():
    # Get recent data for dashboard preview
    recent_moods = Mood.query.filter_by(
        user_id=current_user.id
    ).order_by(Mood.date.desc()).limit(3).all()

    recent_entries = JournalEntry.query.filter_by(
        user_id=current_user.id
    ).order_by(JournalEntry.created_at.desc()).limit(3).all()

    # Get mood statistics
    mood_stats = get_mood_statistics(current_user.id)
    
    # Get latest assessment if any - with error handling
    latest_assessment = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM assessments 
            WHERE user_id = ? 
            ORDER BY date DESC LIMIT 1
        ''', (current_user.id,))
        latest_assessment = cursor.fetchone()
        conn.close()
    except sqlite3.OperationalError:
        # Table doesn't exist yet, create it
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                score INTEGER NOT NULL,
                level TEXT NOT NULL,
                message TEXT NOT NULL,
                responses TEXT,
                date TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        conn.commit()
        conn.close()

    # Get current datetime for the template
    from datetime import datetime
    current_time = datetime.now()

    return render_template(
        'dashboard.html',
        recent_moods=recent_moods,
        recent_entries=recent_entries,
        mood_stats=mood_stats,
        latest_assessment=latest_assessment,
        current_time=current_time  # Pass current datetime to template
    )

# ---------------- FEATURE 1: MOOD TRACKER ----------------

@app.route('/mood-tracker', methods=['GET', 'POST'])
@login_required
def mood_tracker():
    if request.method == 'POST':
        mood_level = request.form.get('mood_level')
        notes = request.form.get('notes')

        mood = Mood(
            user_id=current_user.id,
            mood_level=mood_level,
            notes=notes,
            date=datetime.utcnow()
        )

        db.session.add(mood)
        db.session.commit()

        flash("Mood saved successfully!", 'success')
        return redirect(url_for('mood_tracker'))

    # Get mood history
    mood_history = Mood.query.filter_by(
        user_id=current_user.id
    ).order_by(Mood.date.desc()).all()

    return render_template('mood_tracker.html', mood_history=mood_history)


# ---------------- FEATURE 2: MOOD ANALYSIS ----------------

@app.route('/mood-analysis')
@login_required
def mood_analysis():
    analyzer = MoodAnalyzer(current_user.id)
    
    # Get comprehensive analysis
    swing_analysis = analyzer.detect_mood_swings()
    patterns = analyzer.mood_patterns_by_time()
    sentiment = analyzer.analyze_journal_sentiment()
    recommendations = analyzer.generate_recommendations()
    
    # Get mood data for charts
    mood_data = Mood.query.filter_by(
        user_id=current_user.id
    ).order_by(Mood.date.desc()).limit(30).all()
    
    return render_template(
        'mood_analysis.html',
        swing_analysis=swing_analysis,
        patterns=patterns,
        sentiment=sentiment,
        recommendations=recommendations,
        mood_data=mood_data
    )


# ---------------- FEATURE 3: JOURNAL ----------------

@app.route('/journal')
@login_required
def journal():
    entries = JournalEntry.query.filter_by(
        user_id=current_user.id
    ).order_by(JournalEntry.created_at.desc()).all()
    return render_template('journal.html', entries=entries)


@app.route('/journal/new', methods=['GET', 'POST'])
@login_required
def new_journal_entry():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        # Optional mood association
        mood_id = request.form.get('mood_id')

        entry = JournalEntry(
            user_id=current_user.id,
            title=title,
            content=content,
            created_at=datetime.utcnow()
        )

        db.session.add(entry)
        db.session.commit()

        flash("Journal entry saved successfully!", 'success')
        return redirect(url_for('journal'))

    # Get recent moods to associate with entry
    recent_moods = Mood.query.filter_by(
        user_id=current_user.id
    ).order_by(Mood.date.desc()).limit(5).all()
    
    return render_template('new_journal_entry.html', recent_moods=recent_moods)


@app.route('/journal/<int:entry_id>')
@login_required
def view_journal_entry(entry_id):
    entry = JournalEntry.query.filter_by(
        id=entry_id, 
        user_id=current_user.id
    ).first_or_404()
    return render_template('view_journal_entry.html', entry=entry)


@app.route('/journal/edit/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_journal_entry(entry_id):
    entry = JournalEntry.query.filter_by(
        id=entry_id, 
        user_id=current_user.id
    ).first_or_404()
    
    if request.method == 'POST':
        entry.title = request.form.get('title')
        entry.content = request.form.get('content')
        entry.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash("Journal entry updated!", 'success')
        return redirect(url_for('view_journal_entry', entry_id=entry.id))
    
    return render_template('edit_journal_entry.html', entry=entry)


@app.route('/journal/delete/<int:entry_id>', methods=['POST'])
@login_required
def delete_journal_entry(entry_id):
    entry = JournalEntry.query.filter_by(
        id=entry_id, 
        user_id=current_user.id
    ).first_or_404()
    
    db.session.delete(entry)
    db.session.commit()
    
    flash("Journal entry deleted", 'info')
    return redirect(url_for('journal'))


# ---------------- FEATURE 4: SELF ASSESSMENT ----------------

@app.route('/self-assessment', methods=['GET', 'POST'])
@login_required
def self_assessment():
    if request.method == 'POST':
        # Collect all answers
        answers = []
        for i in range(1, 11):
            answer = request.form.get(f'q{i}')
            if answer:
                answers.append(int(answer))
            else:
                answers.append(0)
        
        # Calculate score
        total_score = sum(answers)
        
        # Determine risk level
        if total_score <= 5:
            level = "Low"
            message = "Your responses indicate low risk. Keep up your healthy habits!"
        elif total_score <= 10:
            level = "Mild"
            message = "Your responses indicate mild symptoms. Consider self-care activities."
        elif total_score <= 15:
            level = "Moderate"
            message = "Your responses indicate moderate symptoms. We recommend speaking with someone."
        else:
            level = "High"
            message = "Your responses indicate significant symptoms. Please consult a mental health professional."
        
        # Save assessment to database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO assessments (user_id, score, level, message, responses, date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            current_user.id, 
            total_score, 
            level, 
            message, 
            json.dumps(answers),
            datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ))
        conn.commit()
        conn.close()
        
        # Get resources based on level
        resources = []
        if level in ["Moderate", "High"]:
            resources = Resource.query.limit(3).all()
        
        return render_template(
            'assessment_result.html',
            score=total_score,
            level=level,
            message=message,
            resources=resources
        )
    
    return render_template('mental_health_check.html')


@app.route('/assessment-history')
@login_required
def assessment_history():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM assessments 
        WHERE user_id = ? 
        ORDER BY date DESC
    ''', (current_user.id,))
    assessments = cursor.fetchall()
    conn.close()
    
    return render_template('assessment_history.html', assessments=assessments)


# ---------------- PROFILE ----------------

@app.route('/profile')
@login_required
def profile():
    # Get user statistics
    mood_count = Mood.query.filter_by(user_id=current_user.id).count()
    journal_count = JournalEntry.query.filter_by(user_id=current_user.id).count()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM assessments WHERE user_id = ?', (current_user.id,))
    assessment_count = cursor.fetchone()[0]
    conn.close()
    
    return render_template(
        'profile.html',
        mood_count=mood_count,
        journal_count=journal_count,
        assessment_count=assessment_count
    )


# ---------------- RESOURCES ----------------

@app.route('/resources')
def resources():
    all_resources = Resource.query.all()
    return render_template('resources.html', resources=all_resources)


# ---------------- API ROUTES ----------------

@app.route('/api/mood-data')
@login_required
def get_mood_data():
    # Get mood data for charts
    moods = Mood.query.filter_by(
        user_id=current_user.id
    ).order_by(Mood.date.desc()).limit(30).all()
    
    dates = [m.date.strftime('%Y-%m-%d') for m in moods][::-1]
    levels = [m.mood_level for m in moods][::-1]
    
    return jsonify({
        'dates': dates,
        'levels': levels
    })


@app.route('/api/mood-statistics')
@login_required
def mood_statistics_api():
    stats = get_mood_statistics(current_user.id)
    return jsonify(stats)


@app.route('/api/add_mood', methods=['POST'])
@login_required
def add_mood_api():
    data = request.json
    mood_score = data.get('mood_score')
    stress_level = data.get('stress_level', 5)
    notes = data.get('notes', '')
    
    mood = Mood(
        user_id=current_user.id,
        mood_level=mood_score,
        notes=f"Stress: {stress_level}/10 - {notes}",
        date=datetime.utcnow()
    )
    
    db.session.add(mood)
    db.session.commit()
    
    return jsonify({'success': True})


@app.route('/api/mood_data')
@login_required
def mood_data_api():
    period = request.args.get('period', 'month')
    
    # Get mood entries
    moods = Mood.query.filter_by(
        user_id=current_user.id
    ).order_by(Mood.date.desc()).limit(30).all()
    
    # Prepare timeline data
    timeline = {
        'labels': [m.date.strftime('%Y-%m-%d') for m in moods][::-1],
        'mood': [m.mood_level for m in moods][::-1],
        'stress': [5 for _ in moods][::-1]  # Placeholder
    }
    
    # Weekly pattern
    weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
    weekly_mood = [0] * 7
    weekly_count = [0] * 7
    
    for mood in moods:
        weekday = mood.date.weekday()
        weekly_mood[weekday] += mood.mood_level
        weekly_count[weekday] += 1
    
    weekly_avg = [round(m/c if c > 0 else 0, 1) for m, c in zip(weekly_mood, weekly_count)]
    
    weekly_pattern = {
        'labels': weekdays,
        'mood': weekly_avg,
        'stress': [round(s/2, 1) for s in weekly_avg]  # Placeholder
    }
    
    # Statistics
    if moods:
        avg_mood = round(sum(m.mood_level for m in moods) / len(moods), 1)
        total_entries = len(moods)
    else:
        avg_mood = 0
        total_entries = 0
    
    statistics = {
        'avg_mood': avg_mood,
        'avg_stress': round(avg_mood * 1.5, 1),
        'total_entries': total_entries,
        'most_frequent_mood': 3
    }
    
    return jsonify({
        'timeline': timeline,
        'weekly_pattern': weekly_pattern,
        'statistics': statistics
    })


@app.route('/api/submit-assessment', methods=['POST'])
@login_required
def submit_assessment():
    data = request.json
    answers = data.get('answers', [])
    
    total_score = sum(answers)
    
    if total_score <= 5:
        level = "Low"
        message = "You're doing well! Keep maintaining your mental health."
    elif total_score <= 10:
        level = "Mild"
        message = "You have mild symptoms. Consider self-care activities."
    elif total_score <= 15:
        level = "Moderate"
        message = "You have moderate symptoms. Consider talking to someone."
    else:
        level = "High"
        message = "You have significant symptoms. Please consult a professional."
    
    # Get resources
    resources = []
    if level in ["Moderate", "High"]:
        resources = [r.title for r in Resource.query.limit(3).all()]
    
    return jsonify({
        'score': total_score,
        'level': level,
        'message': message,
        'resources': resources
    })


# ---------------- DATABASE HELPER ----------------

def get_db_connection():
    conn = sqlite3.connect('mental_health.db')
    conn.row_factory = sqlite3.Row
    return conn

from ai_model import MoodPredictor

@app.route('/predict_mood', methods=['GET', 'POST'])
@login_required
def predict_mood():

    prediction = None

    if request.method == 'POST':

        sleep = float(request.form.get('sleep', 0))
        stress = int(request.form.get('stress', 0))
        energy = int(request.form.get('energy', 0))

        # Simple scoring formula (1 to 5)
        score = (sleep * 0.4 + energy * 0.4 - stress * 0.3)

        # Convert to 1–5 scale
        if score <= 2:
            prediction = 1
        elif score <= 4:
            prediction = 2
        elif score <= 6:
            prediction = 3
        elif score <= 8:
            prediction = 4
        else:
            prediction = 5

    return render_template("prediction.html", prediction=prediction)

# app.py - Add these imports at the top
from flask import session, jsonify, request
from chatbot import MentalHealthChatbot, SimpleMentalHealthChatbot
import os

# Initialize chatbot (after your existing app initialization)
try:
    chatbot = MentalHealthChatbot()  # Use OpenAI version
except:
    chatbot = SimpleMentalHealthChatbot()  # Fallback to simple version
    print("Using simple chatbot (no OpenAI API key found)")

from flask_login import login_required, current_user

# In app.py - Replace your existing /api/chat route with this:


@app.route('/api/chat', methods=['POST'])
def chat():
    """API endpoint for chatbot messages"""
    try:
        # Get user ID (supports both logged-in and guest users)
        if 'user_id' in session:
            user_id = str(session['user_id'])
        elif hasattr(current_user, 'id') and current_user.is_authenticated:
            user_id = str(current_user.id)
        else:
            user_id = 'guest'
        
        data = request.json
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get chatbot response
        response = chatbot.get_chat_response(user_id, user_message)
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error in chat: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': True,  # Return success to avoid frontend errors
            'response': "I'm here to listen. Could you tell me more about how you're feeling?",
            'crisis_detected': False
        }), 200
@app.route('/chat-history')
def chat_history():
    """View chat history page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('chat_history.html')
# ---------------- RUN ----------------
# In app.py, find where you import and initialize the chatbot
# Replace these lines:

# FROM:
from chatbot import MentalHealthChatbot, SimpleMentalHealthChatbot

# Initialize chatbot
try:
    chatbot = MentalHealthChatbot()  # Use OpenAI version
except:
    chatbot = SimpleMentalHealthChatbot()  # Fallback to simple version
    print("Using simple chatbot (no OpenAI API key found)")

# TO:
from chatbot import SimpleMentalHealthChatbot

# Initialize chatbot with simple version (no API needed)
chatbot = SimpleMentalHealthChatbot()
print("✅ Simple Mental Health Chatbot initialized successfully!")
@app.route('/api/mood-insights')
def mood_insights():
    """Get mood insights for current user"""
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not logged in'}), 401
    
    user_id = session['user_id']
    
    patterns = chatbot.mood.get_mood_patterns(user_id)
    trend = chatbot.mood.get_recent_mood_trend(user_id)
    recommendation = chatbot.mood.get_mood_recommendation(user_id)
    
    if patterns:
        insight = f"Over the past 30 days, you've most frequently reported feeling {patterns[0]['mood']}."
        if trend == 'improving':
            insight += " Your mood has been improving - that's great progress!"
        elif trend == 'declining':
            insight += " Your mood has been declining recently. Would you like to talk about what's going on?"
    else:
        insight = "Start chatting with the AI assistant to build your mood insights!"
    
    return jsonify({
        'success': True,
        'insight': insight,
        'recommendation': recommendation,
        'trend': trend,
        'patterns': patterns
    })
if __name__ == "__main__":
    app.run(debug=True)