from datetime import datetime, timedelta
from database import Mood, JournalEntry
import numpy as np
from collections import defaultdict
import re

class MoodAnalyzer:
    def __init__(self, user_id):
        self.user_id = user_id
        self.moods = Mood.query.filter_by(user_id=user_id).order_by(Mood.date).all()
        self.journals = JournalEntry.query.filter_by(user_id=user_id).order_by(JournalEntry.created_at).all()
    
    def detect_mood_swings(self, days=30):
        """Detect significant mood swings in the last X days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        recent_moods = [m for m in self.moods if m.date >= cutoff_date]
        
        if len(recent_moods) < 5:
            return {
                "status": "insufficient_data", 
                "message": "Not enough mood data to detect swings",
                "avg_mood": 0,
                "volatility": 0,
                "stability": "Unknown",
                "stability_desc": "Track more moods to see analysis",
                "swings_count": 0,
                "swings": [],
                "data_points": len(recent_moods)
            }
        
        mood_levels = [m.mood_level for m in recent_moods]
        
        # Calculate mood volatility (standard deviation)
        volatility = float(np.std(mood_levels)) if len(mood_levels) > 1 else 0
        
        # Detect rapid mood changes
        swings = []
        for i in range(1, len(mood_levels)):
            change = abs(mood_levels[i] - mood_levels[i-1])
            if change >= 2:  # Significant change
                swings.append({
                    'date': recent_moods[i].date.strftime('%Y-%m-%d'),
                    'previous': mood_levels[i-1],
                    'current': mood_levels[i],
                    'change': change
                })
        
        # Calculate average mood
        avg_mood = float(np.mean(mood_levels)) if mood_levels else 0
        
        # Determine mood stability
        if volatility < 0.5:
            stability = "Very Stable"
            stability_desc = "Your mood is very consistent"
        elif volatility < 1.0:
            stability = "Moderately Stable"
            stability_desc = "Your mood shows some variation but generally consistent"
        elif volatility < 1.5:
            stability = "Variable"
            stability_desc = "Your mood varies significantly"
        else:
            stability = "Highly Variable"
            stability_desc = "Your mood shows significant swings"
        
        return {
            "status": "success",
            "volatility": round(volatility, 2),
            "stability": stability,
            "stability_desc": stability_desc,
            "swings_count": len(swings),
            "swings": swings[:5],  # Last 5 swings
            "avg_mood": round(avg_mood, 2),
            "data_points": len(recent_moods)
        }
    
    def mood_patterns_by_time(self):
        """Analyze mood patterns by time of day, day of week, etc."""
        if len(self.moods) < 5:
            return {"status": "insufficient_data"}
        
        patterns = {
            'by_hour': defaultdict(list),
            'by_day': defaultdict(list),
            'by_weekday': defaultdict(list)
        }
        
        for mood in self.moods:
            hour = mood.date.hour
            day = mood.date.strftime('%Y-%m-%d')
            weekday = mood.date.strftime('%A')
            
            # Hourly patterns
            patterns['by_hour'][hour].append(mood.mood_level)
            
            # Daily patterns
            patterns['by_day'][day].append(mood.mood_level)
            
            # Weekday patterns
            patterns['by_weekday'][weekday].append(mood.mood_level)
        
        # Calculate averages
        result = {}
        for category in patterns:
            result[category] = {}
            for key in patterns[category]:
                if patterns[category][key]:
                    result[category][key] = round(float(np.mean(patterns[category][key])), 2)
        
        return result
    
    def analyze_journal_sentiment(self):
        """Basic sentiment analysis from journal entries"""
        if len(self.journals) < 3:
            return {"status": "insufficient_data", "scores": [], "trend": "unknown", "avg_sentiment": 0}
        
        # Simple keyword-based sentiment analysis
        positive_words = ['happy', 'good', 'great', 'excellent', 'wonderful', 'peaceful', 
                         'calm', 'relaxed', 'grateful', 'thankful', 'blessed', 'joy', 
                         'love', 'excited', 'hopeful', 'better', 'improved', 'amazing']
        
        negative_words = ['sad', 'bad', 'terrible', 'awful', 'anxious', 'stressed', 
                         'worry', 'fear', 'scared', 'angry', 'frustrated', 'hopeless',
                         'depressed', 'lonely', 'tired', 'exhausted', 'overwhelmed', 'stuck']
        
        sentiment_scores = []
        
        for journal in self.journals[-20:]:  # Last 20 entries
            text = journal.title + " " + journal.content
            text = text.lower()
            
            # Count words
            words = re.findall(r'\w+', text)
            
            # Count positive and negative words
            pos_count = sum(1 for word in words if word in positive_words)
            neg_count = sum(1 for word in words if word in negative_words)
            
            if pos_count + neg_count > 0:
                sentiment = (pos_count - neg_count) / (pos_count + neg_count)
            else:
                sentiment = 0
            
            sentiment_scores.append({
                'date': journal.created_at.strftime('%Y-%m-%d'),
                'sentiment': round(sentiment, 2),
                'title': journal.title
            })
        
        # Calculate overall trend
        if len(sentiment_scores) > 1:
            mid = len(sentiment_scores) // 2
            first_half = sentiment_scores[:mid]
            second_half = sentiment_scores[mid:]
            
            if first_half and second_half:
                avg_first = np.mean([s['sentiment'] for s in first_half])
                avg_second = np.mean([s['sentiment'] for s in second_half])
                
                if avg_second > avg_first + 0.1:
                    trend = "improving"
                elif avg_second < avg_first - 0.1:
                    trend = "declining"
                else:
                    trend = "stable"
            else:
                trend = "stable"
        else:
            trend = "stable"
        
        avg_sentiment = np.mean([s['sentiment'] for s in sentiment_scores]) if sentiment_scores else 0
        
        return {
            "scores": sentiment_scores[-10:],  # Last 10 entries
            "trend": trend,
            "avg_sentiment": round(float(avg_sentiment), 2)
        }
    
    def generate_recommendations(self):
        """Generate personalized recommendations based on mood patterns"""
        swing_analysis = self.detect_mood_swings()
        patterns = self.mood_patterns_by_time()
        sentiment = self.analyze_journal_sentiment()
        
        recommendations = []
        
        if swing_analysis.get('status') == 'success':
            if swing_analysis['volatility'] > 1.2:
                recommendations.append({
                    'type': 'stability',
                    'title': 'Mood Stability Exercise',
                    'description': 'Your mood shows significant variation. Practice grounding techniques.',
                    'action': 'Try the 5-4-3-2-1 grounding technique: Name 5 things you see, 4 you can touch, 3 you hear, 2 you can smell, and 1 you can taste.'
                })
            
            if swing_analysis['avg_mood'] < 2.5:
                recommendations.append({
                    'type': 'low_mood',
                    'title': 'Mood Improvement',
                    'description': 'Your average mood is lower than ideal.',
                    'action': 'Schedule activities you enjoy. Try to do at least one thing that brings you joy each day.'
                })
        
        # Time-based recommendations
        if patterns and patterns != {"status": "insufficient_data"}:
            if 'by_hour' in patterns and patterns['by_hour']:
                # Find worst hour
                if patterns['by_hour']:
                    worst_hour = min(patterns['by_hour'].items(), key=lambda x: x[1])
                    recommendations.append({
                        'type': 'timing',
                        'title': 'Peak Low Mood Time',
                        'description': f'Your mood tends to be lowest around {worst_hour[0]}:00',
                        'action': 'Schedule self-care activities during this time. Consider taking a short break or doing something you enjoy.'
                    })
            
            if 'by_weekday' in patterns and patterns['by_weekday']:
                # Find best and worst days
                if patterns['by_weekday']:
                    best_day = max(patterns['by_weekday'].items(), key=lambda x: x[1])
                    worst_day = min(patterns['by_weekday'].items(), key=lambda x: x[1])
                    
                    recommendations.append({
                        'type': 'weekly',
                        'title': 'Weekly Mood Pattern',
                        'description': f'Your best day is {best_day[0]} and most challenging day is {worst_day[0]}',
                        'action': f'Plan enjoyable activities on {worst_day[0]}s and use {best_day[0]}s for important tasks.'
                    })
        
        # Sentiment-based recommendations
        if sentiment['avg_sentiment'] < -0.2:
            recommendations.append({
                'type': 'journal',
                'title': 'Journal Sentiment',
                'description': 'Your journal entries show negative sentiment patterns.',
                'action': 'Try gratitude journaling. Each day, write down three things you are grateful for.'
            })
        
        return recommendations

# Helper function for routes
def get_mood_statistics(user_id):
    analyzer = MoodAnalyzer(user_id)
    return {
        'swing_analysis': analyzer.detect_mood_swings(),
        'patterns': analyzer.mood_patterns_by_time(),
        'sentiment': analyzer.analyze_journal_sentiment(),
        'recommendations': analyzer.generate_recommendations()
    }
def analyze_moods(moods):
    """
    Analyze mood patterns from user data
    """
    if not moods:
        return {
            'total_entries': 0,
            'most_common_mood': 'No data',
            'mood_distribution': {},
            'trend': 'Not enough data'
        }
    
    # Count moods
    mood_counts = {}
    for entry in moods:
        mood = entry['mood']
        mood_counts[mood] = mood_counts.get(mood, 0) + 1
    
    # Find most common mood
    most_common = max(mood_counts, key=mood_counts.get) if mood_counts else 'No data'
    
    # Calculate percentages
    total = len(moods)
    distribution = {}
    for mood, count in mood_counts.items():
        distribution[mood] = {
            'count': count,
            'percentage': round((count / total) * 100, 1)
        }
    
    # Simple trend analysis (last 7 days vs previous 7)
    if len(moods) >= 14:
        recent = list(moods[:7])
        previous = list(moods[7:14])
        
        recent_score = sum([mood_value(m['mood']) for m in recent]) / 7
        previous_score = sum([mood_value(m['mood']) for m in previous]) / 7
        
        if recent_score > previous_score:
            trend = "Improving"
        elif recent_score < previous_score:
            trend = "Declining"
        else:
            trend = "Stable"
    else:
        trend = "Need more data"
    
    return {
        'total_entries': total,
        'most_common_mood': most_common,
        'mood_distribution': distribution,
        'trend': trend
    }

def mood_value(mood):
    """Convert mood to numerical value for analysis"""
    mood_map = {
        'great': 5,
        'good': 4,
        'okay': 3,
        'bad': 2,
        'terrible': 1
    }
    return mood_map.get(mood.lower(), 3)