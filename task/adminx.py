import xadmin
from xadmin import views

from task.models import LabelClass, LabelSubClass, Task

class TaskInline(object):
    model = Task
    extra = 0

class TaskAdmin(object):
    list_display = ['name', 'creator', 'has_finished', 'creator']
    search_fields = ['name', 'creator']
    readonly_fields = ['has_finished', 'has_distributed', 'creator']

    def save_models(self):
        obj = self.new_obj
        obj.creator = self.request.user
        obj.save()

    def queryset(self):
        qs = super(TaskAdmin, self).queryset()
        user = self.request.user
        if user.is_superuser == 1:
            return qs
        qs = qs.filter(creator = user)
        return qs

class LabelClassAdmin(object):
    list_display = ['name', 'task']
    ordering = ['task']
    inlines = [TaskInline]

class LabelSubClassAdmin(object):
    list_display = ['name', 'parent', 'get_task']
    ordering = ['parent__task', 'parent']

xadmin.site.register(Task, TaskAdmin)
xadmin.site.register(LabelClass, LabelClassAdmin)
xadmin.site.register(LabelSubClass, LabelSubClassAdmin)

class GlobalSettings(object):
    # 修改title
    site_title = '图文联合标注平台'
    # 修改footer
    site_footer = '图文联合标注平台'
    # 收起菜单
    menu_style = 'accordion'
