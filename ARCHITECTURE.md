# Архитектура Mentoria Hub

## 📐 Структура проекта

```
mentoria/
├── migrations/                 # Миграции БД
│   └── 0001_initial.py        # Первоначальные миграции
│
├── templates/                  # HTML шаблоны Jinja2
│   ├── base.html               # Базовый шаблон (header, footer)
│   ├── home.html               # Главная страница
│   ├── dashboard.html          # Дашборд пользователя
│   │
│   ├── registration/           # Страницы аутентификации
│   │   ├── login.html          # Вход
│   │   └── register.html       # Регистрация
│   │
│   ├── onboarding/             # Процесс онбординга
│   │   └── interests.html      # Выбор интересов
│   │
│   ├── courses/                # Курсы
│   │   ├── course_list.html    # Список всех курсов
│   │   ├── course_detail.html  # Детали курса с прогрессом
│   │   └── lesson_detail.html  # Просмотр отдельного урока
│   │
│   ├── opportunities/          # Возможности
│   │   ├── opportunity_list.html     # Список возможностей
│   │   └── opportunity_detail.html   # Детали возможности
│   │
│   └── news/                   # Новости
│       ├── news_list.html      # Список новостей
│       └── news_detail.html    # Детали новости
│
├── templatetags/               # Custom Django template tags
│   ├── __init__.py
│   └── custom_filters.py       # Фильтры для шаблонов (modulo, multiply, divide)
│
├── __init__.py
├── admin.py                    # Конфигурация Django Admin
├── apps.py                     # Конфигурация приложения
├── forms.py                    # Django формы (RegisterForm, InterestsForm)
├── models.py                   # ORM модели
├── signals.py                  # Django сигналы (автосоздание профиля)
├── services.py                 # Бизнес-логика (рекомендации, функции)
├── urls.py                     # URL маршруты приложения
├── views.py                    # View функции и логика обработки запросов
└── tests.py                    # Unit тесты

config/
├── __init__.py
├── settings.py                 # Конфигурация Django
├── urls.py                     # Главные URL маршруты
├── asgi.py                     # ASGI конфигурация
└── wsgi.py                     # WSGI конфигурация

scripts/
├── __init__.py
└── load_data.py                # Скрипт загрузки тестовых данных

manage.py                       # Django утилита
requirements.txt                # Зависимости проекта
README.md                        # Документация проекта
ARCHITECTURE.md                 # Это файл
db.sqlite3                      # SQLite БД (auto-generated)
```

## 🗄️ Модели данных (models.py)

### Skill
```python
id: UUIDField
name: CharField(100)
description: TextField
created_at: DateTimeField
```
Представляет навык, который преподаётся в курсах.

### Course
```python
id: UUIDField
title: CharField(200)
slug: SlugField(unique)
description: TextField
preview_image: ImageField
created_at/updated_at: DateTimeField
```
Курс, содержит несколько уроков.

### Lesson
```python
id: UUIDField
course: ForeignKey(Course)
title: CharField(200)
description: TextField
video_url: URLField
order: PositiveIntegerField
content: TextField
skills: ManyToManyField(Skill)
created_at: DateTimeField
```
Урок внутри курса. Уроки проходятся линейно (как в Duolingo).

### Opportunity
```python
id: UUIDField
title: CharField(200)
slug: SlugField(unique)
category: CharField(20)  # OLYMPIAD, HACKATHON, COMPETITION, INTERNSHIP, GRANT
deadline: DateTimeField
description: TextField
apply_url: URLField
created_at/updated_at: DateTimeField
```
Возможность (олимпиада, хакатон, конкурс, стажировка, грант).

### News
```python
id: UUIDField
title: CharField(200)
text: TextField
image: ImageField
created_at: DateTimeField
```
Новость на главной странице платформы.

### UserProfile
```python
id: UUIDField
user: OneToOneField(User)
interests: CharField(100)
xp: PositiveIntegerField
level: PositiveIntegerField
streak: PositiveIntegerField
last_active: DateTimeField
completed_lessons: ManyToManyField(Lesson)
saved_opportunities: ManyToManyField(Opportunity)
created_at/updated_at: DateTimeField
```
Профиль пользователя с прогрессом и статистикой.

## 🔄 Основные Views (views.py)

### Authentication
- `register()` - Регистрация нового пользователя
- `login_view()` - Вход в систему
- `logout_view()` - Выход из системы

### Onboarding
- `interests_view()` - Выбор интересов после регистрации

### Dashboard
- `home()` - Главная страница
- `dashboard()` - Личный дашборд пользователя

### Courses
- `course_list()` - Список всех курсов с поиском
- `course_detail()` - Детали курса с прогрессом
- `lesson_detail()` - Просмотр отдельного урока
- `complete_lesson()` - Отметить урок как завершённый (AJAX)

### Opportunities
- `opportunity_list()` - Список возможностей с фильтрацией
- `opportunity_detail()` - Детали возможности
- `save_opportunity()` - Сохранить/удалить из избранного (AJAX)

### News
- `news_list()` - Список новостей
- `news_detail()` - Детали новости

## 🧠 Services (services.py)

### get_recommendations(profile)
Система рекомендаций на основе интересов пользователя:
- STEM → Хакатоны, Олимпиады
- BUSINESS → Конкурсы, Стажировки
- ENGLISH → Все возможности
- UNIVERSITY → Гранты, Стажировки

### Утилиты
- `get_featured_courses()` - Получить курсы для главной
- `get_featured_opportunities()` - Получить возможности для главной
- `get_latest_news()` - Получить последние новости

## 🔐 Security Features

1. **CSRF Protection** - Django middleware защищает от CSRF атак
2. **Password Hashing** - Пароли хешируются с использованием PBKDF2
3. **SQL Injection Protection** - ORM защищает от SQL инъекций
4. **Authentication** - Встроенная система аутентификации Django
5. **Permission System** - Проверка прав доступа через `@login_required`

## 📊 Database Schema

```
User (Django auth)
  ↓ OneToOne
UserProfile
  ├── completed_lessons → Lesson (ManyToMany)
  └── saved_opportunities → Opportunity (ManyToMany)

Course
  ├── lessons (ForeignKey)
  │   ├── skills (ManyToMany to Skill)
  │   └── completed_by (ManyToMany to UserProfile)
  └── preview_image

Opportunity
  ├── saved_by (ManyToMany to UserProfile)
  └── news (related)

Skill
  ├── lessons (related)
  └── courses (via Lesson)
```

## 🎯 URLs Routing (urls.py)

```
/                                    → home
/register/                          → register
/login/                             → login_view
/logout/                            → logout_view
/interests/                         → interests_view
/dashboard/                         → dashboard
/courses/                           → course_list
/courses/<slug>/                    → course_detail
/lessons/<uuid>/                    → lesson_detail
/lessons/<uuid>/complete/           → complete_lesson (POST)
/opportunities/                     → opportunity_list
/opportunities/<slug>/              → opportunity_detail
/opportunities/<uuid>/save/         → save_opportunity (POST)
/news/                              → news_list
/news/<uuid>/                       → news_detail
/admin/                             → Django Admin
```

## 🎨 Frontend Stack

- **HTML5** - Семантическая разметка
- **Tailwind CSS** - Утилитарный CSS фреймворк
- **Vanilla JavaScript** - Нет зависимостей от фреймворков
- **Font Awesome Icons** - Иконки 6.4.0
- **Responsive Design** - Mobile-first подход

## 📱 Responsive Breakpoints

- **Mobile**: < 768px (MD breakpoint)
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

Используются Tailwind классы: `md:`, `lg:` для адаптивности.

## 🧩 Key Features Implementation

### XP & Leveling
```python
# При завершении урока:
profile.add_xp(20)  # +20 XP
profile.increment_streak()  # Увеличить streak
# level = xp // 100 + 1 (автоматически)
```

### Рекомендации
```python
# На основе интересов:
recommendations = get_recommendations(profile)
# Возвращает подходящие возможности
```

### Линейное прохождение курсов
```python
# Урок 1 → Открыт
# Урок 2 → Заблокирован (пока не завершён урок 1)
# Урок 3 → Заблокирован (пока не завершены уроки 1-2)
```

## 🔧 Configuration (settings.py)

- `INSTALLED_APPS` - Включено приложение 'mentoria'
- `TEMPLATES['DIRS']` - Путь к шаблонам
- `LANGUAGE_CODE` - 'ru-RU' для русского языка
- `TIME_ZONE` - 'Europe/Moscow'
- `MEDIA_ROOT/URL` - Для загруженных файлов
- `LOGIN_URL` - Перенаправление при не авторизованном доступе
- `LOGIN_REDIRECT_URL` - Редирект после входа

## 🚀 Development Workflow

1. **Местный запуск**:
   ```bash
   python manage.py runserver
   ```

2. **Создание моделей**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Загрузка данных**:
   ```bash
   python manage.py shell < scripts/load_data.py
   ```

4. **Тестирование**:
   ```bash
   python manage.py test
   ```

5. **Сбор статических файлов** (для продакшена):
   ```bash
   python manage.py collectstatic --noinput
   ```

## 📦 Dependencies

```
Django==6.0.6           # Web framework
Pillow==12.2.0         # Image processing
sqlparse==0.5.5        # SQL parsing
asgiref==3.11.1        # ASGI utilities
```

## 🔄 Data Flow

1. **Регистрация** → Django создаёт User → Signal создаёт UserProfile
2. **Выбор интересов** → Сохраняется в UserProfile.interests
3. **Просмотр курса** → Берётся список уроков с статусами доступа
4. **Завершение урока** → View добавляет XP, увеличивает streak
5. **Дашборд** → Рекомендации из get_recommendations()
6. **Сохранение возможности** → Добавляется в saved_opportunities (M2M)

---

Проект готов к развёртыванию и использованию на хакатоне! 🚀
