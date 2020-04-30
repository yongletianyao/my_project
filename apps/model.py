# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)

class MyUserManager(BaseUserManager):
    def create_user(self, username1,date_of_birth ,password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username1:
            raise ValueError('Users must have an mobile')
        user = self.model(
            username1 = self.normalize_email(username1),
            date_of_birth =date_of_birth,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username1,date_of_birth,password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(username1,
                                date_of_birth=date_of_birth,
                                password=password,
                                )
        user.is_staff=True
        user.is_admin = True
        user.is_superuser=True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username1 = models.CharField(
        verbose_name='用户名', max_length=11, unique=True
    )

    date_of_birth = models.DateField()
    is_staff = models.BooleanField(verbose_name='staff status', default=False)
    is_active = models.BooleanField(verbose_name='active', default=True)
    is_admin = models.BooleanField(default=False)
    object = MyUserManager()

    USERNAME_FIELD = 'username1'
    REQUIRED_FIELDS = ['date_of_birth']
    # REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return self.username1

    def get_short_name(self):
        # The user is identified by their email address
        return self.username1

    def __unicode__(self):
        return "{0}, {1}".format(self.id, self.username1)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

class DeInfo(models.Model):
    de_id = models.IntegerField(primary_key=True)
    de_address = models.IntegerField()
    de_status = models.IntegerField()
    de_failuertimes = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'de_info'


class Warning(models.Model):
    w_time = models.DateTimeField()
    w_id = models.IntegerField()
    tem = models.IntegerField()
    img = models.ImageField(upload_to='img')
    iname = models.CharField(max_length=20)
    class Meta:
        managed = False
        db_table = 'warning'
# class img(models.Model):
#     img = models.ImageField(upload_to='img')
#     iname = models.CharField(max_length=20)
#
#     def __str__(self):
#     # 在Python3中使用 def __str__(self):
#         return self.name

