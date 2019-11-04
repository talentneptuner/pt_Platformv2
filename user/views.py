from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from pure_pagination import PageNotAnInteger, Paginator, EmptyPage

from task.views import Task


# Create your views here.
class LoginView(View):
    '''
    登录逻辑
    '''
    def get(self, request):
        return render(request, 'login.html', {'info':'此系统在火狐浏览器上存在问题，请勿使用火狐浏览器登录，推荐使用chrome和edge'})

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user_type = request.POST.get("usertype")
        user = authenticate(username=username, password=password)
        if user:
            if int(user_type) == 1:
                if user.is_staff:
                    login(request, user)
                    from django.urls import reverse
                    return HttpResponseRedirect(reverse('admin_index'))
                else:
                    return render(request, 'login.html', {'info': '没有权限'})
            else:
                login(request, user)
                from django.urls import reverse
                return HttpResponseRedirect(reverse('user_index'))
        return render(request, 'login.html', {'info':'密码或用户名不正确'})



class AdminIndex(View):
    def get(self,request):
        user = request.user
        if not user.is_staff:
            return render(request, 'login.html')
        tasks = user.get_tasks_defined()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(tasks, 10, request=request)
        tasks = p.page(page)
        return render(request, 'tasks_admin.html', {'tasks': tasks})

class UserIndex(View):
    def get(self, request):
        user = request.user
        tasks = (user.get_tasks_unfinished())
        task_idx = set([list(t.values())[0] for t in tasks])
        tasks = Task.objects.filter(id__in=task_idx, has_finished=False)
        task_status = []
        for task in tasks:
            task_status.append([task, user.get_count_unfinished(task.id), user.get_count(task.id)])
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(task_status, 10, request=request)
        task_status = p.page(page)
        return render(request, 'tasks_user.html', {'tasks': task_status})


class LogoutView(View):
    """登出逻辑"""

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("login"), {})







