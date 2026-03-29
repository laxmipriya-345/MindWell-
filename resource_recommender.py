# resource_recommender.py
import random

class ResourceRecommender:
    def __init__(self):
        self.resources = {
            'anxiety': {
                'articles': [
                    {'title': 'Understanding Anxiety: A Guide', 'url': '#', 'source': 'Mental Health America'},
                    {'title': '10 Ways to Manage Anxiety', 'url': '#', 'source': 'Anxiety & Depression Association'},
                ],
                'videos': [
                    {'title': 'Guided Meditation for Anxiety', 'url': '#', 'duration': '10 min'},
                    {'title': 'Understanding Panic Attacks', 'url': '#', 'duration': '5 min'},
                ],
                'apps': [
                    {'name': 'Calm', 'description': 'Meditation and sleep stories'},
                    {'name': 'Headspace', 'description': 'Guided meditations for anxiety'},
                ]
            },
            'depression': {
                'articles': [
                    {'title': 'Coping with Depression', 'url': '#', 'source': 'NAMI'},
                    {'title': 'Behavioral Activation', 'url': '#', 'source': 'Psychology Today'},
                ],
                'videos': [
                    {'title': 'Understanding Depression', 'url': '#', 'duration': '8 min'},
                    {'title': 'Self-Care for Depression', 'url': '#', 'duration': '12 min'},
                ],
                'apps': [
                    {'name': 'MoodTools', 'description': 'Depression management app'},
                    {'name': 'Sanvello', 'description': 'CBT techniques and mood tracking'},
                ]
            },
            'stress': {
                'articles': [
                    {'title': 'Stress Management Techniques', 'url': '#', 'source': 'Mayo Clinic'},
                    {'title': 'Workplace Stress Solutions', 'url': '#', 'source': 'APA'},
                ],
                'videos': [
                    {'title': 'Quick Stress Relief', 'url': '#', 'duration': '3 min'},
                    {'title': 'Mindfulness for Stress', 'url': '#', 'duration': '15 min'},
                ]
            }
        }
        
        self.hotlines = {
            'Crisis Lifeline': '988',
            'Crisis Text Line': '741741 (Text HOME)',
            'SAMHSA Helpline': '1-800-662-4357',
            'NAMI Helpline': '1-800-950-6264'
        }
        
        self.books = [
            {'title': 'The Anxiety and Phobia Workbook', 'author': 'Edmund Bourne'},
            {'title': 'Feeling Good: The New Mood Therapy', 'author': 'David Burns'},
            {'title': 'The Happiness Trap', 'author': 'Russ Harris'},
            {'title': 'Dare: The New Way to End Anxiety', 'author': 'Barry McDonagh'}
        ]
    
    def get_resources(self, emotion, resource_type=None):
        """Get resources for specific emotion"""
        if emotion not in self.resources:
            emotion = 'anxiety'  # Default
        
        resources = self.resources[emotion]
        
        if resource_type:
            return resources.get(resource_type, [])
        
        # Return a mix of resources
        return {
            'articles': random.sample(resources['articles'], min(2, len(resources['articles']))),
            'videos': random.sample(resources['videos'], min(1, len(resources['videos']))),
            'apps': resources.get('apps', [])
        }
    
    def get_hotlines(self):
        """Get crisis hotlines"""
        return self.hotlines
    
    def get_book_recommendation(self, topic=None):
        """Get book recommendation"""
        if topic:
            # Filter books by topic (simplified)
            pass
        return random.choice(self.books)