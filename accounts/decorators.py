""" Модуль not_logged_in_required

    - Цей модуль містить декоратор not_logged_in_required, який перенаправляє
    користувачів на головну сторінку, якщо вони авторизовані, інакше передає
    управління функції-параметру.

    - Декоратор not_logged_in_required приймає один аргумент — функцію-параметр
    view_function, яку потрібно декорувати. Функція-параметр приймає об'єкт
    запиту request, а також будь-яку кількість позиційних
    і іменованих аргументів.

    - Якщо користувач, який робить запит, авторизований, то декоратор
    перенаправляє його на головну сторінку сайту за допомогою функції
    redirect з бібліотеки django.shortcuts. Якщо користувач не авторизований,
    то управління передається функції-параметру view_function.
"""
from django.shortcuts import redirect


def not_logged_in_required(view_function):
    """ Функція "not_logged_in_required" перевіряє,
        чи є користувач автентифікованим. Якщо користувач не автентифікований,
        вона передає управління далі до вхідної функції.
        Якщо користувач автентифікований,
        вона перенаправляє його на сторінку "home".
    """

    def wrapper(request, *args, **kwarsg):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_function(request, *args, **kwarsg)

    return wrapper
