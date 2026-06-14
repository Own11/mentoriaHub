from .models import Opportunity
from django.db.models import Q


def get_recommendations(profile):
    # Recommendation system based on user interests.
    # Logic:
    # - STEM: show hackathons and olympiads
    # - BUSINESS: show competitions and internships
    # - ENGLISH: show opportunities tagged 'English'
    # - UNIVERSITY: show university programs and grants
    
    if not profile.interests:
        return Opportunity.objects.none()
    
    interests = profile.interests.split(',')
    interests = [interest.strip() for interest in interests]
    
    query = Q()
    
    if 'STEM' in interests:
        query |= Q(category__in=['HACKATHON', 'OLYMPIAD'])
    
    if 'BUSINESS' in interests:
        query |= Q(category__in=['COMPETITION', 'INTERNSHIP'])
    
    if 'UNIVERSITY' in interests:
        query |= Q(category__in=['GRANT', 'INTERNSHIP'])
    
    if not query:
        return Opportunity.objects.all()[:10]
    
    return Opportunity.objects.filter(query).order_by('deadline')[:20]


def get_featured_courses(limit=6):
    # Get featured courses for the homepage.
    from .models import Course
    return Course.objects.all()[:limit]


def get_featured_opportunities(limit=6):
    # Get featured opportunities for the homepage.
    return Opportunity.objects.all()[:limit]


def get_latest_news(limit=3):
    # Get latest news.
    from .models import News
    return News.objects.all()[:limit]
