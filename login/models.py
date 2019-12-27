from django.db import models


# Create your models here.

class User(models.Model):
    gender = (
        ('male', "男"),
        ('female', "女"),
    )

    name = models.CharField('姓名', max_length=128, unique=True)
    password = models.CharField('密码', max_length=256)
    email = models.EmailField('邮箱', unique=True)
    sex = models.CharField('性别', max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField('创建时间', auto_now_add=True)
    has_confirmed = models.BooleanField('是否确认邮件', default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "注册成员"
        verbose_name_plural = "注册成员"


class ConfirmString(models.Model):
    code = models.CharField('确认码', max_length=256)
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    c_time = models.DateTimeField('注册时间', auto_now_add=True)

    def __str__(self):
        return self.user.name + ":  " + self.code

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "邮件确认码"
        verbose_name_plural = "邮件确认码"
