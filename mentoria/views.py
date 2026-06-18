from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
import json

from .models import (
    UserProfile, Course, Lesson, Opportunity, News, Skill
)
from .forms import RegisterForm, InterestsForm
from .services import (
    get_recommendations, get_featured_courses, 
    get_featured_opportunities, get_latest_news
)


# ============================================
# AUTHENTICATION VIEWS
# ============================================

def register(request):
    # Registration page view.
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Метод form.save() создает пользователя и автоматически 
            # вызывает ваш сигнал post_save, который создает UserProfile.
            user = form.save()
            
            login(request, user)
            return redirect('interests')
    else:
        form = RegisterForm()
    
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    # Login page view.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'registration/login.html', {
                'error': 'Invalid username or password'
            })
    
    return render(request, 'registration/login.html')


def logout_view(request):
    # Logout view.
    logout(request)
    return redirect('home')


# ============================================
# ONBOARDING VIEWS
# ============================================

@login_required(login_url='login')
def interests_view(request):
    # Interests selection (onboarding) view.
    profile = request.user.profile
    
    if request.method == 'POST':
        form = InterestsForm(request.POST)
        if form.is_valid():
            interests = ','.join(form.cleaned_data['interests'])
            profile.interests = interests
            profile.save()
            return redirect('dashboard')
    else:
        form = InterestsForm()
    
    return render(request, 'onboarding/interests.html', {'form': form})


# ============================================
# HOME & DASHBOARD VIEWS
# ============================================

def home(request):
    # Home page view.
    latest_news = get_latest_news(3)
    featured_courses = get_featured_courses(6)
    featured_opportunities = get_featured_opportunities(6)
    
    context = {
        'latest_news': latest_news,
        'featured_courses': featured_courses,
        'featured_opportunities': featured_opportunities,
    }
    return render(request, 'home.html', context)


@login_required(login_url='login')
def dashboard(request):
    # User dashboard view.
    profile = request.user.profile
    
    if not profile.interests:
        return redirect('interests')
    
    recommendations = get_recommendations(profile)
    saved_opportunities = profile.saved_opportunities.all()[:5]
    completed_lessons = profile.completed_lessons.count()
    total_lessons = Lesson.objects.count()
    
    context = {
        'profile': profile,
        'recommendations': recommendations[:6],
        'saved_opportunities': saved_opportunities,
        'completed_lessons': completed_lessons,
        'total_lessons': total_lessons,
        'upcoming_deadlines': Opportunity.objects.filter(
            deadline__gte=timezone.now()
        ).order_by('deadline')[:5],
    }
    return render(request, 'dashboard.html', context)


# ============================================
# COURSE VIEWS
# ============================================

def course_list(request):
    # List all courses.
    courses = Course.objects.all()
    
    search = request.GET.get('search', '')
    if search:
        courses = courses.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    
    context = {
        'courses': courses,
        'search': search,
    }
    return render(request, 'courses/course_list.html', context)


def course_detail(request, slug):
    # Course detail page with progress.
    course = get_object_or_404(Course, slug=slug)
    lessons = course.lessons.all().order_by('order')
    
    if request.user.is_authenticated:
        profile = request.user.profile
        completed_lessons_ids = profile.completed_lessons.values_list('id', flat=True)
    else:
        completed_lessons_ids = []
    
    lessons_with_status = []
    for idx, lesson in enumerate(lessons):
        is_completed = lesson.id in completed_lessons_ids
        can_access = idx == 0 or lessons[idx - 1].id in completed_lessons_ids
        
        lessons_with_status.append({
            'lesson': lesson,
            'is_completed': is_completed,
            'can_access': can_access,
            'order': idx + 1,
        })
    
    context = {
        'course': course,
        'lessons_with_status': lessons_with_status,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required(login_url='login')
def lesson_detail(request, lesson_id):
    # Lesson detail page.
    lesson = get_object_or_404(Lesson, id=lesson_id)
    profile = request.user.profile
    
    is_completed = lesson in profile.completed_lessons.all()
    
    course = lesson.course
    lessons = course.lessons.all().order_by('order')
    lesson_index = list(lessons).index(lesson)
    
    can_access = lesson_index == 0 or lessons[lesson_index - 1] in profile.completed_lessons.all()
    
    if not can_access and not is_completed:
        return redirect('course_detail', slug=course.slug)
    
    previous_lesson = None
    next_lesson = None
    
    if lesson_index > 0:
        previous_lesson = lessons[lesson_index - 1]
    
    if lesson_index < len(lessons) - 1:
        next_lesson = lessons[lesson_index + 1]
    
    context = {
        'lesson': lesson,
        'course': course,
        'is_completed': is_completed,
        'previous_lesson': previous_lesson,
        'next_lesson': next_lesson,
        'lesson_number': lesson_index + 1,
        'total_lessons': len(lessons),
    }
    return render(request, 'courses/lesson_detail.html', context)


@login_required(login_url='login')
@require_POST
def complete_lesson(request, lesson_id):
    # Mark lesson as completed (AJAX or redirect).
    lesson = get_object_or_404(Lesson, id=lesson_id)
    profile = request.user.profile
    
    if lesson not in profile.completed_lessons.all():
        profile.completed_lessons.add(lesson)
        profile.add_xp(20)
        profile.increment_streak()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'xp': profile.xp,
            'level': profile.level,
            'streak': profile.streak,
        })
    
    course = lesson.course
    lessons = course.lessons.all().order_by('order')
    lesson_index = list(lessons).index(lesson)
    
    if lesson_index < len(lessons) - 1:
        next_lesson = lessons[lesson_index + 1]
        return redirect('lesson_detail', lesson_id=next_lesson.id)
    else:
        return redirect('course_detail', slug=course.slug)


# ============================================
# OPPORTUNITY VIEWS
# ============================================

def opportunity_list(request):
    # List all opportunities.
    opportunities = Opportunity.objects.all()
    
    category = request.GET.get('category', '')
    search = request.GET.get('search', '')
    
    if category:
        opportunities = opportunities.filter(category=category)
    
    if search:
        opportunities = opportunities.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    
    opportunities = opportunities.order_by('deadline')
    
    categories = Opportunity.CATEGORY_CHOICES
    
    context = {
        'opportunities': opportunities,
        'categories': categories,
        'selected_category': category,
        'search': search,
    }
    return render(request, 'opportunities/opportunity_list.html', context)


def opportunity_detail(request, slug):
    # Opportunity detail page.
    opportunity = get_object_or_404(Opportunity, slug=slug)
    
    is_saved = False
    if request.user.is_authenticated:
        is_saved = opportunity in request.user.profile.saved_opportunities.all()
    
    context = {
        'opportunity': opportunity,
        'is_saved': is_saved,
    }
    return render(request, 'opportunities/opportunity_detail.html', context)


@login_required(login_url='login')
@require_POST
def save_opportunity(request, opportunity_id):
    # Toggle save/unsave opportunity for user.
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    profile = request.user.profile
    
    if opportunity in profile.saved_opportunities.all():
        profile.saved_opportunities.remove(opportunity)
        is_saved = False
    else:
        profile.saved_opportunities.add(opportunity)
        is_saved = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'is_saved': is_saved,
        })
    
    return redirect('opportunity_detail', slug=opportunity.slug)


# ============================================
# NEWS VIEWS
# ============================================

def news_list(request):
    # List all news items.
    news = News.objects.all()
    
    search = request.GET.get('search', '')
    if search:
        news = news.filter(
            Q(title__icontains=search) | Q(text__icontains=search)
        )
    
    context = {
        'news': news,
        'search': search,
    }
    return render(request, 'news/news_list.html', context)


def news_detail(request, slug):
    # News detail page.
    news = get_object_or_404(News, id=slug)
    
    context = {
        'news': news,
    }
    return render(request, 'news/news_detail.html', context)