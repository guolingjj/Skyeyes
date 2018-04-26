from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
# Create your models here.
class Host(models.Model):
    '''主机信息'''
    host_name=models.CharField(max_length=64)
    ip_addr=models.GenericIPAddressField(unique=True)
    port=models.PositiveSmallIntegerField(default=22)
    idc=models.ForeignKey("IDC",on_delete=models.CASCADE)
    enabled=models.BooleanField(default=False)
    def __str__(self):
        return self.host_name

class IDC(models.Model):
    '''机房信息'''
    idc_name=models.CharField(max_length=64,unique=True)
    def __str__(self):
        return self.idc_name

class HostGroup(models.Model):
    '''主机组'''
    name=models.CharField(max_length=64,unique=True)
    bind_hosts=models.ManyToManyField("BindHost",blank=True,null=True)
    def __str__(self):
        return self.name

class UserProfileManager(BaseUserManager):
    def create_user(self, email, name, password=None, ):
        """
        Creates and saves a User with the given email,  and password.
        """
        if not email:
            raise ValueError('Users must have an email addres')

        user = self.model(
            email=self.normalize_email(email),
            name=name,


        )

        user.set_password(password)

        self.is_active=True
        user.save(using=self._db)
        return user

    def create_superuser(self, email,name, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            name=name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class UserProfile(AbstractBaseUser,PermissionsMixin):
    '''堡垒机账户'''
    email = models.EmailField(
        verbose_name='邮箱',
        max_length=255,
        unique=True,

    )
    password = models.CharField(_('password'), max_length=128)
    name=models.CharField(max_length=32,verbose_name='用户姓名')
    bind_hosts=models.ManyToManyField('BindHost')
    host_group=models.ManyToManyField('HostGroup')
    is_active = models.BooleanField(default=True,verbose_name='是否活跃')
    is_admin = models.BooleanField(default=False,verbose_name='是否是管理员')
    objects = UserProfileManager()
    USERNAME_FIELD = 'email'#以xx字段为用户名
    REQUIRED_FIELDS = ['name']#那些字段是必须

    def __str__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    class Meta:
        verbose_name="堡垒机账户"
        permissions=(
                     )

class HostUser(models.Model):
    """主机登录账户"""
    auth_type_choices=((0,'ssh-password'),(1,'ssh-key'))
    auth_type=models.PositiveSmallIntegerField(choices=auth_type_choices,default=0)
    username=models.CharField(max_length=64)
    password=models.CharField(max_length=128,blank=True,null=True)
    def __str__(self):
        return self.username
    class Meta:
        unique_together=('auth_type','username','password')

class BindHost(models.Model):
    host=models.ForeignKey('Host',on_delete=models.CASCADE)
    host_user=models.ForeignKey('HostUser',on_delete=models.CASCADE)
    def __str__(self):
        return '%s:%s'%(self.host,self.host_user)
    class Meta:
        unique_together=('host','host_user')

class SeesionLog(models.Model):
    '''存储session日志'''
    user=models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    bind_host=models.ForeignKey('BindHost',on_delete=models.CASCADE)
    session_tag=models.CharField(max_length=128,unique=True)
    date=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.session_tag


class Task(models.Model):
    '''批量任务'''
    task_type_choices=(('cmd','批量命令'),
                       ('file_transfer','文件传输')
                       )
    task_type=models.CharField(max_length=16,choices=task_type_choices)
    content=models.CharField(max_length=255,verbose_name='任务内容')
    user=models.ForeignKey('UserProfile',on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s %s'%(self.task_type,self.content)


class TaskLogDetail(models.Model):
    '''存储主任务的结果'''
    task=models.ForeignKey('Task',on_delete=models.CASCADE)
    bind_host=models.ForeignKey('BindHost',on_delete=models.CASCADE)
    run_result=models.TextField(verbose_name='执行结果',)
    status_choices=((0,'running'),
                    (1,'sucess'),
                    (2,'faile'),
                    (3,'timeout'),
                    )
    status=models.SmallIntegerField(choices=status_choices,default=0)
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s %s'%(self.task,self.bind_host)