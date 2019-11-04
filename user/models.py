from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserProfile(AbstractUser):

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return self.username

    def get_tasks_defined(self):
        return self.task_set.all()

    def get_tasks_undistributed(self):
        return self.task_set.filter(has_distributed=False)

    def get_tasks_unfinished(self):
        all_tasks =  list(self.labeltask_set.values('data_item__task_id'))
        return all_tasks

    def get_count_unfinished(self, id):
        count = self.labeltask_set.filter(data_item__task_id=id, has_done=2).count()
        return count

    def get_count(self, id):
        count = self.labeltask_set.filter(data_item__task_id=id).count()
        return count
