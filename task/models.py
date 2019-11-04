from django.db import models
from user.models import UserProfile
from datetime import datetime

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=200, verbose_name='任务名称')
    has_finished = models.BooleanField(default=False, verbose_name='是否完成')
    creator = models.ForeignKey(UserProfile, blank=True, null=True, verbose_name='创建者', on_delete=models.CASCADE)
    has_distributed = models.BooleanField(default=False, verbose_name='是否分配')
    max_label_nums = models.IntegerField(default=3, verbose_name='最大标注数目')

    def __str__(self):
        return self.name

    def get_classes(self):
        return self.labelclass_set.all()

    def get_sub_classes(self):
        label_classes = self.labelclass_set.all()
        if not label_classes:
            return False
        for label in label_classes:
            if not label.labelsubclass_set.all():
                return False
        return True

    def get_data(self):
        data =  self.dataitem_set().all()
        return data


    class Meta:
        verbose_name = '标注任务'
        verbose_name_plural = verbose_name

class LabelClass(models.Model):
    name = models.CharField(max_length=50, verbose_name='大类标签')
    task = models.ForeignKey(Task, blank=True, null=True, verbose_name='任务', on_delete=models.CASCADE)

    def get_subclasses(self):
        return self.labelsubclass_set.all()

    class Meta:
        verbose_name = '大类标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return  self.name

class LabelSubClass(models.Model):
    name = models.CharField(max_length=50, verbose_name='子类标签')
    desc = models.CharField(max_length=500, verbose_name='说明', blank=True,null=True)
    parent = models.ForeignKey(LabelClass, verbose_name='父类', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '子类标签'
        verbose_name_plural = verbose_name

    def get_task(self):
        return self.parent.task

class DataItem(models.Model):
    mid = models.CharField(max_length=50, verbose_name='自定义id')
    img_name = models.CharField(max_length=50, verbose_name='图片文件', blank=True, null=True)
    txt = models.TextField(verbose_name='文本')
    task = models.ForeignKey(Task, verbose_name='任务', on_delete=models.CASCADE)
    time = models.DateTimeField(verbose_name='标记时间', default=datetime.now)

    class Meta:
        verbose_name = '待标注数据'
        verbose_name_plural = verbose_name
