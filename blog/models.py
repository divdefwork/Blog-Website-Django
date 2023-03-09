from ckeditor.fields import RichTextField
from django.db import models
from django.utils.text import slugify

from accounts.models import User
from .slugs import generate_unique_slug
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150, unique=True,
                             verbose_name="Заголовок")
    slug = models.SlugField(null=True, blank=True,
                            unique=True, db_index=True,
                            verbose_name="URL")
    created_date = models.DateField(auto_now_add=True,
                                    verbose_name="Дата створення")

    class Meta:
        """ Мета для іменування в адміністраторі django описує
            модель, якщо об'єкт є одиничним або множина
        """
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('category_blogs', kwargs={'slug': self.slug})


class Tag(models.Model):
    title = models.CharField(max_length=150,
                             verbose_name="Заголовок")
    slug = models.SlugField(null=True, blank=True,
                            unique=True, db_index=True,
                            verbose_name="URL")
    created_date = models.DateField(auto_now_add=True,
                                    verbose_name="Дата створення")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tag_blogs', kwargs={'slug': self.slug})


class Blog(models.Model):
    user = models.ForeignKey(User, related_name='user_blogs',
                             on_delete=models.CASCADE,
                             verbose_name="Користувач")
    category = models.ForeignKey(Category, related_name='category_blogs',
                                 on_delete=models.CASCADE,
                                 verbose_name="Категорія")
    tags = models.ManyToManyField(Tag, related_name='tag_blogs', blank=True,
                                  verbose_name="Теги")
    likes = models.ManyToManyField(User,
                                   related_name='user_likes', blank=True,
                                   verbose_name="Подобається")
    title = models.CharField(max_length=250,
                             verbose_name="Заголовок")
    slug = models.SlugField(null=True, blank=True,
                            unique=True, db_index=True,
                            verbose_name="URL")
    banner = models.ImageField(upload_to='blog_banners/%Y/%m/%d/',
                               verbose_name="Банер")
    description = RichTextField(verbose_name="Опис")
    created_date = models.DateField(auto_now_add=True,
                                    verbose_name="Дата створення")

    class Meta:
        verbose_name = "Блог"
        verbose_name_plural = "Блоги"
        ordering = ['created_date']

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        updating = self.pk is not None

        if updating:
            self.slug = generate_unique_slug(self, self.title, update=True)
            super().save(*args, **kwargs)
        else:
            self.slug = generate_unique_slug(self, self.title)
            super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_details', kwargs={'slug': self.slug})


class Comment(models.Model):
    user = models.ForeignKey(User, related_name='user_comments',
                             on_delete=models.CASCADE,
                             verbose_name="Користувач")
    blog = models.ForeignKey(Blog, related_name='blog_comments',
                             on_delete=models.CASCADE,
                             verbose_name="Блог")
    text = models.TextField(verbose_name="Зміст")
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name="Дата створення")

    class Meta:
        verbose_name = "Коментар"
        verbose_name_plural = "Коментарі"

    def __str__(self) -> str:
        return self.text


class Reply(models.Model):
    user = models.ForeignKey(User, related_name='user_replies',
                             on_delete=models.CASCADE,
                             verbose_name="Користувач")
    comment = models.ForeignKey(Comment, related_name='comment_replies',
                                on_delete=models.CASCADE,
                                verbose_name="Коментар")
    text = models.TextField(verbose_name="Текст відповіді")
    created_date = models.DateTimeField(auto_now_add=True,
                                        verbose_name="Дата створення")

    class Meta:
        verbose_name = "Відповідь"
        verbose_name_plural = "Відповіді"

    def __str__(self) -> str:
        return self.text
