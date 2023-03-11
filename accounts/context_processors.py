"""
    Назва модуля: user_notifications

    Опис модуля:
    Модуль user_notifications містить функцію user_notifications, яка повертає
    контекст, що містить повідомлення користувача та кількість непрочитаних
    повідомлень для відображення на сторінках Django - проєкту.

    Функції та класи в модулі:

    user_notifications(request): Функція, яка приймає об'єкт запиту request
    та повертає словник context, що містить два ключі: notifications та unseen.
    Ключ notifications містить список повідомлень Notification, які були
    створені для поточного користувача, відсортований в порядку спадання
    за датою створення.
    Ключ unseen містить кількість непрочитаних повідомлень.

    Notification: Модель Django, що представляє повідомлення користувача.
    Кожне повідомлення містить заголовок title, текст повідомлення message,
    дату та час створення created_date, та прапорець is_seen, що позначає,
    чи було повідомлення прочитано користувачем.

    Залежності модуля:
    Модуль user_notifications залежить від моделі Notification, що знаходиться
    в іншому модулі.
"""

from notification.models import Notificaiton


def user_notifications(request):
    """ Функція повертає словник з контекстом для відображення сповіщень
        для залогіненого користувача.
        Функція перевіряє, чи є користувач залогіненим, і якщо так,
        то вибирає всі сповіщення, пов'язані з цим користувачем,
        відсортовані за датою створення.
        Далі вона вибирає всі непрочитані сповіщення і додає їх кількість у
        словник контексту.
        Загалом, ця функція допомагає показувати сповіщення
        для залогіненого користувача на його сторінці.
    """
    context = {}

    if request.user.is_authenticated:
        notifications = Notificaiton.objects.filter(
            user=request.user).order_by('-created_date')
        unseen = notifications.exclude(is_seen=True)
        context['notifications'] = notifications
        context['unseen'] = unseen.count()

    return context
