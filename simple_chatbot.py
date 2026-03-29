# simple_chatbot.py - A complete rule-based chatbot
import random
import re

class SimpleMentalHealthChatbot:
    def __init__(self):
        self.conversation_history = {}
        self.greetings = [
            "Hello! How are you feeling today? 💙",
            "Hi there! I'm here to support you. How can I help?",
            "Hey! How's your day going? I'm listening."
        ]
        
    def get_chat_response(self, user_id, message):
        """Generate response based on keywords"""
        
        message_lower = message.lower()
        
        # Check for crisis keywords first
        crisis_keywords = ['suicide', 'kill myself', 'end my life', 'hurt myself', 
                          'self-harm', 'emergency', 'crisis', 'want to die']
        
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
                'response': random.choice(self.greetings),
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
            
            'relationship': "Relationships affect our mental health deeply. What boundary could you set to protect your peace?",
            
            'therapy': "Therapy is a brave step. A therapist can provide tools and support. Many offer sliding scale fees if cost is a concern.",
            
            'medication': "Medication questions are best discussed with a psychiatrist. I can't give medical advice, but I support you exploring options with professionals.",
            
            'help': "I'm here to help! You can ask me about:\n• Anxiety & stress\n• Depression & sadness\n• Sleep issues\n• Relationship challenges\n• Self-care tips\n\nWhat would be most helpful?",
            
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
        
        # Check for how-long questions
        if 'how long' in message_lower:
            return {
                'success': True,
                'response': "Healing isn't linear. Some feelings pass quickly, others take time. The important thing is you're reaching out. Are you getting support?",
                'crisis_detected': False
            }
        
        # Check for feeling questions
        if 'feel' in message_lower or 'feeling' in message_lower:
            return {
                'success': True,
                'response': "Thank you for sharing. Can you tell me more about what's bringing up these feelings? I'm here to listen.",
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