# minimal_chatbot.py - Enhanced version with all integrations
import random
from sentiment_analyzer import SentimentAnalyzer
from crisis_detector import CrisisDetector
from coping_strategies import CopingStrategyDB
from mood_integration import MoodIntegration
from resource_recommender import ResourceRecommender

class MinimalChatbot:
    def __init__(self):
        print("=" * 50)
        print("🚀 Enhanced Mental Health Chatbot INITIALIZED")
        print("=" * 50)
        
        # Initialize all modules
        self.sentiment = SentimentAnalyzer()
        self.crisis = CrisisDetector()
        self.coping = CopingStrategyDB()
        self.mood = MoodIntegration('mental_health.db')
        self.resources = ResourceRecommender()
        
        self.conversation_memory = {}
        
    def get_chat_response(self, user_id, message):
        """Get intelligent, personalized response"""
        message_lower = message.lower().strip()
        
        print(f"\n📨 User {user_id}: '{message}'")
        
        # Initialize memory for new users
        if user_id not in self.conversation_memory:
            self.conversation_memory[user_id] = []
        
        # 1. CRISIS DETECTION (Highest Priority)
        risk_level, resources = self.crisis.assess_risk_level(message)
        if risk_level != 'none':
            response = self.crisis.get_crisis_response(risk_level, resources)
            return {
                'success': True,
                'response': response,
                'crisis_detected': True,
                'risk_level': risk_level
            }
        
        # 2. EMOTION DETECTION
        emotion = self.sentiment.detect_emotion(message)
        sentiment_score = self.sentiment.get_sentiment_score(message)
        intensity = self.sentiment.get_emotion_intensity(message)
        
        print(f"🎭 Detected: {emotion} (intensity: {intensity}/5, score: {sentiment_score})")
        
        # 3. LOG MOOD
        if user_id != 'guest':
            self.mood.log_chat_mood(int(user_id) if user_id.isdigit() else 0, emotion, message, intensity)
            
            # Get personalized recommendation from mood patterns
            mood_rec = self.mood.get_mood_recommendation(int(user_id) if user_id.isdigit() else 0)
        else:
            mood_rec = None
        
        # 4. GET COPING STRATEGIES
        strategies = self.coping.get_strategies(emotion, limit=2)
        
        # 5. GENERATE RESPONSE
        response = self._generate_response(message, emotion, sentiment_score, strategies, mood_rec)
        
        # 6. ADD RESOURCES FOR INTENSE EMOTIONS
        if intensity >= 4 and emotion != 'neutral':
            resources = self.resources.get_resources(emotion, 'articles')
            if resources:
                response += f"\n\n📚 **Resource:** {resources[0]['title']} - {resources[0]['source']}"
        
        # 7. ADD DAILY PRACTICE SUGGESTION (once per day)
        if len(self.conversation_memory[user_id]) % 10 == 0:  # Every 10 messages
            practice = self.coping.get_daily_practice()
            response += f"\n\n🌟 **Daily practice:** {practice}"
        
        # 8. STORE IN MEMORY
        self.conversation_memory[user_id].append({
            'message': message,
            'emotion': emotion,
            'response': response
        })
        
        # Keep only last 20 messages
        if len(self.conversation_memory[user_id]) > 20:
            self.conversation_memory[user_id] = self.conversation_memory[user_id][-20:]
        
        return {
            'success': True,
            'response': response,
            'crisis_detected': False,
            'emotion': emotion,
            'intensity': intensity
        }
    
    def _generate_response(self, message, emotion, sentiment_score, strategies, mood_rec):
        """Generate intelligent response"""
        message_lower = message.lower()
        
        # Check for specific questions first
        if any(phrase in message_lower for phrase in ['how to happy', 'how to be happy', 'become happy']):
            return self._get_happiness_response()
        
        if any(phrase in message_lower for phrase in ['not selected', 'rejected', 'failed']):
            return self._get_rejection_response(message)
        
        if 'thinking' in message_lower and ('much' in message_lower or 'lot' in message_lower):
            return self._get_overthinking_response()
        
        # Add mood pattern recommendation if available
        if mood_rec:
            return mood_rec
        
        # Emotion-based responses
        emotion_responses = {
            'happy': f"I'm so glad to hear you're feeling happy! 🌟 What's been contributing to your positive mood?",
            'sad': f"I hear your sadness. {self._get_sadness_response()}",
            'anxious': f"I understand anxiety can be overwhelming. {self._get_anxiety_response(strategies)}",
            'angry': f"Anger is valid. Let's take a moment. {self._get_anger_response()}",
            'stressed': f"I hear your stress. {self._get_stress_response(strategies)}",
            'lonely': f"Feeling lonely is hard. {self._get_loneliness_response()}",
            'neutral': self._get_neutral_response(message)
        }
        
        base_response = emotion_responses.get(emotion, emotion_responses['neutral'])
        
        # Add coping strategies if available and not already included
        if strategies and emotion in ['anxious', 'stressed', 'sad'] and 'coping strategy' not in base_response.lower():
            base_response += f"\n\n🧘 **Try this:** {strategies[0]['name']} - {strategies[0]['description']} (takes {strategies[0]['duration']})"
        
        return base_response
    
    def _get_happiness_response(self):
        return """I hear you want to feel happier. Here are some gentle steps:

🌟 **Small steps toward happiness:**
1. **Acknowledge** - It's okay to feel sad right now
2. **One small joy** - Do something you used to enjoy, even briefly
3. **Connect** - Reach out to one person
4. **Move** - A short walk can shift your mood
5. **Be kind to yourself** - Treat yourself like you'd treat a friend

Would you like to try one of these together? 💙"""
    
    def _get_rejection_response(self, message):
        return """I'm really sorry about this disappointment. Rejection hurts.

💙 **Remember:**
- This doesn't define your worth
- Many successful people faced rejections
- This experience will make you stronger
- It's okay to take time to process

Would you like to talk more about how you're feeling?"""
    
    def _get_overthinking_response(self):
        return """Overthinking can be exhausting. Let's break the cycle:

🧠 **To quiet your mind:**
1. **Write it down** - Get thoughts out of your head
2. **Set a timer** - Worry for 5 minutes, then stop
3. **Ask:** "Is this thought helpful right now?"
4. **Take action** - One small step can help
5. **Focus on now** - What's one thing you can control?

What's one small thing you could do right now?"""
    
    def _get_sadness_response(self):
        return """Remember that you're not alone. These feelings will pass, even if it doesn't feel like it now. Would you like to talk about what's making you feel sad, or would some gentle coping ideas help?"""
    
    def _get_anxiety_response(self, strategies):
        if strategies:
            return f"Let's try a quick technique together: {strategies[0]['description']} Would you like to practice this with me?"
        return "Would you like to try a grounding exercise together? 🧘‍♀️"
    
    def _get_stress_response(self, strategies):
        return "Let's take a moment to breathe. What's one thing you can let go of right now, even for 5 minutes?"
    
    def _get_anger_response(self):
        return "Before reacting, let's try: Step away for a moment. Take 5 deep breaths. What's really underneath the anger?"
    
    def _get_loneliness_response(self):
        return "You deserve connection. Could you reach out to one person today? Even a quick text counts. I'm here with you in the meantime. 💙"
    
    def _get_neutral_response(self, message):
        default_responses = [
            "Thank you for sharing. How has this been affecting your daily life?",
            "I appreciate you opening up. What support would help you most?",
            "I hear you. Would you like to explore this more?",
            "Thank you for trusting me. What's one small thing that might help right now?",
            "I'm here to listen. Can you tell me more about what you're experiencing?"
        ]
        return random.choice(default_responses)