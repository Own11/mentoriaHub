from django.contrib import admin
from .models import UserProfile, Skill, Course, Lesson, Opportunity, News


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'xp', 'streak', 'created_at')
    search_fields = ('user__username', 'user__email')
    list_filter = ('level', 'created_at')
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('id', 'created_at')


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('id', 'created_at', 'updated_at')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'created_at')
    search_fields = ('title', 'course__title')
    list_filter = ('course', 'created_at')
    filter_horizontal = ('skills',)
    readonly_fields = ('id', 'created_at')
    ordering = ('course', 'order')


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'deadline', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('category', 'deadline', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'category', 'description')
        }),
        ('Параметры', {
            'fields': ('deadline', 'apply_url')
        }),
        ('Служебная информация', {
            'fields': ('id', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'text')
    list_filter = ('created_at',)
    readonly_fields = ('id', 'created_at')

