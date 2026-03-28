# chatbot.py - Complete file with both chatbot classes
import os
import random
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class MentalHealthChatbot:
    def __init__(self):
        """Initialize the chatbot with OpenAI API"""
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.in_fallback_mode = False
        
        if not self.api_key:
            logging.warning("No OpenAI API key found. Using simple chatbot fallback.")
            self.use_fallback = True
            return
            
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
            self.use_fallback = False
            logging.info("OpenAI chatbot initialized successfully")
        except ImportError:
            logging.error("OpenAI library not installed. Using fallback.")
            self.use_fallback = True
        except Exception as e:
            logging.error(f"Error initializing OpenAI: {e}")
            self.use_fallback = True
            
        self.conversation_history = {}
        
    def get_chat_response(self, user_id, message):
        """Get response with automatic fallback on quota errors"""
        
        # If we're already in fallback mode, use fallback
        if self.use_fallback or self.in_fallback_mode:
            return self.get_fallback_response(user_id, message)
        
        # Initialize conversation history for new users
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = [
                {"role": "system", "content": """You are a compassionate mental health support chatbot. 
                Your role is to provide emotional support, coping strategies, and general mental health 
                information. Always maintain a supportive, non-judgmental tone. Keep responses concise, 
                friendly, and helpful. If someone seems to be in crisis, encourage them to contact 
                professional help services. Never provide medical diagnosis."""}
            ]
        
        # Add user message to history
        self.conversation_history[user_id].append({"role": "user", "content": message})
        
        # Keep only last 10 messages to manage token usage
        if len(self.conversation_history[user_id]) > 11:
            self.conversation_history[user_id] = [
                self.conversation_history[user_id][0]
            ] + self.conversation_history[user_id][-10:]
        
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
            error_msg = str(e)
            logging.error(f"OpenAI API error: {error_msg}")
            
            # Check if it's a quota error
            if 'insufficient_quota' in error_msg or 'exceeded your current quota' in error_msg:
                logging.warning("OpenAI quota exceeded - switching to fallback mode")
                self.in_fallback_mode = True
                return self.get_fallback_response(user_id, message)
            else:
                # Other errors - also use fallback
                return self.get_fallback_response(user_id, message)
    
    def get_fallback_response(self, user_id, message):
        """Simple rule-based chatbot as fallback"""
        
        message_lower = message.lower()
        
        # Check for crisis keywords first
        crisis_keywords = ['suicide', 'kill myself', 'end my life', 'hurt myself', 
                          'self-harm', 'emergency', 'crisis', 'want to die', 
                          'end it all', 'no reason to live']
        
        if any(keyword in message_lower for keyword in crisis_keywords):
            return {
                'success': True,
                'response': "I'm really concerned about what you're sharing. **Please reach out for immediate support:**\n\n📞 **988 Suicide & Crisis Lifeline** - Call or text 988\n💬 **Crisis Text Line** - Text HOME to 741741\n\nYou matter, and there are people who want to help you right now.",
                'crisis_detected': True
            }
        
        # Comprehensive response dictionary
        responses = {
            'hello': "Hello! How are you feeling today? 💙",
            'hi': "Hi there! I'm here to support you. How can I help?",
            'hey': "Hey! How's your day going? I'm listening.",
            'how are you': "I'm doing well, thank you for asking! More importantly, how are you feeling?",
            'anxiety': "I hear that you're feeling anxious. Deep breathing can help - try breathing in for 4 counts, hold for 4, exhale for 4. Would you like to try that with me?",
            'anxious': "Anxiety can feel overwhelming. Here are 3 grounding techniques:\n\n1️⃣ **5-4-3-2-1**: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste\n2️⃣ **Deep breathing**: Inhale for 4 counts, hold for 4, exhale for 4\n3️⃣ **Focus on now**: What's one thing you can control right now?",
            'depressed': "I'm sorry you're feeling this way. Remember that these feelings are temporary. Have you considered talking to a professional about how you're feeling?",
            'depression': "Depression is challenging. Small steps matter - even getting out of bed is an achievement. What's one small thing you could do for yourself today?",
            'stress': "Stress is your body's way of saying you're carrying a lot. Can you identify what's causing the most stress right now?",
            'stressed': "When stressed, try breaking tasks into smaller chunks. What's one small task you could complete right now?",
            'sad': "It's okay to feel sad. Would you like to talk about what's making you feel this way?",
            'happy': "That's wonderful to hear! What's contributing to your happiness today?",
            'good': "I'm glad to hear that! What's been going well for you?",
            'bad': "I'm sorry things aren't going well. Remember that bad days are temporary. What would help you feel a little better right now?",
            'tired': "Rest is important for mental health. When was the last time you took a break?",
            'sleep': "Sleep is crucial for mental health. Try to maintain a consistent sleep schedule. Would you like some tips for better sleep?",
            'lonely': "Feeling lonely is hard. Have you considered reaching out to a friend or joining an online community?",
            'angry': "Anger is valid. Before responding, try counting to ten or taking a short walk to cool down.",
            'help': "I'm here to help! You can ask me about:\n• Anxiety & stress\n• Depression & sadness\n• Sleep issues\n• Relationship challenges\n• Self-care tips\n\nWhat would be most helpful?",
            'thanks': "You're welcome! I'm here whenever you need support. 💙",
            'thank you': "You're welcome! Take care of yourself. 💙",
            'overwhelmed': "Feeling overwhelmed? Let's break it down: What's the ONE most important thing right now? Start there.",
            'panic': "Panic feels scary. Try:\n1. Breathe deeply\n2. Feel your feet on the floor\n3. Name 5 blue things you see\nYou're safe. This will pass."
        }
        
        # Check for exact matches first
        for key, response in responses.items():
            if key in message_lower:
                return {
                    'success': True,
                    'response': response,
                    'crisis_detected': False
                }
        
        # Check for feeling-related questions
        if 'feel' in message_lower or 'feeling' in message_lower:
            return {
                'success': True,
                'response': "Thank you for sharing. Can you tell me more about what's bringing up these feelings? I'm here to listen.",
                'crisis_detected': False
            }
        
        # Default responses
        default_responses = [
            "Thank you for sharing that with me. Can you tell me more about how you're feeling?",
            "I appreciate you opening up. What's been on your mind lately?",
            "Thank you for talking with me. How long have you been feeling this way?",
            "I'm here to listen. What would be most helpful for you right now?",
            "Thank you for sharing. Remember that your feelings are valid. Would you like to explore this more?",
            "I hear you. What support do you need right now?",
            "That's completely valid. Would you like coping strategies or just to talk it through?"
        ]
        
        return {
            'success': True,
            'response': random.choice(default_responses),
            'crisis_detected': False
        }
    
    def detect_crisis_keywords(self, message):
        """Detect if message contains crisis-related keywords"""
        crisis_keywords = ['suicide', 'kill myself', 'end my life', 'hurt myself', 
                          'self-harm', 'emergency', 'crisis', 'want to die', 
                          'end it all', 'no reason to live']
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in crisis_keywords)


# SimpleMentalHealthChatbot class for direct use
class SimpleMentalHealthChatbot:
    def __init__(self):
        """Simple rule-based chatbot that doesn't require API"""
        self.conversation_history = {}
        
    def get_chat_response(self, user_id, message):
        """Generate response based on keywords"""
        
        message_lower = message.lower()
        
        # Check for crisis keywords first
        crisis_keywords = ['suicide', 'kill myself', 'end my life', 'hurt myself', 
                          'self-harm', 'emergency', 'crisis', 'want to die', 
                          'end it all', 'no reason to live']
        
        if any(keyword in message_lower for keyword in crisis_keywords):
            return {
                'success': True,
                'response': "I'm really concerned about what you're sharing. **Please reach out for immediate support:**\n\n📞 **988 Suicide & Crisis Lifeline** - Call or text 988\n💬 **Crisis Text Line** - Text HOME to 741741\n\nYou matter, and there are people who want to help you right now.",
                'crisis_detected': True
            }
        
        # Greeting responses
        greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon']
        if any(greeting in message_lower for greeting in greetings):
            return {
                'success': True,
                'response': random.choice(["Hello! How are you feeling today? 💙", "Hi there! I'm here to support you. How can I help?", "Hey! How's your day going? I'm listening."]),
                'crisis_detected': False
            }
        
        # Comprehensive response dictionary
        responses = {
            'anxiety': "Anxiety can feel overwhelming. Here are 3 grounding techniques:\n\n1️⃣ **5-4-3-2-1**: Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste\n2️⃣ **Deep breathing**: Inhale for 4 counts, hold for 4, exhale for 4\n3️⃣ **Focus on now**: What's one thing you can control right now?",
            'anxious': "I hear your anxiety. Would you like to try a quick breathing exercise with me? 🧘‍♀️",
            'depressed': "Depression is heavy. Remember: you're not alone. Small steps matter. Can you do just one small thing for yourself today? Even making a cup of tea is an achievement. 🌱",
            'depression': "I'm here with you. Depression lies to us - but you matter. Have you considered talking to a therapist? There's no shame in getting support.",
            'stress': "Stress shows you're carrying a lot. What's one thing you can let go of right now? Even for 5 minutes?",
            'stressed': "When stressed, try this: Write down what's stressing you, then write what you CAN control about it. Focus on that.",
            'sad': "It's okay to be sad. Sadness passes through us like weather. Would talking about it help? 💙",
            'lonely': "Loneliness is hard. Even small connections help. Could you text one friend today? Or join a supportive online community?",
            'angry': "Anger is valid. Before reacting, try: step away, breathe, write it out. What's underneath the anger?",
            'sleep': "Sleep tips:\n• Same bedtime/wake time\n• No screens 1hr before bed\n• No caffeine after 2pm\n• Try a sleep meditation app",
            'tired': "Rest is healing. When did you last take real rest? Not just sleep, but letting your mind relax?",
            'overwhelmed': "Feeling overwhelmed? Let's break it down: What's the ONE most important thing right now? Start there.",
            'panic': "Panic feels scary. Try:\n1. Breathe deeply\n2. Feel your feet on the floor\n3. Name 5 blue things you see\nYou're safe. This will pass.",
            'help': "I'm here to help! You can ask me about:\n• Anxiety & stress\n• Depression & sadness\n• Sleep issues\n• Self-care tips\n\nWhat would be most helpful?",
            'thanks': "You're welcome! I'm here anytime. 💙",
            'thank you': "Glad to help! Take care of yourself. 🌟"
        }
        
        # Check for matches
        for key, response in responses.items():
            if key in message_lower:
                return {
                    'success': True,
                    'response': response,
                    'crisis_detected': False
                }
        
        # Default responses
        default_responses = [
            "Thank you for sharing that. How has this been affecting your daily life?",
            "I appreciate you opening up. What support do you need right now?",
            "That's valid. What would be most helpful for you to explore about this?",
            "I'm here to listen. Would you like coping strategies or just to talk it through?",
            "Thank you for trusting me with this. 💙"
        ]
        
        return {
            'success': True,
            'response': random.choice(default_responses),
            'crisis_detected': False
        }
    
    def detect_crisis_keywords(self, message):
        """Check for crisis keywords"""
        crisis_keywords = ['suicide', 'kill myself', 'end my life', 'hurt myself', 
                          'self-harm', 'emergency', 'crisis', 'want to die']
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in crisis_keywords)