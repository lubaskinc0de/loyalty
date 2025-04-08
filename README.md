# 💸 Loyalty

### 📋 Идея проекта
- **Проблема**: Отсутствие единой программы лояльности с гибкой настройкой, куча узкоспециализированных решений под каждое предприятие
- **Цель**: Создание единой системы программы лояльности
- **Целевая аудитория**: Бизнесы и их клиенты

## ✒️🙂 Участники команды
-   **Любавский Илья** 👨‍💻
-   **Мельниченко Роман** 👨‍💻

## Функциональные требования
- До регистрации пользователь может просматривать актуальные программы лояльности
- ✅ Регистрация бизнеса
- ✅ Регистрация клиента (пользователь который участвует в программах лояльности)
- ✅ Логин клиента и бизнеса
- Личный кабинет бизнеса:
    - просмотр информации о бизнесе
    - CRUD над филиалами бизнеса
    - просмотр некоторой статистики
    - CRUD над **программами лояльности**
        - ограничение программы по филиалам
        - добавление описания программы
        - настройка суммы начисления бонусов
        - настройка таргетинга (условий) действия программы
        - настройка наград за бонусы
- Личный кабинет клиента
    - просмотр информации о клиенте
    - вступление в программы лояльности (а также выход из них)
    - просмотр программ лояльности в которые вступил
    - участие в программах (заработок бонусов и обмен их на награды)
- Продуманный механизм начисления бонусов и их обмена на награды
- Создание REST API и OpenAPI спецификации к нему

## Дополнительные фичи (если успеем)
-  Приложение будет предоставлять всю информацию о клиентах, которые зашли в программу лояльности, что может быть использовано для рассылок.
- Создание телеграмм бота взаимодействующего с REST API

## О платформе
-   💵 Наша платформа будет получать прибыль за счёт процента с каждой покупки, которая проведена через наш сервис
-   📊 Администратор платформы может просматривать всю статистику по заработку, а также зарегистрированные бизнесы и клиентов

## Механизм начисления бонусов

При каждой покупке касса предприятия печатает на чеке специальный QR-код, в который "вшита" информация о покупке и программе лояльности. При переходе на него клиенту начисляется определенное количество баллов

## Механизм обмена бонусов на награды

1. Когда у клиента уже есть баллы, он приходит в магазин
2. Кассир сканирует его уникальный QR-код, или же клиент называет уникальный номер своей виртуальной карты лояльности
3. Кассиру отображаются призы, которые может получить клиент
4. Клиент выбирает приз
5. Касса делает запрос у нашего сервиса с указанием выбранного клиентом приза
6. Наша система списывает баллы 💱

## Разделение ответственности
**Илья**:
1. Деплой.
2. Инфраструктура проекта.
3. Архитектура проекта, создание схемы БД.
4. Регистрация, аутентификация и авторизация пользователей.
5. Информация о бизнесе, статистика бизнеса.
6. Информация о клиенте, статистика клиента.
7. Вступление клиента в программу лояльности
8. Механизм начисления бонусов и их обмена на награды
9. Grafana для вывода статистики
10. Подборка программ лояльности для клиента
11. Написание телеграмм бота

**Роман**
1. CRUD над филиалами бизнеса.
2. CRUD над программами лояльности бизнеса.
    1. Настройка программ лояльности
    2. Настройка таргетинга
3. CRUD над программами лояльности клиента.
4. Написание автоматических тестов.
5. Cбор cтатистики платформы
6. Написание телеграмм бота

# Инструкция по работе

## Установить зависимости

Необходимо установить [just](https://github.com/casey/just)

```
uv pip install -e ".[dev]"
```

## Запустить проект

```
just dev
```

Чтобы остановить приложение:

```
just down
```

Чтобы очистить данные приложения:

```
just clear
```

Чтобы запустить линтеры:

```
just lint
```

## Тесты

Запуск e2e тестов

```
just e2e
```
