Тестовое задание: Разработка микросервиса для подготовки дайджестов контента

Требования к микросервису

1. Получение запроса на формирование дайджеста: Микросервис должен уметь принимать запросы от основного приложения на формирование дайджеста для пользователя, идентифицируемого по уникальному ID.

2. Определение подписок пользователя: После получения запроса, микросервис должен определить источники, на которые подписан пользователь, используя информацию о подписках пользователя.

3. Сбор постов из подписок: Зная подписки пользователя, микросервис должен собирать посты из этих источников. Подумайте о нём как о "сканере" подписок пользователя в поисках нового контента.

4. Фильтрация постов: Из собранных постов отфильтруйте те, которые не соответствуют интересам пользователя или недостаточно популярны. Микросервис должен использовать определенные критерии для фильтрации.

5. Создание дайджеста: После фильтрации, оставшиеся посты упаковываются в дайджест. Дайджест - это совокупность постов, отобранных для пользователя.

6. Отправка дайджеста: Сформированный дайджест возвращается в главное приложение, которое предоставит его пользователю.
