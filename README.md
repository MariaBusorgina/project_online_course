
# Тестовое задание Django/Backend

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

Проект представляет собой площадку для размещения онлайн-курсов с набором уроков. Доступ к урокам предоставляется после покупки курса (подписки). Внутри курса студенты автоматически распределяются по группам.

GET http://127.0.0.1:8000/api/v1/available-courses/  
-- список курсов, доступных для покупки (основная информация)  
Пример ответа:  
```json
[
    {
        "id": 3,
        "author": "Автор 3",
        "title": "Третий курс",
        "start_date": "2024-08-19T05:20:12.581457Z",
        "price": "4000.00",
        "lessons_count": 12
    },
    {
        "id": 2,
        "author": "Автор2",
        "title": "Второй курс",
        "start_date": "2024-08-19T05:20:12.581457Z",
        "price": "30000.00",
        "lessons_count": 23
    }
]
```


POST http://127.0.0.1:8000/api/v1/available-courses/<int:pk>/pay/   
-- покупка курса  
* pk — идентификатор курса  
Пример ответа:  
```json
{
    "detail": "Подписка на курс успешно оформлена.",
    "course": {
        "id": 1,
        "title": "Первый курс",
        "price": 10000.0
    },
    "subscription": {
        "id": 20,
        "user": 2,
        "created_at": "2024-08-20T10:20:23.467862Z"
    },
    "user": {
        "balance": 1500.0
    }
}
```


GET http://127.0.0.1:8000/api/v1/courses/<int:pk>/lessons/  
--просмотр уроков курса (доступен после приобретения курса)  
* pk — идентификатор курса  
Пример ответа:  
```json
[
    {
        "title": "урок 1",
        "link": "http://example.com/",
        "course": "Первый курс"
    },
    {
        "title": "урок 2",
        "link": "http://example2.com/",
        "course": "Первый курс"
    }
]
```

GET http://127.0.0.1:8000/api/v1/courses/  
-- просмотр всех курсов (расширенная информация)  
Пример ответа:  
```json
[
    {
        "id": 6,
        "author": "Автор 6",
        "title": "Шестой курс",
        "start_date": "2024-08-19T05:20:12.581457Z",
        "price": "20000.00",
        "lessons_count": 2,
        "lessons": [
            {
                "title": "урок 1"
            },
            {
                "title": "урок 2"
            }
        ],
        "demand_course_percent": 60.0,
        "students_count": 3,
        "groups_filled_percent": 1.0
    }
]
```

GET http://127.0.0.1:8000/api/v1/courses/<int:pk>/groups/   
-- показать список групп определенного курса  
* pk — идентификатор курса  
Пример ответа:  
```json
[
    {
        "title": "Группа №2",
        "course": "Python developer",
        "students": [
            {
                "first_name": "Ольга",
                "last_name": "Иванова",
                "email": "user6@user.com"
            },
            {
                "first_name": "Саша",
                "last_name": "Иванов",
                "email": "user5@user.com"
            },
            {
                "first_name": "Дмитрий",
                "last_name": "Иванов",
                "email": "user4@user.com"
            }
        ]
    },
    {
        "title": "Группа №1",
        "course": "Python developer",
        "students": [
            {
                "first_name": "Андрей",
                "last_name": "Петров",
                "email": "user10@user.com"
            }
        ]
    }
]
```



### __Технологии__
* [Python 3.10.12](https://www.python.org/doc/)
* [Django 4.2.10](https://docs.djangoproject.com/en/4.2/)
* [Django REST Framework  3.14.0](https://www.django-rest-framework.org/)
* [Djoser  2.2.0](https://djoser.readthedocs.io/en/latest/getting_started.html)
