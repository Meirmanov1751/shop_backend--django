from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

from general.models import MediaFile
from notification.tasks import send_notification_to_user


class MyUserManager(BaseUserManager):
    def _create_user(self, email_or_phone, password,
                     is_staff, is_superuser, **extra_fields):
        """ Create EmailPhoneUser with the given email or phone and password.
        :param str email_or_phone: user email or phone
        :param str password: user password
        :param bool is_staff: whether user staff or not
        :param bool is_superuser: whether user admin or not
        :return settings.AUTH_USER_MODEL user: user
        :raise ValueError: email or phone is not set
        :raise NumberParseException: phone does not have correct format
        """
        if not email_or_phone:
            raise ValueError('The given email_or_phone must be set')

        if "@" in email_or_phone:
            email_or_phone = self.normalize_email(email_or_phone)
            username, email, phone = (email_or_phone, email_or_phone, None)
        else:
            username, email, phone = (email_or_phone, None, email_or_phone)
        now = timezone.now()
        is_active = extra_fields.pop("is_active", True)
        user = self.model(
            username=username,
            email=email,
            phone=phone,
            is_admin=is_staff,
            is_active=is_active,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email_or_phone, password=None, **extra_fields):
        return self._create_user(email_or_phone, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        print(username, password)
        return self._create_user(username, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser):
    class ROLES:
        MANAGEMENT_COMPANY = 'management_company'
        USER = 'user'
        SUPER_ADMIN = 'super_admin'
        MASTER = 'master'
        ROLES_CHOICES = ((MANAGEMENT_COMPANY, "Управляющая компания"), (USER, "Пользователь"), (SUPER_ADMIN, 'Супер '
                                                                                                             'админ'),
                         (MASTER, 'Работник'))

    username = models.CharField(max_length=1000, unique=True, null=True, blank=True)
    password = models.CharField("password", max_length=128, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=300, null=True, blank=True)
    avatar = models.ForeignKey(MediaFile, on_delete=models.CASCADE, null=True)
    fullname = models.CharField(max_length=300, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    role = models.CharField(default=ROLES.USER, choices=ROLES.ROLES_CHOICES, max_length=300)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return "%s %s" % (self.username, self.fullname)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_super_admin(self):
        return self.role == User.ROLES.SUPER_ADMIN

    @property
    def is_user(self):
        return self.role == User.ROLES.USER

    @property
    def is_management_company(self):
        management_company = self.managementcompany_set.all()
        return self.role == User.ROLES.MANAGEMENT_COMPANY and management_company.exists()

    def send_notification(self, title, body, url=None, extra={}):
        send_notification_to_user.delay(self.id, title, body, url, extra)

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
