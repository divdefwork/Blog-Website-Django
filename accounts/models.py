from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class User(AbstractUser):
    email = models.EmailField(max_length=150, unique=True,
                              error_messages={
                                  "unique": "Email має бути унікальною"},
                              verbose_name="Електронна адреса")
    profile_image = models.ImageField(null=True, blank=True,
                                      upload_to="profile_images/%Y/%m/%d/",
                                      default="profile_images/default.png",
                                      verbose_name="Зображення профілю")
    followers = models.ManyToManyField("Follow", verbose_name='Підписники')

    REQUIRED_FIELDS = ["email"]
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_profile_picture(self):
        url = ""
        try:
            url = self.profile_image.url
        except:
            url = ""
        return url


class Follow(models.Model):
    followed = models.ForeignKey(User, related_name='user_followers',
                                 on_delete=models.CASCADE,
                                 verbose_name="Підписник")
    followed_by = models.ForeignKey(User, related_name='user_follows',
                                    on_delete=models.CASCADE)
    muted = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.followed_by.username} почав стежити за" \
               f" {self.followed.username}"
