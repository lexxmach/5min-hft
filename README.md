# HFT за 5 минут

*Разработчики: Лозовская Алина, Фролов Константин, Молчан Егор*

Тренажер по программированию, с различными мини-играми.

Мини-игры предоставляются в виде различных уровней сложности, от начинающего до продвинутого.

Каждая мини-игра связанна с различными рабочими трудностями, возникающими при разработке проекта.

Примеры мини-игр: что выведет код, посчитать сложность алгоритма, построчно выполнить код программы. Так же, есть возможность проведения собственного экзамена: наша платформа предоставляет возмонжость и для этого.

## Документации:
- Основное: [docs/](./docs/)
- Карточка проекта: [docs/project-card.png](docs/project-card.png)
- PRD: [docs/PRD.pdf](docs/PRD.pdf)
- Диаграмма Ганта: https://docs.google.com/spreadsheets/d/19IxDveW5Dm3P16UAxXZXRiz_nkg1MDE4at7p8hFMfkA/edit?gid=0#gid=0
- Технический радар: https://docs.google.com/spreadsheets/d/1XgmF2gqGeEAsDxNcD5gmT8FLyCRNOpxdnDFTm9zotzo/edit?gid=0#gid=0
- Матрица планирования Хосин-Канри: https://docs.google.com/spreadsheets/d/1RU-CMqkQ88slHYeuyPCwcD5cqCkfdI2e/edit?usp=sharing&ouid=102374390749273509030&rtpof=true&sd=true
- Интерактивная структура базы данных: https://dbdiagram.io/d/hft-5-min-6728b564e9daa85aca3cf2ea

## Скриншоты

![Регистрация и логин](/docs/screenshots/login-screen.png) 
![Вопросы](/docs/screenshots/question.png) 
![Создание экзаменационной комнаты](/docs/screenshots/room.png) 

# Техническое

## Запуск базы данных и бэкенда:

```
docker-compose up --build -d
```

## Запустить фронтэнд

```
cd front && npm start
```

## Структура базы данных и примеры

Интерактивная: https://dbdiagram.io/d/hft-5-min-6728b564e9daa85aca3cf2ea

![Структура базы данных](/docs/hft-5-min.png) 
