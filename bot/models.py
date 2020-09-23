from django.db import models


# Create your models here.

# 机器人配置
class Bot(models.Model):
    botName = models.CharField(unique=True, max_length=100)
    botType = models.IntegerField(default=0)
    botQQ = models.CharField(max_length=100)
    botPwd = models.CharField(max_length=100)
    botPermission = models.IntegerField(default=0)
    botCode = models.TextField
    userId = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'bit'
