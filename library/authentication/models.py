import datetime
from django.contrib.auth.hashers import make_password
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

ROLE_CHOICES = (
    (0, 'visitor'),
    (1, 'librarian'),
)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        """
        Створіть та збережіть Користувача з вказаною адресою електронної пошти та паролем.
        """
        if not email:
            raise ValueError(('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Створіть та збережіть суперкористувача з вказаною адресою електронної пошти та паролем.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 1)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    """
        Цей клас представляє базового користувача.
    """
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    middle_name = models.CharField(max_length=20)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(default=None, max_length=255)
    created_at = models.DateTimeField(editable=False, auto_now=datetime.datetime.now())
    updated_at = models.DateTimeField(auto_now=datetime.datetime.now())
    role = models.IntegerField(choices=ROLE_CHOICES, default=0)
    is_active = models.BooleanField(default=True)
    id = models.AutoField(primary_key=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """
        Метод Magic перевизначено для відображення всієї інформації про CustomUser.
        """
        return f"{self.first_name} {self.last_name}"

    def __repr__(self):
        """
        Цей магічний метод перевизначено для показу класу та ідентифікатора об'єкта CustomUser.
        """
        return f"{CustomUser.__name__}(id={self.id})"

    def get_role_name(self):
        """
        Повертає ім'я ролі користувача.
        """
        return ROLE_CHOICES[self.role][1]

    def has_module_perms(self, app_label):
        """
        Повертає True, якщо користувач має дозволи на доступ до даної програми.
        """
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        """
        Повертає True, якщо користувач має вказаний дозвіл.
        """
        return self.is_superuser

    def get_short_name(self):
        """
        Повертає коротке ім'я користувача.
        """
        return self.first_name

    @staticmethod
    def get_by_id(user_id):
        custom_user = CustomUser.objects.filter(id=user_id).first()
        return custom_user if custom_user else None

    @staticmethod
    def get_by_email(email):
        """
        Повертає користувачеві електронну пошту
        """
        custom_user = CustomUser.objects.filter(email=email).first()
        return custom_user if custom_user else None

    @staticmethod
    def delete_by_id(user_id):
        user_to_delete = CustomUser.objects.filter(id=user_id).first()
        if user_to_delete:
            CustomUser.objects.filter(id=user_id).delete()
            return True
        return False

    @staticmethod
    def create(email, password, first_name=None, middle_name=None, last_name=None, role='0'):
        try:
            role = int(role)
        except ValueError:
            role = 0

        if len(first_name) <= 20 and len(middle_name) <= 20 and len(last_name) <= 20 and len(email) <= 100 and len(
                email.split('@')) == 2 and len(CustomUser.objects.filter(email=email)) == 0:
            hashed_password = make_password(password)  # Шифруємо пароль перед збереженням в БД
            custom_user = CustomUser(email=email, password=hashed_password, first_name=first_name,
                                     middle_name=middle_name,
                                     last_name=last_name, role=role)
            custom_user.save()
            return custom_user
        return None

    def to_dict(self):
        return {'id': self.id,
                'first_name': f'{self.first_name}',
                'middle_name': f'{self.middle_name}',
                'last_name': f'{self.last_name}',
                'email': f'{self.email}',
                'created_at': int(self.created_at.timestamp()),
                'updated_at': int(self.updated_at.timestamp()),
                'role': self.role,
                'is_active': self.is_active}

    def update(self,
               first_name=None,
               last_name=None,
               middle_name=None,
               password=None,
               role=None,
               is_active=None):
        """
        Оновлює профіль користувача у базі даних із вказаними параметрами.
        """
        user_to_update = CustomUser.objects.filter(email=self.email).first()
        if first_name != None and len(first_name) <= 20:
            user_to_update.first_name = first_name
        if last_name != None and len(last_name) <= 20:
            user_to_update.last_name = last_name
        if middle_name != None and len(middle_name) <= 20:
            user_to_update.middle_name = middle_name
        if password != None:
            user_to_update.password = password
        if role != None:
            user_to_update.role = role
        if is_active != None:
            user_to_update.is_active = is_active
        user_to_update.save()

    @staticmethod
    def get_all():
        """
        Повертає дані для json-запиту з QuerySet всіх користувачів
        """
        return CustomUser.objects.all()

    def get_role_name(self):
        """
        Повертає str ім'я ролі
        """
        return ROLE_CHOICES[self.role][1]

    def get_user_data(self):
        """
        Повертає словник, що містить дані користувача.
        """
        role_name = 'Visitor' if self.role == 0 else 'Librarian'

        return {
            'id': self.id,
            'first_name': self.first_name,
            'middle_name': self.middle_name,
            'last_name': self.last_name,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'role': role_name,
            'is_active': self.is_active,
        }

