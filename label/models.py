from django.db import models
from user.models import UserProfile
from task.models import DataItem, Task, LabelSubClass
from datetime import datetime

# Create your models here.

class LabelTask(models.Model):
    tagger = models.ForeignKey(UserProfile, verbose_name='标注者', on_delete=models.CASCADE)
    data_item = models.ForeignKey(DataItem, verbose_name='数据', on_delete=models.CASCADE)
    has_done = models.IntegerField(default=0,choices=((0, '未标注'), (1, '跳过'), (2, '完成')), verbose_name='是否完成')

    class Meta:
        verbose_name = '任务分配'
        verbose_name_plural = '任务分配'

class Labelresult(models.Model):
    mid = models.CharField(max_length=50, verbose_name='自定义id')
    img_name = models.ImageField(verbose_name='图片文件', blank=True, null=True)
    txt = models.TextField(verbose_name='文本')
    task = models.ForeignKey(Task, verbose_name='任务', on_delete=models.CASCADE)
    tagger = models.ForeignKey(UserProfile, verbose_name='标注者', on_delete=models.CASCADE)
    label = models.ForeignKey(LabelSubClass, verbose_name='标注结果', on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name='标记时间', default=datetime.now)
    remark = models.TextField(verbose_name='备注', null=True, blank=True)

    class Meta:
        verbose_name = '标注记录'
        verbose_name_plural = verbose_name

