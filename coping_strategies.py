# coping_strategies.py
import random

class CopingStrategyDB:
    def __init__(self):
        self.strategies = {
            'anxiety': [
                {
                    'name': '5-4-3-2-1 Grounding',
                    'description': 'Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste',
                    'duration': '3 min',
                    'difficulty': 'easy'
                },
                {
                    'name': 'Box Breathing',
                    'description': 'Inhale 4 sec → Hold 4 sec → Exhale 4 sec → Hold 4 sec. Repeat 5 times',
                    'duration': '2 min',
                    'difficulty': 'easy'
                },
                {
                    'name': 'Worry Time',
                    'description': 'Set a timer for 10 minutes to worry, then stop and do something else',
                    'duration': '10 min',
                    'difficulty': 'medium'
                },
                {
                    'name': 'Butterfly Hug',
                    'description': 'Cross arms over chest, tap alternately left-right-left-right while breathing deeply',
                    'duration': '2 min',
                    'difficulty': 'easy'
                }
            ],
            'stress': [
                {
                    'name': 'Progressive Muscle Relaxation',
                    'description': 'Tense each muscle group for 5 seconds, then release. Start from toes to head',
                    'duration': '10 min',
                    'difficulty': 'medium'
                },
                {
                    'name': 'Mindful Walk',
                    'description': 'Walk slowly and notice 5 things you see, 4 you hear, 3 you feel',
                    'duration': '15 min',
                    'difficulty': 'easy'
                },
                {
                    'name': 'Brain Dump',
                    'description': 'Write down everything on your mind without judgment or organization',
                    'duration': '5 min',
                    'difficulty': 'easy'
                }
            ],
            'sad': [
                {
                    'name': 'Behavioral Activation',
                    'description': 'Do one small activity you used to enjoy, even if you don\'t feel like it',
                    'duration': '5 min',
                    'difficulty': 'hard'
                },
                {
                    'name': 'Gratitude List',
                    'description': 'Write down 3 things you\'re grateful for, no matter how small',
                    'duration': '3 min',
                    'difficulty': 'easy'
                },
                {
                    'name': 'Self-Compassion Letter',
                    'description': 'Write a letter to yourself as you would to a dear friend',
                    'duration': '10 min',
                    'difficulty': 'medium'
                }
            ],
            'angry': [
                {
                    'name': 'Cool Down Timer',
                    'description': 'Step away for 10 minutes before responding to anything',
                    'duration': '10 min',
                    'difficulty': 'easy'
                },
                {
                    'name': 'Anger Journal',
                    'description': 'Write down what triggered you and what you\'re really feeling underneath',
                    'duration': '5 min',
                    'difficulty': 'medium'
                },
                {
                    'name': 'Physical Release',
                    'description': 'Squeeze a pillow, go for a run, or do 10 jumping jacks',
                    'duration': '2 min',
                    'difficulty': 'easy'
                }
            ],
            'lonely': [
                {
                    'name': 'Reach Out',
                    'description': 'Send one text to a friend or family member, even just an emoji',
                    'duration': '1 min',
                    'difficulty': 'hard'
                },
                {
                    'name': 'Community Connection',
                    'description': 'Join an online community about something you enjoy',
                    'duration': '10 min',
                    'difficulty': 'medium'
                },
                {
                    'name': 'Acts of Kindness',
                    'description': 'Do something kind for someone else (compliment, help, donate)',
                    'duration': '5 min',
                    'difficulty': 'easy'
                }
            ]
        }
        
        self.daily_practices = {
            'morning': [
                "Set an intention for the day",
                "Stretch for 2 minutes",
                "Name 3 things you're grateful for"
            ],
            'evening': [
                "Reflect on one good thing that happened",
                "Write down tomorrow's top priority",
                "Create a relaxing bedtime routine"
            ]
        }
    
    def get_strategies(self, emotion, limit=2):
        """Get coping strategies for specific emotion"""
        if emotion in self.strategies:
            strategies = self.strategies[emotion]
            return random.sample(strategies, min(limit, len(strategies)))
        return []
    
    def get_daily_practice(self, time_of_day='morning'):
        """Get a daily practice suggestion"""
        return random.choice(self.daily_practices.get(time_of_day, self.daily_practices['morning']))
    
    def get_strategy_by_difficulty(self, difficulty, limit=2):
        """Get strategies by difficulty level"""
        all_strategies = []
        for emotion in self.strategies:
            for strategy in self.strategies[emotion]:
                if strategy['difficulty'] == difficulty:
                    all_strategies.append(strategy)
        return random.sample(all_strategies, min(limit, len(all_strategies)))