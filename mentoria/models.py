from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid


class Skill(models.Model):
    """
    Навыки, которые преподаются в курсах.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ['name']

    def __str__(self):
        return self.name


class Course(models.Model):
    """
    Курсы, которые могут проходить пользователи.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    preview_image = models.ImageField(upload_to='courses/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Lesson(models.Model):
    """
    Уроки внутри курсов.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField()
    content = models.TextField(blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ['course', 'order']
        unique_together = [['course', 'order']]

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class Opportunity(models.Model):
    """
    Олимпиады, хакатоны, конкурсы, стажировки и гранты.
    """
    CATEGORY_CHOICES = [
        ('OLYMPIAD', 'Олимпиада'),
        ('HACKATHON', 'Хакатон'),
        ('COMPETITION', 'Конкурс'),
        ('INTERNSHIP', 'Стажировка'),
        ('GRANT', 'Грант'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    deadline = models.DateTimeField()
    description = models.TextField()
    apply_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Возможность"
        verbose_name_plural = "Возможности"
        ordering = ['deadline']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class News(models.Model):
    """
    Новости платформы.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='news/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class UserProfile(models.Model):
    """
    Расширенный профиль пользователя.
    """
    INTEREST_CHOICES = [
        ('BUSINESS', 'Business'),
        ('STEM', 'STEM'),
        ('ENGLISH', 'English'),
        ('UNIVERSITY', 'University Prep'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    interests = models.CharField(max_length=100, blank=True, null=True)
    xp = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    streak = models.PositiveIntegerField(default=0)
    last_active = models.DateTimeField(blank=True, null=True)
    completed_lessons = models.ManyToManyField(Lesson, blank=True, related_name='completed_by')
    saved_opportunities = models.ManyToManyField(Opportunity, blank=True, related_name='saved_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"Profile of {self.user.username}"

    def add_xp(self, xp_amount):
        """
        Добавить XP и обновить уровень.
        """
        self.xp += xp_amount
        self.level = self.xp // 100 + 1
        self.save()

    def increment_streak(self):
        """
        Увеличить streak и обновить last_active.
        """
        self.streak += 1
        from django.utils import timezone
        self.last_active = timezone.now()
        self.save()

    def get_recommendations_count(self):
        """
        Получить количество рекомендаций.
        """
        from .services import get_recommendations
        return get_recommendations(self).count()
