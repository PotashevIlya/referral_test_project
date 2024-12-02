# Проект простой реферальной системы
## Описание проекта
Данный проект представляе собой API-функционал для регистрации, аутентификации, получения персонального инвайт-кода, ввода чужого инвайт-кода и получения информации о пользователях, воспользовавшихся вашим инвайт кодом. 
## Техническое описание проекта YAMDB
### Ресурсы 
- Ресурс **auth**: регистрация и авторизация.
- Ресурс **profile**: работа с инвайт-кодами, просмотр информации о пользователе и приглашенных пользователях.
### Эндпоинты
1. /api/auth/signup (POST) - регистрация пользователя по номеру телефона
```
{
  "phone_number": "89763457654"
}
```
2. /api/auth/get_token (POST) - авторизация пользователя по полученному коду подтверждения
```
{
  "confirmation_code": "1234"
}
```
3. /api/profile/<int:id> (GET, PATCH) - профиль пользователя, добавление инвайт-кода (только для авторизованых пользователей)
```
{
  "username": "user",
  "phone_number": "89763457654",
  "invitation_code": "123QWE",
  "invited_by": "456RTY",
  "invitations": [89261234567, 87653451234]
}
```
## Как запустить проект

### В контейнерах
1. Клонировать репозиторий и перейти в него в командной строке
```
https://github.com/PotashevIlya/referral_test_project
```
```
cd referral_test_project
```
2. Создать .env файл в корневой директории по образцу .env.example
3. Запустить docker-compose
```
docker compose up -d
```
4. Применить миграции в контейнере бекэнда
```
docker compose exec backend python manage.py migrate
```
5. Собрать статические файлы - последовательно выполнить команды
```
docker compose exec backend python manage.py collectstatic
```
```
docker compose exec backend cp -r /app/collected_static/. /backend_static/static/
```
### Локально
1. Клонировать репозиторий и перейти в него в командной строке
```
https://github.com/PotashevIlya/referral_test_project
```
```
cd referral_test_project
```
2. Создать .env файл в корневой директории по образцу .env.example
3. Перейди в директорию с файлом manage.py и последовательно выполнить команды
```
python manage.py migrate
```
```
python manage.py runserver
```
___
### Стек :bulb:
Python, Django, DRF, PostgreSQL, Docker.
___  
#### Автор проекта:    
:small_orange_diamond: [Поташев Илья](https://github.com/PotashevIlya)  
