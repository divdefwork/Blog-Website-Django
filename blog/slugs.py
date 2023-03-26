import random
import string

from django.utils.text import slugify


def generate_unique_slug(instance, base_title, new_slug=False, update=False):
    """
        Функція generate_unique_slug генерує унікальний slug для
        елементів моделі Django на основі назви. Ця функція приймає
        чотири аргументи:

        - instance: екземпляр моделі, для якої генерується slug.
        - base_title: назва, на основі якої генерується slug.
        - new_slug (необов'язково): новий slug, який буде використовуватися
        замість того, що згенерувала функція.
        - update (необов'язково): прапорець, що вказує, чи оновлюється
        наявний slug.

        Функція спочатку генерує slug з base_title. Якщо передано аргумент
        new_slug, він використовується замість згенерованого. Якщо передано
        аргумент update, функція перевіряє, чи існує унікальний slug
        згідно з новою назвою. Якщо update встановлено в True,
        функція виключає поточний елемент моделі з перевірки
        унікальності slug. Якщо slug вже існує, функція генерує рандомну
        стрічку з 4 літер, і створює новий slug, що складається з base_title
        та рандомної стрічки. Функція рекурсивно викликається з новим slug,
        якщо новий slug також існує. Якщо унікальний slug вільний,
        функція повертає його.
    """
    slug = slugify(base_title)
    model = instance.__class__

    if new_slug:
        slug = new_slug

    if update:
        slug_exists = model.objects.filter(
            slug__icontains=slug
        ).exclude(pk=instance.pk)
    else:
        slug_exists = model.objects.filter(
            slug__icontains=slug
        ).exists()

    if slug_exists:
        random_string = "".join(random.choices(string.ascii_lowercase, k=4))
        new = slugify(base_title + '-' + random_string)
        return generate_unique_slug(
            instance,
            base_title,
            new_slug=new
        )

    return slug
