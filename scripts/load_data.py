import os
import django
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from mentoria.models import Course, Lesson, Skill, Opportunity, News
from django.utils import timezone

# Очистить старые данные (опционально)
# Course.objects.all().delete()
# Skill.objects.all().delete()
# Opportunity.objects.all().delete()
# News.objects.all().delete()

print("🚀 Загрузка тестовых данных...")

# ============================================
# СОЗДАТЬ НАВЫКИ
# ============================================
skills_data = [
    {'name': 'Python', 'description': 'Язык программирования Python'},
    {'name': 'JavaScript', 'description': 'Язык программирования JavaScript'},
    {'name': 'Web Development', 'description': 'Разработка веб-приложений'},
    {'name': 'Data Science', 'description': 'Наука о данных'},
    {'name': 'Machine Learning', 'description': 'Машинное обучение'},
    {'name': 'English', 'description': 'Английский язык'},
    {'name': 'Business', 'description': 'Предпринимательство'},
    {'name': 'Leadership', 'description': 'Лидерство'},
]

skills = {}
for skill_data in skills_data:
    skill, created = Skill.objects.get_or_create(
        name=skill_data['name'],
        defaults={'description': skill_data['description']}
    )
    skills[skill_data['name']] = skill
    status = "✅ Создан" if created else "⏭️ Уже существует"
    print(f"Навык: {skill_data['name']} {status}")

# ============================================
# СОЗДАТЬ КУРСЫ
# ============================================
courses_data = [
    {
        'title': 'Python для начинающих',
        'slug': 'python-beginners',
        'description': 'Полный курс по основам Python. Научитесь программировать с нуля! Включает практические задачи и проекты.',
    },
    {
        'title': 'JavaScript и Web Development',
        'slug': 'javascript-web-dev',
        'description': 'Создавайте интерактивные веб-приложения с помощью JavaScript. От HTML/CSS до ES6+.',
    },
    {
        'title': 'Data Science с Python',
        'slug': 'data-science-python',
        'description': 'Анализируйте данные с помощью Pandas, NumPy и Matplotlib. Научитесь находить закономерности в большом объёме данных.',
    },
    {
        'title': 'Основы английского',
        'slug': 'english-basics',
        'description': 'Учите английский язык. Grammar, vocabulary, speaking, listening - всё в одном курсе.',
    },
    {
        'title': 'Лидерство и управление',
        'slug': 'leadership-management',
        'description': 'Развивайте навыки лидерства. Как мотивировать команду, принимать решения и достигать целей.',
    },
    {
        'title': 'Web Design с Tailwind CSS',
        'slug': 'web-design-tailwind',
        'description': 'Создавайте красивые веб-интерфейсы быстро! Изучите Tailwind CSS и современные тренды в дизайне.',
    },
]

courses = {}
for course_data in courses_data:
    course, created = Course.objects.get_or_create(
        slug=course_data['slug'],
        defaults={
            'title': course_data['title'],
            'description': course_data['description'],
        }
    )
    courses[course_data['slug']] = course
    status = "✅ Создан" if created else "⏭️ Уже существует"
    print(f"Курс: {course_data['title']} {status}")

# ============================================
# СОЗДАТЬ УРОКИ
# ============================================
lessons_data = {
    'python-beginners': [
        {
            'title': 'Введение в Python',
            'description': 'Первый урок! Изучите что такое Python и почему он популярен.',
            'content': 'Python - один из самых популярных языков программирования. Он используется в Data Science, Web Development, AI и многом другом.',
            'order': 1,
            'skills': ['Python'],
            'video_url': 'https://www.youtube.com/embed/rfscVS0vtik',
        },
        {
            'title': 'Переменные и типы данных',
            'description': 'Изучите переменные, строки, числа и булевы значения.',
            'content': 'В Python есть несколько основных типов данных: int, float, str, bool. Переменные используются для хранения значений.',
            'order': 2,
            'skills': ['Python'],
            'video_url': 'https://www.youtube.com/embed/8DvO9XRbqcc',
        },
        {
            'title': 'Условные операторы',
            'description': 'if, elif, else и логические операции.',
            'content': 'Условные операторы позволяют вашему коду принимать решения. Используйте if, elif и else для создания различных путей выполнения.',
            'order': 3,
            'skills': ['Python'],
            'video_url': 'https://www.youtube.com/embed/bxRXwsMqlF8',
        },
        {
            'title': 'Циклы в Python',
            'description': 'Научитесь использовать for и while циклы.',
            'content': 'Циклы позволяют повторять код несколько раз. for и while - два основных типа циклов в Python.',
            'order': 4,
            'skills': ['Python'],
            'video_url': 'https://www.youtube.com/embed/mGSzM0j7DnM',
        },
    ],
    'javascript-web-dev': [
        {
            'title': 'Основы JavaScript',
            'description': 'Введение в JavaScript и DOM.',
            'content': 'JavaScript - язык программирования для веб-браузеров. Он позволяет создавать интерактивные веб-страницы.',
            'order': 1,
            'skills': ['JavaScript', 'Web Development'],
            'video_url': 'https://www.youtube.com/embed/DHvZLI7Tz58',
        },
        {
            'title': 'Работа с DOM',
            'description': 'Как манипулировать HTML элементами с JavaScript.',
            'content': 'DOM (Document Object Model) - представление структуры HTML документа. Вы можете изменять, добавлять и удалять элементы.',
            'order': 2,
            'skills': ['JavaScript', 'Web Development'],
            'video_url': 'https://www.youtube.com/embed/qDZjf9jkn24',
        },
        {
            'title': 'События и обработчики',
            'description': 'Обработка клика, ввода текста и других событий.',
            'content': 'События - это действия пользователя (клик, ввод текста, прокрутка и т.д.). Обработчики событий позволяют реагировать на эти действия.',
            'order': 3,
            'skills': ['JavaScript'],
            'video_url': 'https://www.youtube.com/embed/IWqAEMO3vYY',
        },
    ],
    'english-basics': [
        {
            'title': 'Алфавит и произношение',
            'description': 'Изучите английский алфавит.',
            'content': 'Английский язык использует латинский алфавит из 26 букв. Правильное произношение очень важно.',
            'order': 1,
            'skills': ['English'],
            'video_url': 'https://www.youtube.com/embed/DpJD-c_6Twc',
        },
        {
            'title': 'Базовый словарь',
            'description': 'Изучите самые важные слова для начинающих.',
            'content': 'Начните с самых распространённых слов: hello, goodbye, thank you, please, yes, no и многие другие.',
            'order': 2,
            'skills': ['English'],
            'video_url': 'https://www.youtube.com/embed/Z3wEE_ZR0s4',
        },
    ],
}

all_lessons = {}
for course_slug, course_lessons in lessons_data.items():
    course = courses[course_slug]
    for lesson_data in course_lessons:
        lesson, created = Lesson.objects.get_or_create(
            course=course,
            order=lesson_data['order'],
            defaults={
                'title': lesson_data['title'],
                'description': lesson_data['description'],
                'content': lesson_data.get('content', ''),
                'video_url': lesson_data.get('video_url', ''),
            }
        )
        
        # Добавить навыки
        for skill_name in lesson_data.get('skills', []):
            if skill_name in skills:
                lesson.skills.add(skills[skill_name])
        
        all_lessons[f"{course_slug}_{lesson_data['order']}"] = lesson
        status = "✅ Создан" if created else "⏭️ Уже существует"
        print(f"  Урок: {lesson_data['title']} {status}")

# ============================================
# СОЗДАТЬ ВОЗМОЖНОСТИ
# ============================================
opportunities_data = [
    {
        'title': 'Олимпиада по программированию "Котов"',
        'slug': 'olympiad-kotos',
        'category': 'OLYMPIAD',
        'description': 'Всероссийская олимпиада школьников по информатике. Для школьников 7-11 классов. Регионального и национального уровня.',
        'deadline': timezone.now() + timedelta(days=45),
        'apply_url': 'https://olympiada.ru',
    },
    {
        'title': 'Хакатон IAMID 2024',
        'slug': 'hackathon-iamid-2024',
        'category': 'HACKATHON',
        'description': 'Крупный хакатон для школьников и студентов. Создавайте приложения, выигрывайте призы! Награды до 500,000 рублей.',
        'deadline': timezone.now() + timedelta(days=30),
        'apply_url': 'https://iamid.ru',
    },
    {
        'title': 'Конкурс "Лидеры России"',
        'slug': 'competition-leaders-russia',
        'category': 'COMPETITION',
        'description': 'Конкурс для выявления и поддержки талантливых школьников. Грантовая поддержка для победителей.',
        'deadline': timezone.now() + timedelta(days=60),
        'apply_url': 'https://liders.gov.ru',
    },
    {
        'title': 'Стажировка в Яндексе',
        'slug': 'internship-yandex',
        'category': 'INTERNSHIP',
        'description': 'Летняя стажировка для школьников в компании Яндекс. Работайте с реальными проектами, учитесь от экспертов, получайте опыт.',
        'deadline': timezone.now() + timedelta(days=20),
        'apply_url': 'https://yandex.ru/careers/internship',
    },
    {
        'title': 'Президентский грант для молодёжи',
        'slug': 'grant-president',
        'category': 'GRANT',
        'description': 'Грант от Президента РФ для молодёжных проектов. До 500,000 рублей на реализацию вашей идеи.',
        'deadline': timezone.now() + timedelta(days=90),
        'apply_url': 'https://grants.gov.ru',
    },
    {
        'title': 'Всероссийская олимпиада по математике',
        'slug': 'olympiad-math',
        'category': 'OLYMPIAD',
        'description': 'Традиционная Всероссийская олимпиада школьников по математике. Школьный, муниципальный, региональный и заключительный этапы.',
        'deadline': timezone.now() + timedelta(days=100),
        'apply_url': 'https://rusolymp.ru',
    },
    {
        'title': 'Хакатон по AI и Machine Learning',
        'slug': 'hackathon-ai-ml',
        'category': 'HACKATHON',
        'description': 'Специализированный хакатон посвящённый искусственному интеллекту и машинному обучению. Менторство от опытных разработчиков.',
        'deadline': timezone.now() + timedelta(days=35),
        'apply_url': 'https://aiml-hackathon.ru',
    },
    {
        'title': 'Стажировка в Google',
        'slug': 'internship-google',
        'category': 'INTERNSHIP',
        'description': 'Международная стажировка в Google для одарённых школьников. Оплата до 2000 USD в месяц.',
        'deadline': timezone.now() + timedelta(days=25),
        'apply_url': 'https://google.com/careers',
    },
]

for opp_data in opportunities_data:
    opportunity, created = Opportunity.objects.get_or_create(
        slug=opp_data['slug'],
        defaults={
            'title': opp_data['title'],
            'category': opp_data['category'],
            'description': opp_data['description'],
            'deadline': opp_data['deadline'],
            'apply_url': opp_data['apply_url'],
        }
    )
    status = "✅ Создана" if created else "⏭️ Уже существует"
    print(f"Возможность: {opp_data['title']} {status}")

# ============================================
# СОЗДАТЬ НОВОСТИ
# ============================================
news_data = [
    {
        'title': '🎉 Запуск Mentoria Hub!',
        'text': 'Мы запустили новую платформу Mentoria Hub! Теперь все школьники могут легко находить олимпиады, хакатоны, курсы и другие возможности для развития. Добро пожаловать на платформу развития!',
    },
    {
        'title': '📚 Новый курс по Data Science',
        'text': 'Мы добавили новый полный курс по Data Science с использованием Python! Изучите Pandas, NumPy, Matplotlib и создавайте собственные аналитические проекты. Более 50 часов видео и практических заданий.',
    },
    {
        'title': '🏆 Результаты олимпиады "Котов"',
        'text': 'Поздравляем наших пользователей со успешным участием в олимпиаде "Котов"! Трое финалистов прошли на международный уровень. Спасибо за использование Mentoria Hub!',
    },
    {
        'title': '💻 Хакатон IAMID 2024 стартует',
        'text': 'Начинается регистрация на крупнейший хакатон IAMID 2024! На платформе вы можете подготовиться к хакатону, просмотрев наши курсы по веб-разработке и машинному обучению.',
    },
    {
        'title': '🌟 Новый дизайн сайта',
        'text': 'Мы обновили дизайн Mentoria Hub! Платформа теперь ещё удобнее и красивее. Новый интерфейс вдохновлён популярным приложением Duolingo. Дайте нам знать ваши впечатления!',
    },
]

for news_item in news_data:
    news, created = News.objects.get_or_create(
        title=news_item['title'],
        defaults={'text': news_item['text']}
    )
    status = "✅ Создана" if created else "⏭️ Уже существует"
    print(f"Новость: {news_item['title'][:40]}... {status}")

print("\n✅ Загрузка тестовых данных завершена!")
print(f"📊 Всего создано:")
print(f"  - Курсов: {Course.objects.count()}")
print(f"  - Уроков: {Lesson.objects.count()}")
print(f"  - Навыков: {Skill.objects.count()}")
print(f"  - Возможностей: {Opportunity.objects.count()}")
print(f"  - Новостей: {News.objects.count()}")
print(f"\n🚀 Платформа готова к использованию!")
