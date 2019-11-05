import random
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

from django.views.generic.base import View

from task.models import Task, DataItem, LabelSubClass
from user.models import UserProfile
from label.models import LabelTask, Labelresult

class DistributeTaskView(View):
    '''
    分配任务
    '''
    def get(self, request, task_id):
        if not (request.user.is_authenticated and request.user.is_staff):
            return render(request, 'login.html')
        task = Task.objects.get(id=task_id)
        users = UserProfile.objects.filter(is_staff=False)
        return render(request, 'distributetask.html', {'task_id':task.id, 'users':users})

    def post(self, request, task_id):
        '''
        m个数据，n个人，k组，把m个数据分为k份，n个人分为k份，分别组合后等分
        :param request:
        :param task_id:
        :return:
        '''
        if not (request.user.is_authenticated and request.user.is_staff):
            return render(request, 'login.html')
        user_idx = request.POST.getlist('users[]')
        num_per = int(request.POST.get('num_per'))
        users = list(UserProfile.objects.filter(id__in=user_idx))
        task = Task.objects.get(id=task_id)
        if not task.get_sub_classes():
            return HttpResponse('{"status":"fail", "info":"类别信息不完整"}', content_type='application/json')
        data = DataItem.objects.filter(task=task)
        if not data:
            return HttpResponse('{"status":"fail", "info":"标注数据未添加"}', content_type='application/json')
        user2count = {}
        print(len(data))
        task_count = len(data) * num_per
        tasks = []
        if (task_count % len(users) == 0):
            max_num = task_count / len(users)
        else:
            max_num = task_count // len(users) + 1
        for user in users:
            user2count[user.username] = 0

        for i, item in enumerate(data):
            if len(users) > num_per:
                choices = random.sample(users, num_per)
            else:
                choices = users
            for user in choices:
                # if user2count[user.username] < max_num:
                label_task = LabelTask()
                label_task.data_item = item
                label_task.tagger = user
                tasks.append(label_task)
                user2count[user.username] += 1
                # if user2count[user.username] >= max_num:
                #     users.remove(user)
                print(user2count)
        LabelTask.objects.bulk_create(tasks)
        task.has_distributed = True
        task.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')

class LabelView(View):
    def get(self, request, task_id):
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        task = Task.objects.get(id=task_id)
        user = request.user
        try:
            label_task = LabelTask.objects.filter(data_item__task=task, has_done=0, tagger=user)[0]
            has_skipped = 0
        except:
            # 已经查不到未标注数据，查询跳过的数据
            try:
                label_task = LabelTask.objects.filter(data_item__task=task, has_done=1, tagger=user)[0]
                has_skipped = 1
            except:
                return HttpResponseRedirect(reverse('user_index'))
        info =  label_task.data_item
        label_classes = task.get_classes()
        unfinished_count = user.get_count_unfinished(task_id)
        count = user.get_count(task_id)
        return render(request, 'label.html', {'id': label_task.id, 'info':info, 'label_classes':label_classes,
                                               'uc':unfinished_count, 'count':count, 'task':task, 'has_skipped':has_skipped})

class NextView(View):
    def post(self, request):
        if not request.user.is_authenticated:
            return render(request, 'login.html')
        user = request.user
        task_id = request.POST.get('task_id')
        label_task_id = request.POST.get('label_task_id')
        remarks = request.POST.get('remarks')
        type = int(request.POST.get('type'))
        label_task = LabelTask.objects.get(id=label_task_id)
        label_task.has_done = type
        label_task.save()
        task = Task.objects.get(id=task_id)
        if type == 2:
            labels = request.POST.getlist('labels[]')
            for label in labels:
                label_result = Labelresult()
                label_result.mid = label_task.data_item.mid
                label_result.txt = label_task.data_item.txt
                label_result.img_name = label_task.data_item.img_name
                label_result.tagger = user
                label_result.remark = remarks
                label_result.label = LabelSubClass.objects.get(id=label)
                label_result.task = task
                label_result.save()

        try:
            label_task = LabelTask.objects.filter(data_item__task=task, has_done=0, tagger=user)[0]
            has_skipped = 0
        except:
            # 已经查不到未标注数据，查询跳过的数据
            try:
                label_task = LabelTask.objects.filter(data_item__task=task, has_done=1, tagger=user)[0]
                has_skipped = 1
            except:
                return HttpResponse('{"status":"finished"}', content_type='application/json')
        info =  label_task.data_item
        unfinished_count = user.get_count_unfinished(task_id)
        msg = {'txt':info.txt, 'image':info.img_name, 'uc':unfinished_count, 'id': label_task.id, 'has_skipped':has_skipped}
        return HttpResponse(json.dumps(msg), content_type='application/json')

class CloseTaskView(View):
    def get(self,request,  task_id):
        if not (request.user.is_authenticated and request.user.is_staff):
            return render(request, 'login.html')
        task = Task.objects.get(id=task_id)
        task.has_finished=True
        task.save()
        return HttpResponseRedirect(reverse('admin_index'))








