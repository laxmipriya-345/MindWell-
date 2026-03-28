# crisis_detector.py
import re

class CrisisDetector:
    def __init__(self):
        self.crisis_patterns = {
            'immediate_risk': [
                r'\b(suicide|kill myself|end my life)\b',
                r'\b(hurt myself|self-harm)\b',
                r'\b(want to die|no reason to live|end it all)\b',
                r'\b(take my life|die)\b.*\b(want|plan)\b'
            ],
            'moderate_risk': [
                r'\b(can\'t go on|give up)\b',
                r'\b(hopeless|worthless)\b',
                r'\b(no one cares|nobody cares)\b',
                r'\b(what\'s the point|why bother)\b'
            ],
            'resources': {
                '988': 'Suicide & Crisis Lifeline - Call or text 988 (24/7)',
                '741741': 'Crisis Text Line - Text HOME to 741741',
                '911': 'Emergency Services - Call 911 for immediate danger'
            }
        }
        
        self.international_resources = {
            'UK': '111 or 999 for emergency',
            'Canada': '988 or 911 for emergency', 
            'Australia': '13 11 14 (Lifeline)',
            'India': '9152987821 (iCall) or 988'
        }
    
    def assess_risk_level(self, message):
        """Assess risk level from message"""
        message_lower = message.lower()
        
        for pattern in self.crisis_patterns['immediate_risk']:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return 'immediate', self.crisis_patterns['resources']
        
        for pattern in self.crisis_patterns['moderate_risk']:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return 'moderate', self.crisis_patterns['resources']
        
        return 'none', None
    
    def get_crisis_response(self, risk_level, resources, location=None):
        """Generate appropriate crisis response"""
        if risk_level == 'immediate':
            response = """⚠️ **I'm very concerned about your safety.**

**You are not alone. Please reach out for immediate support right now:**

📞 **988** - Suicide & Crisis Lifeline (Call or text, 24/7)
💬 **741741** - Crisis Text Line (Text HOME)
🚑 **911** - Emergency Services

**Your life matters.** Please reach out to one of these resources immediately.

If you're in this chat, please confirm that you'll reach out for support. 💙"""
            
            if location and location in self.international_resources:
                response += f"\n\n**In {location}:** {self.international_resources[location]}"
            
            return response
        
        elif risk_level == 'moderate':
            return """💙 **I hear that you're going through a very difficult time.**

**You're not alone in this. Here are resources that can help:**

📞 **988** - Crisis Lifeline (Available 24/7)
💬 **741741** - Text HOME for support
🗣️ **Professional Help** - Consider reaching out to a therapist or counselor

Would you like to talk about what's making you feel this way? I'm here to listen."""
        
        return None
    
    def get_safety_plan_prompt(self):
        """Generate safety planning prompts"""
        return """**Creating a Safety Plan:**

1. **Warning signs:** What thoughts or situations tell you things are getting worse?
2. **Coping strategies:** What helps you feel better when distressed?
3. **Social support:** Who can you reach out to for support?
4. **Professional support:** Who are your mental health professionals?
5. **Safe environment:** How can you make your environment safer?

Would you like to work on creating a safety plan together?"""