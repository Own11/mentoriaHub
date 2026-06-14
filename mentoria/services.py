from .models import Opportunity
from django.db.models import Q


def get_recommendations(profile):
    """
    Система рекомендаций на основе интересов пользователя.
    
    Логика:
    - STEM: показываем хакатоны и олимпиады
    - BUSINESS: показываем конкурсы и стажировки
    - ENGLISH: показываем все возможности с тегом English
    - UNIVERSITY: показываем университетские программы и гранты
    """
    
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
    """
    Получить избранные курсы для главной страницы.
    """
    from .models import Course
    return Course.objects.all()[:limit]


def get_featured_opportunities(limit=6):
    """
    Получить избранные возможности для главной страницы.
    """
    return Opportunity.objects.all()[:limit]


def get_latest_news(limit=3):
    """
    Получить последние новости.
    """
    from .models import News
    return News.objects.all()[:limit]
