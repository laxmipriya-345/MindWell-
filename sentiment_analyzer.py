# sentiment_analyzer.py
import re
from collections import Counter

class SentimentAnalyzer:
    def __init__(self):
        self.emotion_keywords = {
            'happy': ['happy', 'great', 'wonderful', 'excellent', 'amazing', 'joy', 'excited', 
                      'good', 'fantastic', 'awesome', 'glad', 'pleased', 'grateful'],
            'sad': ['sad', 'depressed', 'down', 'low', 'unhappy', 'miserable', 'grief', 
                    'heartbroken', 'devastated', 'blue', 'gloomy'],
            'anxious': ['anxious', 'anxiety', 'worried', 'nervous', 'panic', 'scared', 
                        'fear', 'terrified', 'uneasy', 'apprehensive'],
            'angry': ['angry', 'mad', 'frustrated', 'annoyed', 'irritated', 'rage', 
                      'furious', 'upset', 'resentful'],
            'stressed': ['stress', 'stressed', 'overwhelmed', 'pressure', 'burnout', 
                         'tension', 'burdened', 'exhausted'],
            'lonely': ['lonely', 'alone', 'isolated', 'abandoned', 'forsaken', 'neglected']
        }
        
        self.intensity_modifiers = {
            'very': 2.0,
            'extremely': 2.5,
            'so': 1.8,
            'really': 1.8,
            'quite': 1.5,
            'somewhat': 0.8,
            'a little': 0.6
        }
        
    def detect_emotion(self, text):
        """Detect primary emotion from text"""
        text_lower = text.lower()
        scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in text_lower:
                    # Check for intensity modifiers before the keyword
                    words = text_lower.split()
                    for i, word in enumerate(words):
                        if keyword in word:
                            # Look back for intensity modifier
                            if i > 0 and words[i-1] in self.intensity_modifiers:
                                score += self.intensity_modifiers[words[i-1]]
                            else:
                                score += 1
            
            if score > 0:
                scores[emotion] = score
        
        if not scores:
            return 'neutral'
        
        # Return emotion with highest score
        return max(scores, key=scores.get)
    
    def get_sentiment_score(self, text):
        """Return sentiment score from -1 (negative) to 1 (positive)"""
        positive_words = ['happy', 'great', 'good', 'wonderful', 'excellent', 'amazing', 
                         'awesome', 'fantastic', 'glad', 'joy', 'excited']
        negative_words = ['sad', 'bad', 'terrible', 'awful', 'horrible', 'depressed', 
                         'anxious', 'stress', 'angry', 'lonely', 'miserable']
        
        text_lower = text.lower()
        positive_score = sum(1 for word in positive_words if word in text_lower)
        negative_score = sum(1 for word in negative_words if word in text_lower)
        
        if positive_score == 0 and negative_score == 0:
            return 0
        
        total = positive_score + negative_score
        return (positive_score - negative_score) / total
    
    def get_emotion_intensity(self, text):
        """Get intensity of emotion (1-5)"""
        text_lower = text.lower()
        intensity = 1
        
        for modifier, multiplier in self.intensity_modifiers.items():
            if modifier in text_lower:
                intensity += multiplier * 0.5
        
        # Check for exclamation marks
        exclamation_count = text.count('!')
        intensity += min(exclamation_count * 0.3, 1.5)
        
        # Check for all caps
        if text.isupper() and len(text) > 3:
            intensity += 1
        
        return min(round(intensity), 5)