from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.crypto import get_random_string
from django.utils.translation import ugettext_lazy as _


class MainUserManager(BaseUserManager):
    """
    Main user manager
    """

    def create_user(self, email, password=None, is_active=None, **kwargs):
        """
        Creates and saves a user with the given username and password
        """
        if not email:
            raise ValueError('Users must have an username')
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        if is_active is not None:
            user.is_active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given username and password
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.is_moderator = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Author(AbstractUser):
    username = None
    first_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Имя')
    last_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Почта')
    password = models.CharField(blank=True, null=True, max_length=500, verbose_name='Пароль')
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    verified = models.BooleanField(default=False)

    objects = MainUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    @property
    def is_authenticated(self):
        return True

    def full(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
        }


class ConfirmCode(models.Model):
    code = models.CharField(max_length=6)
    confirm = models.BooleanField(default=False)
    customer = models.ForeignKey(Author, related_name = 'codes' , on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Код подтверждения'
        verbose_name_plural = 'Коды подтверждения'

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(length=6)
        super(ConfirmCode, self).save(*args, **kwargs)
