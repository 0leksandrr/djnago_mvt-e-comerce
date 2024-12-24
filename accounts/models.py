from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class MyAccountManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('Пользователь должен иметь электронный адрес')
        if not username:
            raise ValueError('Пользователь должен иметь имя пользователя')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50, verbose_name='Імя')
    last_name = models.CharField(max_length=50, verbose_name='Прізвище')
    username = models.CharField(max_length=50, unique=True, verbose_name='Імя користувача')
    email = models.EmailField(max_length=100, unique=True, verbose_name='Електронна пошта')
    phone_number = models.CharField(max_length=50, verbose_name='Телефон')

    # required
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата реєстрації')
    last_login = models.DateTimeField(auto_now_add=True, verbose_name='Останній вхід')
    is_admin = models.BooleanField(default=False, verbose_name='Адміністратор')
    is_staff = models.BooleanField(default=False, verbose_name='Персонал')
    is_active = models.BooleanField(default=False, verbose_name='Активний')
    is_superuser = models.BooleanField(default=False, verbose_name='Суперкористувач')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def full_name(self):
        return f'{self.last_name} {self.first_name}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

    class Meta:
        verbose_name = 'Обліковий запис'
        verbose_name_plural = 'Облікові записи'


class UserProfile(models.Model):
    objects = models.Manager()

    user = models.OneToOneField(Account, on_delete=models.CASCADE, verbose_name='Користувач')
    address_line_1 = models.CharField(blank=True, max_length=100, verbose_name='Адреса 1')
    address_line_2 = models.CharField(blank=True, max_length=100, verbose_name='Адреса 2')
    profile_picture = models.ImageField(blank=True, upload_to='userprofile', verbose_name='Фото профілю')
    city = models.CharField(blank=True, max_length=20, verbose_name='Місто')
    region = models.CharField(blank=True, max_length=20, verbose_name='Регіон')
    country = models.CharField(blank=True, max_length=20, verbose_name='Країна')

    def __str__(self):
        return self.user.first_name

    def full_address(self):
        return f'{self.address_line_1}; {self.address_line_2}'

    class Meta:
        verbose_name = 'Профіль користувача'
        verbose_name_plural = 'Профілі користувачів'
