# chatbot.py
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class MentalHealthChatbot:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.conversation_history = {}
        
    def get_chat_response(self, user_id, message):
        """Get response from OpenAI API with mental health context"""
        
        # Initialize conversation history for new users
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = [
                {"role": "system", "content": """You are a compassionate mental health support chatbot. 
                Your role is to provide emotional support, coping strategies, and general mental health 
                information. Always maintain a supportive, non-judgmental tone. If someone seems to be in 
                crisis, encourage them to contact professional help services like crisis hotlines. 
                Never provide medical diagnosis or replace professional mental health care."""}
            ]
        
        # Add user message to history
        self.conversation_history[user_id].append({"role": "user", "content": message})
        
        # Keep only last 10 messages to manage token usage
        if len(self.conversation_history[user_id]) > 11:  # 1 system + 10 conversations
            self.conversation_history[user_id] = [
                self.conversation_history[user_id][0]  # Keep system message
            ] + self.conversation_history[user_id][-10:]  # Keep last 10 messages
        
        try:
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history[user_id],
                max_tokens=300,
                temperature=0.7
            )
            
            bot_response = response.choices[0].message.content
            
            # Add bot response to history
            self.conversation_history[user_id].append(
                {"role": "assistant", "content": bot_response}
            )
            
            return {
                'success': True,
                'response': bot_response,
                'crisis_detected': self.detect_crisis_keywords(message)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def detect_crisis_keywords(self, message):
        """Detect if message contains crisis-related keywords"""
        crisis_keywords = ['suicide', 'kill myself', 'end my life', 'hurt myself', 
                          'self-harm', 'emergency', 'crisis']
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in crisis_keywords)

# Optional: Custom logic fallback if no API key
class SimpleMentalHealthChatbot:
    def get_chat_response(self, user_id, message):
        """Simple rule-based chatbot as fallback"""
        
        responses = {
            'anxiety': "I hear that you're feeling anxious. Have you tried deep breathing exercises? Taking slow, deep breaths can help calm your nervous system.",
            'depressed': "I'm sorry you're feeling depressed. Remember that it's okay to not be okay. Have you considered talking to a professional about these feelings?",
            'stress': "Stress can be overwhelming. Try breaking your tasks into smaller chunks and taking regular breaks. What specific situation is causing you stress?",
            'sleep': "Sleep is crucial for mental health. Try maintaining a consistent sleep schedule and avoiding screens before bedtime.",
            'happy': "That's wonderful to hear! What's contributing to your happiness today?",
            'sad': "It's okay to feel sad. Would you like to talk about what's making you feel this way?",
            'lonely': "Feeling lonely can be difficult. Have you considered joining community groups or reaching out to old friends?",
            'angry': "Anger is a valid emotion. Try counting to ten or going for a walk to cool down before responding to triggering situations."
        }
        
        message_lower = message.lower()
        
        for key, response in responses.items():
            if key in message_lower:
                return {
                    'success': True,
                    'response': response,
                    'crisis_detected': False
                }
        
        return {
            'success': True,
            'response': "Thank you for sharing that with me. How long have you been feeling this way? Remember, I'm here to listen and support you.",
            'crisis_detected': False
        }